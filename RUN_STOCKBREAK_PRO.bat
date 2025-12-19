@echo off
REM =====================================================
REM StockBreak Pro - Complete Launcher
REM Double-click this file to start both backend and frontend
REM =====================================================

title StockBreak Pro - Launcher
color 0B

echo.
echo ========================================================
echo            STOCKBREAK PRO - LAUNCHER
echo ========================================================
echo.
echo Starting Backend and Frontend in separate windows...
echo.

REM Get the directory where this batch file is located
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

echo Project Directory: %PROJECT_DIR%
echo.

REM =====================================================
REM Check Prerequisites
REM =====================================================

echo [STEP 1/4] Checking prerequisites...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python from: https://www.python.org/downloads/
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

echo.

REM =====================================================
REM Start MongoDB
REM =====================================================

echo [STEP 2/4] Starting MongoDB...
net start MongoDB >nul 2>&1
if errorlevel 1 (
    echo [WARNING] MongoDB not started (may already be running or not installed)
) else (
    echo [OK] MongoDB started
)
echo.

REM =====================================================
REM Start Backend in new window
REM =====================================================

echo [STEP 3/4] Starting Backend Server...
echo.

if not exist "backend\server.py" (
    echo [ERROR] Cannot find backend\server.py
    echo Please run this file from the project root directory
    pause
    exit /b 1
)

REM Check if backend .env exists, create if missing
if not exist "backend\.env" (
    echo [INFO] Creating backend .env file...
    (
    echo MONGO_URL=mongodb://localhost:27017
    echo DB_NAME=stockbreak_db
    echo CORS_ORIGINS=*
    ) > "backend\.env"
    echo [OK] Backend .env created
)

REM Check if frontend .env exists, create if missing
if not exist "frontend\.env" (
    echo [INFO] Creating frontend .env file...
    (
    echo REACT_APP_BACKEND_URL=http://localhost:8001
    ) > "frontend\.env"
    echo [OK] Frontend .env created
)

REM Create backend start script
echo @echo off > "%TEMP%\start_backend.bat"
echo title StockBreak Pro - Backend Server >> "%TEMP%\start_backend.bat"
echo color 0A >> "%TEMP%\start_backend.bat"
echo cd /d "%PROJECT_DIR%backend" >> "%TEMP%\start_backend.bat"
echo echo. >> "%TEMP%\start_backend.bat"
echo echo ======================================== >> "%TEMP%\start_backend.bat"
echo echo    STOCKBREAK PRO - BACKEND SERVER >> "%TEMP%\start_backend.bat"
echo echo ======================================== >> "%TEMP%\start_backend.bat"
echo echo. >> "%TEMP%\start_backend.bat"
echo echo [INFO] Working directory: %%CD%% >> "%TEMP%\start_backend.bat"
echo echo. >> "%TEMP%\start_backend.bat"
echo if not exist "venv" ( >> "%TEMP%\start_backend.bat"
echo     echo [INFO] Creating virtual environment... >> "%TEMP%\start_backend.bat"
echo     python -m venv venv >> "%TEMP%\start_backend.bat"
echo     if errorlevel 1 ( >> "%TEMP%\start_backend.bat"
echo         echo [ERROR] Failed to create virtual environment >> "%TEMP%\start_backend.bat"
echo         pause >> "%TEMP%\start_backend.bat"
echo         exit /b 1 >> "%TEMP%\start_backend.bat"
echo     ) >> "%TEMP%\start_backend.bat"
echo     echo [OK] Virtual environment created >> "%TEMP%\start_backend.bat"
echo ) >> "%TEMP%\start_backend.bat"
echo echo. >> "%TEMP%\start_backend.bat"
echo echo [INFO] Activating virtual environment... >> "%TEMP%\start_backend.bat"
echo call venv\Scripts\activate.bat >> "%TEMP%\start_backend.bat"
echo echo. >> "%TEMP%\start_backend.bat"
echo pip show fastapi ^>nul 2^>^&1 >> "%TEMP%\start_backend.bat"
echo if errorlevel 1 ( >> "%TEMP%\start_backend.bat"
echo     echo [INFO] Installing backend dependencies... >> "%TEMP%\start_backend.bat"
echo     echo This may take a few minutes... >> "%TEMP%\start_backend.bat"
echo     pip install -r requirements.txt >> "%TEMP%\start_backend.bat"
echo     if errorlevel 1 ( >> "%TEMP%\start_backend.bat"
echo         echo [ERROR] Failed to install dependencies >> "%TEMP%\start_backend.bat"
echo         pause >> "%TEMP%\start_backend.bat"
echo         exit /b 1 >> "%TEMP%\start_backend.bat"
echo     ) >> "%TEMP%\start_backend.bat"
echo     echo [OK] Dependencies installed >> "%TEMP%\start_backend.bat"
echo ) >> "%TEMP%\start_backend.bat"
echo echo. >> "%TEMP%\start_backend.bat"
echo echo ======================================== >> "%TEMP%\start_backend.bat"
echo echo [INFO] Starting Backend Server... >> "%TEMP%\start_backend.bat"
echo echo Backend URL: http://localhost:8001 >> "%TEMP%\start_backend.bat"
echo echo API Docs: http://localhost:8001/docs >> "%TEMP%\start_backend.bat"
echo echo ======================================== >> "%TEMP%\start_backend.bat"
echo echo. >> "%TEMP%\start_backend.bat"
echo uvicorn server:app --host 0.0.0.0 --port 8001 >> "%TEMP%\start_backend.bat"

