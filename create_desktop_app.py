#!/usr/bin/env python3
"""
StockBreak Pro - Desktop Application Creator
Creates a standalone desktop application using Electron wrapper
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def create_electron_app():
    """Create Electron desktop application wrapper"""
    
    print("🚀 Creating StockBreak Pro Desktop Application...")
    print("=" * 50)
    
    # Create electron app directory
    electron_dir = Path("./stockbreak_desktop")
    electron_dir.mkdir(exist_ok=True)
    
    # Create package.json for Electron app
    package_json = {
        "name": "stockbreak-pro",
        "version": "2.0.0",
        "description": "StockBreak Pro - Professional Stock Analysis Platform",
        "main": "main.js",
        "scripts": {
            "start": "electron .",
            "build": "electron-builder",
            "dist": "electron-builder --publish=never"
        },
        "author": "StockBreak Pro Team",
        "license": "MIT",
        "devDependencies": {
            "electron": "^25.0.0",
            "electron-builder": "^24.0.0"
        },
        "build": {
            "appId": "com.stockbreakpro.app",
            "productName": "StockBreak Pro",
            "directories": {
                "output": "dist"
            },
            "files": [
                "**/*",
                "!node_modules/**/*"
            ],
            "win": {
                "target": "nsis",
                "icon": "assets/icon.ico"
            },
            "nsis": {
                "oneClick": False,
                "allowToChangeInstallationDirectory": True,
                "createDesktopShortcut": True,
                "createStartMenuShortcut": True
            }
        }
    }
    
    # Write package.json
    with open(electron_dir / "package.json", "w") as f:
        json.dump(package_json, f, indent=2)
    
    # Create main Electron process file
    main_js = '''
const { app, BrowserWindow, Menu, shell, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let backendProcess;
let frontendProcess;

// Start backend services
function startBackendServices() {
    console.log('Starting StockBreak Pro services...');
    
    // Start Python backend
    backendProcess = spawn('python', ['backend/server.py'], {
        cwd: path.join(__dirname, '..'),
        stdio: 'pipe'
    });
    
    backendProcess.stdout.on('data', (data) => {
        console.log(`Backend: ${data}`);
    });
    
    // Start frontend (if needed - or just serve static files)
    setTimeout(() => {
        frontendProcess = spawn('npm', ['start'], {
            cwd: path.join(__dirname, '..', 'frontend'),
            stdio: 'pipe'
        });
        
        frontendProcess.stdout.on('data', (data) => {
            console.log(`Frontend: ${data}`);
        });
    }, 3000);
}

// Stop backend services
function stopBackendServices() {
    if (backendProcess) {
        backendProcess.kill();
    }
    if (frontendProcess) {
        frontendProcess.kill();
    }
}

function createWindow() {
    // Create the browser window
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 900,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            enableRemoteModule: false
        },
        icon: path.join(__dirname, 'assets', 'icon.png'),
        title: 'StockBreak Pro - Professional Stock Analysis',
        show: false
    });

    // Load the app
    mainWindow.loadURL('http://localhost:3000');

    // Show window when ready
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
        
        // Show welcome message
        setTimeout(() => {
            dialog.showInfoBox(mainWindow, {
                type: 'info',
                title: 'Welcome to StockBreak Pro',
                message: 'Professional Stock Analysis Platform',
                detail: 'Features:\\n✓ Full NSE Coverage (594+ stocks)\\n✓ 13+ Technical Indicators\\n✓ Real-time Market Data\\n✓ Professional Watchlist\\n✓ Trading Recommendations\\n\\nHappy Trading! 📈'
            });
        }, 2000);
    });

    // Handle window closed
    mainWindow.on('closed', function () {
        mainWindow = null;
        stopBackendServices();
    });
}

// Create application menu
function createMenu() {
    const template = [
        {
            label: 'File',
            submenu: [
                {
                    label: 'Refresh Scan',
                    accelerator: 'CmdOrCtrl+R',
                    click: () => {
                        mainWindow.webContents.executeJavaScript('location.reload()');
                    }
                },
                {
                    label: 'Export Data',
                    accelerator: 'CmdOrCtrl+E',
                    click: () => {
                        // Trigger export functionality
                        mainWindow.webContents.executeJavaScript('window.exportToExcel && window.exportToExcel()');
                    }
                },
                { type: 'separator' },
                {
                    label: 'Exit',
                    accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
                    click: () => {
                        app.quit();
                    }
                }
            ]
        },
        {
            label: 'View',
            submenu: [
                {
                    label: 'Toggle Dark Mode',
                    accelerator: 'CmdOrCtrl+D',
                    click: () => {
                        mainWindow.webContents.executeJavaScript('window.toggleDarkMode && window.toggleDarkMode()');
                    }
                },
                { role: 'reload' },
                { role: 'forceReload' },
                { role: 'toggleDevTools' },
                { type: 'separator' },
                { role: 'resetZoom' },
                { role: 'zoomIn' },
                { role: 'zoomOut' },
                { type: 'separator' },
                { role: 'togglefullscreen' }
            ]
        },
        {
            label: 'Help',
            submenu: [
                {
                    label: 'About StockBreak Pro',
                    click: () => {
                        dialog.showMessageBox(mainWindow, {
                            type: 'info',
                            title: 'About StockBreak Pro',
                            message: 'StockBreak Pro v2.0.0',
                            detail: 'Professional Stock Analysis Platform\\n\\nFeatures:\\n• Full NSE Coverage (594+ stocks)\\n• 13+ Technical Indicators\\n• Real-time Market Data\\n• Professional Watchlist Management\\n• Advanced Breakout Detection\\n• Trading Recommendations\\n• Export & Reporting Tools\\n\\nEducational Use Only - Not Financial Advice'
                        });
                    }
                },
                {
                    label: 'Documentation',
                    click: () => {
                        shell.openExternal('https://github.com/stockbreak-pro/docs');
                    }
                }
            ]
        }
    ];

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
}

// App event handlers
app.whenReady().then(() => {
    startBackendServices();
    
    setTimeout(() => {
        createWindow();
        createMenu();
    }, 5000); // Wait for services to start

    app.on('activate', function () {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', function () {
    stopBackendServices();
    if (process.platform !== 'darwin') app.quit();
});

app.on('before-quit', () => {
    stopBackendServices();
});
'''
    
    # Write main.js
    with open(electron_dir / "main.js", "w") as f:
        f.write(main_js)
    
    # Create assets directory and placeholder icon
    assets_dir = electron_dir / "assets"
    assets_dir.mkdir(exist_ok=True)
    
    # Create installer script for Electron
    installer_script = """
