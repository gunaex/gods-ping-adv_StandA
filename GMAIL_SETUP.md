# Gmail App Password Setup Guide

## Step 1: Enable 2-Factor Authentication (2FA)
1. Go to https://myaccount.google.com/security
2. Under "Signing in to Google", enable "2-Step Verification"
3. Follow the setup process

## Step 2: Generate App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" as the app
3. Select "Windows Computer" (or Other) as the device
4. Click "Generate"
5. Google will show you a 16-character password (like: "abcd efgh ijkl mnop")
6. **Copy this password** - you won't see it again!

## Step 3: Configure in Gods Ping
1. Open the app and go to Settings
2. In the "Email Notifications" section:
   - **Gmail Sender Address**: your-email@gmail.com
   - **Gmail App Password**: paste the 16-character password (no spaces)
   - **Notification Email Address**: where you want to receive notifications
3. Check the notification triggers you want
4. Click "Save Settings"

## Troubleshooting

### Error: "Username and Password not accepted"
- **Cause**: Using regular Gmail password instead of App Password
- **Solution**: Follow Step 2 above to generate an App Password

### Error: "Less secure app access"
- **Cause**: Gmail doesn't allow regular passwords anymore
- **Solution**: Must use App Password (requires 2FA enabled)

### Can't find App Passwords setting
- **Cause**: 2-Factor Authentication is not enabled
- **Solution**: Enable 2FA first (Step 1)

## Security Notes
- App Passwords are safer than your main password
- You can revoke App Passwords anytime without changing your main password
- Each app/device should have its own App Password
- Never share your App Password

## Quick Links
- 2FA Setup: https://myaccount.google.com/security
- App Passwords: https://myaccount.google.com/apppasswords
- Gmail Help: https://support.google.com/mail/?p=BadCredentials

## Example Configuration
```
Gmail Sender Address: trader@gmail.com
Gmail App Password: abcdefghijklmnop (16 chars, no spaces)
Notification Email: trader@gmail.com (can be same or different)
```

## Testing
After configuration, the bot will automatically send emails when:
- ✅ AI executes BUY or SELL (if "Notify on action" is checked)
- ✅ Position size ratio is reached (if checked)
- ✅ AI skips action due to low confidence (if checked)

---
**Important**: The app password is stored securely in your database and masked in the UI as '***'
