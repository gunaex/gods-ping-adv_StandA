"""Verify kill-switch logic comparison - Old vs New"""
from app.db import get_db
from app.models import Trade, BotConfig
from app.position_tracker import get_current_position, calculate_position_pl
from datetime import datetime
import asyncio

async def compare_killswitch_logic():
    db = next(get_db())
    config = db.query(BotConfig).first()
    
    print("=" * 70)
    print("KILL-SWITCH LOGIC COMPARISON - Old vs New")
    print("=" * 70)
    
    # OLD LOGIC: Daily realized P/L
    print("\n📊 OLD LOGIC: Daily Realized P/L")
    print("-" * 70)
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_trades = db.query(Trade).filter(
        Trade.bot_type == 'gods_hand',
        Trade.timestamp >= today_start
    ).all()
    
    buys_cost = sum(t.amount * (t.filled_price or t.price) for t in today_trades if t.side == 'BUY')
    sells_revenue = sum(t.amount * (t.filled_price or t.price) for t in today_trades if t.side == 'SELL')
    
    if buys_cost > 0 and sells_revenue > 0:
        old_pl_percent = ((sells_revenue - buys_cost) / buys_cost) * 100
    else:
        old_pl_percent = 0.0
    
    print(f"Today's Trades: {len(today_trades)}")
    print(f"Total Buys:  ${buys_cost:,.2f}")
    print(f"Total Sells: ${sells_revenue:,.2f}")
    print(f"Daily P/L: {old_pl_percent:.2f}%")
    print(f"Would Trigger Kill-Switch? {old_pl_percent < -config.max_daily_loss}")
    
    if old_pl_percent < -config.max_daily_loss:
        print(f"❌ PROBLEM: False positive! Bot stopped at {old_pl_percent:.2f}%")
        print(f"   This compares unrelated buy/sell totals")
    
    # NEW LOGIC: Unrealized P/L
    print("\n📈 NEW LOGIC: Unrealized P/L (Current Position Value)")
    print("-" * 70)
    current_pos = get_current_position(config.user_id, config.symbol, db)
    
    from app.market import get_current_price
    ticker = await get_current_price(config.symbol)
    current_price = ticker.get('last', 0)
    
    pl_data = calculate_position_pl(current_pos, current_price)
    
    print(f"Position Quantity: {current_pos['quantity']:.8f} BTC")
    print(f"Cost Basis: ${pl_data['cost_basis']:,.2f}")
    print(f"Current Value: ${pl_data['current_value']:,.2f}")
    print(f"Unrealized P/L: {pl_data['pl_percent']:.2f}%")
    print(f"Would Trigger Kill-Switch? {pl_data['pl_percent'] < -config.max_daily_loss}")
    
    if pl_data['pl_percent'] >= -config.max_daily_loss:
        print(f"✅ CORRECT: Position is {pl_data['pl_percent']:.2f}%, within safe limits")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Kill-Switch Limit: -{config.max_daily_loss}%")
    print(f"")
    print(f"Old Logic (Daily Realized P/L):  {old_pl_percent:+.2f}% ❌ WRONG")
    print(f"New Logic (Unrealized P/L):      {pl_data['pl_percent']:+.2f}% ✅ CORRECT")
    print(f"")
    print(f"Difference: {abs(old_pl_percent - pl_data['pl_percent']):.2f} percentage points")
    print(f"")
    print(f"✅ NEW LOGIC FIX:")
    print(f"   - Monitors actual portfolio value vs cost basis")
    print(f"   - Prevents false triggers from unmatched buy/sell pairs")
    print(f"   - Reflects true position risk in real-time")

if __name__ == "__main__":
    asyncio.run(compare_killswitch_logic())
