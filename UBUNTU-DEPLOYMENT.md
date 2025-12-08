# Ubuntu Server Deployment Guide

## Overview

Deploy **Bring Da Ruckus** on your Ubuntu server to simulate network chaos for testing your QwikCut camera system. The server acts as the chaos generator on your LAN.

## Network Architecture

```
[QwikCam] <--ethernet--> [Ubuntu Server] <---> [Router] <---> [Internet/Cloud]
     192.168.1.100      (Run tool here)                      (Backend/S3)
                          eth0 (chaos!)
```

When you run the tool on the Ubuntu server, it disrupts **all traffic** flowing through the specified network interface, affecting the QwikCam's connection to the cloud.

## Prerequisites

- Ubuntu Server 18.04+ (or any Debian-based Linux)
- Root/sudo access
- Python 3.7+
- Network interface connected to the same LAN as QwikCam
- SSH access for remote management

## Installation Steps

### 1. Prepare Your Ubuntu Server

```bash
# Update system
sudo apt-get update

# Install required packages (if not already present)
sudo apt-get install -y python3 iproute2 openssh-server

# Verify Python version
python3 --version  # Should be 3.7 or higher

# Verify tc is available
tc -Version
```

### 2. Transfer the Tool

**Option A: Via SCP from your Windows PC**
```bash
# From Windows PowerShell
scp bring-da-ruckus.py user@server-ip:/home/user/
```

**Option B: Via Git**
```bash
# On the server
cd ~
git clone <your-repo-url>
cd bring-da-ruckus
```

**Option C: Via USB/Manual Copy**
```bash
# Mount USB and copy files
sudo mount /dev/sdb1 /mnt
cp /mnt/bring-da-ruckus.py ~/
```

### 3. Setup on Server

```bash
# Make executable
chmod +x bring-da-ruckus.py

# Test it (will show error message but verify it runs)
python3 bring-da-ruckus.py
# Should show: "ERROR: This tool requires sudo/root privileges"

# Test with sudo
sudo python3 bring-da-ruckus.py
# Should show the interactive menu
```

### 4. Identify Your Network Interface

```bash
# Show all interfaces
ip link show

# Find the default route interface (usually this is the one you want)
ip route show default
# Output: "default via 192.168.1.1 dev eth0 ..."
#                                      ^^^^^ - this is your interface

# Check interface status
ip addr show eth0
```

Common interface names:
- `eth0` - Traditional Ethernet
- `enp0s3` - PCI Ethernet (common in VMs)
- `ens33` - Another naming scheme
- `eno1` - Onboard Ethernet

### 5. First Test Run

```bash
# Run with interface specified
sudo python3 bring-da-ruckus.py --interface eth0

# In the menu:
# Press '1' for Chill (no disruption - test the tool works)
# Press 's' for status
# Press 'q' to quit
```

## Usage Patterns

### Interactive Mode (Recommended)

```bash
# SSH into server
ssh user@server-ip

# Run the tool
sudo python3 bring-da-ruckus.py --interface eth0

# Control via menu while monitoring QwikCam from another terminal/PC
```

### Non-Interactive Mode (Quick Tests)

```bash
# Start with a specific level and timeout
sudo python3 bring-da-ruckus.py --level moderate --timeout 15

# Then interact with the menu or let deadman's switch handle cleanup
```

### Multiple SSH Sessions

**Session 1: Run the chaos tool**
```bash
ssh user@server-ip
sudo python3 bring-da-ruckus.py
```

**Session 2: Monitor effects**
```bash
ssh user@server-ip
watch -n 1 ping -c 3 192.168.1.100  # Monitor QwikCam
```

**Session 3: View tc status**
```bash
ssh user@server-ip
sudo tc -s qdisc show dev eth0  # View traffic control stats
```

## Network Configuration Considerations

### If Server is a Router/Gateway

If your Ubuntu server routes traffic for the QwikCam:
```bash
# Enable IP forwarding (if not already enabled)
sudo sysctl -w net.ipv4.ip_forward=1

# Make permanent
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
```

Configure QwikCam to use server as gateway, then all traffic flows through it.

### If Server is on Same LAN (Peer)

The tool affects the server's own interface. To affect other devices:
- Use iptables to redirect traffic through the server, OR
- Accept that disruptions affect all devices on the network segment

## Testing Workflow

### Typical Test Session

1. **Setup monitoring** (from Windows PC or another SSH session):
   ```bash
   # Continuous ping to QwikCam
   ping -t 192.168.1.100

   # Or on Linux
   ping 192.168.1.100
   ```

