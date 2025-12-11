# 🔧 Fix Dependency Error - Quick Solution

## 🎯 The Problem

You're getting this error:
```
react-day-picker@8.10.1 requires react@"^16.8.0 || ^17.0.0 || ^18.0.0"
but you have react@19.2.1
```

## ✅ Quick Fix (Choose One Method)

### Method 1: Use Legacy Peer Deps (FASTEST - Recommended)

Run this command instead:

```cmd
npm install --legacy-peer-deps
```

This tells npm to ignore the peer dependency conflict. It will work fine!

---

### Method 2: Use Force (Alternative)

```cmd
npm install --force
```

This forces npm to install despite the conflict.

---

### Method 3: Downgrade React (If above don't work)

```cmd
npm install react@18.2.0 react-dom@18.2.0
npm install
```

This downgrades React to version 18 which is compatible.

---

## 🚀 After Installing

Once npm install succeeds, start the frontend:

```cmd
npm start
```

## 📋 Complete Windows Start Guide

Here's the full process:

### Terminal 1 - Start Backend:
```cmd
cd C:\Users\srees\Downloads\StockBreakOutScanner-feature-windows-installer-emergentAI\StockBreakOutScanner-feature-windows-installer-emergentAI\backend

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8001
```

### Terminal 2 - Start Frontend:
```cmd
cd C:\Users\srees\Downloads\StockBreakOutScanner-feature-windows-installer-emergentAI\StockBreakOutScanner-feature-windows-installer-emergentAI\frontend

npm install --legacy-peer-deps
npm start
```

### Terminal 3 - Start MongoDB (if needed):
```cmd
net start MongoDB
```

---

## 🌐 Access the App

Once both terminals show success:
- Open browser: http://localhost:3000
- Backend API: http://localhost:8001

---

## ✅ Expected Output

**Frontend should show**:
```
Compiled successfully!
webpack compiled with 0 errors
```

**Backend should show**:
```
INFO:     Uvicorn running on http://0.0.0.0:8001
```

---

## 🎊 Done!

Your StockBreak Pro web app will be running in your browser!