REM Start backend in new window
start "StockBreak Pro - Backend" cmd /k "%TEMP%\start_backend.bat"

echo [OK] Backend window opened
echo.

REM Wait a bit for backend to initialize
timeout /t 3 /nobreak >nul

REM =====================================================
REM Start Frontend in new window
REM =====================================================

echo [STEP 4/4] Starting Frontend...
echo.

if not exist "frontend\package.json" (
    echo [ERROR] Cannot find frontend\package.json
    pause
    exit /b 1
)

REM Create frontend start script
echo @echo off > "%TEMP%\start_frontend.bat"
echo title StockBreak Pro - Frontend >> "%TEMP%\start_frontend.bat"
echo color 0C >> "%TEMP%\start_frontend.bat"
echo cd /d "%PROJECT_DIR%frontend" >> "%TEMP%\start_frontend.bat"
echo echo. >> "%TEMP%\start_frontend.bat"
echo echo ======================================== >> "%TEMP%\start_frontend.bat"
echo echo    STOCKBREAK PRO - FRONTEND >> "%TEMP%\start_frontend.bat"
echo echo ======================================== >> "%TEMP%\start_frontend.bat"
echo echo. >> "%TEMP%\start_frontend.bat"
echo echo [INFO] Working directory: %%CD%% >> "%TEMP%\start_frontend.bat"
echo echo. >> "%TEMP%\start_frontend.bat"
echo if not exist "node_modules" ( >> "%TEMP%\start_frontend.bat"
echo     echo [INFO] Installing frontend dependencies... >> "%TEMP%\start_frontend.bat"
echo     echo This will take 2-3 minutes... >> "%TEMP%\start_frontend.bat"
echo     echo. >> "%TEMP%\start_frontend.bat"
echo     npm install --legacy-peer-deps >> "%TEMP%\start_frontend.bat"
echo     if errorlevel 1 ( >> "%TEMP%\start_frontend.bat"
echo         echo [ERROR] Failed to install dependencies >> "%TEMP%\start_frontend.bat"
echo         echo. >> "%TEMP%\start_frontend.bat"
echo         echo Trying alternative installation... >> "%TEMP%\start_frontend.bat"
echo         rmdir /s /q node_modules 2^>nul >> "%TEMP%\start_frontend.bat"
echo         del package-lock.json 2^>nul >> "%TEMP%\start_frontend.bat"
echo         npm cache clean --force >> "%TEMP%\start_frontend.bat"
echo         npm install --legacy-peer-deps >> "%TEMP%\start_frontend.bat"
echo         if errorlevel 1 ( >> "%TEMP%\start_frontend.bat"
echo             echo [ERROR] Installation failed. Please check Node.js installation. >> "%TEMP%\start_frontend.bat"
echo             pause >> "%TEMP%\start_frontend.bat"
echo             exit /b 1 >> "%TEMP%\start_frontend.bat"
echo         ) >> "%TEMP%\start_frontend.bat"
echo     ) >> "%TEMP%\start_frontend.bat"
echo     echo [OK] Dependencies installed >> "%TEMP%\start_frontend.bat"
echo ) >> "%TEMP%\start_frontend.bat"
echo echo. >> "%TEMP%\start_frontend.bat"
echo echo ======================================== >> "%TEMP%\start_frontend.bat"
echo echo [INFO] Starting Frontend... >> "%TEMP%\start_frontend.bat"
echo echo Frontend URL: http://localhost:3000 >> "%TEMP%\start_frontend.bat"
echo echo ======================================== >> "%TEMP%\start_frontend.bat"
echo echo. >> "%TEMP%\start_frontend.bat"
echo echo Browser will open automatically... >> "%TEMP%\start_frontend.bat"
echo echo. >> "%TEMP%\start_frontend.bat"
echo npm start >> "%TEMP%\start_frontend.bat"

REM Start frontend in new window
start "StockBreak Pro - Frontend" cmd /k "%TEMP%\start_frontend.bat"

echo [OK] Frontend window opened
echo.

REM =====================================================
REM Wait and open browser
REM =====================================================

echo.
echo ========================================================
echo           STOCKBREAK PRO IS STARTING!
echo ========================================================
echo.
echo Two windows have been opened:
echo   1. Backend Server (Green) - Port 8001
echo   2. Frontend (Red) - Port 3000
echo.
echo Please wait for both services to initialize...
echo This may take 15-30 seconds for first run.
echo.
echo URLs:
echo   Main App:  http://localhost:3000
echo   Backend:   http://localhost:8001
echo   API Docs:  http://localhost:8001/docs
echo.
echo ========================================================
echo.
echo Waiting 20 seconds before opening browser...
timeout /t 20 /nobreak

echo Opening browser...
start http://localhost:3000

echo.
echo ========================================================
echo.
echo [SUCCESS] StockBreak Pro is now running!
echo.
echo To stop the application:
echo   - Close both Backend and Frontend windows
echo   - Or press Ctrl+C in each window
echo.
echo Keep those windows open while using the app.
echo You can close THIS window now.
echo.
echo ========================================================
echo.
echo Press any key to exit this launcher...
pause >nul

exit /b 0
