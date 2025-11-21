"""
Social Sentiment Analysis Service
Integrates real-time data from:
1. Alternative.me (Fear & Greed Index) - Free, Public
2. CryptoPanic (News & Sentiment) - Requires API Key
"""
import requests
import asyncio
from typing import Dict, Optional
from datetime import datetime

# Cache to prevent hitting rate limits
_cache = {
    'fng': {'data': None, 'timestamp': 0},
    'news': {}  # symbol -> {'data': ..., 'timestamp': ...}
}

CACHE_TTL_FNG = 3600  # 1 hour
CACHE_TTL_NEWS = 300  # 5 minutes


async def get_fear_and_greed_index() -> Dict:
    """
    Fetch Crypto Fear & Greed Index from Alternative.me
    Returns: {'value': int, 'classification': str}
    """
    current_ts = datetime.utcnow().timestamp()
    
    # Check cache
    if _cache['fng']['data'] and (current_ts - _cache['fng']['timestamp'] < CACHE_TTL_FNG):
        return _cache['fng']['data']
    
    try:
        # Run blocking request in thread
        response = await asyncio.to_thread(requests.get, "https://api.alternative.me/fng/")
        data = response.json()
        
        if data.get('data'):
            item = data['data'][0]
            result = {
                'value': int(item['value']),
                'classification': item['value_classification']
            }
            # Update cache
            _cache['fng'] = {'data': result, 'timestamp': current_ts}
            return result
            
    except Exception as e:
        print(f"Error fetching Fear & Greed Index: {e}")
    
    # Fallback
    return {'value': 50, 'classification': 'Neutral'}


async def get_cryptopanic_sentiment(api_key: str, symbol: str) -> Dict:
    """
    Fetch news sentiment from CryptoPanic
    Requires API Key
    """
    if not api_key:
        return {'sentiment_score': 0, 'news_count': 0, 'trending': False}
        
    # Normalize symbol (BTC/USDT -> BTC)
    currency = symbol.split('/')[0] if '/' in symbol else symbol
    
    current_ts = datetime.utcnow().timestamp()
    cache_key = f"{currency}_{api_key[:5]}"
    
    # Check cache
    if cache_key in _cache['news']:
        cached = _cache['news'][cache_key]
        if current_ts - cached['timestamp'] < CACHE_TTL_NEWS:
            return cached['data']
            
    try:
        url = f"https://cryptopanic.com/api/v1/posts/?auth_token={api_key}&currencies={currency}&kind=news&filter=hot"
        
        # Run blocking request in thread
        response = await asyncio.to_thread(requests.get, url)
        data = response.json()
        
        results = data.get('results', [])
        
        # Simple sentiment analysis based on votes
        bullish_votes = 0
        bearish_votes = 0
        total_news = len(results)
        
        for post in results:
            votes = post.get('votes', {})
            bullish_votes += votes.get('positive', 0)
            bearish_votes += votes.get('negative', 0)
            bullish_votes += votes.get('liked', 0)
            bearish_votes += votes.get('disliked', 0)
            
        # Calculate score (-1 to 1)
        total_votes = bullish_votes + bearish_votes
        if total_votes > 0:
            sentiment_score = (bullish_votes - bearish_votes) / total_votes
        else:
            sentiment_score = 0
            
        result = {
            'sentiment_score': sentiment_score,
            'news_count': total_news,
            'bullish_votes': bullish_votes,
            'bearish_votes': bearish_votes,
            'trending': total_news > 5  # Simple threshold
        }
        
        # Update cache
        _cache['news'][cache_key] = {'data': result, 'timestamp': current_ts}
        return result
        
    except Exception as e:
        print(f"Error fetching CryptoPanic news: {e}")
        return {'sentiment_score': 0, 'news_count': 0, 'trending': False, 'error': str(e)}


async def get_social_sentiment(symbol: str, cryptopanic_api_key: Optional[str] = None) -> Dict:
    """
    Aggregated Social Sentiment
    Combines Fear & Greed Index + CryptoPanic News
    """
    # Fetch in parallel
    fng_task = get_fear_and_greed_index()
    news_task = get_cryptopanic_sentiment(cryptopanic_api_key, symbol)
    
    fng, news = await asyncio.gather(fng_task, news_task)
    
    # Normalize F&G to -1 to 1 scale (0-100 -> -1 to 1)
    fng_score = (fng['value'] - 50) / 50
    
    # Combine scores (50% F&G, 50% News if available)
    if cryptopanic_api_key:
        combined_score = (fng_score * 0.5) + (news['sentiment_score'] * 0.5)
        confidence = 0.8  # High confidence with real news
    else:
        combined_score = fng_score
        confidence = 0.4  # Lower confidence with only F&G
        
    # Determine label
    if combined_score > 0.2:
        sentiment = "BULLISH"
    elif combined_score < -0.2:
        sentiment = "BEARISH"
    else:
        sentiment = "NEUTRAL"
        
    # Determine social volume
    news_count = news.get('news_count', 0)
    if news_count > 20:
        social_volume = "HIGH"
    elif news_count > 5:
        social_volume = "MEDIUM"
    else:
        social_volume = "LOW"
        
    return {
        "sentiment_score": round(combined_score, 2),
        "sentiment": sentiment,
        "fear_greed_index": fng['value'],
        "fear_greed_label": fng['classification'],
        "news_score": round(news.get('sentiment_score', 0), 2),
        "news_count": news_count,
        "news_mentions": news_count,
        "social_volume": social_volume,
        "trending": news.get('trending', False),
        "confidence": confidence,
        "sources": ["Alternative.me"] + (["CryptoPanic"] if cryptopanic_api_key else [])
    }
