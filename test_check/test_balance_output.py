import os, sys, asyncio
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
from app.db import SessionLocal
from app.main import init_db
from app.market import get_account_balance

async def main():
    init_db()
    with SessionLocal() as db:
        data = await get_account_balance(db, 1, 'USD')
        print('paper_trading:', data.get('paper_trading'))
        print('total_balance:', data.get('total_balance'))
        for a in data.get('assets', []):
            print(a['asset'], a['free'], a['usd_value'])

if __name__ == '__main__':
    asyncio.run(main())
