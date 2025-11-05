# Gods Hand AI Trading Strategy
**Balanced Strategy - Updated November 5, 2025**

## Strategy Overview

The AI uses a **BALANCED** approach that combines:
- ✅ Trend following (buy uptrends, sell downtrends)
- ✅ Dip buying (buy pullbacks in uptrends)
- ✅ Mean reversion (buy oversold, sell overbought)
- ✅ Risk management (confidence threshold, position sizing)

---

## Buy Signals

### 1. **Strong Uptrend Buy** (0.75 confidence)
- **Condition:** SMA20 > SMA50 AND Price > SMA20
- **What it means:** Confirmed uptrend with strong momentum
- **Example:** BTC at $65k, SMA20 at $64.5k, SMA50 at $63k
- **Risk:** Low - buying strength in established trend

### 2. **Dip Buy in Uptrend** (0.70 confidence)
- **Condition:** SMA20 > SMA50 AND Price is 0-3% below SMA20
- **What it means:** Minor pullback in uptrend - good entry
- **Example:** BTC at $63.5k, SMA20 at $64.5k, SMA50 at $63k
- **Risk:** Medium - buying dips, trend could reverse

### 3. **Oversold Buy** (0.80 confidence)
- **Condition:** RSI < 30 (regardless of trend)
- **What it means:** Price oversold, likely to bounce
- **Example:** BTC drops fast, RSI at 25
- **Risk:** Medium - could be start of downtrend

### 4. **Lower Bollinger Band Buy** (0.75 confidence)
- **Condition:** Price touches or goes below lower BB
- **What it means:** Price extended below average, mean reversion opportunity
- **Example:** BTC at $60k, BB_Lower at $60.5k
- **Risk:** Medium - extreme moves can continue

---

## Sell Signals

### 1. **Downtrend Sell** (0.70 confidence)
- **Condition:** SMA20 < SMA50 AND Price < SMA20
- **What it means:** Confirmed downtrend, exit positions
- **Example:** BTC at $61k, SMA20 at $62k, SMA50 at $63k
- **Risk:** Low - selling confirmed weakness

### 2. **Overbought Sell** (0.80 confidence)
- **Condition:** RSI > 70
- **What it means:** Price overbought, likely to pull back
- **Example:** BTC rallies fast, RSI at 75
- **Risk:** Medium - uptrends can stay overbought

### 3. **Upper Bollinger Band Sell** (0.75 confidence)
- **Condition:** Price touches or goes above upper BB
- **What it means:** Price extended above average
- **Example:** BTC at $68k, BB_Upper at $67.5k
- **Risk:** Medium - breakouts can continue

---

## Hold Signals

The AI says HOLD when:
- Confidence < 70% (below your minimum threshold)
- Price more than 3% below SMA20 in uptrend (trend might be reversing)
- Price above SMA20 but SMAs show downtrend (wait for clarity)
- RSI between 30-70 and no other strong signals
- Sideways/choppy market

---

## Signal Aggregation

The AI looks at **multiple indicators** and combines them:

**Example 1: Strong Buy**
- RSI: 28 (oversold) → BUY @0.80
- SMA: Uptrend, price above SMA20 → BUY @0.75
- BB: Price at lower band → BUY @0.75
- **Final:** BUY with 77% confidence (average: 0.77)

**Example 2: Moderate Buy**
- RSI: 45 (neutral) → HOLD @0.50
- SMA: Uptrend, price 2% below SMA20 → BUY @0.70
- BB: In range → no signal
- **Final:** BUY with 60% confidence (average: 0.60)
- **But:** 60% < 70% threshold → **HOLD** (safety gate)

**Example 3: Conflicting Signals**
- RSI: 72 (overbought) → SELL @0.80
- SMA: Strong uptrend → BUY @0.75
- BB: In range → no signal
- **Final:** Count BUY=1, SELL=1 → **HOLD** (tie)

---

## Risk Management

