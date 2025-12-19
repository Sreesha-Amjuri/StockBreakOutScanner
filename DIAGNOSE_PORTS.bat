@echo off
REM =====================================================
REM Diagnose Port Status
REM =====================================================

title Port Diagnostics
color 0E

echo.
echo ========================================================
echo           PORT DIAGNOSTICS
echo ========================================================
echo.

echo Checking what's running on ports 3000 and 8001...
echo.

echo [PORT 3000 - Frontend]
netstat -ano | findstr :3000
if errorlevel 1 (
    echo [STATUS] Nothing running on port 3000
    echo [ERROR] Frontend is NOT running!
) else (
    echo [STATUS] Something is running on port 3000
)
echo.

echo [PORT 8001 - Backend]
netstat -ano | findstr :8001
if errorlevel 1 (
    echo [STATUS] Nothing running on port 8001
    echo [ERROR] Backend is NOT running!
) else (
    echo [STATUS] Something is running on port 8001
)
echo.

echo ========================================================
echo           RECOMMENDATIONS
echo ========================================================
echo.
echo If port 3000 shows nothing:
echo   - Frontend did not start successfully
echo   - Check the Frontend window for errors
echo   - Manually start: cd frontend ^&^& npm start
echo.
echo If port 8001 shows backend only:
echo   - This is correct for backend
echo   - Access backend API: http://localhost:8001/api/
echo   - Frontend should be on port 3000
echo.
pause
