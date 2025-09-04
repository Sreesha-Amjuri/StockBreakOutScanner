@echo off
echo ======================================
echo  StockBreak Pro - Backend Test
echo ======================================
echo.

echo Testing Python modules...
cd backend

echo [1/4] Testing FastAPI...
python -c "import fastapi; print('✓ FastAPI OK')"
if errorlevel 1 (
    echo ❌ FastAPI not found
    echo Run install_dependencies.bat first
    pause
    exit /b 1
)

echo [2/4] Testing Uvicorn...
python -c "import uvicorn; print('✓ Uvicorn OK')"
if errorlevel 1 (
    echo ❌ Uvicorn not found
    echo Run install_dependencies.bat first
    pause
    exit /b 1
)

echo [3/4] Testing other dependencies...
python -c "import yfinance, pandas, numpy; print('✓ Core modules OK')"
if errorlevel 1 (
    echo ❌ Some dependencies missing
    echo Run install_dependencies.bat first
    pause
    exit /b 1
)

echo [4/4] Testing server import...
python -c "from server import app; print('✓ Server module OK')"
if errorlevel 1 (
    echo ❌ Server module has issues
    pause
    exit /b 1
)

cd ..
echo.
echo ======================================
echo  All Tests Passed! ✓
echo ======================================
echo.
echo Backend is ready to start. Run:
echo cd backend
echo python -m uvicorn server:app --reload --host 0.0.0.0 --port 8001
echo.
pause