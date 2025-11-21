import shutil, sqlite3, datetime, json, requests
from pathlib import Path

DB = Path(__file__).resolve().parent / 'gods_ping.db'
BACKUP = DB.with_suffix('.db.bak.' + datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ'))

print('DB path:', DB)
print('Backup to:', BACKUP)
shutil.copy2(str(DB), str(BACKUP))
print('Backup created')

conn = sqlite3.connect(str(DB))
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Show counts before
for t in ('trades','paper_trading_snapshots'):
    try:
        r = c.execute(f'SELECT COUNT(*) as c FROM {t}').fetchone()
        print(f'{t} count before:', r['c'])
    except Exception as e:
        print('err', t, e)

# Show the specific trade and snapshot
print('\nSpecific trade(s) matching gods_hand:')
trades = c.execute("SELECT * FROM trades WHERE bot_type='gods_hand' ORDER BY timestamp DESC").fetchall()
for t in trades:
    print(dict(t))

snapshots = c.execute("SELECT * FROM paper_trading_snapshots WHERE bot_type='gods_hand' ORDER BY timestamp DESC").fetchall()
for s in snapshots:
    print(dict(s))

# Delete the trade(s) and snapshot(s) - targeted deletion
# WARNING: irreversible (we have backup)
print('\nDeleting found trades and snapshots...')
try:
    c.execute("DELETE FROM trades WHERE bot_type='gods_hand'")
    c.execute("DELETE FROM paper_trading_snapshots WHERE bot_type='gods_hand'")
    conn.commit()
    print('Deleted trades and snapshots for gods_hand')
except Exception as e:
    print('delete error', e)

# Show counts after
for t in ('trades','paper_trading_snapshots'):
    try:
        r = c.execute(f'SELECT COUNT(*) as c FROM {t}').fetchone()
        print(f'{t} count after:', r['c'])
    except Exception as e:
        print('err', t, e)

conn.close()

# Check balance endpoints on running server
BASE='http://localhost:8000'
creds={'username':'Admin','password':'K@nph0ng69'}
print('\nLogging into running server...')
r = requests.post(f'{BASE}/api/auth/login', json=creds)
print('login', r.status_code)
if r.status_code==200:
    token=r.json().get('access_token')
    headers={'Authorization':f'Bearer {token}'}
    r2 = requests.get(f'{BASE}/api/debug/balance', headers=headers)
    print('\n/api/debug/balance:', r2.status_code)
    try:
        print(json.dumps(r2.json(), indent=2))
    except Exception:
        print(r2.text)
    r3 = requests.get(f'{BASE}/api/account/balance', headers=headers)
    print('\n/api/account/balance:', r3.status_code)
    try:
        print(json.dumps(r3.json(), indent=2))
    except Exception:
        print(r3.text)
else:
    print('login failed', r.text)
print('\nDone')
