@echo off
echo ======================================
echo  StockBreak Pro - Dependency Installer
echo ======================================
echo.

echo [1/3] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo.
echo [2/3] Installing backend dependencies...
cd backend

echo Installing FastAPI and Uvicorn...
pip install fastapi==0.110.1
pip install uvicorn==0.25.0

echo Installing core dependencies...
pip install -r requirements.txt

echo.
echo [3/3] Verifying uvicorn installation...
python -c "import uvicorn; print('✓ Uvicorn successfully installed')"
if errorlevel 1 (
    echo ERROR: Uvicorn installation failed
    echo Trying alternative installation...
    pip install --upgrade pip
    pip install uvicorn[standard]==0.25.0
    python -c "import uvicorn; print('✓ Uvicorn successfully installed')"
    if errorlevel 1 (
        echo ERROR: Uvicorn still not working
        pause
        exit /b 1
    )
)

cd ..
echo.
echo ======================================
echo  Dependencies Installed Successfully!
echo ======================================
echo.
echo You can now start the backend with:
echo cd backend
echo python -m uvicorn server:app --reload
echo.
pause