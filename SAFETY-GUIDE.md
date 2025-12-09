# 🛡️ SAFETY GUIDE - Preventing Server Lockouts

## ⚠️ CRITICAL: Learn from Our Mistakes

**This tool can and WILL lock you out of your server if used improperly.**

### What Happened

On first deployment, Shaolin Shadow (Chamber 6 - 100% packet loss) was applied without proper safeguards. The result:
- ✅ Tool worked perfectly - blocked ALL network traffic as designed
- ❌ **Blocked SSH access to the server**
- ❌ Python process died when SSH connection dropped
- ❌ Deadman's switch never triggered (process was dead)
- ❌ Server offline for 90+ minutes
- ❌ Required physical reboot to recover

**Lesson learned:** A chaos engineering tool that works perfectly can be your worst enemy if you're not prepared.

---

## 🛡️ Safety Features (NOW IMPLEMENTED)

### 1. SSH Port Protection
**Status:** ✅ ENABLED by default

When Shaolin Shadow is applied, the tool now:
- Automatically whitelists SSH port 22 using iptables
- Detects and whitelists your SSH client IP address
- Maintains management access even during 100% packet loss

```python
# This happens automatically:
iptables -I INPUT -p tcp --dport 22 -j ACCEPT
iptables -I OUTPUT -p tcp --sport 22 -j ACCEPT
iptables -I INPUT -s <YOUR_IP> -j ACCEPT
iptables -I OUTPUT -d <YOUR_IP> -j ACCEPT
```

### 2. Shaolin Shadow Confirmation
**Status:** ✅ REQUIRED for Chamber 6

Before applying 100% packet loss, you must:
1. Type `YES I AM SURE` (case-sensitive)
2. Wait through 3-second countdown
3. See explicit warnings about risks

**You can abort with Ctrl+C during the countdown.**

### 3. Emergency Recovery Script
**Location:** `emergency-recovery.sh`

Run this if you get locked out:
```bash
sudo ./emergency-recovery.sh
```

Clears ALL chaos rules and iptables rules immediately.

---

## 📋 Pre-Flight Checklist

**BEFORE running Shaolin Shadow, verify:**

