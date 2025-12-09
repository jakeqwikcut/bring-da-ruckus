#!/usr/bin/env python3
"""
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
██                   Real-Time Network Health Monitor                         ██
██                        36 Chambers of Chaos                                ██
██                                                                            ██
██                    Created by Jake Mammen - 2025                           ██
██                                                                            ██
████████████████████████████████████████████████████████████████████████████████

DISCLAIMER:
    Wu-Tang is for the children, but with great power comes great responsibility.

    This monitoring tool is designed for LEGITIMATE NETWORK TESTING purposes only.
    Use it to observe network health during chaos engineering tests.

════════════════════════════════════════════════════════════════════════════════

Monitor The Ruckus - Real-Time Network Health Monitoring
Companion tool for Bring Da Ruckus chaos testing
Created by Jake Mammen - 2025

Monitors:
- Local device network health (interface stats, packet loss, errors)
- Ping latency and packet loss to targets
- Bandwidth utilization
- Connection quality metrics
- Network-wide discovery and health
"""

import subprocess
import sys
import time
import threading
import argparse
import select
from datetime import datetime
from typing import Optional, Dict, List
import os
import re


class NetworkMonitor:
    """Real-time network health monitoring"""

    def __init__(self, interface: Optional[str] = None, target_ips: List[str] = None):
        self.interface = interface
        self.target_ips = target_ips or []
        self.running = False
        self.stats = {
            'local': {},
            'targets': {},
            'network': {}
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
            # Get interface stats from /proc/net/dev
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
            return {'error': str(e)}
        return {}

    def ping_target(self, ip: str, count: int = 4):
        """Ping a target and get latency/loss stats"""
        try:
            result = subprocess.run(
                ["ping", "-c", str(count), "-W", "2", ip],
                capture_output=True, text=True, timeout=10
            )

            stats = {
                'ip': ip,
                'reachable': result.returncode == 0,
                'latency_min': None,
                'latency_avg': None,
                'latency_max': None,
                'packet_loss': 100.0
            }

            if result.returncode == 0:
                # Parse ping output
                for line in result.stdout.split('\n'):
                    if 'packet loss' in line:
                        match = re.search(r'(\d+)% packet loss', line)
                        if match:
                            stats['packet_loss'] = float(match.group(1))
                    elif 'rtt min/avg/max' in line or 'round-trip' in line:
                        match = re.search(r'= ([\d.]+)/([\d.]+)/([\d.]+)', line)
                        if match:
                            stats['latency_min'] = float(match.group(1))
                            stats['latency_avg'] = float(match.group(2))
                            stats['latency_max'] = float(match.group(3))

            return stats
        except Exception as e:
            return {
                'ip': ip,
                'reachable': False,
                'error': str(e),
                'packet_loss': 100.0
            }

    def get_bandwidth_usage(self):
        """Calculate current bandwidth usage"""
        stats1 = self.get_interface_stats()
        time.sleep(1)
        stats2 = self.get_interface_stats()

        if 'error' not in stats1 and 'error' not in stats2:
            rx_rate = (stats2['rx_bytes'] - stats1['rx_bytes']) * 8 / 1_000_000  # Mbps
            tx_rate = (stats2['tx_bytes'] - stats1['tx_bytes']) * 8 / 1_000_000  # Mbps

            return {
                'rx_mbps': round(rx_rate, 2),
                'tx_mbps': round(tx_rate, 2),
                'total_mbps': round(rx_rate + tx_rate, 2)
            }
        return {'error': 'Failed to calculate bandwidth'}

    def discover_network(self):
        """Discover active hosts on the network"""
        try:
            # Get network info
            result = subprocess.run(
                ["ip", "-4", "addr", "show", self.interface],
                capture_output=True, text=True, check=True
            )

            # Extract network CIDR
            match = re.search(r'inet ([\d.]+/\d+)', result.stdout)
            if not match:
                return []

            network = match.group(1)

            # Use arp-scan if available, otherwise use nmap or simple ping sweep
            # For now, use a simple approach
            print(f"   🔍 Scanning network {network}...")

            return []  # Placeholder - full implementation would scan the network
        except Exception as e:
            return []

    def display_dashboard(self):
        """Display real-time monitoring dashboard"""
        os.system('clear' if os.name == 'posix' else 'cls')

        print("=" * 80)
        print("                    🥷 MONITOR THE RUCKUS - Network Health 🥷")
        print("=" * 80)
        print(f"📡 Interface: {self.interface}")
        print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

        # Local interface stats
        print("\n🖥️  LOCAL DEVICE HEALTH:")
        stats = self.get_interface_stats()
        if 'error' not in stats:
            print(f"   RX: {stats['rx_packets']:,} packets ({stats['rx_bytes']:,} bytes)")
            print(f"   TX: {stats['tx_packets']:,} packets ({stats['tx_bytes']:,} bytes)")

            error_status = "🟢" if stats['rx_errors'] + stats['tx_errors'] == 0 else "🔴"
            print(f"   {error_status} Errors: RX={stats['rx_errors']}, TX={stats['tx_errors']}")

            drop_status = "🟢" if stats['rx_dropped'] + stats['tx_dropped'] == 0 else "🟡"
            print(f"   {drop_status} Dropped: RX={stats['rx_dropped']}, TX={stats['tx_dropped']}")
        else:
            print(f"   ❌ Error: {stats['error']}")

        # Bandwidth
        print("\n📊 BANDWIDTH USAGE:")
        bw = self.get_bandwidth_usage()
        if 'error' not in bw:
            print(f"   ⬇️  Download: {bw['rx_mbps']} Mbps")
            print(f"   ⬆️  Upload: {bw['tx_mbps']} Mbps")
            print(f"   🔄 Total: {bw['total_mbps']} Mbps")
        else:
            print(f"   ❌ {bw['error']}")

        # Target monitoring
        if self.target_ips:
            print("\n🎯 TARGET MONITORING:")
            for target in self.target_ips:
                print(f"\n   Target: {target}")
                ping_stats = self.ping_target(target, count=3)

                if ping_stats['reachable']:
                    health = "🟢" if ping_stats['packet_loss'] == 0 else "🟡" if ping_stats['packet_loss'] < 10 else "🔴"
                    print(f"   {health} Status: REACHABLE")
                    print(f"      Latency: {ping_stats['latency_avg']:.1f}ms "
                          f"(min: {ping_stats['latency_min']:.1f}, max: {ping_stats['latency_max']:.1f})")
                    print(f"      Packet Loss: {ping_stats['packet_loss']:.1f}%")
                else:
                    print(f"   🔴 Status: UNREACHABLE")
                    if 'error' in ping_stats:
                        print(f"      Error: {ping_stats['error']}")

        print("\n" + "=" * 80)
        print("Press Ctrl+C to stop monitoring")
        print("=" * 80)

    def run_continuous(self, interval: int = 5):
        """Run continuous monitoring"""
        self.running = True

        if not self.interface:
            self.interface = self.detect_interface()

        print(f"\n🎬 Starting network monitoring...")
        print(f"📡 Interface: {self.interface}")
        if self.target_ips:
            print(f"🎯 Monitoring targets: {', '.join(self.target_ips)}")
        print(f"⏱️  Refresh interval: {interval} seconds")
        print("\n⏳ Gathering initial data...\n")

        try:
            while self.running:
                self.display_dashboard()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n👋 Monitoring stopped.")
            self.running = False


def main():
    parser = argparse.ArgumentParser(
        description="Monitor The Ruckus - Real-Time Network Health Monitoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Monitor The Ruckus - Companion tool for Bring Da Ruckus
Monitors network health during chaos engineering tests
Created by Jake Mammen - 2025

Examples:
  # Monitor local device
  python3 monitor-the-ruckus.py

  # Monitor specific targets
  python3 monitor-the-ruckus.py --targets 192.168.1.100 192.168.1.1

  # Monitor with custom interval
  python3 monitor-the-ruckus.py --interval 10 --targets 192.168.1.100

  # Monitor specific interface
  python3 monitor-the-ruckus.py --interface eth1 --targets 192.168.1.100
        """
    )

    parser.add_argument(
        '-i', '--interface',
        help='Network interface to monitor (auto-detect if not specified)',
        default=None
    )

    parser.add_argument(
        '-t', '--targets',
        nargs='+',
        help='Target IP addresses to monitor',
        default=[]
    )

    parser.add_argument(
        '--interval',
        type=int,
        default=5,
        help='Refresh interval in seconds (default: 5)'
    )

    args = parser.parse_args()

    # Check if running on Linux
    if os.name != 'posix':
        print("❌ This tool requires Linux (uses ip command and /proc filesystem)")
        sys.exit(1)

    monitor = NetworkMonitor(
        interface=args.interface,
        target_ips=args.targets
    )

    monitor.run_continuous(interval=args.interval)


if __name__ == "__main__":
    main()
