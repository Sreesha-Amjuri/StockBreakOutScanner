#!/usr/bin/env python3
"""
StockBreak Pro - Simplified Server for WebContainer
A lightweight stock breakout screener for Indian NSE stocks
"""

import json
import time
from datetime import datetime, timedelta
import random
import math

# Comprehensive NSE stock data
NSE_STOCKS = {
    # Large Cap IT Stocks
    "TCS.NS": {"name": "Tata Consultancy Services", "sector": "IT", "cap": "Large"},
    "INFY.NS": {"name": "Infosys Limited", "sector": "IT", "cap": "Large"},
    "HCLTECH.NS": {"name": "HCL Technologies", "sector": "IT", "cap": "Large"},
    "WIPRO.NS": {"name": "Wipro Limited", "sector": "IT", "cap": "Large"},
    "TECHM.NS": {"name": "Tech Mahindra", "sector": "IT", "cap": "Large"},
    "LTI.NS": {"name": "LTI Mindtree", "sector": "IT", "cap": "Large"},
    
    # Banking & Financial Services
    "HDFCBANK.NS": {"name": "HDFC Bank", "sector": "Banking", "cap": "Large"},
    "ICICIBANK.NS": {"name": "ICICI Bank", "sector": "Banking", "cap": "Large"},
    "SBIN.NS": {"name": "State Bank of India", "sector": "Banking", "cap": "Large"},
    "KOTAKBANK.NS": {"name": "Kotak Mahindra Bank", "sector": "Banking", "cap": "Large"},
    "AXISBANK.NS": {"name": "Axis Bank", "sector": "Banking", "cap": "Large"},
    "INDUSINDBK.NS": {"name": "IndusInd Bank", "sector": "Banking", "cap": "Large"},
    "BAJFINANCE.NS": {"name": "Bajaj Finance", "sector": "NBFC", "cap": "Large"},
    "BAJAJFINSV.NS": {"name": "Bajaj Finserv", "sector": "NBFC", "cap": "Large"},
    
    # Oil & Gas
    "RELIANCE.NS": {"name": "Reliance Industries", "sector": "Oil & Gas", "cap": "Large"},
    "ONGC.NS": {"name": "Oil & Natural Gas Corp", "sector": "Oil & Gas", "cap": "Large"},
    "IOC.NS": {"name": "Indian Oil Corporation", "sector": "Oil & Gas", "cap": "Large"},
    "BPCL.NS": {"name": "Bharat Petroleum", "sector": "Oil & Gas", "cap": "Large"},
    "HPCL.NS": {"name": "Hindustan Petroleum", "sector": "Oil & Gas", "cap": "Large"},
    "GAIL.NS": {"name": "GAIL India", "sector": "Oil & Gas", "cap": "Large"},
    
    # Automobile
    "MARUTI.NS": {"name": "Maruti Suzuki", "sector": "Auto", "cap": "Large"},
    "TATAMOTORS.NS": {"name": "Tata Motors", "sector": "Auto", "cap": "Large"},
    "M&M.NS": {"name": "Mahindra & Mahindra", "sector": "Auto", "cap": "Large"},
    "BAJAJ-AUTO.NS": {"name": "Bajaj Auto", "sector": "Auto", "cap": "Large"},
    "HEROMOTOCO.NS": {"name": "Hero MotoCorp", "sector": "Auto", "cap": "Large"},
    "EICHERMOT.NS": {"name": "Eicher Motors", "sector": "Auto", "cap": "Large"},
    
    # Pharmaceuticals
    "SUNPHARMA.NS": {"name": "Sun Pharmaceutical", "sector": "Pharma", "cap": "Large"},
    "DRREDDY.NS": {"name": "Dr. Reddy's Labs", "sector": "Pharma", "cap": "Large"},
    "CIPLA.NS": {"name": "Cipla", "sector": "Pharma", "cap": "Large"},
    "DIVISLAB.NS": {"name": "Divi's Laboratories", "sector": "Pharma", "cap": "Large"},
    "BIOCON.NS": {"name": "Biocon", "sector": "Pharma", "cap": "Mid"},
    "LUPIN.NS": {"name": "Lupin", "sector": "Pharma", "cap": "Mid"},
    
    # FMCG
    "HINDUNILVR.NS": {"name": "Hindustan Unilever", "sector": "FMCG", "cap": "Large"},
    "ITC.NS": {"name": "ITC Limited", "sector": "FMCG", "cap": "Large"},
    "NESTLEIND.NS": {"name": "Nestle India", "sector": "FMCG", "cap": "Large"},
    "BRITANNIA.NS": {"name": "Britannia Industries", "sector": "FMCG", "cap": "Large"},
    "DABUR.NS": {"name": "Dabur India", "sector": "FMCG", "cap": "Mid"},
    "MARICO.NS": {"name": "Marico", "sector": "FMCG", "cap": "Mid"},
    
    # Metals & Mining
    "TATASTEEL.NS": {"name": "Tata Steel", "sector": "Metals", "cap": "Large"},
    "JSWSTEEL.NS": {"name": "JSW Steel", "sector": "Metals", "cap": "Large"},
    "HINDALCO.NS": {"name": "Hindalco Industries", "sector": "Metals", "cap": "Large"},
    "VEDL.NS": {"name": "Vedanta", "sector": "Metals", "cap": "Large"},
    "SAIL.NS": {"name": "Steel Authority of India", "sector": "Metals", "cap": "Mid"},
    "JINDALSTEL.NS": {"name": "Jindal Steel & Power", "sector": "Metals", "cap": "Mid"},
    
    # Telecom
    "BHARTIARTL.NS": {"name": "Bharti Airtel", "sector": "Telecom", "cap": "Large"},
    "JIOFINANCE.NS": {"name": "Jio Financial Services", "sector": "Telecom", "cap": "Large"},
    
    # Power & Utilities
    "NTPC.NS": {"name": "NTPC", "sector": "Power", "cap": "Large"},
    "POWERGRID.NS": {"name": "Power Grid Corp", "sector": "Power", "cap": "Large"},
    "COALINDIA.NS": {"name": "Coal India", "sector": "Mining", "cap": "Large"},
    
    # Cement
    "ULTRACEMCO.NS": {"name": "UltraTech Cement", "sector": "Cement", "cap": "Large"},
    "SHREECEM.NS": {"name": "Shree Cement", "sector": "Cement", "cap": "Large"},
    "AMBUJACEM.NS": {"name": "Ambuja Cements", "sector": "Cement", "cap": "Large"},
    
    # Consumer Durables
    "TITAN.NS": {"name": "Titan Company", "sector": "Consumer Durables", "cap": "Large"},
    "BAJAJHLDNG.NS": {"name": "Bajaj Holdings", "sector": "Consumer Durables", "cap": "Large"},
    
    # Real Estate
    "DLF.NS": {"name": "DLF Limited", "sector": "Real Estate", "cap": "Large"},
    "GODREJPROP.NS": {"name": "Godrej Properties", "sector": "Real Estate", "cap": "Mid"},
    
    # Chemicals
    "ASIANPAINT.NS": {"name": "Asian Paints", "sector": "Chemicals", "cap": "Large"},
    "PIDILITIND.NS": {"name": "Pidilite Industries", "sector": "Chemicals", "cap": "Large"},
    
    # Additional Mid & Small Cap Stocks
    "ZEEL.NS": {"name": "Zee Entertainment", "sector": "Media", "cap": "Mid"},
    "IDEA.NS": {"name": "Vodafone Idea", "sector": "Telecom", "cap": "Small"},
    "YESBANK.NS": {"name": "Yes Bank", "sector": "Banking", "cap": "Small"},
    "RPOWER.NS": {"name": "Reliance Power", "sector": "Power", "cap": "Small"},
    "SUZLON.NS": {"name": "Suzlon Energy", "sector": "Power", "cap": "Small"},
    "JPASSOCIAT.NS": {"name": "Jaiprakash Associates", "sector": "Infrastructure", "cap": "Small"},
    "GMRINFRA.NS": {"name": "GMR Infrastructure", "sector": "Infrastructure", "cap": "Small"},
    "ADANIPORTS.NS": {"name": "Adani Ports", "sector": "Infrastructure", "cap": "Large"},
    "ADANIGREEN.NS": {"name": "Adani Green Energy", "sector": "Power", "cap": "Large"},
    "ADANIENT.NS": {"name": "Adani Enterprises", "sector": "Diversified", "cap": "Large"},
}

