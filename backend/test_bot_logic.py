"""Test the exact code path that bots.py uses"""
import asyncio
from app.db import SessionLocal
from app.position_tracker import get_current_position
from app.models import BotConfig

async def test_bot_position():
    db = SessionLocal()
    try:
        config = db.query(BotConfig).filter(BotConfig.user_id == 1).first()
        
        print("\n" + "="*60)
        print("TESTING BOT POSITION LOGIC")
        print("="*60)
        
        # Step 1: Get position (same as bots.py line 242)
        current_position = get_current_position(1, 'BTC/USDT', db)
        
        print("1. Raw position from get_current_position():")
        print(f"   Quantity: {current_position.get('quantity', 0):.8f}")
        print(f"   Cost basis: ${current_position.get('cost_basis', 0):,.2f}")
        print(f"   Position value: ${current_position.get('position_value_usd', 0):,.2f}")
        print(f"   Paper initial flag: {current_position.get('_paper_initial', False)}")
        
        # Step 2: Apply paper trading logic (same as bots.py lines 244-255)
        if current_position.get('_paper_initial'):
            budget = current_position.get('_budget', config.budget)
            
            # Get current price (simulate)
            current_price = 95200.0  # Simulate current price
            
            print(f"\n2. Applying 50/50 split logic:")
            print(f"   Budget: ${budget:,.2f}")
            print(f"   Current price: ${current_price:,.2f}")
            
            # Start with 50% in BTC, 50% in USDT
            current_position['quantity'] = (budget / 2) / current_price
            current_position['cost_basis'] = budget / 2
            current_position['average_price'] = current_price
            current_position['position_value_usd'] = budget / 2
            current_position['trades_count'] = 0
            
            # Remove the flags
            if '_paper_initial' in current_position:
                del current_position['_paper_initial']
            if '_budget' in current_position:
                del current_position['_budget']
            
            print(f"   Modified quantity: {current_position['quantity']:.8f}")
            print(f"   Modified cost basis: ${current_position['cost_basis']:,.2f}")
            print(f"   Modified position value: ${current_position['position_value_usd']:,.2f}")
        
        # Step 3: Test incremental calculation
        from app.position_tracker import calculate_incremental_amount
        
        max_position_size = config.budget  # Same as risk assessment max
        step_percent = config.exit_step_percent  # 10%
        action = 'SELL'
        
        print(f"\n3. Testing incremental calculation for SELL:")
        print(f"   Max position size: ${max_position_size:,.2f}")
        print(f"   Step percent: {step_percent}%")
        print(f"   Action: {action}")
        
        incremental_calc = calculate_incremental_amount(
            current_position,
            max_position_size,
            step_percent,
            action
        )
        
        print(f"\nIncremental calculation result:")
        print(f"   Can execute: {incremental_calc['can_execute']}")
        print(f"   Step amount USD: ${incremental_calc['step_amount_usd']:,.2f}")
        print(f"   Current fill %: {incremental_calc['current_fill_percent']:.1f}%")
        print(f"   After fill %: {incremental_calc['after_fill_percent']:.1f}%")
        print(f"   Reason: {incremental_calc['reason']}")
        
        print("\n" + "="*60)
        
    finally:
        db.close()

asyncio.run(test_bot_position())