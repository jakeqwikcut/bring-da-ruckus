# QwikCut Camera System Test Scenarios
## The 36 Chambers of Chaos - Testing Methodology

**Created by Jake Mammen - 2025**

Use these scenarios to systematically test how your QwikCut camera system behaves under various network conditions. Progress through the chambers from peace to total darkness.

🥷 **Wu-Tang is for the children. Test responsibly.** 🥷

## Pre-Test Checklist

- [ ] QwikCam is online and streaming
- [ ] Baseline metrics recorded (normal operation)
- [ ] Monitoring tools ready (stream viewer, S3 console, logs)
- [ ] Test duration planned (typically 10-30 minutes per scenario)
- [ ] Deadman switch timeout set appropriately

## Baseline (No Ruckus)

**Goal:** Establish normal operation metrics

**Chaos Chamber:** ☯️ Chamber 0: Peace

**Duration:** 15 minutes

**What to Monitor:**
- RTSP stream quality and bitrate
- Video file upload timing
- S3 upload success rate
- API response times
- WebSocket command latency

**Expected Results:**
- Smooth stream at configured quality
- Uploads complete within X seconds
- 100% upload success rate
- API calls < 200ms
- Commands respond < 500ms

---

## Scenario 1: Typical Home Internet

**Goal:** Test under normal consumer internet conditions

**Chaos Chamber:** 🥋 Chamber 1: The Swarm
- 50ms latency
- 1% packet loss
- 50 Mbps bandwidth

**Duration:** 20 minutes

**What to Monitor:**
- Stream quality (should remain good)
- Upload timing (may be slightly delayed)
- Buffer/queue behavior
- Command responsiveness

**Expected Results:**
- Minor stream quality impact
- Uploads take slightly longer but succeed
- System operates normally overall

**Issues to Look For:**
- Stream freezing
- Corrupted uploads
- Command timeouts

---

## Scenario 2: Congested Network

**Goal:** Simulate multiple devices competing for bandwidth

**Chaos Chamber:** ⚔️ Chamber 9: The Mystery
- 150ms latency
- 3% packet loss
- 10 Mbps bandwidth

**Duration:** 30 minutes

**What to Monitor:**
- Stream adaptation (does quality degrade gracefully?)
- Upload queue building up
- Storage space consumption
- Error rates in logs

**Expected Results:**
- Stream quality reduced but stable
- Uploads queued but processing
- System remains functional
- Possible buffering but no crashes

**Issues to Look For:**
- Stream complete failure
- Upload queue not processing
- Storage filling up uncontrollably
- System becoming unresponsive

---

## Scenario 3: Poor Connection

**Goal:** Test at edge of acceptable performance

**Chaos Chamber:** 🔥 Chamber 18: The Deadly Venoms
- 300ms latency
- 8% packet loss
- 2 Mbps bandwidth

**Duration:** 30 minutes

**What to Monitor:**
- Stream stability
- Upload success vs. failure rate
- Retry logic behavior
- System resource usage (CPU, memory, storage)

**Expected Results:**
- Significant quality degradation
- Uploads heavily delayed
- Multiple retries
- System should still record locally

**Issues to Look For:**
- Complete stream failure
- Corrupted video files
- System crash or freeze
- Inability to recover when network improves

---

## Scenario 4: Near-Failure Conditions

**Goal:** Test extreme degradation before complete failure

**Chaos Chamber:** 💀 Chamber 36: Liquid Swords
- 500ms latency
- 15% packet loss
- 512 Kbps bandwidth

**Duration:** 20 minutes

**What to Monitor:**
- Local recording continues?
- Upload attempts vs. successes
- Error handling and logging
- System stability

**Expected Results:**
- Cloud services mostly unavailable
- Local recording must continue
- Graceful error handling
- No data corruption

**Issues to Look For:**
- System crashes
- Recording stops
- File corruption
- Unrecoverable errors

---

## Scenario 5: Complete Outage

**Goal:** Verify autonomous operation and recovery

**Chaos Chamber:** ☠️ Shaolin Shadow: Total Darkness
- 100% packet loss

**Duration:** 15 minutes outage + 15 minutes recovery

**Test Procedure:**
1. Apply Complete Outage level (15 min)
2. Clear ruckus and restore network (15 min)
3. Monitor recovery process

**What to Monitor:**
- Local recording continues during outage
- Storage management
- Automatic reconnection
- Upload queue processing after recovery
- Data integrity of queued uploads

**Expected Results:**
- Recording never stops
- Files queued locally
- Automatic reconnection when network returns
- Queued files upload successfully
- No data loss or corruption

**Issues to Look For:**
- Recording stops during outage
- System doesn't reconnect automatically
- Queued files fail to upload
- File corruption
- System requires manual intervention

---

## Scenario 6: Intermittent Chaos

**Goal:** Test recovery and adaptation through transitions

