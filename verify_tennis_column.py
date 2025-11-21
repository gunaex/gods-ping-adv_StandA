import sqlite3
import os

db_path = os.path.join('backend', 'gods_ping.db')

def check_schema():
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("PRAGMA table_info(bot_configs)")
        columns = cursor.fetchall()
        print("Columns in bot_configs:")
        found = False
        for col in columns:
            print(f"- {col[1]} ({col[2]})")
            if col[1] == 'tennis_mode_enabled':
                found = True
        
        if found:
            print("\n✅ 'tennis_mode_enabled' column exists.")
        else:
            print("\n❌ 'tennis_mode_enabled' column MISSING.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_schema()