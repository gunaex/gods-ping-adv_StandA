import requests
import json
import time
import websocket
import threading

BASE = 'http://127.0.0.1:8000'
WS_BASE = 'ws://127.0.0.1:8000'

# Test credentials
creds = {'username': 'Admin', 'password': 'ChangeMe123!'}

def on_message(ws, message):
    """Callback for WebSocket messages"""
    try:
        log_data = json.loads(message)
        print(f"[WS LOG] {log_data['timestamp']} [{log_data['level']}] {log_data['source']}: {log_data['message']}")
        if log_data.get('details'):
            print(f"         Details: {log_data['details']}")
    except Exception as e:
        print(f"[WS ERROR] {e}: {message}")

def on_error(ws, error):
    print(f"[WS ERROR] {error}")

def on_close(ws, close_status_code, close_msg):
    print("[WS] Connection closed")

def on_open(ws):
    print("[WS] Connection opened - listening for logs...")

def listen_to_logs(token):
    """Start WebSocket listener in a separate thread"""
    ws_url = f"{WS_BASE}/ws/logs/{token}"
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    
    # Run in a separate thread
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()
    return ws

print("=" * 60)
print("TESTING MULTI-USER BOT SYSTEM")
print("=" * 60)

# Step 1: Login
print("\n[1] Logging in...")
r = requests.post(f'{BASE}/api/auth/login', json=creds)
print(f'    Status: {r.status_code}')
if r.status_code != 200:
    print(f'    Error: {r.text}')
    raise SystemExit(1)

token = r.json().get('access_token')
headers = {'Authorization': f'Bearer {token}'}
print(f'    Token obtained: {token[:20]}...')

# Step 2: Start WebSocket listener
print("\n[2] Starting WebSocket listener...")
ws = listen_to_logs(token)
time.sleep(1)  # Give it time to connect

# Step 3: Get database info
print("\n[3] Fetching database info...")
r = requests.get(f'{BASE}/api/debug/dbinfo', headers=headers)
print(f'    Status: {r.status_code}')
try:
    db_info = r.json()
    print(json.dumps(db_info, indent=2))
except Exception:
    print(f'    Raw response: {r.text}')

# Step 4: Check bot status
print("\n[4] Checking Gods Hand bot status...")
r = requests.get(f'{BASE}/api/bot/gods-hand/status', headers=headers)
print(f'    Status: {r.status_code}')
if r.status_code == 200:
    status = r.json()
    print(f'    Bot Status: {status.get("status", "unknown")}')
else:
    print(f'    Error: {r.text}')

# Step 5: Get bot config
print("\n[5] Fetching bot configuration...")
r = requests.get(f'{BASE}/api/settings/bot-config', headers=headers)
print(f'    Status: {r.status_code}')
if r.status_code == 200:
    config = r.json()
    print(f'    Config: {json.dumps(config, indent=2)}')
else:
    print(f'    Error: {r.text}')

# Step 6: Start the bot
print("\n[6] Starting Gods Hand bot...")
r = requests.post(f'{BASE}/api/bot/gods-hand/start', headers=headers)
print(f'    Status: {r.status_code}')
if r.status_code == 200:
    result = r.json()
    print(f'    Message: {result.get("message")}')
    print(f'    Status: {result.get("status")}')
else:
    print(f'    Error: {r.text}')

# Step 7: Wait and watch logs come in
print("\n[7] Monitoring bot activity for 15 seconds...")
print("    (Watch for real-time logs above)")
time.sleep(15)

# Step 8: Check status again
print("\n[8] Checking bot status after running...")
r = requests.get(f'{BASE}/api/bot/gods-hand/status', headers=headers)
if r.status_code == 200:
    status = r.json()
    print(f'    Bot Status: {status.get("status", "unknown")}')

# Step 9: Fetch logs from API
print("\n[9] Fetching last 10 logs from database...")
r = requests.get(f'{BASE}/api/logs?limit=10', headers=headers)
print(f'    Status: {r.status_code}')
if r.status_code == 200:
    resp = r.json()
    logs = resp.get('logs', [])
    print(f'    Total logs: {resp.get("total", 0)}')
    
    if isinstance(logs, list):
        for log in logs[:5]:
            source = log.get("category") or log.get("source") or "unknown"
            print(f'    - [{log.get("level")}] {source}: {log.get("message")}')
    else:
        print(f"    Unexpected logs format: {type(logs)}")
else:
    print(f'    Error: {r.text}')

# Step 10: Stop the bot
print("\n[10] Stopping Gods Hand bot...")
r = requests.post(f'{BASE}/api/bot/gods-hand/stop', headers=headers)
print(f'    Status: {r.status_code}')
if r.status_code == 200:
    result = r.json()
    print(f'    Message: {result.get("message")}')
else:
    print(f'    Error: {r.text}')

# Step 11: Wait for graceful shutdown
print("\n[11] Waiting for bot to stop gracefully...")
time.sleep(3)

# Step 12: Final status check
print("\n[12] Final status check...")
r = requests.get(f'{BASE}/api/bot/gods-hand/status', headers=headers)
if r.status_code == 200:
    status = r.json()
    print(f'    Bot Status: {status.get("status", "unknown")}')

# Close WebSocket
print("\n[13] Closing WebSocket connection...")
ws.close()

print("\n" + "=" * 60)
print("TEST COMPLETED")
print("=" * 60)
