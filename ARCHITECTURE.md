# Gods Ping System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    GODS PING (七福神)                            │
│              Shichi-Fukujin Trading Platform                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + TypeScript)                 │
│                    Port: 5173                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  LoginPage Component                                      │  │
│  │  - Admin/K@nph0ng69 authentication                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                          │                                       │
│                          ▼                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Shichi-Fukujin Single Page Dashboard                    │  │
│  │                                                            │  │
│  │  ┌────────────────────┬────────────────────┐            │  │
│  │  │ 1. Trading Pair    │ 2. AI Recommend    │            │  │
│  │  │    Selector        │    -ation          │            │  │
│  │  └────────────────────┴────────────────────┘            │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────┐            │  │
│  │  │ 3. Market Data & Candlestick Chart        │            │  │
│  │  │    (TradingView-quality)                  │            │  │
│  │  └──────────────────────────────────────────┘            │  │
│  │                                                            │  │
│  │  ┌────────────────────┬────────────────────┐            │  │
│  │  │ 4. Bots Panel      │ 5. Advanced AI     │            │  │
│  │  │  - Grid Bot        │    Analysis        │            │  │
│  │  │  - DCA Bot         │  - Trends          │            │  │
│  │  └────────────────────┴────────────────────┘            │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────┐            │  │
│  │  │ 6. Gods Hand Autonomous Trading           │            │  │
│  │  │  - Config | Risk | Fees | Paper Trade    │            │  │
│  │  └──────────────────────────────────────────┘            │  │
│  │                                                            │  │
│  │  [⚙️ Settings Button] → Unified Settings Modal           │  │
│  │                                                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  State: Zustand | Charts: lightweight-charts | Icons: Lucide   │
└──────────────────────────────────────────────────────────────────┘
                              │
                              │ REST API (Axios)
                              │
┌─────────────────────────────▼─────────────────────────────────┐
│                    BACKEND (FastAPI + Python)                  │
│                    Port: 8000                                  │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  API Endpoints (main.py)                                │  │
│  │                                                          │  │
│  │  Authentication:                                        │  │
│  │  • POST /api/auth/login                                │  │
│  │  • POST /api/auth/create-user (admin only)            │  │
│  │  • GET  /api/auth/me                                   │  │
│  │                                                          │  │
│  │  Market Data:                                           │  │
│  │  • GET /api/market/ticker/{symbol}                     │  │
│  │  • GET /api/market/candles/{symbol}                    │  │
│  │  • GET /api/market/orderbook/{symbol}                  │  │
│  │                                                          │  │
│  │  AI & Trading:                                          │  │
│  │  • GET /api/ai/recommendation/{symbol}                 │  │
│  │  • GET /api/ai/analysis/{symbol}                       │  │
│  │  • POST /api/trade/execute                             │  │
│  │  • GET  /api/trade/history                             │  │
│  │                                                          │  │
│  │  Bots:                                                  │  │
│  │  • POST /api/bot/grid/start                            │  │
│  │  • POST /api/bot/dca/start                             │  │
│  │  • POST /api/bot/gods-hand/start                       │  │
│  │  • POST /api/bot/{type}/stop                           │  │
│  │  • GET  /api/bot/status                                │  │
│  │                                                          │  │
│  │  Settings:                                              │  │
│  │  • GET/PUT /api/settings/bot-config                    │  │
│  │  • POST    /api/settings/api-keys                      │  │
│  └─────────────────────────────────────────────────────────┘  │
│                          │                                      │
│         ┌────────────────┼────────────────┐                   │
│         ▼                ▼                ▼                    │
│  ┌──────────┐   ┌──────────┐   ┌──────────────┐              │
│  │ auth.py  │   │ market.py│   │ ai_engine.py │              │
│  │          │   │          │   │              │              │
│  │ • JWT    │   │ • ccxt   │   │ • RSI        │              │
│  │ • Bcrypt │   │ • Binance│   │ • SMA        │              │
│  │ • Admin  │   │ • OHLCV  │   │ • MACD       │              │
│  │ • Tokens │   │ • Ticker │   │ • Bollinger  │              │
│  └──────────┘   └──────────┘   │ • Multi-TF   │              │
│                                  └──────────────┘              │
│                          │                                      │
│                          ▼                                      │
│                 ┌──────────────┐                               │
│                 │   bots.py    │                               │
│                 │              │                               │
│                 │ • Grid Bot   │                               │
│                 │ • DCA Bot    │                               │
│                 │ • Gods Hand  │                               │
│                 │ • Risk Mgmt  │                               │
│                 └──────────────┘                               │
│                          │                                      │
│                          ▼                                      │
│         ┌─────────────────────────────────┐                   │
│         │  Database (SQLAlchemy + SQLite)  │                   │
│         │                                   │                   │
│         │  Tables:                          │                   │
│         │  • users (Admin + 1 user)        │                   │
│         │  • trades (history)              │                   │
│         │  • bot_configs (per user)        │                   │
│         └─────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ ccxt API
                              │
┌─────────────────────────────▼─────────────────────────────────┐
│                    BINANCE EXCHANGE                            │
│                    (External API)                              │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  • Real-time market data                                       │
│  • OHLCV candlestick data                                     │
│  • Order execution (when live trading)                        │
│  • Account balance                                            │
│  • 9 Trading pairs: BTC, ETH, BNB, SOL, XRP, etc.            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘


DATA FLOW:
──────────

1. User Login → Frontend → Backend Auth → JWT Token
2. Select Pair → Frontend → Backend → Binance → Real-time Price
3. View Chart → Frontend requests candles → Backend (ccxt) → Binance
4. AI Recommendation → Backend calculates indicators → Returns BUY/SELL/HOLD
5. Start Bot → Frontend → Backend (bot logic) → Database (save trades)
6. Gods Hand → AI analyzes → Risk assessment → Execute (paper/live)
7. Settings → Frontend modal → Backend updates → Database


SECURITY LAYERS:
────────────────

Frontend → JWT Token in localStorage → Backend validates
Backend → Bcrypt password hashing
Backend → Encrypted API keys (XOR + Base64)
Backend → Admin-only endpoints
Database → SQLite (upgrade to PostgreSQL for production)


TRADING MODES:
──────────────

Paper Trading (Default):
  User → Frontend → Backend → Simulated execution → Database only
  
Live Trading (Optional):
  User → Frontend → Backend → Binance API → Real trades → Database


SUPPORTED FEATURES:
───────────────────

✅ 9 Trading pairs (all /USDT)
✅ 2 Fiat currencies (USD, THB)
✅ 2 Users maximum (Admin + 1)
✅ 3 Bot types (Grid, DCA, Gods Hand)
✅ 6 Dashboard sections (single page)
✅ 1 Unified settings modal
✅ Real-time updates (10s intervals)
✅ Paper & Live trading modes
✅ Risk management & fee protection
✅ Technical analysis (5 indicators)
✅ Multi-timeframe analysis (3 TFs)


DEPLOYMENT:
───────────

Local Development: ✅ Ready (start-backend.bat, start-frontend.bat)
Production: Use PostgreSQL + NGINX + SSL certificate
```
