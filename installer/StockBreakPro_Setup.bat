@echo off
title StockBreak Pro - Professional Stock Analysis Platform
color 0A

echo.
echo ========================================
echo    StockBreak Pro - Setup Wizard
echo    Professional Stock Analysis Platform
echo ========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [✓] Running with Administrator privileges
) else (
    echo [!] Please run as Administrator
    echo Right-click this file and select "Run as administrator"
    pause
    exit /b 1
)

echo.
echo [1/7] Checking system requirements...
timeout /t 2 >nul

REM Check Windows version
ver | find "10" >nul
if %errorLevel% == 0 (
    echo [✓] Windows 10/11 detected
) else (
    echo [!] Windows 10 or later required
    pause
    exit /b 1
)

echo.
echo [2/7] Setting up installation directory...
set "INSTALL_DIR=C:\StockBreakPro"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
echo [✓] Installation directory: %INSTALL_DIR%

echo.
echo [3/7] Downloading and installing Python 3.11...
if not exist "C:\Python311\python.exe" (
    echo Downloading Python installer...
    powershell -Command "& {(New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe', '%INSTALL_DIR%\python-installer.exe')}"
    
    echo Installing Python (this may take a few minutes)...
    "%INSTALL_DIR%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    timeout /t 30 >nul
    
    del "%INSTALL_DIR%\python-installer.exe"
    echo [✓] Python 3.11 installed
) else (
    echo [✓] Python already installed
)

echo.
echo [4/7] Downloading and installing Node.js...
if not exist "C:\Program Files\nodejs\node.exe" (
    echo Downloading Node.js installer...
    powershell -Command "& {(New-Object System.Net.WebClient).DownloadFile('https://nodejs.org/dist/v18.17.1/node-v18.17.1-x64.msi', '%INSTALL_DIR%\nodejs-installer.msi')}"
    
    echo Installing Node.js...
    msiexec /i "%INSTALL_DIR%\nodejs-installer.msi" /quiet /norestart
    timeout /t 30 >nul
    
    del "%INSTALL_DIR%\nodejs-installer.msi"
    echo [✓] Node.js installed
) else (
    echo [✓] Node.js already installed
)

echo.
echo [5/7] Downloading and installing MongoDB Community Server...
if not exist "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" (
    echo Downloading MongoDB installer...
    powershell -Command "& {(New-Object System.Net.WebClient).DownloadFile('https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.2-signed.msi', '%INSTALL_DIR%\mongodb-installer.msi')}"
    
    echo Installing MongoDB...
    msiexec /i "%INSTALL_DIR%\mongodb-installer.msi" /quiet /norestart INSTALLLOCATION="C:\Program Files\MongoDB\Server\7.0\" ADDLOCAL="ServerService,Client,MongoImportExportTools,MiscellaneousTools"
    timeout /t 60 >nul
    
    del "%INSTALL_DIR%\mongodb-installer.msi"
    echo [✓] MongoDB installed
) else (
    echo [✓] MongoDB already installed
)

echo.
echo [6/7] Copying StockBreak Pro application files...
xcopy /E /I /Y "%~dp0app\*" "%INSTALL_DIR%\"
echo [✓] Application files copied

echo.
echo [7/7] Setting up Windows services and shortcuts...

REM Create MongoDB data directory
if not exist "C:\data\db" mkdir "C:\data\db"

REM Install Python dependencies
echo Installing Python dependencies...
cd /d "%INSTALL_DIR%\backend"
C:\Python311\python.exe -m pip install -r requirements.txt
echo [✓] Backend dependencies installed

REM Install Node.js dependencies
echo Installing Node.js dependencies...
cd /d "%INSTALL_DIR%\frontend"
call npm install
echo [✓] Frontend dependencies installed

REM Build React application
echo Building React application...
call npm run build
echo [✓] React app built

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\StockBreak Pro.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\StockBreakPro.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.IconLocation = '%INSTALL_DIR%\icon.ico'; $Shortcut.Description = 'StockBreak Pro - Professional Stock Analysis'; $Shortcut.Save()}"

REM Create start menu shortcut
if not exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\StockBreak Pro" mkdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\StockBreak Pro"
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\StockBreak Pro\StockBreak Pro.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\StockBreakPro.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.IconLocation = '%INSTALL_DIR%\icon.ico'; $Shortcut.Description = 'StockBreak Pro - Professional Stock Analysis'; $Shortcut.Save()}"

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo [✓] StockBreak Pro has been successfully installed
echo [✓] Desktop shortcut created
echo [✓] Start menu shortcut created
echo.
echo You can now launch StockBreak Pro from:
echo - Desktop shortcut
echo - Start Menu ^> StockBreak Pro
echo - Or run: %INSTALL_DIR%\StockBreakPro.exe
echo.
echo Press any key to launch StockBreak Pro now...
pause >nul

REM Launch the application
"%INSTALL_DIR%\StockBreakPro.exe"