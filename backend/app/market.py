"""
Market Data Service
Real-time crypto market data via Binance Thailand native client
"""
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models import User
from app.auth import decrypt_api_key
from app.binance_client import get_binance_th_client, get_market_data_client
import asyncio


# Market data client (no auth, cached)
market_client = get_market_data_client()


async def get_account_balance(db: Session, user_id: int, fiat_currency: str = "USD") -> dict:
    """Get account balance and P/L from Binance TH or paper trading simulation"""
    from app.models import BotConfig, Trade
    from app.paper_trading_tracker import calculate_paper_performance
    
    # Get exchange rate
    exchange_rate = get_exchange_rate(fiat_currency)
    
    # Check if paper trading mode
    config = db.query(BotConfig).filter(BotConfig.user_id == user_id).first()
    if config and config.paper_trading:
        # PAPER TRADING MODE: Simulate balance with budget split between base and quote currency
        budget = config.budget
        symbol = config.symbol
        
        # Parse symbol (e.g., "BTC/USDT" -> "BTC", "USDT")
        try:
            base_currency, quote_currency = symbol.split('/')
        except:
            base_currency, quote_currency = "BTC", "USDT"
        
        # Get current price for base currency
        try:
            ticker = await get_current_price(symbol)
            current_price = ticker.get('last', 0)
            if current_price == 0:
                current_price = 0.0  # No fallback to fake prices
        except Exception as e:
            current_price = 0.0  # No fallback to fake prices
        
        # Calculate paper trading performance to get actual position
        perf = calculate_paper_performance(user_id, symbol, 'gods_hand', db, current_price=current_price)
        
        if perf:
            if perf.get('total_trades', 0) > 0:
                # User has trading history - show actual position from trades
                quantity_held = perf.get('quantity_held', 0)
                cash_balance = perf.get('cash_balance', budget / 2)
                position_value = quantity_held * current_price if quantity_held > 0 else 0
            else:
                # No trades yet - use the 50/50 split from performance calculation
                # This ensures consistency between balance API and performance tracker
                cash_balance = perf.get('cash_balance', budget / 2)  # Use perf calculation
                position_value = perf.get('position_value', budget / 2)  # Use perf calculation
                quantity_held = position_value / current_price if current_price > 0 else 0
        else:
            # Fallback if performance calculation fails
            quantity_held = (budget / 2) / current_price  # 50% in BTC
            cash_balance = budget / 2  # 50% in USDT
            position_value = budget / 2  # BTC value in USD
        
        # Build assets list
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
        
        total_balance = cash_balance + position_value
        
        # Calculate P/L if we have trading history
        total_pnl = perf.get('total_pl', 0) if perf else 0
        total_pnl_percentage = perf.get('pl_percent', 0) if perf else 0
        
        return {
            "total_balance": total_balance * exchange_rate,
            "available_balance": total_balance * exchange_rate,
            "in_orders": 0,
            "total_pnl": total_pnl * exchange_rate,
            "total_pnl_percentage": total_pnl_percentage,
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
    
    try:
        # LIVE TRADING MODE: Check if user has API keys configured
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.binance_api_key or not user.binance_api_secret:
            # Return empty balance if API keys not configured
            return {
                "total_balance": 0,
                "available_balance": 0,
                "in_orders": 0,
                "total_pnl": 0,
                "total_pnl_percentage": 0,
                "daily_pnl": 0,
                "daily_pnl_percentage": 0,
                "assets": [],
                "fiat_currency": fiat_currency,
                "exchange_rate": exchange_rate,
                "error": "API keys not configured. Please add your Binance API keys in Settings."
            }
        
        # Decrypt API keys
        api_key = decrypt_api_key(user.binance_api_key)
        api_secret = decrypt_api_key(user.binance_api_secret)
        
        # Create authenticated client
        client = get_binance_th_client(api_key, api_secret)
        
        # Fetch balance using account endpoint
        account_info = client.get_account()
        balances_list = account_info.get('balances', [])

        # Calculate totals
        total_balance = 0.0
        available_balance = 0.0
        in_orders = 0.0
        assets = []

        # Build a quick price cache to reduce calls
        price_cache: Dict[str, float] = {}
        
        for b in balances_list:
            try:
                currency = b.get('asset')
                free = float(b.get('free', 0) or 0)
                locked = float(b.get('locked', 0) or 0)
                amount = free + locked
            except Exception:
                continue

            if amount <= 0:
                continue

            # Determine USD value
            usd_value = 0.0
            try:
                if currency in ('USDT', 'USD', 'BUSD'):
                    usd_value = amount
                elif currency == 'THB':
                    # Approximate THB->USD
                    usd_value = amount * 0.03
                else:
                    symbol = f"{currency}/USDT"
                    if symbol not in price_cache:
                        try:
                            ticker = market_client.fetch_ticker(symbol)
                            price_cache[symbol] = float(ticker['last'] or 0)
                        except:
                            price_cache[symbol] = 0
                    usd_value = amount * price_cache.get(symbol, 0)
            except Exception as ticker_error:
                print(f"Could not get ticker for {currency}: {ticker_error}")
                usd_value = 0.0

            total_balance += usd_value
            available_balance += free * (usd_value / amount if amount > 0 else 0)
            in_orders += locked * (usd_value / amount if amount > 0 else 0)

            assets.append({
                "asset": currency,
                "free": free,
                "locked": locked,
                "total": amount,
                "usd_value": usd_value,
            })
        
        # Calculate P/L from trade history for Live Trading
        total_pnl = 0
        total_pnl_percentage = 0
        
        if config and config.symbol:
            # Try to get current price for P/L calculation
            current_price = 0.0
            # Check if we already have it in cache (from balances loop)
            if config.symbol in price_cache:
                current_price = price_cache[config.symbol]
            else:
                # Fetch fresh price
                try:
                    ticker = await get_current_price(config.symbol)
                    current_price = float(ticker.get('last', 0))
                except Exception:
                    pass

            # Use the shared performance tracker with mode='live'
            perf = calculate_paper_performance(user_id, config.symbol, 'gods_hand', db, mode='live', current_price=current_price)
            if perf:
                total_pnl = perf.get('total_pl', 0)
                total_pnl_percentage = perf.get('pl_percent', 0)
        
        daily_pnl = 0
        daily_pnl_percentage = 0
        
        # Convert all USD values to target fiat currency
        return {
            "total_balance": total_balance * exchange_rate,
            "available_balance": available_balance * exchange_rate,
            "in_orders": in_orders * exchange_rate,
            "total_pnl": total_pnl * exchange_rate,
            "total_pnl_percentage": total_pnl_percentage,
            "daily_pnl": daily_pnl * exchange_rate,
            "daily_pnl_percentage": daily_pnl_percentage,
            "assets": [
                {
                    **asset,
                    "usd_value": asset["usd_value"] * exchange_rate
                }
                for asset in assets
            ],
            "fiat_currency": fiat_currency,
            "exchange_rate": exchange_rate
        }
    except Exception as e:
        print(f"Account balance error: {str(e)}")
        # Return error message instead of raising exception
        return {
            "total_balance": 0,
            "available_balance": 0,
            "in_orders": 0,
            "total_pnl": 0,
            "total_pnl_percentage": 0,
            "daily_pnl": 0,
            "daily_pnl_percentage": 0,
            "assets": [],
            "fiat_currency": fiat_currency,
            "exchange_rate": exchange_rate,
            "error": f"Failed to fetch balance: {str(e)}"
        }


async def get_current_price(symbol: str) -> dict:
    """Get current ticker price for symbol"""
    try:
        ticker = market_client.fetch_ticker(symbol)
        return {
            "symbol": symbol,
            "last": ticker['last'],
            "bid": ticker['bid'],
            "ask": ticker['ask'],
            "high": ticker['high'],
            "low": ticker['low'],
            "volume": ticker['baseVolume'],
            "change_24h": ticker['percentage'],
            "timestamp": ticker['timestamp']
        }
    except Exception as e:
        raise Exception(f"Failed to fetch ticker for {symbol}: {str(e)}")


async def get_candlestick_data(symbol: str, timeframe: str = "1h", limit: int = 100) -> List[dict]:
    """Get OHLCV candlestick data"""
    try:
        ohlcv = market_client.fetch_ohlcv(symbol, timeframe, limit)
        
        candles = []
        for candle in ohlcv:
            candles.append({
                "timestamp": candle[0],
                "open": candle[1],
                "high": candle[2],
                "low": candle[3],
                "close": candle[4],
                "volume": candle[5]
            })
        
        return candles
    except Exception as e:
        raise Exception(f"Failed to fetch candles for {symbol}: {str(e)}")


async def get_order_book(symbol: str, limit: int = 20) -> dict:
    """Get orderbook depth"""
    try:
        orderbook = market_client.fetch_order_book(symbol, limit)
        return {
            "symbol": symbol,
            "bids": orderbook['bids'][:limit],
            "asks": orderbook['asks'][:limit],
            "timestamp": orderbook['timestamp']
        }
    except Exception as e:
        raise Exception(f"Failed to fetch orderbook: {str(e)}")


def convert_to_fiat(amount: float, fiat_currency: str = "USD") -> float:
    """Convert USDT to fiat (simplified, use real forex API in production)"""
    rate = get_exchange_rate(fiat_currency)
    return amount * rate


def get_exchange_rate(fiat_currency: str = "USD") -> float:
    """
    Get exchange rate from USD to target fiat currency.
    
    NOTE: Real-time exchange rates require a Forex API integration.
    Currently defaulting to 1.0 (USD) to avoid using outdated static rates.
    """
    if fiat_currency == "USD":
        return 1.0
        
    # In production, fetch real rate here.
    # Returning 1.0 (no conversion) to avoid using fake/static data.
    return 1.0


async def execute_market_trade(
    user_id: int,
    symbol: str,
    side: str,
    amount: float,
    db: Session
) -> dict:
    """Execute real market trade using user's API keys"""
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.binance_api_key or not user.binance_api_secret:
        raise Exception("API keys not configured")
    
    # Decrypt API keys
    api_key = decrypt_api_key(user.binance_api_key)
    api_secret = decrypt_api_key(user.binance_api_secret)
    
    # Create authenticated client for Binance TH
    client = get_binance_th_client(api_key, api_secret)
    
    try:
        # Execute market order using the native client
        if side.upper() == 'BUY':
            order = client.create_market_buy_order(symbol, amount)
        else:
            order = client.create_market_sell_order(symbol, amount)
        
        return {
            "order_id": order.get('orderId'),
            "symbol": order.get('symbol'),
            "side": order.get('side'),
            "amount": float(order.get('executedQty', 0)),
            "price": float(order.get('price', 0)) if order.get('price') else None,
            "status": order.get('status'),
            "timestamp": order.get('transactTime')
        }
    except Exception as e:
        raise Exception(f"Trade execution failed: {str(e)}")


# Cleanup on shutdown
async def close_exchange():
    """Close exchange connection - not needed for synchronous client"""
    pass
