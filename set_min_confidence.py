#!/usr/bin/env python3
"""Set BotConfig.min_confidence and gods_hand_enabled for Admin user."""
import os, sys
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
from app.db import SessionLocal
from app.main import init_db
from app.models import BotConfig, User

def run():
    init_db()
    with SessionLocal() as db:
        user = db.query(User).filter(User.username == 'Admin').first()
        if not user:
            print('Admin user not found')
            return
        cfg = db.query(BotConfig).filter(BotConfig.user_id == user.id).first()
        if not cfg:
            print('BotConfig not found; creating default')
            cfg = BotConfig(user_id=user.id)
            db.add(cfg)
            db.commit()
            db.refresh(cfg)
        # Set lower threshold and enable gods hand
        cfg.min_confidence = 0.6
        cfg.gods_hand_enabled = True
        db.commit()
        print(f"Updated config: min_confidence={cfg.min_confidence}, gods_hand_enabled={cfg.gods_hand_enabled}, symbol={cfg.symbol}")

if __name__ == '__main__':
    run()
