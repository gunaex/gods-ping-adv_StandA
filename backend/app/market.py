"""
Market Data Service
Real-time crypto market data via ccxt (Binance)
"""
import ccxt.async_support as ccxt
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models import User
from app.auth import decrypt_api_key


# Binance exchange (public data)
exchange = ccxt.binance({
    'enableRateLimit': True,
    'options': {'defaultType': 'spot'}
})


async def get_current_price(symbol: str) -> dict:
    """Get current ticker price for symbol"""
    try:
        ticker = await exchange.fetch_ticker(symbol)
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
        raise Exception(f"Failed to fetch ticker: {str(e)}")


async def get_candlestick_data(symbol: str, timeframe: str = "1h", limit: int = 100) -> List[dict]:
    """Get OHLCV candlestick data"""
    try:
        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        
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
        raise Exception(f"Failed to fetch candles: {str(e)}")


async def get_order_book(symbol: str, limit: int = 20) -> dict:
    """Get orderbook depth"""
    try:
        orderbook = await exchange.fetch_order_book(symbol, limit)
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
    # Simplified conversion rates
    rates = {
        "USD": 1.0,
        "THB": 35.5  # Approximate rate
    }
    return amount * rates.get(fiat_currency, 1.0)


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
    
    # Create authenticated exchange instance
    user_exchange = ccxt.binance({
        'apiKey': api_key,
        'secret': api_secret,
        'enableRateLimit': True,
        'options': {'defaultType': 'spot'}
    })
    
    try:
        # Execute market order
        order_type = 'market'
        order = await user_exchange.create_order(symbol, order_type, side.lower(), amount)
        
        return {
            "order_id": order['id'],
            "symbol": order['symbol'],
            "side": order['side'],
            "amount": order['amount'],
            "price": order.get('average') or order.get('price'),
            "status": order['status'],
            "timestamp": order['timestamp']
        }
    except Exception as e:
        raise Exception(f"Trade execution failed: {str(e)}")
    finally:
        await user_exchange.close()


async def get_account_balance(user_id: int, db: Session) -> dict:
    """Get user's Binance account balance"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.binance_api_key or not user.binance_api_secret:
        raise Exception("API keys not configured")
    
    api_key = decrypt_api_key(user.binance_api_key)
    api_secret = decrypt_api_key(user.binance_api_secret)
    
    user_exchange = ccxt.binance({
        'apiKey': api_key,
        'secret': api_secret,
        'enableRateLimit': True
    })
    
    try:
        balance = await user_exchange.fetch_balance()
        return {
            "total": balance['total'],
            "free": balance['free'],
            "used": balance['used']
        }
    except Exception as e:
        raise Exception(f"Failed to fetch balance: {str(e)}")
    finally:
        await user_exchange.close()


# Cleanup on shutdown
async def close_exchange():
    """Close exchange connection"""
    await exchange.close()
