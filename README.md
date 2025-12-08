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

Bring Da Ruckus is a network chaos engineering toolkit designed to test QwikCut camera systems under adverse network conditions. Deploy it on your Ubuntu server to simulate real-world network problems that can affect video streaming, recording quality, and cloud synchronization.

**Two powerful tools:**
1. **bring-da-ruckus.py** - Apply network chaos (latency, packet loss, bandwidth limits)
2. **monitor-the-ruckus.py** - Real-time network health monitoring

Use them together: monitor in one terminal while chaos tests run in another!

## Features

### Chaos Tool (bring-da-ruckus.py)

- **36 Chambers of Chaos**: Six progressive disruption levels inspired by Wu-Tang
- **Three Chaos Scopes**:
  - 🖥️ **Local Device**: Affects only the server running the tool
  - 🌐 **Entire Network**: Gateway mode - disrupts all traffic flowing through server
  - 🎯 **Targeted IP**: Precision chaos for specific devices (perfect for QwikCam testing)
- **Interactive CLI**: Real-time control with Wu-Tang themed interface
- **Smart Deadman's Switch**: 
  - 5-minute timeout with 30-second warning
  - Prompts to continue or auto-stops
  - Prevents accidental long-term disruption
- **Network Disruptions**:
  - Latency (ping delay)
  - Packet loss
  - Bandwidth throttling
  - Jitter
  - Complete network outages

### Monitoring Tool (monitor-the-ruckus.py)

- **Real-Time Dashboard**: Auto-refreshing network health display
- **Local Device Monitoring**:
  - Interface statistics (packets, bytes, errors, drops)
  - Bandwidth usage (RX/TX in Mbps)
  - Visual health indicators 🟢🟡🔴
- **Target IP Monitoring**:
  - Ping latency (min/avg/max)
  - Packet loss percentage
  - Reachability status
- **Multi-Target Support**: Monitor multiple IPs simultaneously
- **Configurable Refresh**: Set custom update intervals

## Installation

### Prerequisites

**Ubuntu Server (or any Linux distribution):**
- Python 3.7+
- `sudo` access (required for chaos tool)
- `tc` (traffic control) utility from iproute2 (usually pre-installed)

### Setup

```bash
# Clone the repository
git clone https://github.com/jakeqwikcut/bring-da-ruckus.git
cd bring-da-ruckus

# Ensure tc is installed
sudo apt-get install iproute2

# Make scripts executable
chmod +x bring-da-ruckus.py
chmod +x monitor-the-ruckus.py

# No additional Python dependencies required - uses standard library only!
```

## Usage

### Chaos Testing

**Basic Interactive Mode:**

```bash
# Run with sudo (required for tc command)
sudo python3 bring-da-ruckus.py
```

You'll see the Wu-Tang W logo and the iconic quote, then the interactive menu.

**Select Your Scope:**
Press `o` to choose:
1. **Local Device** - Affects only this server (default, no setup needed)
2. **Entire Network** - Gateway mode (requires devices to use this server as gateway)
3. **Targeted IP** - Precision chaos for specific IP (e.g., your QwikCam)

**Then Choose Your Chamber:**
- `1` - Chamber 1: The Swarm (Light - 50ms latency, 1% loss)
- `2` - Chamber 9: The Mystery (Moderate - 150ms latency, 3% loss)
- `3` - Chamber 18: Deadly Venoms (Heavy - 300ms latency, 8% loss)
- `4` - Chamber 36: Liquid Swords (Extreme - 500ms latency, 15% loss)
- `5` - Shaolin Shadow (Total Darkness - 100% packet loss)
- `0` - Peace (Restore normal network)

**Smart Deadman's Switch:**
- 5-minute timeout (was 30 minutes)
- 30-second warning prompt before auto-stop
- Press Y to continue, or let it auto-restore

### Network Monitoring

**Monitor your QwikCam during chaos tests:**

```bash
# Monitor specific target
python3 monitor-the-ruckus.py --targets 192.168.1.100

# Monitor multiple targets
python3 monitor-the-ruckus.py --targets 192.168.1.100 192.168.1.1

# Custom refresh interval (default 5 seconds)
python3 monitor-the-ruckus.py --targets 192.168.1.100 --interval 10

# Specify network interface
python3 monitor-the-ruckus.py --interface eth0 --targets 192.168.1.100
```

