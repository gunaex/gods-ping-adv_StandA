"""
Gods Mode AI - Advanced Multi-Model Trading Strategy
Optimized for Sideways-Down (Bearish Drift) Market Conditions

Architecture: Ensemble Gating Network (Meta-Model)
- Model A: LSTM-inspired Forecast (simplified linear regression with momentum)
- Model B: Classification using Parabolic SAR + RSI regime detection
- Meta-Model: Lightweight decision tree logic that gates Models A & B

Designed for free-tier CPU hosting (Render.com compatible)
"""

import numpy as np
from datetime import datetime, timezone
from typing import Dict, List, Optional
import json


class ModelA_Forecaster:
    """
    Simplified LSTM-inspired forecasting model using exponential moving average
    with momentum and trend strength. Lightweight alternative to full LSTM.
    
    Based on: Time-series prediction with momentum tracking
    Output: Continuous price forecast for next 1-6 hours
    """
    
    @staticmethod
    def predict(candles: List[dict], forecast_hours: int = 1) -> Dict:
        """
        Predict future price using EMA momentum and linear regression
        
        Args:
            candles: Historical OHLCV data (at least 50 candles)
            forecast_hours: How many hours ahead to forecast
            
        Returns:
            {
                'predicted_price': float,
                'trend_strength': float (0-1),
                'momentum': float (-1 to 1, negative = downward)
            }
        """
        if len(candles) < 50:
            raise ValueError("Need at least 50 candles for forecasting")
        
        closes = np.array([c['close'] for c in candles])
        
        # Calculate EMAs for trend detection
        ema_12 = ModelA_Forecaster._ema(closes, 12)
        ema_26 = ModelA_Forecaster._ema(closes, 26)
        ema_50 = ModelA_Forecaster._ema(closes, 50)
        
        # Momentum: normalized MACD-like indicator
        momentum = (ema_12 - ema_26) / ema_26 if ema_26 != 0 else 0
        
        # Trend strength: how far current price is from long-term EMA
        current_price = closes[-1]
        trend_strength = abs(current_price - ema_50) / ema_50 if ema_50 != 0 else 0
        trend_strength = min(1.0, trend_strength * 10)  # Normalize to 0-1
        
        # Simple linear extrapolation based on recent momentum
        recent_closes = closes[-20:]  # Last 20 periods
        time_steps = np.arange(len(recent_closes))
        
        # Linear regression coefficients
        slope, intercept = np.polyfit(time_steps, recent_closes, 1)
        
        # Forecast: extend the line + dampen with EMA convergence
        forecast_step = len(recent_closes) + forecast_hours
        raw_forecast = slope * forecast_step + intercept
        
        # Dampen extreme forecasts toward EMA (mean reversion)
        damping_factor = 0.7  # Higher = more conservative
        predicted_price = (raw_forecast * (1 - damping_factor)) + (ema_26 * damping_factor)
        
        return {
            'predicted_price': float(predicted_price),
            'trend_strength': float(trend_strength),
            'momentum': float(momentum)
        }
    
    @staticmethod
    def _ema(data: np.ndarray, period: int) -> float:
        """Calculate Exponential Moving Average (last value)"""
        if len(data) < period:
            return np.mean(data)
        
        multiplier = 2 / (period + 1)
        ema = data[0]
        for price in data[1:]:
            ema = (price - ema) * multiplier + ema
        return float(ema)


