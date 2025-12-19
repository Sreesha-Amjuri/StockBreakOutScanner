@echo off
REM =====================================================
REM Complete Fix - Backend .env Issue
REM =====================================================

title StockBreak Pro - Complete Fix
color 0B

echo.
echo ========================================================
echo         COMPLETE FIX - BACKEND SETUP
echo ========================================================
echo.

cd /d "%~dp0backend"

echo Current directory: %CD%
echo.

REM ============================================
REM STEP 1: Create .env file
REM ============================================
echo [STEP 1/5] Creating .env file...

(
echo MONGO_URL=mongodb://localhost:27017
echo DB_NAME=stockbreak_db
echo CORS_ORIGINS=*
) > .env

echo [OK] .env file created at: %CD%\.env
echo.
echo Contents of .env:
type .env
echo.

REM ============================================
REM STEP 2: Verify .env file exists
REM ============================================
echo [STEP 2/5] Verifying .env file...

if exist .env (
    echo [OK] .env file exists
) else (
    echo [ERROR] .env file not created!
    pause
    exit /b 1
)
echo.

REM ============================================
REM STEP 3: Activate virtual environment
REM ============================================
echo [STEP 3/5] Activating virtual environment...

if not exist venv (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo [OK] Virtual environment activated
echo.

REM ============================================
REM STEP 4: Install ALL required packages
REM ============================================
echo [STEP 4/5] Installing required packages...
echo This may take 2-3 minutes...
echo.

pip install --upgrade pip
pip install python-dotenv
pip install charset-normalizer
pip install chardet
pip install -r requirements.txt

echo.
echo [OK] All packages installed
echo.

REM ============================================
REM STEP 5: Set environment variables manually
REM ============================================
echo [STEP 5/5] Setting environment variables...

set MONGO_URL=mongodb://localhost:27017
set DB_NAME=stockbreak_db
set CORS_ORIGINS=*

echo [OK] Environment variables set:
echo   MONGO_URL=%MONGO_URL%
echo   DB_NAME=%DB_NAME%
echo   CORS_ORIGINS=%CORS_ORIGINS%
echo.

REM ============================================
REM Start MongoDB
REM ============================================
echo Starting MongoDB service...
net start MongoDB >nul 2>&1
if errorlevel 1 (
    echo [WARNING] MongoDB service not started
    echo Please install MongoDB from: https://www.mongodb.com/try/download/community
    echo Or MongoDB may already be running
) else (
    echo [OK] MongoDB service started
)
echo.

REM ============================================
REM Start Backend
REM ============================================
echo ========================================================
echo            STARTING BACKEND SERVER
echo ========================================================
echo.
echo Backend will start on: http://localhost:8001
echo API Documentation: http://localhost:8001/docs
echo.
echo If you see errors, press Ctrl+C to stop
echo.

uvicorn server:app --host 0.0.0.0 --port 8001

pause
