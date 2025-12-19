# 🔧 Complete Fix Guide - Backend MONGO_URL Error

## 🎯 The Problem

Your backend is crashing with:
```
KeyError: 'MONGO_URL'
```

This means the backend `.env` file is missing.

---

## ✅ Solution - 3 Methods

### Method 1: Use the Fix Script (EASIEST!)

1. Copy `FIX_BACKEND_ERROR.bat` to your project folder:
   ```
   C:\Users\srees\Downloads\StockBreakOutScanner-feature-stockbreakoutscanner-start-stop-automation (1)\StockBreakOutScanner-feature-stockbreakoutscanner-start-stop-automation\
   ```

2. **Double-click** `FIX_BACKEND_ERROR.bat`

3. It will:
   - Create the missing .env file
   - Install missing packages
   - Start MongoDB
   - Start the backend

4. Done! ✅

---

### Method 2: Manual Command Line Fix

Open **Command Prompt** and run:

```cmd
cd "C:\Users\srees\Downloads\StockBreakOutScanner-feature-stockbreakoutscanner-start-stop-automation (1)\StockBreakOutScanner-feature-stockbreakoutscanner-start-stop-automation\backend"

REM Create .env file
echo MONGO_URL=mongodb://localhost:27017 > .env
echo DB_NAME=stockbreak_db >> .env
echo CORS_ORIGINS=* >> .env

REM Activate virtual environment
venv\Scripts\activate

REM Install missing packages
pip install python-dotenv charset-normalizer

REM Start MongoDB
net start MongoDB

REM Start backend
uvicorn server:app --host 0.0.0.0 --port 8001
```

---

### Method 3: Create .env File Manually

1. Open **Notepad**

2. Copy and paste this:
   ```
   MONGO_URL=mongodb://localhost:27017
   DB_NAME=stockbreak_db
   CORS_ORIGINS=*
   ```

3. Click **File → Save As**

4. Navigate to:
   ```
   C:\Users\srees\Downloads\StockBreakOutScanner-feature-stockbreakoutscanner-start-stop-automation (1)\StockBreakOutScanner-feature-stockbreakoutscanner-start-stop-automation\backend
   ```

5. File name: `.env` (with the dot!)

6. Save as type: **All Files**

7. Click **Save**

8. Then run backend again

---

## 🔧 Install Missing Packages

The error also shows missing `charset-normalizer`. Fix this:

```cmd
cd backend
venv\Scripts\activate
pip install charset-normalizer python-dotenv requests
```

---

## 📋 Complete Start Process (After Fix)

### Terminal 1 - Start MongoDB:
```cmd
net start MongoDB
```

### Terminal 2 - Start Backend:
```cmd
cd "C:\Users\srees\Downloads\StockBreakOutScanner-feature-stockbreakoutscanner-start-stop-automation (1)\StockBreakOutScanner-feature-stockbreakoutscanner-start-stop-automation\backend"

venv\Scripts\activate
uvicorn server:app --host 0.0.0.0 --port 8001
```

### Terminal 3 - Start Frontend:
```cmd
cd "C:\Users\srees\Downloads\StockBreakOutScanner-feature-stockbreakoutscanner-start-stop-automation (1)\StockBreakOutScanner-feature-stockbreakoutscanner-start-stop-automation\frontend"

npm start
```

---

## ✅ Expected Backend Output

After fix, you should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

---

## 🔴 If MongoDB Error

If you see:
```
motor.motor_asyncio.AsyncIOMotorClient(...) connection error
```

### Install MongoDB:

1. Download: https://www.mongodb.com/try/download/community
2. Choose "Windows"
3. Install with default settings
4. ✅ Check "Install MongoDB as a Service"
5. After installation, run:
   ```cmd
   net start MongoDB
   ```

---

## 🎯 Quick Fix Summary

**The issue**: Missing `.env` file in backend folder

**The fix**:
1. Create backend/.env with MongoDB URL
2. Install missing packages
3. Start MongoDB service
4. Restart backend

**Files you need**:
- `FIX_BACKEND_ERROR.bat` - Automatic fix
- `SETUP_ENV_FILES.bat` - Setup both backend and frontend .env

---

## 📱 After Backend Starts

Once backend shows:
```
INFO: Uvicorn running on http://0.0.0.0:8001
```

Test it:
1. Open browser
2. Go to: http://localhost:8001/api/
3. Should see: `{"message":"Indian Stock Breakout Screener API - Enhanced Version"}`

Then start the frontend!

---

## 🚀 Updated Launch Batch File

I'll also update your `RUN_STOCKBREAK_PRO.bat` to automatically create .env files if missing.

---

## ✅ Success Checklist

- [ ] Created backend/.env file
- [ ] Installed python-dotenv
- [ ] Installed charset-normalizer
- [ ] Started MongoDB service
- [ ] Backend starts without errors
- [ ] Can access http://localhost:8001/api/
- [ ] Frontend can connect to backend
- [ ] 🎉 App working!

---

**Try Method 1 (FIX_BACKEND_ERROR.bat) first - it's the easiest!** 🚀
