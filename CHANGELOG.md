# Changelog - Bring Da Ruckus

All notable changes to this network chaos engineering toolkit.

---

## [Version 2.0] - 2025-12-08

### 🎯 Major Monitor Enhancement Release

#### Enhanced Monitoring Tool (monitor-the-ruckus.py)

**New Features:**
- **Connection Quality Scoring**: 0-100 quality score per target based on latency, jitter, and packet loss
- **Quality Status Indicators**: Excellent/Good/Fair/Poor/Critical with color-coded emoji
- **Jitter Measurement**: Real-time jitter (mdev) tracking from ping statistics
- **Historical Metrics**: 60-sample rolling averages (1-minute window) for all metrics
- **TCP Retransmit Tracking**: Parse netstat for TCP retransmit rate monitoring
- **Peak Bandwidth Tracking**: Track and display peak bandwidth usage
- **Enhanced Latency Stats**: Min/Avg/Max latency per target with 1-minute averages
- **Configurable Alert Thresholds**: Interactive threshold configuration for latency, loss, and jitter
- **Alert Highlighting**: Visual alerts when metrics exceed configured thresholds
- **htop-Style Display**: Alternate screen buffer mode with locked display (no scrolling!)

**Display Improvements:**
- Changed from scrolling output to fixed in-place updates
- Uses alternate screen buffer (like htop/jtop)
- Cursor hidden during operation for cleaner display
- ANSI escape codes for professional terminal UI
- Screen updates values in place without scroll

**Quality Scoring Algorithm:**
```
Base score: 100
- Latency penalty: (latency_ms / 10)
- Loss penalty: (packet_loss_pct * 5)
- Jitter penalty: (jitter_ms / 5)
Result: Clamped to 0-100 range
```

**Quality Status Thresholds:**
- 90-100: 🟢 Excellent
- 75-89: 🟢 Good
- 50-74: 🟡 Fair
- 25-49: 🔴 Poor
- 0-24: 🔴 Critical

**Technical Details:**
- Ping statistics parsed from `ping -c 5` output
- Historical data stored in 60-sample deque (collections)
- Bandwidth calculation over 2-second intervals
- TCP stats from `netstat -s` command
- Alert thresholds: latency (100ms), loss (5%), jitter (50ms) defaults

---

## [Version 1.5] - 2025-12-07

### 🛡️ Critical Safety Update

**Post-Incident Improvements:**
After a catastrophic server lockout incident (Shaolin Shadow - 100% packet loss), comprehensive safety features were implemented.

#### New Safety Features:
- **SSH Protection**: Automatic iptables rules to exempt SSH port 22 before applying chaos
- **Management IP Whitelist**: Protect specific IP ranges from disruption
- **Shaolin Shadow Confirmation**: Mandatory typed confirmation "YES I UNDERSTAND" for 100% packet loss
- **Enhanced Deadman's Switch**: Reduced timeout from 30 to 5 minutes with 30-second warning
- **Emergency Recovery Script**: Quick recovery script for physical console access
- **Comprehensive Documentation**: Safety guides, incident post-mortem, and recovery procedures

#### New Documentation:
- `SAFETY-GUIDE.md`: Complete safety procedures and best practices
- `LOCKED-OUT.md`: Emergency recovery guide for server lockouts
- `POST-MORTEM.md`: Detailed incident analysis and lessons learned
- `WHATS-FIXED.md`: Summary of safety improvements
- `SAFETY-CARD.txt`: Printable safety checklist
- `emergency-recovery.sh`: Quick recovery script

#### Safety Improvements in Code:
```python
# SSH protection added before tc rules
subprocess.run(['iptables', '-I', 'INPUT', '-p', 'tcp', '--dport', '22', '-j', 'ACCEPT'])

# Confirmation required for Shaolin Shadow
if level == 'shadow':
    print("⚠️  WARNING: SHAOLIN SHADOW (100% PACKET LOSS)")
    confirm = input("Type 'YES I UNDERSTAND' to proceed: ")
    if confirm != "YES I UNDERSTAND":
        return
```

---

## [Version 1.2] - 2025-12-06

### 🎯 Jetson Nano Compatibility

