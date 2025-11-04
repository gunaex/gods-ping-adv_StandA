# Gods Ping - Complete Setup Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Start Backend Server

```bash
# From backend directory
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend running at**: http://localhost:8000
**API docs**: http://localhost:8000/docs

### Step 3: Install Frontend Dependencies

```bash
cd frontend
npm install
```

### Step 4: Start Frontend

```bash
# From frontend directory
npm run dev
```

**Frontend running at**: http://localhost:5173

### Step 5: Login

Open http://localhost:5173 and login with:
- Username: `Admin`
- Password: `K@nph0ng69`

## 📋 Complete Feature List

### 1. Trading Pair Selector
- 9 cryptocurrencies (BTC, ETH, BNB, SOL, XRP, USDC, ADA, DOGE, DOT)
- Fiat currency support (USD/THB)
- Real-time pair switching

### 2. AI Recommendation
- Technical indicators (RSI, SMA, MACD, Bollinger Bands)
- BUY/SELL/HOLD recommendations
- Confidence scoring
- Reasoning display

### 3. Market Data & Charts
- Real-time candlestick charts (TradingView quality)
- Live ticker (updates every 10s)
- 24h price changes
- Volume data
- Multiple timeframes (1h default)

### 4. Trading Bots

#### Grid Bot
- Range-bound trading strategy
- Configurable price levels
- Automatic buy/sell orders
- Paper trading support

#### DCA Bot
- Dollar-cost averaging strategy
- Customizable intervals
- Fixed amount purchases
- Set-and-forget automation

### 5. Advanced AI Analysis
- Multi-timeframe trends (1h, 4h, 1d)
- Support/Resistance levels
- Volatility indicators
- Real-time updates

### 6. Gods Hand (Autonomous AI Trading)
- Fully autonomous decision making
- Risk assessment dashboard
- Fee protection
- Confidence-based execution
- Paper trading mode
- Real-time status monitoring

### 7. Unified Settings Modal
- Trading configuration
- Risk management
- API keys management
- User creation (admin only)
- All settings in one place

## 🔧 Configuration

### Backend (.env) - Optional

Create `backend/.env`:

```env
# Database (uses SQLite by default)
DATABASE_URL=sqlite:///./gods_ping.db

# JWT Secret (auto-generated if not provided)
SECRET_KEY=your-random-secret-key-minimum-32-characters

# Optional: For live trading
BINANCE_API_KEY=your_binance_api_key
BINANCE_API_SECRET=your_binance_api_secret
```

### Frontend (.env) - Optional

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000/api
```

## 📊 Usage Instructions

### Paper Trading (Default - Recommended)

1. Login as Admin
2. Go to Settings → Verify "Paper Trading: ON"
3. Configure your preferences
4. Select trading pair
5. Start any bot or use Gods Hand
6. All trades are simulated (no real money)

### Live Trading (Advanced - Use with Caution)

1. Get Binance API keys from https://www.binance.com/en/my/settings/api-management
2. Go to Settings → API Keys section
3. Enter your Binance API Key and Secret
4. Save API keys
5. Go to Settings → Paper Trading: OFF
6. **⚠️ WARNING**: Real trades will be executed!

## 🛡️ Security Best Practices

1. **Change Admin Password**
   - Modify `ADMIN_PASSWORD_HASH` in `backend/app/auth.py`
   - Or create a new admin user

2. **Use Strong JWT Secret**
   - Generate random key: `python -c "import secrets; print(secrets.token_hex(32))"`
   - Add to `.env`: `SECRET_KEY=generated_key`

3. **API Keys**
   - Never commit API keys to version control
   - Use read-only keys for testing
   - Enable IP restrictions on Binance

4. **Database**
   - Use PostgreSQL for production
   - Regular backups
   - Secure connection strings

## 🎯 Trading Strategy Tips

### Grid Bot Best For:
- Range-bound markets
- Sideways price action
- Known support/resistance levels

### DCA Bot Best For:
- Long-term accumulation
- Dollar-cost averaging
- Reducing timing risk

### Gods Hand Best For:
- Automated AI trading
- When you trust AI recommendations
- Testing with paper trading first

## 🐛 Common Issues

### Port 8000 Already in Use

```bash
# Use different port
uvicorn app.main:app --reload --port 8001
```

### Frontend Can't Connect to Backend

1. Check backend is running
2. Verify CORS settings in `main.py`
3. Check firewall settings

### Database Errors

```bash
# Delete and recreate
rm gods_ping.db
# Restart backend - auto-creates tables
```

### API Rate Limits

- Binance has rate limits
- Use paper trading for testing
- Implement delays between requests

## 📈 Next Steps

1. **Test with Paper Trading**
   - Familiarize yourself with all features
   - Test each bot type
   - Monitor AI recommendations

2. **Configure Risk Settings**
   - Set appropriate budget
   - Configure risk level (conservative recommended)
   - Set max daily loss percentage

3. **Start Small (Live Trading)**
   - Use small amounts initially
   - Monitor first few trades manually
   - Gradually increase if successful

4. **Monitor Performance**
   - Check trade history
   - Review AI accuracy
   - Adjust settings based on results

## 🌟 Pro Tips

1. **AI Recommendations**: Higher confidence (>70%) = more reliable signals
2. **Grid Bot**: Works best in 10-20% price ranges
3. **DCA Bot**: Best for long-term (weeks/months)
4. **Gods Hand**: Test with paper trading for 1 week first
5. **Risk Level**: Start conservative, increase gradually
6. **Timeframes**: Use 1h for day trading, 1d for long-term

## 📞 Support

For issues or questions:
1. Check this guide
2. Review API documentation at http://localhost:8000/docs
3. Check console logs (F12 in browser)
4. Review backend logs in terminal

## 🎉 You're Ready!

Your Gods Ping (Shichi-Fukujin) trading platform is now set up and ready to use. Start with paper trading to get comfortable with the interface and features.

**May the Seven Gods of Fortune (七福神) bring prosperity to your trades!** 🍀
