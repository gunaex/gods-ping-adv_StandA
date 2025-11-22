#!/usr/bin/env python3
"""Test the new preview endpoint"""
import requests

API_BASE = "http://localhost:8000/api"
TOKEN = None

def login():
    global TOKEN
    resp = requests.post(f"{API_BASE}/auth/login", json={"username": "Admin", "password": "admin123"})
    if resp.status_code == 200:
        TOKEN = resp.json()['access_token']
        print("✅ Logged in successfully")
    else:
        print(f"❌ Login failed: {resp.status_code}")
        exit(1)

def preview_gods_hand():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    resp = requests.get(f"{API_BASE}/bot/gods-hand/preview", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        print("\n=== GODS HAND PREVIEW ===")
        print(f"Symbol: {data['symbol']}")
        print(f"Would Execute: {data['would_execute']}")
        print(f"Action: {data['action']}")
        print(f"Confidence: {data['confidence']:.2%}")
        if data['block_reason']:
            print(f"❌ Blocked: {data['block_reason']}")
        print(f"\nCurrent Position:")
        print(f"  - Quantity: {data['current_position']['quantity']}")
        print(f"  - Cost Basis: ${data['current_position']['cost_basis']:.2f}")
        print(f"  - Value USD: ${data['current_position']['position_value_usd']:.2f}")
        print(f"  - Trades: {data['current_position']['trades_count']}")
        print(f"\nIncremental Calculation:")
        inc = data['incremental_calculation']
        print(f"  - Action: {inc['action']}")
        print(f"  - Step Amount USD: ${inc['step_amount_usd']:.2f}")
        print(f"  - Current Fill: {inc['current_fill_percent']:.1f}%")
        print(f"  - After Fill: {inc['after_fill_percent']:.1f}%")
        print(f"  - Can Execute: {inc['can_execute']}")
        print(f"  - Reason: {inc['reason']}")
    else:
        print(f"❌ Preview failed: {resp.status_code} - {resp.text}")

if __name__ == '__main__':
    login()
    preview_gods_hand()
