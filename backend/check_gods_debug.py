import requests, json, os

BASE = 'http://localhost:8000'
creds = {'username': 'Admin', 'password': 'K@nph0ng69'}

print('Logging in...')
r = requests.post(f'{BASE}/api/auth/login', json=creds, timeout=5)
print('Login status:', r.status_code)
if r.status_code != 200:
    print('Login failed:', r.text)
    raise SystemExit(1)

token = r.json().get('access_token')
headers = {'Authorization': f'Bearer {token}'}

print('\nCalling /api/bot/gods-hand/debug')
r2 = requests.get(f'{BASE}/api/bot/gods-hand/debug', headers=headers, timeout=10)
print('Status:', r2.status_code)
try:
    print(json.dumps(r2.json(), indent=2))
except Exception:
    print(r2.text)

print('\nDone')
