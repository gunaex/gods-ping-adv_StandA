from app.db import Base, engine
from app.models import User, Trade, BotConfig
from app.logging_models import Log
import sqlite3

# Create all tables
Base.metadata.create_all(bind=engine)

# Check tables
conn = sqlite3.connect('gods_ping.db')
c = conn.cursor()
c.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = [t[0] for t in c.fetchall()]

print('✅ Database Tables Created:')
for table in tables:
    print(f'  - {table}')

# Check logs table
c.execute('PRAGMA table_info(logs)')
columns = c.fetchall()

print(f'\n✅ Logs Table ({len(columns)} columns):')
for col in columns:
    print(f'  - {col[1]}: {col[2]}')

conn.close()
print('\n🎉 All tables created successfully including logging system!')
