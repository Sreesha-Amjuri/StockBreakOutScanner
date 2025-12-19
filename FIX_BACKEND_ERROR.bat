@echo off
REM =====================================================
REM Fix Backend MONGO_URL Error
REM =====================================================

title StockBreak Pro - Fix Backend
color 0A

echo.
echo ========================================================
echo       FIXING BACKEND MONGO_URL ERROR
echo ========================================================
echo.

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%backend"

echo Current directory: %CD%
echo.

REM Create .env file
echo [STEP 1/3] Creating backend .env file...
(
echo MONGO_URL=mongodb://localhost:27017
echo DB_NAME=stockbreak_db
echo CORS_ORIGINS=*
) > .env

echo [OK] .env file created
echo.
echo Contents:
type .env
echo.

REM Install missing packages
echo [STEP 2/3] Installing missing Python packages...
call venv\Scripts\activate.bat
pip install python-dotenv charset-normalizer requests
echo [OK] Packages installed
echo.

REM Start MongoDB
echo [STEP 3/3] Starting MongoDB...
net start MongoDB >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Could not start MongoDB service
    echo Please ensure MongoDB is installed
    echo Download: https://www.mongodb.com/try/download/community
    echo.
) else (
    echo [OK] MongoDB started
)
echo.

echo ========================================================
echo              FIX COMPLETE!
echo ========================================================
echo.
echo Now starting backend server...
echo.

uvicorn server:app --host 0.0.0.0 --port 8001

pause
