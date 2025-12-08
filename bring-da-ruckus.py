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
██                        BRING DA RUCKUS                                     ██
██                   Network Chaos Engineering Tool                           ██
██                        36 Chambers of Chaos                                ██
██                                                                            ██
██                    Created by Jake Mammen - 2025                           ██
██                                                                            ██
████████████████████████████████████████████████████████████████████████████████

DISCLAIMER:
    Wu-Tang is for the children, but with great power comes great responsibility.

    This software is designed for LEGITIMATE NETWORK TESTING AND CHAOS ENGINEERING
    purposes only. It is intended to help engineers test system resilience and
    identify weaknesses in controlled environments.

    DO NOT use this tool for:
    - Malicious attacks on networks you don't own/control
    - Disrupting production systems without authorization
    - Any illegal or unethical activities
    - Harming others or their infrastructure

    By using this software, you agree to:
    - Use it only on networks you own or have explicit permission to test
    - Accept full responsibility for any consequences of its use
    - Comply with all applicable laws and regulations
    - Not hold the authors liable for any misuse

    Remember: Real ninjas test responsibly. Protect ya neck, and protect your network.

    🥷 RESPECT THE CRAFT. TEST WITH PURPOSE. BRING DA RUCKUS RESPONSIBLY. 🥷

════════════════════════════════════════════════════════════════════════════════

Bring Da Ruckus - Network Chaos Engineering Tool
Inspired by Wu-Tang sword style for testing QwikCut camera systems
Created by Jake Mammen - 2025

Simulates network degradation scenarios using Linux tc (traffic control):
- Latency (ping delay)
- Packet loss
- Bandwidth throttling
- Jitter
- Network outages
"""

import subprocess
import sys
import time
import threading
import argparse
import select
from datetime import datetime, timedelta
from typing import Optional, Dict
import os


class ChaosChamber:
    """The 36 Chambers of Chaos - Wu-Tang inspired network disruption levels"""
    PEACE = {
        "name": "☯️  Chamber 0: Peace (Normal Network)",
        "latency_ms": 0,
        "packet_loss_pct": 0,
        "bandwidth_kbps": None,
        "jitter_ms": 0
    }

    FIRST = {
        "name": "🥋 Chamber 1: The Swarm (Light Disruption)",
        "latency_ms": 50,
        "packet_loss_pct": 1,
        "bandwidth_kbps": 50000,  # 50 Mbps
        "jitter_ms": 10
    }

    NINTH = {
        "name": "⚔️  Chamber 9: The Mystery (Moderate Chaos)",
        "latency_ms": 150,
        "packet_loss_pct": 3,
        "bandwidth_kbps": 10000,  # 10 Mbps
        "jitter_ms": 25
    }

    EIGHTEENTH = {
        "name": "🔥 Chamber 18: The Deadly Venoms (Heavy Ruckus)",
        "latency_ms": 300,
        "packet_loss_pct": 8,
        "bandwidth_kbps": 2000,  # 2 Mbps
        "jitter_ms": 50
    }

    THIRTYSIXTH = {
        "name": "💀 Chamber 36: Liquid Swords (Extreme Chaos)",
        "latency_ms": 500,
        "packet_loss_pct": 15,
        "bandwidth_kbps": 512,  # 512 Kbps
        "jitter_ms": 100
    }

    SHAOLIN = {
        "name": "☠️  Shaolin Shadow: Total Darkness (Complete Outage)",
        "latency_ms": 0,
        "packet_loss_pct": 100,
        "bandwidth_kbps": 0,
        "jitter_ms": 0
    }

    @staticmethod
    def all_chambers():
        """Return all chambers in order"""
        return [
            ChaosChamber.PEACE,
            ChaosChamber.FIRST,
            ChaosChamber.NINTH,
            ChaosChamber.EIGHTEENTH,
            ChaosChamber.THIRTYSIXTH,
            ChaosChamber.SHAOLIN
        ]


class DeadmanSwitch:
    """Safety mechanism to automatically stop ruckus after inactivity"""

    def __init__(self, timeout_minutes: int, callback):
        self.timeout_minutes = timeout_minutes
        self.callback = callback
        self.last_activity = datetime.now()
        self.running = False
        self.thread = None
        self.warned = False

    def reset(self):
        """Reset the timer - call this on any user activity"""
        self.last_activity = datetime.now()

    def start(self):
        """Start monitoring"""
        self.running = True
        self.thread = threading.Thread(target=self._monitor, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop monitoring"""
        self.running = False

    def _monitor(self):
        """Background monitoring thread"""
        while self.running:
            time.sleep(5)  # Check every 5 seconds
            elapsed = (datetime.now() - self.last_activity).total_seconds()
            elapsed_minutes = elapsed / 60
            
            # Warning at 30 seconds before timeout
            if not self.warned and elapsed >= (self.timeout_minutes * 60 - 30):
                self.warned = True
                print(f"\n\n⚠️  WARNING: Deadman's switch will trigger in 30 seconds!")
                print("Continue testing? (Y/N): ", end='', flush=True)
                
                # Start a thread to wait for input
                import select
                import sys
                
                # Non-blocking input check for 30 seconds
                start_wait = datetime.now()
                user_responded = False
                
                while (datetime.now() - start_wait).total_seconds() < 30:
                    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                        response = sys.stdin.readline().strip().upper()
                        if response == 'Y' or response == 'YES':
                            print("✅ Timer reset! Continuing for another {0} minutes.".format(self.timeout_minutes))
                            self.reset()
                            self.warned = False
                            user_responded = True
                            break
                        else:
                            print("🛑 Stopping chaos...")
                            self.callback()
                            return
                    time.sleep(0.5)
                
                # If no response after 30 seconds, trigger callback
                if not user_responded:
                    print("\n\n⏰ No response - Deadman's switch triggered!")
                    self.callback()
                    break
            
            # Final timeout check
            elif elapsed_minutes >= self.timeout_minutes:
                if not self.warned:  # Direct timeout without warning
                    print(f"\n⏰ Deadman's switch triggered after {self.timeout_minutes} minutes of inactivity!")
                    self.callback()
                    break


