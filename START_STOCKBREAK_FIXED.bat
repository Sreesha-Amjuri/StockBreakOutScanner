@echo off
SETLOCAL EnableDelayedExpansion
REM =====================================================
REM StockBreak Pro - Complete Fixed Launcher
REM No trailing spaces, fixed batch syntax
REM =====================================================

title StockBreak Pro - Launcher
color 0B

echo.
echo ========================================================
echo       STOCKBREAK PRO - AUTOMATIC LAUNCHER
echo ========================================================
echo.

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

REM ============================================
REM Check Prerequisites
REM ============================================
echo [CHECKING] Prerequisites...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)
echo [OK] Python found

node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found!
    pause
    exit /b 1
)
echo [OK] Node.js found
echo.

REM ============================================
REM Setup Backend .env (NO TRAILING SPACES!)
REM ============================================
echo [SETUP] Backend environment...
cd backend
(
echo MONGO_URL=mongodb://localhost:27017
echo DB_NAME=stockbreak_db
echo CORS_ORIGINS=*
) > .env

echo [OK] Backend .env created
cd ..

REM ============================================
REM Setup Frontend .env (NO TRAILING SPACES!)
REM ============================================
echo [SETUP] Frontend environment...
cd frontend
echo REACT_APP_BACKEND_URL=http://localhost:8001> .env
echo [OK] Frontend .env created
cd ..
echo.

REM ============================================
REM Start MongoDB
REM ============================================
echo [STARTING] MongoDB...
net start MongoDB >nul 2>&1
if errorlevel 1 (
    echo [WARNING] MongoDB not started
) else (
    echo [OK] MongoDB started
)
echo.

REM ============================================
REM Create Backend Script
REM ============================================
echo [CREATING] Backend script...
set BACKEND_SCRIPT=%TEMP%\start_backend_now.bat

(
echo @echo off
echo title StockBreak Pro - Backend
echo color 0A
echo cd /d "%PROJECT_DIR%backend"
echo.
echo echo ========================================
echo echo    STOCKBREAK PRO - BACKEND
echo echo ========================================
echo echo.
echo.
echo set MONGO_URL=mongodb://localhost:27017
echo set DB_NAME=stockbreak_db
echo set CORS_ORIGINS=*
echo.
echo echo [INFO] MONGO_URL=%%MONGO_URL%%
echo echo [INFO] DB_NAME=%%DB_NAME%%
echo echo.
echo.
echo if not exist venv ^(
echo     echo [INFO] Creating venv...
echo     python -m venv venv
echo ^)
echo.
echo call venv\Scripts\activate.bat
echo.
echo pip show fastapi ^>nul 2^>^&1
echo if errorlevel 1 ^(
echo     echo [INFO] Installing dependencies...
echo     pip install --upgrade pip
echo     pip install python-dotenv charset-normalizer chardet
echo     pip install -r requirements.txt
echo ^)
echo.
echo echo.
echo echo ========================================
echo echo [STARTING] Backend on port 8001
echo echo ========================================
echo echo.
echo.
echo uvicorn server:app --host 0.0.0.0 --port 8001
) > "%BACKEND_SCRIPT%"

REM ============================================
REM Create Frontend Script (Fixed Syntax)
REM ============================================
echo [CREATING] Frontend script...
set FRONTEND_SCRIPT=%TEMP%\start_frontend_now.bat

(
echo @echo off
echo title StockBreak Pro - Frontend
echo color 0C
echo cd /d "%PROJECT_DIR%frontend"
echo.
echo echo ========================================
echo echo    STOCKBREAK PRO - FRONTEND
echo echo ========================================
echo echo.
echo.
echo set REACT_APP_BACKEND_URL=http://localhost:8001
echo echo [INFO] Backend URL: %%REACT_APP_BACKEND_URL%%
echo echo.
echo.
echo if not exist node_modules ^(
echo     echo [INFO] Installing dependencies...
echo     echo [INFO] This takes 2-3 minutes...
echo     echo.
echo     npm cache clean --force
echo     echo [1/3] Installing ajv@8.12.0...
echo     npm install ajv@8.12.0 --save --legacy-peer-deps
echo     echo [2/3] Installing ajv-keywords@5.1.0...
echo     npm install ajv-keywords@5.1.0 --save --legacy-peer-deps
echo     echo [3/3] Installing all dependencies...
echo     npm install --legacy-peer-deps
echo     echo [OK] Dependencies installed
echo ^)
echo.
echo echo.
echo echo ========================================
echo echo [STARTING] Frontend on port 3000
echo echo ========================================
echo echo.
echo.
echo npm start
) > "%FRONTEND_SCRIPT%"

REM ============================================
REM Start Services
REM ============================================
echo [STARTING] Backend...
start "StockBreak Pro - Backend" cmd /k "%BACKEND_SCRIPT%"
echo [OK] Backend window opened
echo.

timeout /t 5 /nobreak >nul

echo [STARTING] Frontend...
start "StockBreak Pro - Frontend" cmd /k "%FRONTEND_SCRIPT%"
echo [OK] Frontend window opened
echo.

REM ============================================
REM Wait and Open Browser
REM ============================================
echo.
echo ========================================================
echo            SERVICES STARTING
echo ========================================================
echo.
echo Two windows opened:
echo   1. Backend - Port 8001
echo   2. Frontend - Port 3000
echo.
echo Please wait 30 seconds...
echo.

timeout /t 30 /nobreak

echo [OPENING] Browser...
start http://localhost:3000

echo.
echo ========================================================
echo             LAUNCH COMPLETE
echo ========================================================
echo.
echo URLs:
echo   App:     http://localhost:3000
echo   Backend: http://localhost:8001
echo   Docs:    http://localhost:8001/docs
echo.
echo Keep Backend and Frontend windows open!
echo.
pause
