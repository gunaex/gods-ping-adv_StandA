#!/usr/bin/env python3
"""
Replicate the exact balance API calculation step by step to find the issue
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.models import BotConfig, User
from app.paper_trading_tracker import calculate_paper_performance
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def replicate_api_balance():
    print("="*80)
    print("REPLICATING EXACT BALANCE API CALCULATION")
    print("="*80)
    
    # Setup database exactly like the API
    engine = create_engine("sqlite:///gods_ping.db", echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        user_id = 1
        fiat_currency = "USD"
        
        print(f"1. API Step: Get exchange rate")
        # get_exchange_rate(fiat_currency) - simplified
        exchange_rate = 1.0 if fiat_currency == "USD" else 1.0
        print(f"   exchange_rate: {exchange_rate}")
        
        print(f"\n2. API Step: Get BotConfig")
        config = db.query(BotConfig).filter(BotConfig.user_id == user_id).first()
        
        if not config:
            print("   ❌ No config found - this would cause issues!")
            return
            
        print(f"   ✅ Config found:")
        print(f"     budget: {config.budget}")
        print(f"     symbol: {config.symbol}")
        print(f"     paper_trading: {config.paper_trading}")
        
        print(f"\n3. API Step: Check if paper trading")
        if config and config.paper_trading:
            print("   ✅ In paper trading mode - should use 50/50 logic")
            
            budget = config.budget
            symbol = config.symbol
            
            print(f"\n4. API Step: Parse symbol")
            try:
                base_currency, quote_currency = symbol.split('/')
            except:
                base_currency, quote_currency = "BTC", "USDT"
            
            print(f"   base_currency: {base_currency}")
            print(f"   quote_currency: {quote_currency}")
            
            print(f"\n5. API Step: Get current price")
            # Simulate get_current_price - we know this works
            current_price = 92240.17
            print(f"   current_price: {current_price}")
            
            print(f"\n6. API Step: Calculate paper performance")
            perf = calculate_paper_performance(user_id, symbol, 'gods_hand', db)
            
            if perf:
                print("   ✅ Performance calculation successful")
                total_trades = perf.get('total_trades', 0)
                print(f"   total_trades: {total_trades}")
                
                if total_trades > 0:
                    print("   API Path: Using actual position from trades")
                    quantity_held = perf.get('quantity_held', 0)
                    cash_balance = perf.get('cash_balance', budget / 2)
                    position_value = quantity_held * current_price if quantity_held > 0 else 0
                else:
                    print("   API Path: Using 50/50 split from performance")
                    cash_balance = perf.get('cash_balance', budget / 2)
                    position_value = perf.get('position_value', budget / 2)
                    quantity_held = position_value / current_price if current_price > 0 else 0
                    
            else:
                print("   ❌ Performance calculation failed - using fallback")
                quantity_held = (budget / 2) / current_price
                cash_balance = budget / 2
                position_value = budget / 2
            
            print(f"\n7. API Step: Final calculations")
            print(f"   quantity_held: {quantity_held}")
            print(f"   cash_balance: {cash_balance}")
            print(f"   position_value: {position_value}")
            
            print(f"\n8. API Step: Build assets array")
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
            
            for asset in assets:
                print(f"   {asset['asset']}: {asset['free']} (${asset['usd_value']})")
            
            total_balance = cash_balance + position_value
            
            print(f"\n9. API Step: Build final response")
            result = {
                "total_balance": total_balance * exchange_rate,
                "available_balance": total_balance * exchange_rate,
                "in_orders": 0,
                "total_pnl": 0,
                "total_pnl_percentage": 0,
                "daily_pnl": 0,
                "daily_pnl_percentage": 0,
                "assets": [
                    {
                        **asset,
                        "usd_value": asset["usd_value"] * exchange_rate
                    }
                    for asset in assets
                ],
                "fiat_currency": fiat_currency,
                "exchange_rate": exchange_rate,
                "paper_trading": True
            }
            
            print(f"   Final result:")
            print(f"     total_balance: {result['total_balance']}")
            print(f"     BTC free: {result['assets'][1]['free']}")
            print(f"     USDT free: {result['assets'][0]['free']}")
            
            print(f"\n10. Comparison with actual API:")
            print(f"     Expected BTC: {result['assets'][1]['free']}")
            print(f"     Actual API BTC: 0.0")
            print(f"     Expected USDT: {result['assets'][0]['free']}")
            print(f"     Actual API USDT: 28482.0")
            
            if result['assets'][1]['free'] > 0 and result['assets'][0]['free'] == 14240.0:
                print("   ✅ Our calculation is correct - API has a bug!")
            else:
                print("   ❌ Our calculation has an issue")
                
        else:
            print("   ❌ Not in paper trading mode or no config")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    replicate_api_balance()