- [ ] Tool detects your SSH client IP correctly
- [ ] You have SSH access from a known, whitelisted IP
- [ ] Running in `screen` or `tmux` (process won't die with SSH)
- [ ] Tested lower chambers successfully first
- [ ] Emergency recovery script is in place
- [ ] You have physical access OR remote console (IPMI/iLO)
- [ ] Team knows you're testing (in case of lockout)

---

## 🚀 Safe Operation Modes

### Option 1: Screen/Tmux (RECOMMENDED)
```bash
# Start in screen
screen -S ruckus
sudo python3 bring-da-ruckus.py

# Detach with: Ctrl+A then D
# Reattach with: screen -r ruckus
```

**Why:** If SSH dies, your process survives and deadman's switch keeps working.

### Option 2: Systemd Service (ADVANCED)
```bash
# Install service
sudo cp bring-da-ruckus.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bring-da-ruckus
sudo systemctl start bring-da-ruckus

# Monitor logs
journalctl -u bring-da-ruckus -f
```

**Why:** Tool runs as a system service, survives SSH disconnects.

### Option 3: Targeted Testing
```bash
# Test on a specific IP only (not yourself!)
sudo python3 bring-da-ruckus.py

# In menu:
# 1. Press 'o' for scope
# 2. Select '3' for targeted IP
# 3. Enter victim IP (NOT your management IP!)
# 4. Apply Shaolin Shadow - affects only that IP
```

**Why:** You can test 100% loss without affecting your own connection.

---

## 🔥 Testing the Safety Features

### Step 1: Verify SSH Protection
```bash
sudo python3 bring-da-ruckus.py
```

At the menu, check for:
```
SSH Protection: 🛡️  ENABLED
Your IP: 192.168.1.x (will be whitelisted)
```

If you see `❌ DISABLED` or no IP detected - **DO NOT USE SHAOLIN SHADOW!**

### Step 2: Test with Lower Chambers First
1. Start with Chamber 1 (The Swarm - 1% loss)
2. Verify SSH still works
3. Progress through chambers gradually
4. Watch deadman's switch countdown

### Step 3: Shaolin Shadow Dry Run
Before actual use:
1. Set up in `screen`
2. Have emergency recovery script ready
3. Have physical access OR remote console available
4. Test on non-critical system first

---

## 🆘 Emergency Procedures

### If Locked Out (SSH Not Responding)

**Option A: Wait for Deadman's Switch**
- Default: 5 minutes of inactivity
- Warning at 30 seconds remaining
- Tool will auto-restore network
- **Only works if process is still alive!**

**Option B: Physical Console Access**
```bash
# At physical console or IPMI/iLO
sudo tc qdisc del dev eth0 root
sudo iptables -F
```

**Option C: Physical Reboot**
- Power cycle the server
- All tc rules clear on reboot
- Server comes back with normal networking

**Option D: Out-of-Band Management**
- Use IPMI/iLO/iDRAC console
- Run emergency recovery commands
- Or reboot remotely

### If Server Completely Unresponsive

This means Shaolin Shadow is active AND process died. You need:
1. Physical reboot (power cycle)
2. OR IPMI/iLO remote reboot
3. OR wait for automatic reboot (if configured)

**There is NO remote recovery without console access.**

---

## 🎓 Lessons for Production Use

### DO:
✅ Always run in `screen` or `tmux`
✅ Test on non-critical systems first
✅ Verify SSH protection before Shaolin Shadow
✅ Have emergency recovery plan
✅ Start with low-impact chambers
✅ Use targeted mode when possible
✅ Keep emergency recovery script handy
✅ Document your tests

### DON'T:
❌ Run in bare SSH session (process dies with SSH)
❌ Skip the confirmation for Shaolin Shadow
❌ Test on servers without physical access
❌ Test on production without backup plan
❌ Ignore SSH protection warnings
❌ Apply to entire network without understanding impact
❌ Use without deadman's switch active
❌ Forget to notify team of testing

---

## 🧪 Recommended Testing Progression

### Week 1: Local Testing
- Chambers 1-2 only
- Local scope
- Verify SSH protection working
- Test deadman's switch
- Practice emergency recovery

### Week 2: Network Testing
- Chambers 3-4
- Network scope on test segment
- Monitor impact on cameras
- Document findings

### Week 3: Targeted Testing
- Chambers 5-6
- Targeted scope only
- Test specific devices
- Refine recovery procedures

### Week 4: Controlled Shaolin
- Shaolin Shadow (Chamber 6)
- Targeted mode on sacrificial device
- Screen/tmux session active
- Emergency recovery tested
- Team on standby

---

## 📊 Safety Verification Commands

**Before each session:**
```bash
# Check your IP
who am i
echo $SSH_CLIENT

# Verify network interface
ip route | grep default

# Test emergency recovery
sudo ./emergency-recovery.sh --dry-run

# Verify iptables
sudo iptables -L -n | grep 22
```

**During session:**
```bash
# From another terminal (in screen):
watch -n 1 'tc qdisc show; echo "---"; iptables -L -n | grep 22'
```

---

## 🔧 Troubleshooting

### "Could not detect your SSH IP"
**Cause:** Running locally or SSH_CLIENT env var not set
**Fix:** Manually add to whitelist or avoid Shaolin Shadow

### "SSH access maintained via iptables exemption" not shown
**Cause:** SSH protection disabled or failed
**Fix:** DO NOT use Shaolin Shadow until resolved

### Deadman's switch doesn't trigger
**Cause:** Process died (not in screen/tmux)
**Fix:** Always use screen/tmux for persistence

### Server offline after Shaolin Shadow
**Cause:** SSH protection failed or process died
**Fix:** Physical reboot required

---

## 📞 When All Else Fails

1. **Don't Panic** - The server is fine, just unreachable
2. **Physical Access** - Reboot clears all tc rules
3. **IPMI/iLO** - Remote console access works
4. **Wait** - If in screen, deadman's switch will trigger
5. **Learn** - Update this guide with what happened

---

## ⚡ Quick Reference Card

```
┌────────────────────────────────────────────────────┐
│  SHAOLIN SHADOW SAFETY CHECKLIST                   │
├────────────────────────────────────────────────────┤
│  ☑ Running in screen/tmux                          │
│  ☑ SSH IP detected: 192.168.x.x                    │
│  ☑ Emergency recovery script ready                 │
│  ☑ Physical access OR remote console available     │
│  ☑ Tested lower chambers first                     │
│  ☑ Team notified of testing                        │
│  ☑ Non-critical system OR off-hours                │
│                                                     │
│  🛡️  SSH Protection: ENABLED                       │
│  ⏰ Deadman Timer: 5 minutes                       │
│  📍 Scope: [Local/Network/Targeted]                │
│                                                     │
│  Emergency: sudo ./emergency-recovery.sh           │
│  Abort: Ctrl+C during 3-second countdown           │
└────────────────────────────────────────────────────┘
```

---

## 🎯 TL;DR - Critical Safety Rules

1. **ALWAYS run in screen or tmux**
2. **VERIFY SSH protection before Shaolin Shadow**
3. **TEST progressively** through chambers
4. **HAVE physical access** OR remote console
5. **NOTIFY team** before testing
6. **KEEP emergency recovery** script handy

**Remember: This tool WILL lock you out if you ignore safety procedures.**

---

*"Protection & power are demonstrated in the life of an individual who is sincere, true, and honest. Livin' a lie, everything he represents is a lie. So the power that I have, is through respect & knowledge." - GZA*

☯️  May the Wu-Tang protect your networks.
