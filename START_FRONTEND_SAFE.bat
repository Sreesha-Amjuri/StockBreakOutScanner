@echo off
REM =====================================================
REM Safe Frontend Start
REM =====================================================

cd /d "%~dp0frontend"

REM Create .env if missing
if not exist .env (
    echo REACT_APP_BACKEND_URL=http://localhost:8001 > .env
)

REM Set environment variable
set REACT_APP_BACKEND_URL=http://localhost:8001

REM Check if node_modules exists
if not exist node_modules (
    echo Installing dependencies...
    npm install --legacy-peer-deps
)

REM Start frontend
npm start
