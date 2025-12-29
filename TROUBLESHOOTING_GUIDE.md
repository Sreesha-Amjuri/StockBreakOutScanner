# StockBreak Pro - Troubleshooting Guide

## Quick Start Options

### Option 1: Start Everything (Recommended)
Double-click **`START_STOCKBREAK.bat`**

### Option 2: Start Separately (If Option 1 fails)
1. First, double-click **`START_BACKEND.bat`** and wait for it to show "Uvicorn running"
2. Then, double-click **`START_FRONTEND.bat`**
3. Open browser to http://localhost:3000

---

## Common Issues & Solutions

### ❌ Backend Not Starting

**Symptoms:**
- Backend window closes immediately
- "uvicorn not found" error
- "Module not found" error

**Solutions:**

1. **Install Python dependencies manually:**
   ```
   cd backend
   pip install -r requirements.txt
   pip install uvicorn
   ```

2. **Run backend directly:**
   ```
   cd backend
   python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
   ```

3. **Check Python version (need 3.9+):**
   ```
   python --version
   ```

---

### ❌ Frontend Not Starting

**Symptoms:**
- "yarn not found" error
- Blank page at localhost:3000

**Solutions:**

1. **Install yarn:**
   ```
   npm install -g yarn
   ```

2. **Install dependencies manually:**
   ```
   cd frontend
   yarn install
   yarn start
   ```

---

### ❌ MongoDB Connection Error

**Symptoms:**
- Backend starts but shows "MongoDB connection failed"
- API returns 500 errors

**Solutions:**

1. **Install MongoDB Community Server:**
   Download from: https://www.mongodb.com/try/download/community

2. **Start MongoDB service:**
   - Windows: Open Services, find "MongoDB", click Start
   - Or run: `net start MongoDB`

3. **Verify MongoDB is running:**
   ```
   mongosh
   ```

---

### ❌ Rate Limiting Errors

**Symptoms:**
- "Rate limited, try again" errors
- Stock data not loading
- "Too many requests" messages

**Solutions:**

This is normal behavior from Yahoo Finance API (free tier). Wait 1-2 minutes and try again.

**Tips to reduce rate limiting:**
- Use "Quick Scan" instead of "Full Scan"
- Don't refresh stock data too frequently
- Add fewer stocks to watchlist at once

---

### ❌ Port Already in Use

**Symptoms:**
- "Port 8001 already in use"
- "Port 3000 already in use"

**Solutions:**

1. **Kill the process using the port:**
   ```
   netstat -ano | findstr :8001
   taskkill /PID <PID_NUMBER> /F
   ```

2. **Or restart your computer**

---

## Verify Installation

### Check Backend:
Open browser to: http://localhost:8001/docs

You should see FastAPI documentation page.

### Check Frontend:
Open browser to: http://localhost:3000

You should see the StockBreak Pro dashboard.

### Check APIs:
Open browser to: http://localhost:8001/api/stocks/search?q=REL

You should see JSON response with stock data.

---

## Support Files

| File | Purpose |
|------|---------|
| `START_STOCKBREAK.bat` | Start both backend and frontend |
| `START_BACKEND.bat` | Start backend only |
| `START_FRONTEND.bat` | Start frontend only |
| `STOP_STOCKBREAK.bat` | Stop all servers |
| `FIX_DEPENDENCIES.bat` | Reinstall all dependencies |

---

## Still Having Issues?

1. Make sure Python 3.9+ is installed
2. Make sure Node.js 16+ is installed
3. Make sure MongoDB is running
4. Try running servers in separate command windows manually
5. Check the console output for specific error messages
