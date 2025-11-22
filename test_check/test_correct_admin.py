#!/usr/bin/env python3
"""
Test with correct admin credentials
"""
import requests
import json

def test_with_correct_admin():
    print("="*80)
    print("TESTING WITH CORRECT ADMIN CREDENTIALS")
    print("="*80)
    
    base_url = "http://localhost:8000/api"
    
    # Correct admin credentials from auth.py
    admin_creds = {
        "username": "Admin", 
        "password": "K@nph0ng69"
    }
    
    print(f"1. Logging in as: {admin_creds['username']}")
    
    try:
        response = requests.post(f"{base_url}/auth/login", json=admin_creds)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print(f"   ✅ Login successful! Token: {token[:20]}...")
            
            print(f"\n2. Testing authenticated balance API...")
            
            headers = {"Authorization": f"Bearer {token}"}
            balance_response = requests.get(f"{base_url}/account/balance?fiat_currency=USD", headers=headers)
            
            print(f"   Status: {balance_response.status_code}")
            
            if balance_response.status_code == 200:
                balance_data = balance_response.json()
                print("   ✅ Balance API successful!")
                
                # Check for BTC
                btc_found = False
                usdt_found = False
                
                if 'assets' in balance_data:
                    print(f"   Assets count: {len(balance_data['assets'])}")
                    
                    for asset in balance_data['assets']:
                        print(f"     - {asset['asset']}: {asset['free']} (${asset.get('usd_value', 0):.2f})")
                        
                        if asset['asset'] == 'BTC':
                            btc_found = True
                            if float(asset['free']) > 0:
                                print(f"     ✅ BTC balance is NOT zero: {asset['free']}")
                            else:
                                print(f"     ❌ BTC balance IS zero: {asset['free']}")
                        
                        if asset['asset'] == 'USDT':
                            usdt_found = True
                
                if not btc_found:
                    print("     ❌ BTC asset not found in response!")
                if not usdt_found:
                    print("     ❌ USDT asset not found in response!")
                
                print(f"\n   Full response:")
                print(f"   {json.dumps(balance_data, indent=2)}")
                
            else:
                print(f"   ❌ Balance API failed: {balance_response.text}")
        else:
            print(f"   ❌ Login failed: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print(f"\n3. Solution for frontend:")
    print("   The frontend needs to:")
    print("   1. Login with username: 'Admin' and password: 'K@nph0ng69'")
    print("   2. Store the token in localStorage")
    print("   3. Make balance API calls with the token")
    print("   4. If BTC shows 0 but backend returns correct value, check browser DevTools")

if __name__ == "__main__":
    test_with_correct_admin()