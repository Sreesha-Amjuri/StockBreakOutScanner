# 🔧 Troubleshooting Frontend "Can't Reach" Issue

## 🎯 Quick Checks

### Step 1: Check the Frontend Window

Look at the **red/pink Frontend window** that opened. What does it show?

#### ✅ If it shows this (GOOD):
```
Compiled successfully!
webpack compiled successfully

You can now view frontend in the browser.

Local:            http://localhost:3000
```
**Then frontend is running!** Try refreshing browser.

---

#### ❌ If it shows errors (BAD):

Common errors you might see:
1. `Cannot find module 'ajv/dist/compile/codegen'`
2. `ERESOLVE unable to resolve dependency tree`
3. `Port 3000 is already in use`
4. Window closes immediately

**If you see errors, continue reading below.**

---

## 🔧 Solution 1: Fix Dependency Issues

The most common issue is the `ajv` module error.

### Open Command Prompt and run:

```cmd
cd C:\Users\srees\Downloads\StockBreakOutScanner-feature-windows-installer-emergentAI\StockBreakOutScanner-feature-windows-installer-emergentAI\frontend

REM Clean everything
rmdir /s /q node_modules
del package-lock.json
npm cache clean --force

REM Install specific versions that work
npm install ajv@8.12.0 --legacy-peer-deps
npm install ajv-keywords@5.1.0 --legacy-peer-deps

REM Install all dependencies
npm install --legacy-peer-deps

REM Start frontend
npm start
```

**Wait 2-3 minutes** for installation to complete.

---

## 🔧 Solution 2: Check if Port 3000 is Free

### Check if something is using port 3000:

```cmd
netstat -ano | findstr :3000
```

**If you see output**, something is using port 3000.

### Kill the process:
```cmd
REM Find the PID number from above command
taskkill /F /PID <PID_NUMBER>

REM Example: taskkill /F /PID 12345
```

Then try starting again.

---

## 🔧 Solution 3: Use Yarn Instead of npm

Sometimes Yarn handles dependencies better:

```cmd
cd C:\Users\srees\Downloads\StockBreakOutScanner-feature-windows-installer-emergentAI\StockBreakOutScanner-feature-windows-installer-emergentAI\frontend

REM Install Yarn globally (if not already installed)
npm install -g yarn

REM Clean and install with Yarn
rmdir /s /q node_modules
del yarn.lock
yarn install

REM Start with Yarn
yarn start
```

---

## 🔧 Solution 4: Downgrade Node.js Version

You're using Node.js v24.3.0 which is very new and might have compatibility issues.

### Check your Node version:
```cmd
node --version
```

### If it's v24.x, downgrade to v20 LTS:

1. Download Node.js v20 LTS: https://nodejs.org/dist/v20.11.0/node-v20.11.0-x64.msi
2. Install it (will replace v24)
3. Restart Command Prompt
4. Verify: `node --version` (should show v20.x.x)
5. Try running the app again

**Node.js v20 is the stable LTS version** and works best with React.

---

## 🔧 Solution 5: Manual Step-by-Step Start

Let's start everything manually to see exact errors:

### Terminal 1 - Backend:
```cmd
cd C:\Users\srees\Downloads\StockBreakOutScanner-feature-windows-installer-emergentAI\StockBreakOutScanner-feature-windows-installer-emergentAI\backend

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8001
```

**Wait until you see**: `INFO: Uvicorn running on http://0.0.0.0:8001`

### Terminal 2 - Frontend:
```cmd
cd C:\Users\srees\Downloads\StockBreakOutScanner-feature-windows-installer-emergentAI\StockBreakOutScanner-feature-windows-installer-emergentAI\frontend

REM Use one of these:
npm start
# OR
yarn start
```

**Copy and send me any errors you see!**

---

## 🔧 Solution 6: Check Windows Firewall

Windows Firewall might be blocking port 3000.

### Temporarily disable firewall to test:
1. Search "Windows Defender Firewall"
2. Click "Turn Windows Defender Firewall on or off"
3. Turn off for Private network (temporarily)
4. Try accessing http://localhost:3000
5. **Remember to turn it back on!**

### Or add firewall rule:
```cmd
REM Run as Administrator
netsh advfirewall firewall add rule name="StockBreak Pro Frontend" dir=in action=allow protocol=TCP localport=3000

netsh advfirewall firewall add rule name="StockBreak Pro Backend" dir=in action=allow protocol=TCP localport=8001
```

---

## 📊 What to Tell Me

Please check the Frontend window and tell me:

1. **What does the frontend window show?**
   - Exact error message
   - Or "Compiled successfully"

2. **Does the backend window show this?**
   ```
   INFO: Uvicorn running on http://0.0.0.0:8001
   ```

3. **Run this command and tell me output:**
   ```cmd
   netstat -ano | findstr :3000
   netstat -ano | findstr :8001
   ```

4. **What's your Node.js version?**
   ```cmd
   node --version
   ```

With this information, I can give you exact fix!

---

## 🎯 Most Likely Fix (Try This First)

Based on your earlier error with `ajv`, this is most likely the issue:

```cmd
cd C:\Users\srees\Downloads\StockBreakOutScanner-feature-windows-installer-emergentAI\StockBreakOutScanner-feature-windows-installer-emergentAI\frontend

rmdir /s /q node_modules
del package-lock.json
npm cache clean --force

npm install ajv@8.12.0 --save --legacy-peer-deps
npm install --legacy-peer-deps

npm start
```

This should work! Let me know if it doesn't.

---

## 🔄 Alternative: Use the Web App from My Server

If nothing works locally, you can use the deployed version:
```
https://breakout-dash.preview.emergentagent.com
```

This is already running and working!

---

## 📞 Need More Help?

Send me:
1. Screenshot of Frontend window
2. Screenshot of Backend window  
3. Any error messages you see
4. Output of: `node --version`

I'll provide exact solution!