**New Tool: bring-da-ruckus-iptables.py**
- Alternative version for systems without netem kernel module
- Uses iptables statistic module for packet loss simulation
- Jetson Nano compatible (kernel 5.15.136-tegra)
- Supports INPUT/OUTPUT/FORWARD chains for local network
- SSH protection included

**Limitations:**
- Packet loss only (no latency/jitter/bandwidth throttling)
- Cannot replicate latency-based field issues
- Suitable for basic packet loss testing

**New Tool: camera-chaos.py**
- Camera-specific chaos targeting (e.g., 192.168.1.78)
- Interactive Wu-Tang themed menu
- 5 chambers: Swarm (1%), Mystery (9%), Venoms (18%), Swords (36%), Shaolin (100%)
- Famous Wu-Tang quote: "En garde, I'll let you try my Wu-Tang style"
- Status and clear commands

---

## [Version 1.0] - 2025-12-05

### 🥷 Initial Release - Wu-Tang Sword Style Edition

**Core Features:**
- **6 Chambers of Chaos**: Progressive network disruption levels
- **3 Scope Modes**: Local device, entire network gateway, targeted IP
- **Interactive CLI**: Wu-Tang themed terminal interface
- **Smart Deadman's Switch**: 30-minute timeout with auto-restore
- **Monitoring Tool**: Real-time network health dashboard
- **Multi-target Monitoring**: Track multiple IPs simultaneously

**The 36 Chambers:**
1. **Peace** (0): Normal network operation
2. **The Swarm** (1): 50ms latency, 1% loss, 50 Mbps, 10ms jitter
3. **The Mystery** (9): 150ms latency, 3% loss, 10 Mbps, 25ms jitter
4. **Deadly Venoms** (18): 300ms latency, 8% loss, 2 Mbps, 50ms jitter
5. **Liquid Swords** (36): 500ms latency, 15% loss, 512 Kbps, 100ms jitter
6. **Shaolin Shadow**: 100% packet loss (total outage)

**Technical Implementation:**
- Linux `tc` (traffic control) with `netem` for network emulation
- Token bucket filter (tbf) for bandwidth throttling
- Real-time interface statistics from `/proc/net/dev`
- Ping-based latency and packet loss monitoring
- Python standard library only (no external dependencies)

**Interactive Commands:**
- `o`: Set scope (Local/Network/Targeted)
- `1-5`: Select chamber
- `0`: Restore peace
- `s`: Show status
- `c`: Clear disruption
- `i`: Set interface
- `d`: Show detailed config
- `q`: Quit

**Safety Features:**
- Clean exit on Ctrl+C
- Auto-cleanup of tc rules
- Status monitoring
- Network scope isolation

**Use Cases:**
- IP camera system testing
- Video streaming quality analysis
- Cloud upload resilience testing
- Network failure recovery validation
- Autonomous mode engagement testing

---

## Development Notes

### Field Testing Results
- **Packet Loss Testing**: Shows buffering behavior (expected)
- **Field Issue Diagnosis**: Pixelation/artifacts indicate latency/jitter (NOT packet loss)
- **Suspected Cause**: WiFi repeater in school gym deployment
- **Resolution**: Requires full netem version for latency/jitter simulation

### Hardware Compatibility
- **Ubuntu Server**: Full netem support, all features available
- **Jetson Nano**: No netem module, iptables-only version required
- **Recommendation**: Use Ubuntu server for complete testing capabilities

### Testing Workflow
1. Start monitor tool in Terminal 1
2. Apply chaos in Terminal 2
3. Observe quality degradation in real-time
4. Document failure thresholds
5. Test recovery mechanisms
6. Validate autonomous mode

---

## Repository
**GitHub**: https://github.com/jakeqwikcut/bring-da-ruckus
**Author**: Jake Mammen
**Created**: December 2025
**License**: Open Source---

**🥷 Wu-Tang is for the children. Test responsibly. 🥷**

*"Shaolin shadowboxing and the Wu-Tang sword style. If what you say is true, the Shaolin and the Wu-Tang could be dangerous."*

**C.R.E.A.M.** - Chaos Rules Everything Around Me 💎⚔️