# StockBreak Pro Desktop Installer

## Installation Steps

1. **Install Node.js** (if not already installed):
   - Download from: https://nodejs.org/
   - Install LTS version

2. **Install Electron dependencies**:
   ```bash
   cd stockbreak_desktop
   npm install
   ```

3. **Build desktop application**:
   ```bash
   npm run build
   ```

4. **Run desktop app**:
   ```bash
   npm start
   ```

## Creating Distributable Package

```bash
npm run dist
```

This creates installer files in the `dist/` directory.

## Features

- Native desktop application
- System tray integration
- Auto-updater support
- Cross-platform compatibility
- Professional UI with native menus

## System Requirements

- Windows 10/11, macOS 10.15+, or Linux
- Node.js 16+
- 4GB RAM minimum
- 2GB disk space
"""
    
    with open(electron_dir / "INSTALLER_README.md", "w") as f:
        f.write(installer_script)
    
    print(f"✅ Electron app created in: {electron_dir}")
    print("\n📋 Next steps:")
    print("1. cd stockbreak_desktop")
    print("2. npm install") 
    print("3. npm start (to run)")
    print("4. npm run dist (to build installer)")

if __name__ == "__main__":
    create_electron_app()
    print("\n🎉 StockBreak Pro Desktop Application Ready!")