# 🎯 Incremental Position Building - Quick Reference

## What Changed

### Before (All-in/All-out)
```
BUY Signal  →  Invest 100% of position size  →  DONE
SELL Signal →  Sell 100% of holdings        →  DONE
```

### After (Incremental DCA)
```
BUY Signal #1  →  Invest 10% of max position  →  Position: 10%
BUY Signal #2  →  Invest 10% of max position  →  Position: 20%
BUY Signal #3  →  Invest 10% of max position  →  Position: 30%
...
BUY Signal #10 →  Invest 10% of max position  →  Position: 100% ✅
BUY Signal #11 →  HOLD (Already at 100%)      →  Position: 100%

SELL Signal #1  →  Sell 10% of holdings       →  Position: 90%
SELL Signal #2  →  Sell 10% of holdings       →  Position: 80%
...
SELL Signal #10 →  Sell remaining 10%         →  Position: 0% ✅
```

---

## New Settings

### Location: Settings Modal → Risk Management

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| **Entry Step %** | 1-100% | 10% | How much to BUY per BUY signal |
| **Exit Step %** | 1-100% | 10% | How much to SELL per SELL signal |

---

## Your 3 Scenarios Explained

### 1️⃣ Consecutive BUY Signals (Accumulation)

```
Time     Signal  Action              Position
─────────────────────────────────────────────────
10:00    BUY     Buy 10%            10% ($712)
10:01    BUY     Buy 10%            20% ($1,425)
10:02    BUY     Buy 10%            30% ($2,138)
10:03    BUY     Buy 10%            40% ($2,850)
10:04    BUY     Buy 10%            50% ($3,563)
10:05    BUY     Buy 10%            60% ($4,275)
10:06    BUY     Buy 10%            70% ($4,988)
10:07    BUY     Buy 10%            80% ($5,700)
10:08    BUY     Buy 10%            90% ($6,413)
10:09    BUY     Buy 10%            100% ($7,125) ✅ FULL
10:10    BUY     HOLD (at limit)    100% (no change)
```

**Result:** Gradually accumulated position, averaging out price movements

---

### 2️⃣ Consecutive SELL Signals (Exit)

```
Time     Signal  Action              Position
─────────────────────────────────────────────────
Starting with 100% position (0.12 BTC)

11:00    SELL    Sell 10% of 0.12   90% (0.108 BTC)
11:01    SELL    Sell 10% of 0.108  80% (0.0972 BTC)
11:02    SELL    Sell 10% of 0.0972 70% (0.0875 BTC)
11:03    SELL    Sell 10% of 0.0875 60% (0.0787 BTC)
11:04    SELL    Sell 10% of 0.0787 50% (0.0708 BTC)
11:05    SELL    Sell 10% of 0.0708 40% (0.0637 BTC)
11:06    SELL    Sell 10% of 0.0637 30% (0.0573 BTC)
11:07    SELL    Sell 10% of 0.0573 20% (0.0516 BTC)
11:08    SELL    Sell 10% of 0.0516 10% (0.0464 BTC)
11:09    SELL    Sell remaining 10%  0% ✅ FULLY EXITED
11:10    SELL    HOLD (no position) 0% (no change)
```

**Result:** Gradual exit, reducing risk incrementally

---

### 3️⃣ Mixed Signals (Market Reversal)

```
Time     Signal  Action              Position    Reason
──────────────────────────────────────────────────────────────
Starting with 50% position

12:00    BUY     Buy 10%            60%         Uptrend
12:01    BUY     Buy 10%            70%         Still up
12:02    SELL ⚠️  Sell 10% of 70%    63%         Reversal!
12:03    SELL    Sell 10% of 63%    56.7%       Downtrend
12:04    BUY ⚠️   Buy 10%            66.7%       Bounced!
12:05    BUY     Buy 10%            76.7%       Recovery
12:06    SELL ⚠️  Sell 10% of 76.7%  69%         Weak again
```

**Result:** AI can change direction anytime, adapting to market

---

## Fee Management (CRITICAL!)

### Trading Fees: 0.1% per trade

#### Example with 10% Steps (10 trades to 100%)

**Entry Fees:**
- 10 BUY trades × 0.1% each = 1% total fee on entry
- On $7,125 position = ~$71 in fees

**Exit Fees:**
- 10 SELL trades × 0.1% each = 1% total fee on exit  
- On $7,125 position = ~$71 in fees

