#!/usr/bin/env python3
"""
Debug why BTC balance shows 0 instead of 50% allocation
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import asyncio
from app.models import BotConfig, Trade
from app.market import get_account_balance
from app.paper_trading_tracker import calculate_paper_performance
from sqlalchemy.orm import sessionmaker
from app.db import engine

async def debug_btc_zero_balance():
    print("="*80)
    print("DEBUGGING BTC ZERO BALANCE ISSUE")
    print("="*80)
    
    # Create session
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Get bot config
        config = db.query(BotConfig).first()
        if not config:
            print("❌ No bot config found")
            return
        
        user_id = config.user_id
        symbol = config.symbol
        budget = config.budget
        
        print(f"Config:")
        print(f"  Budget: ${budget:,.2f}")
        print(f"  Symbol: {symbol}")
        print(f"  Paper Trading: {config.paper_trading}")
        
        # Check for any existing trades
        all_trades = db.query(Trade).filter(
            Trade.user_id == user_id,
            Trade.symbol == symbol
        ).all()
        
        paper_trades = db.query(Trade).filter(
            Trade.user_id == user_id,
            Trade.symbol == symbol,
            Trade.status.in_(['completed_paper', 'simulated'])
        ).all()
        
        print(f"\nTrade Analysis:")
        print(f"  Total trades in DB: {len(all_trades)}")
        print(f"  Paper trades: {len(paper_trades)}")
        
        if all_trades:
            print(f"  Trade statuses: {set(t.status for t in all_trades)}")
            for i, trade in enumerate(all_trades[-3:]):  # Last 3 trades
                print(f"    {i+1}. {trade.side} {trade.amount} @ {trade.price} - Status: '{trade.status}'")
        
        # Test balance calculation step by step
        print(f"\n{'='*60}")
        print("STEP-BY-STEP BALANCE CALCULATION")
        print(f"{'='*60}")
        
        # Step 1: Performance calculation
        perf = calculate_paper_performance(user_id, symbol, 'gods_hand', db)
        
        print(f"1. Performance Calculation:")
        if perf:
            print(f"   Starting Balance: ${perf.get('starting_balance', 0):,.2f}")
            print(f"   Current Balance: ${perf.get('current_balance', 0):,.2f}")
            print(f"   Cash Balance: ${perf.get('cash_balance', 0):,.2f}")
            print(f"   Position Value: ${perf.get('position_value', 0):,.2f}")
            print(f"   Quantity Held: {perf.get('quantity_held', 0):,.8f}")
            print(f"   Total Trades: {perf.get('total_trades', 0)}")
        else:
            print("   ❌ Performance calculation returned None")
        
        # Step 2: Market balance calculation  
        print(f"\n2. Market Balance API:")
        balance = await get_account_balance(db, user_id, "USD")
        
        print(f"   Paper Trading: {balance.get('paper_trading', False)}")
        print(f"   Total Balance: ${balance.get('total_balance', 0):,.2f}")
        
        assets = balance.get('assets', [])
        print(f"   Assets found: {len(assets)}")
        
        for asset in assets:
            print(f"   {asset['asset']}:")
            print(f"     Free: {asset['free']:,.8f}")
            print(f"     Total: {asset['total']:,.8f}")
            print(f"     USD Value: ${asset['usd_value']:,.2f}")
        
        # Step 3: Current price check
        print(f"\n3. Current Price Check:")
        try:
            from app.market import get_current_price
            ticker = await get_current_price(symbol)
            current_price = ticker.get('last', 0)
            print(f"   Current BTC Price: ${current_price:,.2f}")
            
            if current_price > 0:
                expected_btc_quantity = (budget / 2) / current_price
                print(f"   Expected BTC Quantity: {expected_btc_quantity:.8f}")
            else:
                print(f"   ❌ Current price is 0 or invalid")
        except Exception as e:
            print(f"   ❌ Price fetch error: {e}")
        
        # Step 4: Root cause analysis
        print(f"\n{'='*60}")
        print("ROOT CAUSE ANALYSIS")
        print(f"{'='*60}")
        
        issues = []
        
        # Check if performance calculation has trades but balance API doesn't reflect them
        if perf and perf.get('total_trades', 0) > 0:
            if perf.get('cash_balance', 0) != budget / 2:
                issues.append("Performance shows trades but cash balance doesn't match expected 50%")
        
        # Check if balance API is showing wrong split
        usdt_asset = next((a for a in assets if a['asset'] == 'USDT'), None)
        btc_asset = next((a for a in assets if a['asset'] == 'BTC'), None)
        
        if usdt_asset and usdt_asset['usd_value'] > budget * 0.9:
            issues.append(f"USDT has {usdt_asset['usd_value']:.0f}% of budget - should be 50%")
        
        if btc_asset and btc_asset['total'] == 0:
            issues.append("BTC quantity is exactly 0 - should have some allocation")
        
        if not btc_asset:
            issues.append("BTC asset not found in balance response")
        
        # Check if there are trades with wrong status
        wrong_status_trades = [t for t in all_trades if t.status not in ['completed_paper', 'simulated']]
        if wrong_status_trades:
            issues.append(f"Found {len(wrong_status_trades)} trades with wrong status: {set(t.status for t in wrong_status_trades)}")
        
        print("Issues Found:")
        if issues:
            for issue in issues:
                print(f"❌ {issue}")
        else:
            print("✅ No obvious issues detected")
        
        # Step 5: Expected vs Actual comparison
        print(f"\n{'='*60}")
        print("EXPECTED VS ACTUAL")
        print(f"{'='*60}")
        
        expected_usdt = budget / 2
        expected_btc_value = budget / 2
        
        actual_usdt = usdt_asset['usd_value'] if usdt_asset else 0
        actual_btc_value = btc_asset['usd_value'] if btc_asset else 0
        
        print(f"Expected USDT: ${expected_usdt:,.2f}")
        print(f"Actual USDT: ${actual_usdt:,.2f}")
        print(f"Difference: ${actual_usdt - expected_usdt:,.2f}")
        
        print(f"\nExpected BTC Value: ${expected_btc_value:,.2f}")
        print(f"Actual BTC Value: ${actual_btc_value:,.2f}")
        print(f"Difference: ${actual_btc_value - expected_btc_value:,.2f}")
        
        if actual_btc_value == 0 and actual_usdt > budget * 0.9:
            print(f"\n🎯 ISSUE IDENTIFIED: 100% USDT, 0% BTC allocation")
            print(f"   This suggests the 50/50 split logic is not working")
            print(f"   All budget is in USDT, no BTC position exists")
    
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(debug_btc_zero_balance())