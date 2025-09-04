@echo off
echo ======================================
echo  StockBreak Pro - Windows Setup
echo  With Valuation Filter Feature
echo ======================================
echo.

echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo ✓ Python found

echo.
echo [2/6] Upgrading pip...
python -m pip install --upgrade pip
echo ✓ Pip upgraded

echo.
echo [3/6] Installing critical backend dependencies...
cd backend
echo Installing FastAPI and Uvicorn first...
pip install fastapi==0.110.1
pip install uvicorn==0.25.0

echo Installing remaining dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install backend dependencies
    echo Trying with --upgrade flag...
    pip install -r requirements.txt --upgrade
    if errorlevel 1 (
        echo ERROR: Backend installation failed completely
        pause
        exit /b 1
    )
)
echo ✓ Backend dependencies installed

echo.
echo [4/6] Verifying uvicorn installation...
python -c "import uvicorn; print('Uvicorn version:', uvicorn.__version__)"
if errorlevel 1 (
    echo ERROR: Uvicorn verification failed
    echo Installing uvicorn with standard extras...
    pip install uvicorn[standard]==0.25.0
    python -c "import uvicorn; print('Uvicorn version:', uvicorn.__version__)"
    if errorlevel 1 (
        echo ERROR: Uvicorn still not working
        pause
        exit /b 1
    )
)
echo ✓ Uvicorn verified

echo.
echo [5/6] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)
echo ✓ Node.js found

echo.
echo [6/6] Installing frontend dependencies...
cd ..\frontend
echo Installing with dependency resolution fixes...
npm install --legacy-peer-deps
if errorlevel 1 (
    echo ERROR: Failed to install frontend dependencies
    echo Trying alternative installation method...
    npm install --force
    if errorlevel 1 (
        echo ERROR: Frontend installation failed completely
        pause
        exit /b 1
    )
)
echo ✓ Frontend dependencies installed

cd ..
echo.
echo ======================================
echo  Setup Complete!
echo ======================================
echo.
echo New Features Added:
echo + Comprehensive Valuation Filter (5 categories)
echo + Financial Metrics Analysis (P/E, P/B, PEG, Dividend Yield)
echo + Weighted Scoring System with confidence levels
echo + Exception handling for missing financial data
echo.
echo To start StockBreak Pro:
echo 1. Run: start_stockbreak.cmd
echo.
echo Or manually:
echo 1. Backend: cd backend ^& python -m uvicorn server:app --reload --host 0.0.0.0 --port 8001
echo 2. Frontend: cd frontend ^& npm start
echo.
echo If you still get uvicorn errors, run: install_dependencies.bat
echo.
pause