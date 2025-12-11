# 🪟 StockBreak Pro - Windows Setup Guide

## 🎯 Run the Web Application on Windows

This guide will help you run StockBreak Pro web application on your Windows computer and access it in your browser.

---

## 📋 Prerequisites

Before starting, you need:

### Required Software:

1. **Python 3.8+** 
   - Download: https://www.python.org/downloads/
   - ✅ During installation, CHECK "Add Python to PATH"

2. **Node.js 18+**
   - Download: https://nodejs.org/
   - Choose "LTS" version
   - ✅ Install with default settings

3. **MongoDB**
   - Download: https://www.mongodb.com/try/download/community
   - Choose "Windows" version
   - ✅ Install as a service

### Verify Installation:

Open **Command Prompt** (cmd) and run:

```cmd
python --version
node --version
npm --version
mongod --version
```

You should see version numbers for all. If not, reinstall and ensure "Add to PATH" is checked.

---

## 🚀 Method 1: Quick Start (Using Script)

### Step 1: Download the Project

1. Download all files from `/app/` folder to your computer
2. Place in: `C:\StockBreakPro\`
3. You should have folders: `backend`, `frontend`, `mobile`, etc.

### Step 2: Run the Launcher Script

**Option A: Double-click**
1. Navigate to `C:\StockBreakPro\`
2. **Double-click** on `start_stockbreak.cmd`
3. Wait for services to start
4. Browser opens automatically at http://localhost:3000

**Option B: Right-click Run as Administrator**
1. Right-click `start_stockbreak.cmd`
2. Select "Run as administrator"
3. Wait for services to start

### Step 3: Access the Application

The script will automatically:
- ✅ Start MongoDB
- ✅ Start Backend (port 8001)
- ✅ Start Frontend (port 3000)
- ✅ Open browser to http://localhost:3000

**That's it!** 🎉

---

## 🔧 Method 2: Manual Start (Step by Step)

If the script doesn't work, follow these manual steps:

### Step 1: Start MongoDB

**Option A: If installed as service**
```cmd
net start MongoDB
```

**Option B: Manual start**
```cmd
mongod
```

Keep this window open.

### Step 2: Setup Backend

Open **new Command Prompt** and run:

```cmd
# Navigate to project
cd C:\StockBreakPro\backend

# Create virtual environment (first time only)
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Start backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**You should see**:
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete
```

Keep this window open.

### Step 3: Setup Frontend

Open **another new Command Prompt** and run:

```cmd
# Navigate to frontend
cd C:\StockBreakPro\frontend

# Install dependencies (first time only)
npm install
# or
yarn install

# Start frontend
npm start
# or
yarn start
```

**You should see**:
```
Compiled successfully!
Local:            http://localhost:3000
```

Browser opens automatically. Keep this window open.

### Step 4: Access the Application

Open your browser and go to:
```
http://localhost:3000
```

**You should see**: Beautiful pastel purple StockBreak Pro dashboard! 🎉

---

## 📱 Using the Application

### First Time Use:

1. **Dashboard loads** showing:
   - Stocks Scanned count
   - Breakouts Found count
   - List of stocks in breakout

2. **Features available**:
   - 🔍 Search stocks
   - 📊 View technical analysis
   - 💡 See trading recommendations
   - ⭐ Add to watchlist
   - 🔄 Pull to refresh
   - 🌓 Dark/Light mode toggle

### Navigation:

- **Dashboard**: Main page with all breakout stocks
- **Stock Details**: Click any stock card to see detailed analysis
- **Watchlist**: View your saved stocks
- **Settings**: Configure preferences

---

## 🔌 Accessing from Other Devices

### On Same Network (LAN):

1. **Find your computer's IP address**:
   ```cmd
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

2. **On another device** (phone, tablet, other computer):
   ```
   http://YOUR_IP_ADDRESS:3000
   ```
   Example: `http://192.168.1.100:3000`

3. **Make sure**:
   - Both devices on same WiFi network
   - Windows Firewall allows connections

### Open Firewall (if needed):

1. Search for "Windows Defender Firewall"
2. Click "Advanced settings"
3. Click "Inbound Rules" → "New Rule"
4. Port → TCP → Port 3000 and 8001
5. Allow connection → Name it "StockBreak Pro"

---

## 🛑 Stopping the Application

### If using script:
- Just close the Command Prompt windows

### If running manually:
1. Press `Ctrl + C` in each Command Prompt window
2. Type `Y` when asked to terminate

### Stop MongoDB:
```cmd
net stop MongoDB
```

---

## 🔄 Restarting After Computer Restart

### Quick Method:
1. Double-click `start_stockbreak.cmd`

### Manual Method:
1. Start MongoDB (if not auto-starting)
2. Open Command Prompt → Navigate to backend
3. Run: `venv\Scripts\activate && uvicorn server:app --host 0.0.0.0 --port 8001`
4. Open another Command Prompt → Navigate to frontend
5. Run: `npm start`

---

## 🐛 Troubleshooting

### Backend won't start

**Error**: "Port 8001 already in use"
```cmd
# Kill process on port 8001
netstat -ano | findstr :8001
taskkill /PID <PID_NUMBER> /F
```

**Error**: "Module not found"
```cmd
cd backend
pip install -r requirements.txt
```

