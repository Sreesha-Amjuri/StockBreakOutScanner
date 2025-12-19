@echo off
title StockBreak Pro - Diagnostics
color 0B

echo ============================================
echo      StockBreak Pro - System Diagnostics
echo ============================================
echo.
echo Running diagnostics... Please wait.
echo.

echo [1/6] Checking Node.js...
where node >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%i in ('node -v') do echo   Version: %%i [OK]
) else (
    echo   [ERROR] Node.js NOT FOUND
    echo   Download from: https://nodejs.org/
)
echo.

echo [2/6] Checking Python...
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%i in ('python --version') do echo   %%i [OK]
) else (
    echo   [ERROR] Python NOT FOUND
    echo   Download from: https://python.org/
)
echo.

echo [3/6] Checking Yarn...
where yarn >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%i in ('yarn -v') do echo   Version: %%i [OK]
) else (
    echo   [WARNING] Yarn not found. Installing...
    npm install -g yarn
)
echo.

echo [4/6] Checking Port 3000 (Frontend)...
netstat -ano | findstr :3000 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [WARNING] Port 3000 is IN USE
    netstat -ano | findstr :3000
) else (
    echo   Port 3000 is AVAILABLE [OK]
)
echo.

echo [5/6] Checking Port 8001 (Backend)...
netstat -ano | findstr :8001 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [WARNING] Port 8001 is IN USE
    netstat -ano | findstr :8001
) else (
    echo   Port 8001 is AVAILABLE [OK]
)
echo.

echo [6/6] Checking MongoDB connection...
if exist "%~dp0backend\.env" (
    echo   Backend .env file found [OK]
) else (
    echo   [ERROR] Backend .env file MISSING
    echo   Please create backend\.env with MONGO_URL
)
echo.

echo ============================================
echo           Diagnostics Complete
echo ============================================
echo.
pause
