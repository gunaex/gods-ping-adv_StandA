"""
API Integration Test Script
Tests all critical API endpoints after servers are running
Run this AFTER starting both backend and frontend servers
"""
import sys
from pathlib import Path
import requests
import json
import time
from datetime import datetime

# Add backend to Python path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

BASE_URL = "http://localhost:8000"
token = None

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def test_health_check():
    """Test root endpoint health check"""
    print_header("Test 1: Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Status: {response.status_code}")
            print_info(f"Message: {data['message']}")
            print_info(f"Version: {data['version']}")
            print_info(f"Server Time: {data['server_time']}")
            print_info(f"Timezone: {data['server_timezone']}")
            return True
        else:
            print_error(f"Unexpected status: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check failed: {e}")
        print_info("Is the backend server running on port 8000?")
        return False

def test_login():
    """Test login endpoint"""
    print_header("Test 2: Login")
    
    global token
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "username": "Admin",
                "password": "admin123"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data['access_token']
            print_success(f"Login successful")
            print_info(f"Access Token: {token[:20]}...")
            print_info(f"Token Type: {data['token_type']}")
            print_info(f"User: {data['user']['username']}")
            return True
        else:
            print_error(f"Login failed: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Login test failed: {e}")
        return False

def test_get_me():
    """Test get current user endpoint"""
    print_header("Test 3: Get Current User")
    
    if not token:
        print_error("No token available - login first")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Got user info")
            print_info(f"Username: {data['username']}")
            print_info(f"Is Admin: {data['is_admin']}")
            return True
        else:
            print_error(f"Get user failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Get user test failed: {e}")
        return False

def test_get_logs():
    """Test get logs endpoint"""
    print_header("Test 4: Get Logs")
    
    if not token:
        print_error("No token available - login first")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/logs?limit=10",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            logs = data['logs']
            print_success(f"Retrieved {len(logs)} logs")
            print_info(f"Total: {data['total']}")
            print_info(f"Page: {data['page']}")
            
            if logs:
                print_info(f"Latest log: {logs[0]['category']} - {logs[0]['message'][:50]}...")
            
            return True
        else:
            print_error(f"Get logs failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Get logs test failed: {e}")
        return False

def test_get_log_categories():
    """Test get log categories endpoint"""
    print_header("Test 5: Get Log Categories")
    
    if not token:
        print_error("No token available - login first")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/logs/categories",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            categories = data['categories']
            print_success(f"Retrieved {len(categories)} categories")
            for cat in categories:
                print_info(f"  - {cat['label']} ({cat['value']})")
            return True
        else:
            print_error(f"Get categories failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Get categories test failed: {e}")
        return False

def test_get_ai_actions():
    """Test AI actions comparison endpoint"""
    print_header("Test 6: Get AI Actions Comparison")
    
    if not token:
        print_error("No token available - login first")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/logs/ai-actions?limit=5",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Retrieved AI actions comparison")
            print_info(f"Thinking logs: {len(data['thinking'])}")
            print_info(f"Action logs: {len(data['actions'])}")
            return True
        else:
            print_error(f"Get AI actions failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Get AI actions test failed: {e}")
        return False

def test_create_test_logs():
    """Create test logs using the logger"""
    print_header("Test 7: Create Test Logs")
    
    try:
        from app.db import get_db
        from app.logger import get_logger
        
        db = next(get_db())
        logger = get_logger(db)
        
        # Create various test logs
        logger.error("Test error from API test", details="Testing error logging")
        logger.user_action(user_id=1, message="Test user action", details="User performed test action")
        logger.ai_thinking(
            symbol="BTCUSDT",
            message="AI analyzing BTC/USDT",
            recommendation="BUY",
            confidence=0.85,
            details="RSI oversold, MACD bullish crossover"
        )
        logger.ai_action(
            symbol="BTCUSDT",
            message="AI executed BUY order",
            recommendation="BUY",
            executed=True,
            reason="High confidence signal"
        )
        logger.trading(symbol="BTCUSDT", message="Test trade executed", details="Buy 0.001 BTC at $50000")
        
        db.close()
        print_success("Created 5 test log entries")
        return True
    except Exception as e:
        print_error(f"Create test logs failed: {e}")
        return False

def test_filter_logs():
    """Test log filtering"""
    print_header("Test 8: Filter Logs by Category")
    
    if not token:
        print_error("No token available - login first")
        return False
    
    categories = ['error', 'ai_thinking', 'ai_action', 'trading']
    
    try:
        for category in categories:
            response = requests.get(
                f"{BASE_URL}/api/logs?category={category}&limit=5",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Category '{category}': {len(data['logs'])} logs")
            else:
                print_error(f"Filter by {category} failed")
                return False
        
        return True
    except Exception as e:
        print_error(f"Filter logs test failed: {e}")
        return False

def test_api_docs():
    """Test API documentation is accessible"""
    print_header("Test 9: API Documentation")
    
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print_success("API docs accessible at http://localhost:8000/docs")
            return True
        else:
            print_error(f"API docs not accessible: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"API docs test failed: {e}")
        return False

def test_frontend():
    """Test frontend is running"""
    print_header("Test 10: Frontend Availability")
    
    try:
        response = requests.get("http://localhost:5173")
        if response.status_code == 200:
            print_success("Frontend accessible at http://localhost:5173")
            print_info("Open in browser to test UI")
            return True
        else:
            print_error(f"Frontend not accessible: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Frontend test failed: {e}")
        print_info("Is the frontend server running? (npm run dev)")
        return False

def main():
    """Run all API tests"""
    print("\n" + "="*60)
    print("  🧪 GODS PING - API INTEGRATION TEST SUITE")
    print("="*60)
    print("\nMake sure both servers are running:")
    print("  Backend:  http://localhost:8000")
    print("  Frontend: http://localhost:5173")
    print("\nWaiting 2 seconds...")
    time.sleep(2)
    
    tests = [
        test_health_check,
        test_login,
        test_get_me,
        test_create_test_logs,
        test_get_logs,
        test_get_log_categories,
        test_get_ai_actions,
        test_filter_logs,
        test_api_docs,
        test_frontend,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            time.sleep(0.5)  # Small delay between tests
        except Exception as e:
            print_error(f"Test crashed: {e}")
            results.append(False)
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    print(f"Tests Failed: {total - passed}/{total}")
    
    if all(results):
        print("\n" + "🎉 " * 20)
        print("\n  ✅ ALL API TESTS PASSED!")
        print("\n  Your Gods Ping application is fully operational!")
        print("\n  Access points:")
        print("    - Frontend: http://localhost:5173")
        print("    - API: http://localhost:8000")
        print("    - API Docs: http://localhost:8000/docs")
        print("\n  Login credentials:")
        print("    Username: Admin")
        print("    Password: admin123")
        print("\n" + "🎉 " * 20)
        return 0
    else:
        print("\n" + "⚠️ " * 20)
        print("\n  ❌ SOME TESTS FAILED")
        print("\n  Check the errors above.")
        print("\n" + "⚠️ " * 20)
        return 1

if __name__ == "__main__":
    exit(main())
