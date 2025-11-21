#!/usr/bin/env python3
"""
Test the paper performance calculation in different contexts
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.paper_trading_tracker import calculate_paper_performance
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def test_performance_calculation():
    print("="*80)
    print("TESTING PAPER PERFORMANCE CALCULATION")
    print("="*80)
    
    # Setup database connection exactly like the API
    engine = create_engine("sqlite:///gods_ping.db", echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        user_id = 1
        symbol = "BTC/USDT"
        bot_type = "gods_hand"
        
        print(f"1. Calling calculate_paper_performance({user_id}, '{symbol}', '{bot_type}', db)...")
        
        # This is the exact call the balance API makes
        perf = calculate_paper_performance(user_id, symbol, bot_type, db)
        
        print(f"2. Performance result:")
        if perf is None:
            print("   ❌ Performance calculation returned None!")
            return
        
        print("   ✅ Performance calculation successful:")
        for key, value in perf.items():
            print(f"     {key}: {value}")
        
        print(f"\n3. Key values for balance calculation:")
        total_trades = perf.get('total_trades', 0)
        quantity_held = perf.get('quantity_held', 0)
        cash_balance = perf.get('cash_balance', 0)
        position_value = perf.get('position_value', 0)
        
        print(f"   total_trades: {total_trades}")
        print(f"   quantity_held: {quantity_held}")
        print(f"   cash_balance: {cash_balance}")
        print(f"   position_value: {position_value}")
        
        print(f"\n4. Balance API logic simulation:")
        budget = 28480.0  # From our config check
        current_price = 92240.17  # From our price test
        
        if total_trades > 0:
            print("   API would use: actual position from trades")
            api_quantity = quantity_held
            api_cash = cash_balance  
            api_position_value = quantity_held * current_price if quantity_held > 0 else 0
        else:
            print("   API would use: 50/50 split from performance calculation")
            api_cash = perf.get('cash_balance', budget / 2)
            api_position_value = perf.get('position_value', budget / 2) 
            api_quantity = api_position_value / current_price if current_price > 0 else 0
        
        print(f"   API calculations:")
        print(f"     quantity_held (BTC): {api_quantity}")
        print(f"     cash_balance (USDT): {api_cash}")
        print(f"     position_value (USD): {api_position_value}")
        
        print(f"\n5. Expected vs Actual API response:")
        print(f"   Expected USDT: {api_cash}")
        print(f"   Expected BTC: {api_quantity}")
        print(f"   Actual API USDT: 28482.0")
        print(f"   Actual API BTC: 0.0")
        
        if abs(api_cash - 28482.0) > 10:
            print("   ❌ USDT values don't match - performance calculation issue")
        else:
            print("   ✅ USDT values roughly match")
            
        if api_quantity == 0.0:
            print("   ❌ BTC quantity is 0 - this explains the frontend issue!")
        else:
            print("   ✅ BTC quantity is non-zero - API should show this")
    
    except Exception as e:
        print(f"   ❌ Error in performance calculation: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_performance_calculation()