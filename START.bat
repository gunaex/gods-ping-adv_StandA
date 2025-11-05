@echo off
echo ========================================
echo   GODS PING - Starting All Servers
echo ========================================
echo.
echo Starting Backend and Frontend servers...
echo.
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:5173
echo.
echo Press Ctrl+C in each window to stop
echo ========================================
echo.

REM Activate virtual environment and start backend in new window
start "Gods Ping - Backend" cmd /k "cd /d %~dp0 && .venv\Scripts\activate.bat && cd backend && python -m uvicorn app.main:app --reload --port 8000"

REM Wait 2 seconds for backend to initialize
timeout /t 2 /nobreak >nul

REM Start frontend in new window
start "Gods Ping - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo   Both servers started!
echo ========================================
echo.
echo Backend window opened (black window)
echo Frontend window opened (black window)
echo.
echo Wait a few seconds for servers to start, then:
echo Open browser: http://localhost:5173
echo.
echo Login:
echo   Username: Admin
echo   Password: K@nph0ng69
echo.
echo Close both terminal windows to stop servers.
echo.
pause
