@echo off
REM =====================================================
REM StockBreak Pro - Complete Safe Launcher
REM Sets all environment variables and starts services
REM =====================================================

title StockBreak Pro - Complete Launcher
color 0B

echo.
echo ========================================================
echo       STOCKBREAK PRO - COMPLETE LAUNCHER
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
    echo [ERROR] Python not found! Install from: https://www.python.org/downloads/
    pause
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found! Install from: https://nodejs.org/
    pause
    exit /b 1
)

echo [OK] Prerequisites found
echo.

REM ============================================
REM Setup Backend .env
REM ============================================
echo [SETUP] Creating backend .env...

if not exist "backend\.env" (
    (
    echo MONGO_URL=mongodb://localhost:27017
    echo DB_NAME=stockbreak_db
    echo CORS_ORIGINS=*
    ) > "backend\.env"
    echo [OK] Backend .env created
) else (
    echo [OK] Backend .env exists
)
echo.

REM ============================================
REM Setup Frontend .env
REM ============================================
echo [SETUP] Creating frontend .env...

if not exist "frontend\.env" (
    (
    echo REACT_APP_BACKEND_URL=http://localhost:8001
    ) > "frontend\.env"
    echo [OK] Frontend .env created
) else (
    echo [OK] Frontend .env exists
)
echo.

REM ============================================
REM Start MongoDB
REM ============================================
echo [STARTING] MongoDB service...
net start MongoDB >nul 2>&1
if errorlevel 1 (
    echo [WARNING] MongoDB not started (may already be running)
) else (
    echo [OK] MongoDB started
)
echo.

REM ============================================
REM Create Backend Start Script
REM ============================================
echo [CREATING] Backend start script...

echo @echo off > "%TEMP%\start_backend_safe.bat"
echo title StockBreak Pro - Backend >> "%TEMP%\start_backend_safe.bat"
echo color 0A >> "%TEMP%\start_backend_safe.bat"
echo cd /d "%PROJECT_DIR%backend" >> "%TEMP%\start_backend_safe.bat"
echo. >> "%TEMP%\start_backend_safe.bat"
echo echo ======================================== >> "%TEMP%\start_backend_safe.bat"
echo echo    STOCKBREAK PRO - BACKEND SERVER >> "%TEMP%\start_backend_safe.bat"
echo echo ======================================== >> "%TEMP%\start_backend_safe.bat"
echo echo. >> "%TEMP%\start_backend_safe.bat"
echo. >> "%TEMP%\start_backend_safe.bat"
echo REM Set environment variables >> "%TEMP%\start_backend_safe.bat"
echo set MONGO_URL=mongodb://localhost:27017 >> "%TEMP%\start_backend_safe.bat"
echo set DB_NAME=stockbreak_db >> "%TEMP%\start_backend_safe.bat"
echo set CORS_ORIGINS=* >> "%TEMP%\start_backend_safe.bat"
echo. >> "%TEMP%\start_backend_safe.bat"
echo echo [INFO] Environment variables set: >> "%TEMP%\start_backend_safe.bat"
echo echo   MONGO_URL=%%MONGO_URL%% >> "%TEMP%\start_backend_safe.bat"
echo echo   DB_NAME=%%DB_NAME%% >> "%TEMP%\start_backend_safe.bat"
echo echo. >> "%TEMP%\start_backend_safe.bat"
echo. >> "%TEMP%\start_backend_safe.bat"
echo if not exist venv ( >> "%TEMP%\start_backend_safe.bat"
echo     echo [INFO] Creating virtual environment... >> "%TEMP%\start_backend_safe.bat"
echo     python -m venv venv >> "%TEMP%\start_backend_safe.bat"
echo ) >> "%TEMP%\start_backend_safe.bat"
echo. >> "%TEMP%\start_backend_safe.bat"
echo echo [INFO] Activating virtual environment... >> "%TEMP%\start_backend_safe.bat"
echo call venv\Scripts\activate.bat >> "%TEMP%\start_backend_safe.bat"
echo. >> "%TEMP%\start_backend_safe.bat"
echo pip show fastapi ^>nul 2^>^&1 >> "%TEMP%\start_backend_safe.bat"
echo if errorlevel 1 ( >> "%TEMP%\start_backend_safe.bat"
echo     echo [INFO] Installing dependencies... >> "%TEMP%\start_backend_safe.bat"
echo     pip install python-dotenv charset-normalizer chardet >> "%TEMP%\start_backend_safe.bat"
echo     pip install -r requirements.txt >> "%TEMP%\start_backend_safe.bat"
echo ) >> "%TEMP%\start_backend_safe.bat"
echo. >> "%TEMP%\start_backend_safe.bat"
echo echo. >> "%TEMP%\start_backend_safe.bat"
echo echo ======================================== >> "%TEMP%\start_backend_safe.bat"
echo echo [STARTING] Backend Server... >> "%TEMP%\start_backend_safe.bat"
echo echo URL: http://localhost:8001 >> "%TEMP%\start_backend_safe.bat"
echo echo Docs: http://localhost:8001/docs >> "%TEMP%\start_backend_safe.bat"
echo echo ======================================== >> "%TEMP%\start_backend_safe.bat"
echo echo. >> "%TEMP%\start_backend_safe.bat"
echo. >> "%TEMP%\start_backend_safe.bat"
echo uvicorn server:app --host 0.0.0.0 --port 8001 >> "%TEMP%\start_backend_safe.bat"

