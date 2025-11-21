import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'gods_ping.db')

def migrate():
    print(f"\n🔑 Migrating database for CryptoPanic API Key: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Add cryptopanic_api_key column
        cursor.execute("ALTER TABLE bot_configs ADD COLUMN cryptopanic_api_key VARCHAR")
        print("✅ Added 'cryptopanic_api_key' column")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e):
            print("ℹ️ 'cryptopanic_api_key' column already exists")
        else:
            print(f"❌ Error adding column: {e}")

    conn.commit()
    conn.close()
    print("✅ Migration complete!")

if __name__ == "__main__":
    migrate()
