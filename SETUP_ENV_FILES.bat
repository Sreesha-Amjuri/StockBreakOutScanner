@echo off
REM =====================================================
REM Create Missing .env Files
REM =====================================================

title StockBreak Pro - Setup Environment Files
color 0B

echo.
echo ========================================================
echo      STOCKBREAK PRO - ENVIRONMENT SETUP
echo ========================================================
echo.

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

echo [1/2] Creating Backend .env file...
cd backend

if exist .env (
    echo [INFO] Backend .env already exists
    echo Current contents:
    type .env
    echo.
    set /p "OVERWRITE=Overwrite? (Y/N): "
    if /i "%OVERWRITE%" NEQ "Y" goto frontend_env
)

echo Creating backend .env file...
(
echo MONGO_URL=mongodb://localhost:27017
echo DB_NAME=stockbreak_db
echo CORS_ORIGINS=*
) > .env

echo [OK] Backend .env created
echo.
echo Contents:
type .env
echo.

:frontend_env
cd ..
echo [2/2] Creating Frontend .env file...
cd frontend

if exist .env (
    echo [INFO] Frontend .env already exists
    echo Current contents:
    type .env
    echo.
    set /p "OVERWRITE=Overwrite? (Y/N): "
    if /i "%OVERWRITE%" NEQ "Y" goto done
)

echo Creating frontend .env file...
(
echo REACT_APP_BACKEND_URL=http://localhost:8001
) > .env

echo [OK] Frontend .env created
echo.
echo Contents:
type .env
echo.

:done
cd ..
echo.
echo ========================================================
echo         ENVIRONMENT FILES SETUP COMPLETE!
echo ========================================================
echo.
echo Backend .env location:
echo   %PROJECT_DIR%backend\.env
echo.
echo Frontend .env location:
echo   %PROJECT_DIR%frontend\.env
echo.
echo You can now start the application!
echo.
pause
