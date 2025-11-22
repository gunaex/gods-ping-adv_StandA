#!/usr/bin/env python3
"""
Test what the frontend API is actually receiving for balance
"""
import requests
import json
import sys

def test_frontend_balance_api():
    print("="*80)
    print("TESTING FRONTEND BALANCE API CALL")
    print("="*80)
    
    # Test the same API call the frontend makes
    base_url = "http://localhost:8000"
    
    print("1. Testing unauthenticated balance API call...")
    try:
        # This is what the frontend calls
        response = requests.get(f"{base_url}/api/account/balance?fiat_currency=USD")
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 403:
            print("   ✅ Correctly requires authentication")
        elif response.status_code == 200:
            print("   ⚠️  Unexpected success without authentication")
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        else:
            print(f"   ❌ Unexpected status code: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n2. Checking if there are multiple balance endpoints...")
    
    # Check for other balance endpoints
    endpoints_to_check = [
        "/api/account/balance",
        "/api/balance", 
        "/api/paper-trading/balance",
        "/api/bot/balance"
    ]
    
    for endpoint in endpoints_to_check:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            print(f"   {endpoint}: Status {response.status_code}")
            
            if response.status_code == 200:
                print(f"     ⚠️  Unexpected success: {response.text[:100]}...")
                
        except Exception as e:
            print(f"   {endpoint}: Error - {e}")
    
    print("\n3. Frontend symbol parsing analysis...")
    
    # Check how the frontend might be parsing the symbol
    symbol = "BTC/USDT"
    base_currency = symbol.split('/')[0]  # Should be "BTC"
    quote_currency = symbol.split('/')[1] if '/' in symbol else 'USDT'  # Should be "USDT"
    
    print(f"   Symbol: {symbol}")
    print(f"   Base Currency: {base_currency}")
    print(f"   Quote Currency: {quote_currency}")
    
    # Test if the backend balance has the right asset names
    print("\n4. Checking backend asset naming...")
    
    # Simulate what the frontend should find
    mock_assets = [
        {"asset": "USDT", "free": 14240.0, "total": 14240.0, "usd_value": 14240.0},
        {"asset": "BTC", "free": 0.15435182, "total": 0.15435182, "usd_value": 14240.0}
    ]
    
    base_asset = next((a for a in mock_assets if a['asset'] == base_currency), None)
    quote_asset = next((a for a in mock_assets if a['asset'] == quote_currency), None)
    
    print(f"   Looking for base asset '{base_currency}': {'Found' if base_asset else 'NOT FOUND'}")
    print(f"   Looking for quote asset '{quote_currency}': {'Found' if quote_asset else 'NOT FOUND'}")
    
    if base_asset:
        print(f"   Base asset data: {base_asset}")
    if quote_asset:
        print(f"   Quote asset data: {quote_asset}")
    
    print("\n5. Possible frontend issues...")
    
    issues = [
        "Frontend not authenticated - getting empty balance",
        "Frontend caching old balance data", 
        "Asset matching logic failing (case sensitivity, etc.)",
        "Balance API returning different data to frontend vs backend test",
        "Frontend using wrong symbol format",
        "React state not updating with new balance data"
    ]
    
    print("   Potential causes:")
    for i, issue in enumerate(issues, 1):
        print(f"     {i}. {issue}")
    
    print(f"\n{'='*80}")
    print("RECOMMENDATIONS")
    print(f"{'='*80}")
    
    print("1. Check browser DevTools Network tab:")
    print("   - Look for /api/account/balance calls")
    print("   - Check if they're returning 200 OK")
    print("   - Verify the response contains BTC asset")
    
    print("\n2. Check frontend console for errors:")
    print("   - Authentication failures")
    print("   - Balance loading errors")
    print("   - Asset parsing issues")
    
    print("\n3. Hard refresh the frontend:")
    print("   - Ctrl+Shift+R to bypass cache")
    print("   - Or clear localStorage and reload")
    
    print("\n4. If issue persists, check:")
    print("   - Frontend authentication token validity")
    print("   - Balance API endpoint returning correct data")
    print("   - Asset name matching logic")

if __name__ == "__main__":
    test_frontend_balance_api()