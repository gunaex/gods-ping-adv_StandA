#!/usr/bin/env python3
"""
Test the current price fetching that the balance API uses
"""
import requests
import json

def test_price_fetching():
    print("="*80)
    print("TESTING PRICE FETCHING FOR BALANCE API")
    print("="*80)
    
    base_url = "http://localhost:8000/api"
    
    # Login first
    admin_creds = {"username": "Admin", "password": "K@nph0ng69"}
    
    try:
        print("1. Getting authentication token...")
        response = requests.post(f"{base_url}/auth/login", json=admin_creds)
        
        if response.status_code != 200:
            print(f"   ❌ Login failed: {response.text}")
            return
            
        data = response.json()
        token = data.get('access_token')
        headers = {"Authorization": f"Bearer {token}"}
        print("   ✅ Login successful")
        
        print(f"\n2. Testing current price API for BTC/USDT...")
        
        # Test the ticker endpoint that balance API uses
        price_response = requests.get(f"{base_url}/market/ticker/BTC/USDT", headers=headers)
        
        if price_response.status_code == 200:
            ticker_data = price_response.json()
            print(f"   ✅ Price API successful:")
            print(f"   {json.dumps(ticker_data, indent=2)}")
            
            current_price = ticker_data.get('last', 0)
            print(f"\n   Current price (last): {current_price}")
            
            if current_price == 0:
                print(f"   ❌ Current price is 0 - this causes BTC quantity to be 0!")
                print(f"   When quantity_held = position_value / current_price")
                print(f"   And current_price = 0, then quantity_held = 14240 / 0 = ERROR or 0")
            else:
                expected_btc = 14240.0 / current_price
                print(f"   ✅ Current price is valid: ${current_price}")
                print(f"   Expected BTC quantity: {expected_btc}")
        else:
            print(f"   ❌ Price API failed: {price_response.status_code}")
            print(f"   Response: {price_response.text}")
            print(f"   This means get_current_price() in balance API fails!")
            
        print(f"\n3. Testing alternative price endpoints...")
        
        # Test different price formats
        price_endpoints = [
            "/market/ticker/BTC/USDT",
            "/market/ticker/BTCUSDT", 
            "/market/ticker/BTC-USDT"
        ]
        
        for endpoint in price_endpoints:
            try:
                test_response = requests.get(f"{base_url}{endpoint}", headers=headers)
                print(f"   {endpoint}: Status {test_response.status_code}")
                
                if test_response.status_code == 200:
                    data = test_response.json()
                    last_price = data.get('last', 0)
                    print(f"     Last price: {last_price}")
            except Exception as e:
                print(f"   {endpoint}: Error - {e}")
                
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print(f"\n4. Analysis:")
    print("   If the price API returns 0 or fails, the balance API will:")
    print("   1. Set current_price = 0")
    print("   2. Calculate quantity_held = position_value / 0 = 0 (or error)")
    print("   3. Show BTC balance as 0.0")
    print("   4. Show all funds as USDT")
    print(f"\n   Expected behavior:")
    print("   1. Use fallback price of $42,000 if price API fails")
    print("   2. Calculate quantity_held = $14,240 / $42,000 = 0.339 BTC")
    print("   3. Show proper 50/50 split")

if __name__ == "__main__":
    test_price_fetching()