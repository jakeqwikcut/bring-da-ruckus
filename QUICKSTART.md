# Quick Start Guide - Bring Da Ruckus
## 36 Chambers of Chaos - Wu-Tang Sword Style Edition

**Created by Jake Mammen - 2025**

🥷 **Wu-Tang is for the children. Test responsibly.** 🥷

## 5-Minute Setup on Ubuntu Server

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jakeqwikcut/bring-da-ruckus.git
   cd bring-da-ruckus
   ```

2. **Make scripts executable:**
   ```bash
   chmod +x bring-da-ruckus.py
   chmod +x monitor-the-ruckus.py
   ```

3. **Verify tc is installed:**
   ```bash
   tc -Version
   # If not found: sudo apt-get install iproute2
   ```

4. **Run the chaos tool:**
   ```bash
   sudo python3 bring-da-ruckus.py
   ```

   You'll see the Wu-Tang W logo and the quote:
   *"Shaolin shadowboxing and the Wu-Tang sword style..."*

5. **Set your scope (press `o`):**
   - Choose `1` for Local (default - affects only this server)
   - Choose `2` for Network (gateway mode - affects all devices)
   - Choose `3` for Targeted IP (precision chaos for your QwikCam)

6. **Select a chamber:**
   - Press `1` for Chamber 1: The Swarm (Light disruption)
   - Press `2` for Chamber 9: The Mystery (Moderate chaos)
   - Press `3` for Chamber 18: Deadly Venoms (Heavy ruckus)
   - Press `4` for Chamber 36: Liquid Swords (Extreme chaos)
   - Press `5` for Shaolin Shadow (Total darkness)
   - Press `0` to restore Peace

## First Test Scenario - Targeted QwikCam Test

### What You'll Need:
- QwikCam IP address (e.g., 192.168.1.100)
- Two terminal windows/SSH sessions
- Way to view the RTSP stream

### Test Procedure:

1. **Terminal 1 - Start Monitoring:**
   ```bash
   python3 monitor-the-ruckus.py --targets 192.168.1.100 192.168.1.1
   ```
   You'll see real-time stats for your QwikCam and router.

2. **Terminal 2 - Apply Chaos:**
   ```bash
   sudo python3 bring-da-ruckus.py
   ```

3. **Configure Targeted Mode:**
   - Press `o` (set scope)
   - Choose `3` (Targeted IP)
   - Enter `192.168.1.100` (your QwikCam IP)

4. **Progress Through Chambers:**
   - Press `1` - Chamber 1 (The Swarm - 50ms latency, 1% loss)
   - Watch monitoring terminal for 2-3 minutes
   - Observe QwikCam behavior
   - Press `2` - Chamber 9 (The Mystery - 150ms latency, 3% loss)
   - Continue monitoring
   - Press `3` - Chamber 18 if system handles it well
   - Press `0` to restore Peace

5. **Review Results:**
   - Check monitoring terminal for latency/loss patterns
   - Verify stream quality degradation/recovery
   - Check S3 uploads completed

## Monitoring Dashboard Explained

```
🖥️  LOCAL DEVICE HEALTH:
   RX: 12,345,678 packets (1,234,567,890 bytes)
   TX: 9,876,543 packets (987,654,321 bytes)
   🟢 Errors: RX=0, TX=0                    ← No errors = healthy
   🟢 Dropped: RX=0, TX=0                   ← No drops = healthy

📊 BANDWIDTH USAGE:
   ⬇️  Download: 45.2 Mbps
   ⬆️  Upload: 12.8 Mbps
   🔄 Total: 58.0 Mbps

🎯 TARGET MONITORING:
   Target: 192.168.1.100
   🟢 Status: REACHABLE                     ← Green = good
      Latency: 52.3ms (min: 50.1, max: 55.8)
      Packet Loss: 1.2%                     ← Should match chamber specs
```

**Health Indicators:**
- 🟢 Green = Healthy
- 🟡 Yellow = Warning (some packet loss)
- 🔴 Red = Critical (unreachable or high loss)

## Quick Command Reference

**In Chaos Tool (bring-da-ruckus.py):**

| Key | Action |
|-----|--------|
| `o` | Set scope (Local / Network / Targeted IP) |
| `1` | Chamber 1: The Swarm (Light) |
| `2` | Chamber 9: The Mystery (Moderate) |
| `3` | Chamber 18: Deadly Venoms (Heavy) |
| `4` | Chamber 36: Liquid Swords (Extreme) |
| `5` | Shaolin Shadow (Total outage) |
| `0` | Peace (Restore normal) |
| `s` | Show status |
| `c` | Clear all disruption |
| `i` | Set network interface |
| `d` | Show detailed tc configuration |
| `q` | Quit and cleanup |

**Monitoring Tool (monitor-the-ruckus.py):**

```bash
# Basic monitoring
python3 monitor-the-ruckus.py --targets 192.168.1.100

