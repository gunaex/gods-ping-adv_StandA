#!/usr/bin/env python3
"""Test current system status and SELL execution readiness"""

import os
import sys

# Add the backend path to sys.path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from app.db import SessionLocal
from app.main import init_db
from app.models import Trade
from app.position_tracker import get_current_position, calculate_incremental_amount
from app.market import get_account_balance

def test_system_status():
    print("=== SYSTEM STATUS TEST ===\n")
    
    # Initialize database
    init_db()
    
    with SessionLocal() as db:
        # Check trades
        trades = db.query(Trade).filter(Trade.symbol == "BTCUSDT").all()
        print(f"Current trades count: {len(trades)}")
        
        if trades:
            for trade in trades:
                print(f"- Trade ID {trade.id}: {trade.side} {trade.quantity} BTC at ${trade.price}")
        else:
            print("- No trades found")
        
        print()
        
        # Check position (assume user_id = 1 for admin)
        current_position = get_current_position(1, "BTCUSDT", db)
        
        print(f"Current Position:")
        print(f"- Quantity: {current_position['quantity']}")
        print(f"- Average Price: ${current_position['average_price']:.2f}")
        print(f"- Cost Basis: ${current_position['cost_basis']:.2f}")
        print(f"- Paper Initial: {current_position.get('_paper_initial', False)}")
        print(f"- Budget: ${current_position.get('_budget', 0):.2f}")
        print()
        
        # Check bot config
        from app.models import BotConfig
        config = db.query(BotConfig).filter(BotConfig.user_id == 1).first()
        if config:
            print(f"Bot Config:")
            print(f"- Paper Trading: {config.paper_trading}")
            print(f"- Budget: ${config.budget:.2f}")
            print(f"- Symbol: {config.symbol}")
            print()
        else:
            print("❌ No bot config found for user_id=1")
            print()
        
        # Check balance (only if config exists)
        if config:
            balance = get_account_balance(1, "paper")
            print(f"Account Balance:")
            for asset in balance.get('balances', []):
                print(f"- {asset['asset']}: {asset['free']} (${asset['usd_value']:.2f})")
            print()
        else:
            print("Skipping balance check - no config found")
            print()
        
        # Test SELL execution readiness
        print("=== SELL EXECUTION TEST ===")
        
        # Check if we can execute a SELL
        if current_position['quantity'] > 0:
            print("✅ Position exists - SELL should be possible")
            
            # Calculate incremental amount
            incremental_amount = calculate_incremental_amount(
                1, "BTCUSDT", "SELL", current_position, db
            )
            
            print(f"Incremental SELL amount: {incremental_amount} BTC")
            print(f"This is {(incremental_amount / current_position['quantity']) * 100:.1f}% of position")
            
        else:
            print("❌ No position exists - SELL not possible")
            if current_position.get('_paper_initial', False):
                print("📋 Paper trading in initial state (50/50 split)")
                
        print("\n=== RECOMMENDATION ===")
        if current_position.get('_paper_initial', False):
            print("System is in paper trading initial state.")
            print("Backend should show 50/50 balance split.")
            print("Gods Hand should be able to execute BUY or SELL trades.")
        elif current_position['quantity'] > 0:
            print("System has active position - SELL trades should work.")
        else:
            print("System has no position - only BUY trades should work.")

if __name__ == "__main__":
    test_system_status()