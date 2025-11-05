# 🎌 Gods Ping - First Time Startup Guide

## Quick Start (5 Minutes)

### Step 1: Activate Python Environment
```bash
# Open terminal in project root (D:\git\gods-ping)
.venv\Scripts\activate
```

### Step 2: Start Backend Server
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```
**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Backend API:** http://localhost:8000
**API Docs:** http://localhost:8000/docs (Swagger UI)

### Step 3: Start Frontend (New Terminal)
```bash
# Open NEW terminal
cd frontend
npm run dev
```
**Expected Output:**
```
VITE v5.0.8  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h to show help
```

**Frontend App:** http://localhost:5173

---

## 📋 Complete Operation Steps

### Prerequisites Check
```bash
# Check Python version (should be 3.13.9)
python --version

# Check Node.js (should be installed)
node --version

# Check npm (should be installed)
npm --version
```

---

### Backend Setup & Start

#### 1. Activate Virtual Environment
```bash
# Windows PowerShell
.venv\Scripts\activate

# You should see (.venv) in your prompt
```

#### 2. Verify Backend Dependencies
```bash
# Check installed packages
python -c "import fastapi, uvicorn, sqlalchemy, pydantic; print('✅ All packages installed')"
```

#### 3. Initialize Database
```bash
# The database will auto-create on first run, but you can verify:
python check_db.py
```

**Expected Output:**
```
✅ Database Tables Created:
  - users
  - logs
  - trades
  - bot_configs

✅ Logs Table (13 columns):
  - id, timestamp, category, level
  - message, details
  - user_id, symbol, bot_type
  - ai_recommendation, ai_confidence, ai_executed, execution_reason
```

#### 4. Start Backend Server
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**Or use the batch file:**
```bash
# From project root
start-backend.bat
```

---

### Frontend Setup & Start

#### 1. Open New Terminal (keep backend running)

#### 2. Navigate to Frontend
```bash
cd frontend
```

#### 3. Verify Node Modules (already installed)
```bash
# Should show node_modules folder
dir
```

#### 4. Start Development Server
```bash
npm run dev
```

**Or use the batch file:**
```bash
# From project root
start-frontend.bat
```

---

## 🧪 Testing After Startup

### Test 1: Backend Health Check
Open browser: http://localhost:8000

**Expected Response:**
```json
{
  "message": "Gods Ping API - Shichi-Fukujin Trading Platform",
  "status": "running",
  "version": "1.0.0",
  "server_time": "2025-11-05T10:30:00.123456",
  "server_timezone": "UTC",
  "timestamp": 1730800200
}
```

### Test 2: API Documentation
Open: http://localhost:8000/docs

**You should see:**
- ✅ Swagger UI with all endpoints
- ✅ Authentication endpoints (/api/auth/*)
- ✅ Trading endpoints (/api/trading/*)
- ✅ Bot endpoints (/api/bots/*)
- ✅ Log endpoints (/api/logs/*)

### Test 3: Frontend Loading
Open: http://localhost:5173

**You should see:**
- ✅ Login page with "Gods Ping" title
- ✅ "七福神 Shichi-Fukujin" subtitle
- ✅ Username/Password fields

### Test 4: Login (Default Admin)
```
Username: Admin
Password: admin123
```

**After login, you should see:**
- ✅ Shichi-Fukujin dashboard
- ✅ Real-time clock with timezone
- ✅ Trading pair selector
- ✅ "Logs" button in header
- ✅ "Settings" button
- ✅ "Logout" button

---

## 🔍 Run Test Scripts

### Test Logging System
```bash
# From project root (with .venv activated)
python test_logging_system.py
```

**Expected Output:**
```
🧪 Testing Logging System...

✅ Test 1: Create error log
✅ Test 2: Create user log
✅ Test 3: Create AI thinking log
✅ Test 4: Create AI action log
✅ Test 5: Create trading log
✅ Test 6: Retrieve logs by category
✅ Test 7: AI comparison

All tests passed! 🎉
```

### Verify Database
```bash
python check_db.py
```

### Manual API Test (using curl or PowerShell)
```powershell
# Test health endpoint
Invoke-RestMethod -Uri http://localhost:8000 -Method Get

# Test login
$body = @{
    username = "Admin"
    password = "admin123"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/api/auth/login -Method Post -Body $body -ContentType "application/json"
```

---

## 📱 Using the Application

### 1. Login
- Use default credentials: `Admin` / `admin123`
- After first login, change password in Settings

### 2. View Logs
- Click "Logs" button in top-right header
- See categorized logs in tabs:
  - **All Logs**: Every log entry
  - **AI Thinking vs Actions**: Compare AI decisions with actual trades

### 3. Change Settings
- Click "Settings" gear icon
- Configure:
  - Binance API keys (encrypted in database)
  - Trading preferences
  - Risk management settings

### 4. Monitor Trading (when bots are active)
- Trading pairs display in main panel
- AI recommendations shown in real-time
- Bot status indicators
- Market data updates

---

## 🛠️ Troubleshooting

### Backend Won't Start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed (replace PID)
taskkill /PID <PID> /F

# Restart backend
cd backend
uvicorn app.main:app --reload --port 8000
```

### Frontend Won't Start
```bash
# Check if port 5173 is in use
netstat -ano | findstr :5173

# Try different port
npm run dev -- --port 5174
```

### Database Issues
```bash
# Delete and recreate database
del gods_ping.db
python check_db.py
```

### Import Errors
```bash
# Ensure virtual environment is activated
.venv\Scripts\activate

# Verify packages
python -c "import fastapi, uvicorn, sqlalchemy; print('OK')"
```

### TypeScript Errors
```bash
# Restart TypeScript server in VS Code
# Press Ctrl+Shift+P -> "TypeScript: Restart TS Server"

# Or reinstall node modules
cd frontend
rmdir /s /q node_modules
npm install
```

---

## 🎯 Next Steps After First Start

1. **Explore API Docs**: http://localhost:8000/docs
2. **Configure Binance API**: Settings → Add API keys
3. **Test Logging**: Click "Logs" button, check categories
4. **Review Code**: Check `backend/app/` and `frontend/src/`
5. **Start Trading Bot**: Configure in Settings, activate bots

---

## 📊 Port Summary

| Service | Port | URL |
|---------|------|-----|
| Backend API | 8000 | http://localhost:8000 |
| API Docs | 8000 | http://localhost:8000/docs |
| Frontend | 5173 | http://localhost:5173 |
| Database | - | SQLite file (gods_ping.db) |

---

## 🔐 Default Credentials

**Username:** `Admin`  
**Password:** `admin123`

⚠️ **Change these after first login!**

---

## 💡 Tips

- Keep both terminals open (backend + frontend)
- Backend auto-reloads on code changes (`--reload` flag)
- Frontend auto-refreshes on file changes (Vite HMR)
- Check browser console (F12) for frontend errors
- Check terminal output for backend errors
- Use API docs for testing endpoints directly

---

## 🎉 You're Ready!

Both servers should now be running:
- ✅ Backend: http://localhost:8000
- ✅ Frontend: http://localhost:5173

Open the frontend URL in your browser and start exploring! 🚀
