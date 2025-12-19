@echo off
REM =====================================================
REM Manual Frontend Start with Error Display
REM =====================================================

title StockBreak Pro - Frontend Manual Start
color 0C

cd /d "%~dp0frontend"

echo.
echo ========================================================
echo       STARTING FRONTEND MANUALLY
echo ========================================================
echo.

echo Current directory: %CD%
echo.

REM Set environment variable
set REACT_APP_BACKEND_URL=http://localhost:8001

echo [INFO] Backend URL set to: %REACT_APP_BACKEND_URL%
echo.

REM Check if node_modules exists
if not exist node_modules (
    echo [WARNING] node_modules not found!
    echo [INFO] Installing dependencies...
    echo This will take 2-3 minutes...
    echo.
    
    REM Clean install
    npm cache clean --force
    rmdir /s /q node_modules 2>nul
    del package-lock.json 2>nul
    
    REM Install with legacy peer deps
    npm install --legacy-peer-deps
    
    if errorlevel 1 (
        echo.
        echo [ERROR] npm install failed!
        echo.
        echo Trying alternative method...
        npm install --force
    )
    
    echo.
    echo [OK] Dependencies installed
)

echo.
echo ========================================================
echo       STARTING FRONTEND ON PORT 3000
echo ========================================================
echo.
echo If you see errors, they will be displayed below.
echo Frontend should compile and open browser automatically.
echo.
echo If it says "Something is already running on port 3000":
echo   1. Close this window
echo   2. Run: netstat -ano ^| findstr :3000
echo   3. Kill that process
echo   4. Try again
echo.

REM Start frontend
npm start

echo.
echo [INFO] npm start exited
echo.
pause
