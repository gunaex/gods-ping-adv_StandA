#!/usr/bin/env python3
"""
Test paper trading balance with existing trades to identify USDT balance issue
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
from datetime import datetime

async def test_paper_balance_with_trades():
    print("="*80)
    print("TESTING PAPER TRADING BALANCE WITH TRADES - USDT ISSUE DEBUG")
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
        
        print(f"Config: Budget=${budget:,.2f}, Symbol={symbol}, Paper Trading={config.paper_trading}")
        
        # Check existing trades
        trades = db.query(Trade).filter(
            Trade.user_id == user_id,
            Trade.symbol == symbol
        ).all()
        
        print(f"\nExisting trades: {len(trades)}")
        for i, trade in enumerate(trades[-5:]):  # Show last 5
            print(f"  {i+1}. {trade.side} {trade.amount} @ {trade.price} - Status: {trade.status}")
        
        print(f"\n{'='*50}")
        print("TESTING BALANCE CALCULATION - NO TRADES SCENARIO")
        print(f"{'='*50}")
        
        # Test 1: Balance with no paper trades (fresh start)
        balance_no_trades = await get_account_balance(db, user_id, "USD")
        print(f"Paper Trading: {balance_no_trades.get('paper_trading', False)}")
        print(f"Total Balance: ${balance_no_trades.get('total_balance', 0):,.2f}")
        
        usdt_no_trades = next((a for a in balance_no_trades.get('assets', []) if a['asset'] == 'USDT'), None)
        btc_no_trades = next((a for a in balance_no_trades.get('assets', []) if a['asset'] == 'BTC'), None)
        
        print("Assets (no trades scenario):")
        if usdt_no_trades:
            print(f"  USDT: {usdt_no_trades['total']:,.2f} (${usdt_no_trades['usd_value']:,.2f})")
        if btc_no_trades:
            print(f"  BTC: {btc_no_trades['total']:,.8f} (${btc_no_trades['usd_value']:,.2f})")
        
        print(f"\n{'='*50}")
        print("TESTING PAPER PERFORMANCE CALCULATION")
        print(f"{'='*50}")
        
        # Test 2: Paper performance calculation
        perf = calculate_paper_performance(user_id, symbol, 'gods_hand', db)
        if perf:
            print(f"Performance calculation:")
            print(f"  Starting Balance: ${perf.get('starting_balance', 0):,.2f}")
            print(f"  Current Balance: ${perf.get('current_balance', 0):,.2f}")
            print(f"  Cash Balance: ${perf.get('cash_balance', 0):,.2f}")
            print(f"  Position Value: ${perf.get('position_value', 0):,.2f}")
            print(f"  Quantity Held: {perf.get('quantity_held', 0):,.8f}")
            print(f"  Total Trades: {perf.get('total_trades', 0)}")
            print(f"  Total P/L: ${perf.get('total_pl', 0):,.2f}")
        else:
            print("❌ No performance data")
        
        print(f"\n{'='*50}")
        print("ANALYZING POTENTIAL USDT ISSUES")
        print(f"{'='*50}")
        
        # Common issues analysis
        issues_found = []
        
        # Issue 1: Check if USDT balance doesn't match expected 50% split
        if usdt_no_trades:
            expected_usdt = budget / 2
            actual_usdt = usdt_no_trades['usd_value']
            if abs(actual_usdt - expected_usdt) > 1:
                issues_found.append(f"USDT balance mismatch: Expected ${expected_usdt:,.2f}, Got ${actual_usdt:,.2f}")
        
        # Issue 2: Check if free vs total USDT differs
        if usdt_no_trades:
            if usdt_no_trades['free'] != usdt_no_trades['total']:
                issues_found.append(f"USDT free vs total mismatch: Free={usdt_no_trades['free']}, Total={usdt_no_trades['total']}")
        
        # Issue 3: Check if performance calculation differs from balance API
        if perf and usdt_no_trades:
            perf_cash = perf.get('cash_balance', 0)
            api_usdt = usdt_no_trades['total']
            if abs(perf_cash - api_usdt) > 1:
                issues_found.append(f"Performance vs API USDT mismatch: Perf=${perf_cash:,.2f}, API=${api_usdt:,.2f}")
        
        # Issue 4: Check for trades with incorrect status filtering
        paper_trades = db.query(Trade).filter(
            Trade.user_id == user_id,
            Trade.symbol == symbol,
            Trade.status.in_(['completed_paper', 'simulated'])
        ).all()
        
        all_trades = db.query(Trade).filter(
            Trade.user_id == user_id,
            Trade.symbol == symbol
        ).all()
        
        if len(paper_trades) != len([t for t in all_trades if t.status in ['completed_paper', 'simulated']]):
            issues_found.append("Trade status filtering issue - some paper trades may have wrong status")
        
        print("Issues Analysis:")
        if issues_found:
            for issue in issues_found:
                print(f"❌ {issue}")
        else:
            print("✅ No obvious issues detected")
        
        print(f"\n{'='*50}")
        print("FRONTEND DISPLAY TEST")
        print(f"{'='*50}")
        
        # Test what the frontend would show
        if balance_no_trades.get('assets'):
            assets = balance_no_trades['assets']
            base_currency, quote_currency = symbol.split('/')
            
            baseAsset = next((a for a in assets if a['asset'] == base_currency), None)
            quoteAsset = next((a for a in assets if a['asset'] == quote_currency), None)
            
            print("Frontend would display:")
            if baseAsset:
                print(f"  {base_currency}: {baseAsset['total']:.8f} (Free: {baseAsset['free']:.8f})")
            else:
                print(f"  {base_currency}: 0.00000000")
            
            if quoteAsset:
                print(f"  {quote_currency}: {quoteAsset['total']:.2f} (Free: {quoteAsset['free']:.2f})")
            else:
                print(f"  {quote_currency}: 0.00")
        
        print(f"\nBudget display: ${config.budget:.2f}")
        print(f"Mode: {'📝 PAPER' if config.paper_trading else '💰 REAL'}")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_paper_balance_with_trades())