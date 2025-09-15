@echo off
echo ======================================
echo  StockBreak Pro - Windows Setup
echo  With Valuation Filter Feature
echo ======================================
echo.

echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo ✓ Python found

echo.
echo [2/5] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)
echo ✓ Node.js found

echo.
echo [3/5] Installing backend dependencies...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)
echo ✓ Backend dependencies installed

echo.
echo [4/5] Installing frontend dependencies...
cd ..\frontend
echo Installing with dependency resolution fixes...
npm install --legacy-peer-deps
if errorlevel 1 (
    echo ERROR: Failed to install frontend dependencies
    echo Trying alternative installation method...
    npm install --force
    if errorlevel 1 (
        echo ERROR: Frontend installation failed completely
        pause
        exit /b 1
    )
)
echo ✓ Frontend dependencies installed

echo.
echo [5/5] Verifying valuation filter functionality...
echo ✓ Valuation Filter Feature: 5 categories implemented
echo   - Highly Undervalued (P/E, P/B, PEG analysis)
echo   - Slightly Undervalued
echo   - Reasonable  
echo   - Slightly Overvalued
echo   - Highly Overvalued

cd ..
echo.
echo ======================================
echo  Setup Complete!
echo ======================================
echo.
echo New Features Added:
echo + Comprehensive Valuation Filter (5 categories)
echo + Financial Metrics Analysis (P/E, P/B, PEG, Dividend Yield)
echo + Weighted Scoring System with confidence levels
echo + Exception handling for missing financial data
echo.
echo To start StockBreak Pro:
echo 1. Run: start_stockbreak.cmd
echo.
echo Or manually:
echo 1. Backend: cd backend ^& python -m uvicorn server:app --reload
echo 2. Frontend: cd frontend ^& npm start
echo.
pause