REM ============================================
REM Create Frontend Start Script
REM ============================================
echo [CREATING] Frontend start script...

echo @echo off > "%TEMP%\start_frontend_safe.bat"
echo title StockBreak Pro - Frontend >> "%TEMP%\start_frontend_safe.bat"
echo color 0C >> "%TEMP%\start_frontend_safe.bat"
echo cd /d "%PROJECT_DIR%frontend" >> "%TEMP%\start_frontend_safe.bat"
echo. >> "%TEMP%\start_frontend_safe.bat"
echo echo ======================================== >> "%TEMP%\start_frontend_safe.bat"
echo echo    STOCKBREAK PRO - FRONTEND >> "%TEMP%\start_frontend_safe.bat"
echo echo ======================================== >> "%TEMP%\start_frontend_safe.bat"
echo echo. >> "%TEMP%\start_frontend_safe.bat"
echo. >> "%TEMP%\start_frontend_safe.bat"
echo REM Set environment variable >> "%TEMP%\start_frontend_safe.bat"
echo set REACT_APP_BACKEND_URL=http://localhost:8001 >> "%TEMP%\start_frontend_safe.bat"
echo. >> "%TEMP%\start_frontend_safe.bat"
echo echo [INFO] Backend URL: %%REACT_APP_BACKEND_URL%% >> "%TEMP%\start_frontend_safe.bat"
echo echo. >> "%TEMP%\start_frontend_safe.bat"
echo. >> "%TEMP%\start_frontend_safe.bat"
echo if not exist node_modules ( >> "%TEMP%\start_frontend_safe.bat"
echo     echo [INFO] Installing dependencies... >> "%TEMP%\start_frontend_safe.bat"
echo     npm install --legacy-peer-deps >> "%TEMP%\start_frontend_safe.bat"
echo ) >> "%TEMP%\start_frontend_safe.bat"
echo. >> "%TEMP%\start_frontend_safe.bat"
echo echo. >> "%TEMP%\start_frontend_safe.bat"
echo echo ======================================== >> "%TEMP%\start_frontend_safe.bat"
echo echo [STARTING] Frontend... >> "%TEMP%\start_frontend_safe.bat"
echo echo URL: http://localhost:3000 >> "%TEMP%\start_frontend_safe.bat"
echo echo ======================================== >> "%TEMP%\start_frontend_safe.bat"
echo echo. >> "%TEMP%\start_frontend_safe.bat"
echo. >> "%TEMP%\start_frontend_safe.bat"
echo npm start >> "%TEMP%\start_frontend_safe.bat"

REM ============================================
REM Start Backend Window
REM ============================================
echo [STARTING] Backend in new window...
start "StockBreak Pro - Backend" cmd /k "%TEMP%\start_backend_safe.bat"
echo [OK] Backend window opened
echo.

timeout /t 5 /nobreak >nul

REM ============================================
REM Start Frontend Window
REM ============================================
echo [STARTING] Frontend in new window...
start "StockBreak Pro - Frontend" cmd /k "%TEMP%\start_frontend_safe.bat"
echo [OK] Frontend window opened
echo.

REM ============================================
REM Wait and Open Browser
REM ============================================
echo.
echo ========================================================
echo            SERVICES STARTING!
echo ========================================================
echo.
echo Two windows opened:
echo   1. Backend (Green) - Port 8001
echo   2. Frontend (Red) - Port 3000
echo.
echo Environment Variables Set:
echo   MONGO_URL=mongodb://localhost:27017
echo   REACT_APP_BACKEND_URL=http://localhost:8001
echo.
echo Please wait 20 seconds for services to start...
echo.

timeout /t 20 /nobreak

echo [OPENING] Browser...
start http://localhost:3000

echo.
echo ========================================================
echo             SUCCESS!
echo ========================================================
echo.
echo Access URLs:
echo   Main App:  http://localhost:3000
echo   Backend:   http://localhost:8001
echo   API Docs:  http://localhost:8001/docs
echo.
echo Keep the Backend and Frontend windows open!
echo You can close THIS window now.
echo.
pause
