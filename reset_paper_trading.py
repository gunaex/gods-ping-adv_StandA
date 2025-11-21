#!/usr/bin/env python3
"""
Reset paper trading data for fresh regression testing after AI fixes
"""
import sqlite3
import sys
import os
from datetime import datetime

def reset_paper_trading():
    print("="*80)
    print("RESETTING PAPER TRADING DATA FOR REGRESSION TESTING")
    print("="*80)
    
    db_path = os.path.join(os.path.dirname(__file__), 'gods_ping.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check current paper trading data
        cursor.execute("SELECT COUNT(*) FROM trades WHERE paper_trading = 1")
        paper_trades = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM paper_trading_snapshots")
        snapshots = cursor.fetchone()[0]
        
        print(f"Found {paper_trades} paper trades and {snapshots} snapshots")
        
        if paper_trades == 0 and snapshots == 0:
            print("📋 No paper trading data to reset")
            conn.close()
            return True
            
        # Backup current data first
        backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print(f"📦 Creating backup with timestamp: {backup_timestamp}")
        
        # Create backup tables
        cursor.execute(f"""
            CREATE TABLE trades_backup_{backup_timestamp} AS 
            SELECT * FROM trades WHERE paper_trading = 1
        """)
        
        cursor.execute(f"""
            CREATE TABLE snapshots_backup_{backup_timestamp} AS 
            SELECT * FROM paper_trading_snapshots
        """)
        
        backup_trades = cursor.rowcount
        
        print(f"✅ Backup created: trades_backup_{backup_timestamp}")
        print(f"✅ Backup created: snapshots_backup_{backup_timestamp}")
        
        # Reset paper trading data
        cursor.execute("DELETE FROM trades WHERE paper_trading = 1")
        deleted_trades = cursor.rowcount
        
        cursor.execute("DELETE FROM paper_trading_snapshots")
        deleted_snapshots = cursor.rowcount
        
        # Reset paper trading tracker state if it exists
        try:
            cursor.execute("UPDATE bot_configs SET paper_trading = 1")  # Ensure paper trading is enabled
            updated_configs = cursor.rowcount
            print(f"✅ Ensured paper trading is enabled for {updated_configs} bot configs")
        except Exception as e:
            print(f"ℹ️  Could not update bot configs: {e}")
        
        conn.commit()
        
        print(f"🗑️  Deleted {deleted_trades} paper trades")
        print(f"🗑️  Deleted {deleted_snapshots} snapshots")
        print()
        
        # Verify reset
        cursor.execute("SELECT COUNT(*) FROM trades WHERE paper_trading = 1")
        remaining_trades = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM paper_trading_snapshots")
        remaining_snapshots = cursor.fetchone()[0]
        
        if remaining_trades == 0 and remaining_snapshots == 0:
            print("✅ Paper trading data successfully reset")
            print("📊 Ready for fresh regression testing")
            print()
            print("REGRESSION TESTING CHECKLIST:")
            print("- ✅ AI engine confidence bug fixed")
            print("- ✅ RSI thresholds balanced for more BUY signals")
            print("- ✅ Volume analysis added")
            print("- ✅ Min confidence lowered to 0.5")
            print("- ✅ Paper trading data reset")
            print("- 🔄 Start Gods Hand bot and monitor performance")
            print("- 📈 Target: Win rate > 50% (vs previous 38.1%)")
        else:
            print(f"❌ Reset incomplete: {remaining_trades} trades, {remaining_snapshots} snapshots remain")
            conn.close()
            return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error resetting paper trading: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_backup_info():
    """Show available backups"""
    db_path = os.path.join(os.path.dirname(__file__), 'gods_ping.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name LIKE 'trades_backup_%'
            ORDER BY name DESC
        """)
        
        backups = cursor.fetchall()
        if backups:
            print("\n📦 Available backup tables:")
            for backup in backups:
                table_name = backup[0]
                timestamp = table_name.split('_')[-2] + '_' + table_name.split('_')[-1]
                
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                
                print(f"  - {table_name}: {count} trades (backup from {timestamp})")
        else:
            print("\nℹ️  No backup tables found")
            
        conn.close()
        
    except Exception as e:
        print(f"Error checking backups: {e}")

def main():
    print("🔄 GODS PING ADVANCED - PAPER TRADING RESET")
    print()
    
    success = reset_paper_trading()
    show_backup_info()
    
    if success:
        print()
        print("🎯 READY FOR REGRESSION TESTING!")
        print()
        print("To start testing:")
        print("1. Run: START_BACKEND.bat")
        print("2. Run: START_FRONTEND.bat") 
        print("3. Enable Gods Hand in the web interface")
        print("4. Monitor AI decisions and win rate")
        print("5. Expected improvements:")
        print("   - More BUY signals generated")
        print("   - Better confidence calculations")
        print("   - Win rate > 50%")
    else:
        print("❌ Reset failed. Please check the errors above.")
        
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)