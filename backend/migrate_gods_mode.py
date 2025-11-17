"""
Migration: Add gods_mode_enabled column to bot_configs table
Run this script to update existing database
"""
import sqlite3
import os
from pathlib import Path

# Database path - check both locations
DB_PATH_1 = Path(__file__).parent / "gods_ping.db"  # backend/gods_ping.db
DB_PATH_2 = Path(__file__).parent.parent / "gods_ping.db"  # gods_ping.db

# Use the one that exists and has data
if DB_PATH_1.exists() and DB_PATH_1.stat().st_size > 100000:
    DB_PATH = DB_PATH_1
elif DB_PATH_2.exists():
    DB_PATH = DB_PATH_2
else:
    DB_PATH = DB_PATH_1  # Default to backend location

def migrate():
    """Add gods_mode_enabled column if it doesn't exist"""
    
    if not DB_PATH.exists():
        print(f"❌ Database not found at {DB_PATH}")
        print("ℹ️  Database will be created automatically on first run")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(bot_configs)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'gods_mode_enabled' in columns:
            print("✅ Column 'gods_mode_enabled' already exists")
        else:
            # Add the column
            cursor.execute("""
                ALTER TABLE bot_configs 
                ADD COLUMN gods_mode_enabled BOOLEAN DEFAULT 0
            """)
            conn.commit()
            print("✅ Added 'gods_mode_enabled' column to bot_configs table")
        
        # Show current state
        cursor.execute("SELECT id, user_id, gods_hand_enabled, gods_mode_enabled FROM bot_configs")
        configs = cursor.fetchall()
        
        if configs:
            print("\n📊 Current Bot Configs:")
            print("ID | User ID | Gods Hand | Gods Mode")
            print("-" * 45)
            for row in configs:
                print(f"{row[0]:2d} | {row[1]:7d} | {row[2]:9d} | {row[3]:9d}")
        else:
            print("\nℹ️  No bot configs found (will be created on first login)")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 Running Gods Mode Migration...")
    print(f"📁 Database: {DB_PATH}")
    print()
    migrate()
    print("\n✨ Migration complete!")
