# 📈 StockBreak Pro - Indian Stock Breakout Screener

<div align="center">

![StockBreak Pro](https://img.shields.io/badge/StockBreak-Pro-blue?style=for-the-badge&logo=trending-up)
![Version](https://img.shields.io/badge/version-2.0.0-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-orange?style=for-the-badge)

**A professional-grade Indian stock market breakout screener with real-time NSE data, advanced technical analysis, and actionable trading recommendations.**

</div>

## 🚀 Features

### 📊 **Core Functionality**
- **Real-time NSE Data**: Live stock prices and market data from Yahoo Finance
- **Advanced Breakout Detection**: 5 different breakout types (200 DMA, Resistance, Momentum, Bollinger, Stochastic)
- **Professional Trading Recommendations**: Entry points, stop losses, target prices, and position sizing
- **Comprehensive Technical Analysis**: 15+ indicators (RSI, MACD, Bollinger Bands, VWAP, ATR, etc.)
- **Risk Assessment**: Algorithmic risk scoring with detailed risk factors
- **Multi-source Data Validation**: Cross-verification for data accuracy

### 🎯 **Trading Features**
- **Smart Entry Points**: Optimal prices based on breakout analysis
- **Professional Risk Management**: Support/ATR/volatility-based stop losses  
- **Target Price Calculation**: Risk-reward ratios from 1:2 to 1:3
- **Position Size Recommendations**: 3-15% portfolio allocation suggestions
- **Trading Actions**: BUY/WAIT/AVOID recommendations with confidence scoring

### 📱 **User Interface**
- **Premium Dashboard**: Modern glass-morphism design with soft pastel colors
- **Interactive Charts**: Multi-timeframe charts (5D, 1M, 3M, 6M, 1Y, 2Y)
- **Advanced Filtering**: Filter by sector, confidence level, risk assessment
- **Real-time Market Status**: NSE market hours with IST timing
- **Watchlist Management**: Save and track favorite stocks
- **Responsive Design**: Works on desktop, tablet, and mobile

## 🏗️ Architecture

```
StockBreak Pro/
├── 🎨 Frontend (React 19)
│   ├── Modern UI with Tailwind CSS
│   ├── Interactive charts with Recharts
│   ├── ShadCN UI components
│   └── Real-time data updates
├── ⚡ Backend (FastAPI)
│   ├── RESTful API endpoints
│   ├── Multi-source data validation
│   ├── Advanced technical analysis
│   └── Trading recommendation engine
└── 🗄️ Database (MongoDB)
    ├── Watchlist management
    ├── User preferences
    └── Historical data caching
```

## 📋 Prerequisites

### System Requirements
- **Node.js**: 18.0.0 or higher
- **Python**: 3.8 or higher
- **MongoDB**: 4.4 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space

### Required Accounts
- **Yahoo Finance**: Free (for stock data)
- **MongoDB**: Free cluster or local installation

## 🛠️ Installation Guide

### 🪟 **Windows Installation**

#### Step 1: Install Prerequisites

1. **Install Node.js**
   ```bash
   # Download from https://nodejs.org/
   # Or using Chocolatey
   choco install nodejs
   ```

2. **Install Python**
   ```bash
   # Download from https://python.org/
   # Or using Chocolatey
   choco install python
   ```

3. **Install MongoDB**
   ```bash
   # Download MongoDB Community Server from https://mongodb.com/
   # Or using Chocolatey
   choco install mongodb
   ```

4. **Install Git**
   ```bash
   # Download from https://git-scm.com/
   # Or using Chocolatey
   choco install git
   ```

#### Step 2: Clone and Setup Project

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-username/stockbreak-pro.git
   cd stockbreak-pro
   ```

2. **Setup Backend**
   ```bash
   cd backend
   
   # Create virtual environment
   python -m venv venv
   venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Create .env file
   copy .env.example .env
   notepad .env
   ```

3. **Configure Backend Environment**
   ```env
   # backend/.env
   MONGO_URL=mongodb://localhost:27017
   DB_NAME=stockbreak_pro
   CORS_ORIGINS=http://localhost:3000
   ```

4. **Setup Frontend**
   ```bash
   cd ..\frontend
   
   # Install dependencies
   npm install
   # or
   yarn install
   
   # Create .env file
   copy .env.example .env
   notepad .env
   ```

5. **Configure Frontend Environment**
   ```env
   # frontend/.env
   REACT_APP_BACKEND_URL=http://localhost:8001
   ```

#### Step 3: Run the Application

1. **Start MongoDB**
   ```bash
   # Start MongoDB service
   net start MongoDB
   ```

2. **Start Backend** (in new terminal)
   ```bash
   cd backend
   venv\Scripts\activate
   uvicorn server:app --host 0.0.0.0 --port 8001 --reload
   ```

3. **Start Frontend** (in new terminal)
   ```bash
   cd frontend
   npm start
   # or
   yarn start
   ```

4. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8001
   - API Documentation: http://localhost:8001/docs

### 🐧 **Linux Installation**

#### Step 1: Install Prerequisites

1. **Ubuntu/Debian**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Node.js
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   
   # Install Python and pip
   sudo apt install python3 python3-pip python3-venv -y
   
   # Install MongoDB
   wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
   echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
   sudo apt-get update
   sudo apt-get install -y mongodb-org
   
   # Install Git
   sudo apt install git -y
   ```

2. **CentOS/RHEL/Fedora**
   ```bash
   # Install Node.js
   curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
   sudo dnf install nodejs -y
   
   # Install Python
   sudo dnf install python3 python3-pip -y
   
   # Install MongoDB
   sudo dnf install mongodb mongodb-server -y
   
   # Install Git
   sudo dnf install git -y
   ```

#### Step 2: Clone and Setup Project

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-username/stockbreak-pro.git
   cd stockbreak-pro
   ```

2. **Setup Backend**
   ```bash
   cd backend
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Create .env file
   cp .env.example .env
   nano .env
   ```

3. **Configure Backend Environment**
   ```env
   # backend/.env
   MONGO_URL=mongodb://localhost:27017
   DB_NAME=stockbreak_pro
   CORS_ORIGINS=http://localhost:3000
   ```

4. **Setup Frontend**
   ```bash
   cd ../frontend
   
   # Install dependencies
   npm install
   # or
   yarn install
   
   # Create .env file
   cp .env.example .env
   nano .env
   ```

5. **Configure Frontend Environment**
   ```env
   # frontend/.env
   REACT_APP_BACKEND_URL=http://localhost:8001
   ```

#### Step 3: Run the Application

1. **Start MongoDB**
   ```bash
   # Ubuntu/Debian
   sudo systemctl start mongod
   sudo systemctl enable mongod
   
   # CentOS/RHEL/Fedora
   sudo systemctl start mongodb
   sudo systemctl enable mongodb
   ```

2. **Start Backend** (in new terminal)
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn server:app --host 0.0.0.0 --port 8001 --reload
   ```

3. **Start Frontend** (in new terminal)
   ```bash
   cd frontend
   npm start
   # or
   yarn start
   ```

4. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8001
   - API Documentation: http://localhost:8001/docs

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
# Database Configuration
MONGO_URL=mongodb://localhost:27017
DB_NAME=stockbreak_pro

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# API Configuration
API_VERSION=v1
DEBUG=true

# Stock Data Configuration
DEFAULT_SCAN_LIMIT=50
MAX_CONCURRENT_REQUESTS=10
```

#### Frontend (.env)
```env
# Backend API URL
REACT_APP_BACKEND_URL=http://localhost:8001

# Application Configuration
REACT_APP_NAME=StockBreak Pro
REACT_APP_VERSION=2.0.0

# Feature Flags
REACT_APP_ENABLE_ANALYTICS=false
REACT_APP_ENABLE_NOTIFICATIONS=true
```

## 📚 API Documentation

### Core Endpoints

#### Stock Data
```http
GET /api/stocks/symbols
GET /api/stocks/{symbol}
GET /api/stocks/{symbol}/chart?timeframe=1mo
GET /api/stocks/{symbol}/validate
```

#### Breakout Analysis
```http
GET /api/stocks/breakouts/scan
GET /api/stocks/breakouts/scan?sector=IT&min_confidence=0.7
```

#### Market Data
```http
GET /api/stocks/market-overview
```

#### Watchlist Management
```http
GET /api/watchlist
POST /api/watchlist?symbol=RELIANCE
DELETE /api/watchlist/{symbol}
```

### Response Examples

#### Breakout Scan Response
```json
{
  "breakout_stocks": [
    {
      "symbol": "RELIANCE",
      "name": "Reliance Industries Limited",
      "current_price": 2450.75,
      "change_percent": 2.3,
      "breakout_type": "200_dma",
      "confidence_score": 0.85,
      "trading_recommendation": {
        "entry_price": 2460.00,
        "stop_loss": 2380.00,
        "target_price": 2700.00,
        "risk_reward_ratio": 3.0,
        "action": "BUY",
        "position_size_percent": 8.5
      },
      "technical_data": {
        "rsi": 65.4,
        "macd": 12.5,
        "sma_200": 2420.30
      },
      "risk_assessment": {
        "risk_level": "Medium",
        "risk_score": 5.2
      }
    }
  ],
  "breakouts_found": 15,
  "total_scanned": 50
}
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Run unit tests
pytest tests/ -v

# Run specific test
pytest tests/test_breakout_detection.py -v

# Run with coverage
pytest --cov=. tests/
```

### Frontend Testing
```bash
cd frontend

# Run unit tests
npm test
# or
yarn test

# Run integration tests
npm run test:integration

# Run e2e tests
npm run test:e2e
```

### API Testing
```bash
# Test individual endpoints
curl -X GET "http://localhost:8001/api/stocks/RELIANCE"
curl -X GET "http://localhost:8001/api/stocks/breakouts/scan?limit=10"

# Test with different parameters
curl -X GET "http://localhost:8001/api/stocks/breakouts/scan?sector=IT&min_confidence=0.8"
```

## 🚀 Deployment

### Production Environment Variables

#### Backend
```env
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/stockbreak_pro
CORS_ORIGINS=https://yourdomain.com
DEBUG=false
API_RATE_LIMIT=100
```

#### Frontend
```env
REACT_APP_BACKEND_URL=https://api.yourdomain.com
REACT_APP_ENABLE_ANALYTICS=true
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Checklist
- [ ] Environment variables configured
- [ ] Database indexes created
- [ ] SSL certificates installed
- [ ] Rate limiting enabled
- [ ] Monitoring setup
- [ ] Backup strategy implemented
- [ ] CDN configured for frontend assets

## 🛠️ Troubleshooting

### Common Issues

#### Frontend Issues

**Issue**: "Network Error" when loading data
```bash
# Check if backend is running
curl http://localhost:8001/api/

# Check environment variables
echo $REACT_APP_BACKEND_URL

# Clear browser cache and reload
```

**Issue**: npm install fails with "Could not read package.json"
```bash
# The npm install command must be run from the frontend directory
cd frontend
npm install

# Or use the root-level script to install all dependencies
npm run install-all
```

**Issue**: Charts not loading
```bash
# Check if chart data endpoint works
curl http://localhost:8001/api/stocks/RELIANCE/chart

# Verify recharts dependency
npm list recharts
```

#### Backend Issues

**Issue**: MongoDB connection failed
```bash
# Check MongoDB status
sudo systemctl status mongod  # Linux
net start MongoDB             # Windows

# Test connection
python -c "from pymongo import MongoClient; print(MongoClient('mongodb://localhost:27017').admin.command('ping'))"
```

**Issue**: Yahoo Finance data not loading
```bash
# Test yfinance directly
python -c "import yfinance as yf; print(yf.Ticker('RELIANCE.NS').history(period='1d'))"

# Check internet connection and firewall
curl -I https://finance.yahoo.com
```

**Issue**: High memory usage
```bash
# Monitor process
top -p $(pgrep -f uvicorn)

# Reduce concurrent requests in .env
DEFAULT_SCAN_LIMIT=20
MAX_CONCURRENT_REQUESTS=5
```

### Performance Optimization

#### Backend Optimization
```python
# Add to server.py for production
import asyncio

# Increase worker processes
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8001, workers=4)
```

#### Frontend Optimization
```bash
# Build optimized version
npm run build

# Analyze bundle size
npm install -g webpack-bundle-analyzer
npx webpack-bundle-analyzer build/static/js/*.js
```

### Debug Mode

#### Enable Debug Logging
```python
# backend/server.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

```javascript
// frontend/src/App.js
const DEBUG = process.env.NODE_ENV === 'development';
if (DEBUG) console.log('Debug info:', data);
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- Backend: Follow PEP 8 (use `black` and `flake8`)
- Frontend: Follow Airbnb JavaScript Style Guide (use `eslint` and `prettier`)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**Important**: This application is for educational and informational purposes only. It is not intended as financial advice. Always consult with qualified financial professionals before making investment decisions. The developers are not responsible for any financial losses incurred from using this application.

## 🙏 Acknowledgments

- [Yahoo Finance](https://finance.yahoo.com) for stock data
- [React](https://reactjs.org/) for the frontend framework
- [FastAPI](https://fastapi.tiangolo.com/) for the backend API
- [MongoDB](https://mongodb.com/) for the database
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [ShadCN UI](https://ui.shadcn.com/) for UI components

## 📞 Support

For support, email support@stockbreakpro.com or create an issue on GitHub.

---

<div align="center">

**Made with ❤️ for the Indian stock market community**

![India](https://img.shields.io/badge/Made%20in-India-ff9933?style=for-the-badge&logo=india)

</div>
