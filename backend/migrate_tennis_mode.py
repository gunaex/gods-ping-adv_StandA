import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'gods_ping.db')

def migrate():
    print(f"\n🎾 Migrating database for Tennis Mode: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Add tennis_mode_enabled column
        cursor.execute("ALTER TABLE bot_configs ADD COLUMN tennis_mode_enabled BOOLEAN DEFAULT 0")
        print("✅ Added 'tennis_mode_enabled' column")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e):
            print("ℹ️ 'tennis_mode_enabled' column already exists")
        else:
            print(f"❌ Error adding column: {e}")

    conn.commit()
    conn.close()
    print("✅ Migration complete!")

if __name__ == "__main__":
    migrate()