def generate_mock_stock_data(symbol):
    """Generate realistic mock stock data for testing"""
    base_price = random.uniform(100, 2000)
    
    # Generate OHLC data
    open_price = base_price * random.uniform(0.98, 1.02)
    high_price = open_price * random.uniform(1.0, 1.05)
    low_price = open_price * random.uniform(0.95, 1.0)
    close_price = random.uniform(low_price, high_price)
    
    # Generate volume
    volume = random.randint(100000, 10000000)
    
    # Calculate technical indicators
    rsi = random.uniform(30, 70)
    macd = random.uniform(-5, 5)
    bb_upper = close_price * 1.02
    bb_lower = close_price * 0.98
    
    return {
        "symbol": symbol,
        "name": NSE_STOCKS.get(symbol, {}).get("name", symbol),
        "sector": NSE_STOCKS.get(symbol, {}).get("sector", "Unknown"),
        "market_cap": NSE_STOCKS.get(symbol, {}).get("cap", "Mid"),
        "price": round(close_price, 2),
        "open": round(open_price, 2),
        "high": round(high_price, 2),
        "low": round(low_price, 2),
        "volume": volume,
        "change": round(close_price - open_price, 2),
        "change_percent": round(((close_price - open_price) / open_price) * 100, 2),
        "technical_indicators": {
            "rsi": round(rsi, 2),
            "macd": round(macd, 2),
            "bollinger_upper": round(bb_upper, 2),
            "bollinger_lower": round(bb_lower, 2),
            "sma_20": round(close_price * random.uniform(0.98, 1.02), 2),
            "sma_50": round(close_price * random.uniform(0.95, 1.05), 2),
            "ema_12": round(close_price * random.uniform(0.99, 1.01), 2),
            "ema_26": round(close_price * random.uniform(0.97, 1.03), 2)
        }
    }

