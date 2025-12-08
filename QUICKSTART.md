# Quick Start Guide - Bring Da Ruckus
## 36 Chambers of Chaos - Wu-Tang Sword Style Edition

**Created by Jake Mammen - 2025**

🥷 **Wu-Tang is for the children. Test responsibly.** 🥷

## 5-Minute Setup on Ubuntu Server

1. **Transfer the script to your Ubuntu server:**
   ```bash
   # Via SCP from your Windows PC
   scp bring-da-ruckus.py user@your-server-ip:/home/user/

   # Or via git, USB, etc.
   ```

2. **SSH into your server:**
   ```bash
   ssh user@your-server-ip
   ```

3. **Make it executable:**
   ```bash
   chmod +x bring-da-ruckus.py
   ```

4. **Verify tc is installed:**
   ```bash
   tc -Version
   # If not found: sudo apt-get install iproute2
   ```

5. **Run it:**
   ```bash
   sudo python3 bring-da-ruckus.py
   ```

6. **Start testing:**
   - Press `2` for Chamber 1: The Swarm
   - Press `s` to see status
   - Press `d` to see detailed tc config
   - Press `c` to clear when done (restore peace)
   - Press `q` to quit

## First Test Scenario

### What You'll Need:
- QwikCam IP address (e.g., 192.168.1.100)
- Way to view the RTSP stream
- Access to check S3 uploads

### Test Procedure:

1. **Start with baseline (Chamber 0 - Peace):**
   ```bash
   sudo python3 bring-da-ruckus.py
   # Select option 1 (Chamber 0: Peace)
   # Watch stream for 5 minutes
   # Note the quality
   ```

2. **Apply Chamber 1 - The Swarm:**
   ```bash
   # Select option 2 (Chamber 1: The Swarm)
   # Watch stream for 10 minutes
   # Note any changes
   ```

3. **Clear disruption:**
   ```bash
   # Press 'c' to clear
   # Press 's' to verify it's cleared
   ```

4. **Exit safely:**
   ```bash
   # Press 'q' to quit
   ```

## What to Watch For

### Good Signs ✅
- Stream quality adjusts smoothly
- Uploads complete eventually (may be delayed)
- System stays responsive
- No crashes or corrupted files

### Warning Signs ⚠️
- Stream becomes choppy but recovers
- Uploads delayed but queue is processing
- Occasional reconnections
- Temporary buffering

### Bad Signs ❌
- Stream completely fails (doesn't degrade)
- System crashes
- Uploads permanently fail
- Files get corrupted
- System becomes unresponsive

## Quick Command Reference

| Key | Action |
|-----|--------|
| `1-6` | Select chaos chamber (Peace, Swarm, Mystery, Venoms, Swords, Shadow) |
| `s` | Show status |
| `c` | Clear all disruption (restore peace) |
| `t` | Set target IP |
| `i` | Set interface |
| `d` | Show detailed tc configuration |
| `q` | Quit |

## Your First Day Testing Plan

### Morning (2 hours)
1. Setup and verify tool works (30 min)
2. Baseline testing - Level 1 (30 min)
3. Light chaos - Level 2 (30 min)
4. Moderate chaos - Level 3 (30 min)

### Afternoon (2 hours)
1. Heavy chaos - Level 4 (30 min)
2. Extreme chaos - Level 5 (30 min)
3. Complete outage - Level 6 (15 min)
4. Recovery verification (15 min)
## Common Questions

**Q: Does this only work on Ubuntu?**
A: Works on any Linux with tc/iproute2 (Ubuntu, Debian, RHEL, CentOS, etc.)

**Q: Will this break my network permanently?**
A: No. Changes are temporary and automatically reversed when you quit or if deadman's switch triggers.

**Q: What if I lose connection to the server?**
A: The deadman's switch will auto-stop disruptions after timeout. You can also SSH in from another machine and clear manually.

**Q: How do I know it's actually working?**
A: Run `ping <qwikcam-ip>` in another terminal while disruption is active - you'll see increased latency/loss. Also use `d` command to view tc config.

**Q: What's the best starting chamber?**
A: Start with Chamber 1 (The Swarm). It's noticeable but not extreme.

**Q: Can I target just the QwikCam?**
A: Partially implemented. Currently affects all traffic on the interface, but you can use iptables in addition for more targeted control.

**Q: What do the chamber numbers mean?**
A: Inspired by Wu-Tang's 36 Chambers. Chamber 1 is light, Chamber 36 is extreme, and Shaolin Shadow is total network darkness.
**Q: What's the best starting level?**
A: Start with Level 2 (Light Sparring). It's noticeable but not extreme.
See the full documentation:
- `README.md` - Complete guide and features
- `test-scenarios.md` - Detailed test cases for QwikCut
- `examples.sh` - Command examples
- `test-scenarios.md` - Detailed test cases
- `windows-setup.md` - Windows-specific info
- `examples.sh` - Command examples

## Emergency Stop

If things go wrong:
1. Press `Ctrl+C` in the terminal
2. Or just close the terminal
3. Or wait for deadman's switch timeout
4. Network automatically restores

## Next Steps

After your first test:
1. Review `test-scenarios.md` for comprehensive testing
2. Document your findings
3. Try targeted disruption with `--target` flag
4. Test longer durations with custom `--timeout`

**Now go bring da ruckus! 🥷**
