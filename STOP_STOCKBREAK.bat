@echo off
title StockBreak Pro - Stop Services
color 0C

echo ============================================
echo       Stopping StockBreak Pro Services
echo ============================================
echo.

echo Stopping Node.js processes...
taskkill /F /IM node.exe >nul 2>&1

echo Stopping Python processes...
taskkill /F /FI "WINDOWTITLE eq StockBreak Backend*" >nul 2>&1

echo.
echo [OK] All StockBreak services stopped.
echo.
pause
