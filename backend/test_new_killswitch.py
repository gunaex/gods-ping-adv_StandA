"""Test the new unrealized P/L kill-switch logic"""
from app.db import get_db
from app.models import BotConfig
from app.position_tracker import get_current_position, calculate_position_pl
import asyncio

async def test_killswitch():
    db = next(get_db())
    
    # Get config
    config = db.query(BotConfig).first()
    if not config:
        print("❌ No config found")
        return
    
    print(f"\n=== Kill-Switch Test ===")
    print(f"Symbol: {config.symbol}")
    print(f"Max Daily Loss Limit: {config.max_daily_loss}%")
    print(f"Paper Trading: {config.paper_trading}")
    
    # Get current position
    current_pos = get_current_position(config.user_id, config.symbol, db)
    
    print(f"\n=== Current Position ===")
    print(f"Quantity: {current_pos['quantity']:.8f} BTC")
    print(f"Cost Basis: ${current_pos['cost_basis']:,.2f}")
    print(f"Average Price: ${current_pos['average_price']:,.2f}")
    print(f"Total Fees Paid: ${current_pos['total_fees_paid']:,.2f}")
    print(f"Trades Count: {current_pos['trades_count']}")
    
    # Get current price
    from app.market import get_current_price
    ticker = await get_current_price(config.symbol)
    current_price = ticker.get('last', 0)
    
    print(f"\n=== Current Market ===")
    print(f"Current Price: ${current_price:,.2f}")
    
    # Calculate unrealized P/L
    pl_data = calculate_position_pl(current_pos, current_price)
    
    print(f"\n=== Unrealized P/L ===")
    print(f"Current Value: ${pl_data['current_value']:,.2f}")
    print(f"Cost Basis: ${pl_data['cost_basis']:,.2f}")
    print(f"P/L Amount: ${pl_data['pl_amount']:,.2f}")
    print(f"P/L Percent: {pl_data['pl_percent']:.2f}%")
    
    # Check kill-switch
    print(f"\n=== Kill-Switch Status ===")
    print(f"Max Loss Allowed: -{config.max_daily_loss}%")
    print(f"Current Unrealized P/L: {pl_data['pl_percent']:.2f}%")
    
    if pl_data['pl_percent'] < -config.max_daily_loss:
        print(f"🚨 KILL-SWITCH WOULD TRIGGER!")
        print(f"   Loss of {pl_data['pl_percent']:.2f}% exceeds limit of -{config.max_daily_loss}%")
    else:
        print(f"✅ Kill-switch OK - within safe limits")
        margin = config.max_daily_loss + pl_data['pl_percent']
        print(f"   Margin before trigger: {margin:.2f}%")
    
    # Show what would need to happen to trigger
    if current_pos['quantity'] > 0:
        trigger_price = current_pos['average_price'] * (1 - config.max_daily_loss/100)
        print(f"\n💡 Kill-switch would trigger if price drops to: ${trigger_price:,.2f}")
        print(f"   Current price: ${current_price:,.2f}")
        drop_needed = ((trigger_price - current_price) / current_price) * 100
        print(f"   Price needs to drop: {drop_needed:.2f}% from current level")

if __name__ == "__main__":
    asyncio.run(test_killswitch())
