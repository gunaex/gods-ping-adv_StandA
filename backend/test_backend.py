import requests

def test_backend():
    try:
        # Test basic connection
        r = requests.get('http://localhost:8000/api/bot/status', timeout=5)
        print(f"✅ Backend responsive: {r.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Backend not accessible - connection refused")
        return False
    except Exception as e:
        print(f"❌ Backend error: {e}")
        return False

if __name__ == "__main__":
    test_backend()