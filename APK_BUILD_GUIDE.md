# 📱 StockBreak Pro - Android APK Build Guide

## Step-by-Step Instructions to Get Your APK

### Step 1: Save to GitHub (Using Emergent Platform)

1. **In the Emergent chat interface**, look for the **"Save to GitHub"** button in the chat input area
2. Click on it and connect your GitHub account if not already connected
3. Create a new repository or select an existing one
4. Push the code to GitHub

### Step 2: Enable GitHub Actions

1. Go to your GitHub repository: `https://github.com/YOUR_USERNAME/YOUR_REPO`
2. Click on **"Actions"** tab at the top
3. If prompted, click **"I understand my workflows, go ahead and enable them"**
4. You should see the **"Build Android APK"** workflow

### Step 3: Trigger the Build

**Option A: Automatic (on push)**
- The build automatically starts when you push code to `main` or `master` branch

**Option B: Manual Trigger**
1. Go to **Actions** tab
2. Click on **"Build Android APK"** workflow on the left
3. Click **"Run workflow"** dropdown on the right
4. Select `main` branch and click **"Run workflow"**

### Step 4: Wait for Build (~5-10 minutes)

1. Click on the running workflow to see progress
2. You'll see steps like:
   - ✅ Checkout repository
   - ✅ Setup Node.js
   - ✅ Setup Java JDK
   - ✅ Setup Android SDK
   - ✅ Install dependencies
   - ✅ Build Android APK
   - ✅ Upload APK to Artifacts

### Step 5: Download Your APK

**Method 1: From Artifacts (Always Available)**
1. Go to **Actions** tab
2. Click on the completed workflow run
3. Scroll down to **"Artifacts"** section
4. Click **"StockBreakPro-APK"** to download the ZIP
5. Extract the ZIP to get `app-release.apk`

**Method 2: From Releases (If build was on main/master)**
1. Go to **Releases** section (right sidebar of repo)
2. Find the latest release
3. Download `StockBreakPro-v1.0.X.apk`

### Step 6: Install on Your Android Phone

1. **Transfer APK to phone** (email, Google Drive, USB, etc.)
2. **Enable Unknown Sources**:
   - Go to **Settings > Security** (or **Settings > Apps > Special Access**)
   - Enable **"Install unknown apps"** for your file manager/browser
3. **Tap the APK file** to install
4. **Open StockBreak Pro** and enjoy!

---

## 🔧 Troubleshooting

### Build Failed?
- Check the workflow logs for specific errors
- Most common: dependency version mismatches
- Try triggering the build again (sometimes network issues)

### Can't Find Actions Tab?
- Make sure you're logged into GitHub
- The repo must not be a fork (or enable Actions in fork settings)

### APK Won't Install?
- Make sure "Unknown Sources" is enabled
- Check if you have enough storage space
- Ensure your Android version is 6.0 or higher

---

## 📋 App Features

- 📊 Real-time stock breakout scanning
- 📈 Technical analysis (RSI, MACD, Bollinger Bands)
- 💰 Trading recommendations (Entry, Stop Loss, Target)
- ❤️ Watchlist management
- 🔐 User authentication
- 🎨 Beautiful pastel UI

---

## 📞 Support

If you encounter any issues, check the GitHub Actions logs for detailed error messages.
