import sys
import os

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db import SessionLocal
from app.models import User
from app.auth import verify_password

def check_login(username, password):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"User '{username}' not found.")
            return

        print(f"User found: {user.username}")
        print(f"Is Active: {user.is_active}")
        print(f"Is Admin: {user.is_admin}")
        
        if verify_password(password, user.hashed_password):
            print("✅ Password verification SUCCESSFUL.")
        else:
            print("❌ Password verification FAILED.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_login("Admin", "K@nph0ng69")
