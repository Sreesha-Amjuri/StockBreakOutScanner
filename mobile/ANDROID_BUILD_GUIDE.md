# StockBreak Pro - Android App Build Guide

## Prerequisites

To build the Android APK, you need:
1. Node.js (v18+)
2. Java JDK 17
3. Android SDK
4. Android Build Tools

## Setup Instructions

### 1. Install Dependencies

```bash
cd /app/mobile
yarn install
```

### 2. Generate Release Keystore

The keystore is needed to sign the APK for installation:

```bash
cd android/app
keytool -genkeypair -v -storetype PKCS12 -keystore stockbreak-release-key.keystore -alias stockbreak-key -keyalg RSA -keysize 2048 -validity 10000
```

Use the following credentials:
- Keystore Password: `stockbreak2024`
- Key Password: `stockbreak2024`
- First and Last Name: `StockBreak Pro`
- Organizational Unit: `Development`
- Organization: `StockBreak`
- City: `Mumbai`
- State: `Maharashtra`
- Country Code: `IN`

### 3. Build the APK

#### Option A: Using Gradle (Recommended)

```bash
cd /app/mobile/android
./gradlew assembleRelease
```

The APK will be generated at:
`/app/mobile/android/app/build/outputs/apk/release/app-release.apk`

#### Option B: Using React Native CLI

```bash
cd /app/mobile
npx react-native run-android --variant=release
```

### 4. Install the APK

#### On Physical Device:
1. Enable "Install from Unknown Sources" in device settings
2. Transfer the APK to your device
3. Open the APK file and follow installation prompts

#### On Emulator:
```bash
adb install android/app/build/outputs/apk/release/app-release.apk
```

## Testing the App

### Run in Development Mode

```bash
# Start Metro bundler
npx react-native start

# In another terminal, run on Android
npx react-native run-android
```

### Debug on Device

```bash
adb devices  # Check connected devices
adb logcat *:E  # View error logs
```

## App Features

✅ User Authentication (Register/Login with JWT)
✅ Dashboard with Real-time Stock Breakout Scanning  
✅ Individual Stock Detail Pages
✅ Technical Indicators (RSI, MACD, Bollinger Bands, etc.)
✅ Trading Recommendations (Entry, Stop Loss, Target)
✅ Watchlist Management
✅ Elegant Pastel UI Theme
✅ Pull-to-Refresh
✅ Search Functionality
✅ Auto-refresh with FAB button

## API Configuration

The app connects to the backend API at:
`https://tradewise-176.preview.emergentagent.com/api`

To change the API URL, edit `/app/mobile/.env`:
```
API_BASE_URL=your_api_url_here
```

## Troubleshooting

### Build Failures

1. **Gradle Sync Issues:**
   ```bash
   cd android
   ./gradlew clean
   ./gradlew build
   ```

2. **Dependency Errors:**
   ```bash
   cd ..
   rm -rf node_modules
   yarn install
   ```

3. **Metro Bundler Issues:**
   ```bash
   npx react-native start --reset-cache
   ```

### Installation Issues

1. **"App not installed" error:**
   - Uninstall any previous version
   - Clear package installer cache
   - Ensure "Install from Unknown Sources" is enabled

2. **Signature mismatch:**
   - Uninstall the existing app completely
   - Install the new APK

## App Size

The release APK size is approximately **50-70 MB**.

To reduce size:
- Enable Proguard (already configured)
- Use split APKs for different architectures
- Remove unused resources

## Permissions

The app requires:
- `INTERNET` - For API calls
- `ACCESS_NETWORK_STATE` - For network connectivity checks

## Security

- All passwords are hashed with bcrypt
- JWT tokens are stored securely in AsyncStorage
- HTTPS is enforced for API calls
- No sensitive data is logged in production

## Support

For issues or questions:
- Check the backend logs: `tail -f /var/log/supervisor/backend.err.log`
- Test API endpoints: `curl https://tradewise-176.preview.emergentagent.com/api/`
- Review React Native logs: `adb logcat`

## Version Information

- App Version: 1.0.0
- React Native: 0.73.0
- Target Android SDK: 34 (Android 14)
- Minimum Android SDK: 23 (Android 6.0)