class NetworkRuckus:
    """Main class for managing network chaos on Ubuntu Server using tc (traffic control)"""

    def __init__(self, interface: Optional[str] = None, deadman_timeout: int = 5):
        self.interface = interface
        self.current_chamber = ChaosChamber.PEACE
        self.is_active = False
        self.deadman = DeadmanSwitch(deadman_timeout, self._emergency_stop)
        self.target_ip = None
        self.scope = 'local'  # 'local', 'network', or 'targeted'
        self.gateway_configured = False

    def detect_interface(self):
        """Auto-detect the primary network interface"""
        try:
            # Try to get the default route interface
            result = subprocess.run(
                ["ip", "route", "show", "default"],
                capture_output=True, text=True, check=True
            )
            # Parse output like: "default via 192.168.1.1 dev eth0"
            words = result.stdout.split()
            if "dev" in words:
                dev_idx = words.index("dev")
                if dev_idx + 1 < len(words):
                    return words[dev_idx + 1]
        except:
            pass

        # Fallback: find first non-loopback interface that's up
        try:
            result = subprocess.run(
                ["ip", "link", "show"],
                capture_output=True, text=True, check=True
            )
            for line in result.stdout.split('\n'):
                if 'state UP' in line and 'lo:' not in line:
                    interface = line.split(':')[1].strip()
                    return interface
        except:
            pass

        return "eth0"  # Final fallback

    def set_target(self, ip: str):
        """Set specific target IP for disruption"""
        self.target_ip = ip
        self.scope = 'targeted'
        print(f"🎯 Target set to: {ip}")
        print("   Chaos will only affect traffic to/from this IP")

    def set_scope(self, scope: str):
        """Set the scope of network disruption"""
        if scope not in ['local', 'network', 'targeted']:
            print("❌ Invalid scope. Use 'local', 'network', or 'targeted'")
            return False
        
        self.scope = scope
        
        if scope == 'network':
            # Check if IP forwarding is enabled
            try:
                result = subprocess.run(
                    ["sysctl", "net.ipv4.ip_forward"],
                    capture_output=True, text=True, check=True
                )
                if "net.ipv4.ip_forward = 0" in result.stdout:
                    print("\n⚠️  IP forwarding is disabled. Network-wide chaos requires this server to act as a gateway.")
                    response = input("Enable IP forwarding now? (Y/N): ").strip().upper()
                    if response == 'Y' or response == 'YES':
                        subprocess.run(["sysctl", "-w", "net.ipv4.ip_forward=1"], check=True)
                        # Set up NAT
                        subprocess.run(
                            f"iptables -t nat -A POSTROUTING -o {self.interface} -j MASQUERADE",
                            shell=True, check=True
                        )
                        self.gateway_configured = True
                        print("✅ IP forwarding enabled. This server is now acting as a gateway.")
                        print("   Configure devices to use this server's IP as their gateway.")
                    else:
                        print("❌ Network-wide chaos requires IP forwarding. Reverting to local scope.")
                        self.scope = 'local'
                        return False
                else:
                    self.gateway_configured = True
                    print("✅ IP forwarding already enabled")
            except Exception as e:
                print(f"❌ Failed to configure IP forwarding: {e}")
                self.scope = 'local'
                return False
        
        scope_names = {
            'local': '🖥️  Local Device Only',
            'network': '🌐 Entire Network (Gateway Mode)',
            'targeted': '🎯 Targeted IP'
        }
        print(f"\n📍 Scope set to: {scope_names[scope]}")
        return True

    def apply_ruckus(self, level: Dict):
        """Apply network disruption using Linux tc (traffic control)"""
        print(f"\n🔧 Applying: {level['name']}")

        if not self.interface:
            self.interface = self.detect_interface()

        # Clear existing rules first
        subprocess.run(f"tc qdisc del dev {self.interface} root",
                      shell=True, stderr=subprocess.DEVNULL)
        subprocess.run(f"tc filter del dev {self.interface}",
                      shell=True, stderr=subprocess.DEVNULL)

        if level['packet_loss_pct'] == 100:
            # Complete outage
            if self.scope == 'targeted' and self.target_ip:
                # Targeted outage using iptables
                subprocess.run(f"iptables -A INPUT -s {self.target_ip} -j DROP", shell=True, check=True)
                subprocess.run(f"iptables -A OUTPUT -d {self.target_ip} -j DROP", shell=True, check=True)
                print(f"   ☠️  Complete outage for {self.target_ip}")
            else:
                cmd = f"tc qdisc add dev {self.interface} root netem loss 100%"
                subprocess.run(cmd, shell=True, check=True)
                scope_msg = "entire network" if self.scope == 'network' else "this device"
                print(f"   ☠️  Complete network outage on {self.interface} ({scope_msg})")

        elif level == ChaosChamber.PEACE:
            # Clear iptables rules too
            if self.target_ip:
                subprocess.run(f"iptables -D INPUT -s {self.target_ip} -j DROP", 
                             shell=True, stderr=subprocess.DEVNULL)
                subprocess.run(f"iptables -D OUTPUT -d {self.target_ip} -j DROP", 
                             shell=True, stderr=subprocess.DEVNULL)
            print(f"   ✅ All disruptions cleared on {self.interface}")
            print(f"   ☯️  Network has returned to peace")

        else:
            # Build tc netem command for latency, jitter, and packet loss
            params = []

            if level['latency_ms'] > 0:
                params.append(f"delay {level['latency_ms']}ms")
                if level['jitter_ms'] > 0:
                    params.append(f"{level['jitter_ms']}ms")

            if level['packet_loss_pct'] > 0:
                params.append(f"loss {level['packet_loss_pct']}%")

            # Apply netem for latency/loss/jitter
            if params:
                try:
                    if self.scope == 'targeted' and self.target_ip:
                        # Use tc with filters for targeted disruption
                        # Create root qdisc with prio
                        subprocess.run(f"tc qdisc add dev {self.interface} root handle 1: prio", 
                                     shell=True, check=True)
                        # Add netem to band 1
                        cmd = f"tc qdisc add dev {self.interface} parent 1:1 handle 10: netem {' '.join(params)}"
                        subprocess.run(cmd, shell=True, check=True)
                        # Filter traffic to target IP
                        subprocess.run(
                            f"tc filter add dev {self.interface} protocol ip parent 1:0 prio 1 u32 match ip dst {self.target_ip} flowid 1:1",
                            shell=True, check=True
                        )
                        print(f"   ✅ Applied to traffic targeting: {self.target_ip}")
                    else:
                        # Standard application for local or network-wide
                        cmd = f"tc qdisc add dev {self.interface} root netem {' '.join(params)}"
                        subprocess.run(cmd, shell=True, check=True)
                        scope_msg = "entire network" if self.scope == 'network' else "this device"
                        print(f"   ✅ Applied on interface: {self.interface} ({scope_msg})")
                    
                    if level['latency_ms'] > 0:
                        print(f"   ⏱️  Latency: {level['latency_ms']}ms ± {level['jitter_ms']}ms")
                    if level['packet_loss_pct'] > 0:
                        print(f"   📉 Packet Loss: {level['packet_loss_pct']}%")
                except subprocess.CalledProcessError as e:
                    print(f"   ❌ Failed to apply netem rules: {e}")
                    return False

            # For bandwidth limiting, we need to use tbf (token bucket filter)
            # Note: Can't easily combine netem and tbf, so bandwidth is separate
            if level['bandwidth_kbps'] and level['bandwidth_kbps'] > 0:
                # If we already applied netem, we need to nest tbf under it
                if params:
                    # Add tbf as child qdisc (more complex, skip for now)
                    print(f"   ⚠️  Bandwidth limiting not combined with other rules")
                else:
                    # No netem, can use tbf directly
                    bw_cmd = f"tc qdisc add dev {self.interface} root tbf rate {level['bandwidth_kbps']}kbit burst 32kbit latency 400ms"
                    try:
                        subprocess.run(bw_cmd, shell=True, check=True)
                        print(f"   🚦 Bandwidth limited to {level['bandwidth_kbps']} Kbps ({level['bandwidth_kbps']/1000:.1f} Mbps)")
                    except subprocess.CalledProcessError as e:
                        print(f"   ⚠️  Could not apply bandwidth limit: {e}")

        self.current_chamber = level
        self.is_active = (level != ChaosChamber.PEACE)
        self.deadman.reset()
        return True

    def clear_ruckus(self):
        """Clear all network disruptions"""
        print("\n🧹 Clearing all network disruptions...")
        if not self.interface:
            self.interface = self.detect_interface()

        subprocess.run(f"tc qdisc del dev {self.interface} root",
                      shell=True, stderr=subprocess.DEVNULL)
        print(f"   ✅ Network restored to normal on {self.interface}")
        print(f"   ☯️  Peace has been restored to the chambers")

        self.is_active = False
        self.current_chamber = ChaosChamber.PEACE

    def _emergency_stop(self):
        """Emergency stop triggered by deadman's switch"""
        print("\n🚨 EMERGENCY STOP - Clearing all ruckus!")
        self.clear_ruckus()
        self.is_active = False

    def get_status(self):
        """Get current status"""
        status = f"\n{'='*60}\n"
        status += f"🥷 BRING DA RUCKUS - Status\n"
        status += f"{'='*60}\n"
        status += f"Current Chamber: {self.current_chamber['name']}\n"
        status += f"Active: {'🟢 YES' if self.is_active else '🔴 NO'}\n"
        status += f"Interface: {self.interface or 'Auto-detect'}\n"
        
        scope_names = {
            'local': '🖥️  Local Device Only',
            'network': '🌐 Entire Network (Gateway Mode)',
            'targeted': '🎯 Targeted IP'
        }
        status += f"Scope: {scope_names.get(self.scope, self.scope)}\n"
        
        if self.target_ip and self.scope == 'targeted':
            status += f"Target IP: {self.target_ip}\n"
        status += f"Deadman Timeout: {self.deadman.timeout_minutes} minutes\n"

        if self.is_active:
            elapsed = (datetime.now() - self.deadman.last_activity).total_seconds() / 60
            status += f"Time since last activity: {elapsed:.1f} minutes\n"

        status += f"{'='*60}\n"
        return status

    def show_tc_status(self):
        """Show current tc configuration"""
        if not self.interface:
            self.interface = self.detect_interface()

        print(f"\n📋 Current tc configuration on {self.interface}:")
        print("="*60)
        result = subprocess.run(
            f"tc qdisc show dev {self.interface}",
            shell=True, capture_output=True, text=True
        )
        print(result.stdout if result.stdout else "   No qdisc configured (normal operation)")
        print("="*60)


