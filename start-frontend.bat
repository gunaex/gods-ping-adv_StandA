@echo off
echo.
echo ========================================
echo   Gods Ping - Frontend Startup
echo   七福神 Shichi-Fukujin
echo ========================================
echo.

cd frontend

echo Installing/Updating dependencies...
call npm install

echo.
echo Starting Vite development server...
echo.
echo Frontend will be available at: http://localhost:5173
echo.
echo Default login:
echo Username: Admin
echo Password: K@nph0ng69
echo.

call npm run dev

pause
