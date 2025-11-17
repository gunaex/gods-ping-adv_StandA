"""Manually test one Gods Hand cycle"""
import asyncio
from app.db import SessionLocal
from app.bots import gods_hand_once
from app.models import BotConfig

async def manual_gods_hand():
    db = SessionLocal()
    try:
        # Get config
        config = db.query(BotConfig).filter(BotConfig.user_id == 1).first()
        
        print("\n" + "="*70)
        print("MANUAL GODS HAND TEST")
        print("="*70)
        print(f"Config: {config.symbol}, Budget: ${config.budget:,.2f}")
        print(f"Paper Trading: {config.paper_trading}")
        print(f"Gods Mode: {config.gods_mode_enabled}")
        
        # Run one cycle
        print("\n🚀 Executing Gods Hand cycle...")
        result = await gods_hand_once(1, config, db)
        
        print(f"\n✅ Result:")
        print(f"   Status: {result.get('status', 'unknown')}")
        print(f"   Action: {result.get('action', 'unknown')}")
        print(f"   Reason: {result.get('reason', 'unknown')}")
        
        if 'crypto_amount' in result:
            print(f"   Crypto amount: {result['crypto_amount']:.8f}")
            print(f"   USD value: ${result.get('usd_value', 0):,.2f}")
            print(f"   Price: ${result.get('price', 0):,.2f}")
        
        # Check if trade was created
        from app.models import Trade
        trades = db.query(Trade).filter(
            Trade.user_id == 1,
            Trade.symbol == config.symbol
        ).all()
        
        print(f"\n📈 Trades in DB: {len(trades)}")
        if trades:
            latest = trades[-1]
            print(f"   Latest: {latest.side} {latest.amount:.8f} @ ${latest.price:.2f}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()

asyncio.run(manual_gods_hand())