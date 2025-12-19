@echo off
REM =====================================================
REM Create .env files with NO trailing spaces
REM =====================================================

title Create Environment Files
color 0B

echo.
echo ========================================================
echo       CREATING ENVIRONMENT FILES
echo ========================================================
echo.

cd /d "%~dp0"

REM ============================================
REM Backend .env
REM ============================================
echo [1/2] Creating backend/.env...
cd backend

echo MONGO_URL=mongodb://localhost:27017> .env
echo DB_NAME=stockbreak_db>> .env
echo CORS_ORIGINS=*>> .env

echo [OK] Created backend/.env
echo.
echo Contents:
type .env
echo.

cd ..

REM ============================================
REM Frontend .env
REM ============================================
echo [2/2] Creating frontend/.env...
cd frontend

echo REACT_APP_BACKEND_URL=http://localhost:8001> .env

echo [OK] Created frontend/.env
echo.
echo Contents:
type .env
echo.

cd ..

echo ========================================================
echo       ENVIRONMENT FILES CREATED
echo ========================================================
echo.
echo You can now start the application!
echo.
pause
