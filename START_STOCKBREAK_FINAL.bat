@echo off
REM =====================================================
REM StockBreak Pro - Automatic Complete Launcher
REM Fixes all issues automatically - No manual steps!
REM =====================================================

title StockBreak Pro - Auto Launcher
color 0B

echo.
echo ========================================================
echo       STOCKBREAK PRO - AUTOMATIC LAUNCHER
echo       (Fixes all dependency issues automatically)
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
echo [OK] Python found

node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found! Install from: https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] Node.js found
echo.

REM ============================================
REM Setup Backend .env
REM ============================================
echo [SETUP] Backend environment...
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

REM ============================================
REM Setup Frontend .env
REM ============================================
echo [SETUP] Frontend environment...
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
echo [STARTING] MongoDB...
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

echo @echo off > "%TEMP%\start_backend_final.bat"
echo title StockBreak Pro - Backend >> "%TEMP%\start_backend_final.bat"
echo color 0A >> "%TEMP%\start_backend_final.bat"
echo cd /d "%PROJECT_DIR%backend" >> "%TEMP%\start_backend_final.bat"
echo. >> "%TEMP%\start_backend_final.bat"
echo echo ======================================== >> "%TEMP%\start_backend_final.bat"
echo echo    STOCKBREAK PRO - BACKEND SERVER >> "%TEMP%\start_backend_final.bat"
echo echo ======================================== >> "%TEMP%\start_backend_final.bat"
echo echo. >> "%TEMP%\start_backend_final.bat"
echo. >> "%TEMP%\start_backend_final.bat"
echo REM Set environment variables >> "%TEMP%\start_backend_final.bat"
echo set MONGO_URL=mongodb://localhost:27017 >> "%TEMP%\start_backend_final.bat"
echo set DB_NAME=stockbreak_db >> "%TEMP%\start_backend_final.bat"
echo set CORS_ORIGINS=* >> "%TEMP%\start_backend_final.bat"
echo. >> "%TEMP%\start_backend_final.bat"
echo echo [INFO] Environment: >> "%TEMP%\start_backend_final.bat"
echo echo   MONGO_URL=%%MONGO_URL%% >> "%TEMP%\start_backend_final.bat"
echo echo   DB_NAME=%%DB_NAME%% >> "%TEMP%\start_backend_final.bat"
echo echo. >> "%TEMP%\start_backend_final.bat"
echo. >> "%TEMP%\start_backend_final.bat"
echo if not exist venv ( >> "%TEMP%\start_backend_final.bat"
echo     echo [INFO] Creating virtual environment... >> "%TEMP%\start_backend_final.bat"
echo     python -m venv venv >> "%TEMP%\start_backend_final.bat"
echo ) >> "%TEMP%\start_backend_final.bat"
echo. >> "%TEMP%\start_backend_final.bat"
echo call venv\Scripts\activate.bat >> "%TEMP%\start_backend_final.bat"
echo. >> "%TEMP%\start_backend_final.bat"
echo pip show fastapi ^>nul 2^>^&1 >> "%TEMP%\start_backend_final.bat"
echo if errorlevel 1 ( >> "%TEMP%\start_backend_final.bat"
echo     echo [INFO] Installing backend dependencies... >> "%TEMP%\start_backend_final.bat"
echo     pip install --upgrade pip >> "%TEMP%\start_backend_final.bat"
echo     pip install python-dotenv charset-normalizer chardet >> "%TEMP%\start_backend_final.bat"
echo     pip install -r requirements.txt >> "%TEMP%\start_backend_final.bat"
echo     echo [OK] Dependencies installed >> "%TEMP%\start_backend_final.bat"
echo ) >> "%TEMP%\start_backend_final.bat"
echo. >> "%TEMP%\start_backend_final.bat"
echo echo. >> "%TEMP%\start_backend_final.bat"
echo echo ======================================== >> "%TEMP%\start_backend_final.bat"
echo echo [STARTING] Backend Server... >> "%TEMP%\start_backend_final.bat"
echo echo URL: http://localhost:8001 >> "%TEMP%\start_backend_final.bat"
echo echo API Docs: http://localhost:8001/docs >> "%TEMP%\start_backend_final.bat"
echo echo ======================================== >> "%TEMP%\start_backend_final.bat"
echo echo. >> "%TEMP%\start_backend_final.bat"
echo. >> "%TEMP%\start_backend_final.bat"
echo uvicorn server:app --host 0.0.0.0 --port 8001 >> "%TEMP%\start_backend_final.bat"

