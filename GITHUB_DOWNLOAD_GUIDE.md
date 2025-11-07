# 📥 Download StockBreak Pro APK from GitHub - Complete Guide

## 🎯 Overview

Your Android app is now configured to **automatically build** on GitHub! When you push the code to GitHub, it will:
1. ✅ Automatically build the APK
2. ✅ Upload it to GitHub Releases
3. ✅ Make it available for download

---

## 📋 Step-by-Step Instructions

### Step 1: Create GitHub Repository

1. **Go to GitHub**: https://github.com/new

2. **Create a new repository**:
   - Repository name: `stockbreak-pro` (or any name you like)
   - Description: `StockBreak Pro - Professional Stock Analysis Android App`
   - **Keep it Private** (recommended) or Public
   - **DON'T** initialize with README
   - Click "Create repository"

### Step 2: Push Your Code to GitHub

Open your terminal and run these commands:

```bash
# 1. Navigate to your project
cd /app

# 2. Initialize git (if not already done)
git init

# 3. Add all files
git add .

# 4. Commit
git commit -m "Initial commit - StockBreak Pro Android App"

# 5. Add your GitHub repository as remote
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/stockbreak-pro.git

# 6. Push to GitHub
git push -u origin main
```

**Note**: If your default branch is `master` instead of `main`:
```bash
git branch -M main
git push -u origin main
```

### Step 3: GitHub Actions Builds Your APK

After pushing:

1. **GitHub Actions automatically starts** building your APK
2. Go to your repository on GitHub
3. Click on the **"Actions"** tab at the top
4. You'll see "Build Android APK" workflow running
5. **Wait 5-10 minutes** for the build to complete

### Step 4: Download Your APK

You have **2 ways** to download:

#### Option A: From Releases (Recommended - Easier!)

1. Go to your repository on GitHub
2. Click **"Releases"** (right side of the page)
3. Click on the latest release (e.g., "StockBreak Pro v1.0.1")
4. Under "Assets", click on **`StockBreakPro-v1.0.1.apk`**
5. APK downloads to your computer! 🎉

#### Option B: From Actions (Alternative)

1. Go to your repository on GitHub
2. Click **"Actions"** tab
3. Click on the completed workflow run (green checkmark ✅)
4. Scroll down to **"Artifacts"** section
5. Click **"StockBreakPro-APK"** to download
6. Unzip the downloaded file to get the APK

---

## 🔄 Every Time You Make Changes

Whenever you push new code to GitHub:

```bash
cd /app
git add .
git commit -m "Updated features"
git push
```

GitHub will **automatically**:
- Build a new APK
- Create a new release
- Increment version number

You can download the latest version from Releases!

---

## 📱 Install APK on Your Phone

After downloading the APK:

### Method 1: USB Transfer
```bash
# Connect your phone via USB
adb install StockBreakPro-v1.0.1.apk
```

### Method 2: Cloud Transfer
1. Upload APK to Google Drive/Dropbox
2. Download on your phone
3. Open Downloads folder
4. Tap APK file → Install

### Method 3: Email
1. Email the APK to yourself
2. Open email on phone
3. Download attachment
4. Tap to install

**Before Installing**:
- Go to Settings → Security
- Enable "Install from Unknown Sources" or "Allow from this source"

---

## 🎨 What Your Workflow Does

The GitHub Actions workflow (`.github/workflows/build-android-apk.yml`) automatically:

1. ✅ Sets up Node.js 18
2. ✅ Sets up Java JDK 17
3. ✅ Installs Android SDK
4. ✅ Installs all dependencies (`yarn install`)
5. ✅ Builds the release APK (`./gradlew assembleRelease`)
6. ✅ Signs the APK with your keystore
7. ✅ Uploads to Artifacts
8. ✅ Creates a GitHub Release
9. ✅ Attaches APK to the release

**Build Time**: 5-10 minutes  
**Cost**: FREE (GitHub Actions free tier: 2,000 minutes/month)

---

## 🔧 Trigger Manual Build

You can manually trigger a build without pushing code:

1. Go to your repository on GitHub
2. Click **"Actions"** tab
3. Click **"Build Android APK"** workflow (left sidebar)
4. Click **"Run workflow"** button (right side)
5. Select branch (main)
6. Click green **"Run workflow"** button
7. Wait for build to complete
8. Download from Releases or Artifacts

---

## 📊 Build Status

After each push, you can check:

1. **Build Status**: 
   - Green checkmark ✅ = Success
   - Red X ❌ = Failed (check logs)
   - Yellow dot 🟡 = Building...

