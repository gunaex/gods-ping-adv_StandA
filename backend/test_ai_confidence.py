#!/usr/bin/env python3
"""
Test AI Engine Confidence Calculation
Debug why confidence shows 100% when only one signal has 80%
"""

def test_confidence_calculation():
    """Simulate the AI confidence calculation logic"""
    
    # Your example from logs: 4 signals analyzed, 1 SELL with 80%
    # Let's simulate possible scenarios
    
    import numpy as np
    
    print("=== Testing AI Confidence Calculation ===\n")
    
    # Scenario 1: What you reported
    signals = ['SELL']
    confidence_factors = [0.8]
    
    print("Scenario 1: Your reported case")
    print(f"Signals: {signals}")
    print(f"Confidence factors: {confidence_factors}")
    
    buy_count = signals.count('BUY')
    sell_count = signals.count('SELL')
    hold_count = signals.count('HOLD')
    
    if buy_count > sell_count and buy_count > hold_count:
        action = 'BUY'
    elif sell_count > buy_count and sell_count > hold_count:
        action = 'SELL'
    else:
        action = 'HOLD'
    
    # OLD logic (what was causing the bug)
    old_confidence = np.mean(confidence_factors)
    
    # NEW logic (fixed)
    if action == 'SELL':
        sell_confidences = [confidence_factors[i] for i, sig in enumerate(signals) if sig == 'SELL']
        new_confidence = np.mean(sell_confidences) if sell_confidences else 0.5
    
    print(f"Action: {action}")
    print(f"OLD Confidence (avg all): {old_confidence:.3f} = {old_confidence*100:.0f}%")
    print(f"NEW Confidence (avg SELL only): {new_confidence:.3f} = {new_confidence*100:.0f}%")
    
    print("\n" + "="*50)
    
    # Scenario 2: What might have actually happened (4 signals)
    print("\nScenario 2: Possible 4-signal case")
    signals = ['HOLD', 'SELL', 'HOLD', 'HOLD'] 
    confidence_factors = [0.5, 0.8, 0.5, 0.5]
    
    print(f"Signals: {signals}")
    print(f"Confidence factors: {confidence_factors}")
    
    buy_count = signals.count('BUY')
    sell_count = signals.count('SELL') 
    hold_count = signals.count('HOLD')
    
    if buy_count > sell_count and buy_count > hold_count:
        action = 'BUY'
    elif sell_count > buy_count and sell_count > hold_count:
        action = 'SELL'
    else:
        action = 'HOLD'
    
    old_confidence = np.mean(confidence_factors)
    
    if action == 'SELL':
        sell_confidences = [confidence_factors[i] for i, sig in enumerate(signals) if sig == 'SELL']
        new_confidence = np.mean(sell_confidences) if sell_confidences else 0.5
    elif action == 'HOLD':
        new_confidence = np.mean(confidence_factors)
    
    print(f"Action: {action}")
    print(f"OLD Confidence (avg all): {old_confidence:.3f} = {old_confidence*100:.0f}%")
    print(f"NEW Confidence: {new_confidence:.3f} = {new_confidence*100:.0f}%")
    
    print("\n" + "="*50)
    
    # Scenario 3: Edge case that could cause 100%
    print("\nScenario 3: Multiple SELL signals averaging to 100%")
    signals = ['SELL', 'SELL', 'HOLD', 'HOLD']
    confidence_factors = [0.8, 1.0, 0.5, 0.5]  # Two SELL: 0.8 and 1.0 → avg = 0.9
    
    print(f"Signals: {signals}")
    print(f"Confidence factors: {confidence_factors}")
    
    buy_count = signals.count('BUY')
    sell_count = signals.count('SELL')
    hold_count = signals.count('HOLD')
    
    if sell_count > buy_count and sell_count > hold_count:
        action = 'SELL'
    
    sell_confidences = [confidence_factors[i] for i, sig in enumerate(signals) if sig == 'SELL']
    new_confidence = np.mean(sell_confidences) if sell_confidences else 0.5
    
    print(f"Action: {action}")
    print(f"SELL confidences only: {sell_confidences}")
    print(f"NEW Confidence (avg SELL only): {new_confidence:.3f} = {new_confidence*100:.0f}%")

if __name__ == "__main__":
    test_confidence_calculation()