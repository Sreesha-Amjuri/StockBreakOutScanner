@echo off
echo ======================================
echo  StockBreak Pro - Docker Launch
echo ======================================
echo.

echo Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not running
    echo Please install Docker Desktop from https://docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo ✓ Docker found

echo.
echo Checking Docker Compose...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Compose not found
    echo Please ensure Docker Desktop is running
    pause
    exit /b 1
)
echo ✓ Docker Compose found

echo.
echo Building and starting StockBreak Pro...
echo This may take a few minutes on first run...
echo.

docker-compose up --build -d

if errorlevel 1 (
    echo ERROR: Failed to start containers
    echo Run 'docker-compose logs' to see detailed errors
    pause
    exit /b 1
)

echo.
echo ======================================
echo  StockBreak Pro Started Successfully!
echo ======================================
echo.
echo Services:
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8001
echo API Docs: http://localhost:8001/docs
echo.
echo New Features Available:
echo + 5-Stage Valuation Filter
echo + AI Chat Assistant (GPT-4o-mini)
echo + Dark/Light Theme Toggle
echo + Technical ^& Fundamental Analysis
echo.
echo To stop: docker-compose down
echo To view logs: docker-compose logs -f
echo.
echo Opening StockBreak Pro in your browser...
timeout /t 3 /nobreak >nul
start http://localhost:3000
echo.
pause