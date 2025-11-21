import sqlite3, json

conn = sqlite3.connect('gods_ping.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print('Trades:')
try:
    cur.execute("SELECT * FROM trades WHERE bot_type='gods_hand' ORDER BY timestamp DESC")
    rows = cur.fetchall()
    print('count', len(rows))
    for r in rows:
        print(dict(r))
except Exception as e:
    print('trades err', e)

print('\nPaper trading snapshots:')
try:
    cur.execute("SELECT * FROM paper_trading_snapshots WHERE bot_type='gods_hand' ORDER BY timestamp DESC")
    rows = cur.fetchall()
    print('count', len(rows))
    for r in rows:
        d=dict(r)
        # shorten
        d['data_preview']= {k:d[k] for k in ('starting_balance','current_balance','quantity_held','total_trades') if k in d}
        print(d)
except Exception as e:
    print('snapshots err', e)

conn.close()