class ModelB_Classifier:
    """
    Market regime classifier using Parabolic SAR + RSI + Volatility
    
    Based on: SVM/Random Forest classification with technical indicators
    Output: Discrete signal (BUY/SELL/HOLD) + regime (TREND/RANGE/VOLATILITY)
    
    Lightweight rule-based classifier (no actual SVM to save CPU)
    """
    
    @staticmethod
    def classify(candles: List[dict]) -> Dict:
        """
        Classify market regime and generate signal
        
        Returns:
            {
                'signal': 'BUY' | 'SELL' | 'HOLD',
                'regime': 'TREND_UP' | 'TREND_DOWN' | 'RANGE' | 'HIGH_VOLATILITY',
                'confidence': float (0-1),
                'features': dict of indicator values
            }
        """
        if len(candles) < 50:
            raise ValueError("Need at least 50 candles for classification")
        
        closes = np.array([c['close'] for c in candles])
        highs = np.array([c['high'] for c in candles])
        lows = np.array([c['low'] for c in candles])
        
        # Calculate indicators
        rsi = ModelB_Classifier._calculate_rsi(closes, 14)
        atr = ModelB_Classifier._calculate_atr(highs, lows, closes, 14)
        psar = ModelB_Classifier._parabolic_sar(highs, lows, closes)
        
        current_price = closes[-1]
        
        # Volatility assessment
        volatility = atr / current_price if current_price != 0 else 0
        is_high_volatility = volatility > 0.03  # 3% ATR threshold
        
        # Regime detection
        regime = ModelB_Classifier._detect_regime(closes, psar, rsi, volatility)
        
        # Signal generation based on regime
        signal, confidence = ModelB_Classifier._generate_signal(
            current_price, psar, rsi, regime, volatility
        )
        
        return {
            'signal': signal,
            'regime': regime,
            'confidence': float(confidence),
            'features': {
                'rsi': float(rsi),
                'atr': float(atr),
                'volatility': float(volatility),
                'psar': float(psar),
                'current_price': float(current_price)
            }
        }
    
    @staticmethod
    def _calculate_rsi(closes: np.ndarray, period: int = 14) -> float:
        """Calculate RSI indicator"""
        if len(closes) < period + 1:
            return 50.0
        
        deltas = np.diff(closes)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        # Handle edge cases
        if avg_loss == 0 and avg_gain == 0:
            return 50.0  # No movement
        elif avg_loss == 0:
            return 85.0  # Strong buying but not extreme
        elif avg_gain == 0:
            return 15.0  # Strong selling but not extreme
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return float(rsi)
    
    @staticmethod
    def _calculate_atr(highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, period: int = 14) -> float:
        """Calculate Average True Range"""
        if len(closes) < period + 1:
            return 0.0
        
        tr_list = []
        for i in range(1, len(closes)):
            high_low = highs[i] - lows[i]
            high_close = abs(highs[i] - closes[i-1])
            low_close = abs(lows[i] - closes[i-1])
            tr = max(high_low, high_close, low_close)
            tr_list.append(tr)
        
        atr = np.mean(tr_list[-period:])
        return float(atr)
    
    @staticmethod
    def _parabolic_sar(highs: np.ndarray, lows: np.ndarray, closes: np.ndarray) -> float:
        """
        Simplified Parabolic SAR (last value only)
        Returns approximate SAR level for current position
        """
        if len(closes) < 5:
            return closes[-1]
        
        # Simplified: SAR is below price in uptrend, above in downtrend
        recent_trend = closes[-1] - closes[-5]
        
        if recent_trend > 0:  # Uptrend
            sar = min(lows[-5:]) * 0.98  # Below recent lows
        else:  # Downtrend
            sar = max(highs[-5:]) * 1.02  # Above recent highs
        
        return float(sar)
    
    @staticmethod
    def _detect_regime(closes: np.ndarray, psar: float, rsi: float, volatility: float) -> str:
        """Detect current market regime"""
        current_price = closes[-1]
        
        # High volatility overrides other regimes
        if volatility > 0.04:
            return "HIGH_VOLATILITY"
        
        # Price vs PSAR determines trend
        if current_price > psar * 1.01:
            return "TREND_UP"
        elif current_price < psar * 0.99:
            return "TREND_DOWN"
        else:
            return "RANGE"
    
    @staticmethod
    def _generate_signal(price: float, psar: float, rsi: float, regime: str, volatility: float) -> tuple:
        """
        Generate trading signal based on regime and indicators
        Optimized for SIDEWAYS-DOWN markets (LONG-ONLY strategy)
        
        Returns: (signal, confidence)
        """
        # SIDEWAYS-DOWN strategy: 
        # - SELL on resistance with high confidence
        # - BUY on strong oversold + low volatility (mean reversion)
        
        if regime == "TREND_DOWN":
            # Strong downtrend: Exit longs, wait for oversold to buy
            if rsi < 30 and volatility < 0.015:
                return "BUY", 0.75  # Buy oversold in downtrend (mean reversion)
            elif rsi > 50:
                return "SELL", 0.80  # Exit longs in downtrend
            else:
                return "HOLD", 0.60
        
        elif regime == "RANGE":
            # Sideways: Range-bound mean reversion
            if rsi > 65 and volatility < 0.02:
                return "SELL", 0.75  # Sell resistance in low vol
            elif rsi < 35 and volatility < 0.02:
                return "BUY", 0.70  # Buy support in low vol
            else:
                return "HOLD", 0.55
        
        elif regime == "HIGH_VOLATILITY":
            # High volatility: Defensive - avoid new positions
            if rsi > 70:
                return "SELL", 0.80  # Exit overbought
            elif rsi < 30:
                return "HOLD", 0.50  # Don't catch falling knife in high vol
            else:
                return "HOLD", 0.60
        
        else:  # TREND_UP
            # Uptrend: Buy pullbacks, sell overbought
            if rsi < 40:
                return "BUY", 0.70  # Buy on pullback
            elif rsi > 70:
                return "SELL", 0.75  # Take profit
            else:
                return "HOLD", 0.55
        
        return "HOLD", 0.50


