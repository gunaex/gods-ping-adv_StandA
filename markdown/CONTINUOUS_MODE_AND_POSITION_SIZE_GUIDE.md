# 🤖 Continuous Mode & Position Size Guide

## 📋 Table of Contents
1. [Continuous Mode](#continuous-mode)
2. [Position Size](#position-size)
3. [How They Work Together](#how-they-work-together)
4. [Examples](#examples)
5. [Best Practices](#best-practices)

---

## 🔄 Continuous Mode

### What is Continuous Mode?

**Gods Hand bot has 2 execution modes:**

| Mode | Behavior | Use Case |
|------|----------|----------|
| **One-off** (Continuous OFF) | Runs once when you click "Execute Now" | Manual control, testing, learning |
| **Continuous** (Continuous ON) | Runs automatically every X seconds | Automated 24/7 trading |

### How It Works

```
┌─────────────────────────────────────────┐
│ Continuous Mode: OFF (Default)          │
├─────────────────────────────────────────┤
│ 1. Click "Execute Now"                  │
│ 2. AI analyzes market                   │
│ 3. Makes decision (BUY/SELL/HOLD)       │
│ 4. STOPS ⏸️                              │
│ 5. You must click again for next check  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Continuous Mode: ON                      │
├─────────────────────────────────────────┤
│ 1. Click "Execute Now"                  │
│ 2. AI analyzes market                   │
│ 3. Makes decision (BUY/SELL/HOLD)       │
│ 4. Waits for interval (e.g., 60 sec) ⏱️  │
│ 5. Repeats from step 2 automatically    │
│ 6. Runs until you click "Stop" 🛑       │
└─────────────────────────────────────────┘
```

### Settings

**Interval (10-3600 seconds):**
- **60 seconds:** High frequency (checks every minute)
- **300 seconds:** Moderate (checks every 5 minutes)
- **900 seconds:** Conservative (checks every 15 minutes)
- **3600 seconds:** Low frequency (checks every hour)

**Recommendation:**
- **Day Trading:** 60-300 seconds (fast market changes)
- **Swing Trading:** 900-3600 seconds (slower trends)
- **Testing:** Start with 300 seconds and adjust

---

## 💰 Position Size

### What is Position Size?

**Position size = How much money the bot uses per trade**

This is controlled by TWO settings that multiply together:

1. **Position Size Ratio** (10%-100%, default 95%)
2. **Risk Level** (Conservative/Moderate/Aggressive)

### The Formula

```
Your Budget: $10,000
Position Size Ratio: 95% (0.95)
Risk Level: Moderate

Step 1: Calculate Max Position
Max Position = Budget × Position Size Ratio
Max Position = $10,000 × 0.95 = $9,500

Step 2: Apply Risk Level Multiplier
┌──────────────┬────────────┬──────────────┐
│  Risk Level  │ Multiplier │ Final Amount │
├──────────────┼────────────┼──────────────┤
│ Conservative │   0.50×    │    $4,750    │
│ Moderate     │   0.75×    │    $7,125    │
│ Aggressive   │   1.00×    │    $9,500    │
└──────────────┴────────────┴──────────────┘

Result: Bot will use $7,125 per trade
```

### Position Size Ratio Explained

**What it does:**
- Sets the **maximum** percentage of your budget available for trading
- Leaves some cash as a safety buffer
- Prevents you from going "all-in" on a single trade

**Examples:**

| Budget | Ratio | Max Available | Buffer |
|--------|-------|---------------|--------|
| $10,000 | 95% | $9,500 | $500 (5%) |
| $10,000 | 80% | $8,000 | $2,000 (20%) |
| $10,000 | 50% | $5,000 | $5,000 (50%) |

**Why have a buffer?**
- Exchange fees might exceed your cash
- Market volatility can change prices before order executes
- Safety margin for unexpected costs

---

## 🎯 How They Work Together

### Example Scenario

**Your Settings:**
```yaml
Budget: $10,000
Position Size Ratio: 95%
Risk Level: Moderate (75%)
Continuous Mode: ON
Interval: 60 seconds
```

**What Happens:**

```
Time: 10:00:00 AM
┌─────────────────────────────────────┐
│ AI Check #1                         │
├─────────────────────────────────────┤
│ Signal: BUY (Uptrend + Dip)         │
│ Confidence: 70%                     │
│ Position: $10,000 × 0.95 × 0.75     │
│         = $7,125                    │
│ ACTION: Buy BTC for $7,125 ✅       │
└─────────────────────────────────────┘

Time: 10:01:00 AM (60 seconds later)
┌─────────────────────────────────────┐
│ AI Check #2                         │
├─────────────────────────────────────┤
│ Signal: HOLD (Already have position)│
│ Confidence: N/A                     │
│ ACTION: No trade                    │
└─────────────────────────────────────┘

Time: 10:02:00 AM (60 seconds later)
┌─────────────────────────────────────┐
│ AI Check #3                         │
├─────────────────────────────────────┤
│ Signal: SELL (Downtrend starts)     │
│ Confidence: 70%                     │
│ ACTION: Sell all BTC ✅             │
│ Profit/Loss: +$150 (2.1%)           │
└─────────────────────────────────────┘

... Continues every 60 seconds ...
```

---

## 📊 Examples

### Example 1: Conservative Safe Trading

**Settings:**
```yaml
Budget: $5,000
Position Size Ratio: 80%
Risk Level: Conservative
Continuous Mode: ON
Interval: 300 seconds (5 min)
```

**Result:**
- Max Position: $5,000 × 0.80 = $4,000
- Actual Position: $4,000 × 0.50 = **$2,000 per trade**
- Checks market every 5 minutes
- Low risk, lower returns
- Good for beginners

---

### Example 2: Moderate Balanced Trading

**Settings:**
```yaml
Budget: $10,000
Position Size Ratio: 95%
Risk Level: Moderate
Continuous Mode: ON
Interval: 60 seconds (1 min)
```

**Result:**
- Max Position: $10,000 × 0.95 = $9,500
- Actual Position: $9,500 × 0.75 = **$7,125 per trade**
- Checks market every minute
- Balanced risk/reward
- Good for experienced traders

---

### Example 3: Aggressive High-Frequency Trading

**Settings:**
```yaml
Budget: $20,000
Position Size Ratio: 100%
Risk Level: Aggressive
Continuous Mode: ON
Interval: 10 seconds
```

**Result:**
- Max Position: $20,000 × 1.00 = $20,000
- Actual Position: $20,000 × 1.00 = **$20,000 per trade**
- Checks market every 10 seconds
- Maximum risk, maximum returns
- ⚠️ **DANGER:** All eggs in one basket!

---

## ✅ Best Practices

### Position Size Recommendations

| Your Experience | Position Size Ratio | Risk Level |
|----------------|---------------------|------------|
| Beginner       | 50-70%             | Conservative |
| Intermediate   | 80-95%             | Moderate     |
| Expert         | 95-100%            | Aggressive   |

### Interval Recommendations

| Market Condition | Interval | Why |
|-----------------|----------|-----|
| High volatility (BTC pumping) | 60-120 sec | Catch quick moves |
| Normal market | 300-600 sec | Balance speed/cost |
| Low volatility (sideways) | 900-3600 sec | Avoid overtrading |
| Sleeping hours | Turn OFF | Don't trade while sleeping |

### Risk Management Rules

1. **Never use 100% position size ratio + Aggressive risk** unless you understand the risks
2. **Start small:** Begin with Conservative risk and low budget
3. **Test in paper trading first:** Enable paper trading in Settings
4. **Monitor regularly:** Even in continuous mode, check logs daily
5. **Set max daily loss:** Use the "Max Daily Loss %" setting (default 10%)
6. **Have a buffer:** Leave 5-10% of budget unused (position_size_ratio = 90-95%)

---

## 🎓 Learning Path

**Week 1: Understanding**
- ✅ Run in one-off mode (continuous OFF)
- ✅ Click "Execute Now" manually and watch AI decisions
- ✅ Read logs and understand why AI buys/sells
- ✅ Use position_size_ratio = 50%, Conservative risk

**Week 2: Testing**
- ✅ Enable continuous mode with 300-second interval
- ✅ Monitor for 1-2 days
- ✅ Analyze performance in Performance tab
- ✅ Adjust position_size_ratio to 70-80%

**Week 3: Optimizing**
- ✅ Find your optimal interval based on win rate
- ✅ Experiment with Moderate risk level
- ✅ Increase position_size_ratio to 90-95%
- ✅ Fine-tune based on market conditions

**Week 4: Automation**
- ✅ Fully automated 24/7 trading
- ✅ Daily performance reviews
- ✅ Adjust settings based on market trends
- ✅ Enjoy profits! 🎉

---

## 🚨 Common Mistakes to Avoid

❌ **DON'T:**
- Use 100% position size + Aggressive risk without experience
- Set interval too low (< 60 seconds) unless you know what you're doing
- Trade with real money before testing in paper mode
- Run continuous mode without checking logs regularly
- Ignore max daily loss warnings

✅ **DO:**
- Start conservative and gradually increase risk
- Monitor performance and adjust settings
- Use paper trading to learn
- Read AI strategy guide (AI_STRATEGY_GUIDE.md)
- Keep some budget as buffer (position_size_ratio < 100%)

---

## 📖 Related Documentation

- **AI_STRATEGY_GUIDE.md:** Understand how AI makes trading decisions
- **README.md:** General setup and features
- **Settings Modal:** Configure all these settings in the UI

---

**Happy Trading! 🚀**
