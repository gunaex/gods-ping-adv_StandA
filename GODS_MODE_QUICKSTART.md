# 🚀 Gods Mode Quick Start Guide

## What is Gods Mode?

Gods Mode is an **advanced AI trading system** specifically designed for **sideways-down (bearish) markets** - perfect for the current crypto market conditions!

It uses a **3-layer AI architecture**:
1. **Model A**: Forecasts future price using momentum
2. **Model B**: Detects market regime (downtrend, range, etc.)
3. **Meta-Model**: Intelligently combines both models based on conditions

## ⚡ 5-Minute Setup

### Step 1: Run Database Migration
```bash
cd backend
python migrate_gods_mode.py
```
Expected output: `✅ Added 'gods_mode_enabled' column`

### Step 2: Start Your App
```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm run dev
```

### Step 3: Enable Gods Mode

1. **Login** to your app
2. Go to **Gods Hand** panel (bottom of page)
3. Click **⚙️ Settings** button
4. Find the **Gods Mode** toggle:
   ```
   🤖 Standard AI  →  🚀 GODS MODE
   ```
5. Click to enable (it will glow red!)
6. Click **Save Settings**

### Step 4: Verify It's Working

✅ You should see a new panel appear:
```
🧠 GODS MODE - Meta-Model AI Analytics
```

✅ This panel shows:
- 📈 Model A (Forecaster)
- 🎯 Model B (Classifier)  
- 🧠 Meta-Model (Gating Logic)

### Step 5: Start Trading!

1. Click **Execute Now** in Gods Hand
2. Watch the logs - you should see:
   ```
   AI DECISION CALCULATION for BTC/USDT (GODS MODE (Meta-Model AI))
   ```
3. Check the decision reasoning in the Gods Hand panel

---

## 🎯 Current Market Strategy (Sideways-Down)

### Recommended Settings for Bearish Markets

```
Paper Trading: ON ✅ (test first!)
Budget: $10,000
Risk Level: Conservative 🛡️
Min Confidence: 75%
Entry Step: 5% (small positions)
Exit Step: 15% (quick exits)
Trailing TP: 2.5%
Hard Stop Loss: 3.0%
Gods Mode: ON 🚀
```

### Why These Settings?

- **Conservative risk**: Protect capital in uncertain markets
- **High confidence (75%)**: Only take high-probability trades
- **Small entries (5%)**: Build positions gradually
- **Fast exits (15%)**: Lock in profits quickly
- **Tight stops (3%)**: Limit downside

---

## 📊 What to Expect

### Gods Mode Trading Logic

In **sideways-down markets**, Gods Mode will:

✅ **SELL/SHORT** when:
- Downtrend detected + RSI > 50
- Range resistance + RSI > 65
- High volatility + RSI > 70

✅ **BUY** when:
- Range support + RSI < 35 + low volatility
- Oversold bounce + RSI < 30

❌ **HOLD** when:
- Confidence < 75%
- High volatility + RSI < 30 (don't catch falling knife)
- No clear edge

### Example Decision

```json
{
  "signal": "SELL",
  "confidence": 82%,
  "reason": "Downtrend: Both models agree SHORT (forecast: $41,850)"
}
```

---

## 🧪 Testing & Validation

### Day 1-2: Paper Trading
1. Enable **Paper Trading** mode
2. Let Gods Mode run for 24-48 hours
3. Check **Paper Trading Performance** panel
4. Goal: Win rate > 55%, Net P/L > 0%

### Day 3-4: Compare Results
1. Check Gods Mode vs Standard AI performance
2. Look at logs to understand decisions
3. Adjust `min_confidence` if needed:
   - Too many trades? Increase to 80%
   - Too few trades? Decrease to 70%

### Day 5+: Go Live (Optional)
1. Only if paper trading shows profit!
2. Disable **Paper Trading** mode
3. Start with small budget ($100-$500)
4. Monitor closely for first week

---

## 🔍 Monitoring & Debugging

### Check if Gods Mode is Active

**In Logs** (📝 Logs button):
```
AI DECISION CALCULATION for BTC/USDT (GODS MODE (Meta-Model AI))
```
Should say "GODS MODE" not "Standard AI"

**In Gods Mode Panel**:
- Panel should be visible
- ACTIVE badge should be glowing

### Understanding Decisions

Each decision shows:
- **Signal**: BUY/SELL/SHORT/COVER/HOLD
- **Confidence**: 0-100%
- **Reason**: Why this decision was made

Example reason:
```
"Range market: Model A forecasts +2.3% rise, RSI=45"
```
This means:
- Market is range-bound (not trending)
- Model A predicts price will rise 2.3%
- RSI is neutral (45)
- Action: BUY opportunity

---

## ⚠️ Important Notes

### Risk Management

1. **Always start with paper trading**
2. **Never invest more than you can lose**
3. **Set max_daily_loss limits** (default: 5%)
4. **Monitor daily** - don't set and forget

### When Gods Mode Works Best

✅ Perfect for:
- Bitcoin/Ethereum in bearish trend
- Sideways markets (low volatility)
- High volatility with clear reversals

❌ Not ideal for:
- Strong bull runs (use Standard AI)
- Extremely low liquidity coins
- News-driven pumps/dumps

### Performance Expectations

**Realistic goals** (paper trading):
- Win rate: 55-70%
- Monthly return: 3-8%
- Max drawdown: 5-10%

**Red flags** (stop trading):
- Win rate < 40%
- Daily loss > 10%
- Confidence always < 60%

---

## 🆘 Troubleshooting

### "Gods Mode panel doesn't appear"
**Fix**: 
1. Refresh page (F5)
2. Check Settings → Gods Mode is ON
3. Clear browser cache

### "No trades executed"
**Check**:
1. Confidence < min_confidence? (increase threshold)
2. Position limit reached? (check budget)
3. Market regime = HIGH_VOLATILITY? (wait for calm)

### "Too many HOLD signals"
**Fix**:
- Lower `min_confidence` from 75% to 70%
- Check market is not in HIGH_VOLATILITY regime
- Review logs for detailed reasons

### "Losing money"
**Action**:
1. **STOP** immediately
2. Switch to paper trading
3. Review last 10 trades in logs
4. Adjust settings (higher confidence, smaller steps)
5. Consider switching back to Standard AI

---

## 📚 Learn More

- **[GODS_MODE_GUIDE.md](GODS_MODE_GUIDE.md)** - Complete technical guide
- **[GODS_MODE_IMPLEMENTATION.md](GODS_MODE_IMPLEMENTATION.md)** - For developers
- **Logs Panel** - Real-time decision explanations

---

## 🎯 Success Checklist

Before going live, make sure:

- [x] Migration completed successfully
- [x] Gods Mode panel appears
- [x] Paper trading shows profit (24h+)
- [x] Win rate > 55%
- [x] Understanding decision reasoning
- [x] Set max_daily_loss limit
- [x] Started with small budget (<$500)
- [x] Monitoring daily performance

---

## 💡 Pro Tips

1. **Review logs daily** - Learn from AI decisions
2. **Adjust confidence** - Higher = safer, Lower = more trades
3. **Watch volatility** - Gods Mode adapts automatically
4. **Be patient** - Sideways markets = fewer trades (normal!)
5. **Take profits** - Don't be greedy, trailing TP is your friend

---

**Ready to profit in bearish markets? Enable Gods Mode now!** 🚀

Questions? Check the logs or documentation.

Happy Trading! 💰