class MetaModel_Gating:
    """
    Meta-Model: Ensemble Gating Network
    
    Decides HOW and WHEN to use Model A (Forecaster) vs Model B (Classifier)
    based on market context (volatility, RSI, current regime).
    
    Architecture: Rule-based decision tree (lightweight, no training needed)
    
    Logic:
    1. In HIGH VOLATILITY → Trust Model B's regime classification more
    2. In LOW VOLATILITY RANGE → Trust Model A's forecast for entries
    3. In STRONG TREND → Combine both with weighted ensemble
    """
    
    @staticmethod
    def make_decision(
        model_a_output: Dict,
        model_b_output: Dict,
        current_price: float,
        position: str = "FLAT"  # FLAT | LONG
    ) -> Dict:
        """
        Meta-decision logic: Gate between Model A and Model B
        LONG-ONLY strategy (no short selling)
        
        Returns:
            {
                "signal": "BUY" | "SELL" | "HOLD",
                "price": float,
                "timestamp": int,
                "confidence_score": float (0-1),
                "reason": str
            }
        """
        # Extract features
        forecast_price = model_a_output['predicted_price']
        momentum = model_a_output['momentum']
        trend_strength = model_a_output['trend_strength']
        
        regime = model_b_output['regime']
        classifier_signal = model_b_output['signal']
        classifier_confidence = model_b_output['confidence']
        rsi = model_b_output['features']['rsi']
        volatility = model_b_output['features']['volatility']
        
        # Gating Decision Tree
        
        # GATE 0: High-confidence Model B signals pass through (NEW)
        if classifier_confidence >= 0.75 and classifier_signal != 'HOLD':
            reason = f"High confidence Model B ({classifier_confidence:.0%}): {regime}, RSI={rsi:.0f}"
            return MetaModel_Gating._format_output(
                classifier_signal,
                current_price,
                classifier_confidence,
                reason
            )
        
        # GATE 1: High Volatility → Trust Model B (regime classifier) - RELAXED threshold
        if volatility > 0.025:  # Reduced from 0.03
            reason = f"High volatility ({volatility:.1%}): Following Model B regime classifier ({regime})"
            return MetaModel_Gating._format_output(
                classifier_signal,
                current_price,
                classifier_confidence * 0.95,  # Slight penalty for uncertainty
                reason
            )
        
        # GATE 2: Sideways Range + Low Volatility → Use Model A forecast for entries - RELAXED
        if regime == "RANGE" and volatility < 0.025:  # Relaxed from 0.02
            price_diff_pct = (forecast_price - current_price) / current_price
            
            # Model A predicts UP movement (>0.5%) and RSI not overbought
            if price_diff_pct > 0.005 and rsi < 65:  # Relaxed from 1% and 60
                signal = "BUY" if position != "LONG" else "HOLD"
                confidence = min(0.85, classifier_confidence + abs(momentum) * 0.5)
                reason = f"Range market: Model A forecasts +{price_diff_pct:.2%} rise, RSI={rsi:.0f}"
                return MetaModel_Gating._format_output(signal, current_price, confidence, reason)
            
            # Model A predicts DOWN movement (<-0.5%) and RSI not oversold
            elif price_diff_pct < -0.005 and rsi > 40:  # Relaxed from -1%
                signal = "SELL" if position == "LONG" else "HOLD"
                confidence = min(0.85, classifier_confidence + abs(momentum) * 0.5)
                reason = f"Range market: Model A forecasts {price_diff_pct:.2%} drop, RSI={rsi:.0f}"
                return MetaModel_Gating._format_output(signal, current_price, confidence, reason)
            
            else:
                # No clear forecast edge
                return MetaModel_Gating._format_output(
                    "HOLD",
                    current_price,
                    0.60,
                    f"Range market: Model A forecast unclear ({price_diff_pct:+.2%})"
                )
        
        # GATE 3: Downtrend → Ensemble weighted toward Model B - RELAXED threshold
        if regime == "TREND_DOWN" and momentum < -0.005:  # Relaxed from -0.01:  # Relaxed from -0.01
            # Downtrend confirmed by both models
            if classifier_signal == "SELL" and position == "LONG":
                # Exit longs in downtrend
                forecast_agrees = forecast_price < current_price * 0.99
                confidence = classifier_confidence
                if forecast_agrees:
                    confidence = min(0.90, confidence + 0.10)
                    reason = f"Downtrend: Both models agree SELL (forecast: {forecast_price:.2f})"
                else:
                    reason = f"Downtrend: Model B signals SELL, Model A neutral"
                
                return MetaModel_Gating._format_output(
                    "SELL",
                    current_price,
                    confidence,
                    reason
                )
            
            elif classifier_signal == "BUY" and rsi < 30:
                # Oversold buy in downtrend (mean reversion)
                return MetaModel_Gating._format_output(
                    "BUY",
                    current_price,
                    classifier_confidence,
                    f"Downtrend: Oversold bounce opportunity (RSI={rsi:.0f})"
                )
            
            else:
                return MetaModel_Gating._format_output(
                    "HOLD",
                    current_price,
                    0.60,
                    f"Downtrend: Waiting for better entry (RSI={rsi:.0f})"
                )
        
        # GATE 4: Weak Trend or Uncertain → Conservative HOLD or follow high-confidence Model B
        if classifier_confidence > 0.75:
            reason = f"Model B high confidence ({classifier_confidence:.0%}): {regime}"
            return MetaModel_Gating._format_output(
                classifier_signal,
                current_price,
                classifier_confidence * 0.90,
                reason
            )
        
        # DEFAULT: HOLD when no clear edge
        return MetaModel_Gating._format_output(
            "HOLD",
            current_price,
            0.50,
            f"No clear edge: {regime}, RSI={rsi:.0f}, momentum={momentum:+.3f}"
        )
    
    @staticmethod
    def _format_output(signal: str, price: float, confidence: float, reason: str) -> Dict:
        """Format final output JSON"""
        return {
            "signal": signal,
            "price": round(price, 2),
            "timestamp": int(datetime.now(timezone.utc).timestamp()),
            "confidence_score": round(min(1.0, max(0.0, confidence)), 2),
            "reason": reason
        }


