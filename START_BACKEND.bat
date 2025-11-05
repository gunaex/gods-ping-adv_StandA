@echo off
echo ========================================
echo   GODS PING - Quick Start
echo ========================================
echo.

echo Step 1: Activating Python virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Step 2: Starting Backend Server...
echo Backend will be available at: http://localhost:8000
echo API Docs at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

cd backend
python -m uvicorn app.main:app --reload --port 8000
