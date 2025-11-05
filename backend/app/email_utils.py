import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
from zoneinfo import ZoneInfo

def format_trade_email(action, trade_value_fiat, confidence, pl_percent, account_balance_fiat, fiat_currency, timezone='Asia/Bangkok'):
    """
    Format a beautiful trade notification email.
    
    Args:
        action: 'BUY' or 'SELL'
        trade_value_fiat: Trade value in fiat currency
        confidence: AI confidence (0-1)
        pl_percent: Profit/Loss percentage (can be None for BUY)
        account_balance_fiat: Current account balance in fiat
        fiat_currency: 'USD' or 'THB'
        timezone: Timezone name (default: 'Asia/Bangkok')
    """
    # Get current time in user's timezone
    try:
        tz = ZoneInfo(timezone)
        now = datetime.now(tz)
        time_str = now.strftime('%a, %b %d, %Y, %I:%M:%S %p GMT%z')
        tz_offset = now.strftime('%z')
        tz_offset_formatted = f"UTC{tz_offset[:3]}:{tz_offset[3:]}"
    except:
        now = datetime.utcnow()
        time_str = now.strftime('%a, %b %d, %Y, %I:%M:%S %p UTC')
        tz_offset_formatted = "UTC+00:00"
    
    # Format P/L for subject
    pl_display = f"+{pl_percent:.2f}%" if pl_percent and pl_percent > 0 else f"{pl_percent:.2f}%" if pl_percent else "N/A"
    
    # Subject line
    subject = f"GODS ping to You | {action} | {pl_display}"
    
    # Motivational quote based on P/L
    if pl_percent is None or action == 'BUY':
        quote = "Gods Say! The journey begins with a single step!"
    elif pl_percent > 20:
        quote = "Gods Say! You are the champion!!!!"
    elif pl_percent > 10:
        quote = "Gods Say! Excellent work, keep it up!"
    elif pl_percent > 0:
        quote = "Gods Say! Profit is profit, stay wise!"
    elif pl_percent > -5:
        quote = "Gods Say! Stay calm, the tides will turn!"
    else:
        quote = "Gods Say! Learn from this, grow stronger!"
    
    # Format numbers with commas
    trade_value_str = f"{trade_value_fiat:,.2f}"
    balance_str = f"{account_balance_fiat:,.2f}"
    confidence_str = f"{int(confidence * 100)}%"
    
    # Email body
    body = f"""GODS PING TO YOU | {action} | {pl_display}

{time_str}
({timezone} • {tz_offset_formatted})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Trade Value: {trade_value_str} {fiat_currency}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AI Confidence: {confidence_str}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

P/L: {pl_display}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Action: {action}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Account Balance: {balance_str} {fiat_currency}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{quote}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return subject, body


def send_gmail(to_email, subject, body, gmail_user=None, gmail_password=None):
    """
    Send an email using Gmail SMTP.
    If gmail_user and gmail_password are provided, use those.
    Otherwise, fall back to environment variables:
      GMAIL_USER: your Gmail address
      GMAIL_APP_PASSWORD: your Gmail app password (not your main password)
    """
    sender_email = gmail_user or os.getenv('GMAIL_USER')
    sender_password = gmail_password or os.getenv('GMAIL_APP_PASSWORD')
    
    if not sender_email or not sender_password:
        print("⚠️  Gmail credentials not configured. Skipping email notification.")
        print("   Configure in Settings or set GMAIL_USER/GMAIL_APP_PASSWORD environment variables.")
        return False
    
    if sender_password == '***':
        print("⚠️  Gmail app password is masked. Please enter your actual app password in Settings.")
        return False

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print(f"✅ Email sent successfully to {to_email}")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Gmail authentication failed: {e}")
        print("   Please generate an App Password at: https://myaccount.google.com/apppasswords")
        print("   See GMAIL_SETUP.md for instructions.")
        return False
    except Exception as e:
        print(f"❌ Email send failed: {e}")
        return False