def show_menu():
    """Display the main menu"""
    print("\n" + "="*60)
    print("🥷 BRING DA RUCKUS - Wu-Tang Sword Style")
    print("   36 Chambers of Network Chaos")
    print("   Ubuntu Server Edition - Using tc (traffic control)")
    print("="*60)
    print("\n📍 SCOPE:")
    print("  o - Set scope: Local / Network / Targeted IP")
    print("\n🔱 Select Your Chamber:")
    for i, chamber in enumerate(ChaosChamber.all_chambers(), 1):
        print(f"  {i}. {chamber['name']}")
    print("\n⚡ Commands:")
    print("  s - Show current status")
    print("  c - Clear all ruckus (restore normal network)")
    print("  i - Set network interface")
    print("  d - Show detailed tc configuration")
    print("  q - Quit and clean up")
    print("="*60)


def interactive_mode(ruckus: NetworkRuckus):
    """Run interactive CLI mode"""
    print("\n🎬 Starting interactive mode...")
    print(f"⏰ Deadman's switch active: {ruckus.deadman.timeout_minutes} minutes")
    print(f"🔧 Interface: {ruckus.interface or 'Auto-detect'}")

    ruckus.deadman.start()

    try:
        while True:
            show_menu()
            choice = input("\n👉 Enter your choice: ").strip().lower()

            ruckus.deadman.reset()  # Reset deadman on any activity

            if choice == 'q':
                print("\n👋 Exiting and cleaning up...")
                ruckus.clear_ruckus()
                ruckus.deadman.stop()
                break

            elif choice == 's':
                print(ruckus.get_status())

            elif choice == 'c':
                ruckus.clear_ruckus()

            elif choice == 'd':
                ruckus.show_tc_status()

            elif choice == 'o':
                print("\n📍 Select scope:")
                print("   [1] Local device only (default)")
                print("   [2] Entire network (requires gateway mode)")
                print("   [3] Targeted IP address")
                scope_choice = input("Enter choice: ").strip()
                
                if scope_choice == '1':
                    ruckus.set_scope('local')
                elif scope_choice == '2':
                    ruckus.set_scope('network')
                elif scope_choice == '3':
                    ip = input("Enter target IP address: ").strip()
                    if ip:
                        ruckus.set_target(ip)
                    else:
                        print("❌ Invalid IP")

            elif choice == 't':
                ip = input("Enter target IP address: ").strip()
                if ip:
                    ruckus.set_target(ip)
                else:
                    ruckus.target_ip = None
                    print("🌐 Targeting all traffic")

            elif choice == 'i':
                interface = input("Enter network interface name: ").strip()
                if interface:
                    ruckus.interface = interface
                    print(f"🔧 Interface set to: {interface}")

            elif choice.isdigit():
                chamber_idx = int(choice) - 1
                chambers = ChaosChamber.all_chambers()
                if 0 <= chamber_idx < len(chambers):
                    ruckus.apply_ruckus(chambers[chamber_idx])
                else:
                    print("❌ Invalid chamber number")

            else:
                print("❌ Invalid choice")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted! Cleaning up...")
        ruckus.clear_ruckus()
        ruckus.deadman.stop()


