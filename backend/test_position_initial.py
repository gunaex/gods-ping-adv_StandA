"""Test position tracker with initial balance"""
import asyncio
from app.db import SessionLocal
from app.position_tracker import get_current_position
from app.models import BotConfig

async def test():
    db = SessionLocal()
    try:
        # Get config
        config = db.query(BotConfig).filter(BotConfig.user_id == 1).first()
        
        # Get position (no trades)
        position = get_current_position(1, 'BTC/USDT', db)
        
        print("\n" + "="*60)
        print("POSITION TRACKER TEST (No Trades)")
        print("="*60)
        print(f"Symbol: {position['symbol']}")
        print(f"Quantity: {position['quantity']:.8f} BTC")
        print(f"Cost Basis: ${position['cost_basis']:,.2f}")
        print(f"Position Value: ${position['position_value_usd']:,.2f}")
        print(f"Trades Count: {position['trades_count']}")
        
        if position.get('_paper_initial'):
            print(f"\n⚠️  Paper Initial Flag: True")
            print(f"Budget: ${position.get('_budget', 0):,.2f}")
            
            # Simulate applying the initial position
            from app.market import get_current_price
            ticker = await get_current_price('BTC/USDT')
            current_price = ticker['last']
            
            budget = position['_budget']
            quantity = (budget / 2) / current_price
            
            print(f"\n✅ After applying 50/50 split:")
            print(f"Quantity: {quantity:.8f} BTC")
            print(f"Cost Basis: ${budget/2:,.2f}")
            print(f"Position Value: ${budget/2:,.2f}")
        
        print("\n" + "="*60)
        
    finally:
        db.close()

asyncio.run(test())
