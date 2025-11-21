#!/usr/bin/env python3
"""
Test WebSocket connection and diagnose proxy errors
"""
import asyncio
import websockets
import json
import sys

async def test_websocket_connection():
    print("="*80)
    print("WEBSOCKET CONNECTION TEST")
    print("="*80)
    
    # Test backend WebSocket directly
    backend_url = "ws://localhost:8000/ws/logs/test-token"
    
    print(f"1. Testing direct backend WebSocket connection...")
    print(f"   URL: {backend_url}")
    
    try:
        async with websockets.connect(backend_url) as websocket:
            print("✅ Direct backend connection successful")
            
            # Send ping
            await websocket.send("ping")
            print("📤 Sent: ping")
            
            # Wait for pong
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            print(f"📥 Received: {response}")
            
    except websockets.exceptions.ConnectionRefused:
        print("❌ Backend WebSocket server not running")
        print("   Make sure backend is started with: START_BACKEND.bat")
        return False
    except websockets.exceptions.InvalidStatusCode as e:
        print(f"❌ Backend WebSocket authentication failed: {e}")
        print("   This is expected with test-token - backend is running")
        return True  # Backend is running, just auth failed
    except Exception as e:
        print(f"❌ Backend WebSocket error: {e}")
        return False
    
    # Test frontend proxy
    frontend_proxy_url = "ws://localhost:5174/ws/logs/test-token"
    
    print(f"\n2. Testing frontend proxy WebSocket connection...")
    print(f"   URL: {frontend_proxy_url}")
    
    try:
        async with websockets.connect(frontend_proxy_url) as websocket:
            print("✅ Frontend proxy connection successful")
            
            # Send ping
            await websocket.send("ping")
            print("📤 Sent: ping")
            
            # Wait for pong
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            print(f"📥 Received: {response}")
            
    except websockets.exceptions.ConnectionRefused:
        print("❌ Frontend dev server not running")
        print("   Make sure frontend is started with: npm run dev")
        return False
    except Exception as e:
        print(f"❌ Frontend proxy error: {e}")
        print("   This might be the source of the ECONNRESET errors")
        return False
    
    return True

def check_services():
    print("="*80)
    print("SERVICE STATUS CHECK")
    print("="*80)
    
    import requests
    
    # Check backend
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        print("✅ Backend server (port 8000): Running")
    except requests.exceptions.ConnectionError:
        print("❌ Backend server (port 8000): Not running")
        return False
    except Exception as e:
        print(f"⚠️ Backend server (port 8000): {e}")
    
    # Check frontend
    try:
        response = requests.get("http://localhost:5174/", timeout=5)
        print("✅ Frontend server (port 5174): Running")
    except requests.exceptions.ConnectionError:
        print("❌ Frontend server (port 5174): Not running")
        return False
    except Exception as e:
        print(f"⚠️ Frontend server (port 5174): {e}")
    
    return True

def print_solutions():
    print("\n" + "="*80)
    print("WEBSOCKET PROXY ERROR SOLUTIONS")
    print("="*80)
    
    print("✅ FIXES APPLIED:")
    print("   1. Improved Vite proxy configuration with error handling")
    print("   2. Added WebSocket connection retry with exponential backoff")
    print("   3. Enhanced backend WebSocket error handling")
    print("   4. Added connection state checking in WebSocket manager")
    print("   5. Improved ping/pong keepalive mechanism")
    
    print("\n🔧 IF ERRORS PERSIST:")
    print("   1. Restart both servers:")
    print("      - Stop frontend (Ctrl+C in terminal)")
    print("      - Stop backend (Ctrl+C in terminal)")
    print("      - Start backend: cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    print("      - Start frontend: cd frontend && npm run dev")
    
    print("\n   2. Clear browser cache and reload the page")
    print("      - Hard refresh: Ctrl+Shift+R")
    print("      - Or open DevTools and disable cache")
    
    print("\n   3. Check for port conflicts:")
    print("      - Backend should be on port 8000")
    print("      - Frontend should be on port 5173 or 5174")
    
    print("\n   4. The WebSocket errors might be transient and not affect functionality")
    print("      - Check if real-time features still work")
    print("      - Kill-switch notifications, live logs, etc.")
    
    print("\n⚠️ EXPECTED BEHAVIOR:")
    print("   - Initial connection attempts may fail until backend is fully ready")
    print("   - WebSocket will auto-reconnect with exponential backoff")
    print("   - Connection should stabilize after 1-2 reconnection attempts")

async def main():
    print("🔍 WEBSOCKET PROXY ERROR DIAGNOSIS")
    
    # Check if services are running
    services_ok = check_services()
    
    if services_ok:
        # Test WebSocket connections
        await test_websocket_connection()
    
    # Show solutions
    print_solutions()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted")
    except Exception as e:
        print(f"\n❌ Test error: {e}")