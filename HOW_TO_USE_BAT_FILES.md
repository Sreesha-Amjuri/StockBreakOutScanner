# 🎯 How to Use the Batch Files

## 📁 What You Need to Do

### Step 1: Copy the Batch Files

Copy these two files to your project folder:

```
C:\Users\srees\Downloads\StockBreakOutScanner-feature-windows-installer-emergentAI\StockBreakOutScanner-feature-windows-installer-emergentAI\
```

The files you need to copy:
1. **RUN_STOCKBREAK_PRO.bat** - Starts everything
2. **STOP_STOCKBREAK_PRO.bat** - Stops everything

---

## 🚀 To START the Application

### Method 1: Double-Click (Easiest!)

1. Navigate to your project folder
2. **Double-click** `RUN_STOCKBREAK_PRO.bat`
3. Two windows will open:
   - **Green window** = Backend Server (Port 8001)
   - **Red window** = Frontend (Port 3000)
4. Wait 20-30 seconds
5. Browser opens automatically at http://localhost:3000
6. **Done!** 🎉

### Method 2: Right-Click → Run as Administrator

If double-click doesn't work:
1. Right-click `RUN_STOCKBREAK_PRO.bat`
2. Select "Run as administrator"
3. Follow the same process

---

## 🛑 To STOP the Application

### Method 1: Double-Click Stop Script

1. **Double-click** `STOP_STOCKBREAK_PRO.bat`
2. All services stop automatically

### Method 2: Close Windows Manually

1. Close the **Backend** window (green)
2. Close the **Frontend** window (red)
3. Press `Ctrl+C` if asked to confirm

### Method 3: Press Ctrl+C

1. Click on the Backend window
2. Press `Ctrl+C`
3. Type `Y` and press Enter
4. Repeat for Frontend window

---

## 📊 What the Script Does

### When You Run RUN_STOCKBREAK_PRO.bat:

```
1. ✅ Checks Python installed
2. ✅ Checks Node.js installed
3. ✅ Starts MongoDB service
4. ✅ Opens Backend window:
   - Creates virtual environment (if needed)
   - Installs Python dependencies (if needed)
   - Starts backend server on port 8001
5. ✅ Opens Frontend window:
   - Installs Node dependencies (if needed)
   - Starts frontend on port 3000
6. ✅ Waits 20 seconds
7. ✅ Opens browser to http://localhost:3000
8. ✅ Shows success message
```

---

## 🎨 What You'll See

### Main Launcher Window (Blue):
```
========================================================
           STOCKBREAK PRO - LAUNCHER
========================================================

Starting Backend and Frontend in separate windows...

[STEP 1/4] Checking prerequisites...
[OK] Python found
[OK] Node.js found

[STEP 2/4] Starting MongoDB...
[OK] MongoDB started

[STEP 3/4] Starting Backend Server...
[OK] Backend window opened

[STEP 4/4] Starting Frontend...
[OK] Frontend window opened

========================================================
          STOCKBREAK PRO IS STARTING!
========================================================

Two windows have been opened:
  1. Backend Server (Green) - Port 8001
  2. Frontend (Red) - Port 3000
```

### Backend Window (Green):
```
========================================
   STOCKBREAK PRO - BACKEND SERVER
========================================

[INFO] Creating virtual environment...
[OK] Virtual environment created
[INFO] Activating virtual environment...
[INFO] Installing backend dependencies...
[OK] Dependencies installed

========================================
[INFO] Starting Backend Server...
Backend URL: http://localhost:8001
API Docs: http://localhost:8001/docs
========================================

INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete
```

### Frontend Window (Red):
```
========================================
   STOCKBREAK PRO - FRONTEND
========================================

[INFO] Installing frontend dependencies...
This will take 2-3 minutes...
[OK] Dependencies installed

========================================
[INFO] Starting Frontend...
Frontend URL: http://localhost:3000
========================================

Browser will open automatically...

Compiled successfully!
webpack compiled successfully
```

---

## 🌐 Accessing the Application

Once everything is running:

### On Your Computer:
```
Main App:    http://localhost:3000
Backend:     http://localhost:8001
API Docs:    http://localhost:8001/docs
```

### On Other Devices (Phone, Tablet):