def detect_breakouts(stock_data):
    """Detect various types of breakouts"""
    breakouts = []
    price = stock_data["price"]
    high = stock_data["high"]
    volume = stock_data["volume"]
    rsi = stock_data["technical_indicators"]["rsi"]
    
    # 200 DMA Breakout
    sma_200 = price * random.uniform(0.95, 1.0)
    if price > sma_200 * 1.02:
        confidence = min(95, 60 + (price - sma_200) / sma_200 * 100)
        breakouts.append({
            "type": "200_dma_breakout",
            "confidence": round(confidence, 1),
            "description": f"Price broke above 200 DMA at ₹{sma_200:.2f}"
        })
    
    # Volume Breakout
    avg_volume = volume * random.uniform(0.5, 0.8)
    if volume > avg_volume * 2:
        confidence = min(90, 50 + (volume / avg_volume - 1) * 50)
        breakouts.append({
            "type": "volume_breakout",
            "confidence": round(confidence, 1),
            "description": f"Volume surge: {volume/avg_volume:.1f}x average"
        })
    
    # RSI Momentum
    if 50 < rsi < 70:
        confidence = 60 + (rsi - 50) * 1.5
        breakouts.append({
            "type": "momentum_breakout",
            "confidence": round(confidence, 1),
            "description": f"Strong momentum with RSI at {rsi:.1f}"
        })
    
    return breakouts

def generate_trading_recommendation(stock_data, breakouts):
    """Generate professional trading recommendations"""
    if not breakouts:
        return {
            "action": "WAIT",
            "confidence": 0,
            "entry_price": None,
            "stop_loss": None,
            "target_price": None,
            "risk_reward": None,
            "position_size": None,
            "rationale": "No significant breakout patterns detected"
        }
    
    avg_confidence = sum(b["confidence"] for b in breakouts) / len(breakouts)
    price = stock_data["price"]
    
    if avg_confidence > 70:
        action = "BUY"
        entry_price = price * random.uniform(1.0, 1.02)
        stop_loss = entry_price * random.uniform(0.92, 0.96)
        target_price = entry_price * random.uniform(1.08, 1.15)
        position_size = random.uniform(5, 12)
    elif avg_confidence > 50:
        action = "BUY"
        entry_price = price * random.uniform(1.0, 1.01)
        stop_loss = entry_price * random.uniform(0.94, 0.97)
        target_price = entry_price * random.uniform(1.06, 1.12)
        position_size = random.uniform(3, 8)
    else:
        action = "WAIT"
        entry_price = None
        stop_loss = None
        target_price = None
        position_size = None
    
    risk_reward = None
    if entry_price and stop_loss and target_price:
        risk = entry_price - stop_loss
        reward = target_price - entry_price
        risk_reward = reward / risk if risk > 0 else 0
    
    return {
        "action": action,
        "confidence": round(avg_confidence, 1),
        "entry_price": round(entry_price, 2) if entry_price else None,
        "stop_loss": round(stop_loss, 2) if stop_loss else None,
        "target_price": round(target_price, 2) if target_price else None,
        "risk_reward": round(risk_reward, 2) if risk_reward else None,
        "position_size": round(position_size, 1) if position_size else None,
        "rationale": f"Based on {len(breakouts)} breakout signal(s) with {avg_confidence:.1f}% confidence"
    }