2. **Start the chaos tool** (on Ubuntu server):
   ```bash
   sudo python3 bring-da-ruckus.py --interface eth0 --timeout 30
   ```

3. **Apply disruption levels progressively**:
   - Start with Level 2 (Light)
   - Watch QwikCam stream quality
   - Increase to Level 3 (Moderate)
   - Monitor upload behavior
   - Continue as needed

4. **Clear and document**:
   - Press 'c' to clear disruptions
   - Press 's' to verify clear
   - Document observations
   - Press 'q' to quit

## Safety & Best Practices

### Deadman's Switch

- Default: 30 minutes of inactivity triggers auto-cleanup
- Adjust with `--timeout` flag
- Resets on any menu interaction
- Essential for unattended tests

### Emergency Recovery

**If you lose SSH connection:**
1. Deadman's switch will auto-clear after timeout
2. Or physically access server and reboot
3. Or SSH from another machine on different network

**Manual cleanup if needed:**
```bash
# SSH in from another session
ssh user@server-ip

# Clear tc rules manually
sudo tc qdisc del dev eth0 root

# Verify cleared
tc qdisc show dev eth0
```

### Running as Systemd Service (Advanced)

For automated testing, create a service:

```bash
# Create service file
sudo nano /etc/systemd/system/bring-da-ruckus.service
```

```ini
[Unit]
Description=Bring Da Ruckus Network Chaos
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/user
ExecStart=/usr/bin/python3 /home/user/bring-da-ruckus.py --level moderate --timeout 60 --interface eth0
Restart=no

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl daemon-reload
sudo systemctl start bring-da-ruckus
sudo systemctl status bring-da-ruckus

# Stop
sudo systemctl stop bring-da-ruckus
```

## Verification Commands

### Check if tc rules are active:
```bash
sudo tc qdisc show dev eth0
```

### View detailed statistics:
```bash
sudo tc -s qdisc show dev eth0
```

### Test from another machine:
```bash
# Ping QwikCam to see latency/loss
ping 192.168.1.100

# With statistics
ping -c 100 192.168.1.100

# Continuous with summary
ping 192.168.1.100 | while read line; do
    echo "$(date): $line"
done
```

### Monitor network traffic:
```bash
# Install if needed
sudo apt-get install iftop

# Monitor interface
sudo iftop -i eth0

# Or use tcpdump
sudo tcpdump -i eth0 host 192.168.1.100
```

## Troubleshooting

### "Cannot find device eth0"
- Wrong interface name
- Use `ip link show` to find correct name
- May be `enp0s3`, `ens33`, etc.

### "Operation not permitted"
- Forgot `sudo`
- Must be root for tc commands

### "tc command not found"
```bash
sudo apt-get install iproute2
```

### Disruptions not affecting QwikCam
- Verify QwikCam traffic goes through this interface
- Check with: `sudo tcpdump -i eth0 host 192.168.1.100`
- May need to route traffic differently

### Server becomes unresponsive
- Deadman's switch should clear
- Or reboot server
- Consider lowering disruption levels

## Performance Tips

### For Long-Running Tests

```bash
# Use screen or tmux to persist session
sudo apt-get install screen

# Start screen session
screen -S chaos

# Run tool
sudo python3 bring-da-ruckus.py

# Detach: Ctrl+A, then D
# Reattach: screen -r chaos
```

### For Automated Testing

Create a test script:
```bash
#!/bin/bash
# test-sequence.sh

echo "Starting automated chaos testing..."

# Test 1: Light (10 min)
sudo python3 bring-da-ruckus.py --level light --timeout 10 &
sleep 600
killall python3

# Test 2: Moderate (10 min)
sudo python3 bring-da-ruckus.py --level moderate --timeout 10 &
sleep 600
killall python3

# Test 3: Heavy (10 min)
sudo python3 bring-da-ruckus.py --level heavy --timeout 10 &
sleep 600
killall python3

echo "Automated testing complete!"
```

## Security Considerations

- Tool requires root access
- Only run on trusted/isolated networks
- Don't expose server to internet while testing
- Consider firewall rules to protect SSH access
- Use key-based SSH authentication

## Summary Checklist

- [ ] Ubuntu server on same LAN as QwikCam
- [ ] Python 3.7+ installed
- [ ] iproute2/tc installed
- [ ] Tool copied to server
- [ ] Network interface identified
- [ ] SSH access working
- [ ] First test run successful
- [ ] Monitoring setup (ping, stream viewer)
- [ ] Deadman timeout configured appropriately
- [ ] Emergency recovery plan understood

**Now you're ready to bring da ruckus to your network! 🥷**
