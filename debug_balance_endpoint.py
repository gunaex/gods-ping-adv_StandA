#!/usr/bin/env python3
"""
Add temporary debug logging to the balance API to see what's happening
"""

# First, let's create a simple debug endpoint we can add to the API
debug_balance_code = '''
@app.get("/api/debug/balance")
async def debug_balance(
    fiat_currency: str = "USD",
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Debug version of balance API with detailed logging"""
    from app.market import get_current_price
    from app.models import BotConfig, User
    from app.paper_trading_tracker import calculate_paper_performance
    
    debug_info = {"steps": []}
    
    try:
        user_id = current_user['id']
        debug_info["user_id"] = user_id
        debug_info["steps"].append("Got user ID")
        
        # Check if paper trading mode
        config = db.query(BotConfig).filter(BotConfig.user_id == user_id).first()
        if not config:
            debug_info["error"] = "No bot config found"
            return debug_info
            
        debug_info["config"] = {
            "budget": config.budget,
            "symbol": config.symbol,
            "paper_trading": config.paper_trading
        }
        debug_info["steps"].append("Got bot config")
        
        if config and config.paper_trading:
            budget = config.budget
            symbol = config.symbol
            
            # Parse symbol
            try:
                base_currency, quote_currency = symbol.split('/')
                debug_info["currencies"] = {"base": base_currency, "quote": quote_currency}
                debug_info["steps"].append("Parsed symbol")
            except Exception as e:
                base_currency, quote_currency = "BTC", "USDT"
                debug_info["currencies"] = {"base": base_currency, "quote": quote_currency}
                debug_info["steps"].append(f"Symbol parse failed, using defaults: {str(e)}")
            
            # Get current price
            try:
                ticker = await get_current_price(symbol)
                current_price = ticker.get('last', 0)
                debug_info["price_fetch"] = {"ticker": ticker, "current_price": current_price}
                
                if current_price == 0:
                    current_price = 42000.0
                    debug_info["steps"].append("Used fallback price (ticker returned 0)")
                else:
                    debug_info["steps"].append("Got valid price from ticker")
            except Exception as e:
                current_price = 42000.0
                debug_info["price_fetch"] = {"error": str(e), "current_price": current_price}
                debug_info["steps"].append(f"Price fetch failed, using fallback: {str(e)}")
            
            debug_info["final_current_price"] = current_price
            
            # Calculate performance
            try:
                perf = calculate_paper_performance(user_id, symbol, 'gods_hand', db)
                debug_info["performance"] = perf
                debug_info["steps"].append("Got performance calculation")
            except Exception as e:
                debug_info["performance"] = {"error": str(e)}
                debug_info["steps"].append(f"Performance calculation failed: {str(e)}")
                perf = None
            
            # Balance calculation logic
            if perf:
                debug_info["steps"].append("Performance data available")
                
                total_trades = perf.get('total_trades', 0)
                debug_info["total_trades"] = total_trades
                
                if total_trades > 0:
                    debug_info["steps"].append("Has trading history - using actual position")
                    quantity_held = perf.get('quantity_held', 0)
                    cash_balance = perf.get('cash_balance', budget / 2)
                    position_value = quantity_held * current_price if quantity_held > 0 else 0
                else:
                    debug_info["steps"].append("No trades - using 50/50 split from performance")
                    cash_balance = perf.get('cash_balance', budget / 2)
                    position_value = perf.get('position_value', budget / 2)
                    quantity_held = position_value / current_price if current_price > 0 else 0
                    
            else:
                debug_info["steps"].append("No performance data - using fallback calculation")
                quantity_held = (budget / 2) / current_price
                cash_balance = budget / 2
                position_value = budget / 2
            
            debug_info["final_calculation"] = {
                "quantity_held": quantity_held,
                "cash_balance": cash_balance, 
                "position_value": position_value,
                "total_balance": cash_balance + position_value
            }
            
            # Build assets
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
            
            debug_info["assets"] = assets
            debug_info["steps"].append("Built assets array")
            
            return debug_info
        else:
            debug_info["error"] = "Not in paper trading mode or no config"
            return debug_info
            
    except Exception as e:
        debug_info["error"] = str(e)
        import traceback
        debug_info["traceback"] = traceback.format_exc()
        return debug_info
'''

print("Debug Balance API Code:")
print("="*60)
print("Add this to backend/app/main.py to debug the balance calculation:")
print(debug_balance_code)
print("\n" + "="*60)
print("Then call: GET /api/debug/balance")
print("This will show exactly what's happening in the balance calculation.")