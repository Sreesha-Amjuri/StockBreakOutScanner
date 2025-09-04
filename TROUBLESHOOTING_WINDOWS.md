# StockBreak Pro - Windows Troubleshooting Guide

## Common Issues and Solutions

### 1. "No module named uvicorn" Error

**Problem**: Getting `python.exe: No module named uvicorn` when starting backend

**Solutions** (try in order):

#### Solution A: Run the dependency installer
```cmd
# Navigate to StockBreak Pro folder
install_dependencies.bat
```

#### Solution B: Manual uvicorn installation
```cmd
cd backend
pip install uvicorn==0.25.0
pip install uvicorn[standard]==0.25.0
```

#### Solution C: Virtual environment approach
```cmd
# Create virtual environment
python -m venv stockbreak_env

# Activate virtual environment
stockbreak_env\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Start backend
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

#### Solution D: Check Python PATH
```cmd
# Check if Python is in PATH
python --version
pip --version

# If not found, add Python to PATH or reinstall Python with "Add to PATH" option
```

### 2. NPM Dependency Conflicts

**Problem**: Getting `npm error ERESOLVE unable to resolve dependency tree`

**Solutions**:

```cmd
cd frontend

# Try legacy peer deps
npm install --legacy-peer-deps

# If that fails, try force
npm install --force

# If still failing, clear cache and retry
npm cache clean --force
npm install --legacy-peer-deps
```

### 3. Backend Won't Start

**Problem**: Backend starts but shows errors or crashes

**Solutions**:

#### Check dependencies
```cmd
# Run the test script
test_backend.bat
```

#### Check for missing modules
```cmd
cd backend
python -c "import fastapi, uvicorn, yfinance, pandas"
```

#### Reinstall problematic modules
```cmd
pip uninstall uvicorn fastapi
pip install uvicorn==0.25.0 fastapi==0.110.1
```

### 4. Frontend Won't Start

**Problem**: Frontend shows compilation errors

**Solutions**:

```cmd
cd frontend

# Clear node_modules and reinstall
rmdir /s node_modules
npm install --legacy-peer-deps

# If React version conflicts
npm install react@19.0.0 react-dom@19.0.0 --legacy-peer-deps
```

### 5. Port Already in Use

**Problem**: `Error: listen EADDRINUSE: address already in use :::8001`

**Solutions**:

```cmd
# Find what's using port 8001
netstat -ano | findstr :8001

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use different ports
# Backend:
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8002

# Update frontend .env file to point to new backend port
```

### 6. MongoDB Connection Issues

**Problem**: Backend logs show MongoDB connection errors

**Solutions**:

The app uses MongoDB internally - if you see connection errors:

1. **Check if backend is using correct MongoDB URL** in `.env` file
2. **Restart the application** - MongoDB should start automatically
3. **Check supervisor logs**:
   ```cmd
   # Check backend logs for detailed error messages
   ```

### 7. Slow Performance or Timeouts

**Problem**: Stock scanning takes too long or times out

**Solutions**:

1. **Reduce scan limit**:
   - In the UI, use smaller numbers (10-20 stocks instead of 50)
   
2. **Check internet connection**:
   - The app fetches real-time stock data from Yahoo Finance
   
3. **Clear cache**:
   ```cmd
   cd backend
   # Remove any cache files
   del *.cache 2>nul
   ```

## Quick Diagnostic Commands

### Test Python Environment
```cmd
python --version
pip --version
python -c "import sys; print(sys.executable)"
```

### Test Backend Dependencies
```cmd
cd backend
python -c "import fastapi, uvicorn, yfinance, pandas, numpy; print('All modules OK')"
```

### Test Frontend Dependencies
```cmd
cd frontend
npm list react react-dom
```

### Test API Connectivity
```cmd
# After starting backend, test in browser:
# http://localhost:8001/docs
```

## Complete Reinstallation

If all else fails, complete clean reinstall:

```cmd
# 1. Delete node_modules
cd frontend
rmdir /s node_modules
cd ..

# 2. Reinstall Python packages
cd backend
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
cd ..

# 3. Reinstall Node packages
cd frontend
npm install --legacy-peer-deps
cd ..

# 4. Run setup again
setup_windows.bat
```

## Getting Help

1. **Check the error logs** carefully for specific error messages
2. **Run the test scripts**: `test_backend.bat` and diagnostic commands
3. **Try the specific solution** for your error message above
4. **Use virtual environment** if you have Python conflicts

## System Requirements Reminder

- **Windows 10/11** (64-bit recommended)
- **Python 3.8+** (3.11 recommended)
- **Node.js 16+** (18+ recommended)
- **4GB+ RAM** (8GB+ recommended)
- **Stable internet connection** for real-time stock data