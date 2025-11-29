import sys
import os

# Add the current directory to sys.path to allow importing app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db import SessionLocal, engine, Base
from app.models import User
from app.auth import get_password_hash

def create_admin_user():
    db = SessionLocal()
    try:
        username = "Admin"
        password = "K@nph0ng69"
        hashed_password = get_password_hash(password)

        user = db.query(User).filter(User.username == username).first()

        if user:
            print(f"User {username} already exists. Updating password.")
            user.hashed_password = hashed_password
            user.is_admin = True
            user.is_active = True
        else:
            print(f"Creating user {username}.")
            user = User(
                username=username,
                hashed_password=hashed_password,
                is_admin=True,
                is_active=True
            )
            db.add(user)

        db.commit()
        print(f"Admin user '{username}' configured successfully.")

    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    create_admin_user()
