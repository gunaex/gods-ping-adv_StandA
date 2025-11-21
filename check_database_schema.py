#!/usr/bin/env python3
"""
Check what tables actually exist in the database
"""
import sqlite3

def check_tables():
    print("="*80)
    print("DATABASE SCHEMA INSPECTION")
    print("="*80)
    
    try:
        conn = sqlite3.connect('gods_ping.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("1. Available tables:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table['name']
            print(f"   - {table_name}")
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print(f"     Columns:")
            for col in columns:
                print(f"       {col['name']}: {col['type']} {'(PK)' if col['pk'] else ''}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = cursor.fetchone()['count']
            print(f"     Rows: {count}")
            print()
        
        print("2. Looking for bot configuration in other tables...")
        
        # Check if bot config might be in users table
        cursor.execute("PRAGMA table_info(users)")
        user_columns = cursor.fetchall()
        
        print("   Users table columns:")
        for col in user_columns:
            print(f"     - {col['name']}: {col['type']}")
        
        # Get user data
        cursor.execute("SELECT * FROM users WHERE id = 1")
        user = cursor.fetchone()
        
        if user:
            print(f"\n   User 1 data:")
            for key in user.keys():
                print(f"     {key}: {user[key]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_tables()