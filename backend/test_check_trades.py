"""Check trades"""
from app.db import SessionLocal
from app.models import Trade

db = SessionLocal()
try:
    trades = db.query(Trade).filter(
        Trade.user_id == 1,
        Trade.symbol == 'BTC/USDT'
    ).all()
    
    print(f"\nTotal trades: {len(trades)}")
    
    if trades:
        print("\nLast 5 trades:")
        for t in trades[-5:]:
            print(f"  {t.timestamp} - {t.side} {t.amount:.8f} @ ${t.price:.2f} [{t.status}]")
    else:
        print("No trades found")
        
    # Check paper performance
    from app.paper_trading_tracker import calculate_paper_performance
    perf = calculate_paper_performance(1, 'BTC/USDT', 'gods_hand', db)
    print(f"\nPaper Performance:")
    print(f"  Total trades: {perf.get('total_trades', 0)}")
    print(f"  Quantity held: {perf.get('quantity_held', 0):.8f}")
    print(f"  Cash balance: ${perf.get('cash_balance', 0):.2f}")
    
finally:
    db.close()
