#!/usr/bin/env python3
"""
Add kill-switch columns to main database
"""
import sqlite3
import sys
import os

def migrate_main_db():
    print("Adding kill-switch columns to main database...")
    
    db_path = os.path.join(os.path.dirname(__file__), 'gods_ping.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(bot_configs)")
        existing_columns = [col[1] for col in cursor.fetchall()]
        
        kill_switch_columns = [
            ('kill_switch_baseline', 'FLOAT'),
            ('kill_switch_last_trigger', 'DATETIME'),
            ('kill_switch_cooldown_minutes', 'INTEGER', 5),
            ('kill_switch_consecutive_breaches', 'INTEGER', 0)
        ]
        
        for column_info in kill_switch_columns:
            column_name = column_info[0]
            column_type = column_info[1] 
            default_value = column_info[2] if len(column_info) > 2 else None
            
            if column_name not in existing_columns:
                if default_value is not None:
                    sql = f"ALTER TABLE bot_configs ADD COLUMN {column_name} {column_type} DEFAULT {default_value}"
                else:
                    sql = f"ALTER TABLE bot_configs ADD COLUMN {column_name} {column_type}"
                    
                cursor.execute(sql)
                print(f"✅ Added column: {column_name}")
            else:
                print(f"ℹ️  Column already exists: {column_name}")
        
        conn.commit()
        conn.close()
        
        print("✅ Kill-switch migration completed")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    success = migrate_main_db()
    sys.exit(0 if success else 1)