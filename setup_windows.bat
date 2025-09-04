@echo off
echo ======================================
echo  StockBreak Pro - Windows Setup
echo ======================================
echo.

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo ✓ Python found

echo.
echo [2/4] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)
echo ✓ Node.js found

echo.
echo [3/4] Installing backend dependencies...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)
echo ✓ Backend dependencies installed

echo.
echo [4/4] Installing frontend dependencies...
cd ..\frontend
npm install
if errorlevel 1 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)
echo ✓ Frontend dependencies installed

cd ..
echo.
echo ======================================
echo  Setup Complete!
echo ======================================
echo.
echo To start StockBreak Pro:
echo 1. Run: start_stockbreak.cmd
echo.
echo Or manually:
echo 1. Backend: cd backend ^& python -m uvicorn server:app --reload
echo 2. Frontend: cd frontend ^& npm start
echo.
pause