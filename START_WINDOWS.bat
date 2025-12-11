@echo off
REM =====================================================
REM StockBreak Pro - Windows Launcher
REM =====================================================
REM Run this file to start the application

title StockBreak Pro - Starting...
color 0A

echo.
echo ========================================================
echo              STOCKBREAK PRO - WEB APPLICATION
echo ========================================================
echo.

REM Check if running from correct directory
if not exist "backend\server.py" (
    echo [ERROR] Cannot find backend\server.py
    echo.
    echo Please run this file from the StockBreakPro folder!
    echo Current directory: %CD%
    echo.
    pause
    exit /b 1
)

echo [INFO] Found StockBreak Pro installation
echo [INFO] Location: %CD%
echo.

REM =====================================================
REM STEP 1: Check Prerequisites
REM =====================================================

echo [STEP 1/5] Checking prerequisites...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
echo [OK] Python found

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found!
    echo Please install Node.js from: https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] Node.js found

REM Check npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm not found!
    echo Please reinstall Node.js
    pause
    exit /b 1
)
echo [OK] npm found

echo.

REM =====================================================
REM STEP 2: Start MongoDB
REM =====================================================

echo [STEP 2/5] Starting MongoDB...
echo.

REM Try to start MongoDB service
net start MongoDB >nul 2>&1
if errorlevel 1 (
    echo [WARNING] MongoDB service not running or not installed
    echo Please ensure MongoDB is installed and running
    echo Download from: https://www.mongodb.com/try/download/community
    echo.
    echo Press any key to continue anyway (app may not work without MongoDB)
    pause >nul
) else (
    echo [OK] MongoDB service started
)

echo.

REM =====================================================
REM STEP 3: Start Backend
REM =====================================================

echo [STEP 3/5] Starting Backend Server...
echo.

cd backend

REM Check if venv exists
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate and install dependencies
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check if dependencies are installed
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing backend dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [OK] Backend dependencies ready

REM Start backend in new window
echo [INFO] Starting backend server on port 8001...
start "StockBreak Pro - Backend" cmd /k "cd /d %CD% && venv\Scripts\activate && uvicorn server:app --host 0.0.0.0 --port 8001"

cd ..
echo [OK] Backend starting in new window
echo.

REM Wait a bit for backend to initialize
timeout /t 3 /nobreak >nul

REM =====================================================
REM STEP 4: Start Frontend
REM =====================================================

echo [STEP 4/5] Starting Frontend...
echo.

cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo [INFO] Installing frontend dependencies (this may take a few minutes)...
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install frontend dependencies
        pause
        exit /b 1
    )
)

echo [OK] Frontend dependencies ready

REM Start frontend in new window
echo [INFO] Starting frontend on port 3000...
start "StockBreak Pro - Frontend" cmd /k "cd /d %CD% && npm start"

cd ..
echo [OK] Frontend starting in new window
echo.

REM =====================================================
REM STEP 5: Open Browser
REM =====================================================

echo [STEP 5/5] Opening browser...
echo.

echo Waiting for services to initialize...
timeout /t 15 /nobreak

echo [INFO] Opening StockBreak Pro in your default browser...
start http://localhost:3000

echo.
echo ========================================================
echo              STOCKBREAK PRO IS NOW RUNNING!
echo ========================================================
echo.
echo URLs:
echo   Frontend:  http://localhost:3000  (Main Application)
echo   Backend:   http://localhost:8001  (API Server)
echo   API Docs:  http://localhost:8001/docs
echo.
echo Access from other devices on your network:
echo   1. Find your IP: Open cmd and run "ipconfig"
echo   2. Look for IPv4 Address (e.g., 192.168.1.100)
echo   3. On other device, open: http://YOUR_IP:3000
echo.
echo ========================================================
echo.
echo To stop the application:
echo   - Close the Backend and Frontend windows
echo   - Or press Ctrl+C in each window
echo.
echo Keep this window open to see status messages.
echo Press any key to exit this launcher (app will keep running)
echo.
pause

exit /b 0
