import sqlite3
import sys
sys.path.insert(0, 'backend')

# First ensure tables are created
from app.db import Base, engine
print('Creating all database tables...')
Base.metadata.create_all(bind=engine)
print('✅ Tables created\n')

conn = sqlite3.connect('backend/gods_ping.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print('📊 Database Tables Created:')
for table in tables:
    print(f'  ✅ {table[0]}')
    
    # Get column info for logs table
    if table[0] == 'logs':
        cursor.execute(f"PRAGMA table_info(logs)")
        columns = cursor.fetchall()
        print(f'\n  📋 Logs Table Columns:')
        for col in columns:
            print(f'    - {col[1]} ({col[2]})')

conn.close()
print('\n✅ Database successfully configured with logging support!')
