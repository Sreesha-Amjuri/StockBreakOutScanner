@echo off
title StockBreak Backend Only
color 0A

echo ============================================
echo   Starting Backend Server ONLY
echo ============================================
echo.

:: Navigate to backend folder
cd /d "%~dp0backend"

:: Check Python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found! Install from python.org
    pause
    exit /b 1
)

echo [OK] Python found
echo.

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Some dependencies may have failed to install
)
echo.

:: Start server
echo ============================================
echo Starting Backend on http://localhost:8001
echo API Docs: http://localhost:8001/docs
echo ============================================
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn server:app --host 0.0.0.0 --port 8001 --reload

pause
