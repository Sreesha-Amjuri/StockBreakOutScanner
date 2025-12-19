@echo off
title StockBreak Pro - Fix Dependencies
color 0E

echo ============================================
echo    StockBreak Pro - Dependency Fixer
echo ============================================
echo.
echo This will reinstall all dependencies.
echo.
pause

echo.
echo [1/4] Cleaning Frontend...
cd /d "%~dp0frontend"
if exist node_modules rmdir /s /q node_modules
if exist yarn.lock del /f yarn.lock
if exist package-lock.json del /f package-lock.json
echo   Cleaned frontend dependencies.

echo.
echo [2/4] Installing Frontend Dependencies...
call yarn install
if %ERRORLEVEL% NEQ 0 (
    echo   [WARNING] Trying with legacy peer deps...
    call npm install --legacy-peer-deps
)
echo   Frontend dependencies installed.

echo.
echo [3/4] Installing Backend Dependencies...
cd /d "%~dp0backend"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo   Backend dependencies installed.

echo.
echo [4/4] Verifying installation...
cd /d "%~dp0frontend"
call yarn list react --depth=0
echo.

echo ============================================
echo       Dependency Fix Complete!
echo ============================================
echo.
echo You can now run START_STOCKBREAK.bat
echo.
pause
