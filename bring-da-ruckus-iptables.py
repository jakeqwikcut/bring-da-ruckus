#!/usr/bin/env python3
"""
Bring Da Ruckus - iptables Edition
Network Chaos Engineering Tool for systems without netem kernel module
Uses iptables for packet loss simulation (works on Jetson, embedded devices, etc.)

Note: This version only supports packet loss chaos, not latency/jitter/bandwidth
"""

import subprocess
import time
import sys
import os
import signal
from datetime import datetime
from typing import Optional
from threading import Thread

class ChaosChamber:
    """Wu-Tang inspired chaos levels - iptables edition (packet loss only)"""

    PEACE = {
        'name': '0. ☯️  Enter the Peace (No Chaos)',
        'number': 0,
        'packet_loss_pct': 0,
        'description': 'Restore harmony to the network'
    }

    SWARM = {
        'name': '1. 🐝 The Swarm (Minor Disruption)',
        'number': 1,
        'packet_loss_pct': 1,
        'description': '1% packet loss - Annoying but survivable'
    }

    MYSTERY = {
        'name': '2. 🌫️  The Mystery (Moderate Chaos)',
        'number': 2,
        'packet_loss_pct': 9,
        'description': '9% packet loss - Streams start stuttering'
    }

    VENOMS = {
        'name': '3. 🐍 The 5 Deadly Venoms (Serious Degradation)',
        'number': 3,
        'packet_loss_pct': 18,
        'description': '18% packet loss - Severe quality issues'
    }

    SWORDS = {
        'name': '4. ⚔️  The 36 Swords (Heavy Chaos)',
        'number': 4,
        'packet_loss_pct': 36,
        'description': '36% packet loss - Connection barely usable'
    }

    SHAOLIN = {
        'name': '5. ☠️  Shaolin Shadow (Complete Outage)',
        'number': 5,
        'packet_loss_pct': 100,
        'description': '100% packet loss - Total network failure (SSH protected)'
    }

    @classmethod
    def all_chambers(cls):
        return [cls.PEACE, cls.SWARM, cls.MYSTERY, cls.VENOMS, cls.SWORDS, cls.SHAOLIN]


