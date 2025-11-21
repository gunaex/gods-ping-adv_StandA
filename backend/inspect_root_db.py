import sqlite3
from pathlib import Path
p = Path('..').resolve() / 'gods_ping.db'
print('Root DB path:', p)
conn = sqlite3.connect(str(p))
conn.row_factory = sqlite3.Row
c = conn.cursor()

print('\nBot configs:')
try:
    c.execute('SELECT * FROM bot_configs')
    for r in c.fetchall():
        print(dict(r))
except Exception as e:
    print('err bot_configs', e)

print('\nTrades:')
try:
    c.execute("SELECT * FROM trades WHERE bot_type='gods_hand'")
    rows = c.fetchall()
    print('count', len(rows))
    for r in rows:
        print(dict(r))
except Exception as e:
    print('err trades', e)

conn.close()
