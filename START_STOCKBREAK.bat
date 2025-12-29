@echo off
title StockBreak Pro Launcher
color 0A

echo ============================================
echo         StockBreak Pro - Quick Start
echo ============================================
echo.

:: Get the directory where this batch file is located
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

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

:: Check for MongoDB
echo [INFO] Make sure MongoDB is running on localhost:27017
echo.

:: Start Backend
echo ============================================
echo Starting Backend Server...
echo ============================================
cd /d "%PROJECT_DIR%backend"

:: Install backend dependencies first
echo Installing Python dependencies...
pip install -r requirements.txt

:: Start backend in new window
echo Starting backend server...
start "StockBreak Backend" cmd /k "cd /d "%PROJECT_DIR%backend" && uvicorn server:app --host 0.0.0.0 --port 8001 --reload"

:: Wait for backend to start
echo Waiting for backend to initialize (10 seconds)...
timeout /t 10 /nobreak >nul

:: Test backend is running
echo Testing backend connection...
curl -s http://localhost:8001/api/health >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Backend may not have started yet. Continuing anyway...
) else (
    echo [OK] Backend is running!
)
echo.

:: Start Frontend
echo ============================================
echo Starting Frontend Server...
echo ============================================
cd /d "%PROJECT_DIR%frontend"

:: Start frontend in new window
start "StockBreak Frontend" cmd /k "cd /d "%PROJECT_DIR%frontend" && yarn install && yarn start"

echo.
echo ============================================
echo   StockBreak Pro is starting!
echo ============================================
echo.
echo   Backend:  http://localhost:8001
echo   Frontend: http://localhost:3000
echo   API Docs: http://localhost:8001/docs
echo.
echo ============================================
echo.
echo Waiting for frontend to start (15 seconds)...
timeout /t 15 /nobreak >nul

echo Opening browser...
start http://localhost:3000

echo.
echo [INFO] Both servers are running in separate windows.
echo [INFO] Do NOT close those windows to keep the app running.
echo.
pause
