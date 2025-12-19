@echo off
REM =====================================================
REM StockBreak Pro - Service Diagnostics
REM =====================================================

title StockBreak Pro - Diagnostics
color 0E

echo.
echo ========================================================
echo         STOCKBREAK PRO - SERVICE DIAGNOSTICS
echo ========================================================
echo.

echo [1] Checking Node.js Version...
node --version
if errorlevel 1 (
    echo [ERROR] Node.js not found!
) else (
    echo [OK] Node.js installed
)
echo.

echo [2] Checking Python Version...
python --version
if errorlevel 1 (
    echo [ERROR] Python not found!
) else (
    echo [OK] Python installed
)
echo.

echo [3] Checking if Backend is running (Port 8001)...
netstat -ano | findstr :8001
if errorlevel 1 (
    echo [INFO] Backend NOT running on port 8001
) else (
    echo [OK] Backend is running on port 8001
)
echo.

echo [4] Checking if Frontend is running (Port 3000)...
netstat -ano | findstr :3000
if errorlevel 1 (
    echo [INFO] Frontend NOT running on port 3000
) else (
    echo [OK] Frontend is running on port 3000
)
echo.

echo [5] Checking MongoDB service...
sc query MongoDB | findstr STATE
if errorlevel 1 (
    echo [INFO] MongoDB service not found or not running
) else (
    echo [OK] MongoDB service found
)
echo.

echo [6] Testing Backend API...
curl -s http://localhost:8001/api/ >nul 2>&1
if errorlevel 1 (
    echo [INFO] Backend API NOT responding
) else (
    echo [OK] Backend API is responding
)
echo.

echo [7] Testing Frontend...
curl -s http://localhost:3000 >nul 2>&1
if errorlevel 1 (
    echo [INFO] Frontend NOT responding
) else (
    echo [OK] Frontend is responding
)
echo.

echo ========================================================
echo                  DIAGNOSTIC COMPLETE
echo ========================================================
echo.
echo If Backend or Frontend are NOT running:
echo 1. Check the Backend/Frontend windows for errors
echo 2. Read TROUBLESHOOT_FRONTEND.md for solutions
echo.
pause
