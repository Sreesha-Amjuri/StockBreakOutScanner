@echo off
title StockBreak Pro Launcher
color 0A

echo ============================================
echo         StockBreak Pro - Quick Start
echo ============================================
echo.

:: Check if Node.js is installed
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed!
    echo Please download from: https://nodejs.org/
    pause
    exit /b 1
)

:: Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed!
    echo Please download from: https://python.org/
    pause
    exit /b 1
)

echo [OK] Node.js found
echo [OK] Python found
echo.

:: Start Backend
echo Starting Backend Server...
cd /d "%~dp0backend"
start "StockBreak Backend" cmd /k "python -m pip install -r requirements.txt >nul 2>&1 && python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload"

:: Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

:: Start Frontend
echo Starting Frontend Server...
cd /d "%~dp0frontend"
start "StockBreak Frontend" cmd /k "yarn install && yarn start"

echo.
echo ============================================
echo   StockBreak Pro is starting!
echo   Backend: http://localhost:8001
echo   Frontend: http://localhost:3000
echo ============================================
echo.
echo Press any key to open the app in browser...
pause >nul
start http://localhost:3000
