"""
Database migration script to add incremental position building columns
Run this once to update your existing database
"""
import sqlite3
import os
import sys

# Try multiple possible database locations
DB_PATHS = [
    "gods_ping.db",                    # Current directory
    "backend/gods_ping.db",            # From project root
    "./gods_ping.db",                  # Explicit current dir
    "../gods_ping.db",                 # Parent directory
]

DB_PATH = None
for path in DB_PATHS:
    if os.path.exists(path):
        DB_PATH = path
        break

if DB_PATH is None:
    print("❌ Database file not found in any of these locations:")
    for path in DB_PATHS:
        print(f"   - {os.path.abspath(path)}")
    print("\nℹ️  The database is created when you first run the backend server.")
    print("   Please start the backend at least once, then run this migration.")
    sys.exit(1)

print(f"📊 Connecting to database: {DB_PATH}")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(bot_configs)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'entry_step_percent' in columns and 'exit_step_percent' in columns:
        print("✅ Columns already exist! No migration needed.")
    else:
        print("🔧 Adding new columns to bot_configs table...")
        
        # Add entry_step_percent column
        if 'entry_step_percent' not in columns:
            cursor.execute("""
                ALTER TABLE bot_configs 
                ADD COLUMN entry_step_percent REAL DEFAULT 10.0
            """)
            print("✅ Added entry_step_percent column (default: 10.0)")
        
        # Add exit_step_percent column
        if 'exit_step_percent' not in columns:
            cursor.execute("""
                ALTER TABLE bot_configs 
                ADD COLUMN exit_step_percent REAL DEFAULT 10.0
            """)
            print("✅ Added exit_step_percent column (default: 10.0)")
        
        # Commit changes
        conn.commit()
        print("✅ Database migration completed successfully!")
        
        # Verify columns were added
        cursor.execute("PRAGMA table_info(bot_configs)")
        columns_after = [row[1] for row in cursor.fetchall()]
        print(f"\n📋 Current bot_configs columns: {', '.join(columns_after)}")

except sqlite3.Error as e:
    print(f"❌ Migration failed: {e}")
    conn.rollback()
    exit(1)

finally:
    conn.close()
    print("\n🎉 Done! You can now restart your backend server.")