**Error**: "MongoDB connection failed"
```cmd
# Start MongoDB
net start MongoDB
# Or manually
mongod
```

---

### Frontend won't start

**Error**: "Port 3000 already in use"
```cmd
# Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F
```

**Error**: "Command 'npm' not found"
- Reinstall Node.js
- Ensure "Add to PATH" is checked

**Error**: "Dependencies not installed"
```cmd
cd frontend
npm install
```

---

### Application not loading

**Blank page**:
1. Open browser console (F12)
2. Check for errors
3. Ensure backend is running
4. Check backend URL in frontend/.env

**Connection refused**:
1. Verify backend is running on port 8001
2. Verify frontend is running on port 3000
3. Check firewall settings

**Data not loading**:
1. Check MongoDB is running
2. Check backend logs for errors
3. Verify internet connection (for stock data)

---

### MongoDB issues

**Error**: "MongoDB service not found"
```cmd
# Reinstall MongoDB as a service
# Or run manually:
mongod --dbpath C:\data\db
```

**Error**: "Data directory not found"
```cmd
# Create data directory
mkdir C:\data\db
mongod --dbpath C:\data\db
```

---

## 📊 Verifying Everything Works

### Check Backend:

Open browser and go to:
```
http://localhost:8001/api/
```

You should see: `{"message":"Indian Stock Breakout Screener API - Enhanced Version"}`

### Check Frontend:

Go to:
```
http://localhost:3000
```

You should see the dashboard with stock data.

### Test API:

Open browser and go to:
```
http://localhost:8001/api/stocks/symbols
```

You should see JSON data with stock symbols.

---

## 🎨 Application Features

### Dashboard:
- ✅ Real-time stock scanning
- ✅ Breakout detection
- ✅ Technical indicators
- ✅ Search functionality
- ✅ Filter by sector
- ✅ Sort by multiple columns

### Stock Details:
- ✅ Interactive charts
- ✅ Technical analysis (RSI, MACD, Bollinger Bands)
- ✅ Trading recommendations
- ✅ Risk assessment
- ✅ Support/Resistance levels

### Watchlist:
- ✅ Save favorite stocks
- ✅ Track performance
- ✅ Set price alerts
- ✅ Add notes

---

## ⚙️ Configuration

### Backend Configuration:

Edit `backend/.env`:
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=stockbreak_db
CORS_ORIGINS=*
```

### Frontend Configuration:

Edit `frontend/.env`:
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

---

## 🔐 Security Notes

### For Local Use Only:
- Default configuration allows local access
- Safe for development and personal use

### For Network Access:
1. Change `CORS_ORIGINS` in backend/.env
2. Add your IP address or use `*` (less secure)
3. Configure firewall rules
4. Consider using HTTPS

---

## 📂 Project Structure

```
C:\StockBreakPro\
├── backend\
│   ├── server.py          ← Main backend file
│   ├── requirements.txt   ← Python dependencies
│   ├── .env              ← Backend configuration
│   └── venv\             ← Virtual environment
│
├── frontend\
│   ├── src\              ← React source code
│   ├── public\           ← Static files
│   ├── package.json      ← Node dependencies
│   └── .env              ← Frontend configuration
│
├── mobile\               ← Android app (separate)
├── start_stockbreak.cmd  ← Quick launcher
└── README.md             ← Documentation
```

---

## 🚀 Performance Tips

### Speed Up Loading:
1. Keep MongoDB running (installed as service)
2. Use SSD for database storage
3. Increase MongoDB cache size
4. Use production build for frontend

### Production Build:
```cmd
cd frontend
npm run build
# Serve with: npx serve -s build
```

---

## 🆘 Getting Help

### Log Files:

**Backend logs**:
```cmd
# Check terminal where backend is running
# Or check: backend/stock_screener.log
```

**Frontend logs**:
```cmd
# Check browser console (F12)
# Or check terminal where frontend is running
```

### Debug Mode:

**Backend**:
```cmd
uvicorn server:app --host 0.0.0.0 --port 8001 --reload --log-level debug
```

**Frontend**:
- Already in development mode when using `npm start`

---

## 📝 Quick Reference

### URLs:
```
Frontend:  http://localhost:3000
Backend:   http://localhost:8001
API Docs:  http://localhost:8001/docs
```

### Commands:

**Start Everything**:
```cmd
# Double-click: start_stockbreak.cmd
```

**Start Backend Only**:
```cmd
cd backend
venv\Scripts\activate
uvicorn server:app --host 0.0.0.0 --port 8001
```

**Start Frontend Only**:
```cmd
cd frontend
npm start
```

**Stop Everything**:
```cmd
Ctrl + C in each window
```

---

## ✅ Success Checklist

- [ ] Python installed and in PATH
- [ ] Node.js installed and in PATH
- [ ] MongoDB installed and running
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can access http://localhost:3000
- [ ] Dashboard loads with stock data
- [ ] Can click on stocks for details
- [ ] Watchlist works
- [ ] Search works

---

## 🎊 Enjoy StockBreak Pro!

Once everything is running, you have:
- ✅ Professional stock analysis tool
- ✅ Real-time breakout detection
- ✅ Technical indicators
- ✅ Trading recommendations
- ✅ Beautiful pastel UI

**Happy stock scanning on Windows!** 📊💻✨
