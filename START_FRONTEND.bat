@echo off
title StockBreak Frontend Only
color 0B

echo ============================================
echo   Starting Frontend Server ONLY
echo ============================================
echo.

:: Navigate to frontend folder
cd /d "%~dp0frontend"

:: Check Node.js
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js not found! Install from nodejs.org
    pause
    exit /b 1
)

echo [OK] Node.js found
echo.

:: Check if backend is running
echo Checking if backend is running...
curl -s http://localhost:8001/api/health >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Backend is NOT running!
    echo [WARNING] Please start START_BACKEND.bat first!
    echo.
    set /p continue="Continue anyway? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
)
echo.

:: Install dependencies
echo Installing dependencies (this may take a minute)...
call yarn install
echo.

:: Start server
echo ============================================
echo Starting Frontend on http://localhost:3000
echo ============================================
echo.
echo Press Ctrl+C to stop the server
echo.

call yarn start

pause
