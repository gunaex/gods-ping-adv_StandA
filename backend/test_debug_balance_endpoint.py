from fastapi.testclient import TestClient
from app import main

client = TestClient(main.app)

ADMIN_CREDS = {"username": "Admin", "password": "K@nph0ng69"}


def test_debug_balance():
    # Login to get token
    r = client.post('/api/auth/login', json=ADMIN_CREDS)
    assert r.status_code == 200, f"Login failed: {r.text}"
    token = r.json().get('access_token')
    assert token, 'No token returned'

    headers = {'Authorization': f'Bearer {token}'}

    r = client.get('/api/debug/balance', headers=headers)
    print('\nDEBUG BALANCE RESPONSE:\n', r.status_code, r.text)
    assert r.status_code == 200, f"Debug endpoint failed: {r.text}"


if __name__ == '__main__':
    test_debug_balance()
    print('Done')
