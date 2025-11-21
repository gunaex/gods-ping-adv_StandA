#!/usr/bin/env python3
"""
WebSocket Connection Test
Tests the WebSocket endpoint to ensure it works properly
"""
import asyncio
import websockets
import json
import sys

async def test_websocket():
    """Test WebSocket connection to backend"""
    
    # First, let's get a token by logging in
    import requests
    
    # Login to get a token
    try:
        login_response = requests.post(
            'http://localhost:8000/api/auth/login',
            json={'username': 'Admin', 'password': 'admin'}
        )
        
        if login_response.status_code != 200:
            print("❌ Failed to login")
            return False
            
        token = login_response.json()['access_token']
        print(f"✅ Got auth token: {token[:20]}...")
        
    except Exception as e:
        print(f"❌ Failed to get token: {e}")
        return False
    
    # Test WebSocket connection
    uri = f"ws://localhost:8000/ws/logs/{token}"
    print(f"\n🔌 Testing WebSocket connection to: {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connected successfully!")
            
            # Send a ping
            await websocket.send("ping")
            print("📤 Sent ping")
            
            # Wait for response (with timeout)
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"📥 Received: {response}")
            except asyncio.TimeoutError:
                print("⏰ No response received (this is okay for a ping)")
            
            print("✅ WebSocket test completed successfully!")
            return True
            
    except Exception as e:
        print(f"❌ WebSocket connection failed: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_websocket())
    sys.exit(0 if result else 1)