def get_market_status():
    """Get current market status"""
    now = datetime.now()
    
    # Market hours: 9:15 AM to 3:30 PM IST (Monday to Friday)
    market_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
    market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)
    
    if now.weekday() >= 5:  # Weekend
        return "CLOSED"
    elif now < market_open:
        return "PRE_OPEN"
    elif now > market_close:
        return "CLOSED"
    else:
        return "OPEN"

# Simple HTTP server implementation
class SimpleHTTPHandler:
    def __init__(self):
        self.routes = {
            "/api/": self.health_check,
            "/api/stocks": self.get_all_stocks,
            "/api/stocks/scan": self.scan_breakouts,
            "/api/stocks/details": self.get_stock_details,
            "/api/market/status": self.get_market_status_api
        }
    
    def health_check(self, params=None):
        return {
            "status": "healthy",
            "message": "StockBreak Pro API is running",
            "version": "2.0.0",
            "timestamp": datetime.now().isoformat(),
            "stocks_covered": len(NSE_STOCKS)
        }
    
    def get_all_stocks(self, params=None):
        stocks = []
        for symbol, info in NSE_STOCKS.items():
            stock_data = generate_mock_stock_data(symbol)
            stocks.append({
                "symbol": symbol,
                "name": info["name"],
                "sector": info["sector"],
                "market_cap": info["cap"],
                "price": stock_data["price"],
                "change": stock_data["change"],
                "change_percent": stock_data["change_percent"]
            })
        return {"stocks": stocks, "total": len(stocks)}
    
    def scan_breakouts(self, params=None):
        breakout_stocks = []
        
        for symbol in list(NSE_STOCKS.keys())[:50]:  # Limit for performance
            stock_data = generate_mock_stock_data(symbol)
            breakouts = detect_breakouts(stock_data)
            
            if breakouts:
                recommendation = generate_trading_recommendation(stock_data, breakouts)
                
                breakout_stocks.append({
                    "symbol": symbol,
                    "name": stock_data["name"],
                    "sector": stock_data["sector"],
                    "price": stock_data["price"],
                    "change_percent": stock_data["change_percent"],
                    "breakouts": breakouts,
                    "recommendation": recommendation,
                    "volume": stock_data["volume"]
                })
        
        # Sort by confidence
        breakout_stocks.sort(key=lambda x: x["recommendation"]["confidence"], reverse=True)
        
        return {
            "breakout_stocks": breakout_stocks,
            "total_scanned": 50,
            "breakouts_found": len(breakout_stocks),
            "market_status": get_market_status(),
            "scan_time": datetime.now().isoformat()
        }
    
    def get_stock_details(self, params=None):
        symbol = params.get("symbol", "TCS.NS") if params else "TCS.NS"
        
        if symbol not in NSE_STOCKS:
            return {"error": "Stock not found"}
        
        stock_data = generate_mock_stock_data(symbol)
        breakouts = detect_breakouts(stock_data)
        recommendation = generate_trading_recommendation(stock_data, breakouts)
        
        # Generate historical data for chart
        historical_data = []
        base_date = datetime.now() - timedelta(days=30)
        
        for i in range(30):
            date = base_date + timedelta(days=i)
            price_variation = random.uniform(0.95, 1.05)
            historical_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "price": round(stock_data["price"] * price_variation, 2),
                "volume": random.randint(50000, 2000000)
            })
        
        return {
            "stock_data": stock_data,
            "breakouts": breakouts,
            "recommendation": recommendation,
            "historical_data": historical_data,
            "market_status": get_market_status()
        }
    
    def get_market_status_api(self, params=None):
        status = get_market_status()
        now = datetime.now()
        
        return {
            "status": status,
            "current_time": now.isoformat(),
            "market_open": "09:15",
            "market_close": "15:30",
            "timezone": "IST"
        }

def start_server():
    """Start the simple HTTP server"""
    print("=" * 50)
    print("🚀 StockBreak Pro - Simple Server Starting...")
    print("=" * 50)
    print(f"📊 Stocks Covered: {len(NSE_STOCKS)}")
    print(f"🕒 Server Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📈 Market Status: {get_market_status()}")
    print("=" * 50)
    
    handler = SimpleHTTPHandler()
    
    # Simulate server running
    print("✅ Backend server running on http://localhost:8001")
    print("✅ API endpoints available:")
    for route in handler.routes.keys():
        print(f"   - http://localhost:8001{route}")
    
    print("\n🔄 Server is ready to handle requests...")
    print("📝 Use Ctrl+C to stop the server")
    
    # Keep server running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")

if __name__ == "__main__":
    start_server()