def main():
    parser = argparse.ArgumentParser(
        description="Bring Da Ruckus - Network Chaos Engineering Tool for Ubuntu Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sudo python3 bring-da-ruckus.py                         # Interactive mode
  sudo python3 bring-da-ruckus.py --level ninth           # Start with Chamber 9
  sudo python3 bring-da-ruckus.py --level thirtysixth --timeout 15  # Chamber 36
  sudo python3 bring-da-ruckus.py --interface eth0 --timeout 15     # Custom settings

Requirements:
  - Ubuntu Server (or any Linux with tc/iproute2)
  - sudo/root privileges
  - tc (traffic control) command available

🥷 Wu-Tang is for the children. Test responsibly. Bring da ruckus. 🥷
        """
    )

    parser.add_argument(
        '-i', '--interface',
        help='Network interface to apply chaos to (auto-detect if not specified)'
    )

    parser.add_argument(
        '-l', '--level',
        choices=['peace', 'first', 'ninth', 'eighteenth', 'thirtysixth', 'shaolin'],
        help='Initial chaos chamber (peace, first, ninth, eighteenth, thirtysixth, shaolin)'
    )

    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=30,
        help='Deadman switch timeout in minutes (default: 30)'
    )

    parser.add_argument(
        '--target',
        help='Target specific IP address (not yet implemented)'
    )

    args = parser.parse_args()

    # Check for sudo/root privileges (required for tc command)
    if os.geteuid() != 0:
        print("❌ ERROR: This tool requires sudo/root privileges")
        print("   Traffic control (tc) commands need root access")
        print("   Please run with: sudo python3 bring-da-ruckus.py")
        sys.exit(1)

    # Check if tc is available
    try:
        subprocess.run(["tc", "-Version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ ERROR: tc (traffic control) command not found")
        print("   Please install iproute2: sudo apt-get install iproute2")
        sys.exit(1)

    # Create ruckus instance
    ruckus = NetworkRuckus(
        interface=args.interface,
        deadman_timeout=args.timeout
    )

    if args.target:
        ruckus.set_target(args.target)

    # Apply initial chamber if specified
    if args.level:
        chamber_map = {
            'peace': ChaosChamber.PEACE,
            'first': ChaosChamber.FIRST,
            'ninth': ChaosChamber.NINTH,
            'eighteenth': ChaosChamber.EIGHTEENTH,
            'thirtysixth': ChaosChamber.THIRTYSIXTH,
            'shaolin': ChaosChamber.SHAOLIN
        }
        ruckus.apply_ruckus(chamber_map[args.level])

    # Start interactive mode
    interactive_mode(ruckus)


if __name__ == "__main__":
    main()
