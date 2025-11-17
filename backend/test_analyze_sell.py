"""Analyze the SELL trade"""
budget = 24343
price = 95481.90

simulated_btc = budget / price
print(f"Simulated BTC position: {simulated_btc:.8f}")
print(f"10% of that: {simulated_btc * 0.10:.8f}")

# Actual trade
actual_sold = 0.02142291
print(f"\nActual BTC sold: {actual_sold:.8f}")
print(f"Percentage: {(actual_sold / simulated_btc) * 100:.2f}%")

# What should remain
remaining_btc = simulated_btc - actual_sold
print(f"\nShould remain: {remaining_btc:.8f} BTC")
print(f"Worth: ${remaining_btc * price:.2f}")