2. **Build Logs**: 
   - Click on the workflow run
   - Click on "build-android" job
   - Expand steps to see detailed logs

3. **Build Time**: Usually 5-10 minutes

---

## 🐛 Troubleshooting

### Build Fails

**Check the logs**:
1. Go to Actions tab
2. Click on the failed workflow
3. Click "build-android"
4. Look at the red X steps

**Common issues**:

**Problem**: "yarn.lock not found"
**Solution**: 
```bash
cd /app/mobile
yarn install
git add yarn.lock
git commit -m "Add yarn.lock"
git push
```

**Problem**: "gradlew permission denied"
**Solution**: Already fixed in the workflow (chmod +x)

**Problem**: "Keystore not found"
**Solution**: Keystore is already in `/app/mobile/android/app/stockbreak-release-key.keystore`

### APK Not in Releases

**If APK only in Artifacts**:
- This happens if you pushed to a branch other than `main`/`master`
- Only pushes to `main`/`master` create releases
- You can still download from Artifacts

**Solution**: Push to main branch
```bash
git checkout main
git push origin main
```

### Can't Push to GitHub

**Authentication required**:

1. **Use Personal Access Token** (recommended):
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate new token (classic)
   - Select `repo` scope
   - Copy the token
   - Use token as password when pushing

2. **Or use SSH**:
   ```bash
   # Change remote to SSH
   git remote set-url origin git@github.com:YOUR_USERNAME/stockbreak-pro.git
   ```

---

## 📦 What Gets Built

Your APK will be:
- **Name**: `StockBreakPro-v1.0.X.apk`
- **Size**: ~50-70 MB
- **Signed**: Yes (with your release keystore)
- **Optimized**: Yes (ProGuard enabled)
- **Min Android**: 6.0 (API 23)
- **Target Android**: 14 (API 34)

---

## 🎉 Success Checklist

- [ ] Created GitHub repository
- [ ] Pushed code to GitHub
- [ ] GitHub Actions workflow running
- [ ] Build completed successfully (green ✅)
- [ ] APK visible in Releases tab
- [ ] Downloaded APK to computer
- [ ] Transferred APK to phone
- [ ] Enabled Unknown Sources
- [ ] Installed StockBreak Pro
- [ ] App opens and works! 🎊

---

## 🔄 Version Numbers

Each build automatically increments:
- First push: `v1.0.1`
- Second push: `v1.0.2`
- Third push: `v1.0.3`
- And so on...

The version is based on GitHub run number.

---

## 💡 Pro Tips

1. **Test Locally First**: Make sure the app works before pushing to GitHub

2. **Branch Protection**: For production, use branches:
   ```bash
   git checkout -b develop
   git push origin develop
   # Test builds on develop branch
   # Merge to main when ready
   ```

3. **Release Notes**: Edit releases on GitHub to add:
   - What's new
   - Bug fixes
   - Known issues

4. **Multiple APKs**: GitHub Actions keeps last 30 builds in Artifacts

5. **Build Badge**: Add to your README:
   ```markdown
   ![Build Status](https://github.com/YOUR_USERNAME/stockbreak-pro/actions/workflows/build-android-apk.yml/badge.svg)
   ```

---

## 🆘 Need Help?

**Workflow file location**: `/app/.github/workflows/build-android-apk.yml`

**Key files**:
- GitHub Actions workflow: `.github/workflows/build-android-apk.yml`
- Gradle wrapper: `mobile/android/gradlew`
- Build config: `mobile/android/app/build.gradle`
- Keystore: `mobile/android/app/stockbreak-release-key.keystore`

**Helpful commands**:
```bash
# Check git status
git status

# View commit history
git log --oneline

# Force push (if needed)
git push -f origin main

# Check remote
git remote -v
```

---

## 📞 Quick Reference

**GitHub Repository**: `https://github.com/YOUR_USERNAME/stockbreak-pro`  
**Actions Page**: `https://github.com/YOUR_USERNAME/stockbreak-pro/actions`  
**Releases Page**: `https://github.com/YOUR_USERNAME/stockbreak-pro/releases`

**Keystore Password**: `stockbreak2024`  
**Key Alias**: `stockbreak-key`  
**Key Password**: `stockbreak2024`

---

## 🎊 That's It!

Once you push to GitHub:
1. ⏰ Wait 5-10 minutes
2. 📥 Download APK from Releases
3. 📱 Install on your phone
4. 🚀 Enjoy StockBreak Pro!

**GitHub does all the hard work for you!** 🎉
