#!/usr/bin/env python3
"""
Check the actual BotConfig data
"""
import sqlite3

def check_bot_config():
    print("="*80)
    print("BOT CONFIG INSPECTION")
    print("="*80)
    
    try:
        conn = sqlite3.connect('gods_ping.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("1. BotConfig data for user 1:")
        cursor.execute("SELECT * FROM bot_configs WHERE user_id = 1")
        config = cursor.fetchone()
        
        if config:
            print("   ✅ BotConfig found!")
            for key in config.keys():
                value = config[key]
                if key in ['created_at', 'updated_at', 'kill_switch_last_trigger']:
                    print(f"     {key}: {value}")
                elif 'password' in key or 'secret' in key:
                    print(f"     {key}: {'***' if value else None}")
                else:
                    print(f"     {key}: {value}")
        else:
            print("   ❌ No BotConfig found for user 1!")
        
        conn.close()
        
        print(f"\n2. Analysis:")
        if config:
            budget = config['budget']
            symbol = config['symbol'] 
            paper_trading = config['paper_trading']
            
            print(f"   Budget: ${budget}")
            print(f"   Symbol: {symbol}")
            print(f"   Paper Trading: {paper_trading}")
            
            if paper_trading:
                print(f"   Expected 50/50 split:")
                print(f"     - USDT: ${budget / 2}")
                print(f"     - BTC value: ${budget / 2}")
                
                # With current BTC price around $92,240
                btc_price = 92240.17
                expected_btc = (budget / 2) / btc_price
                print(f"     - BTC quantity: {expected_btc} BTC")
            
        print(f"\n3. The problem might be in the balance API code...")
        print("   The API should be finding this config and calculating the 50/50 split")
        print("   But it's returning BTC: 0.0 instead")
        print("   This suggests there might be an exception in the balance calculation")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_bot_config()