async def run_gods_mode(candles: List[dict], current_position: str = "FLAT") -> Dict:
    """
    Main entry point for Gods Mode AI
    LONG-ONLY strategy optimized for sideways-down markets
    
    Args:
        candles: List of OHLCV candlestick data (minimum 50 candles)
        current_position: "FLAT" | "LONG" (no short positions supported)
    
    Returns:
        Final trading decision JSON with signal (BUY/SELL/HOLD), price, confidence, reason
    """
    if len(candles) < 50:
        return {
            "signal": "HOLD",
            "price": candles[-1]['close'] if candles else 0,
            "timestamp": int(datetime.now(timezone.utc).timestamp()),
            "confidence_score": 0.0,
            "reason": "Insufficient data (need 50+ candles)"
        }
    
    # Run Model A: Forecaster
    try:
        model_a_output = ModelA_Forecaster.predict(candles, forecast_hours=1)
    except Exception as e:
        model_a_output = {
            'predicted_price': candles[-1]['close'],
            'trend_strength': 0.5,
            'momentum': 0.0
        }
        print(f"[WARN] Model A failed: {e}")
    
    # Run Model B: Classifier
    try:
        model_b_output = ModelB_Classifier.classify(candles)
    except Exception as e:
        model_b_output = {
            'signal': 'HOLD',
            'regime': 'UNKNOWN',
            'confidence': 0.5,
            'features': {'rsi': 50, 'atr': 0, 'volatility': 0, 'psar': candles[-1]['close'], 'current_price': candles[-1]['close']}
        }
        print(f"[WARN] Model B failed: {e}")
    
    current_price = candles[-1]['close']
    
    # Run Meta-Model: Gating Decision
    decision = MetaModel_Gating.make_decision(
        model_a_output,
        model_b_output,
        current_price,
        current_position
    )
    
    # Add debug info
    decision['_debug'] = {
        'model_a': model_a_output,
        'model_b': model_b_output,
        'current_position': current_position
    }
    
    return decision
