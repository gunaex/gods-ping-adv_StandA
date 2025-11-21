#!/usr/bin/env python3
"""
Trading Performance Root Cause Analysis
"""
import sqlite3
import json
from datetime import datetime, timedelta

def analyze_poor_performance():
    """Identify why win rate is only 38.1%"""
    
    conn = sqlite3.connect('gods_ping.db')
    cursor = conn.cursor()
    
    print("=== WIN RATE ANALYSIS: 38.1% (8/21 trades) ===\n")
    
    # Get recent trade pattern
    print("1. TRADE PATTERN (Last 10 trades):")
    cursor.execute('''
        SELECT timestamp, side, amount, filled_price 
        FROM trades 
        ORDER BY timestamp DESC 
        LIMIT 10
    ''')
    trades = cursor.fetchall()
    
    recent_buys = 0
    recent_sells = 0
    
    for trade in trades:
        timestamp, side, amount, price = trade
        if side == 'BUY':
            recent_buys += 1
        else:
            recent_sells += 1
        print(f"  {timestamp} | {side:4} | ${price:8,.2f}")
    
    print(f"  Recent pattern: {recent_buys} BUY vs {recent_sells} SELL")
    
    # Check AI confidence issues
    print("\n2. AI CONFIDENCE ISSUES:")
    cursor.execute('''
        SELECT details FROM logs 
        WHERE message LIKE '%confidence%' AND message LIKE '%min%'
        ORDER BY timestamp DESC 
        LIMIT 3
    ''')
    
    confidence_issues = cursor.fetchall()
    if confidence_issues:
        print("  ⚠️  Recent low confidence rejections found")
        for issue in confidence_issues:
            if issue[0]:
                try:
                    details = json.loads(issue[0])
                    conf = details.get('confidence', 0)
                    min_conf = details.get('min_confidence', 0)
                    print(f"    Confidence {conf:.2f} < Min {min_conf:.2f}")
                except:
                    pass
    else:
        print("  ✅ No recent confidence rejection issues")
    
    # Check stop-loss triggers
    print("\n3. STOP-LOSS ANALYSIS:")
    cursor.execute('''
        SELECT details FROM logs 
        WHERE message LIKE '%STOP LOSS%' OR message LIKE '%stop%'
        ORDER BY timestamp DESC 
        LIMIT 3
    ''')
    
    stop_losses = cursor.fetchall()
    if stop_losses:
        print("  ⚠️  Stop-loss triggers found")
        for sl in stop_losses:
            if sl[0]:
                print(f"    Stop-loss event logged")
    else:
        print("  ✅ No recent stop-loss triggers")
    
    # Check market conditions
    print("\n4. MARKET CONDITIONS:")
    cursor.execute('SELECT * FROM paper_trading_snapshots ORDER BY timestamp DESC LIMIT 1')
    latest = cursor.fetchone()
    if latest:
        print(f"  Current P/L: {latest[13]:.2f}% ({latest[18]} trades)")
        print(f"  Win rate: {latest[17]}/{latest[18]} = {(latest[17]/latest[18]*100):.1f}%")
        print(f"  Max drawdown: {latest[19]:.2f}%")
    
    # Get current settings
    print("\n5. CURRENT SETTINGS:")
    cursor.execute('SELECT min_confidence, hard_stop_loss_percent FROM bot_configs LIMIT 1')
    settings = cursor.fetchone()
    if settings:
        min_conf, stop_loss = settings
        print(f"  Min Confidence: {min_conf:.2f} ({'HIGH' if min_conf > 0.7 else 'MEDIUM' if min_conf > 0.5 else 'LOW'})")
        print(f"  Stop Loss: {stop_loss:.1f}% ({'TIGHT' if stop_loss < 3 else 'NORMAL' if stop_loss < 5 else 'LOOSE'})")
    
    conn.close()
    
    print("\n=== ROOT CAUSE ANALYSIS ===")
    
    # Analyze the data we found
    if recent_sells > recent_buys * 2:
        print("🔴 ISSUE 1: Excessive selling - possible bearish bias")
        print("   → AI may be too sensitive to downtrends")
    
    if settings and settings[0] > 0.65:
        print("🔴 ISSUE 2: Min confidence too high")
        print(f"   → {settings[0]:.2f} confidence threshold rejecting good trades")
    
    if settings and settings[1] < 3.5:
        print("🔴 ISSUE 3: Stop-loss too tight")
        print(f"   → {settings[1]:.1f}% stop-loss triggering on normal volatility")
    
    print("\n=== RECOMMENDATIONS ===")
    print("1. Lower min_confidence from 0.60 to 0.50-0.55")
    print("2. Increase stop_loss from 3.0% to 4.0-5.0%")
    print("3. Check if AI signals have bearish bias")
    print("4. Consider market conditions (BTC volatility)")

if __name__ == "__main__":
    analyze_poor_performance()