**Chaos Chambers:** Progressive through the chambers
- Start: Chamber 1 - The Swarm (5 min)
- Chamber 9 - The Mystery (5 min)
- Chamber 18 - The Deadly Venoms (5 min)
- Back to Chamber 9 (5 min)
- Back to Chamber 1 (5 min)
- Clear to Peace (5 min)

**Duration:** 30 minutes

**What to Monitor:**
- Quality adaptation during transitions
- Upload queue behavior
- System stability through changes
- Recovery time when conditions improve

**Expected Results:**
- Smooth adaptation to changing conditions
- Quality scales with available bandwidth
- No crashes during transitions
- Uploads catch up when bandwidth improves

**Issues to Look For:**
- System gets "stuck" at lower quality
- Crashes during transitions
- Upload queue grows indefinitely
- Poor recovery when network improves

---

## Scenario 7: Targeted Disruption

**Goal:** Isolate camera-to-cloud path specifically

**Chaos Chamber:** ⚔️ Chamber 9: The Mystery (with target IP)

**Setup:**
```bash
sudo python3 bring-da-ruckus.py --target [QWIKCAM_IP] --level ninth
```

**Duration:** 20 minutes

**What to Monitor:**
- Camera-specific impacts
- Other LAN devices remain unaffected
- Isolation of camera traffic

**Expected Results:**
- Only camera traffic disrupted
- Rest of network normal
- Same results as Scenario 2 but isolated

---

## Scenario 8: Long-Duration Stress Test

**Goal:** Test sustained operation under stress

**Chaos Chamber:** ⚔️ Chamber 9: The Mystery

**Duration:** 2-4 hours

**What to Monitor:**
- Resource leaks (memory, storage)
- Upload queue steady-state behavior
- Long-term stability
- Logs for repeated errors

**Expected Results:**
- Stable operation throughout
- Upload queue reaches equilibrium
- No resource exhaustion
- Consistent behavior

**Issues to Look For:**
- Memory leaks
- Storage exhaustion
- Performance degradation over time
- System becomes unstable

---

## Test Result Template

For each scenario, record:

```
## Scenario: [Name]
Date: [YYYY-MM-DD]
Duration: [X minutes]
Chaos Chamber: [Chamber Name]

### Observations
- Stream quality: [Description]
- Upload behavior: [Description]
- System stability: [Description]
- Unexpected issues: [Description]

### Metrics
- Upload success rate: [X%]
- Average upload time: [X seconds]
- Command latency: [X ms]
- Errors/warnings: [Count]

### Verdict
✅ PASS / ⚠️ ISSUES / ❌ FAIL

### Notes
[Additional observations, screenshots, log excerpts]

### Action Items
- [ ] [Fix or investigation needed]
- [ ] [Configuration adjustment]
```

---

## Interpreting Results

### Healthy System Indicators
- ✅ Degrades gracefully, never crashes
- ✅ Continues local recording during outages
- ✅ Automatically recovers when network improves
- ✅ Uploads eventually catch up
- ✅ No file corruption
- ✅ Reasonable resource usage

### Problem Indicators
- ❌ Crashes under network stress
- ❌ Recording stops during disruptions
- ❌ Corrupted video files
- ❌ Doesn't reconnect automatically
- ❌ Upload queue grows unbounded
- ❌ Memory/storage leaks
- ❌ Poor/no recovery after outage

---

## Recommended Testing Schedule

**Phase 1: Basic Validation (1 day)**
- Baseline
- Scenario 1 (Light)
- Scenario 2 (Moderate)

**Phase 2: Stress Testing (1 day)**
- Scenario 3 (Heavy)
- Scenario 4 (Extreme)
- Scenario 5 (Outage)

**Phase 3: Advanced Testing (1 day)**
- Scenario 6 (Intermittent)
- Scenario 8 (Long-duration)

**Phase 4: Targeted Testing (As needed)**
- Scenario 7 (Targeted disruption)
- Custom scenarios based on Phase 1-3 findings

---

## Safety Reminders

- ⏰ Keep deadman switch timeout reasonable (10-30 min)
- 👀 Monitor actively during tests
- 📊 Document everything
- 🔄 Always restore network between tests
- 💾 Back up critical data before testing
- 🛑 Stop immediately if system behaves dangerously

---

## Quick Reference: Symptoms vs. Chaos Chamber

| Symptom | Likely Cause | Test With |
|---------|--------------|--------|
| Stream pixelated/stuttering | Low bandwidth | Chamber 9/18 |
| Upload delays | Bandwidth + latency | Chamber 1/9 |
| Command lag | High latency | Chamber 18/36 |
| Intermittent disconnects | Packet loss | Chamber 9/18 |
| Failed uploads | High packet loss | Chamber 18/36 |
| Complete failure | Total outage | Shaolin Shadow |

**Now go forth and bring da ruckus! 🥷**
