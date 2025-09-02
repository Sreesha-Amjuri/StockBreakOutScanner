# 🚀 StockBreak Pro - Windows Installation Guide

## Professional Stock Analysis Platform for Windows 11

### 📋 **Quick Start (Recommended)**

1. **Download the installer package**
2. **Right-click** `StockBreakPro_Setup.bat` → **"Run as administrator"**
3. **Follow the installation wizard** (automated process)
4. **Launch from desktop shortcut** or Start Menu

---

### 📦 **What Gets Installed**

#### **Core Dependencies (Automated)**
- ✅ **Python 3.11** - Backend API server
- ✅ **Node.js 18** - Frontend React application  
- ✅ **MongoDB 7.0** - Database for watchlists and data storage
- ✅ **StockBreak Pro** - Complete application suite

#### **Application Components**
- ✅ **Backend API Server** (Port 8001)
- ✅ **Frontend Web Interface** (Port 3000)
- ✅ **Database Services** (Port 27017)
- ✅ **Desktop & Start Menu Shortcuts**

---

### 🎯 **System Requirements**

| Component | Requirement |
|-----------|-------------|
| **Operating System** | Windows 10/11 (64-bit) |
| **RAM** | 4GB minimum, 8GB recommended |
| **Storage** | 2GB free space |
| **Internet** | Required for real-time stock data |
| **Admin Rights** | Required for installation only |

---

### 🏃‍♂️ **Running StockBreak Pro**

#### **Method 1: Desktop Shortcut**
- Double-click **"StockBreak Pro"** icon on desktop

#### **Method 2: Start Menu**  
- Start Menu → **"StockBreak Pro"** → **"StockBreak Pro"**

#### **Method 3: Manual Launch**
- Navigate to `C:\StockBreakPro\`
- Double-click `StockBreakPro.exe`

#### **Method 4: Direct URL**
- Open browser → `http://localhost:3000`

---

### 🔧 **Advanced Configuration**

#### **Port Configuration (If Needed)**
```bash
# Backend API (if port 8001 is busy)
C:\StockBreakPro\backend\server.py - line 15: port = 8001

# Frontend (if port 3000 is busy)  
C:\StockBreakPro\frontend\package.json - "start": "PORT=3001 react-scripts start"
```

#### **MongoDB Database Location**
- **Data Directory**: `C:\data\db\`
- **Log Files**: `C:\data\db\mongodb.log`
- **Configuration**: Default settings (port 27017)

---

### 🛠️ **Troubleshooting**

#### **Common Issues & Solutions**

| Issue | Solution |
|-------|----------|
| **Port already in use** | Restart computer or change ports |
| **MongoDB won't start** | Check `C:\data\db\` exists and has permissions |
| **Python errors** | Reinstall Python 3.11 with "Add to PATH" |
| **React won't build** | Delete `node_modules`, run `npm install` |
| **Can't access localhost:3000** | Check Windows Firewall settings |

#### **Manual Service Restart**
```batch
# Stop all services
taskkill /F /IM python.exe
taskkill /F /IM node.exe  
taskkill /F /IM mongod.exe

# Start manually
C:\StockBreakPro\StockBreakPro.exe
```

---

### 🗑️ **Uninstallation**

1. **Run** `C:\StockBreakPro\Uninstall_StockBreakPro.bat`
2. **Confirm** removal when prompted
3. **Done!** - All files and shortcuts removed

**Note**: Python, Node.js, and MongoDB remain installed as they may be used by other applications.

---

### 📱 **Features Overview**

#### **Professional Trading Tools**
- 🎯 **Full NSE Coverage** - 594+ stocks across 39 sectors
- 📊 **13+ Technical Indicators** - RSI, MACD, Bollinger Bands, etc.
- 💼 **Professional Watchlist** - Real-time tracking like Zerodha/Upstox
- 🔍 **Advanced Breakout Detection** - Multiple timeframes & patterns
- 💰 **Trading Recommendations** - Entry, Stop Loss, Targets
- 📈 **Multi-column Sorting** - Shift+click for advanced sorting

#### **Export & Automation**  
- 📊 **Excel Export** - Complete analysis data
- 📄 **PDF Reports** - Professional market reports
- ⏰ **Auto-scanning** - Scheduled market monitoring
- 🚨 **Price Alerts** - Custom price level notifications
- ⌨️ **Keyboard Shortcuts** - Power user efficiency

---

### 🆘 **Support**

#### **Quick Help**
- **Keyboard Shortcuts**: `Ctrl+R` (Refresh), `Ctrl+E` (Export), `Ctrl+D` (Dark Mode)
- **Application Logs**: Check console output in the command window
- **Data Issues**: Try refreshing the scan or check internet connection

#### **Performance Tips**
- 💡 **Close unused browser tabs** for better performance
- 💡 **Use Chrome/Edge** for best compatibility  
- 💡 **Ensure stable internet** for real-time data
- 💡 **Run as administrator** if permission issues occur

---

### ⚖️ **Legal Disclaimer**

StockBreak Pro is for **educational and research purposes only**. 

- ❌ **Not financial advice** - Always consult qualified financial advisors
- ❌ **No guarantees** - Past performance doesn't predict future results  
- ❌ **Use at your risk** - Trading involves substantial risk of loss
- ✅ **Educational tool** - Learn technical analysis and market patterns

---

### 🌟 **Thank You!**

Welcome to **StockBreak Pro** - Your professional stock analysis platform!

**Happy Trading! 📈**