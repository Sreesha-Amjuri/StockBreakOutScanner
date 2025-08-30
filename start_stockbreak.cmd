@echo off
REM StockBreak Pro Simple Launcher
REM Right-click this file and select "Run as Administrator" if needed

title StockBreak Pro Launcher
color 02

echo.
echo =============================================
echo          StockBreak Pro Launcher
echo =============================================
echo.

REM Check current directory
echo Checking installation directory...
if not exist "backend\server.py" (
    echo ERROR: Run this from StockBreakOutScanner folder!
    echo Current location: %CD%
    pause
    exit
)

echo ✓ Found StockBreak Pro installation
echo.

REM Start MongoDB
echo [1/3] Starting MongoDB...
net start MongoDB 2>nul || echo MongoDB already running or needs manual start

REM Start Backend
echo [2/3] Starting Backend...
cd backend
start /min "Backend" cmd /k "venv\Scripts\activate && uvicorn server:app --host 0.0.0.0 --port 8001"
cd ..

REM Start Frontend
echo [3/3] Starting Frontend...
cd frontend
start /min "Frontend" cmd /k "npm start"
cd ..

echo.
echo ✓ Services starting...
echo ✓ Backend: http://localhost:8001
echo ✓ Frontend: http://localhost:3000
echo.
echo Opening browser in 10 seconds...
timeout 10
start http://localhost:3000

echo.
echo StockBreak Pro is now running!
pause