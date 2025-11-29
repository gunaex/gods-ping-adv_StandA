import time
from app.binance_client import get_market_data_client

client = get_market_data_client()
symbol = "BTC/USDT"

print(f"Fetching ticker for {symbol}...")
ticker1 = client.fetch_ticker(symbol)
print(f"Price 1: {ticker1['last']}")

print("Waiting 5 seconds...")
time.sleep(5)

print(f"Fetching ticker for {symbol} again...")
ticker2 = client.fetch_ticker(symbol)
print(f"Price 2: {ticker2['last']}")

if ticker1['last'] == ticker2['last']:
    print("WARNING: Price did not change in 5 seconds (could be stable market or cache issue)")
else:
    print("SUCCESS: Price changed, data is live")
