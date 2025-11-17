"""
Test price fetching
"""
import asyncio
from app.market import get_current_price

async def test_price():
    try:
        ticker = await get_current_price("BTC/USDT")
        print(f"✅ Price fetch successful:")
        print(f"   Last: {ticker['last']}")
        print(f"   Bid: {ticker['bid']}")
        print(f"   Ask: {ticker['ask']}")
    except Exception as e:
        print(f"❌ Price fetch failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_price())
