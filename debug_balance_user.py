#!/usr/bin/env python3
"""
Test the balance API and debug what user ID it's actually using
"""
import requests
import json

def debug_balance_api_user():
    print("="*80)
    print("DEBUGGING BALANCE API USER AND DATABASE CONNECTION")
    print("="*80)
    
    base_url = "http://localhost:8000/api"
    
    # Login and get token
    admin_creds = {"username": "Admin", "password": "K@nph0ng69"}
    
    try:
        print("1. Logging in...")
        response = requests.post(f"{base_url}/auth/login", json=admin_creds)
        
        if response.status_code != 200:
            print(f"   ❌ Login failed: {response.text}")
            return
            
        data = response.json()
        token = data.get('access_token')
        print(f"   ✅ Login successful")
        
        print(f"\n2. Checking who the current user is...")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get current user info
        me_response = requests.get(f"{base_url}/auth/me", headers=headers)
        if me_response.status_code == 200:
            user_data = me_response.json()
            print(f"   Current user: {json.dumps(user_data, indent=2)}")
            user_id = user_data.get('id')
            print(f"   User ID: {user_id}")
        else:
            print(f"   ❌ Failed to get current user: {me_response.text}")
            return
        
        print(f"\n3. Calling balance API and checking response...")
        balance_response = requests.get(f"{base_url}/account/balance?fiat_currency=USD", headers=headers)
        
        if balance_response.status_code == 200:
            balance_data = balance_response.json()
            print(f"   Balance API response:")
            print(f"   {json.dumps(balance_data, indent=2)}")
            
            # Check if it's using paper trading
            is_paper = balance_data.get('paper_trading', False)
            print(f"\n   Paper trading mode: {is_paper}")
            
            if is_paper:
                btc_asset = None
                for asset in balance_data.get('assets', []):
                    if asset['asset'] == 'BTC':
                        btc_asset = asset
                        break
                
                if btc_asset:
                    btc_amount = btc_asset['free']
                    btc_value = btc_asset['usd_value']
                    
                    if btc_amount == 0:
                        print(f"   ❌ BTC amount is 0 - this is the problem!")
                        print(f"   Expected: ~0.339 BTC worth $14,240")
                        print(f"   Actual: {btc_amount} BTC worth ${btc_value}")
                    else:
                        print(f"   ✅ BTC amount is correct: {btc_amount} BTC worth ${btc_value}")
        else:
            print(f"   ❌ Balance API failed: {balance_response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print(f"\n4. Possible causes of the discrepancy:")
    causes = [
        "Database connection issue in the API",
        "Wrong user ID being used in balance calculation", 
        "Paper trading calculation not working in API context",
        "Exception being caught and returning default values",
        "Different database file being used by API vs debug script"
    ]
    
    for i, cause in enumerate(causes, 1):
        print(f"   {i}. {cause}")

if __name__ == "__main__":
    debug_balance_api_user()