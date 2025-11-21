#!/usr/bin/env python3

import requests
import sys

def test_endpoints():
    """Test the endpoints that were failing"""
    
    base_url = "http://localhost:8000"
    
    endpoints = [
        "/api/paper-trading/performance",
        "/api/paper-trading/history?days=7",
        "/api/market/forecast/BTC/USDT?forecast_hours=6"
    ]
    
    for endpoint in endpoints:
        try:
            print(f"\n🧪 Testing: {endpoint}")
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"✅ Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"✅ Success! Response length: {len(response.text)}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection failed - server not running?")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return True

if __name__ == "__main__":
    test_endpoints()