REM ============================================
REM Create Frontend Start Script with AJV Fix
REM ============================================
echo [CREATING] Frontend start script with automatic fixes...

echo @echo off > "%TEMP%\start_frontend_final.bat"
echo title StockBreak Pro - Frontend >> "%TEMP%\start_frontend_final.bat"
echo color 0C >> "%TEMP%\start_frontend_final.bat"
echo cd /d "%PROJECT_DIR%frontend" >> "%TEMP%\start_frontend_final.bat"
echo. >> "%TEMP%\start_frontend_final.bat"
echo echo ======================================== >> "%TEMP%\start_frontend_final.bat"
echo echo    STOCKBREAK PRO - FRONTEND >> "%TEMP%\start_frontend_final.bat"
echo echo    (Auto-fixing dependencies) >> "%TEMP%\start_frontend_final.bat"
echo echo ======================================== >> "%TEMP%\start_frontend_final.bat"
echo echo. >> "%TEMP%\start_frontend_final.bat"
echo. >> "%TEMP%\start_frontend_final.bat"
echo REM Set environment variable >> "%TEMP%\start_frontend_final.bat"
echo set REACT_APP_BACKEND_URL=http://localhost:8001 >> "%TEMP%\start_frontend_final.bat"
echo echo [INFO] Backend URL: %%REACT_APP_BACKEND_URL%% >> "%TEMP%\start_frontend_final.bat"
echo echo. >> "%TEMP%\start_frontend_final.bat"
echo. >> "%TEMP%\start_frontend_final.bat"
echo REM Check if node_modules exists >> "%TEMP%\start_frontend_final.bat"
echo if not exist node_modules ( >> "%TEMP%\start_frontend_final.bat"
echo     echo [INFO] Installing frontend dependencies... >> "%TEMP%\start_frontend_final.bat"
echo     echo [INFO] This will take 2-3 minutes... >> "%TEMP%\start_frontend_final.bat"
echo     echo. >> "%TEMP%\start_frontend_final.bat"
echo     echo [STEP 1/4] Cleaning cache... >> "%TEMP%\start_frontend_final.bat"
echo     npm cache clean --force >> "%TEMP%\start_frontend_final.bat"
echo     echo. >> "%TEMP%\start_frontend_final.bat"
echo     echo [STEP 2/4] Installing ajv ^(fixing compatibility^)... >> "%TEMP%\start_frontend_final.bat"
echo     npm install ajv@8.12.0 --save --legacy-peer-deps >> "%TEMP%\start_frontend_final.bat"
echo     echo. >> "%TEMP%\start_frontend_final.bat"
echo     echo [STEP 3/4] Installing ajv-keywords... >> "%TEMP%\start_frontend_final.bat"
echo     npm install ajv-keywords@5.1.0 --save --legacy-peer-deps >> "%TEMP%\start_frontend_final.bat"
echo     echo. >> "%TEMP%\start_frontend_final.bat"
echo     echo [STEP 4/4] Installing all dependencies... >> "%TEMP%\start_frontend_final.bat"
echo     npm install --legacy-peer-deps >> "%TEMP%\start_frontend_final.bat"
echo     echo. >> "%TEMP%\start_frontend_final.bat"
echo     echo [OK] Dependencies installed >> "%TEMP%\start_frontend_final.bat"
echo ) else ( >> "%TEMP%\start_frontend_final.bat"
echo     REM Check if ajv is correct version >> "%TEMP%\start_frontend_final.bat"
echo     npm list ajv ^| findstr "8.12.0" ^>nul 2^>^&1 >> "%TEMP%\start_frontend_final.bat"
echo     if errorlevel 1 ( >> "%TEMP%\start_frontend_final.bat"
echo         echo [WARNING] Incorrect ajv version detected >> "%TEMP%\start_frontend_final.bat"
echo         echo [INFO] Fixing dependency issue... >> "%TEMP%\start_frontend_final.bat"
echo         echo. >> "%TEMP%\start_frontend_final.bat"
echo         rmdir /s /q node_modules >> "%TEMP%\start_frontend_final.bat"
echo         del package-lock.json 2^>nul >> "%TEMP%\start_frontend_final.bat"
echo         npm cache clean --force >> "%TEMP%\start_frontend_final.bat"
echo         echo [INFO] Installing fixed versions... >> "%TEMP%\start_frontend_final.bat"
echo         npm install ajv@8.12.0 --save --legacy-peer-deps >> "%TEMP%\start_frontend_final.bat"
echo         npm install ajv-keywords@5.1.0 --save --legacy-peer-deps >> "%TEMP%\start_frontend_final.bat"
echo         npm install --legacy-peer-deps >> "%TEMP%\start_frontend_final.bat"
echo         echo [OK] Dependencies fixed >> "%TEMP%\start_frontend_final.bat"
echo     ) >> "%TEMP%\start_frontend_final.bat"
echo ) >> "%TEMP%\start_frontend_final.bat"
echo. >> "%TEMP%\start_frontend_final.bat"
echo echo. >> "%TEMP%\start_frontend_final.bat"
echo echo ======================================== >> "%TEMP%\start_frontend_final.bat"
echo echo [STARTING] Frontend... >> "%TEMP%\start_frontend_final.bat"
echo echo URL: http://localhost:3000 >> "%TEMP%\start_frontend_final.bat"
echo echo ======================================== >> "%TEMP%\start_frontend_final.bat"
echo echo. >> "%TEMP%\start_frontend_final.bat"
echo echo Browser will open automatically... >> "%TEMP%\start_frontend_final.bat"
echo echo. >> "%TEMP%\start_frontend_final.bat"
echo. >> "%TEMP%\start_frontend_final.bat"
echo npm start >> "%TEMP%\start_frontend_final.bat"

