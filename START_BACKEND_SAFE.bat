@echo off
REM =====================================================
REM Safe Backend Start with Environment Variables
REM =====================================================

cd /d "%~dp0backend"

REM Set environment variables BEFORE starting
set MONGO_URL=mongodb://localhost:27017
set DB_NAME=stockbreak_db
set CORS_ORIGINS=*

REM Activate venv
call venv\Scripts\activate.bat

REM Start backend with env vars
uvicorn server:app --host 0.0.0.0 --port 8001
