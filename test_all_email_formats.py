"""
Test email notification with sample BUY trade
"""
import sys
sys.path.append('backend')

from app.email_utils import format_trade_email, send_gmail
import os

print("\n" + "=" * 60)
print("SAMPLE BUY NOTIFICATION")
print("=" * 60)

# Sample BUY trade data
action = "BUY"
trade_value_fiat = 50000.00  # THB
confidence = 0.82  # 82%
pl_percent = None  # No P/L on BUY
account_balance_fiat = 1850000.00  # THB
fiat_currency = "THB"

subject, body = format_trade_email(
    action=action,
    trade_value_fiat=trade_value_fiat,
    confidence=confidence,
    pl_percent=pl_percent,
    account_balance_fiat=account_balance_fiat,
    fiat_currency=fiat_currency,
    timezone='Asia/Bangkok'
)

print(f"Subject: {subject}")
print("=" * 60)
print(body)
print("=" * 60)

print("\n" + "=" * 60)
print("SAMPLE SELL NOTIFICATION (PROFIT)")
print("=" * 60)

# Sample SELL trade data with profit
subject2, body2 = format_trade_email(
    action="SELL",
    trade_value_fiat=120400.45,
    confidence=0.78,
    pl_percent=18.79,
    account_balance_fiat=2321375.78,
    fiat_currency="THB",
    timezone='Asia/Bangkok'
)

print(f"Subject: {subject2}")
print("=" * 60)
print(body2)
print("=" * 60)

print("\n" + "=" * 60)
print("SAMPLE SELL NOTIFICATION (LOSS)")
print("=" * 60)

# Sample SELL trade data with loss
subject3, body3 = format_trade_email(
    action="SELL",
    trade_value_fiat=45000.00,
    confidence=0.65,
    pl_percent=-8.5,
    account_balance_fiat=1750000.00,
    fiat_currency="THB",
    timezone='Asia/Bangkok'
)

print(f"Subject: {subject3}")
print("=" * 60)
print(body3)
print("=" * 60)

print("\n✅ Email formatting test complete!")
print("\nTo send actual email, edit test_email.py and uncomment the sending section.")