### Confidence Threshold (Default: 70%)
- Only executes trades with ≥70% confidence
- Prevents low-quality signals
- Can be adjusted in Settings (conservative: 80%, aggressive: 60%)

### Position Sizing
- Conservative: 50% of max position
- Moderate: 75% of max position
- Aggressive: 100% of max position

### Max Daily Loss
- Default: 5% of budget
- Bot stops trading if daily loss hits limit
- Resets at midnight UTC

---

## What Changed from Previous Version

### OLD (Conservative):
- ❌ Only bought when price > SMA20 in uptrend
- ❌ Missed dip-buying opportunities
- ❌ Required price above moving average (late entries)

### NEW (Balanced):
- ✅ Buys dips up to 3% below SMA20 in uptrend
- ✅ Better entry prices
- ✅ More trading opportunities
- ✅ Still protects from catching falling knives (won't buy >3% dips)
- ✅ Still avoids buying in downtrends

---

## Scenarios Explained

### Scenario 1: Price Dips in Uptrend
```
Market: BTC uptrend
- SMA50: $63,000 (long-term average)
- SMA20: $64,500 (short-term average, above SMA50 = uptrend)
- Current: $63,500 (dips below SMA20)

OLD AI: HOLD (waits for price to go back above $64,500)
NEW AI: BUY @70% confidence (buys the dip, only 1.5% below SMA20)

Why it works: In uptrends, dips often bounce back. Getting better entry.
```

### Scenario 2: Price Crashes Hard
```
Market: BTC starts dropping
- SMA50: $63,000
- SMA20: $64,500
- Current: $62,000 (drops 3.9% below SMA20)

OLD AI: HOLD
NEW AI: HOLD (>3% dip = possible trend reversal, wait)

Why it works: Protects from catching falling knives.
```

### Scenario 3: Downtrend
```
Market: BTC downtrend
- SMA50: $65,000
- SMA20: $63,000 (below SMA50 = downtrend)
- Current: $62,000

OLD AI: SELL
NEW AI: SELL (same)

Why it works: Never fights the trend. Both avoid buying in downtrends.
```

---

## Testing & Monitoring

### Paper Trading First
1. Enable Paper Trading in Settings
2. Run Gods Hand for 1-7 days
3. Monitor performance in Logs
4. Check win rate and PnL
5. Adjust confidence threshold if needed

### Check the Logs
Look at "AI Thinking" logs to see:
- Signal breakdown (which indicators fired)
- Confidence calculation (how it was computed)
- Final decision (buy/sell/hold and why)

### Performance Metrics
- Win Rate: Aim for >50%
- Average Profit: Should be > Average Loss
- Net PnL: Positive over time
- Sharpe Ratio: Risk-adjusted returns

---

## Recommended Settings

### Conservative (Lower risk, fewer trades)
- Risk Level: Conservative
- Min Confidence: 80%
- Position Size: 50%
- Max Daily Loss: 3%

### Balanced (Recommended)
- Risk Level: Moderate
- Min Confidence: 70%
- Position Size: 75%
- Max Daily Loss: 5%

### Aggressive (Higher risk, more trades)
- Risk Level: Aggressive
- Min Confidence: 60%
- Position Size: 100%
- Max Daily Loss: 7%

---

## Important Notes

⚠️ **Always use Paper Trading first** to test the strategy
⚠️ **Start with small positions** when going live
⚠️ **Monitor daily** - check logs and performance
⚠️ **Markets change** - what works today may not work tomorrow
⚠️ **Set stop losses** - use Max Daily Loss protection
⚠️ **Diversify** - don't put all your money in one trade

---

## Questions?

Check the logs for detailed signal breakdowns. The AI will show you:
- What each indicator said (RSI, SMA, BB)
- What confidence each gave (0.5 - 0.8)
- How the final decision was made
- Why trades were or weren't executed

**Remember:** No trading strategy is perfect. Always trade responsibly and only with money you can afford to lose.
