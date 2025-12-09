#!/usr/bin/env python3
"""
Monitor The Ruckus - Enhanced Network Health Monitor
Real-time monitoring with ping latency, packet loss, jitter, quality scores, and alerts
"""

import subprocess
import sys
import time
import statistics
from datetime import datetime
from typing import Optional, Dict, List
import os
import re
from collections import deque


class NetworkMonitor:
    """Enhanced real-time network health monitoring"""

    def __init__(self, interface: Optional[str] = None, targets: Dict[str, str] = None):
        self.interface = interface
        self.targets = targets or {}
        self.running = False

        # Historical data (last 60 samples = ~1 minute at 1 sec interval)
        self.history_size = 60
        self.bandwidth_history = deque(maxlen=self.history_size)
        self.latency_history = {name: deque(maxlen=self.history_size) for name in self.targets}
        self.packet_loss_history = {name: deque(maxlen=self.history_size) for name in self.targets}

        # Previous stats for bandwidth calculation
        self.prev_stats = None
        self.prev_time = None

        # Alert thresholds
        self.alert_thresholds = {
            'latency_ms': 100,
            'packet_loss_pct': 5,
            'jitter_ms': 50,
            'quality_score': 70
        }

    def detect_interface(self):
        """Auto-detect the primary network interface"""
        try:
            result = subprocess.run(
                ["ip", "route", "show", "default"],
                capture_output=True, text=True, check=True
            )
            words = result.stdout.split()
            if "dev" in words:
                dev_idx = words.index("dev")
                if dev_idx + 1 < len(words):
                    return words[dev_idx + 1]
        except Exception:
            pass
        return "eth0"

    def get_interface_stats(self):
        """Get current interface statistics"""
        if not self.interface:
            self.interface = self.detect_interface()

        try:
            with open('/proc/net/dev', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if self.interface in line:
                        parts = line.split()
                        return {
                            'rx_bytes': int(parts[1]),
                            'rx_packets': int(parts[2]),
                            'rx_errors': int(parts[3]),
                            'rx_dropped': int(parts[4]),
                            'tx_bytes': int(parts[9]),
                            'tx_packets': int(parts[10]),
                            'tx_errors': int(parts[11]),
                            'tx_dropped': int(parts[12])
                        }
        except Exception as e:
            return None

    def calculate_bandwidth(self, current_stats):
        """Calculate bandwidth usage"""
        if not self.prev_stats or not self.prev_time:
            self.prev_stats = current_stats
            self.prev_time = time.time()
            return {'download_mbps': 0, 'upload_mbps': 0, 'total_mbps': 0}

        time_diff = time.time() - self.prev_time
        if time_diff == 0:
            return {'download_mbps': 0, 'upload_mbps': 0, 'total_mbps': 0}

        rx_diff = current_stats['rx_bytes'] - self.prev_stats['rx_bytes']
        tx_diff = current_stats['tx_bytes'] - self.prev_stats['tx_bytes']

        download_mbps = (rx_diff * 8) / (time_diff * 1_000_000)
        upload_mbps = (tx_diff * 8) / (time_diff * 1_000_000)
        total_mbps = download_mbps + upload_mbps

        self.prev_stats = current_stats
        self.prev_time = time.time()

        return {
            'download_mbps': download_mbps,
            'upload_mbps': upload_mbps,
            'total_mbps': total_mbps
        }

    def ping_target(self, ip: str, count: int = 5):
        """Ping target and return latency, packet loss, and jitter"""
        try:
            result = subprocess.run(
                ['ping', '-c', str(count), '-i', '0.2', '-W', '1', ip],
                capture_output=True, text=True, timeout=10
            )

            output = result.stdout

            # Parse packet loss
            loss_match = re.search(r'(\d+)% packet loss', output)
            packet_loss = int(loss_match.group(1)) if loss_match else 100

            # Parse latency stats
            stats_match = re.search(r'rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+)', output)
            if stats_match:
                min_ms = float(stats_match.group(1))
                avg_ms = float(stats_match.group(2))
                max_ms = float(stats_match.group(3))
                mdev_ms = float(stats_match.group(4))  # Standard deviation (jitter)

                return {
                    'success': True,
                    'min_ms': min_ms,
                    'avg_ms': avg_ms,
                    'max_ms': max_ms,
                    'jitter_ms': mdev_ms,
                    'packet_loss_pct': packet_loss
                }
            else:
                return {
                    'success': False,
                    'packet_loss_pct': 100
                }
        except Exception:
            return {
                'success': False,
                'packet_loss_pct': 100
            }

    def calculate_quality_score(self, latency_ms, packet_loss_pct, jitter_ms):
        """Calculate connection quality score (0-100)"""
        # Start with perfect score
        score = 100

        # Deduct for latency (exponential penalty)
        if latency_ms > 20:
            score -= min(30, (latency_ms - 20) * 0.5)

        # Deduct for packet loss (severe penalty)
        score -= packet_loss_pct * 5

        # Deduct for jitter
        if jitter_ms > 10:
            score -= min(20, (jitter_ms - 10) * 0.5)

        return max(0, min(100, score))

    def get_quality_status(self, score):
        """Get quality status based on score"""
        if score >= 85:
            return "🟢 EXCELLENT"
        elif score >= 70:
            return "🟡 GOOD"
        elif score >= 50:
            return "🟠 FAIR"
        elif score >= 30:
            return "🔴 POOR"
        else:
            return "⚫ CRITICAL"

    def check_tcp_retransmits(self):
        """Check TCP retransmit rate"""
        try:
            result = subprocess.run(
                ['netstat', '-s'],
                capture_output=True, text=True
            )
            output = result.stdout

            # Parse TCP stats
            segments_sent = 0
            segments_retransmitted = 0

            for line in output.split('\n'):
                if 'segments sent out' in line.lower():
                    match = re.search(r'(\d+)', line)
                    if match:
                        segments_sent = int(match.group(1))
                elif 'segments retransmitted' in line.lower() or 'segments retransmited' in line.lower():
                    match = re.search(r'(\d+)', line)
                    if match:
                        segments_retransmitted = int(match.group(1))

            if segments_sent > 0:
                retransmit_rate = (segments_retransmitted / segments_sent) * 100
                return {
                    'sent': segments_sent,
                    'retransmitted': segments_retransmitted,
                    'rate_pct': retransmit_rate
                }
        except Exception:
            pass

        return None

    def display_dashboard(self):
        """Display comprehensive monitoring dashboard"""
        # Move cursor to home position (top-left) without clearing screen
        print("\033[H", end='')
        sys.stdout.flush()

        print("=" * 80)
        print("                🥷 MONITOR THE RUCKUS - Network Health 🥷")
        print("=" * 80)
        print(f"📡 Interface: {self.interface}")
        print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

        # Get current stats
        stats = self.get_interface_stats()
        if stats:
            # Local device health
            print("\n🖥️  LOCAL DEVICE HEALTH:")
            print(f"   RX: {stats['rx_packets']:,} packets ({stats['rx_bytes']:,} bytes)")
            print(f"   TX: {stats['tx_packets']:,} packets ({stats['tx_bytes']:,} bytes)")

            rx_status = "🟢" if stats['rx_errors'] == 0 else "🔴"
            tx_status = "🟢" if stats['tx_errors'] == 0 else "🔴"
            print(f"   {rx_status} Errors: RX={stats['rx_errors']}, TX={stats['tx_errors']}")

            drop_status = "🟢" if (stats['rx_dropped'] == 0 and stats['tx_dropped'] == 0) else "🔴"
            print(f"   {drop_status} Dropped: RX={stats['rx_dropped']}, TX={stats['tx_dropped']}")

            # Bandwidth
            bandwidth = self.calculate_bandwidth(stats)
            self.bandwidth_history.append(bandwidth['total_mbps'])

            print(f"\n📊 BANDWIDTH USAGE:")
            print(f"   ⬇️  Download: {bandwidth['download_mbps']:.2f} Mbps")
            print(f"   ⬆️  Upload: {bandwidth['upload_mbps']:.2f} Mbps")
            print(f"   🔄 Total: {bandwidth['total_mbps']:.2f} Mbps")

            if len(self.bandwidth_history) > 5:
                avg_bw = statistics.mean(self.bandwidth_history)
                max_bw = max(self.bandwidth_history)
                print(f"   📈 Avg (1min): {avg_bw:.2f} Mbps  |  Peak: {max_bw:.2f} Mbps")

        # TCP retransmits
        tcp_stats = self.check_tcp_retransmits()
        if tcp_stats:
            print(f"\n🔄 TCP RETRANSMITS:")
            print(f"   Sent: {tcp_stats['sent']:,}  |  Retransmitted: {tcp_stats['retransmitted']:,}")

            status = "🟢" if tcp_stats['rate_pct'] < 1 else "🟡" if tcp_stats['rate_pct'] < 5 else "🔴"
            print(f"   {status} Retransmit Rate: {tcp_stats['rate_pct']:.3f}%")

        # Target monitoring
        if self.targets:
            print(f"\n" + "=" * 80)
            print("🎯 TARGET MONITORING:")
            print("=" * 80)

            for name, ip in self.targets.items():
                print(f"\n📍 {name} ({ip}):")

                # Ping target
                ping_result = self.ping_target(ip, count=5)

                if ping_result['success']:
                    latency = ping_result['avg_ms']
                    jitter = ping_result['jitter_ms']
                    packet_loss = ping_result['packet_loss_pct']

                    # Store history
                    self.latency_history[name].append(latency)
                    self.packet_loss_history[name].append(packet_loss)

                    # Calculate quality score
                    quality_score = self.calculate_quality_score(latency, packet_loss, jitter)
                    quality_status = self.get_quality_status(quality_score)

                    print(f"   ⏱️  Latency: {latency:.1f}ms (min: {ping_result['min_ms']:.1f}, max: {ping_result['max_ms']:.1f})")
                    print(f"   📶 Jitter: {jitter:.1f}ms")
                    print(f"   📉 Packet Loss: {packet_loss}%")
                    print(f"   ⭐ Quality Score: {quality_score:.0f}/100 - {quality_status}")

                    # Historical stats
                    if len(self.latency_history[name]) > 5:
                        avg_latency = statistics.mean(self.latency_history[name])
                        max_latency = max(self.latency_history[name])
                        avg_loss = statistics.mean(self.packet_loss_history[name])

                        print(f"   📊 1-min Avg: Latency={avg_latency:.1f}ms, Loss={avg_loss:.1f}%, Max Latency={max_latency:.1f}ms")

                    # Alerts
                    alerts = []
                    if latency > self.alert_thresholds['latency_ms']:
                        alerts.append(f"HIGH LATENCY ({latency:.0f}ms)")
                    if packet_loss > self.alert_thresholds['packet_loss_pct']:
                        alerts.append(f"PACKET LOSS ({packet_loss}%)")
                    if jitter > self.alert_thresholds['jitter_ms']:
                        alerts.append(f"HIGH JITTER ({jitter:.0f}ms)")
                    if quality_score < self.alert_thresholds['quality_score']:
                        alerts.append(f"POOR QUALITY ({quality_score:.0f}/100)")

                    if alerts:
                        print(f"   ⚠️  ALERTS: {', '.join(alerts)}")
                else:
                    print(f"   ❌ UNREACHABLE - 100% packet loss")
                    self.latency_history[name].append(0)
                    self.packet_loss_history[name].append(100)

        print("\n" + "=" * 80)
        print("Press Ctrl+C to stop monitoring")
        print("=" * 80)

    def run(self, interval: float = 2.0):
        """Run monitoring loop"""
        self.running = True

        if not self.interface:
            self.interface = self.detect_interface()

        print(f"\n🎬 Starting network monitoring...")
        print(f"📡 Interface: {self.interface}")
        print(f"🎯 Targets: {', '.join([f'{name} ({ip})' for name, ip in self.targets.items()])}")
        print(f"⏱️  Update interval: {interval}s")
        print(f"\nGathering initial data...\n")

        time.sleep(2)

        # Enter alternate screen buffer and hide cursor (like htop)
        print("\033[?1049h\033[?25l", end='')
        sys.stdout.flush()

        try:
            while self.running:
                self.display_dashboard()
                time.sleep(interval)
        except KeyboardInterrupt:
            pass
        finally:
            # Exit alternate screen buffer and show cursor
            print("\033[?1049l\033[?25h", end='')
            sys.stdout.flush()
            print("\n👋 Monitoring stopped")
            self.running = False


def main():
    """Main entry point"""
    print("""
████████████████████████████████████████████████████████████████████████████████
██                                                                            ██
██                          ██╗    ██╗██╗   ██╗                               ██
██                          ██║    ██║██║   ██║                               ██
██                          ██║ █╗ ██║██║   ██║                               ██
██                          ██║███╗██║██║   ██║                               ██
██                          ╚███╔███╔╝╚██████╔╝                               ██
██                           ╚══╝╚══╝  ╚═════╝                                ██
██                                                                            ██
██                         WU-TANG SWORD STYLE                                ██
██                      MONITOR THE RUCKUS                                    ██
██                   Enhanced Network Health Monitor                          ██
██                                                                            ██
████████████████████████████████████████████████████████████████████████████████

"The mind is a terrible thing to taste" - RZA

Features:
  • Real-time bandwidth monitoring
  • Ping latency and packet loss tracking
  • Jitter measurement
  • Connection quality scoring
  • Historical metrics (1-minute averages)
  • TCP retransmit rate
  • Automatic alerts for degraded connections

════════════════════════════════════════════════════════════════════════════════
""")

    # Get monitoring targets
    targets = {}

    print("🎯 Configure monitoring targets:")
    print("   Enter IP addresses to monitor (press ENTER to skip)")
    print()

    # Default suggestions
    camera = input("📹 Camera IP (e.g., 192.168.1.78): ").strip()
    if camera:
        targets['Camera'] = camera

    gateway = input("🌐 Gateway/Router IP (e.g., 192.168.1.1): ").strip()
    if gateway:
        targets['Gateway'] = gateway

    server = input("☁️  Server IP (e.g., 8.8.8.8): ").strip()
    if server:
        targets['Server'] = server

    # Custom targets
    while True:
        custom = input("➕ Add another target? (name:ip or ENTER to finish): ").strip()
        if not custom:
            break
        if ':' in custom:
            name, ip = custom.split(':', 1)
            targets[name.strip()] = ip.strip()

    if not targets:
        print("\n⚠️  No targets specified. Monitoring local interface only.")

    # Create monitor
    monitor = NetworkMonitor(targets=targets)

    # Set custom thresholds
    print("\n⚙️  Alert thresholds (press ENTER for defaults):")

    try:
        latency = input(f"   Latency threshold (default: 100ms): ").strip()
        if latency:
            monitor.alert_thresholds['latency_ms'] = float(latency)

        loss = input(f"   Packet loss threshold (default: 5%): ").strip()
        if loss:
            monitor.alert_thresholds['packet_loss_pct'] = float(loss)

        jitter = input(f"   Jitter threshold (default: 50ms): ").strip()
        if jitter:
            monitor.alert_thresholds['jitter_ms'] = float(jitter)
    except ValueError:
        print("   Using default thresholds")

    # Start monitoring
    monitor.run(interval=2.0)


if __name__ == "__main__":
    main()