REM ============================================
REM Start Backend
REM ============================================
echo [STARTING] Backend in new window...
start "StockBreak Pro - Backend" cmd /k "%TEMP%\start_backend_final.bat"
echo [OK] Backend window opened
echo.

timeout /t 5 /nobreak >nul

REM ============================================
REM Start Frontend
REM ============================================
echo [STARTING] Frontend in new window...
echo [INFO] Frontend will auto-fix ajv dependencies if needed...
start "StockBreak Pro - Frontend" cmd /k "%TEMP%\start_frontend_final.bat"
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
echo The frontend will automatically:
echo   - Fix ajv dependency issues
echo   - Install compatible versions
echo   - Start on port 3000
echo.
echo This may take 2-3 minutes on first run.
echo.
echo Please wait 30 seconds for services to start...
echo.

timeout /t 30 /nobreak

echo [OPENING] Browser...
start http://localhost:3000

echo.
echo ========================================================
echo             LAUNCH COMPLETE!
echo ========================================================
echo.
echo Access URLs:
echo   Main App:  http://localhost:3000
echo   Backend:   http://localhost:8001
echo   API Docs:  http://localhost:8001/docs
echo.
echo If browser shows "Not Found":
echo   - Wait a bit longer for frontend to compile
echo   - Check Frontend window for progress
echo   - Refresh browser after you see "Compiled successfully!"
echo.
echo Keep Backend and Frontend windows open!
echo You can close THIS window now.
echo.
pause
