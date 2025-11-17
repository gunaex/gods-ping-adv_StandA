#!/usr/bin/env python3
"""Check and set up bot configuration for Gods Hand"""

import os
import sys

# Add the backend path to sys.path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from app.db import SessionLocal
from app.main import init_db
from app.models import BotConfig, User
from datetime import datetime

def check_and_setup_config():
    print("=== BOT CONFIGURATION CHECK ===\n")
    
    # Initialize database
    init_db()
    
    with SessionLocal() as db:
        # Check all users
        users = db.query(User).all()
        print("Users in database:")
        for user in users:
            print(f"- ID: {user.id}, Username: {user.username}")
        
        print()
        
        # Check all bot configs
        configs = db.query(BotConfig).all()
        print("Bot configurations:")
        if configs:
            for config in configs:
                print(f"- User ID: {config.user_id}, Symbol: {config.symbol}, Paper: {config.paper_trading}, Budget: ${config.budget}")
        else:
            print("- No configurations found")
        
        print()
        
        # Setup default config for admin user if none exists
        admin_user = db.query(User).filter(User.username == "Admin").first()
        if admin_user:
            existing_config = db.query(BotConfig).filter(BotConfig.user_id == admin_user.id).first()
            
            if not existing_config:
                print(f"Creating default configuration for admin user (ID: {admin_user.id})...")
                
                config = BotConfig(
                    user_id=admin_user.id,
                    symbol="BTC/USDT",
                    paper_trading=True,
                    budget=25000.0,  # $25k paper trading budget
                    position_size_ratio=1.0,  # 100% as mentioned in conversation
                    risk_level='moderate',
                    min_confidence=0.7,
                    entry_step_percent=10.0,
                    exit_step_percent=10.0
                )
                
                db.add(config)
                db.commit()
                
                print("✅ Default configuration created:")
                print(f"   - Symbol: BTCUSDT")
                print(f"   - Paper Trading: True")
                print(f"   - Budget: $25,000")
                print(f"   - Position Size Ratio: 100%")
                
            else:
                print(f"✅ Configuration already exists for admin user")
                print(f"   - Symbol: {existing_config.symbol}")
                print(f"   - Paper Trading: {existing_config.paper_trading}")
                print(f"   - Budget: ${existing_config.budget}")
                
        else:
            print("❌ Admin user not found")

if __name__ == "__main__":
    check_and_setup_config()