1. Find your computer's IP address:
   ```cmd
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

2. On other device (same WiFi):
   ```
   http://192.168.1.100:3000
   ```

---

## 🐛 Troubleshooting

### "Python not found" Error

**Solution**: Install Python
- Download: https://www.python.org/downloads/
- ✅ Check "Add Python to PATH" during installation
- Restart command prompt

---

### "Node.js not found" Error

**Solution**: Install Node.js
- Download: https://nodejs.org/
- Choose "LTS" version
- Restart command prompt

---

### "MongoDB not started" Warning

**Solution**: Install MongoDB
- Download: https://www.mongodb.com/try/download/community
- Install as Windows Service
- Or manually start: `mongod`

---

### Port Already in Use

**Backend (Port 8001) or Frontend (Port 3000) already in use**

**Solution 1**: Use the stop script
```cmd
Double-click: STOP_STOCKBREAK_PRO.bat
```

**Solution 2**: Kill manually
```cmd
REM Kill frontend (port 3000)
netstat -ano | findstr :3000
taskkill /F /PID <number>

REM Kill backend (port 8001)
netstat -ano | findstr :8001
taskkill /F /PID <number>
```

---

### Frontend Fails to Install (ajv error)

This is what you experienced. The script handles it automatically by:
1. Using `--legacy-peer-deps` flag
2. If that fails, cleans cache and retries

If still failing, the window will show the error.

---

### Backend Window Closes Immediately

**Possible reasons**:
- Python not installed
- Virtual environment creation failed
- Dependencies installation failed

**Solution**: 
- Check the error message in the window
- Manually run backend commands to see full error
- Ensure Python and pip are working

---

### Frontend Window Closes Immediately

**Possible reasons**:
- Node.js not installed
- npm not working
- Dependency conflicts

**Solution**:
- Check error in the window
- Try manual installation
- Clear cache: `npm cache clean --force`

---

## 📝 First Run vs Subsequent Runs

### First Run (Longer):
```
Prerequisites Check:    5 seconds
MongoDB Start:         2 seconds
Backend Setup:         30-60 seconds (creates venv, installs deps)
Frontend Setup:        2-3 minutes (installs node_modules)
Total:                 ~4-5 minutes
```

### Subsequent Runs (Fast):
```
Prerequisites Check:    5 seconds
MongoDB Start:         2 seconds
Backend Start:         5 seconds (venv already exists)
Frontend Start:        10-15 seconds (node_modules exists)
Total:                 ~20-25 seconds
```

---

## ✅ Success Indicators

You'll know everything is working when:

✅ **Launcher window shows**:
```
[SUCCESS] StockBreak Pro is now running!
```

✅ **Backend window shows**:
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete
```

✅ **Frontend window shows**:
```
Compiled successfully!
webpack compiled successfully
```

✅ **Browser opens** to http://localhost:3000

✅ **Dashboard loads** with beautiful purple UI

✅ **Stock data appears** in cards

---

## 🎊 Daily Usage

### To Start Working:
1. Double-click `RUN_STOCKBREAK_PRO.bat`
2. Wait 20-30 seconds
3. Use the app in browser

### When Done:
1. Double-click `STOP_STOCKBREAK_PRO.bat`
2. Or just close the Backend and Frontend windows

---

## 💡 Pro Tips

1. **Create Desktop Shortcuts**:
   - Right-click `RUN_STOCKBREAK_PRO.bat`
   - Send to → Desktop (create shortcut)
   - Rename to "Start StockBreak Pro"

2. **Pin to Taskbar**:
   - Right-click the batch file
   - Pin to taskbar (if available)

3. **Keep Windows Open**:
   - Don't close Backend/Frontend windows while using
   - Minimize them instead

4. **Use Stop Script**:
   - Always use `STOP_STOCKBREAK_PRO.bat` for clean shutdown
   - Prevents orphan processes

5. **Check Logs**:
   - Backend window shows all backend logs
   - Frontend window shows compilation logs
   - Keep them visible for troubleshooting

---

## 🔄 Updating Dependencies

If you update code and need to reinstall dependencies:

### Backend:
```cmd
cd backend
rmdir /s /q venv
REM Then run RUN_STOCKBREAK_PRO.bat
```

### Frontend:
```cmd
cd frontend
rmdir /s /q node_modules
del package-lock.json
REM Then run RUN_STOCKBREAK_PRO.bat
```

The script will automatically reinstall everything.

---

## 📞 Quick Reference

| Action | File | Description |
|--------|------|-------------|
| Start | `RUN_STOCKBREAK_PRO.bat` | Starts backend + frontend |
| Stop | `STOP_STOCKBREAK_PRO.bat` | Stops all services |
| Main App | http://localhost:3000 | Web interface |
| Backend | http://localhost:8001 | API server |
| API Docs | http://localhost:8001/docs | Interactive API docs |

---

## 🎉 That's It!

**To use daily**:
1. Double-click `RUN_STOCKBREAK_PRO.bat`
2. Wait for browser to open
3. Start analyzing stocks!

**To stop**:
1. Double-click `STOP_STOCKBREAK_PRO.bat`
2. Done!

---

**Simple, fast, and reliable!** 🚀
