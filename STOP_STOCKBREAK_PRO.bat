@echo off
REM =====================================================
REM StockBreak Pro - Stop All Services
REM =====================================================

title StockBreak Pro - Stopping Services
color 0C

echo.
echo ========================================================
echo         STOPPING STOCKBREAK PRO SERVICES
echo ========================================================
echo.

echo [1/3] Stopping Frontend (Node.js)...
taskkill /F /FI "WINDOWTITLE eq StockBreak Pro - Frontend*" >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
if errorlevel 1 (
    echo [INFO] No frontend processes found
) else (
    echo [OK] Frontend stopped
)
echo.

echo [2/3] Stopping Backend (Python)...
taskkill /F /FI "WINDOWTITLE eq StockBreak Pro - Backend*" >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8001') do (
    taskkill /F /PID %%a >nul 2>&1
)
if errorlevel 1 (
    echo [INFO] No backend processes found
) else (
    echo [OK] Backend stopped
)
echo.

echo [3/3] Checking MongoDB...
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
echo StockBreak Pro has been stopped.
echo You can safely close this window.
echo.
pause
