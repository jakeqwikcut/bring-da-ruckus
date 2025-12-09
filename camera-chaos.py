#!/usr/bin/env python3
"""
Bring Da Ruckus - Camera Specific Edition
Apply chaos ONLY to traffic from specific camera IP (simulates bad LAN/WiFi repeater)
"""

import subprocess
import sys

CAMERA_IP = "192.168.1.78"  # Your Axis camera

def apply_camera_chaos(loss_percent):
    """Apply packet loss only to traffic from camera"""
    chain = "CAMERA_CHAOS"
    
    # Create chain
    subprocess.run(f"iptables -N {chain}", shell=True, stderr=subprocess.DEVNULL)
    subprocess.run(f"iptables -F {chain}", shell=True, stderr=subprocess.DEVNULL)
    
    # Drop packets from camera with probability
    probability = loss_percent / 100.0
    subprocess.run(
        f"iptables -A {chain} -s {CAMERA_IP} -m statistic --mode random --probability {probability} -j DROP",
        shell=True, check=True
    )
    
    # Apply to INPUT (packets coming from camera to Jetson)
    subprocess.run(f"iptables -I INPUT -j {chain}", shell=True, check=True)
    
    print(f"✅ Applying {loss_percent}% packet loss to traffic FROM {CAMERA_IP}")
    print(f"   Camera → Jetson link now has chaos")
    print(f"   Jetson → Server link is NORMAL")

def clear_camera_chaos():
    """Clear all camera chaos rules"""
    chain = "CAMERA_CHAOS"
    subprocess.run(f"iptables -D INPUT -j {chain}", shell=True, stderr=subprocess.DEVNULL)
    subprocess.run(f"iptables -F {chain}", shell=True, stderr=subprocess.DEVNULL)
    subprocess.run(f"iptables -X {chain}", shell=True, stderr=subprocess.DEVNULL)
    print(f"✅ Cleared all chaos for {CAMERA_IP}")

def show_status():
    """Show current iptables rules"""
    print("\n📊 Current iptables rules for camera:")
    subprocess.run(f"iptables -L CAMERA_CHAOS -n -v 2>/dev/null || echo 'No chaos active'", shell=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"""
╔════════════════════════════════════════════════════════════════╗
║  Camera-Specific Chaos Tool                                    ║
║  Target: {CAMERA_IP}                                    ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  Usage:                                                        ║
║    sudo python3 camera-chaos.py <percent>                      ║
║    sudo python3 camera-chaos.py clear                          ║
║    sudo python3 camera-chaos.py status                         ║
║                                                                ║
║  Examples:                                                     ║
║    sudo python3 camera-chaos.py 1      # 1% loss              ║
║    sudo python3 camera-chaos.py 9      # 9% loss              ║
║    sudo python3 camera-chaos.py 18     # 18% loss             ║
║    sudo python3 camera-chaos.py clear  # Remove chaos         ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
""")
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "clear":
        clear_camera_chaos()
    elif cmd == "status":
        show_status()
    else:
        try:
            loss = int(cmd)
            if loss < 0 or loss > 100:
                print("❌ Loss percent must be 0-100")
                sys.exit(1)
            clear_camera_chaos()  # Clear old rules first
            if loss > 0:
                apply_camera_chaos(loss)
        except ValueError:
            print("❌ Invalid command. Use a number (0-100), 'clear', or 'status'")
            sys.exit(1)
