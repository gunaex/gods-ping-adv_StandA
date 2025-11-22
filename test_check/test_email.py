"""
Test email notification with sample SELL trade
"""
import sys
sys.path.append('backend')

from app.email_utils import format_trade_email, send_gmail
import os

# Sample SELL trade data
action = "SELL"
trade_value_fiat = 120400.45  # THB
confidence = 0.78  # 78%
pl_percent = 18.79  # +18.79%
account_balance_fiat = 2321375.78  # THB
fiat_currency = "THB"

# Format the email
subject, body = format_trade_email(
    action=action,
    trade_value_fiat=trade_value_fiat,
    confidence=confidence,
    pl_percent=pl_percent,
    account_balance_fiat=account_balance_fiat,
    fiat_currency=fiat_currency,
    timezone='Asia/Bangkok'
)

print("=" * 60)
print("EMAIL PREVIEW")
print("=" * 60)
print(f"Subject: {subject}")
print("=" * 60)
print(body)
print("=" * 60)

# To actually send the email, uncomment below and set your credentials
# Uncomment and fill in your details:
"""
# Set these or use environment variables
GMAIL_USER = "your-email@gmail.com"
GMAIL_APP_PASSWORD = "your-app-password"
RECIPIENT = "recipient@email.com"

success = send_gmail(
    to_email=RECIPIENT,
    subject=subject,
    body=body,
    gmail_user=GMAIL_USER,
    gmail_password=GMAIL_APP_PASSWORD
)

if success:
    print("✅ Email sent successfully!")
else:
    print("❌ Email send failed!")
"""
