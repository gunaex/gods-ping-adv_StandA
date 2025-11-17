# Gods Ping (七福神 Shichi-Fukujin)

A streamlined, single-page AI-powered crypto trading platform.

## Features

- 🔐 **Secure Admin Access**: Hardcoded admin + create 1 additional user
- 💱 **Fiat Currency Support**: Trade with THB/USD
- 📊 **Real-time Market Data**: Live candlestick charts
- 🤖 **AI Trading**: Recommendations, Grid Bot, DCA Bot, Gods Hand
- 🚀 **Gods Mode**: Advanced Meta-Model AI optimized for sideways-down markets
- ⚙️ **Unified Settings**: All configurations in one place
- 📝 **Paper Trading**: Test strategies without risk

## Supported Trading Pairs

ETH, USDT, BNB, SOL, XRP, USDC, ADA, DOGE, DOT (all /USDT)

## Quick Start

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev
```

## Default Admin Credentials
- Username: `Admin`
- Password: `K@nph0ng69`

⚠️ **Change this in production!**

## Tech Stack

- Backend: FastAPI, SQLAlchemy, SQLite (default) or PostgreSQL
- Exchange: Native Binance Thailand REST client (no ccxt required for TH)
- Frontend: React, TypeScript, Vite, lightweight-charts
- AI: Custom trading algorithms with risk management
- Gods Mode: Meta-Model AI (Forecaster + Classifier + Gating Logic)

## Environment Variables

### Backend (.env)
```
# Defaults to SQLite file ./gods_ping.db if not set
DATABASE_URL=sqlite:///./gods_ping.db
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
SECRET_KEY=your_jwt_secret
ENVIRONMENT=production
ALLOW_REGISTRATION=false
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api
```

## License

Private - For authorized use only

---

## 🚀 Deployment

Ready to deploy to production? See detailed guides:

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete deployment guide for Render + Vercel
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Step-by-step checklist

### Quick Deploy

**Backend (Render):**
1. Push to GitHub
2. Connect repository to Render
3. Set environment variables
4. Deploy!

**Frontend (Vercel):**
1. Connect repository to Vercel
2. Set `VITE_API_URL` to your Render backend URL
3. Deploy!

**Free Hosting:** Both Render and Vercel offer free tiers! 🎉

---

## API Notes

- Validate Binance TH keys: GET /api/settings/validate-keys
- Gods Hand start: POST /api/bot/gods-hand/start?continuous=true&interval_seconds=60
- Gods Hand status: GET /api/bot/status
- Gods Hand performance: GET /api/bot/gods-hand/performance?days=7
	- Returns summary (win rate, net/gross PnL, counts), open positions, and last 5 trades for bot_type=gods_hand.
- Reset paper trading: POST /api/bot/paper-trading/reset?symbol=BTC/USDT
- Price forecast: GET /api/market/forecast/BTC/USDT?forecast_hours=6

---

## 🚀 Gods Mode - Advanced AI

**New!** Gods Mode is an advanced Meta-Model AI system optimized for sideways-down markets.

### Architecture

- **Model A (Forecaster)**: LSTM-inspired price prediction with momentum
- **Model B (Classifier)**: Market regime detection (Parabolic SAR + RSI + ATR)
- **Meta-Model**: Ensemble gating logic that decides when to use each model

### How to Enable

1. Go to Gods Hand panel → Click **⚙️ Settings**
2. Toggle **Gods Mode** ON (🚀 GODS MODE)
3. Click **Save Settings**
4. A new "GODS MODE - Meta-Model AI Analytics" panel will appear

### Documentation

- **[GODS_MODE_GUIDE.md](GODS_MODE_GUIDE.md)** - Complete guide with examples
- **[GODS_MODE_IMPLEMENTATION.md](GODS_MODE_IMPLEMENTATION.md)** - Technical details

### When to Use

✅ **Use Gods Mode** for:
- Sideways or bearish markets
- High volatility conditions
- SHORT/SELL strategies

❌ **Use Standard AI** for:
- Strong uptrends
- Stable trending markets

**Always test in paper trading first!**

