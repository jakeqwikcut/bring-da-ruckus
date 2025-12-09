#!/usr/bin/env python3
"""
Bring Da Ruckus - Camera Specific Edition
Apply chaos ONLY to traffic from specific camera IP (simulates bad LAN/WiFi repeater)
"""

import subprocess
import sys
import os
import re

def validate_ip(ip):
    """Validate IP address format"""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    parts = ip.split('.')
    return all(0 <= int(part) <= 255 for part in parts)

def apply_camera_chaos(camera_ip, loss_percent):
    """Apply packet loss only to traffic from camera"""
    chain = "CAMERA_CHAOS"

    # Create chain
    subprocess.run(f"iptables -N {chain}", shell=True, stderr=subprocess.DEVNULL)
    subprocess.run(f"iptables -F {chain}", shell=True, stderr=subprocess.DEVNULL)

    # Drop packets from camera with probability
    probability = loss_percent / 100.0
    subprocess.run(
        f"iptables -A {chain} -s {camera_ip} -m statistic --mode random --probability {probability} -j DROP",
        shell=True, check=True
    )

    # Apply to INPUT (packets coming from camera to Jetson)
    subprocess.run(f"iptables -I INPUT -j {chain}", shell=True, check=True)

    print(f"\n✅ Applying {loss_percent}% packet loss to traffic FROM {camera_ip}")
    print(f"   📹 Camera → Jetson link now has chaos")
    print(f"   🌐 Jetson → Server link is NORMAL")

def clear_camera_chaos(camera_ip):
    """Clear all camera chaos rules"""
    chain = "CAMERA_CHAOS"
    subprocess.run(f"iptables -D INPUT -j {chain}", shell=True, stderr=subprocess.DEVNULL)
    subprocess.run(f"iptables -F {chain}", shell=True, stderr=subprocess.DEVNULL)
    subprocess.run(f"iptables -X {chain}", shell=True, stderr=subprocess.DEVNULL)
    print(f"\n✅ Cleared all chaos for {camera_ip}")

def show_status():
    """Show current iptables rules"""
    print("\n📊 Current iptables rules for camera:")
    subprocess.run(f"iptables -L CAMERA_CHAOS -n -v 2>/dev/null || echo 'No chaos active'", shell=True)

def show_menu():
    """Display interactive menu"""
    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║  📹 Camera Chaos - Wu-Tang Style                               ║")
    print("╠════════════════════════════════════════════════════════════════╣")
    print("║                                                                ║")
    print("║  [1] The Swarm (1% loss)                                       ║")
    print("║  [2] The Mystery (9% loss)                                     ║")
    print("║  [3] The 5 Deadly Venoms (18% loss)                            ║")
    print("║  [4] The 36 Swords (36% loss)                                  ║")
    print("║  [5] Shaolin Shadow (100% loss)                                ║")
    print("║                                                                ║")
    print("║  [s] Show Status      [c] Clear All      [q] Quit             ║")
    print("╚════════════════════════════════════════════════════════════════╝")

def interactive_mode(camera_ip):
    """Run interactive mode"""
    print("\n🎬 Interactive mode - Camera Chaos")
    print(f"🎯 Target: {camera_ip}")
    print(f"📹 Affecting: Camera → Jetson only")
    print(f"🌐 Normal: Jetson → Server (your stream upload is fine)")

    chambers = {
        '1': ('The Swarm', 1),
        '2': ('The Mystery', 9),
        '3': ('The 5 Deadly Venoms', 18),
        '4': ('The 36 Swords', 36),
        '5': ('Shaolin Shadow', 100)
    }

    try:
        while True:
            show_menu()
            choice = input("\n👉 Enter your choice: ").strip().lower()

            if choice == 'q':
                print("\n👋 Exiting and cleaning up...")
                clear_camera_chaos(camera_ip)
                break

            elif choice == 's':
                show_status()

            elif choice == 'c':
                clear_camera_chaos(camera_ip)

            elif choice in chambers:
                name, loss = chambers[choice]
                print(f"\n🥋 Applying: {name}")
                clear_camera_chaos(camera_ip)  # Clear old first
                apply_camera_chaos(camera_ip, loss)

            else:
                print("❌ Invalid choice")

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted! Cleaning up...")
        clear_camera_chaos(camera_ip)

if __name__ == "__main__":
    # Check for root
    if os.geteuid() != 0:
        print("❌ This tool requires root privileges")
        print("   Please run with sudo:")
        print(f"   sudo python3 {sys.argv[0]}")
        sys.exit(1)

    # Show banner
    print("\n████████████████████████████████████████████████████████████████")
    print("██                                                            ██")
    print("██                    CAMERA CHAOS TOOL                       ██")
    print("██                   Wu-Tang Sword Style                      ██")
    print("██                                                            ██")
    print("████████████████████████████████████████████████████████████████")
    print()

    # Get camera IP
    if len(sys.argv) > 1:
        camera_ip = sys.argv[1]
    else:
        camera_ip = input("📹 Enter camera IP address: ").strip()
        if not camera_ip:
            print("❌ No IP address provided")
            sys.exit(1)
    
    # Validate IP address
    if not validate_ip(camera_ip):
        print(f"❌ Invalid IP address: {camera_ip}")
        print("   Please enter a valid IPv4 address (e.g., 192.168.1.100)")
        sys.exit(1)

    # Wu-Tang quote
    print()
    print("🥋 \"En garde, I'll let you try my Wu-Tang style\"")
    print()
    input("Press ENTER to continue...")

    # Start interactive mode
    interactive_mode(camera_ip)