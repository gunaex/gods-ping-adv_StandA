import asyncio
import json
from sqlalchemy.orm import sessionmaker
from app.db import engine
from app.models import BotConfig
from app.position_tracker import get_current_position, calculate_incremental_amount
from app.market import get_current_price

Session = sessionmaker(bind=engine)

def cents(x):
    try:
        return float(x)
    except:
        return 0.0

async def main():
    s = Session()
    try:
        config = s.query(BotConfig).first()
        if not config:
            print('No BotConfig found')
            return
        user_id = config.user_id
        symbol = config.symbol
        print('Config:')
        print(json.dumps({
            'user_id': user_id,
            'symbol': symbol,
            'budget': config.budget,
            'position_size_ratio': config.position_size_ratio,
            'entry_step_percent': config.entry_step_percent,
            'exit_step_percent': config.exit_step_percent
        }, indent=2))

        current_position = get_current_position(user_id, symbol, s)
        print('\nCurrent Position:')
        print(json.dumps(current_position, indent=2))

        # Fetch live price
        try:
            ticker = await get_current_price(symbol)
            current_price = ticker.get('last')
        except Exception as e:
            current_price = current_position.get('average_price') or 0.0
        print('\nCurrent price used: ', current_price)

        # Compute max_position_size from config
        max_pos = config.budget * config.position_size_ratio

        print('\n--- Incremental Calculation (using current config) ---')
        buy_calc = calculate_incremental_amount(current_position, max_pos, config.entry_step_percent, 'BUY')
        sell_calc = calculate_incremental_amount(current_position, max_pos, config.exit_step_percent, 'SELL')

        # For buy, convert USD step to crypto amount using current_price
        buy_crypto = buy_calc['step_amount_usd'] / current_price if current_price > 0 else 0.0
        # For sell, crypto amount = current_position.quantity * (exit_step_percent/100)
        sell_crypto = current_position.get('quantity', 0.0) * (config.exit_step_percent / 100.0)

        print('\nBUY step:')
        print(json.dumps(buy_calc, indent=2))
        print(f" -> BUY crypto amount (approx): {buy_crypto:.8f} {symbol.split('/')[0]}")

        print('\nSELL step:')
        print(json.dumps(sell_calc, indent=2))
        print(f" -> SELL crypto amount: {sell_crypto:.8f} {symbol.split('/')[0]}")

        # Example with user's desired 95% max and budget example
        print('\n--- Example: budget=20000, position_size_ratio=0.95, step=10% ---')
        example_budget = 20000.0
        example_pos_ratio = 0.95
        example_step = 10.0
        example_max_pos = example_budget * example_pos_ratio
        example_current_position = {
            'symbol': 'BTC/USDT',
            'quantity': 0.10,
            'cost_basis': 0.0,
            'average_price': current_price if current_price else 0.0,
            'total_fees_paid': 0.0,
            'position_value_usd': 0.10 * (current_price or 0.0),
            'trades_count': 1
        }
        ex_buy = calculate_incremental_amount(example_current_position, example_max_pos, example_step, 'BUY')
        ex_sell = calculate_incremental_amount(example_current_position, example_max_pos, example_step, 'SELL')
        ex_buy_crypto = ex_buy['step_amount_usd'] / (current_price or 1)
        ex_sell_crypto = example_current_position['quantity'] * (example_step / 100.0)
        print('Example max position (USD):', example_max_pos)
        print('\nExample BUY step (USD):')
        print(json.dumps(ex_buy, indent=2))
        print(f' -> BUY crypto amount (approx): {ex_buy_crypto:.8f} BTC')
        print('\nExample SELL step (USD):')
        print(json.dumps(ex_sell, indent=2))
        print(f' -> SELL crypto amount: {ex_sell_crypto:.8f} BTC')

    finally:
        s.close()

if __name__ == '__main__':
    asyncio.run(main())
