"""
Authentication and Security
Hardcoded Admin + JWT tokens
"""
import os
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "gods-ping-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
REFRESH_TOKEN_EXPIRE_DAYS = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Hardcoded Admin Credentials
ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD_HASH = pwd_context.hash("K@nph0ng69")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access"):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != token_type:
            raise HTTPException(status_code=401, detail="Invalid token type")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current user from token"""
    token = credentials.credentials
    payload = verify_token(token, "access")
    
    user_id: int = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user.to_dict()


def get_current_active_user(current_user: dict = Depends(get_current_user)):
    """Ensure user is active"""
    if not current_user.get("is_active"):
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user


def ensure_admin_exists(db: Session):
    """Bootstrap: Create hardcoded admin if not exists"""
    admin = db.query(User).filter(User.username == ADMIN_USERNAME).first()
    if not admin:
        admin = User(
            username=ADMIN_USERNAME,
            hashed_password=ADMIN_PASSWORD_HASH,
            is_admin=True,
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        return True  # Created
    return False  # Already exists


# Simple encryption for API keys (base64 + XOR - upgrade to Fernet in production)
def encrypt_api_key(api_key: str) -> str:
    """Simple encryption (upgrade to Fernet for production)"""
    import base64
    key = SECRET_KEY[:16].encode()
    encrypted = bytes([a ^ b for a, b in zip(api_key.encode(), key * (len(api_key) // len(key) + 1))])
    return base64.b64encode(encrypted).decode()


def decrypt_api_key(encrypted: str) -> str:
    """Simple decryption (upgrade to Fernet for production)"""
    import base64
    key = SECRET_KEY[:16].encode()
    encrypted_bytes = base64.b64decode(encrypted.encode())
    decrypted = bytes([a ^ b for a, b in zip(encrypted_bytes, key * (len(encrypted_bytes) // len(key) + 1))])
    return decrypted.decode()
