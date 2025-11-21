import sys
import os
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
import json

# Add backend directory to path so we can import app modules
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.db import DATABASE_URL
from app.logging_models import Log, LogCategory

def check_logs():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        print("--- Checking AI Logs ---")
        
        # Check AI_THINKING logs
        thinking_logs = db.query(Log).filter(
            Log.category == LogCategory.AI_THINKING
        ).order_by(desc(Log.timestamp)).limit(5).all()

        print(f"\nFound {len(thinking_logs)} recent AI_THINKING logs:")
        for log in thinking_logs:
            print(f"[{log.timestamp}] {log.symbol} - Rec: {log.ai_recommendation} (Conf: {log.ai_confidence})")
            print(f"Message: {log.message[:100]}...")
            if log.details:
                try:
                    details = json.loads(log.details)
                    print(f"Details keys: {list(details.keys())}")
                except:
                    print("Details: (invalid json)")
            print("-" * 20)

        # Check AI_ACTION logs
        action_logs = db.query(Log).filter(
            Log.category == LogCategory.AI_ACTION
        ).order_by(desc(Log.timestamp)).limit(5).all()

        print(f"\nFound {len(action_logs)} recent AI_ACTION logs:")
        for log in action_logs:
            print(f"[{log.timestamp}] {log.symbol} - Executed: {log.ai_executed}")
            print(f"Message: {log.message}")
            print(f"Reason: {log.execution_reason}")
            print("-" * 20)

    except Exception as e:
        print(f"Error checking logs: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_logs()