**Pro Tip:** Run monitoring in one terminal, chaos in another:
```bash
# Terminal 1
python3 monitor-the-ruckus.py --targets 192.168.1.100

# Terminal 2  
sudo python3 bring-da-ruckus.py
# Press 'o', select '3' (Targeted IP), enter 192.168.1.100
# Then select a chamber and watch the chaos unfold!
```

### Advanced Options

```bash
# Start with specific chamber (bypasses menu, not recommended)
sudo python3 bring-da-ruckus.py --chamber first

# Emergency restore if you lose connection
sudo python3 bring-da-ruckus.py --restore

# Custom deadman timeout (minutes)
sudo python3 bring-da-ruckus.py --timeout 10

# Specify interface
sudo python3 bring-da-ruckus.py --interface eth1
```

## Typical Testing Workflow

1. **Start Monitoring**
   ```bash
   python3 monitor-the-ruckus.py --targets <qwikcam-ip> <router-ip>
   ```

2. **In Another Terminal, Start Chaos Tool**
   ```bash
   sudo python3 bring-da-ruckus.py
   ```

3. **Configure Scope**
   - Press `o`
   - Choose targeted IP mode
   - Enter your QwikCam IP

4. **Apply Chambers Progressively**
   - Start with Chamber 1 (The Swarm)
   - Observe QwikCam behavior in monitoring terminal
   - Progress through chambers as needed
   - Test video quality, recording, cloud uploads

5. **Document Issues**
   - Note which chamber causes problems
   - Check latency/packet loss thresholds
   - Identify failure points

6. **Restore Peace**
   - Press `0` or wait for deadman's switch
   - Verify network returns to normal in monitor

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

- **o**: Set scope (Local / Network / Targeted IP)
- **1-6**: Select chamber (0=Peace, 1=Swarm, 2=Mystery, 3=Venoms, 4=Swords, 5=Shadow)
- **s**: Show current status and statistics
- **c**: Clear all ruckus (restore normal network)
- **i**: Set network interface
- **d**: Show detailed tc configuration
- **q**: Quit and clean up

## Deadman's Switch

The deadman's switch is a **critical safety feature** that automatically stops all network disruptions if the operator becomes inactive.

- Default timeout: **5 minutes** (reduced from 30 for safety)
- **30-second warning**: Prompts "Continue? (Y/N)" before auto-stop
- Resets on any user interaction
- Press Y to continue for another 5 minutes
- No response = automatic restore to peace
- Prevents accidental long-term network disruption

## Testing Scenarios for QwikCut

See [test-scenarios.md](test-scenarios.md) for 8 comprehensive testing scenarios.

### Quick Example: Targeted QwikCam Test

```bash
# Terminal 1: Start monitoring
python3 monitor-the-ruckus.py --targets 192.168.1.100 --interval 5

# Terminal 2: Apply chaos to QwikCam
sudo python3 bring-da-ruckus.py
# Press 'o' → Choose '3' (Targeted IP) → Enter 192.168.1.100
# Press '1' for Chamber 1 (The Swarm)
# Observe in monitoring terminal
# Progress through chambers: 2, 3, 4
# Press '0' to restore peace
```

### Testing Progression

1. **Chamber 1 (The Swarm)**: Good mobile network - verify basic degradation handling
2. **Chamber 2 (The Mystery)**: Congested network - test upload queuing
3. **Chamber 3 (Deadly Venoms)**: Poor connection - verify resilience
4. **Chamber 4 (Liquid Swords)**: Near failure - test autonomous mode
5. **Chamber 5 (Shaolin Shadow)**: Complete outage - test recovery mechanisms

## How It Works

### Ubuntu/Linux Implementation
Uses `tc` (traffic control) with `netem` (network emulation):
- Adds queuing disciplines (qdisc) to network interface
- `netem` handles latency, jitter, and packet loss
- `tbf` (token bucket filter) handles bandwidth throttling
- Works at the kernel level for realistic network simulation
- Three scope modes:
  - **Local**: Affects only server's own traffic
  - **Network**: Gateway mode - affects all devices routing through server
  - **Targeted**: Precision chaos using tc filters for specific IP

