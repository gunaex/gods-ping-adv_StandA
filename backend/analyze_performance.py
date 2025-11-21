#!/usr/bin/env python3
"""
Analyze Trading Performance Issues
"""
import sqlite3
from datetime import datetime, timedelta

def analyze_trading_performance():
    """Check recent trading performance and configuration"""
    
    conn = sqlite3.connect('gods_ping.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = [t[0] for t in cursor.fetchall()]
    print('Available tables:', tables)
    
    # Check bot configuration
    print('\n=== BOT CONFIGURATION ===')
    if 'bot_configs' in tables:
        cursor.execute('''
            SELECT min_confidence, hard_stop_loss_percent, 
                   trailing_take_profit_percent, max_daily_loss,
                   entry_step_percent, exit_step_percent
            FROM bot_configs LIMIT 1
        ''')
        config = cursor.fetchone()
        if config:
            print(f'Min Confidence: {config[0]:.2f}')
            print(f'Hard Stop Loss: {config[1]:.1f}%')
            print(f'Trailing Take Profit: {config[2]:.1f}%') 
            print(f'Max Daily Loss: {config[3]:.1f}%')
            print(f'Entry Step: {config[4]:.1f}%')
            print(f'Exit Step: {config[5]:.1f}%')
    
    # Check recent AI decisions
    print('\n=== RECENT AI DECISIONS ===')
    if 'logs' in tables:
        cursor.execute('''
            SELECT timestamp, message, details 
            FROM logs 
            WHERE message LIKE "%Gods Hand%" OR message LIKE "%AI%" OR message LIKE "%confidence%"
            ORDER BY timestamp DESC 
            LIMIT 10
        ''')
        logs = cursor.fetchall()
        for log in logs:
            print(f'{log[0]} | {log[1][:80]}...')
    
    # Check trading performance
    print('\n=== PAPER TRADING PERFORMANCE ===')
    for table in ['paper_trades', 'trades', 'paper_trading_snapshots']:
        if table in tables:
            print(f'Found {table} table')
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            count = cursor.fetchone()[0]
            print(f'{table}: {count} records')
            
            if count > 0:
                cursor.execute(f'SELECT * FROM {table} ORDER BY timestamp DESC LIMIT 5')
                cols = [description[0] for description in cursor.description]
                print(f'Columns: {cols}')
                recent = cursor.fetchall()
                for row in recent:
                    print(f'  {row}')
    
    conn.close()

if __name__ == "__main__":
    analyze_trading_performance()