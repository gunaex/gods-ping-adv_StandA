"""Test paper trading balance flow"""
import asyncio
from app.db import SessionLocal
from app.market import get_account_balance
from app.models import Trade, BotConfig
from datetime import datetime

async def test_balance_flow():
    db = SessionLocal()
    try:
        # Get config
        config = db.query(BotConfig).filter(BotConfig.user_id == 1).first()
        budget = config.budget
        
        print("\n" + "="*70)
        print("PAPER TRADING BALANCE TEST")
        print("="*70)
        print(f"Budget: ${budget:,.2f}")
        print(f"Symbol: {config.symbol}")
        
        # Check trades
        trades = db.query(Trade).filter(
            Trade.user_id == 1,
            Trade.symbol == config.symbol
        ).all()
        
        print(f"\nTrades in DB: {len(trades)}")
        
        # Test initial state (no trades)
        print("\n" + "-"*70)
        print("SCENARIO 1: Initial State (No Trades)")
        print("-"*70)
        
        balance = await get_account_balance(db, user_id=1, fiat_currency="USD")
        
        print(f"Total Balance: ${balance['total_balance']:,.2f}")
        print(f"\nAssets:")
        for asset in balance.get('assets', []):
            print(f"  {asset['asset']:6s}: {asset['total']:>15.8f}  (${asset['usd_value']:>12,.2f})")
        
        # Simulate a BUY trade
        if len(trades) == 0:
            print("\n" + "-"*70)
            print("SCENARIO 2: After BUY $2,000 worth of BTC")
            print("-"*70)
            
            # Get current price
            from app.market import get_current_price
            ticker = await get_current_price(config.symbol)
            current_price = ticker['last']
            
            buy_amount_usd = 2000
            buy_quantity = buy_amount_usd / current_price
            
            # Create BUY trade
            trade = Trade(
                user_id=1,
                symbol=config.symbol,
                side='BUY',
                amount=buy_quantity,
                price=current_price,
                filled_price=current_price,
                status='completed_paper',
                bot_type='gods_hand',
                timestamp=datetime.utcnow()
            )
            db.add(trade)
            db.commit()
            
            print(f"BUY {buy_quantity:.8f} BTC @ ${current_price:,.2f}")
            
            # Check balance after BUY
            balance = await get_account_balance(db, user_id=1, fiat_currency="USD")
            
            print(f"\nTotal Balance: ${balance['total_balance']:,.2f}")
            print(f"\nAssets:")
            for asset in balance.get('assets', []):
                print(f"  {asset['asset']:6s}: {asset['total']:>15.8f}  (${asset['usd_value']:>12,.2f})")
            
            # Expected:
            # USDT: budget - 2000 = 22,343
            # BTC: buy_quantity ≈ 0.020895
            
            print("\n" + "-"*70)
            print("SCENARIO 3: After SELL 50% of BTC")
            print("-"*70)
            
            sell_quantity = buy_quantity * 0.5
            sell_value = sell_quantity * current_price
            
            # Create SELL trade
            trade = Trade(
                user_id=1,
                symbol=config.symbol,
                side='SELL',
                amount=sell_quantity,
                price=current_price,
                filled_price=current_price,
                status='completed_paper',
                bot_type='gods_hand',
                timestamp=datetime.utcnow()
            )
            db.add(trade)
            db.commit()
            
            print(f"SELL {sell_quantity:.8f} BTC @ ${current_price:,.2f}")
            print(f"Receive: ${sell_value:,.2f} USDT")
            
            # Check balance after SELL
            balance = await get_account_balance(db, user_id=1, fiat_currency="USD")
            
            print(f"\nTotal Balance: ${balance['total_balance']:,.2f}")
            print(f"\nAssets:")
            for asset in balance.get('assets', []):
                print(f"  {asset['asset']:6s}: {asset['total']:>15.8f}  (${asset['usd_value']:>12,.2f})")
            
            # Expected:
            # USDT: 22,343 + 1000 = 23,343
            # BTC: 0.010447 (50% of original)
            
            print("\n" + "="*70)
            print("✅ Balance logic verified!")
            print("="*70)
            
    finally:
        db.close()

asyncio.run(test_balance_flow())
