```
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
```

## Overview

Bring Da Ruckus is a network chaos engineering tool designed to test QwikCut camera systems under adverse network conditions. Deploy it on your Ubuntu server to simulate real-world network problems that can affect video streaming, recording quality, and cloud synchronization.

## Features

- **36 Chambers of Chaos**: Six progressive disruption levels inspired by Wu-Tang
- **Interactive CLI**: Real-time control with on-the-fly chamber transitions
- **Deadman's Switch**: Automatic safety shutdown after inactivity
- **Network Disruptions**:
  - Latency (ping delay)
  - Packet loss
  - Bandwidth throttling
  - Jitter
  - Complete network outages

## Installation

### Prerequisites

**Ubuntu Server (or any Linux distribution):**
- Python 3.7+
- `sudo` access (required)
- `tc` (traffic control) utility from iproute2 (usually pre-installed)

### Setup

```bash
# On your Ubuntu server
cd /path/to/bring-da-ruckus

# Ensure tc is installed
sudo apt-get install iproute2

# Make executable
chmod +x bring-da-ruckus.py

# No additional Python dependencies required - uses standard library only!
```

## Usage

### Basic Interactive Mode

```bash
# Run with sudo (required for tc command)
sudo python3 bring-da-ruckus.py
```

### Advanced Options

```bash
# Start with a specific ruckus level
sudo python3 bring-da-ruckus.py --level moderate

# Set custom deadman timeout (15 minutes)
sudo python3 bring-da-ruckus.py --timeout 15

# Specify network interface
sudo python3 bring-da-ruckus.py --interface eth0

# Target specific IP (QwikCam IP) - not yet fully implemented
sudo python3 bring-da-ruckus.py --target 192.168.1.100

# Combine options
sudo python3 bring-da-ruckus.py --level heavy --timeout 10 --interface enp0s3
```

## The 36 Chambers of Chaos

### ☯️ Chamber 0: Peace (Normal Network)
- No disruptions
- Baseline for comparison
- **Use case**: Verify system works normally

### 🥋 Chamber 1: The Swarm (Light Disruption)
- Latency: 50ms
- Packet Loss: 1%
- Bandwidth: 50 Mbps
- Jitter: 10ms
- **Use case**: Typical consumer internet, light congestion

### ⚔️ Chamber 9: The Mystery (Moderate Chaos)
- Latency: 150ms
- Packet Loss: 3%
- Bandwidth: 10 Mbps
- Jitter: 25ms
- **Use case**: Congested network, multiple devices streaming

### 🔥 Chamber 18: The Deadly Venoms (Heavy Ruckus)
- Latency: 300ms
- Packet Loss: 8%
- Bandwidth: 2 Mbps
- Jitter: 50ms
- **Use case**: Poor connection, distant cell tower, overloaded wifi

### 💀 Chamber 36: Liquid Swords (Extreme Chaos)
- Latency: 500ms
- Packet Loss: 15%
- Bandwidth: 512 Kbps
- Jitter: 100ms
- **Use case**: Terrible connection, rural/remote deployment

### ☠️ Shaolin Shadow: Total Darkness (Complete Outage)
- Packet Loss: 100%
- **Use case**: Total network failure, test autonomous mode

## Interactive Commands

Once in interactive mode:

- **1-6**: Select ruckus level
- **s**: Show current status and statistics
- **c**: Clear all ruckus (restore normal network)
- **t**: Set target IP address (optional)
- **i**: Set network interface
- **q**: Quit and clean up

## Deadman's Switch

The deadman's switch is a **critical safety feature** that automatically stops all network disruptions if the operator becomes inactive.

- Default timeout: **30 minutes**
- Resets on any user interaction
- Prevents accidental long-term network disruption
- Customize with `--timeout` flag

## Testing Scenarios for QwikCut

### Scenario 1: Stream Quality Degradation
```bash
sudo python3 bring-da-ruckus.py --level first
```
Monitor RTSP stream quality. Does it degrade gracefully?

### Scenario 2: Upload Queue Buildup
```bash
sudo python3 bring-da-ruckus.py --level ninth
```
Check if video clips queue up properly when bandwidth is limited.

### Scenario 3: Command Latency
```bash
sudo python3 bring-da-ruckus.py --level eighteenth
```
Test WebSocket command responsiveness with high latency.

