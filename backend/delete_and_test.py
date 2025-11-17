"""Delete all trades and test position immediately"""
from app.db import SessionLocal
from app.models import Trade
from app.position_tracker import get_current_position

db = SessionLocal()
try:
    # Delete ALL trades
    deleted = db.query(Trade).filter(Trade.user_id == 1).delete()
    db.commit()
    print(f"✅ Deleted {deleted} trades")
    
    # Test position immediately
    pos = get_current_position(1, 'BTC/USDT', db)
    
    print(f"\n📊 Position after deletion:")
    print(f"   Quantity: {pos['quantity']:.8f}")
    print(f"   Cost basis: ${pos['cost_basis']:.2f}")
    print(f"   Paper initial flag: {pos.get('_paper_initial', False)}")
    print(f"   Budget: ${pos.get('_budget', 0):.2f}")
    
finally:
    db.close()