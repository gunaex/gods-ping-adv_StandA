#!/usr/bin/env python3
"""
Debug the exact paper trading calculation used by the balance API
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.paper_trading_tracker import calculate_paper_performance
from app.models import BotConfig
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def debug_api_paper_calculation():
    print("="*80)
    print("DEBUGGING ACTUAL API PAPER TRADING CALCULATION")
    print("="*80)
    
    # Setup database connection
    engine = create_engine("sqlite:///gods_ping.db", echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Get user ID 1 (Admin)
        user_id = 1
        
        print(f"1. Getting BotConfig for user {user_id}...")
        config = db.query(BotConfig).filter(BotConfig.user_id == user_id).first()
        
        if not config:
            print("   ❌ No BotConfig found!")
            return
        
        print(f"   ✅ Found BotConfig:")
        print(f"     - Budget: ${config.budget}")
        print(f"     - Symbol: {config.symbol}")
        print(f"     - Paper Trading: {config.paper_trading}")
        
        print(f"\n2. Calling calculate_paper_performance with same parameters as API...")
        
        # This is the exact call the API makes
        perf = calculate_paper_performance(user_id, config.symbol, 'gods_hand', db)
        
        print(f"   Performance calculation result:")
        if perf:
            print(f"   ✅ Performance found:")
            for key, value in perf.items():
                print(f"     - {key}: {value}")
                
            # Check the specific values the API uses
            total_trades = perf.get('total_trades', 0)
            quantity_held = perf.get('quantity_held', 0)
            cash_balance = perf.get('cash_balance', config.budget / 2)
            position_value = perf.get('position_value', config.budget / 2)
            
            print(f"\n   Values that API will use:")
            print(f"     - Total trades: {total_trades}")
            print(f"     - Quantity held (BTC): {quantity_held}")
            print(f"     - Cash balance (USDT): {cash_balance}")
            print(f"     - Position value (USD): {position_value}")
            
            # Check the condition
            if total_trades > 0:
                print(f"\n   ✅ Has trading history - using actual position")
            else:
                print(f"\n   ⚠️  No trading history - should use 50/50 split from perf")
                
        else:
            print("   ❌ Performance calculation returned None!")
            
        print(f"\n3. Simulating the exact API balance calculation...")
        
        # This is exactly what the API does
        budget = config.budget
        symbol = config.symbol
        
        # Parse symbol
        try:
            base_currency, quote_currency = symbol.split('/')
        except:
            base_currency, quote_currency = "BTC", "USDT"
            
        print(f"   - Base currency: {base_currency}")
        print(f"   - Quote currency: {quote_currency}")
        print(f"   - Budget: ${budget}")
        
        # Current price (fallback)
        current_price = 42000.0  # API uses this as fallback
        print(f"   - Current price (fallback): ${current_price}")
        
        if perf:
            if perf.get('total_trades', 0) > 0:
                print(f"   API Path: Using actual position from trades")
                quantity_held = perf.get('quantity_held', 0)
                cash_balance = perf.get('cash_balance', budget / 2)
                position_value = quantity_held * current_price if quantity_held > 0 else 0
            else:
                print(f"   API Path: Using 50/50 split from performance calculation")
                cash_balance = perf.get('cash_balance', budget / 2)
                position_value = perf.get('position_value', budget / 2)
                quantity_held = position_value / current_price if current_price > 0 else 0
        else:
            print(f"   API Path: Fallback calculation")
            quantity_held = (budget / 2) / current_price
            cash_balance = budget / 2
            position_value = budget / 2
            
        print(f"\n   Final API calculations:")
        print(f"     - Quantity held (BTC): {quantity_held}")
        print(f"     - Cash balance (USDT): {cash_balance}")
        print(f"     - Position value (USD): ${position_value}")
        print(f"     - Total balance: ${cash_balance + position_value}")
        
        # Build the assets as the API does
        assets = [
            {
                "asset": quote_currency,
                "free": cash_balance,
                "locked": 0.0,
                "total": cash_balance,
                "usd_value": cash_balance,
            },
            {
                "asset": base_currency,
                "free": quantity_held,
                "locked": 0.0,
                "total": quantity_held,
                "usd_value": position_value,
            }
        ]
        
        print(f"\n   Final assets that API returns:")
        for asset in assets:
            print(f"     - {asset['asset']}: {asset['free']} (${asset['usd_value']})")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_api_paper_calculation()