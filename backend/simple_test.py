#!/usr/bin/env python3
"""Simple WebSocket test using Python requests"""

import requests
import json

def test_login():
    """Test login to get token"""
    try:
        response = requests.post(
            'http://localhost:8000/api/auth/login',
            json={'username': 'Admin', 'password': 'admin'}
        )
        
        print(f"Login status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Login successful, token: {data['access_token'][:20]}...")
            return data['access_token']
        else:
            print(f"❌ Login failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

if __name__ == "__main__":
    token = test_login()
    if token:
        print(f"\n✅ WebSocket URL would be: ws://localhost:8000/ws/logs/{token}")
    else:
        print("❌ Cannot test WebSocket without valid token")