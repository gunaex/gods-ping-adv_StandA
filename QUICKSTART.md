# Gods Ping - Quick Start Instructions

## 🎯 Fastest Way to Get Started

### Option 1: Using Startup Scripts (Windows)

1. **Start Backend** (in one terminal):
   ```cmd
   start-backend.bat
   ```

2. **Start Frontend** (in another terminal):
   ```cmd
   start-frontend.bat
   ```

3. **Open Browser**:
   - Go to http://localhost:5173
   - Login with: Admin / K@nph0ng69

### Option 2: Manual Start

#### Terminal 1 - Backend:
```cmd
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

#### Terminal 2 - Frontend:
```cmd
cd frontend
npm install
npm run dev
```

## 📋 First Time Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 18+ installed
- [ ] Git installed (already have this)
- [ ] Two terminals open

## 🎮 What to Do After Startup

1. **Login** with Admin credentials
2. **Go to Settings** (gear icon in header)
3. **Configure**:
   - Set budget (e.g., $10,000 for paper trading)
   - Choose risk level (start with Conservative)
   - Ensure Paper Trading is ON
4. **Select Trading Pair** (e.g., BTC/USDT)
5. **Try AI Recommendation** - click refresh to see analysis
6. **View Market Chart** - real-time candlestick data
7. **Test a Bot** - try DCA Bot with small amounts in paper mode
8. **Try Gods Hand** - execute autonomous AI trade

## ⚠️ Important Notes

- **Paper Trading is ON by default** - no real money used
- **Backend must start first** - frontend needs it
- **First startup takes longer** - installing dependencies
- **All data is in SQLite** - gods_ping.db in backend folder

## 🔍 URLs Reference

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (interactive Swagger UI)
- **Alternative API Docs**: http://localhost:8000/redoc

## 🛟 Troubleshooting

**Backend won't start?**
- Check if Python is installed: `python --version`
- Try: `python -m pip install --upgrade pip`

**Frontend won't start?**
- Check if Node.js is installed: `node --version`
- Delete node_modules: `rd /s /q node_modules` then `npm install`

**Can't login?**
- Check backend is running at http://localhost:8000
- Check browser console (F12) for errors

## 🎉 You're All Set!

Once both servers are running and you can login, you have a fully functional AI-powered crypto trading platform!

**See SETUP_GUIDE.md for detailed feature documentation.**
