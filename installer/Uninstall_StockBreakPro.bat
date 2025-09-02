@echo off
title StockBreak Pro - Uninstaller
color 0C

echo.
echo ========================================
echo    StockBreak Pro - Uninstaller
echo ========================================
echo.
echo This will remove StockBreak Pro from your system.
echo.
set /p confirm=Are you sure you want to uninstall? (Y/N): 

if /I not "%confirm%"=="Y" (
    echo Uninstall cancelled.
    pause
    exit /b 0
)

echo.
echo [1/5] Stopping StockBreak Pro services...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq*StockBreak*" 2>nul
taskkill /F /IM node.exe /FI "WINDOWTITLE eq*StockBreak*" 2>nul
taskkill /F /IM mongod.exe 2>nul
echo [✓] Services stopped

echo.
echo [2/5] Removing application files...
set "INSTALL_DIR=C:\StockBreakPro"
if exist "%INSTALL_DIR%" (
    rmdir /S /Q "%INSTALL_DIR%"
    echo [✓] Application files removed
) else (
    echo [!] Installation directory not found
)

echo.
echo [3/5] Removing desktop shortcuts...
if exist "%USERPROFILE%\Desktop\StockBreak Pro.lnk" (
    del "%USERPROFILE%\Desktop\StockBreak Pro.lnk"
    echo [✓] Desktop shortcut removed
)

echo.
echo [4/5] Removing start menu shortcuts...
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\StockBreak Pro" (
    rmdir /S /Q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\StockBreak Pro"
    echo [✓] Start menu shortcuts removed
)

echo.
echo [5/5] Cleanup complete...
echo.
echo ========================================
echo    Uninstall Complete
echo ========================================
echo.
echo StockBreak Pro has been removed from your system.
echo.
echo Note: MongoDB, Python, and Node.js were NOT removed
echo as they may be used by other applications.
echo.
echo Thank you for using StockBreak Pro!
echo.
pause