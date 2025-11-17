"""Test balance with budget 24343"""
import asyncio
from app.db import SessionLocal
from app.market import get_account_balance

async def test():
    db = SessionLocal()
    try:
        balance = await get_account_balance(db, user_id=1, fiat_currency="USD")
        
        print("\n" + "="*60)
        print(f"BALANCE TEST - Budget: 24343")
        print("="*60)
        print(f"Total: ${balance['total_balance']:,.2f}")
        print(f"Paper Trading: {balance.get('paper_trading', False)}")
        print(f"\nAssets:")
        for asset in balance.get('assets', []):
            print(f"  {asset['asset']}: {asset['total']:,.8f} (${asset['usd_value']:,.2f})")
    finally:
        db.close()

asyncio.run(test())
