#!/usr/bin/env python3
"""
Update min_confidence for existing bot configurations to 0.5 for better trading opportunities
"""
import sqlite3
import sys
import os

def update_min_confidence():
    db_path = os.path.join(os.path.dirname(__file__), 'gods_ping.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check current configs
        cursor.execute("SELECT id, symbol, min_confidence FROM bot_config")
        configs = cursor.fetchall()
        print(f"Found {len(configs)} bot configurations:")
        
        for config_id, symbol, min_conf in configs:
            print(f"  Config {config_id} ({symbol}): min_confidence = {min_conf}")
        
        # Update all configs to 0.5
        cursor.execute("UPDATE bot_config SET min_confidence = 0.5 WHERE min_confidence > 0.5")
        updated = cursor.rowcount
        
        conn.commit()
        print(f"\nUpdated {updated} configurations to min_confidence = 0.5")
        
        # Verify changes
        cursor.execute("SELECT id, symbol, min_confidence FROM bot_config")
        configs = cursor.fetchall()
        print("\nAfter update:")
        for config_id, symbol, min_conf in configs:
            print(f"  Config {config_id} ({symbol}): min_confidence = {min_conf}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error updating configurations: {e}")
        return False

if __name__ == "__main__":
    success = update_min_confidence()
    sys.exit(0 if success else 1)