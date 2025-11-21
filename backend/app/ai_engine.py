"""
AI Trading Engine
AI-powered recommendations and market analysis
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from app.market import get_candlestick_data, get_current_price, get_order_book
from app.models import BotConfig


async def calculate_technical_indicators(candles: List[dict]) -> dict:
    """Calculate technical indicators from candlestick data"""
    closes = np.array([c['close'] for c in candles])
    highs = np.array([c['high'] for c in candles])
    lows = np.array([c['low'] for c in candles])
    volumes = np.array([c['volume'] for c in candles])
    
    # Simple Moving Averages
    sma_20 = np.mean(closes[-20:]) if len(closes) >= 20 else None
    sma_50 = np.mean(closes[-50:]) if len(closes) >= 50 else None
    
    # RSI (Relative Strength Index)
    def calculate_rsi(prices, period=14):
        if len(prices) < period + 1:
            return None
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    rsi = calculate_rsi(closes)
    
    # MACD
    def calculate_ema(data, period):
        return data[-1] if len(data) < period else np.mean(data[-period:])
    
    ema_12 = calculate_ema(closes, 12)
    ema_26 = calculate_ema(closes, 26)
    macd = ema_12 - ema_26 if ema_12 and ema_26 else None
    
    # Bollinger Bands
    bb_middle = sma_20
    bb_std = np.std(closes[-20:]) if len(closes) >= 20 else None
    bb_upper = (bb_middle + 2 * bb_std) if bb_middle and bb_std else None
    bb_lower = (bb_middle - 2 * bb_std) if bb_middle and bb_std else None
    
    # ADX Calculation (Tennis Mode)
    adx = None
    try:
        df = pd.DataFrame(candles)
        if len(df) >= 28:
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)
            df['close'] = df['close'].astype(float)
            
            # True Range
            df['tr0'] = abs(df['high'] - df['low'])
            df['tr1'] = abs(df['high'] - df['close'].shift(1))
            df['tr2'] = abs(df['low'] - df['close'].shift(1))
            df['tr'] = df[['tr0', 'tr1', 'tr2']].max(axis=1)
            
            # Directional Movement
            df['up_move'] = df['high'] - df['high'].shift(1)
            df['down_move'] = df['low'].shift(1) - df['low']
            
            df['plus_dm'] = np.where((df['up_move'] > df['down_move']) & (df['up_move'] > 0), df['up_move'], 0)
            df['minus_dm'] = np.where((df['down_move'] > df['up_move']) & (df['down_move'] > 0), df['down_move'], 0)
            
            # Smoothed TR and DM (Wilder's Smoothing approximation using EMA)
            alpha = 1/14
            df['tr_smooth'] = df['tr'].ewm(alpha=alpha, adjust=False).mean()
            df['plus_dm_smooth'] = df['plus_dm'].ewm(alpha=alpha, adjust=False).mean()
            df['minus_dm_smooth'] = df['minus_dm'].ewm(alpha=alpha, adjust=False).mean()
            
            # DI+ and DI-
            df['plus_di'] = 100 * (df['plus_dm_smooth'] / df['tr_smooth'])
            df['minus_di'] = 100 * (df['minus_dm_smooth'] / df['tr_smooth'])
            
            # DX and ADX
            df['dx'] = 100 * abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di'])
            df['adx'] = df['dx'].ewm(alpha=alpha, adjust=False).mean()
            
            adx = float(df['adx'].iloc[-1])
    except Exception as e:
        print(f"Error calculating ADX: {e}")

    # Current price position
    current_price = closes[-1]
    
    return {
        "sma_20": float(sma_20) if sma_20 else None,
        "sma_50": float(sma_50) if sma_50 else None,
        "rsi": float(rsi) if rsi else None,
        "macd": float(macd) if macd else None,
        "bb_upper": float(bb_upper) if bb_upper else None,
        "bb_middle": float(bb_middle) if bb_middle else None,
        "bb_lower": float(bb_lower) if bb_lower else None,
        "adx": adx,
        "current_price": float(current_price),
        "volume_avg": float(np.mean(volumes[-20:])) if len(volumes) >= 20 else None
    }


def evaluate_tennis_mode(indicators: dict, config: Optional[BotConfig]) -> tuple:
    """
    Sideways Sniper: Tennis Mode Logic
    Only active if ADX < 25 (Non-trending)
    Returns: (action, confidence, reason)
    """
    if not config or not getattr(config, 'tennis_mode_enabled', False):
        return None, 0.0, "Tennis Mode OFF"

    adx = indicators.get('adx')
    rsi = indicators.get('rsi')
    current_price = indicators.get('current_price')
    bb_lower = indicators.get('bb_lower')
    bb_upper = indicators.get('bb_upper')
    
    if adx is None or rsi is None or bb_lower is None or bb_upper is None:
        return "HOLD", 0.0, "Tennis Mode: Insufficient data"

    # 1. Check Market Condition: Must be Sideways (ADX < 25)
    if adx >= 25:
        return "HOLD", 0.0, f"Tennis Mode: Market Trending (ADX {adx:.1f} >= 25)"

    reason = f"Tennis Mode (ADX {adx:.1f}): "

    # 2. Long Entry (Bounce off bottom)
    # Price < Lower Band AND RSI < 35
    if current_price < bb_lower and rsi < 35:
        return "BUY", 0.95, reason + f"Oversold bounce! Price < Lower BB & RSI {rsi:.1f}"

    # 3. Short Entry / Sell (Bounce off top)
    # Price > Upper Band AND RSI > 65
    if current_price > bb_upper and rsi > 65:
        return "SELL", 0.95, reason + f"Overbought rejection! Price > Upper BB & RSI {rsi:.1f}"

    return "HOLD", 0.0, reason + "Waiting for edge bounce"


async def get_trading_recommendation(symbol: str, config: Optional[BotConfig] = None) -> dict:
    """
    Generate AI trading recommendation based on technical analysis
    Returns: action (BUY/SELL/HOLD), confidence, reasoning
    """
    try:
        # Fetch market data
        candles = await get_candlestick_data(symbol, "1h", 100)
        ticker = await get_current_price(symbol)
        
        # Calculate indicators
        indicators = await calculate_technical_indicators(candles)
        
        # --- TENNIS MODE CHECK ---
        # This overrides standard logic if it triggers a high confidence signal
        tennis_action, tennis_conf, tennis_reason = evaluate_tennis_mode(indicators, config)
        
        if tennis_action in ["BUY", "SELL"] and tennis_conf > 0.8:
            print(f"🎾 TENNIS MODE TRIGGERED: {tennis_action}")
            return {
                "symbol": symbol,
                "action": tennis_action,
                "confidence": tennis_conf,
                "reasoning": [tennis_reason],
                "indicators": indicators,
                "signal_breakdown": [f"🎾 {tennis_reason}"],
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # AI Decision Logic
        signals = []
        confidence_factors = []
        signal_details = []  # Track what each indicator is saying
        
        # RSI Analysis - BALANCED (less bearish)
        rsi = indicators.get('rsi')
        if rsi:
            if rsi < 35:  # More lenient oversold
                signals.append('BUY')
                confidence_factors.append(0.75)
                signal_details.append(f"RSI={rsi:.1f} (oversold) → BUY @0.75")
            elif rsi > 65:  # More lenient overbought
                signals.append('SELL')
                confidence_factors.append(0.75)
                signal_details.append(f"RSI={rsi:.1f} (overbought) → SELL @0.75")
            elif rsi < 45:  # Slight buy bias
                signals.append('BUY')
                confidence_factors.append(0.6)
                signal_details.append(f"RSI={rsi:.1f} (slight oversold) → BUY @0.6")
            elif rsi > 55:  # Slight sell signal
                signals.append('SELL')
                confidence_factors.append(0.6)
                signal_details.append(f"RSI={rsi:.1f} (slight overbought) → SELL @0.6")
            else:
                signals.append('HOLD')
                confidence_factors.append(0.5)
                signal_details.append(f"RSI={rsi:.1f} (neutral) → HOLD @0.5")
        
        # SMA Crossover and Trend Analysis (BALANCED STRATEGY)
        sma_20 = indicators.get('sma_20')
        sma_50 = indicators.get('sma_50')
        current = indicators['current_price']
        
        if sma_20 and sma_50:
            # Determine overall trend
            is_uptrend = sma_20 > sma_50
            is_downtrend = sma_20 < sma_50
            
            if is_uptrend:
                # UPTREND: Buy on strength OR buy dips (within reason)
                distance_from_sma20 = ((current - sma_20) / sma_20) * 100
                
                if current > sma_20:
                    # Strong uptrend - price above both SMAs
                    signals.append('BUY')
                    confidence_factors.append(0.8)  # Higher confidence
                    signal_details.append(f"Strong uptrend: SMA20({sma_20:.2f}) > SMA50({sma_50:.2f}), Price({current:.2f}) > SMA20 → BUY @0.8")
                elif distance_from_sma20 > -5:  # More lenient - 5% below SMA20
                    # Dip in uptrend - good buying opportunity
                    signals.append('BUY')
                    confidence_factors.append(0.75)  # Higher confidence
                    signal_details.append(f"Dip in uptrend: Price({current:.2f}) {distance_from_sma20:.1f}% below SMA20 in uptrend → BUY @0.75")
                else:
                    # Deeper dip but still in uptrend
                    signals.append('BUY')
                    confidence_factors.append(0.6)  # Still buy, lower confidence
                    signal_details.append(f"Deep dip in uptrend: Price {distance_from_sma20:.1f}% below SMA20 → BUY @0.6")
            
            elif is_downtrend:
                # DOWNTREND: Sell on weakness, avoid buying unless oversold
                if current < sma_20:
                    # Confirmed downtrend
                    signals.append('SELL')
                    confidence_factors.append(0.70)
                    signal_details.append(f"Downtrend: SMA20({sma_20:.2f}) < SMA50({sma_50:.2f}), Price({current:.2f}) < SMA20 → SELL @0.70")
                else:
                    # Price above SMA20 but still in downtrend - wait and see
                    signals.append('HOLD')
                    confidence_factors.append(0.55)
                    signal_details.append(f"Price above SMA20 but in downtrend → HOLD @0.55")
            else:
                # Sideways market
                signals.append('HOLD')
                confidence_factors.append(0.5)
                signal_details.append(f"Sideways market (SMAs close) → HOLD @0.5")
        
        # Volume Analysis - NEW (to increase BUY opportunities)
        volume = indicators.get('volume_sma')
        if volume and latest_data.get('volume'):
            current_volume = latest_data['volume']
            if current_volume > volume * 1.5:
                # High volume - confirms trend
                signals.append('BUY')  # Volume often precedes price rises
                confidence_factors.append(0.65)
                signal_details.append(f"High volume({current_volume:.0f} vs avg {volume:.0f}) → BUY @0.65")
            elif current_volume < volume * 0.5:
                # Low volume - market uncertainty
                signals.append('HOLD')
                confidence_factors.append(0.4)
                signal_details.append(f"Low volume({current_volume:.0f} vs avg {volume:.0f}) → HOLD @0.4")
        
        # Bollinger Bands - ENHANCED
        bb_upper = indicators.get('bb_upper')
        bb_lower = indicators.get('bb_lower')
        
        if bb_upper and bb_lower:
            if current <= bb_lower:
                signals.append('BUY')
                confidence_factors.append(0.8)  # Higher confidence at BB bottom
                signal_details.append(f"Price({current:.2f}) ≤ BB_Lower({bb_lower:.2f}) → BUY @0.8")
            elif current >= bb_upper:
                signals.append('SELL')
                confidence_factors.append(0.75)
                signal_details.append(f"Price({current:.2f}) ≥ BB_Upper({bb_upper:.2f}) → SELL @0.75")
            elif current < (bb_lower + bb_upper) * 0.4:  # Near lower band
                signals.append('BUY')
                confidence_factors.append(0.6)
                signal_details.append(f"Price({current:.2f}) near BB_Lower → BUY @0.6")
            else:
                signal_details.append(f"Price in BB range ({bb_lower:.2f} - {bb_upper:.2f}) → no signal")
        
        # Aggregate signals
        buy_count = signals.count('BUY')
        sell_count = signals.count('SELL')
        hold_count = signals.count('HOLD')
        
        # Log signal breakdown for debugging
        print(f"\n{'='*60}")
        print(f"AI DECISION CALCULATION for {symbol}")
        print(f"{'='*60}")
        for i, detail in enumerate(signal_details):
            signal_type = signals[i] if i < len(signals) else "UNKNOWN"
            confidence_val = confidence_factors[i] if i < len(confidence_factors) else 0
            print(f"  • {signal_type}: {detail}")
        print(f"\nSignal Summary: BUY={buy_count}, SELL={sell_count}, HOLD={hold_count}")
        print(f"All confidence factors: {confidence_factors}")
        print(f"All signals: {signals}")
        
        if buy_count > sell_count and buy_count > hold_count:
            action = 'BUY'
        elif sell_count > buy_count and sell_count > hold_count:
            action = 'SELL'
        else:
            action = 'HOLD'
        
        # Calculate confidence based on winning signals only - FIXED
        if action == 'BUY':
            # Average confidence of BUY signals only
            buy_confidences = [confidence_factors[i] for i, sig in enumerate(signals) if sig == 'BUY']
            confidence = np.mean(buy_confidences) if buy_confidences else 0.5
            print(f"BUY Confidence: {confidence:.3f} (average of {len(buy_confidences)} BUY signals)")
        elif action == 'SELL':
            # Average confidence of SELL signals only
            sell_confidences = [confidence_factors[i] for i, sig in enumerate(signals) if sig == 'SELL']
            confidence = np.mean(sell_confidences) if sell_confidences else 0.5
            print(f"SELL Confidence: {confidence:.3f} (average of {len(sell_confidences)} SELL signals)")
        else:
            # HOLD: average all signals (conservative approach)
            confidence = np.mean(confidence_factors) if confidence_factors else 0.5
            print(f"HOLD Confidence: {confidence:.3f} (average of {len(confidence_factors)} total signals)")
        
        # CRITICAL FIX: Ensure confidence is never 0 when we have valid signals
        if len(confidence_factors) > 0 and confidence == 0.0:
            confidence = max(0.3, np.mean(confidence_factors))  # Minimum 30% if signals exist
            print(f"🔧 Fixed zero confidence: adjusted to {confidence:.3f}")
        
        print(f"Confidence Breakdown: BUY signals={buy_count}, SELL signals={sell_count}, HOLD signals={hold_count}")
        
        # Apply user's risk settings - LOWERED for better performance
        min_confidence = config.min_confidence if config else 0.5  # Lowered from 0.7 to 0.5
        original_action = action
        if confidence < min_confidence:
            action = 'HOLD'
            print(f"⚠️  Confidence {confidence:.2f} < minimum {min_confidence} → Overriding {original_action} to HOLD")
        
        print(f"\nFinal Decision: {action} @ {confidence:.0%} confidence")
        print(f"{'='*60}\n")
        
        # Reasoning
        reasoning = []
        if rsi:
            reasoning.append(f"RSI: {rsi:.2f} ({'oversold' if rsi < 30 else 'overbought' if rsi > 70 else 'neutral'})")
        if sma_20 and sma_50:
            reasoning.append(f"SMA20 {'above' if sma_20 > sma_50 else 'below'} SMA50")
        reasoning.append(f"Price: ${current:.2f}")
        
        return {
            "symbol": symbol,
            "action": action,
            "confidence": round(confidence, 2),
            "reasoning": reasoning,
            "indicators": indicators,
            "signal_breakdown": signal_details,  # Add detailed breakdown to response
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        return {
            "symbol": symbol,
            "action": "HOLD",
            "confidence": 0.0,
            "reasoning": [f"Error: {str(e)}"],
            "indicators": {},
            "timestamp": datetime.utcnow().isoformat()
        }


async def get_advanced_analysis(symbol: str) -> dict:
    """
    Advanced AI market analysis with multiple timeframes and deeper insights
    """
    try:
        # Fetch multiple timeframes
        candles_1h = await get_candlestick_data(symbol, "1h", 100)
        candles_4h = await get_candlestick_data(symbol, "4h", 50)
        candles_1d = await get_candlestick_data(symbol, "1d", 30)
        
        # Calculate indicators for each timeframe
        indicators_1h = await calculate_technical_indicators(candles_1h)
        indicators_4h = await calculate_technical_indicators(candles_4h)
        indicators_1d = await calculate_technical_indicators(candles_1d)
        
        # Trend analysis
        def determine_trend(candles):
            closes = [c['close'] for c in candles[-10:]]
            if len(closes) < 2:
                return "UNKNOWN"
            slope = (closes[-1] - closes[0]) / len(closes)
            if slope > 0:
                return "UPTREND"
            elif slope < 0:
                return "DOWNTREND"
            else:
                return "SIDEWAYS"
        
        trend_1h = determine_trend(candles_1h)
        trend_4h = determine_trend(candles_4h)
        trend_1d = determine_trend(candles_1d)
        
        # Support/Resistance levels
        all_closes = [c['close'] for c in candles_1d]
        all_lows = [c['low'] for c in candles_1d]
        all_highs = [c['high'] for c in candles_1d]
        
        support = min(all_lows[-10:]) if all_lows else None
        resistance = max(all_highs[-10:]) if all_highs else None
        
        # Volatility
        volatility = np.std(all_closes[-20:]) if len(all_closes) >= 20 else 0
        
        return {
            "symbol": symbol,
            "trends": {
                "1h": trend_1h,
                "4h": trend_4h,
                "1d": trend_1d
            },
            "indicators": {
                "1h": indicators_1h,
                "4h": indicators_4h,
                "1d": indicators_1d
            },
            "levels": {
                "support": float(support) if support else None,
                "resistance": float(resistance) if resistance else None,
                "current": float(all_closes[-1]) if all_closes else None
            },
            "volatility": float(volatility),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        return {
            "symbol": symbol,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


async def calculate_risk_assessment(symbol: str, config: BotConfig) -> dict:
    """
    Calculate risk assessment for Gods Hand trading
    """
    try:
        candles = await get_candlestick_data(symbol, "1h", 100)
        indicators = await calculate_technical_indicators(candles)
        
        # Calculate volatility risk
        closes = [c['close'] for c in candles]
        volatility = np.std(closes[-20:]) / np.mean(closes[-20:]) if len(closes) >= 20 else 0
        
        # Risk score (0-100, lower is safer)
        risk_score = min(100, volatility * 1000)
        
        # Position sizing: position_size_ratio is the ABSOLUTE MAX the user configured
        # This is the hard limit that should never be exceeded
        max_position = config.budget * config.position_size_ratio
        
        # Risk adjustments affect the RECOMMENDED position size within the max limit
        # This guides the AI but doesn't prevent reaching the user's configured max
        if config.risk_level == 'conservative':
            suggested_multiplier = 0.5
        elif config.risk_level == 'moderate':
            suggested_multiplier = 0.75
        else:  # aggressive
            suggested_multiplier = 1.0
        
        # Suggested position considers risk, but max_position is the hard limit
        suggested_position = max_position * suggested_multiplier * (1 - risk_score / 200)
        
        # The recommended_position_size is now the MAX position configured by user
        # This allows incremental building up to the full position_size_ratio
        recommended_position = max_position
        
        # Fee calculation (Binance spot: ~0.1%)
        trading_fee_rate = 0.001
        estimated_fees = recommended_position * trading_fee_rate
        
        return {
            "symbol": symbol,
            "risk_score": round(risk_score, 2),
            "risk_level": config.risk_level,
            "volatility": round(volatility * 100, 2),
            "recommended_position_size": round(recommended_position, 2),
            "suggested_position_size": round(suggested_position, 2),  # For reference/logging
            "estimated_fees": round(estimated_fees, 2),
            "max_daily_loss": config.max_daily_loss,
            "current_price": indicators['current_price'],
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        return {
            "symbol": symbol,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
