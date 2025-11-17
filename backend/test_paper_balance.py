"""
Test paper trading balance calculation
"""
import asyncio
from app.db import SessionLocal
from app.market import get_account_balance

async def test_balance():
    db = SessionLocal()
    try:
        # User ID 1
        balance = await get_account_balance(db, user_id=1, fiat_currency="USD")
        
        print("\n" + "="*60)
        print("PAPER TRADING BALANCE TEST")
        print("="*60)
        print(f"\nTotal Balance: ${balance['total_balance']:,.2f}")
        print(f"Available: ${balance['available_balance']:,.2f}")
        print(f"Paper Trading: {balance.get('paper_trading', False)}")
        print(f"\nAssets ({len(balance.get('assets', []))} total):")
        print("-"*60)
        
        for asset in balance.get('assets', []):
            print(f"\n{asset['asset']}:")
            print(f"  Free: {asset['free']:,.8f}")
            print(f"  Locked: {asset['locked']:,.8f}")
            print(f"  Total: {asset['total']:,.8f}")
            print(f"  USD Value: ${asset['usd_value']:,.2f}")
        
        print("\n" + "="*60)
        
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_balance())
