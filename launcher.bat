@echo off
title StockBreak Pro - Indian Stock Breakout Screener
color 0A

echo ========================================
echo    StockBreak Pro Launcher v2.0
echo ========================================
echo.
echo Starting Indian Stock Breakout Screener...
echo.

REM Check if we're in the right directory
if not exist "backend\server.py" (
    echo ERROR: Please run this script from the StockBreakOutScanner directory!
    echo Current directory: %CD%
    echo Expected files: backend\server.py, frontend\package.json
    pause
    exit /b 1
)

echo [1/5] Checking system requirements...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from https://python.org/downloads/
    pause
    exit /b 1
) else (
    echo ✓ Python found
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
) else (
    echo ✓ Node.js found
)

echo.
echo [2/5] Starting MongoDB service...

REM Try to start MongoDB service
net start MongoDB >nul 2>&1
if errorlevel 1 (
    echo ⚠ MongoDB service not found or already running
    echo Checking if MongoDB is available on port 27017...
    
    REM Check if MongoDB is accessible
    timeout /t 2 >nul
    netstat -an | findstr ":27017" >nul
    if errorlevel 1 (
        echo ERROR: MongoDB is not running on port 27017!
        echo Please install MongoDB or start it manually
        echo Download from: https://www.mongodb.com/try/download/community
        pause
        exit /b 1
    ) else (
        echo ✓ MongoDB is accessible on port 27017
    )
) else (
    echo ✓ MongoDB service started successfully
)

echo.
echo [3/5] Setting up backend environment...

REM Navigate to backend directory
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

REM Check if requirements are installed
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Installing Python dependencies...
    echo This may take a few minutes on first run...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install Python dependencies!
        pause
        exit /b 1
    )
) else (
    echo ✓ Python dependencies already installed
)

echo.
echo [4/5] Setting up frontend environment...

REM Navigate to frontend directory
cd ..\frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    echo This may take several minutes on first run...
    npm install
    if errorlevel 1 (
        echo ERROR: Failed to install Node.js dependencies!
        pause
        exit /b 1
    )
) else (
    echo ✓ Node.js dependencies already installed
)

echo.
echo [5/5] Starting applications...

REM Create environment files if they don't exist
if not exist ".env" (
    echo Creating frontend .env file...
    echo REACT_APP_BACKEND_URL=http://localhost:8001> .env
)

cd ..\backend
if not exist ".env" (
    echo Creating backend .env file...
    (
        echo MONGO_URL=mongodb://localhost:27017
        echo DB_NAME=stockbreak_pro
        echo CORS_ORIGINS=http://localhost:3000
    ) > .env
)

echo.
echo ✓ All prerequisites met! Starting services...
echo.
echo ========================================
echo         Application Status
echo ========================================

REM Start backend in background
echo Starting Backend Server on http://localhost:8001...
start "StockBreak Pro Backend" /min cmd /c "cd /d %CD% && venv\Scripts\activate && uvicorn server:app --host 0.0.0.0 --port 8001 --reload"

REM Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 5 >nul

REM Check if backend is running
for /l %%i in (1,1,10) do (
    curl -s http://localhost:8001/api/ >nul 2>&1
    if not errorlevel 1 (
        echo ✓ Backend server is running
        goto backend_ready
    )
    echo Waiting for backend... (%%i/10)
    timeout /t 2 >nul
)

echo ⚠ Backend may still be starting, continuing anyway...

:backend_ready

REM Start frontend
cd ..\frontend
echo.
echo Starting Frontend Server on http://localhost:3000...
start "StockBreak Pro Frontend" cmd /c "cd /d %CD% && npm start"

REM Wait for frontend to start
echo Waiting for frontend to initialize...
timeout /t 10 >nul

echo.
echo ========================================
echo        StockBreak Pro Started!
echo ========================================
echo.
echo 🚀 Frontend: http://localhost:3000
echo 🔧 Backend:  http://localhost:8001
echo 📚 API Docs: http://localhost:8001/docs
echo.
echo The application should open automatically in your browser.
echo If not, please navigate to http://localhost:3000
echo.
echo To stop the application:
echo - Close this window
echo - Or press Ctrl+C in the backend/frontend windows
echo.

REM Open browser automatically
timeout /t 3 >nul
start http://localhost:3000

echo ✓ Application launched successfully!
echo.
echo Press any key to keep this window open...
echo (Closing this window will NOT stop the servers)
pause >nul

echo.
echo To completely stop all services, run: stop_stockbreak.bat
echo.