**Technical Details:**
- Modifies the qdisc (queuing discipline) on your network interface
- Applies rules that delay, drop, or limit packets
- Changes are live and immediate
- Completely reversible - no permanent changes to system
- Network scope requires IP forwarding and NAT configuration

### Monitoring Tool
Real-time Python dashboard using:
- `/proc/net/dev` for interface statistics
- `ping` command for latency/loss measurements
- Bandwidth calculated from byte counters over time intervals
- Auto-refreshing curses-style display

## Safety Features

1. **Smart Deadman's Switch**: 5-minute timeout with 30-second warning prompt
2. **Clean Exit**: Ctrl+C gracefully restores network
3. **Status Monitoring**: Always see what's active
4. **Scope Isolation**: Choose to affect only specific targets
5. **Auto-cleanup**: iptables and tc rules cleared on exit
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
- Use `i` command to manually specify interface
- View active rules: `sudo tc qdisc show dev eth0`
- **For targeted IP**: Ensure target IP is correct and reachable
- **For network-wide**: Ensure devices are using server as gateway

### Monitoring Tool Shows No Data
- Verify network interface exists: `ip addr show`
- Check target IPs are reachable: `ping <target-ip>`
- Ensure proper permissions (no sudo needed for monitoring)
- For bandwidth stats: Interface must have traffic flowing

### Deadman's Switch Not Working
- Ensure script remains running in foreground
- Don't minimize or background the terminal
- Watch for timeout messages

## Best Practices

1. **Start Small**: Begin with Chamber 1 (The Swarm)
2. **Use Targeted Mode**: Focus chaos on specific QwikCam IP for precise testing
3. **Monitor Everything**: Run monitor-the-ruckus.py in separate terminal
4. **Document Results**: Note which chambers cause which symptoms
5. **Test in Phases**: Test one aspect at a time (streaming, uploads, commands)
6. **Progress Gradually**: Move through chambers sequentially, don't jump to Shadow
7. **Verify Recovery**: Always return to Peace and verify normal operation

## Tools in the Toolkit

### bring-da-ruckus.py - Chaos Generator
Apply network disruptions using Linux traffic control.

**Key Features:**
- 6 progressive chambers (Peace → Shaolin Shadow)
- 3 scope modes (Local / Network / Targeted)
- Smart deadman's switch (5 min with 30s warning)
- Interactive Wu-Tang themed CLI
- Auto-cleanup on exit

### monitor-the-ruckus.py - Health Monitor  
Real-time network monitoring companion tool.

**Key Features:**
- Local device stats (packets, bytes, errors, drops)
- Bandwidth monitoring (RX/TX Mbps)
- Target ping monitoring (latency, packet loss)
- Multi-target support
- Auto-refreshing dashboard
- Visual health indicators 🟢🟡🔴

## QwikCut-Specific Testing

### Testing Checklist

- [ ] RTSP stream quality at each chamber
- [ ] Video recording quality (check uploaded files)
- [ ] S3 upload success rate and timing
- [ ] WebSocket command responsiveness
- [ ] API call success/failure patterns
- [ ] System behavior during recovery from outage
- [ ] Storage handling when uploads queue
- [ ] DeepStream/GStreamer pipeline stability
- [ ] Monitor dashboard shows degradation
- [ ] Autonomous mode engages during Shadow chamber

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

## Wu-Tang Inspiration

*"Shaolin shadowboxing and the Wu-Tang sword style. If what you say is true, the Shaolin and the Wu-Tang could be dangerous. Do you think your Wu-Tang sword can defeat me?"*

This toolkit is inspired by Wu-Tang Clan's legendary album "Enter the Wu-Tang (36 Chambers)" and their emphasis on disciplined training and mastery through progressive challenges. Each chamber represents a level of network adversity your system must master.

**C.R.E.A.M.** - Chaos Rules Everything Around Me 💎⚔️

## Contributing

This tool is designed for QwikCut internal use. Suggestions and improvements welcome!

## Author

Created by Jake Mammen - 2025

Wu-Tang is for the children. Test responsibly. 🥷

Internal QwikCut tool - All rights reserved.

---

**🥷 Now bring da ruckus to your network and test that camera system!**
