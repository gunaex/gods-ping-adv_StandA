#!/usr/bin/env python3
"""
Direct database inspection to see the exact state
"""
import sqlite3
import json

def inspect_database():
    print("="*80)
    print("DIRECT DATABASE INSPECTION")
    print("="*80)
    
    try:
        # Connect to database
        conn = sqlite3.connect('gods_ping.db')
        conn.row_factory = sqlite3.Row  # This enables column access by name
        cursor = conn.cursor()
        
        print("1. Checking Users table...")
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        for user in users:
            print(f"   User {user['id']}: {user['username']} (admin: {user['is_admin']})")
        
        print(f"\n2. Checking BotConfig for user 1...")
        cursor.execute("SELECT * FROM bot_config WHERE user_id = 1")
        config = cursor.fetchone()
        
        if config:
            print(f"   Budget: ${config['budget']}")
            print(f"   Symbol: {config['symbol']}")
            print(f"   Paper Trading: {config['paper_trading']}")
            print(f"   Updated At: {config['updated_at']}")
        else:
            print("   ❌ No BotConfig found for user 1!")
            
        print(f"\n3. Checking Trades for user 1...")
        cursor.execute("""
            SELECT COUNT(*) as total_trades, 
                   SUM(CASE WHEN side = 'buy' THEN 1 ELSE 0 END) as buy_trades,
                   SUM(CASE WHEN side = 'sell' THEN 1 ELSE 0 END) as sell_trades
            FROM trades 
            WHERE user_id = 1 AND bot_type = 'gods_hand'
        """)
        trade_summary = cursor.fetchone()
        
        print(f"   Total trades: {trade_summary['total_trades']}")
        print(f"   Buy trades: {trade_summary['buy_trades']}")
        print(f"   Sell trades: {trade_summary['sell_trades']}")
        
        if trade_summary['total_trades'] > 0:
            print(f"\n   Recent trades:")
            cursor.execute("""
                SELECT * FROM trades 
                WHERE user_id = 1 AND bot_type = 'gods_hand'
                ORDER BY timestamp DESC 
                LIMIT 5
            """)
            recent_trades = cursor.fetchall()
            
            for trade in recent_trades:
                print(f"     {trade['timestamp']}: {trade['side']} {trade['amount']} {trade['symbol']} @ ${trade['price']}")
        
        print(f"\n4. Checking for any other budget/balance related data...")
        
        # Check if there are any other tables that might affect balance
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"   Available tables:")
        for table in tables:
            table_name = table['name']
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = cursor.fetchone()['count']
            print(f"     - {table_name}: {count} rows")
            
        print(f"\n5. Raw BotConfig data...")
        cursor.execute("SELECT * FROM bot_config WHERE user_id = 1")
        config = cursor.fetchone()
        if config:
            print("   Raw config data:")
            for key in config.keys():
                print(f"     {key}: {config[key]}")
                
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    inspect_database()