@echo off
REM =====================================================
REM StockBreak Pro - Stop Script
REM =====================================================

title StockBreak Pro - Stopping Services
color 0C

echo.
echo ========================================================
echo         STOPPING STOCKBREAK PRO SERVICES
echo ========================================================
echo.

REM Kill Node.js processes (Frontend)
echo [1/3] Stopping Frontend...
taskkill /F /IM node.exe >nul 2>&1
if errorlevel 1 (
    echo [INFO] No frontend processes found
) else (
    echo [OK] Frontend stopped
)

REM Kill Python processes (Backend)
echo [2/3] Stopping Backend...
taskkill /F /IM python.exe >nul 2>&1
if errorlevel 1 (
    echo [INFO] No backend processes found
) else (
    echo [OK] Backend stopped
)

REM Optionally stop MongoDB
echo [3/3] MongoDB service status...
net stop MongoDB >nul 2>&1
if errorlevel 1 (
    echo [INFO] MongoDB service not stopped (may be needed by other apps)
) else (
    echo [OK] MongoDB service stopped
)

echo.
echo ========================================================
echo           ALL SERVICES STOPPED
echo ========================================================
echo.
echo Press any key to exit...
pause >nul