**Total Round-Trip Fees:** ~$142 (2% of position)

**What this means:**
✅ Need > 2% profit to break even
✅ Smaller steps (5%) = more trades = more fees
✅ Larger steps (25%) = fewer trades = less fees
✅ **Sweet spot: 10% steps balances DCA benefits vs fee costs**

### Fee Tracking

Every trade automatically includes fees in your position:

```json
{
  "current_position": {
    "quantity": 0.05,
    "cost_basis": 3000.00,
    "total_fees_paid": 30.50,  // ← Monitor this!
    "trades_count": 10
  }
}
```

---

## Quick Start Guide

### Step 1: Configure Settings

1. Open **Settings** → **Risk Management**
2. Set **Entry Step %**: `10` (recommended)
3. Set **Exit Step %**: `10` (recommended)
4. Click **Save All Settings**

### Step 2: Enable Continuous Mode

1. Go to **Gods Hand** tab
2. Toggle **Continuous Mode**: ON
3. Set **Interval**: `60` seconds
4. Click **Execute Now**

### Step 3: Monitor Logs

Watch the logs for position updates:

```
✅ "Adding 10% step ($712.50) to existing 30% position"
✅ "Position before: 30% → Position after: 40%"
✅ "Fees included in position tracking (0.1%)"
```

### Step 4: Check Position Fill

In log details, look for:
```json
"current_fill_percent": 40.0
"after_fill_percent": 50.0
```

---

## Recommended Settings by Experience

### Beginner (Safe DCA)
```yaml
Entry Step: 5%   # Very gradual entry
Exit Step: 20%   # Faster exit for safety
Interval: 300s   # Check every 5 minutes
Risk Level: Conservative
```

### Intermediate (Balanced)
```yaml
Entry Step: 10%  # Standard DCA
Exit Step: 10%   # Balanced exit
Interval: 60s    # Check every minute
Risk Level: Moderate
```

### Advanced (Fast Trading)
```yaml
Entry Step: 20%  # Quick accumulation
Exit Step: 25%   # Quick exits
Interval: 30s    # Check every 30 seconds
Risk Level: Aggressive
```

---

## Files Modified

### Backend
- ✅ `backend/app/models.py` - Added `entry_step_percent` and `exit_step_percent` columns
- ✅ `backend/app/position_tracker.py` - NEW FILE with position tracking logic
- ✅ `backend/app/bots.py` - Updated `gods_hand_once()` for incremental trading

### Frontend
- ✅ `frontend/src/components/SettingsModal.tsx` - Added Entry/Exit step % controls

### Documentation
- ✅ `INCREMENTAL_POSITION_BUILDING_GUIDE.md` - Complete 15-minute guide with examples
- ✅ `INCREMENTAL_QUICK_REFERENCE.md` - This file (quick lookup)

---

## Testing Checklist

Before going live, test in paper trading:

- [ ] Set entry_step to 10%, start continuous mode
- [ ] Watch logs - should see "Adding 10% to existing X% position"
- [ ] Check position increases by 10% each BUY
- [ ] Verify fees are tracked in total_fees_paid
- [ ] Test SELL signals reduce position by 10%
- [ ] Confirm cannot buy beyond 100%
- [ ] Confirm cannot sell below 0%
- [ ] Test mixed BUY/SELL signals work correctly

---

## Troubleshooting

### "Already at 100% - cannot buy more"
✅ **Normal!** Position is full. Bot will HOLD until SELL signal.

### "No position to sell"
✅ **Normal!** You exited completely. Bot will HOLD until BUY signal.

### Fees seem high
⚠️ Check `total_fees_paid` in logs. If > 2% of position, consider:
- Increasing step % (fewer trades)
- Longer intervals (less frequent trading)
- Higher confidence threshold (fewer signals)

### Position not reaching 100%
Check:
- Are BUY signals stopping? (check AI logs)
- Is confidence dropping below threshold?
- Is continuous mode still running?

---

## Support

- **Full Guide:** `INCREMENTAL_POSITION_BUILDING_GUIDE.md`
- **Position Sizing:** `CONTINUOUS_MODE_AND_POSITION_SIZE_GUIDE.md`
- **AI Strategy:** `AI_STRATEGY_GUIDE.md`
- **General Help:** `README.md`

---

**🎉 You're now ready for incremental position building!**

Start with paper trading, monitor for 1-2 days, then go live when comfortable.
