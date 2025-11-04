@echo off
echo.
echo ========================================
echo   Gods Ping - Backend Server Startup
echo   七福神 Shichi-Fukujin
echo ========================================
echo.

cd backend

echo Installing/Updating dependencies...
pip install -r requirements.txt

echo.
echo Starting FastAPI backend server...
echo.
echo Backend will be available at: http://localhost:8000
echo API documentation at: http://localhost:8000/docs
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