class DeadmanSwitch:
    """Safety mechanism that auto-clears chaos after timeout"""

    def __init__(self, timeout_minutes: int, emergency_callback):
        self.timeout_minutes = timeout_minutes
        self.emergency_callback = emergency_callback
        self.last_activity = datetime.now()
        self.running = False
        self.thread = None
        self.warning_shown = False

    def start(self):
        """Start the deadman's switch monitoring"""
        self.running = True
        self.last_activity = datetime.now()
        self.thread = Thread(target=self._monitor, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop monitoring"""
        self.running = False

    def reset(self):
        """Reset the activity timer"""
        self.last_activity = datetime.now()
        self.warning_shown = False

    def _monitor(self):
        """Monitor for timeout"""
        while self.running:
            elapsed = (datetime.now() - self.last_activity).total_seconds()
            remaining = (self.timeout_minutes * 60) - elapsed

            # Warning at 30 seconds
            if remaining <= 30 and not self.warning_shown:
                self.warning_shown = True
                print(f"\n⚠️  WARNING: Deadman's switch triggering in {int(remaining)} seconds!")
                print(f"⚠️  Press any key to reset, or 'Y' to confirm and continue...")

            if remaining <= 0:
                print("\n🚨 DEADMAN'S SWITCH TRIGGERED - AUTO-CLEARING CHAOS!")
                self.emergency_callback()
                break

            time.sleep(1)


class NetworkRuckus:
    """iptables-based network chaos for systems without netem"""

    def __init__(self, interface: Optional[str] = None, deadman_timeout: int = 5):
        self.interface = interface
        self.current_chamber = ChaosChamber.PEACE
        self.is_active = False
        self.deadman = DeadmanSwitch(deadman_timeout, self._emergency_stop)
        self.ssh_client_ip = self._detect_ssh_client_ip()
        self.management_whitelist = [self.ssh_client_ip] if self.ssh_client_ip else []
        self.ssh_protection_enabled = True
        self.iptables_chain = "BRING_DA_RUCKUS"

    def _detect_ssh_client_ip(self):
        """Detect the IP address of the SSH client for protection"""
        try:
            ssh_client = os.environ.get('SSH_CLIENT', '').split()[0]
            if ssh_client:
                return ssh_client

            result = subprocess.run(
                ["who", "am", "i"],
                capture_output=True, text=True
            )
            import re
            match = re.search(r'\((\d+\.\d+\.\d+\.\d+)\)', result.stdout)
            if match:
                return match.group(1)
        except Exception:
            pass
        return None

    def detect_interface(self):
        """Auto-detect the primary network interface"""
        try:
            result = subprocess.run(
                ["ip", "route", "show", "default"],
                capture_output=True, text=True, check=True
            )
            interface = result.stdout.split()[4]
            return interface
        except:
            return "eth0"

    def _setup_iptables_chain(self):
        """Create custom iptables chain for chaos rules"""
        # Create chain if it doesn't exist
        subprocess.run(
            f"iptables -N {self.iptables_chain}",
            shell=True, stderr=subprocess.DEVNULL
        )

        # Clear any existing rules in the chain
        subprocess.run(
            f"iptables -F {self.iptables_chain}",
            shell=True, stderr=subprocess.DEVNULL
        )

    def apply_ruckus(self, level: dict):
        """Apply packet loss using iptables probability matching"""
        print(f"\n🔧 Applying: {level['name']}")

        if not self.interface:
            self.interface = self.detect_interface()

        # Clear existing chaos
        self.clear_ruckus()

        if level['packet_loss_pct'] == 0:
            print(f"   ✅ All chaos cleared on {self.interface}")
            print(f"   ☯️  Network has returned to peace")
            self.current_chamber = level
            self.is_active = False
            return True

        # Setup iptables chain
        self._setup_iptables_chain()

        if level['packet_loss_pct'] == 100:
            # Complete outage - CRITICAL: Protect SSH access!
            print(f"\n{'='*70}")
            print(f"⚠️  ☠️  CRITICAL: APPLYING SHAOLIN SHADOW ☠️  ⚠️")
            print(f"{'='*70}")

            if self.ssh_protection_enabled:
                # Whitelist SSH port 22
                subprocess.run(
                    f"iptables -I INPUT -p tcp --dport 22 -j ACCEPT",
                    shell=True, stderr=subprocess.DEVNULL
                )
                subprocess.run(
                    f"iptables -I OUTPUT -p tcp --sport 22 -j ACCEPT",
                    shell=True, stderr=subprocess.DEVNULL
                )

                # Whitelist management IPs
                for mgmt_ip in self.management_whitelist:
                    subprocess.run(
                        f"iptables -I INPUT -s {mgmt_ip} -j ACCEPT",
                        shell=True, stderr=subprocess.DEVNULL
                    )
                    subprocess.run(
                        f"iptables -I OUTPUT -d {mgmt_ip} -j ACCEPT",
                        shell=True, stderr=subprocess.DEVNULL
                    )

                print(f"   🛡️  SSH (port 22) protected from chaos")
                if self.ssh_client_ip:
                    print(f"   🛡️  Management IP {self.ssh_client_ip} whitelisted")

            # Drop all other packets
            subprocess.run(
                f"iptables -A INPUT -i {self.interface} -j DROP",
                shell=True, check=True
            )
            subprocess.run(
                f"iptables -A OUTPUT -o {self.interface} -j DROP",
                shell=True, check=True
            )

            print(f"   ☠️  Complete network outage on {self.interface}")
            print(f"   ⚠️  SSH access maintained via iptables exemption")
            print(f"{'='*70}\n")

        else:
            # Partial packet loss using statistic module
            # Convert percentage to probability for iptables (--probability expects 0.0-1.0, e.g. 0.01 = 1% drop rate)
            probability = level['packet_loss_pct'] / 100.0

            # Drop packets randomly based on probability
            subprocess.run(
                f"iptables -A {self.iptables_chain} -m statistic --mode random --probability {probability} -j DROP",
                shell=True, check=True
            )

            # Jump to our chain for incoming and outgoing
            subprocess.run(
                f"iptables -I INPUT -i {self.interface} -j {self.iptables_chain}",
                shell=True, check=True
            )
            subprocess.run(
                f"iptables -I OUTPUT -o {self.interface} -j {self.iptables_chain}",
                shell=True, check=True
            )

            print(f"   ✅ Applied on interface: {self.interface}")
            print(f"   📉 Packet Loss: {level['packet_loss_pct']}%")

        self.current_chamber = level
        self.is_active = (level != ChaosChamber.PEACE)
        self.deadman.reset()
        return True

    def clear_ruckus(self):
        """Clear all iptables chaos rules"""
        print("\n🧹 Clearing all network disruptions...")

        if not self.interface:
            self.interface = self.detect_interface()

        # Remove jumps to our chain
        subprocess.run(
            f"iptables -D INPUT -i {self.interface} -j {self.iptables_chain}",
            shell=True, stderr=subprocess.DEVNULL
        )
        subprocess.run(
            f"iptables -D OUTPUT -o {self.interface} -j {self.iptables_chain}",
            shell=True, stderr=subprocess.DEVNULL
        )

        # Flush and delete our chain
        subprocess.run(
            f"iptables -F {self.iptables_chain}",
            shell=True, stderr=subprocess.DEVNULL
        )
        subprocess.run(
            f"iptables -X {self.iptables_chain}",
            shell=True, stderr=subprocess.DEVNULL
        )

        # Clear any DROP rules on interface
        subprocess.run(
            f"iptables -D INPUT -i {self.interface} -j DROP",
            shell=True, stderr=subprocess.DEVNULL
        )
        subprocess.run(
            f"iptables -D OUTPUT -o {self.interface} -j DROP",
            shell=True, stderr=subprocess.DEVNULL
        )

        # Clear SSH protection rules
        if self.ssh_protection_enabled:
            subprocess.run(
                "iptables -D INPUT -p tcp --dport 22 -j ACCEPT",
                shell=True, stderr=subprocess.DEVNULL
            )
            subprocess.run(
                "iptables -D OUTPUT -p tcp --sport 22 -j ACCEPT",
                shell=True, stderr=subprocess.DEVNULL
            )

            for mgmt_ip in self.management_whitelist:
                subprocess.run(
                    f"iptables -D INPUT -s {mgmt_ip} -j ACCEPT",
                    shell=True, stderr=subprocess.DEVNULL
                )
                subprocess.run(
                    f"iptables -D OUTPUT -d {mgmt_ip} -j ACCEPT",
                    shell=True, stderr=subprocess.DEVNULL
                )

        print(f"   ✅ Network restored to normal on {self.interface}")
        print(f"   ☯️  Peace has been restored to the chambers")

        self.is_active = False
        self.current_chamber = ChaosChamber.PEACE

    def _emergency_stop(self):
        """Emergency stop triggered by deadman's switch"""
        print("\n🚨 EMERGENCY STOP - Clearing all ruckus!")
        self.clear_ruckus()
        self.is_active = False

    def show_iptables_status(self):
        """Show current iptables rules"""
        print("\n📊 Current iptables Rules:\n")
        subprocess.run("iptables -L -n -v | head -50", shell=True)

    def get_status(self):
        """Get current status"""
        status = f"\n{'='*60}\n"
        status += f"🥷 BRING DA RUCKUS - iptables Edition - Status\n"
        status += f"{'='*60}\n"
        status += f"Current Chamber: {self.current_chamber['name']}\n"
        status += f"Active: {'🟢 YES' if self.is_active else '🔴 NO'}\n"
        status += f"Interface: {self.interface or 'Auto-detect'}\n"
        status += f"Method: iptables (no netem required)\n"
        status += f"SSH Protection: {'🛡️  ENABLED' if self.ssh_protection_enabled else '❌ DISABLED'}\n"
        if self.ssh_client_ip:
            status += f"Your IP: {self.ssh_client_ip} (whitelisted)\n"
        status += f"Deadman Timeout: {self.deadman.timeout_minutes} minutes\n"

        if self.is_active:
            elapsed = (datetime.now() - self.deadman.last_activity).total_seconds() / 60
            remaining = self.deadman.timeout_minutes - elapsed
            status += f"Time Since Activity: {elapsed:.1f} min\n"
            status += f"Time Until Auto-Clear: {remaining:.1f} min\n"

        status += f"{'='*60}\n"
        return status


def show_banner():
    """Display Wu-Tang inspired ASCII banner"""
    banner = """
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
██                     iptables Edition (No netem)                            ██
██                                                                            ██
████████████████████████████████████████████████████████████████████████████████

"Protect Ya Neck... and Protect Ya SSH"

⚠️  iptables Edition - For systems without netem kernel module
    (Jetson, embedded devices, minimal kernels)

    Supports: Packet Loss only (SSH protected)
    Does NOT support: Latency, Jitter, Bandwidth limiting

"""
    print(banner)


def show_menu():
    """Display interactive menu"""
    menu = """
╔════════════════════════════════════════════════════════════════════════════╗
║  🥷 SELECT YOUR CHAMBER (iptables Packet Loss)                             ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
"""
    chambers = ChaosChamber.all_chambers()
    for chamber in chambers:
        menu += f"║  [{chamber['number']}] {chamber['name']:<70} ║\n"
        menu += f"║      → {chamber['description']:<66} ║\n"
        menu += f"║                                                                            ║\n"

    menu += """╠════════════════════════════════════════════════════════════════════════════╣
║  [s] Show Status      [c] Clear All      [d] Show iptables                ║
║  [i] Set Interface    [q] Quit                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""
    print(menu)


def interactive_mode(ruckus: NetworkRuckus):
    """Run interactive CLI mode"""
    print("\n🎬 Starting interactive mode...")
    print(f"⏰ Deadman's switch active: {ruckus.deadman.timeout_minutes} minutes")
    print(f"🔧 Interface: {ruckus.interface or 'Auto-detect'}")
    print(f"⚙️  Method: iptables (no netem required)")

    ruckus.deadman.start()

    try:
        while True:
            show_menu()
            choice = input("\n👉 Enter your choice: ").strip().lower()

            ruckus.deadman.reset()

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
                ruckus.show_iptables_status()

            elif choice == 'i':
                interface = input("Enter network interface name: ").strip()
                if interface:
                    ruckus.interface = interface
                    print(f"🔧 Interface set to: {interface}")

            elif choice.isdigit():
                chamber_idx = int(choice)
                chambers = ChaosChamber.all_chambers()
                if 0 <= chamber_idx < len(chambers):
                    chamber = chambers[chamber_idx]

                    # CRITICAL SAFETY: Confirm Shaolin Shadow
                    if chamber['packet_loss_pct'] == 100:
                        print("\n" + "="*70)
                        print("⚠️  ☠️  CRITICAL WARNING: SHAOLIN SHADOW ☠️  ⚠️")
                        print("="*70)
                        print("You are about to apply 100% PACKET LOSS!")
                        print()
                        print("THIS WILL BLOCK ALL NETWORK TRAFFIC!")
                        print()
                        print(f"SSH Protection: {'🛡️  ENABLED' if ruckus.ssh_protection_enabled else '❌ DISABLED'}")
                        if ruckus.ssh_client_ip:
                            print(f"Your IP: {ruckus.ssh_client_ip} (will be whitelisted)")
                        else:
                            print("⚠️  Could not detect your SSH IP - protection may fail!")
                        print()
                        print("Are you ABSOLUTELY SURE you want to proceed?")
                        print("="*70)

                        confirm = input("Type 'YES I AM SURE' to continue: ").strip()
                        if confirm != "YES I AM SURE":
                            print("❌ Shaolin Shadow cancelled - wisdom prevails")
                            continue

                        print("\n🔥 Applying Shaolin Shadow in 3 seconds... (Ctrl+C to abort)")
                        for i in range(3, 0, -1):
                            print(f"   {i}...")
                            time.sleep(1)

                    ruckus.apply_ruckus(chamber)
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
    """Main entry point"""
    show_banner()

    # Check for root
    if os.geteuid() != 0:
        print("❌ This tool requires root privileges")
        print("   Please run with sudo:")
        print(f"   sudo python3 {sys.argv[0]}")
        sys.exit(1)

    # Create ruckus instance
    ruckus = NetworkRuckus(deadman_timeout=5)

    # Auto-detect interface
    if not ruckus.interface:
        ruckus.interface = ruckus.detect_interface()

    print(f"\n🔍 Detected interface: {ruckus.interface}")
    if ruckus.ssh_client_ip:
        print(f"🛡️  SSH client IP detected: {ruckus.ssh_client_ip}")
    else:
        print(f"⚠️  Could not detect SSH client IP - Shaolin Shadow may lock you out!")

    # Setup signal handlers
    def signal_handler(sig, frame):
        print("\n\n🛑 Signal received! Cleaning up...")
        ruckus.clear_ruckus()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start interactive mode
    interactive_mode(ruckus)


if __name__ == "__main__":
    main()
