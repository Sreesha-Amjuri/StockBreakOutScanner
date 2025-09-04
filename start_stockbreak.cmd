@echo off
title StockBreak Pro - Starting Services
echo ======================================
echo  StockBreak Pro - Performance Optimized
echo ======================================
echo.

echo Starting backend server...
cd backend
start "StockBreak Pro Backend" cmd /k "python -m uvicorn server:app --reload --host 0.0.0.0 --port 8001"

echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

echo Starting frontend server...
cd ..\frontend  
start "StockBreak Pro Frontend" cmd /k "npm start"

echo.
echo ======================================
echo  StockBreak Pro Services Started!
echo ======================================
echo.
echo Backend API: http://localhost:8001
echo Frontend:    http://localhost:3000
echo API Docs:    http://localhost:8001/docs
echo.
echo Services are starting in separate windows...
echo Close this window when you're done.
echo.
pause