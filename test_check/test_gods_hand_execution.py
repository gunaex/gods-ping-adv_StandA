#!/usr/bin/env python3
"""Manually trigger Gods Hand execution to test SELL capability"""

import os
import sys
import asyncio

# Add the backend path to sys.path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from app.db import SessionLocal
from app.main import init_db
from app.models import BotConfig
from app.bots import gods_hand_once

async def test_gods_hand_execution():
    print("=== GODS HAND EXECUTION TEST ===\n")
    
    # Initialize database
    init_db()
    
    with SessionLocal() as db:
        # Get bot config
        config = db.query(BotConfig).filter(BotConfig.user_id == 1).first()
        
        if not config:
            print("❌ No bot configuration found")
            return
            
        print(f"Bot Config Found:")
        print(f"- User ID: {config.user_id}")
        print(f"- Symbol: {config.symbol}")
        print(f"- Paper Trading: {config.paper_trading}")
        print(f"- Budget: ${config.budget}")
        print()
        
        print("Executing Gods Hand cycle...")
        
        try:
            # Execute one Gods Hand cycle
            result = await gods_hand_once(1, config, db)
            print(f"✅ Gods Hand executed successfully!")
            print(f"Result: {result}")
            
        except Exception as e:
            print(f"❌ Gods Hand execution failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_gods_hand_execution())