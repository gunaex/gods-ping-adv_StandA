#!/usr/bin/env python3
"""
Check database schema and update min_confidence
"""
import sqlite3
import sys
import os

def check_and_update():
    db_path = os.path.join(os.path.dirname(__file__), 'gods_ping.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check what tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Available tables: {[t[0] for t in tables]}")
        
        # Check if bot_configurations exists
        for table_name in ['bot_configs', 'bot_config', 'bot_configurations', 'botconfig']:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"Table '{table_name}' has {count} rows")
                
                # Get schema for this table
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                print(f"Columns in {table_name}: {[col[1] for col in columns]}")
                
                # Check for min_confidence column
                if any('min_confidence' in col[1] for col in columns):
                    # Update min_confidence
                    cursor.execute(f"SELECT id, symbol, min_confidence FROM {table_name}")
                    configs = cursor.fetchall()
                    print(f"\nCurrent configurations in {table_name}:")
                    
                    for config_id, symbol, min_conf in configs:
                        print(f"  Config {config_id} ({symbol}): min_confidence = {min_conf}")
                    
                    # Update to 0.5
                    cursor.execute(f"UPDATE {table_name} SET min_confidence = 0.5 WHERE min_confidence > 0.5")
                    updated = cursor.rowcount
                    
                    conn.commit()
                    print(f"\nUpdated {updated} configurations to min_confidence = 0.5")
                    
                    # Verify changes
                    cursor.execute(f"SELECT id, symbol, min_confidence FROM {table_name}")
                    configs = cursor.fetchall()
                    print("\nAfter update:")
                    for config_id, symbol, min_conf in configs:
                        print(f"  Config {config_id} ({symbol}): min_confidence = {min_conf}")
                    
                    break
                    
            except sqlite3.OperationalError as e:
                print(f"Table '{table_name}' does not exist: {e}")
                continue
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = check_and_update()
    sys.exit(0 if success else 1)