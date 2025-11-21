"""
Database Migration: Add Kill-Switch Fields to BotConfig
Adds columns for baseline, cooldown, and consecutive breach tracking
"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'gods_ping.db')

def migrate():
    print(f"\n📊 Migrating database: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(bot_configs)")
    columns = [row[1] for row in cursor.fetchall()]
    
    migrations = []
    
    if 'kill_switch_baseline' not in columns:
        migrations.append(("kill_switch_baseline", "ALTER TABLE bot_configs ADD COLUMN kill_switch_baseline REAL"))
    
    if 'kill_switch_last_trigger' not in columns:
        migrations.append(("kill_switch_last_trigger", "ALTER TABLE bot_configs ADD COLUMN kill_switch_last_trigger TIMESTAMP"))
    
    if 'kill_switch_cooldown_minutes' not in columns:
        migrations.append(("kill_switch_cooldown_minutes", "ALTER TABLE bot_configs ADD COLUMN kill_switch_cooldown_minutes INTEGER DEFAULT 60"))
    
    if 'kill_switch_consecutive_breaches' not in columns:
        migrations.append(("kill_switch_consecutive_breaches", "ALTER TABLE bot_configs ADD COLUMN kill_switch_consecutive_breaches INTEGER DEFAULT 3"))
    
    if not migrations:
        print("✅ Database already up to date!")
        conn.close()
        return
    
    print(f"\n🔧 Running {len(migrations)} migration(s):")
    for col_name, sql in migrations:
        try:
            cursor.execute(sql)
            print(f"  ✅ Added column: {col_name}")
        except sqlite3.OperationalError as e:
            print(f"  ⚠️  Column {col_name} may already exist: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Migration complete!")
    
    # Verify
    print("\n📋 Verifying new columns:")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(bot_configs)")
    for row in cursor.fetchall():
        col_name = row[1]
        if 'kill_switch' in col_name:
            print(f"  ✓ {col_name}: {row[2]} (default: {row[4]})")
    conn.close()


if __name__ == "__main__":
    migrate()