# Multiple targets
python3 monitor-the-ruckus.py --targets 192.168.1.100 192.168.1.1 8.8.8.8

# Custom refresh interval
python3 monitor-the-ruckus.py --targets 192.168.1.100 --interval 10
```

## Your First Day Testing Plan

### Morning Session (2 hours)

**Setup (30 min):**
1. Clone repo and verify tc installed
2. Start monitoring tool
3. Verify QwikCam is reachable

**Progressive Testing (90 min):**
1. **Chamber 1 - The Swarm** (20 min)
   - Set scope to Targeted IP
   - Monitor stream quality
   - Check upload timing
   
2. **Chamber 2 - The Mystery** (20 min)
   - Observe degradation
   - Note upload queue behavior
   - Test command responsiveness

3. **Chamber 3 - Deadly Venoms** (20 min)
   - Heavy stress test
   - Verify resilience mechanisms
   - Document failure points

4. **Chamber 4 - Liquid Swords** (15 min)
   - Extreme conditions
   - Test autonomous mode
   - Recovery testing

5. **Chamber 5 - Shaolin Shadow** (10 min)
   - Total outage simulation
   - Verify autonomous recording continues
   - Test reconnection/sync

6. **Recovery Verification** (5 min)
   - Return to Peace
   - Verify all systems normal

### Afternoon Session (Document & Analyze)
- Review monitoring logs
- Document which chambers caused issues
- Identify improvement areas
- Plan fixes/optimizations

## Common Questions

**Q: Does this only work on Ubuntu?**
A: Works on any Linux with tc/iproute2 (Ubuntu, Debian, RHEL, CentOS, Fedora, etc.)

**Q: Will this break my network permanently?**
A: No. All changes are temporary and automatically reversed when you quit or after 5-minute timeout.

**Q: What if I lose connection to the server?**
A: Deadman's switch triggers after 5 minutes (with 30-second warning). You can also SSH from another machine and run `sudo python3 bring-da-ruckus.py --restore`

**Q: How do I know it's actually working?**
A: 
1. Watch the monitoring tool for latency/loss increases
2. Run `ping <qwikcam-ip>` in another terminal
3. Press `d` in chaos tool to see tc configuration
4. Press `s` to see current status

**Q: What's the best starting chamber?**
A: Chamber 1 (The Swarm). It's noticeable but gentle.

**Q: Can I target just the QwikCam?**
A: Yes! Press `o`, choose `3` (Targeted IP), enter your QwikCam IP address.

**Q: How do I test the entire network?**
A: Press `o`, choose `2` (Network), follow prompts to enable gateway mode. Then configure devices to use server as gateway.

**Q: What's with the Wu-Tang theme?**
A: Inspired by "Enter the Wu-Tang (36 Chambers)" - progressive levels of mastery. Each chamber tests a different level of network adversity.

**Q: The deadman's switch is too short/long?**
A: Run with `--timeout <minutes>`: `sudo python3 bring-da-ruckus.py --timeout 10`

## See Full Documentation

- **README.md** - Complete feature guide
- **CHAMBERS.md** - Detailed chamber descriptions  
- **test-scenarios.md** - 8 comprehensive test scenarios
- **examples.sh** - Command examples
- **UBUNTU-DEPLOYMENT.md** - Deployment guide

## Emergency Stop

If things go wrong:

1. **In the tool**: Press `Ctrl+C` or `q`
2. **Lost connection**: Wait 5 minutes for auto-restore
3. **Manual restore**: SSH in and run:
   ```bash
   sudo python3 bring-da-ruckus.py --restore
   ```
4. **Nuclear option**: Reboot the server (clears all tc rules)

**Now go bring da ruckus! Test responsibly. 🥷**
4. Network automatically restores

## Next Steps

After your first test:
1. Review `test-scenarios.md` for comprehensive testing
2. Document your findings
3. Try targeted disruption with `--target` flag
4. Test longer durations with custom `--timeout`

**Now go bring da ruckus! 🥷**
