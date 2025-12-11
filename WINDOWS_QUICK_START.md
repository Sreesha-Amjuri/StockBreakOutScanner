# ⚡ Windows Quick Start - 2 Minutes!

## 🎯 Super Fast Method

### Prerequisites (One-time setup):

1. **Install Python**: https://www.python.org/downloads/
   - ✅ Check "Add Python to PATH"

2. **Install Node.js**: https://nodejs.org/
   - Choose "LTS" version

3. **Install MongoDB**: https://www.mongodb.com/try/download/community
   - Choose "Windows" version

---

## 🚀 Start the Application

### Method 1: Double-Click (Easiest!)

1. Navigate to your project folder (e.g., `C:\StockBreakPro\`)
2. **Double-click** `START_WINDOWS.bat`
3. Wait 15-20 seconds
4. Browser opens automatically at http://localhost:3000
5. **Done!** 🎉

---

### Method 2: Command Line (Alternative)

Open **Command Prompt** in project folder:

```cmd
START_WINDOWS.bat
```

---

## 🛑 Stop the Application

### Method 1: Close Windows
- Close the "Backend" window
- Close the "Frontend" window

### Method 2: Use Stop Script
- **Double-click** `STOP_WINDOWS.bat`

---

## 🌐 Access URLs

Once running:

```
Main App:    http://localhost:3000
API Server:  http://localhost:8001
API Docs:    http://localhost:8001/docs
```

---

## 📱 Access from Phone/Tablet

1. On your computer, find IP address:
   ```cmd
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

2. On phone/tablet (same WiFi network):
   ```
   http://192.168.1.100:3000
   ```

---

## ⚡ What Each File Does

| File | Purpose |
|------|---------|
| `START_WINDOWS.bat` | Starts everything (Backend + Frontend) |
| `STOP_WINDOWS.bat` | Stops all services |
| `start_stockbreak.cmd` | Alternative launcher |

---

## 🐛 Quick Troubleshooting

### Port Already in Use

**Kill processes**:
```cmd
# Kill frontend (port 3000)
netstat -ano | findstr :3000
taskkill /PID <number> /F

# Kill backend (port 8001)
netstat -ano | findstr :8001
taskkill /PID <number> /F
```

### Dependencies Not Installed

**Backend**:
```cmd
cd backend
pip install -r requirements.txt
```

**Frontend**:
```cmd
cd frontend
npm install
```

### MongoDB Not Running

```cmd
net start MongoDB
```

Or manually:
```cmd
mongod
```

---

## ✅ Success Indicators

You'll know it's working when:

✅ Two new windows open (Backend and Frontend)  
✅ Backend window shows: "Uvicorn running on http://0.0.0.0:8001"  
✅ Frontend window shows: "Compiled successfully!"  
✅ Browser opens to http://localhost:3000  
✅ Dashboard loads with purple UI  
✅ Stock data appears  

---

## 🎊 That's It!

**To use daily**:
1. Double-click `START_WINDOWS.bat`
2. Wait 20 seconds
3. Start analyzing stocks!

**To stop**:
- Close the windows
- Or double-click `STOP_WINDOWS.bat`

---

## 📚 Need More Help?

Read the detailed guide: `WINDOWS_SETUP_GUIDE.md`

---

**Total Setup Time**: 2 minutes after prerequisites installed! ⚡
