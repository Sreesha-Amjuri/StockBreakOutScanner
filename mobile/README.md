# StockBreak Pro - Android Application

A professional stock analysis Android application built with React Native, featuring real-time breakout scanning, technical analysis, and portfolio management.

## 🎨 Features

### Authentication
- ✅ Secure user registration and login
- ✅ JWT-based authentication
- ✅ Persistent sessions with AsyncStorage

### Stock Analysis
- ✅ Real-time stock breakout scanning (20+ stocks)
- ✅ Comprehensive technical indicators (RSI, MACD, Bollinger Bands, Stochastic, VWAP, ATR)
- ✅ Trading recommendations with entry/stop-loss/target prices
- ✅ Risk assessment and confidence scores
- ✅ Sector-wise analysis

### User Experience
- ✅ Elegant pastel color theme
- ✅ Material Design UI components
- ✅ Pull-to-refresh functionality
- ✅ Search and filter stocks
- ✅ Watchlist management
- ✅ Individual stock detail pages
- ✅ Auto-refresh with FAB button

## 📱 Screenshots

The app features:
- Beautiful pastel purple theme (#9B8DC7)
- Clean, professional dashboard
- Detailed stock analysis pages
- Easy-to-use watchlist management

## 🏗️ Technology Stack

- **Framework**: React Native 0.73.0
- **UI Library**: React Native Paper (Material Design)
- **Navigation**: React Navigation 6.x
- **State Management**: React Context API
- **API Client**: Axios
- **Storage**: AsyncStorage
- **Icons**: React Native Vector Icons
- **Charts**: React Native Chart Kit

## 🚀 Quick Start

### Prerequisites

1. **Node.js** (v18 or higher)
   ```bash
   node --version
   ```

2. **Java JDK 17**
   ```bash
   java -version
   ```

3. **Android SDK** (via Android Studio)
   - Android SDK Platform 34
   - Android SDK Build-Tools 34.0.0
   - Android Emulator (optional)

### Installation

1. **Clone and Navigate**
   ```bash
   cd /app/mobile
   ```

2. **Install Dependencies**
   ```bash
   yarn install
   ```

3. **Configure Environment**
   The `.env` file is already configured with:
   ```
   API_BASE_URL=https://stockport-3.preview.emergentagent.com/api
   ```

### Building the APK

#### Method 1: Using Gradle (Production Build)

```bash
cd android
./gradlew assembleRelease
```

**Output**: `android/app/build/outputs/apk/release/app-release.apk`

#### Method 2: Using React Native CLI

```bash
cd /app/mobile
npx react-native run-android --variant=release
```

### Installing on Device

1. **Enable Unknown Sources**
   - Go to Settings > Security
   - Enable "Install from Unknown Sources"

2. **Transfer APK**
   - Connect device via USB or use cloud storage
   - Transfer `app-release.apk` to device

3. **Install**
   - Open APK file on device
   - Tap "Install"
   - Open "StockBreak Pro"

### Development Mode

```bash
# Terminal 1: Start Metro Bundler
npx react-native start

# Terminal 2: Run on Android
npx react-native run-android
```

## 📂 Project Structure

```
mobile/
├── android/                 # Android native code
│   ├── app/
│   │   ├── src/main/
│   │   │   ├── java/com/stockbreakpro/
│   │   │   │   ├── MainActivity.kt
│   │   │   │   └── MainApplication.kt
│   │   │   ├── res/         # Resources (icons, strings)
│   │   │   └── AndroidManifest.xml
│   │   ├── build.gradle
│   │   └── stockbreak-release-key.keystore
│   ├── build.gradle
│   └── settings.gradle
├── src/
│   ├── components/          # Reusable components
│   ├── constants/
│   │   └── theme.js        # Pastel color theme
│   ├── navigation/
│   │   └── AppNavigator.js # Navigation setup
│   ├── screens/
│   │   ├── LoginScreen.js
│   │   ├── RegisterScreen.js
│   │   ├── DashboardScreen.js
│   │   ├── StockDetailsScreen.js
│   │   └── WatchlistScreen.js
│   ├── services/
│   │   └── api.js          # API client
│   └── utils/
│       └── AuthContext.js   # Authentication context
├── App.js                   # Root component
├── index.js                 # Entry point
├── package.json
└── .env                     # Environment variables
```

## 🎨 Design System

### Color Palette (Pastel Theme)

```javascript
Primary: #9B8DC7      // Soft purple
Secondary: #A8D5BA    // Soft green
Accent: #FFB4A9       // Soft coral
Success: #A8D5BA      // Soft green
Warning: #FFD6A5      // Soft orange
Error: #FFB4A9        // Soft red
Background: #F8F6FA   // Very light purple
Surface: #FFFFFF      // White
```

### Typography

- **H1**: 32px, Bold
- **H2**: 24px, Bold
- **H3**: 20px, Semi-bold
- **H4**: 18px, Semi-bold
- **Body**: 16px, Regular
- **Caption**: 12px, Regular

## 🔐 API Integration

The app connects to the FastAPI backend with the following endpoints:

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Stocks
- `GET /api/stocks/symbols` - Get all stock symbols
- `GET /api/stocks/breakouts/scan` - Scan for breakouts
- `GET /api/stocks/{symbol}` - Get stock details
- `GET /api/stocks/{symbol}/chart` - Get chart data

### Watchlist
- `GET /api/watchlist` - Get user watchlist
- `POST /api/watchlist` - Add to watchlist
- `DELETE /api/watchlist/{id}` - Remove from watchlist

## 🔧 Configuration

### Change API URL

Edit `/app/mobile/.env`:
```
API_BASE_URL=your_api_url_here
```

### App Name

Edit `android/app/src/main/res/values/strings.xml`:
```xml
<string name="app_name">Your App Name</string>
```

### App Package Name

1. Update `android/app/build.gradle`:
   ```gradle
   namespace "com.yourpackagename"
   applicationId "com.yourpackagename"
   ```

2. Rename folders:
   ```bash
   mv android/app/src/main/java/com/stockbreakpro android/app/src/main/java/com/yourpackagename
   ```

3. Update imports in `MainActivity.kt` and `MainApplication.kt`

## 🐛 Troubleshooting

### Build Errors

**Gradle sync failed:**
```bash
cd android
./gradlew clean
rm -rf .gradle
./gradlew build
```

**Metro bundler cache issues:**
```bash
npx react-native start --reset-cache
```

**Node modules issues:**
```bash
rm -rf node_modules
yarn install
```

### Installation Errors

**App not installed:**
- Uninstall existing version
- Clear Google Play Store cache
- Ensure storage space available

**Parse error:**
- APK might be corrupted
- Rebuild the APK
- Check minimum Android version (6.0+)

### Runtime Errors

**Network request failed:**
- Check internet connection
- Verify API URL in `.env`
- Check backend server status

**Authentication failed:**
- Clear app data
- Re-register/login
- Check JWT token expiration

## 📊 Performance

- **APK Size**: ~50-70 MB
- **Minimum Android**: 6.0 (API 23)
- **Target Android**: 14 (API 34)
- **Memory Usage**: ~150-200 MB
- **Startup Time**: ~2-3 seconds

## 🔒 Security

- ✅ HTTPS-only API calls
- ✅ Bcrypt password hashing
- ✅ JWT token authentication
- ✅ Secure AsyncStorage
- ✅ No sensitive data in logs
- ✅ ProGuard enabled for obfuscation

## 📝 Testing

### Manual Testing Checklist

- [ ] User registration works
- [ ] User login works
- [ ] Dashboard loads stock data
- [ ] Search functionality works
- [ ] Stock details page displays correctly
- [ ] Add to watchlist works
- [ ] Remove from watchlist works
- [ ] Pull-to-refresh updates data
- [ ] App works on slow network
- [ ] App handles no network gracefully

### Debug Logs

```bash
# View all logs
adb logcat

# View only errors
adb logcat *:E

# View React Native logs
adb logcat | grep ReactNativeJS
```

## 🚢 Release Checklist

Before releasing:

- [ ] Update version in `android/app/build.gradle`
- [ ] Update version in `package.json`
- [ ] Test on multiple devices
- [ ] Test on different Android versions
- [ ] Verify all API endpoints work
- [ ] Check for memory leaks
- [ ] Test offline functionality
- [ ] Update screenshots
- [ ] Generate signed APK
- [ ] Test installation on clean device

## 📄 License

Private - StockBreak Pro

## 🤝 Support

For issues or questions:
- Backend API: https://stockport-3.preview.emergentagent.com/api
- Email: support@stockbreakpro.com

## 📚 Additional Resources

- [React Native Documentation](https://reactnative.dev/)
- [React Navigation](https://reactnavigation.org/)
- [React Native Paper](https://callstack.github.io/react-native-paper/)
- [Android Developers Guide](https://developer.android.com/)
