# 🚀 Simple Start Guide - Zero Manual Steps!

## ✅ What You Need

Just copy **ONE FILE** to your project folder:

```
START_STOCKBREAK_FINAL.bat
```

Copy it to:
```
C:\Users\srees\Downloads\StockBreakOutScanner-feature-stockbreakoutscanner-start-stop-automation\StockBreakOutScanner-feature-stockbreakoutscanner-start-stop-automation\
```

---

## 🎯 How to Use

1. **Double-click**: `START_STOCKBREAK_FINAL.bat`

2. **Wait** (2-3 minutes on first run)

3. **Browser opens** automatically to http://localhost:3000

4. **Done!** 🎉

---

## ✨ What It Does Automatically

The script will:

✅ Check Python and Node.js installed  
✅ Create backend `.env` file  
✅ Create frontend `.env` file  
✅ Start MongoDB service  
✅ Open Backend window (port 8001)  
✅ Open Frontend window (port 3000)  
✅ **Automatically fix ajv dependency issue**  
✅ Install compatible ajv@8.12.0  
✅ Install compatible ajv-keywords@5.1.0  
✅ Install all other dependencies  
✅ Set all environment variables  
✅ Open browser to http://localhost:3000  

**No manual commands needed!**

---

## 📊 What You'll See

### Main Launcher Window:
```
========================================================
      STOCKBREAK PRO - AUTOMATIC LAUNCHER
      (Fixes all dependency issues automatically)
========================================================

[CHECKING] Prerequisites...
[OK] Python found
[OK] Node.js found

[SETUP] Backend environment...
[OK] Backend .env created

[SETUP] Frontend environment...
[OK] Frontend .env created

[STARTING] MongoDB...
[OK] MongoDB started

[CREATING] Backend start script...
[STARTING] Backend in new window...
[OK] Backend window opened

[CREATING] Frontend start script with automatic fixes...
[STARTING] Frontend in new window...
[OK] Frontend window opened
```

### Backend Window (Green):
```
========================================
   STOCKBREAK PRO - BACKEND SERVER
========================================

[INFO] Environment:
  MONGO_URL=mongodb://localhost:27017
  DB_NAME=stockbreak_db

========================================
[STARTING] Backend Server...
URL: http://localhost:8001
API Docs: http://localhost:8001/docs
========================================

INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete.
```

### Frontend Window (Red):
```
========================================
   STOCKBREAK PRO - FRONTEND
   (Auto-fixing dependencies)
========================================

[INFO] Backend URL: http://localhost:8001

[INFO] Installing frontend dependencies...
[INFO] This will take 2-3 minutes...

[STEP 1/4] Cleaning cache...
[STEP 2/4] Installing ajv (fixing compatibility)...
[STEP 3/4] Installing ajv-keywords...
[STEP 4/4] Installing all dependencies...

[OK] Dependencies installed

========================================
[STARTING] Frontend...
URL: http://localhost:3000
========================================

Compiled successfully!
You can now view frontend in the browser.
Local: http://localhost:3000
```

---

## ⏱️ Timeline

**First Run** (installs everything):
- Backend starts: 10 seconds
- Frontend installs dependencies: 2-3 minutes
- Frontend compiles: 30 seconds
- **Total: ~3-4 minutes**

**Subsequent Runs** (everything installed):
- Backend starts: 5 seconds
- Frontend starts: 15-20 seconds
- **Total: ~25 seconds**

---

## 🌐 URLs

Once running:

| Service | URL | What You See |
|---------|-----|--------------|
| **Frontend** | http://localhost:3000 | Purple dashboard with stock cards |
| **Backend** | http://localhost:8001/api/ | JSON: `{"message":"Indian Stock..."}` |
| **API Docs** | http://localhost:8001/docs | Interactive API documentation |

---

## 🛑 To Stop

Just close the Backend and Frontend windows, or use:

```
STOP_STOCKBREAK_PRO.bat
```

---

## ✅ Success Checklist

After running the script:

- [ ] Two windows opened (Backend + Frontend)
- [ ] Backend shows "Uvicorn running"
- [ ] Frontend shows "Compiled successfully!"
- [ ] Browser opened to http://localhost:3000
- [ ] Dashboard visible with purple theme
- [ ] Stock cards showing data

---

## 🔧 If Something Goes Wrong

### Frontend window closes immediately:
- Look for error message before it closes
- Node.js v24 might be too new
- Consider downgrading to Node.js v20 LTS

### Backend fails:
- MongoDB might not be installed
- Install from: https://www.mongodb.com/try/download/community

### Browser shows "Not Found":
- Wait longer (frontend still compiling)
- Check Frontend window progress
- Refresh browser after seeing "Compiled successfully!"

---

## 💡 Pro Tips

1. **First run takes longer** - Dependencies need to install (2-3 mins)
2. **Subsequent runs are fast** - Everything already installed (~25 secs)
3. **Keep windows open** - Don't close Backend/Frontend windows
4. **Check Frontend window** - Shows compilation progress
5. **Wait for "Compiled successfully!"** - Then refresh browser

---

## 🎊 That's It!

**One file, one double-click, zero manual steps!**

Just run `START_STOCKBREAK_FINAL.bat` and everything works automatically! 🚀
