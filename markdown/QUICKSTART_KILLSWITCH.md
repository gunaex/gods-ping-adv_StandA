# ⚡ Quick Start: Kill-Switch Improvements

## What's New?
✅ Popup when kill-switch triggers with "Continue & Reset" button  
✅ User action logs (config save, start, stop)  
✅ Requires 3 consecutive breaches before stopping (not just 1)  
✅ 60-minute cooldown after trigger  
✅ Baseline persists across restarts  
✅ Instant WebSocket notifications (no 5s polling delay)  

---

## 🚀 Setup (5 Minutes)

### Step 1: Start Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```
Wait for: `Application startup complete.`

### Step 2: Run Migration
```bash
# In a new terminal
cd backend
python migrate_killswitch.py
```
Expected output:
```
🔧 Running 4 migration(s):
  ✅ Added column: kill_switch_baseline
  ✅ Added column: kill_switch_last_trigger
  ✅ Added column: kill_switch_cooldown_minutes
  ✅ Added column: kill_switch_consecutive_breaches
✅ Migration complete!
```

### Step 3: Start Frontend
```bash
cd frontend
npm run dev
```
Open http://localhost:5173

### Step 4: Verify
1. **Login** (admin/admin)
2. **Open browser console** (F12)
3. **Look for:** `✅ WebSocket connected`
4. **Open Logs panel** → Filter "User Actions"
5. **Save config** → See log entry appear

---

## 🧪 Test Kill-Switch Flow

### Trigger Kill-Switch (Manual Test):
1. **Set threshold low:** Settings → `max_daily_loss = 2.0` (2%)
2. **Start Gods Hand:** Click "Start Gods Hand"
3. **Wait for market to drop 2%+ for 3 consecutive checks**
4. **Modal pops up** with:
   - Unrealized P/L: -X.XX%
   - Consecutive Breaches: 3/3
   - "Continue & Reset Baseline" button
5. **Click "Continue"** → Bot restarts with new baseline

---

## ⚙️ Configuration

### Default Settings (Recommended):
```javascript
max_daily_loss: 5.0                      // Stop if loss > 5%
kill_switch_consecutive_breaches: 3      // Need 3 consecutive breaches
kill_switch_cooldown_minutes: 60         // 1 hour cooldown
```

### More Conservative (Tighter Stop):
```javascript
max_daily_loss: 3.0                      // Stop if loss > 3%
kill_switch_consecutive_breaches: 2      // Only 2 breaches needed
kill_switch_cooldown_minutes: 120        // 2 hour cooldown
```

### More Aggressive (Looser Stop):
```javascript
max_daily_loss: 10.0                     // Stop if loss > 10%
kill_switch_consecutive_breaches: 5      // Need 5 consecutive breaches
kill_switch_cooldown_minutes: 30         // 30 minute cooldown
```

---

## 📊 Viewing Logs

### User Actions:
1. Click **"Logs"** button (top right)
2. Filter to **"👤 User Actions"**
3. See: Config saves, bot starts/stops, baseline resets

### Kill-Switch Events:
1. Click **"Logs"** button
2. Filter to **"🤖 Bot Operations"**
3. Search for: "KILL-SWITCH"

---

## 🐛 Troubleshooting

### WebSocket Not Connecting:
- **Check console:** Should see `✅ WebSocket connected`
- **If not:** Restart backend and refresh browser
- **Fallback:** Polling still works (5s delay instead of instant)

### Modal Not Appearing:
- **Check:** Is Gods Hand running? (status should be "running")
- **Check:** Has kill-switch triggered? (see logs for "KILL-SWITCH")
- **Check:** Is threshold set correctly? (e.g., `max_daily_loss = 5.0`)

### Migration Failed:
```bash
# If "no such table: bot_configs"
# 1. Start backend first to create tables
python -m uvicorn app.main:app --reload

# 2. In new terminal, run migration
python migrate_killswitch.py
```

---

## 📱 Using the Kill-Switch Modal

### When It Appears:
- Automatically pops up when kill-switch triggers
- Shows detailed info about the stop

### What to Do:
1. **Review Details:**
   - Unrealized P/L: How much loss triggered the stop
   - Consecutive Breaches: How many checks failed (e.g., 3/3)
   - Baseline: Current baseline (if set)
   - Position Value: Current value of your position

2. **Options:**
   - **"Continue & Reset Baseline"** → Accepts current loss as new baseline and restarts bot
   - **"View Logs"** → Opens logs panel to see full history
   - **Close (X)** → Dismisses modal, bot stays stopped

### After Clicking "Continue":
- Baseline is set to current P/L (e.g., -7% becomes new 0%)
- Gods Hand restarts automatically
- Cooldown period starts (no new checks for 60 min)

---

## 🎯 Best Practices

### 1. Set Realistic Thresholds:
```javascript
// For volatile markets (BTC, ETH)
max_daily_loss: 10.0  // Allow more room for volatility

// For stable markets (USDC, stablecoins)
max_daily_loss: 2.0   // Tighter control
```

### 2. Monitor User Logs:
- Check daily for: excessive start/stop cycles
- Sign of: too-sensitive threshold or market volatility

### 3. Adjust Consecutive Breaches:
```javascript
// If getting false positives (stop too often)
kill_switch_consecutive_breaches: 5  // Require more breaches

// If losses are running away before stop
kill_switch_consecutive_breaches: 2  // Faster stop
```

### 4. Use Baseline After Major Events:
- After resetting: baseline is your new "zero"
- Use when: accepting a loss and starting fresh
- Example: -10% loss → reset → new baseline at -10% → next stop at -15% (5% from new baseline)

---

## 📖 API Reference

### Reset Kill-Switch Baseline:
```bash
POST /api/bot/gods-hand/reset-kill-switch?restart=true
Authorization: Bearer {token}

Response:
{
  "ok": true,
  "baseline": {
    "status": "reset",
    "baseline_pl_percent": -7.5
  },
  "restarted": true
}
```

### WebSocket Connection:
```javascript
const token = localStorage.getItem('token');
const ws = new WebSocket(`ws://localhost:8000/ws/logs/${token}`);

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (message.type === 'kill_switch') {
    // Handle kill-switch event
    console.log('Kill-switch triggered:', message.data);
  }
};
```

---

## ✅ Verification Checklist

After setup, verify:
- [ ] Backend started without errors
- [ ] Migration completed successfully
- [ ] Frontend shows "✅ WebSocket connected" in console
- [ ] Logs panel shows "User Actions" filter
- [ ] Saving config creates a USER log entry
- [ ] Starting Gods Hand creates a USER log entry
- [ ] Kill-switch modal appears when threshold breached
- [ ] "Continue & Reset" button works and restarts bot

---

## 🆘 Need Help?

### Documentation:
- **Full details:** `KILLSWITCH_IMPROVEMENTS.md`
- **Implementation:** `KILLSWITCH_IMPLEMENTATION_SUMMARY.md`

### Common Issues:
1. **"No such column"** → Run migration script
2. **WebSocket not connecting** → Check backend logs for errors
3. **Modal not showing** → Check browser console for errors
4. **Logs not appearing** → Clear logs and trigger new events

---

**Ready to go!** 🚀  
Start trading with enhanced safety and monitoring!
