import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent / 'gods_ping.db'
print('DB path:', db_path)
conn = sqlite3.connect(str(db_path))
conn.row_factory = sqlite3.Row
c = conn.cursor()

print('\nbot_configs:')
try:
    c.execute('SELECT * FROM bot_configs')
    rows = c.fetchall()
    print('count', len(rows))
    for r in rows:
        d = dict(r)
        # mask secrets
        if 'gmail_app_password' in d:
            d['gmail_app_password'] = '***' if d['gmail_app_password'] else None
        print(d)
except Exception as e:
    print('err bot_configs', e)

print('\ntrades (last 10):')
try:
    c.execute("SELECT * FROM trades WHERE bot_type='gods_hand' ORDER BY timestamp DESC LIMIT 10")
    rows = c.fetchall()
    print('count', len(rows))
    for r in rows:
        print(dict(r))
except Exception as e:
    print('err trades', e)

print('\npaper_trading_snapshots (last 10):')
try:
    c.execute("SELECT * FROM paper_trading_snapshots WHERE bot_type='gods_hand' ORDER BY timestamp DESC LIMIT 10")
    rows = c.fetchall()
    print('count', len(rows))
    for r in rows:
        d=dict(r)
        d_short={k:d[k] for k in ('id','timestamp','starting_balance','current_balance','quantity_held','total_trades') if k in d}
        print(d_short)
except Exception as e:
    print('err snapshots', e)

conn.close()
