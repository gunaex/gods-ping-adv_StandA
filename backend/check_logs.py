"""Check latest Gods Hand logs"""
from app.db import SessionLocal
from app.logging_models import Log
from app.models import Trade

db = SessionLocal()
try:
    # Get latest logs
    logs = db.query(Log).filter(
        Log.bot_type == 'gods_hand'
    ).order_by(Log.timestamp.desc()).limit(5).all()
    
    print("\n" + "="*70)
    print("LATEST GODS HAND LOGS")
    print("="*70)
    
    for log in logs:
        print(f"\n📅 {log.timestamp}")
        print(f"📊 {log.category} - {log.level}")
        print(f"💬 {log.message}")
        if log.details:
            print(f"📝 Details:")
            import json
            try:
                details = json.loads(log.details)
                for key, value in list(details.items())[:10]:
                    if isinstance(value, dict):
                        print(f"   {key}: {list(value.keys())}")
                    else:
                        print(f"   {key}: {value}")
            except:
                print(f"   {log.details[:300]}")
        print("-"*70)
    
    # Check trades
    trades = db.query(Trade).filter(
        Trade.user_id == 1,
        Trade.symbol == 'BTC/USDT'
    ).order_by(Trade.timestamp.desc()).limit(3).all()
    
    print(f"\n📈 Total BTC/USDT Trades: {len(db.query(Trade).filter(Trade.user_id == 1, Trade.symbol == 'BTC/USDT').all())}")
    
    if trades:
        print("\nLatest Trades:")
        for t in trades:
            print(f"  {t.timestamp} - {t.side} {t.amount:.8f} @ ${t.price:.2f} [{t.status}]")
    
finally:
    db.close()
