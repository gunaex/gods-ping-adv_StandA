#!/usr/bin/env python3
"""
Test complete authentication and balance flow
"""
import requests
import json
import sys

def test_complete_auth_flow():
    print("="*80)
    print("TESTING COMPLETE AUTHENTICATION AND BALANCE FLOW")
    print("="*80)
    
    base_url = "http://localhost:8000/api"
    
    print("1. Testing authentication...")
    
    # Try to login with default credentials
    login_attempts = [
        {"username": "admin", "password": "admin123"},
        {"username": "admin", "password": "password"},
        {"username": "user", "password": "user123"},
        {"username": "test", "password": "test123"}
    ]
    
    token = None
    for creds in login_attempts:
        try:
            print(f"   Trying login: {creds['username']}/{creds['password']}")
            response = requests.post(f"{base_url}/auth/login", json=creds)
            
            if response.status_code == 200:
                data = response.json()
                token = data.get('access_token')
                print(f"   ✅ Login successful! Token: {token[:20]}...")
                break
            else:
                print(f"   ❌ Login failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"   ❌ Login error: {e}")
    
    if not token:
        print("\n   ⚠️  No valid login found. Checking if user creation is needed...")
        
        # Try to create a user
        try:
            new_user = {"username": "admin", "password": "admin123"}
            print(f"   Creating user: {new_user['username']}")
            response = requests.post(f"{base_url}/auth/create-user", json=new_user)
            
            if response.status_code == 200:
                print("   ✅ User created successfully!")
                
                # Try to login again
                response = requests.post(f"{base_url}/auth/login", json=new_user)
                if response.status_code == 200:
                    data = response.json()
                    token = data.get('access_token')
                    print(f"   ✅ Login after creation successful! Token: {token[:20]}...")
                else:
                    print(f"   ❌ Login after creation failed: {response.text}")
            else:
                print(f"   ❌ User creation failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"   ❌ User creation error: {e}")
    
    if not token:
        print("\n❌ Could not obtain authentication token. Cannot test balance API.")
        return
    
    print(f"\n2. Testing authenticated balance API call...")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{base_url}/account/balance?fiat_currency=USD", headers=headers)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Balance API call successful!")
            
            # Check if we have assets
            if 'assets' in data:
                print(f"   Assets found: {len(data['assets'])}")
                
                btc_asset = None
                usdt_asset = None
                
                for asset in data['assets']:
                    if asset['asset'] == 'BTC':
                        btc_asset = asset
                    elif asset['asset'] == 'USDT':
                        usdt_asset = asset
                
                if btc_asset:
                    print(f"   ✅ BTC asset: {btc_asset}")
                else:
                    print("   ❌ No BTC asset found!")
                    
                if usdt_asset:
                    print(f"   ✅ USDT asset: {usdt_asset}")
                else:
                    print("   ❌ No USDT asset found!")
                
                # Show all assets
                print(f"   All assets:")
                for asset in data['assets']:
                    print(f"     - {asset['asset']}: {asset['free']} (${asset.get('usd_value', 'N/A')})")
            else:
                print("   ❌ No 'assets' field in response!")
                print(f"   Response: {json.dumps(data, indent=2)}")
        else:
            print(f"   ❌ Balance API failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Balance API error: {e}")
    
    print(f"\n3. Frontend checklist...")
    
    checklist = [
        "✓ Is the backend running on localhost:8000?",
        "✓ Is the frontend running and connecting to the right backend?",
        "✓ Did you login to the frontend UI?",
        "✓ Check browser DevTools > Application > Local Storage for 'token'",
        "✓ Check browser DevTools > Network tab for balance API calls",
        "✓ Check browser DevTools > Console for error messages"
    ]
    
    print("   Frontend debugging checklist:")
    for item in checklist:
        print(f"   {item}")
    
    print(f"\n4. Quick fix suggestions...")
    
    fixes = [
        "Refresh the frontend page (Ctrl+F5)",
        "Login again in the frontend",
        "Check if localStorage has a valid token",
        "Verify backend is returning correct balance data",
        "Clear browser cache and localStorage"
    ]
    
    print("   Try these fixes:")
    for i, fix in enumerate(fixes, 1):
        print(f"   {i}. {fix}")

if __name__ == "__main__":
    test_complete_auth_flow()