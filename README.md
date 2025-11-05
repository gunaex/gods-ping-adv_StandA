# Gods Ping (七福神 Shichi-Fukujin)

A streamlined, single-page AI-powered crypto trading platform.

## Features

- 🔐 **Secure Admin Access**: Hardcoded admin + create 1 additional user
- 💱 **Fiat Currency Support**: Trade with THB/USD
- 📊 **Real-time Market Data**: Live candlestick charts
- 🤖 **AI Trading**: Recommendations, Grid Bot, DCA Bot, Gods Hand
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

## API Notes

- Validate Binance TH keys: GET /api/settings/validate-keys
- Gods Hand start: POST /api/bot/gods-hand/start?continuous=true&interval_seconds=60
- Gods Hand status: GET /api/bot/status
- Gods Hand performance: GET /api/bot/gods-hand/performance?days=7
	- Returns summary (win rate, net/gross PnL, counts), open positions, and last 5 trades for bot_type=gods_hand.
