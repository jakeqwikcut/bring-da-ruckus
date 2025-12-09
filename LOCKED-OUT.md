# 🆘 LOCKED OUT? Emergency Recovery Guide

## You're Here Because...
Your server isn't responding after using Shaolin Shadow (Chamber 6 - 100% packet loss).

## Don't Panic
The server is fine. It just can't talk to you. Here's what to do:

---

## Option 1: Wait for Deadman's Switch (IF running in screen/tmux)
**Time Required:** Up to 5 minutes

If you started the tool in `screen` or `tmux`:
1. Wait 5 minutes (deadman's switch timeout)
2. Tool will auto-restore network
3. SSH will become available again

**⚠️ This ONLY works if the process is still running!**

If you ran in a normal SSH session, the process is dead. Skip to Option 2.

---

## Option 2: Physical Console Access
**Time Required:** 5-10 minutes

If you have physical access to the server:

1. **Go to the physical server**
2. **Log in at console**
3. **Run these commands:**
   ```bash
   sudo tc qdisc del dev eth0 root
   sudo iptables -F
   sudo systemctl restart networking
   ```
4. **Test SSH:**
   ```bash
   ping 8.8.8.8
   ```

Server should be back online.

---

## Option 3: IPMI / iLO / iDRAC / Remote Console
**Time Required:** 5-10 minutes

If you have out-of-band management:

1. **Connect to IPMI/iLO web interface**
2. **Open remote console (HTML5 or Java)**
3. **Run recovery commands:**
   ```bash
   sudo tc qdisc del dev eth0 root
   sudo iptables -F
   ```
4. **Or just reboot:**
   ```bash
   sudo reboot
   ```

All chaos rules clear on reboot.

---

## Option 4: Physical Reboot (Last Resort)
**Time Required:** 2-5 minutes

If you can physically access the server:

1. **Press and hold power button** (5 seconds)
2. **Wait for complete shutdown**
3. **Press power button again** to start
4. **Wait for boot** (1-3 minutes)
5. **Try SSH again**

**Why this works:** All tc and iptables rules clear on reboot.

---

## Option 5: Remote Power Management
**Time Required:** 2-5 minutes

If you have PDU, IPMI, or remote power control:

1. **Access power management interface**
2. **Cycle power** (off then on)
3. **Wait for boot**
4. **Try SSH again**

---

## What NOT to Do

❌ **Don't repeatedly try SSH** - You're just wasting time
❌ **Don't run more chaos commands** - Can't reach server
❌ **Don't panic and break things** - Server is fine
❌ **Don't blame Wu-Tang** - The tool worked perfectly

---

## After Recovery: Prevent This Forever

1. **Update to latest version:**
   ```bash
   cd bring-da-ruckus
   git pull
   ```

2. **ALWAYS run in screen:**
   ```bash
   screen -S ruckus
   sudo python3 bring-da-ruckus.py
   # Detach: Ctrl+A then D
   ```

3. **Read the safety guide:**
   ```bash
   cat SAFETY-GUIDE.md
   ```

4. **Verify SSH protection before Shaolin Shadow:**
   - Look for: `SSH Protection: 🛡️  ENABLED`
   - Look for: `Your IP: x.x.x.x (will be whitelisted)`

---

## Emergency Contact Template

If you need help from your team:

```
URGENT: Server locked due to network chaos testing

Server: [hostname/IP]
Status: Unresponsive to SSH
Cause: Applied Shaolin Shadow (100% packet loss) without screen
Impact: Cannot access server remotely
Recovery: Need physical console or IPMI access

Actions needed:
1. Physical access to server console
2. Run: sudo tc qdisc del dev eth0 root
3. Run: sudo iptables -F
4. Or: Reboot server (power cycle)

ETA: ~5-10 minutes
Priority: Medium (server functional, just unreachable)
```

---

## Quick Decision Tree

```
Can't SSH to server?
│
├─ Running in screen/tmux?
│  ├─ YES → Wait 5 min for deadman's switch
│  └─ NO  → Process is dead, need physical access
│
├─ Have physical access?
│  ├─ YES → Go to console, run recovery commands
│  └─ NO  → Try next option
│
├─ Have IPMI/iLO access?
│  ├─ YES → Use remote console or reboot
│  └─ NO  → Try next option
│
├─ Have remote power control?
│  ├─ YES → Power cycle server
│  └─ NO  → Contact someone who does
│
└─ No access at all?
   └─ Wait for someone with physical access
   └─ Or wait for scheduled reboot (if any)
   └─ Or... schedule a data center visit
```

---

## Timeline Expectations

| Method | Time to Recovery | Requires |
|--------|-----------------|----------|
| Deadman's switch | 0-5 min | screen/tmux |
| Physical console | 5-10 min | Physical access |
| IPMI/iLO console | 5-10 min | Remote management |
| Physical reboot | 2-5 min | Physical access |
| Remote power cycle | 2-5 min | Power management |
| Wait for someone | Hours to days | Patience |

---

## Prevention Checklist for Next Time

Before using Shaolin Shadow:

- [ ] Running in `screen -S ruckus`
- [ ] SSH protection shows ENABLED
- [ ] Your IP detected and whitelisted
- [ ] Emergency recovery script ready
- [ ] Physical access OR IPMI available
- [ ] Team knows you're testing
- [ ] Read SAFETY-GUIDE.md

---

## Still Stuck?

**Remember:**
- Server is NOT broken
- Data is NOT lost
- Services are NOT damaged
- You just can't TALK to it

**You need physical or remote console access. There is no magic remote fix.**

---

*"The most important thing is to protect ya neck, but we forgot to protect our SSH." - The RZA (probably)*

☯️  Learn, adapt, and bring da ruckus more safely next time.
