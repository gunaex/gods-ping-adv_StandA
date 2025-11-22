#!/usr/bin/env python3
"""
Test paper trading balance initialization with budget 28480
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import asyncio
from app.models import BotConfig
from app.market import get_account_balance
from sqlalchemy.orm import sessionmaker
from app.db import engine

async def test_paper_balance_28480():
    print("="*80)
    print("TESTING PAPER TRADING BALANCE WITH BUDGET 28,480")
    print("="*80)
    
    # Create session
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Get or create bot config with budget 28,480
        config = db.query(BotConfig).first()
        if config:
            print(f"Found existing config:")
            print(f"  Budget: ${config.budget:,.2f}")
            print(f"  Symbol: {config.symbol}")
            print(f"  Paper Trading: {config.paper_trading}")
            
            if config.budget != 28480:
                print(f"\nUpdating budget from ${config.budget:,.2f} to $28,480")
                config.budget = 28480
                config.paper_trading = True
                db.commit()
                print("✅ Budget updated")
        else:
            print("❌ No bot config found")
            db.close()
            return
        
        print(f"\n{'='*50}")
        print("TESTING BALANCE CALCULATION")
        print(f"{'='*50}")
        
        # Test balance calculation
        balance = await get_account_balance(db, config.user_id, "USD")
        
        print(f"Paper Trading Mode: {balance.get('paper_trading', False)}")
        print(f"Total Balance: ${balance.get('total_balance', 0):,.2f}")
        print(f"Available Balance: ${balance.get('available_balance', 0):,.2f}")
        
        print(f"\nAssets:")
        assets = balance.get('assets', [])
        for asset in assets:
            print(f"  {asset['asset']}:")
            print(f"    Free: {asset['free']:,.8f}")
            print(f"    Total: {asset['total']:,.8f}")
            print(f"    USD Value: ${asset['usd_value']:,.2f}")
        
        # Expected values for 28,480 budget
        print(f"\n{'='*50}")
        print("EXPECTED VS ACTUAL")
        print(f"{'='*50}")
        
        expected_usdt = 28480 / 2  # Should be $14,240
        expected_btc_value = 28480 / 2  # Should be $14,240 worth of BTC
        
        print(f"Expected USDT: ${expected_usdt:,.2f}")
        print(f"Expected BTC Value: ${expected_btc_value:,.2f}")
        print(f"Expected Total: ${28480:,.2f}")
        
        # Find actual values
        usdt_asset = next((a for a in assets if a['asset'] == 'USDT'), None)
        btc_asset = next((a for a in assets if a['asset'] == 'BTC'), None)
        
        if usdt_asset:
            actual_usdt = usdt_asset['usd_value']
            print(f"Actual USDT: ${actual_usdt:,.2f}")
            usdt_diff = actual_usdt - expected_usdt
            print(f"USDT Difference: ${usdt_diff:,.2f}")
        else:
            print("❌ USDT asset not found!")
        
        if btc_asset:
            actual_btc_value = btc_asset['usd_value']
            print(f"Actual BTC Value: ${actual_btc_value:,.2f}")
            btc_diff = actual_btc_value - expected_btc_value
            print(f"BTC Difference: ${btc_diff:,.2f}")
        else:
            print("❌ BTC asset not found!")
        
        actual_total = balance.get('total_balance', 0)
        total_diff = actual_total - 28480
        print(f"Actual Total: ${actual_total:,.2f}")
        print(f"Total Difference: ${total_diff:,.2f}")
        
        # Analysis
        print(f"\n{'='*50}")
        print("ISSUE ANALYSIS")
        print(f"{'='*50}")
        
        if abs(total_diff) > 1:  # Allow $1 tolerance for rounding
            print("❌ ISSUE FOUND: Total balance doesn't match budget")
            print("Possible causes:")
            print("1. Split calculation error (should be budget/2 each)")
            print("2. Price fetching issue affecting BTC portion")
            print("3. Exchange rate conversion problem")
        else:
            print("✅ Total balance matches budget")
        
        if usdt_asset and abs(usdt_asset['usd_value'] - expected_usdt) > 1:
            print("❌ USDT ISSUE: USDT balance incorrect")
            print("Should be exactly budget/2 = $14,240")
        else:
            print("✅ USDT balance correct")
        
        if btc_asset and abs(btc_asset['usd_value'] - expected_btc_value) > 1:
            print("❌ BTC ISSUE: BTC value incorrect")
            print("Should be budget/2 worth of BTC at current price")
        else:
            print("✅ BTC value correct")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_paper_balance_28480())