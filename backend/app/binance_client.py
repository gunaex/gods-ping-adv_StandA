"""
Binance Thailand API Integration
Compatible with Binance TH API v1.0.0
Base URL: https://api.binance.th
"""

import hashlib
import hmac
import time
import requests
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class BinanceThailandClient:
    """
    Direct REST client for Binance Thailand API v1.0.0
    Supports both public and private endpoints with HMAC SHA256 authentication
    """
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.binance.th"
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({
                'X-MBX-APIKEY': api_key
            })
    
    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """Generate HMAC SHA256 signature for authenticated requests"""
        query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _request(self, method: str, endpoint: str, signed: bool = False, **kwargs) -> Any:
        """Make HTTP request to Binance TH API"""
        url = f"{self.base_url}{endpoint}"
        
        if signed:
            if not self.api_key or not self.api_secret:
                raise ValueError("API key and secret required for signed endpoints")
            
            params = kwargs.pop('params', {})
            params['timestamp'] = int(time.time() * 1000)
            
            # Generate query string manually to ensure signature matches exactly what is sent
            # Sort params to be deterministic
            ordered_params = sorted(params.items())
            query_string = '&'.join([f"{k}={v}" for k, v in ordered_params])
            
            signature = hmac.new(
                self.api_secret.encode('utf-8'),
                query_string.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            # Append signature
            full_query = f"{query_string}&signature={signature}"
            
            # Append to URL
            if '?' in url:
                url = f"{url}&{full_query}"
            else:
                url = f"{url}?{full_query}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Binance TH API error: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise
    
    # ========== PUBLIC ENDPOINTS ==========
    
    def get_ticker_24h(self, symbol: Optional[str] = None) -> Any:
        """Get 24hr ticker price change statistics"""
        params = {'symbol': symbol} if symbol else {}
        return self._request('GET', '/api/v1/ticker/24hr', params=params)
    
    def get_klines(self, symbol: str, interval: str = '1h', limit: int = 500, 
                   start_time: Optional[int] = None, end_time: Optional[int] = None) -> List:
        """
        Get candlestick/kline data
        Intervals: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        """
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        if start_time:
            params['startTime'] = start_time
        if end_time:
            params['endTime'] = end_time
        
        return self._request('GET', '/api/v1/klines', params=params)
    
    def get_order_book(self, symbol: str, limit: int = 100) -> Dict:
        """Get order book (market depth)"""
        params = {'symbol': symbol, 'limit': limit}
        return self._request('GET', '/api/v1/depth', params=params)
    
    def get_exchange_info(self, symbol: Optional[str] = None) -> Dict:
        """Get exchange trading rules and symbol information"""
        params = {'symbol': symbol} if symbol else {}
        return self._request('GET', '/api/v1/exchangeInfo', params=params)
    
    def get_avg_price(self, symbol: str) -> Dict:
        """Get current average price"""
        params = {'symbol': symbol}
        return self._request('GET', '/api/v1/avgPrice', params=params)
    
    # ========== PRIVATE ENDPOINTS ==========
    
    def get_account(self) -> Dict:
        """Get account information including balances"""
        return self._request('GET', '/api/v1/account', signed=True)
    
    def get_balance(self) -> List[Dict]:
        """Get account balances (non-zero only)"""
        account = self.get_account()
        return [b for b in account.get('balances', []) if float(b['free']) > 0 or float(b['locked']) > 0]
    
    def create_order(self, symbol: str, side: str, order_type: str, 
                     quantity: Optional[float] = None, 
                     quote_order_qty: Optional[float] = None,
                     price: Optional[float] = None,
                     time_in_force: str = 'GTC') -> Dict:
        """
        Create new order
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            order_type: 'LIMIT', 'MARKET', 'STOP_LOSS', etc.
            quantity: Order quantity (for MARKET sell or LIMIT orders)
            quote_order_qty: Quote asset quantity (for MARKET buy orders)
            price: Order price (required for LIMIT orders)
            time_in_force: 'GTC', 'IOC', 'FOK'
        """
        params = {
            'symbol': symbol,
            'side': side.upper(),
            'type': order_type.upper(),
        }
        
        if quantity:
            params['quantity'] = quantity
        if quote_order_qty:
            params['quoteOrderQty'] = quote_order_qty
        if price:
            params['price'] = price
        if order_type.upper() == 'LIMIT':
            params['timeInForce'] = time_in_force
        
        return self._request('POST', '/api/v1/order', signed=True, params=params)
    
    def create_market_buy_order(self, symbol: str, amount: float) -> Dict:
        """
        Create market buy order
        
        Args:
            symbol: Trading pair in ccxt format (e.g., 'BTC/USDT')
            amount: Amount in base currency (e.g., BTC) — the quantity to buy
        """
        # Convert symbol format: BTC/USDT -> BTCUSDT
        binance_symbol = symbol.replace('/', '')
        
        # Use 'quantity' (base asset amount) for market buy to match callers that pass base units
        return self.create_order(
            symbol=binance_symbol,
            side='BUY',
            order_type='MARKET',
            quantity=amount
        )
    
    def create_market_sell_order(self, symbol: str, amount: float) -> Dict:
        """
        Create market sell order
        
        Args:
            symbol: Trading pair in ccxt format (e.g., 'BTC/USDT')
            amount: Amount in base currency (BTC)
        """
        # Convert symbol format: BTC/USDT -> BTCUSDT
        binance_symbol = symbol.replace('/', '')
        
        return self.create_order(
            symbol=binance_symbol,
            side='SELL',
            order_type='MARKET',
            quantity=amount
        )
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """Cancel an active order"""
        params = {
            'symbol': symbol,
            'orderId': order_id
        }
        return self._request('DELETE', '/api/v1/order', signed=True, params=params)
    
    def get_order(self, symbol: str, order_id: int) -> Dict:
        """Query order status"""
        params = {
            'symbol': symbol,
            'orderId': order_id
        }
        return self._request('GET', '/api/v1/order', signed=True, params=params)
    
    def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get all open orders"""
        params = {'symbol': symbol} if symbol else {}
        return self._request('GET', '/api/v1/openOrders', signed=True, params=params)
    
    def get_all_orders(self, symbol: str, limit: int = 500) -> List[Dict]:
        """Get all orders (active, canceled, or filled)"""
        params = {
            'symbol': symbol,
            'limit': limit
        }
        return self._request('GET', '/api/v1/allOrders', signed=True, params=params)
    
    def get_my_trades(self, symbol: str, limit: int = 500) -> List[Dict]:
        """Get trades for a specific symbol"""
        params = {
            'symbol': symbol,
            'limit': limit
        }
        return self._request('GET', '/api/v1/myTrades', signed=True, params=params)


class BinanceThMarketData:
    """
    ccxt-compatible market data client with caching and rate limit protection
    """
    
    def __init__(self):
        self.client = BinanceThailandClient()
        self._ticker_cache = {}
        self._ohlcv_cache = {}
        self._orderbook_cache = {}
        self._rate_limit_until = None
        
        # Cache durations (seconds)
        self.ticker_cache_duration = 2  # Reduced from 5s
        self.orderbook_cache_duration = 2
        self.ohlcv_cache_durations = {
            '1m': 5,    # Reduced from 60s
            '5m': 10,   # Reduced from 120s
            '15m': 15,  # Reduced from 300s
            '1h': 15,   # Reduced from 600s (10m) -> 15s
            '4h': 30,   # Reduced from 1800s
            '1d': 60    # Reduced from 3600s
        }
    
    def _check_rate_limit(self):
        """Check if we're in rate limit cooldown"""
        if self._rate_limit_until:
            if datetime.now() < self._rate_limit_until:
                wait_seconds = (self._rate_limit_until - datetime.now()).total_seconds()
                raise Exception(f"Rate limited. Please wait {wait_seconds:.0f} seconds")
            else:
                self._rate_limit_until = None
    
    def _handle_rate_limit_error(self):
        """Set 60s cooldown on 429 error"""
        self._rate_limit_until = datetime.now() + timedelta(seconds=60)
        logger.warning("Rate limit hit. Cooldown for 60 seconds")
    
    def _normalize_symbol(self, symbol: str) -> str:
        """Convert BTC/USDT to BTCUSDT"""
        return symbol.replace('/', '')
    
    def _denormalize_symbol(self, symbol: str) -> str:
        """Convert BTCUSDT to BTC/USDT (simple heuristic for common pairs)"""
        if 'USDT' in symbol:
            return symbol.replace('USDT', '/USDT')
        elif 'BTC' in symbol and symbol != 'BTC':
            return symbol.replace('BTC', '/BTC')
        return symbol
    
    def fetch_ticker(self, symbol: str) -> Dict:
        """
        Get ticker with caching
        
        Returns ccxt-compatible format:
        {
            'symbol': 'BTC/USDT',
            'last': 50000.0,
            'bid': 49999.0,
            'ask': 50001.0,
            'high': 51000.0,
            'low': 49000.0,
            'volume': 1000.0,
            ...
        }
        """
        self._check_rate_limit()
        
        cache_key = symbol
        now = datetime.now()
        
        # Check cache
        if cache_key in self._ticker_cache:
            cached_data, cached_time = self._ticker_cache[cache_key]
            if (now - cached_time).total_seconds() < self.ticker_cache_duration:
                return cached_data
        
        try:
            binance_symbol = self._normalize_symbol(symbol)
            data = self.client.get_ticker_24h(binance_symbol)
            
            # Convert to ccxt format
            result = {
                'symbol': symbol,
                'timestamp': int(data['closeTime']),
                'datetime': datetime.fromtimestamp(data['closeTime'] / 1000).isoformat(),
                'high': float(data['highPrice']),
                'low': float(data['lowPrice']),
                'bid': float(data['bidPrice']),
                'ask': float(data['askPrice']),
                'last': float(data['lastPrice']),
                'close': float(data['lastPrice']),
                'previousClose': float(data['prevClosePrice']),
                'change': float(data['priceChange']),
                'percentage': float(data['priceChangePercent']),
                'baseVolume': float(data['volume']),
                'quoteVolume': float(data['quoteVolume']),
                'info': data
            }
            
            # Cache result
            self._ticker_cache[cache_key] = (result, now)
            return result
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                self._handle_rate_limit_error()
            raise
    
    def fetch_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 200,
                    since: Optional[int] = None) -> List[List]:
        """
        Get candlestick data with caching
        
        Returns ccxt-compatible format:
        [
            [timestamp, open, high, low, close, volume],
            ...
        ]
        """
        self._check_rate_limit()
        
        cache_key = f"{symbol}_{timeframe}_{limit}"
        now = datetime.now()
        cache_duration = self.ohlcv_cache_durations.get(timeframe, 300)
        
        # Check cache
        if cache_key in self._ohlcv_cache:
            cached_data, cached_time = self._ohlcv_cache[cache_key]
            if (now - cached_time).total_seconds() < cache_duration:
                return cached_data
        
        try:
            binance_symbol = self._normalize_symbol(symbol)
            data = self.client.get_klines(
                symbol=binance_symbol,
                interval=timeframe,
                limit=limit,
                start_time=since
            )
            
            # Convert to ccxt format
            result = [
                [
                    int(candle[0]),  # timestamp
                    float(candle[1]),  # open
                    float(candle[2]),  # high
                    float(candle[3]),  # low
                    float(candle[4]),  # close
                    float(candle[5])   # volume
                ]
                for candle in data
            ]
            
            # Cache result
            self._ohlcv_cache[cache_key] = (result, now)
            return result
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                self._handle_rate_limit_error()
            raise
    
    def fetch_order_book(self, symbol: str, limit: int = 100) -> Dict:
        """
        Get order book with caching
        
        Returns ccxt-compatible format:
        {
            'bids': [[price, amount], ...],
            'asks': [[price, amount], ...],
            'timestamp': ...,
            'datetime': ...
        }
        """
        self._check_rate_limit()
        
        cache_key = f"{symbol}_{limit}"
        now = datetime.now()
        
        # Check cache
        if cache_key in self._orderbook_cache:
            cached_data, cached_time = self._orderbook_cache[cache_key]
            if (now - cached_time).total_seconds() < self.orderbook_cache_duration:
                return cached_data
        
        try:
            binance_symbol = self._normalize_symbol(symbol)
            data = self.client.get_order_book(binance_symbol, limit)
            
            # Convert to ccxt format
            result = {
                'symbol': symbol,
                'bids': [[float(bid[0]), float(bid[1])] for bid in data['bids']],
                'asks': [[float(ask[0]), float(ask[1])] for ask in data['asks']],
                'timestamp': int(time.time() * 1000),
                'datetime': datetime.now().isoformat(),
                'nonce': None,
                'info': data
            }
            
            # Cache result
            self._orderbook_cache[cache_key] = (result, now)
            return result
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                self._handle_rate_limit_error()
            raise


# ========== CONVENIENCE FUNCTIONS ==========

def get_binance_th_client(api_key: str, api_secret: str) -> BinanceThailandClient:
    """
    Get authenticated Binance TH client for trading
    
    Args:
        api_key: User's Binance TH API key
        api_secret: User's Binance TH API secret
    
    Returns:
        BinanceThailandClient instance
    """
    return BinanceThailandClient(api_key=api_key, api_secret=api_secret)


def get_market_data_client() -> BinanceThMarketData:
    """
    Get market data client (no authentication required, with caching)
    
    Returns:
        BinanceThMarketData instance
    """
    return BinanceThMarketData()
