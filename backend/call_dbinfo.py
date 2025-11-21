import requests, json
BASE='http://localhost:8000'
creds={'username':'Admin','password':'K@nph0ng69'}

r = requests.post(f'{BASE}/api/auth/login', json=creds)
print('login', r.status_code)
if r.status_code!=200:
    print(r.text)
    raise SystemExit(1)

token=r.json().get('access_token')
headers={'Authorization':f'Bearer {token}'}

r = requests.get(f'{BASE}/api/debug/dbinfo', headers=headers)
print('dbinfo status', r.status_code)
try:
    print(json.dumps(r.json(), indent=2))
except Exception:
    print(r.text)
