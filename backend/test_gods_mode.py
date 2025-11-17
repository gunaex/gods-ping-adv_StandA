"""
Test Gods Mode AI with sample data
"""
import sys
sys.path.append('.')

from app.gods_mode_ai import run_gods_mode, ModelA_Forecaster, ModelB_Classifier, MetaModel_Gating
import asyncio
import random

def generate_sample_candles(num_candles=100, trend='down'):
    """Generate realistic sample candles for testing"""
    candles = []
    base_price = 42000.0
    
    for i in range(num_candles):
        if trend == 'down':
            # Downtrend with noise
            base_price -= random.uniform(5, 50)
            if i % 10 == 0:  # Occasional bounce
                base_price += random.uniform(50, 200)
        elif trend == 'sideways':
            # Range-bound
            base_price += random.uniform(-100, 100)
        else:  # up
            base_price += random.uniform(5, 50)
        
        volatility = random.uniform(50, 200)
        
        candles.append({
            'timestamp': 1700000000 + i * 3600,
            'open': base_price - random.uniform(-50, 50),
            'high': base_price + volatility,
            'low': base_price - volatility,
            'close': base_price,
            'volume': random.uniform(100, 1000)
        })
    
    return candles


async def test_gods_mode():
    """Test all three components of Gods Mode"""
    
    print("=" * 70)
    print("🧪 TESTING GODS MODE AI")
    print("=" * 70)
    
    # Generate sample data for different market conditions
    print("\n📊 Generating sample market data...")
    
    test_scenarios = [
        ('Downtrend (Bearish)', 'down'),
        ('Sideways (Range)', 'sideways'),
        ('Uptrend (Bullish)', 'up')
    ]
    
    for scenario_name, trend_type in test_scenarios:
        print(f"\n{'='*70}")
        print(f"📈 Scenario: {scenario_name}")
        print(f"{'='*70}")
        
        candles = generate_sample_candles(100, trend_type)
        current_price = candles[-1]['close']
        
        print(f"\n💰 Current Price: ${current_price:,.2f}")
        print(f"📊 Candles: {len(candles)}")
        
        # Test Model A
        print(f"\n🔵 Model A (Forecaster):")
        try:
            model_a_result = ModelA_Forecaster.predict(candles, forecast_hours=1)
            print(f"   Predicted Price: ${model_a_result['predicted_price']:,.2f}")
            print(f"   Trend Strength: {model_a_result['trend_strength']:.3f}")
            print(f"   Momentum: {model_a_result['momentum']:+.4f}")
            
            price_diff = model_a_result['predicted_price'] - current_price
            price_pct = (price_diff / current_price) * 100
            print(f"   Forecast: {price_pct:+.2f}% ({price_diff:+.2f})")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test Model B
        print(f"\n🟠 Model B (Classifier):")
        try:
            model_b_result = ModelB_Classifier.classify(candles)
            print(f"   Signal: {model_b_result['signal']}")
            print(f"   Regime: {model_b_result['regime']}")
            print(f"   Confidence: {model_b_result['confidence']:.0%}")
            print(f"   RSI: {model_b_result['features']['rsi']:.1f}")
            print(f"   Volatility: {model_b_result['features']['volatility']:.3%}")
            print(f"   PSAR: ${model_b_result['features']['psar']:,.2f}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test Full Gods Mode
        print(f"\n🔴 Meta-Model (Final Decision):")
        try:
            decision = await run_gods_mode(candles, current_position='FLAT')
            print(f"   Signal: {decision['signal']}")
            print(f"   Price: ${decision['price']:,.2f}")
            print(f"   Confidence: {decision['confidence_score']:.0%}")
            print(f"   Reason: {decision['reason']}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n{'='*70}")
    print("✅ GODS MODE AI TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    print("\n🚀 Gods Mode AI - Component Test Suite")
    print("Testing with synthetic market data...\n")
    asyncio.run(test_gods_mode())
    print("\n✨ All tests completed!")
