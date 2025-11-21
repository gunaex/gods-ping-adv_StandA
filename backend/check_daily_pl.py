"""Check why Gods Hand stopped - analyze daily P/L"""
from app.db import get_db
from app.models import Trade
from datetime import datetime

db = next(get_db())

# Get today's trades
today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
trades = db.query(Trade).filter(
    Trade.bot_type == 'gods_hand',
    Trade.timestamp >= today_start
).order_by(Trade.timestamp).all()

print(f"\n=== Today's Trades (since {today_start}) ===")
print(f"Found {len(trades)} trades\n")

total_buy_cost = 0
total_sell_revenue = 0

for t in trades:
    price = t.filled_price or t.price
    cost = t.amount * price
    print(f"{t.timestamp} | {t.side:4s} | {t.amount:.8f} BTC @ ${price:,.2f} = ${cost:,.2f}")
    
    if t.side == 'BUY':
        total_buy_cost += cost
    else:
        total_sell_revenue += cost

print(f"\n--- Daily Summary ---")
print(f"Total Buys Cost: ${total_buy_cost:,.2f}")
print(f"Total Sells Revenue: ${total_sell_revenue:,.2f}")

if total_buy_cost > 0 and total_sell_revenue > 0:
    pl_percent = ((total_sell_revenue - total_buy_cost) / total_buy_cost) * 100
    print(f"Daily P/L: {pl_percent:.2f}%")
    print(f"\nKill-Switch Limit: -5.0%")
    print(f"KILL-SWITCH TRIGGERED: {pl_percent < -5.0}")
    
    if pl_percent < -5.0:
        print(f"\n⚠️  Gods Hand stopped because daily loss ({pl_percent:.2f}%) exceeded limit (-5.0%)")
else:
    print(f"Daily P/L: 0.0% (no realized P/L yet)")
    print(f"Note: Need both buys and sells to calculate realized P/L")
