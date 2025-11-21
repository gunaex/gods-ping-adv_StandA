import requests, json

LOGIN_URL = 'http://127.0.0.1:8000/api/auth/login'
BALANCE_URL = 'http://127.0.0.1:8000/api/account/balance?fiat_currency=USD'

try:
    login = requests.post(LOGIN_URL, json={"username":"Admin","password":"K@nph0ng69"}, timeout=5)
    if login.status_code != 200:
        print('Login failed', login.status_code, login.text)
    else:
        token = login.json().get('access_token')
        headers = {'Authorization': f'Bearer {token}'}
        r = requests.get(BALANCE_URL, headers=headers, timeout=5)
        print('STATUS', r.status_code)
        try:
            print(json.dumps(r.json(), indent=2))
        except Exception:
            print(r.text)
except Exception as e:
    print('Request failed:', e)
