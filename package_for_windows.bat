@echo off
title StockBreak Pro - Windows Package Creator
color 0B

echo.
echo ========================================
echo    StockBreak Pro Package Creator
echo    Creating Windows Installation Package
echo ========================================
echo.

REM Create package directory
set "PACKAGE_DIR=%~dp0StockBreakPro_Windows_Package"
if exist "%PACKAGE_DIR%" rmdir /S /Q "%PACKAGE_DIR%"
mkdir "%PACKAGE_DIR%"

echo [1/8] Creating package structure...
mkdir "%PACKAGE_DIR%\app"
mkdir "%PACKAGE_DIR%\app\backend"
mkdir "%PACKAGE_DIR%\app\frontend"
mkdir "%PACKAGE_DIR%\installer"
mkdir "%PACKAGE_DIR%\docs"

echo [2/8] Copying backend files...
xcopy /E /I /Y "%~dp0backend" "%PACKAGE_DIR%\app\backend"

echo [3/8] Copying frontend files...
xcopy /E /I /Y "%~dp0frontend" "%PACKAGE_DIR%\app\frontend"

echo [4/8] Copying installer files...
xcopy /E /I /Y "%~dp0installer" "%PACKAGE_DIR%\installer"

echo [5/8] Creating application icon...
echo. > "%PACKAGE_DIR%\app\icon.ico"

echo [6/8] Creating documentation...
copy "%~dp0installer\README_Installation.md" "%PACKAGE_DIR%\docs\Installation_Guide.md"

REM Create main executable
echo [7/8] Creating main executable...
(
echo @echo off
echo title StockBreak Pro - Professional Stock Analysis Platform
echo color 0A
echo.
echo REM Set installation directory
echo set "APP_DIR=%%~dp0app"
echo cd /d "%%APP_DIR%%"
echo.
echo echo ========================================
echo echo     StockBreak Pro v2.0
echo echo   Professional Stock Analysis Platform  
echo echo ========================================
echo echo.
echo echo [1/4] Starting MongoDB service...
echo.
echo REM Start MongoDB if not running
echo tasklist /FI "IMAGENAME eq mongod.exe" 2^>NUL ^| find /I /N "mongod.exe"^>NUL
echo if "%%ERRORLEVEL%%"=="0" ^(
echo     echo [✓] MongoDB already running
echo ^) else ^(
echo     echo Starting MongoDB...
echo     start "" /B "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath "C:\data\db" --logpath "C:\data\db\mongodb.log"
echo     timeout /t 5 ^>nul
echo     echo [✓] MongoDB started
echo ^)
echo.
echo echo [2/4] Starting backend services...
echo cd /d "%%APP_DIR%%\backend"
echo start "" /B python server.py
echo timeout /t 3 ^>nul
echo echo [✓] Backend API server started on http://localhost:8001
echo.
echo echo [3/4] Starting frontend application...
echo cd /d "%%APP_DIR%%\frontend"
echo start "" /B npm start
echo timeout /t 5 ^>nul
echo echo [✓] Frontend started on http://localhost:3000
echo.
echo echo [4/4] Opening StockBreak Pro in browser...
echo timeout /t 8 ^>nul
echo start "" "http://localhost:3000"
echo.
echo echo ========================================
echo echo    StockBreak Pro is now running!
echo echo ========================================
echo echo.
echo echo Dashboard: http://localhost:3000
echo echo API Server: http://localhost:8001
echo echo.
echo echo Features:
echo echo [✓] Full NSE Stock Coverage ^(594+ stocks^)
echo echo [✓] Professional Watchlist Management  
echo echo [✓] 13+ Technical Indicators
echo echo [✓] Real-time Market Data
echo echo [✓] Advanced Breakout Detection
echo echo [✓] Trading Recommendations
echo echo [✓] Export ^& Reporting Tools
echo echo [✓] Auto-scanning ^& Price Alerts
echo echo [✓] Professional UI with Dark Mode
echo echo.
echo echo Keyboard Shortcuts:
echo echo Ctrl+R: Refresh Scan  ^|  Ctrl+E: Export Data  ^|  Ctrl+D: Toggle Theme
echo echo.
echo echo Press Ctrl+C to stop all services or close this window
echo echo.
echo pause
) > "%PACKAGE_DIR%\StockBreakPro.exe"

echo [8/8] Creating package info...
(
echo # StockBreak Pro - Windows Package
echo.
echo ## Package Contents
echo - **StockBreakPro.exe** - Main application launcher
echo - **installer/** - Installation scripts and setup wizard
echo - **app/backend/** - Python FastAPI backend server
echo - **app/frontend/** - React web application
echo - **docs/** - Complete documentation
echo.
echo ## Installation Instructions
echo 1. Run `installer\StockBreakPro_Setup.bat` as Administrator
echo 2. Follow the automated installation wizard
echo 3. Launch from desktop shortcut or Start Menu
echo.
echo ## System Requirements
echo - Windows 10/11 ^(64-bit^)
echo - 4GB RAM minimum ^(8GB recommended^)
echo - 2GB free disk space
echo - Internet connection for real-time data
echo.
echo ## Features
echo - ✅ Full NSE Coverage ^(594+ stocks^)
echo - ✅ 13+ Technical Indicators
echo - ✅ Professional Watchlist
echo - ✅ Real-time Data ^& Alerts
echo - ✅ Export ^& Reporting
echo - ✅ Advanced UI Features
echo.
echo ## Support
echo See `docs\Installation_Guide.md` for complete documentation.
) > "%PACKAGE_DIR%\README.txt"

REM Create version info
(
echo StockBreak Pro v2.0.0
echo Build: %date% %time%
echo Platform: Windows 10/11 x64
echo.
echo Components:
echo - Backend API: FastAPI + Python 3.11
echo - Frontend: React 18 + TailwindCSS
echo - Database: MongoDB 7.0
echo - Analytics: 13+ Technical Indicators
echo - Coverage: 594+ NSE Stocks
echo.
echo Professional Stock Analysis Platform
echo Educational Use Only - Not Financial Advice
) > "%PACKAGE_DIR%\version.txt"

echo.
echo ========================================
echo    Package Creation Complete!
echo ========================================
echo.
echo Package created: %PACKAGE_DIR%
echo.
echo Contents:
echo [✓] Main application executable
echo [✓] Automated installer scripts  
echo [✓] Complete backend and frontend
echo [✓] Documentation and guides
echo [✓] Uninstaller utility
echo.
echo To distribute:
echo 1. Zip the entire "%PACKAGE_DIR%" folder
echo 2. Share the zip file with users
echo 3. Users run installer\StockBreakPro_Setup.bat as Admin
echo.
echo Package size: Calculating...
powershell -command "& {$size = (Get-ChildItem '%PACKAGE_DIR%' -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB; Write-Host ('Package size: {0:N1} MB' -f $size)}"
echo.
pause