#!/usr/bin/env python3
"""
Check database schema to understand trade tracking
"""
import sqlite3
import sys
import os

def check_db_schema():
    db_path = os.path.join(os.path.dirname(__file__), 'gods_ping.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check trades table
        print("TRADES TABLE SCHEMA:")
        cursor.execute("PRAGMA table_info(trades)")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        print("\nTRADES TABLE SAMPLE:")
        cursor.execute("SELECT * FROM trades LIMIT 5")
        trades = cursor.fetchall()
        for trade in trades:
            print(f"  {trade}")
            
        print(f"\nTotal trades: {len(trades)}")
        
        # Check paper_trading_snapshots
        print("\n" + "="*50)
        print("PAPER TRADING SNAPSHOTS TABLE:")
        try:
            cursor.execute("PRAGMA table_info(paper_trading_snapshots)")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  {col[1]} ({col[2]})")
                
            cursor.execute("SELECT COUNT(*) FROM paper_trading_snapshots")
            count = cursor.fetchone()[0]
            print(f"\nTotal snapshots: {count}")
            
        except Exception as e:
            print(f"No paper_trading_snapshots table: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_db_schema()