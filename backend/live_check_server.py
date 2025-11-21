import requests, os, sys

BASE='http://localhost:8000'

print('Environment:')
print('DATABASE_URL=', os.environ.get('DATABASE_URL'))
print('PYTHONEXE=', sys.executable)
print('CWD=', os.getcwd())
print('\n1) GET /api/debug/balance (no auth)')
try:
    r = requests.get(f'{BASE}/api/debug/balance')
    print('Status', r.status_code)
    print(r.text)
except Exception as e:
    print('Error:', e)

print('\n2) Attempt login and GET /api/debug/balance with token')
creds={'username':'Admin','password':'K@nph0ng69'}
try:
    r = requests.post(f'{BASE}/api/auth/login', json=creds, timeout=5)
    print('Login status', r.status_code)
    print(r.text)
    if r.status_code==200:
        token=r.json().get('access_token')
        headers={'Authorization':f'Bearer {token}'}
        r2 = requests.get(f'{BASE}/api/debug/balance', headers=headers, timeout=5)
        print('Debug balance (auth) status', r2.status_code)
        print(r2.text)
        r3 = requests.get(f'{BASE}/api/account/balance', headers=headers, timeout=5)
        print('Account balance status', r3.status_code)
        print(r3.text)
except Exception as e:
    print('Error during auth/checks:', e)

print('\n3) GET / (root)')
try:
    r = requests.get(BASE+'/', timeout=5)
    print('Root status', r.status_code)
    print(r.text[:500])
except Exception as e:
    print('Root error', e)

print('\nDone')