### Scenario 4: Complete Outage Recovery
```bash
sudo python3 bring-da-ruckus.py --level shaolin
```
Verify autonomous recording continues and syncs when connection restored.

### Scenario 5: Intermittent Issues
Start at Chamber 1, gradually increase to Chamber 18, then back down. Monitor system behavior through transitions.

## How It Works

### Ubuntu/Linux Implementation
Uses `tc` (traffic control) with `netem` (network emulation):
- Adds queuing disciplines (qdisc) to network interface
- `netem` handles latency, jitter, and packet loss
- `tbf` (token bucket filter) handles bandwidth throttling
- All disruptions are temporary and automatically cleaned up on exit
- Works at the kernel level for realistic network simulation

**Technical Details:**
- Modifies the qdisc (queuing discipline) on your network interface
- Applies rules that delay, drop, or limit packets
- Changes are live and immediate
- Completely reversible - no permanent changes to system

## Safety Features

1. **Deadman's Switch**: Auto-shutdown on inactivity
2. **Clean Exit**: Ctrl+C gracefully restores network
3. **Status Monitoring**: Always see what's active
## Troubleshooting

### "Operation not permitted" or "Permission denied"
- Must run with `sudo`: `sudo python3 bring-da-ruckus.py`
- The tool requires root privileges for tc commands

### "tc command not found"
- Install iproute2: `sudo apt-get install iproute2`
- On some systems it may be: `sudo yum install iproute`

### Network Not Disrupting
- Verify correct interface: `ip link show`
- Check interface is UP: `ip addr show`
- Use `-i` flag to manually specify interface
- View active rules: `sudo tc qdisc show dev eth0`

### Interface Auto-Detection Failing
- Manually specify interface: `sudo python3 bring-da-ruckus.py -i eth0`
- Find your interface: `ip route show default`nk show` (Linux) or `Get-NetAdapter` (Windows)
- Use `-i` flag to manually specify interface
- Check if you have proper permissions

### Deadman's Switch Not Working
- Ensure script remains running in foreground
- Don't minimize or background the terminal
- Watch for timeout messages

## Best Practices

1. **Start Small**: Begin with Light or Moderate levels
2. **Monitor Everything**: Watch streams, uploads, logs simultaneously
3. **Document Results**: Note which levels cause which symptoms
4. **Test in Phases**: Test one aspect at a time (streaming, uploads, commands)
5. **Use Target IP**: Focus disruption on QwikCam IP for precise testing
6. **Safety First**: Keep deadman timeout reasonable (10-30 minutes)

## QwikCut-Specific Testing

### Testing Checklist

- [ ] RTSP stream quality at each level
- [ ] Video recording quality (check uploaded files)
- [ ] S3 upload success rate and timing
- [ ] WebSocket command responsiveness
- [ ] API call success/failure patterns
- [ ] System behavior during recovery from outage
- [ ] Storage handling when uploads queue
- [ ] DeepStream/GStreamer pipeline stability

### Expected Behaviors

**Good System Behavior:**
- Graceful quality degradation
- Proper queuing of uploads
- Continued autonomous recording during outage
- Automatic sync when connection restored
- No corrupted video files

**Problem Indicators:**
- Stream completely fails (doesn't degrade gracefully)
- Video files corrupted
- System crashes or freezes
- Uploads fail permanently
- Storage fills up uncontrollably

## Architecture Notes

The tool focuses on **uplink disruption** (camera → cloud) which is most relevant for:
- Video upload to S3
- API calls to backend
- WebSocket command channel
- Remote access (ngrok)

The **downlink** (cloud → camera) is less critical as:
- Game schedules can be cached
- Commands are less frequent
- Software updates are async

## Documentation

- **[CHAMBERS.md](CHAMBERS.md)** - Complete guide to the 36 Chambers of Chaos
- **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
- **[UBUNTU-DEPLOYMENT.md](UBUNTU-DEPLOYMENT.md)** - Complete deployment guide for Ubuntu Server
- **[test-scenarios.md](test-scenarios.md)** - 8 comprehensive test scenarios for QwikCut
- **[examples.sh](examples.sh)** - Command examples and configurations

## Contributing

This tool is designed for QwikCut internal use. Suggestions and improvements welcome!

## License

Internal QwikCut tool - All rights reserved.

---

**🥷 Now bring da ruckus to your network and test that camera system!**
