"""
StockBreak Pro - Indian Stock Breakout Screener Backend
Advanced NSE stock analysis with real-time data and trading recommendations
"""

import os
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import pytz
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import yfinance as yf
import pandas as pd
import numpy as np
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from utils.stock_data import COMPREHENSIVE_NSE_STOCKS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="StockBreak Pro API",
    description="Advanced Indian Stock Market Breakout Screener",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB configuration
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "stockbreak_pro")

# Global variables
mongo_client = None
db = None
nse_symbols_cache = COMPREHENSIVE_NSE_STOCKS
last_symbols_update = None

# Use comprehensive NSE stock universe
NSE_STOCK_UNIVERSE = COMPREHENSIVE_NSE_STOCKS

# Pydantic models
class WatchlistItem(BaseModel):
    symbol: str
    added_at: datetime

class TradingRecommendation(BaseModel):
    entry_price: float
    stop_loss: float
    target_price: float
    risk_reward_ratio: float
    position_size_percent: float
    action: str
    entry_rationale: str
    stop_loss_rationale: str

class BreakoutStock(BaseModel):
    symbol: str
    name: str
    current_price: float
    change_percent: float
    breakout_type: str
    confidence_score: float
    sector: str
    trading_recommendation: Optional[TradingRecommendation]
    technical_data: Dict
    risk_assessment: Dict

# Database connection
async def connect_to_mongo():
    global mongo_client, db
    try:
        mongo_client = AsyncIOMotorClient(MONGO_URL)
        db = mongo_client[DB_NAME]
        # Test connection
        await db.admin.command('ping')
        logger.info("Connected to MongoDB successfully")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        # Continue without database for basic functionality
        mongo_client = None
        db = None

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    logger.info("StockBreak Pro API started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    if mongo_client:
        mongo_client.close()
    logger.info("StockBreak Pro API shutdown")

# Utility functions
def get_ist_time():
    """Get current IST time"""
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist)

def is_market_open():
    """Check if NSE market is currently open"""
    now = get_ist_time()
    
    # Market is closed on weekends
    if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
        return False, "Market is closed (Weekend)"
    
    # Market hours: 9:15 AM to 3:30 PM IST
    market_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
    market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)
    pre_open_start = now.replace(hour=9, minute=0, second=0, microsecond=0)
    
    if now < pre_open_start:
        next_open = market_open.strftime("%Y-%m-%d %H:%M:%S IST")
        return False, f"Market opens at 9:15 AM IST. Next open: {next_open}"
    elif pre_open_start <= now < market_open:
        return False, "Pre-open session (9:00-9:15 AM IST)"
    elif market_open <= now <= market_close:
        time_to_close = int((market_close - now).total_seconds())
        return True, f"Market is open. Closes in {time_to_close//3600}h {(time_to_close%3600)//60}m"
    else:
        # Market closed for the day
        next_day = now + timedelta(days=1)
        # Skip weekends
        while next_day.weekday() >= 5:
            next_day += timedelta(days=1)
        next_open = next_day.replace(hour=9, minute=15, second=0, microsecond=0)
        return False, f"Market closed. Next open: {next_open.strftime('%Y-%m-%d %H:%M:%S IST')}"

def calculate_technical_indicators(df):
    """Calculate comprehensive technical indicators"""
    try:
        if df.empty or len(df) < 20:
            return {}
        
        # Price data
        close = df['Close']
        high = df['High']
        low = df['Low']
        volume = df['Volume']
        
        indicators = {}
        
        # Moving Averages
        indicators['sma_20'] = close.rolling(window=20).mean().iloc[-1] if len(close) >= 20 else None
        indicators['sma_50'] = close.rolling(window=50).mean().iloc[-1] if len(close) >= 50 else None
        indicators['sma_200'] = close.rolling(window=200).mean().iloc[-1] if len(close) >= 200 else None
        indicators['ema_12'] = close.ewm(span=12).mean().iloc[-1] if len(close) >= 12 else None
        indicators['ema_26'] = close.ewm(span=26).mean().iloc[-1] if len(close) >= 26 else None
        
        # RSI
        if len(close) >= 14:
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            indicators['rsi'] = (100 - (100 / (1 + rs))).iloc[-1]
        
        # MACD
        if indicators['ema_12'] and indicators['ema_26']:
            ema_12_series = close.ewm(span=12).mean()
            ema_26_series = close.ewm(span=26).mean()
            macd_line = ema_12_series - ema_26_series
            signal_line = macd_line.ewm(span=9).mean()
            indicators['macd'] = macd_line.iloc[-1]
            indicators['macd_signal'] = signal_line.iloc[-1]
            indicators['macd_histogram'] = (macd_line - signal_line).iloc[-1]
        
        # Bollinger Bands
        if len(close) >= 20:
            sma_20_series = close.rolling(window=20).mean()
            std_20 = close.rolling(window=20).std()
            indicators['bollinger_upper'] = (sma_20_series + (std_20 * 2)).iloc[-1]
            indicators['bollinger_middle'] = sma_20_series.iloc[-1]
            indicators['bollinger_lower'] = (sma_20_series - (std_20 * 2)).iloc[-1]
        
        # Stochastic Oscillator
        if len(close) >= 14:
            lowest_low = low.rolling(window=14).min()
            highest_high = high.rolling(window=14).max()
            k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
            indicators['stochastic_k'] = k_percent.iloc[-1]
            indicators['stochastic_d'] = k_percent.rolling(window=3).mean().iloc[-1]
        
        # VWAP (Volume Weighted Average Price)
        if len(volume) > 0 and volume.sum() > 0:
            typical_price = (high + low + close) / 3
            vwap = (typical_price * volume).cumsum() / volume.cumsum()
            indicators['vwap'] = vwap.iloc[-1]
        
        # ATR (Average True Range)
        if len(df) >= 14:
            high_low = high - low
            high_close = np.abs(high - close.shift())
            low_close = np.abs(low - close.shift())
            true_range = np.maximum(high_low, np.maximum(high_close, low_close))
            indicators['atr'] = true_range.rolling(window=14).mean().iloc[-1]
        
        # Support and Resistance levels
        recent_data = df.tail(50)  # Last 50 days
        indicators['support_level'] = recent_data['Low'].min()
        indicators['resistance_level'] = recent_data['High'].max()
        
        # Volume analysis
        avg_volume = volume.rolling(window=20).mean().iloc[-1] if len(volume) >= 20 else volume.mean()
        current_volume = volume.iloc[-1]
        indicators['volume_ratio'] = current_volume / avg_volume if avg_volume > 0 else 1.0
        
        return indicators
        
    except Exception as e:
        logger.error(f"Error calculating technical indicators: {e}")
        return {}

def detect_breakouts(df, indicators):
    """Detect various types of breakouts"""
    try:
        if df.empty or len(df) < 20:
            return []
        
        current_price = df['Close'].iloc[-1]
        breakouts = []
        
        # 200 DMA Breakout
        if indicators.get('sma_200') and current_price > indicators['sma_200'] * 1.02:
            confidence = min(0.9, (current_price - indicators['sma_200']) / indicators['sma_200'] * 10)
            breakouts.append({
                'type': '200_dma',
                'confidence': confidence,
                'breakout_price': indicators['sma_200'],
                'description': f"Price broke above 200 DMA at ₹{indicators['sma_200']:.2f}"
            })
        
        # Resistance Breakout
        if indicators.get('resistance_level') and current_price > indicators['resistance_level'] * 1.01:
            confidence = min(0.85, (current_price - indicators['resistance_level']) / indicators['resistance_level'] * 15)
            breakouts.append({
                'type': 'resistance',
                'confidence': confidence,
                'breakout_price': indicators['resistance_level'],
                'description': f"Price broke above resistance at ₹{indicators['resistance_level']:.2f}"
            })
        
        # Momentum Breakout (RSI > 60 with volume surge)
        if indicators.get('rsi') and indicators.get('volume_ratio'):
            if indicators['rsi'] > 60 and indicators['volume_ratio'] > 1.5:
                confidence = min(0.8, (indicators['rsi'] - 50) / 50 * indicators['volume_ratio'] / 2)
                breakouts.append({
                    'type': 'momentum',
                    'confidence': confidence,
                    'breakout_price': current_price,
                    'description': f"Momentum breakout with RSI {indicators['rsi']:.1f} and volume surge"
                })
        
        # Bollinger Upper Band Breakout
        if indicators.get('bollinger_upper') and current_price > indicators['bollinger_upper']:
            confidence = min(0.75, (current_price - indicators['bollinger_upper']) / indicators['bollinger_upper'] * 20)
            breakouts.append({
                'type': 'bollinger_upper',
                'confidence': confidence,
                'breakout_price': indicators['bollinger_upper'],
                'description': f"Price broke above Bollinger upper band at ₹{indicators['bollinger_upper']:.2f}"
            })
        
        # Stochastic Breakout
        if indicators.get('stochastic_k') and indicators.get('stochastic_d'):
            if indicators['stochastic_k'] > 80 and indicators['stochastic_k'] > indicators['stochastic_d']:
                confidence = min(0.7, indicators['stochastic_k'] / 100)
                breakouts.append({
                    'type': 'stochastic',
                    'confidence': confidence,
                    'breakout_price': current_price,
                    'description': f"Stochastic overbought breakout (%K: {indicators['stochastic_k']:.1f})"
                })
        
        return breakouts
        
    except Exception as e:
        logger.error(f"Error detecting breakouts: {e}")
        return []

def calculate_trading_recommendation(current_price, indicators, breakout_data, risk_assessment):
    """Calculate professional trading recommendations"""
    try:
        if not breakout_data:
            return None
        
        # Get the highest confidence breakout
        best_breakout = max(breakout_data, key=lambda x: x['confidence'])
        
        # Calculate entry price (slightly above current price)
        entry_price = current_price * 1.005  # 0.5% above current price
        
        # Calculate stop loss based on ATR and support
        atr = indicators.get('atr', current_price * 0.02)  # Default 2% if ATR not available
        support_level = indicators.get('support_level', current_price * 0.95)
        
        # Use the lower of ATR-based stop or support level
        atr_stop = current_price - (atr * 2)  # 2x ATR below current price
        stop_loss = max(atr_stop, support_level * 0.98)  # 2% below support
        
        # Calculate target price (risk-reward ratio between 1:2 to 1:3)
        risk_amount = entry_price - stop_loss
        risk_reward_ratio = 2.5 + (best_breakout['confidence'] * 1.5)  # 2.5 to 4.0 based on confidence
        target_price = entry_price + (risk_amount * risk_reward_ratio)
        
        # Determine action based on confidence and risk
        confidence = best_breakout['confidence']
        risk_score = risk_assessment.get('risk_score', 5.0)
        
        if confidence >= 0.8 and risk_score <= 6:
            action = "BUY"
        elif confidence >= 0.6 and risk_score <= 7:
            action = "BUY"
        elif confidence >= 0.5:
            action = "WAIT"
        else:
            action = "AVOID"
        
        # Calculate position size (3-15% based on confidence and risk)
        base_position = 5.0  # Base 5%
        confidence_bonus = confidence * 8  # Up to 8% bonus for high confidence
        risk_penalty = (risk_score - 5) * 1.5  # Reduce for higher risk
        position_size = max(3.0, min(15.0, base_position + confidence_bonus - risk_penalty))
        
        return TradingRecommendation(
            entry_price=round(entry_price, 2),
            stop_loss=round(stop_loss, 2),
            target_price=round(target_price, 2),
            risk_reward_ratio=round(risk_reward_ratio, 1),
            position_size_percent=round(position_size, 1),
            action=action,
            entry_rationale=f"Breakout above {best_breakout['type'].replace('_', ' ')} with {confidence*100:.0f}% confidence",
            stop_loss_rationale=f"ATR-based stop loss with support at ₹{support_level:.2f}"
        )
        
    except Exception as e:
        logger.error(f"Error calculating trading recommendation: {e}")
        return None

def calculate_risk_assessment(df, indicators):
    """Calculate comprehensive risk assessment"""
    try:
        if df.empty:
            return {"risk_level": "High", "risk_score": 8.0, "risk_factors": ["Insufficient data"]}
        
        risk_factors = []
        risk_score = 5.0  # Base risk score
        
        # Volatility analysis
        returns = df['Close'].pct_change().dropna()
        volatility = returns.std() * np.sqrt(252)  # Annualized volatility
        
        if volatility > 0.4:  # 40% annual volatility
            risk_score += 2
            risk_factors.append("High volatility (>40% annually)")
        elif volatility > 0.25:  # 25% annual volatility
            risk_score += 1
            risk_factors.append("Moderate volatility")
        
        # RSI analysis
        rsi = indicators.get('rsi')
        if rsi:
            if rsi > 80:
                risk_score += 1.5
                risk_factors.append("Extremely overbought (RSI > 80)")
            elif rsi > 70:
                risk_score += 0.5
                risk_factors.append("Overbought conditions (RSI > 70)")
        
        # Volume analysis
        volume_ratio = indicators.get('volume_ratio', 1.0)
        if volume_ratio < 0.5:
            risk_score += 1
            risk_factors.append("Low volume support")
        
        # Price vs moving averages
        current_price = df['Close'].iloc[-1]
        sma_200 = indicators.get('sma_200')
        if sma_200 and current_price < sma_200:
            risk_score += 1
            risk_factors.append("Trading below 200 DMA")
        
        # Determine risk level
        if risk_score <= 3:
            risk_level = "Low"
        elif risk_score <= 6:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        # Calculate beta (simplified)
        if len(returns) >= 50:
            # Simplified beta calculation (assuming market return of 12%)
            market_return = 0.12 / 252  # Daily market return
            beta = returns.cov(pd.Series([market_return] * len(returns))) / (market_return ** 2)
        else:
            beta = 1.0
        
        return {
            "risk_level": risk_level,
            "risk_score": round(min(10.0, risk_score), 1),
            "risk_factors": risk_factors,
            "volatility": volatility,
            "beta": beta
        }
        
    except Exception as e:
        logger.error(f"Error calculating risk assessment: {e}")
        return {"risk_level": "Medium", "risk_score": 5.0, "risk_factors": ["Risk calculation error"]}

async def get_stock_data(symbol: str):
    """Get comprehensive stock data with error handling"""
    try:
        # Add .NS suffix for NSE stocks
        yahoo_symbol = f"{symbol}.NS"
        
        # Get stock info
        stock = yf.Ticker(yahoo_symbol)
        
        # Get historical data (1 year for comprehensive analysis)
        hist = stock.history(period="1y")
        if hist.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        
        # Get current price and change
        current_price = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        change_percent = ((current_price - prev_close) / prev_close) * 100
        
        # Calculate technical indicators
        indicators = calculate_technical_indicators(hist)
        
        # Detect breakouts
        breakouts = detect_breakouts(hist, indicators)
        
        # Calculate risk assessment
        risk_assessment = calculate_risk_assessment(hist, indicators)
        
        # Get stock info
        info = stock.info
        
        # Calculate trading recommendation
        trading_recommendation = None
        if breakouts:
            trading_recommendation = calculate_trading_recommendation(
                current_price, indicators, breakouts, risk_assessment
            )
        
        # Get fundamental data
        fundamental_data = {
            "market_cap": info.get('marketCap'),
            "pe_ratio": info.get('trailingPE'),
            "pb_ratio": info.get('priceToBook'),
            "eps": info.get('trailingEps'),
            "book_value": info.get('bookValue'),
            "roe": info.get('returnOnEquity'),
            "debt_to_equity": info.get('debtToEquity'),
            "dividend_yield": info.get('dividendYield'),
            "earnings_growth": info.get('earningsGrowth')
        }
        
        # Get stock metadata
        stock_info = NSE_STOCK_UNIVERSE.get(symbol, {})
        
        return {
            "symbol": symbol,
            "name": stock_info.get("name", info.get('longName', symbol)),
            "sector": stock_info.get("sector", info.get('sector', 'Unknown')),
            "current_price": round(current_price, 2),
            "change_percent": round(change_percent, 2),
            "volume": int(hist['Volume'].iloc[-1]) if not hist['Volume'].empty else 0,
            "market_cap": fundamental_data["market_cap"],
            "technical_indicators": indicators,
            "fundamental_data": fundamental_data,
            "risk_assessment": risk_assessment,
            "breakout_data": breakouts[0] if breakouts else None,
            "trading_recommendation": trading_recommendation.dict() if trading_recommendation else None,
            "data_validation": {
                "source": "Yahoo Finance Real-time",
                "timestamp": get_ist_time().strftime("%Y-%m-%d %H:%M:%S IST"),
                "data_age_warning": None
            }
        }
        
    except Exception as e:
        logger.error(f"Error fetching stock data for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch data for {symbol}: {str(e)}")

# API Routes

@app.get("/api/")
async def root():
    """API root endpoint"""
    return {
        "message": "StockBreak Pro API v2.0",
        "status": "active",
        "timestamp": get_ist_time().isoformat(),
        "market_status": is_market_open()[1]
    }

@app.get("/api/stocks/symbols")
async def get_nse_symbols():
    """Get all NSE stock symbols with sectors"""
    try:
        symbols = list(NSE_STOCK_UNIVERSE.keys())
        symbols_with_sectors = {
            symbol: data for symbol, data in NSE_STOCK_UNIVERSE.items()
        }
        
        # Get unique sectors
        sectors = list(set(data["sector"] for data in NSE_STOCK_UNIVERSE.values()))
        sectors.sort()
        
        return {
            "symbols": symbols,
            "symbols_with_sectors": symbols_with_sectors,
            "count": len(symbols),
            "sectors": sectors,
            "last_updated": get_ist_time().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting NSE symbols: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch NSE symbols")

@app.get("/api/stocks/search")
async def search_stocks(q: str = Query(..., min_length=1)):
    """Search stocks by symbol or name"""
    try:
        query = q.upper().strip()
        results = []
        
        for symbol, data in NSE_STOCK_UNIVERSE.items():
            if query in symbol or query in data["name"].upper():
                results.append({
                    "symbol": symbol,
                    "name": data["name"],
                    "sector": data["sector"]
                })
        
        return {
            "query": q,
            "results": results[:20],  # Limit to 20 results
            "total_found": len(results)
        }
        
    except Exception as e:
        logger.error(f"Error searching stocks: {e}")
        raise HTTPException(status_code=500, detail="Search failed")

@app.get("/api/stocks/{symbol}")
async def get_stock_details(symbol: str):
    """Get detailed stock information"""
    symbol = symbol.upper()
    if symbol not in NSE_STOCK_UNIVERSE:
        raise HTTPException(status_code=404, detail=f"Stock symbol {symbol} not found in NSE universe")
    
    return await get_stock_data(symbol)

@app.get("/api/stocks/{symbol}/validate")
async def validate_stock_data(symbol: str):
    """Validate stock data quality and freshness"""
    try:
        symbol = symbol.upper()
        if symbol not in NSE_STOCK_UNIVERSE:
            raise HTTPException(status_code=404, detail=f"Stock symbol {symbol} not found")
        
        # Get data from Yahoo Finance
        yahoo_symbol = f"{symbol}.NS"
        stock = yf.Ticker(yahoo_symbol)
        hist = stock.history(period="1d")
        
        if hist.empty:
            return {
                "symbol": symbol,
                "validation_timestamp": get_ist_time().isoformat(),
                "data_quality_score": 0,
                "quality_level": "Failed",
                "warnings": ["No data available from Yahoo Finance"],
                "yahoo_finance": None
            }
        
        current_price = hist['Close'].iloc[-1]
        volume = hist['Volume'].iloc[-1]
        
        # Calculate data quality score
        quality_score = 100
        warnings = []
        
        # Check data freshness
        last_update = hist.index[-1]
        now = datetime.now()
        data_age_hours = (now - last_update.to_pydatetime().replace(tzinfo=None)).total_seconds() / 3600
        
        if data_age_hours > 24:
            quality_score -= 30
            warnings.append(f"Data is {data_age_hours:.1f} hours old")
        elif data_age_hours > 4:
            quality_score -= 15
            warnings.append(f"Data is {data_age_hours:.1f} hours old")
        
        # Check volume
        if volume == 0:
            quality_score -= 20
            warnings.append("Zero volume reported")
        
        # Check price validity
        if current_price <= 0:
            quality_score -= 50
            warnings.append("Invalid price data")
        
        # Determine quality level
        if quality_score >= 90:
            quality_level = "Excellent"
        elif quality_score >= 75:
            quality_level = "Good"
        elif quality_score >= 60:
            quality_level = "Fair"
        elif quality_score >= 40:
            quality_level = "Poor"
        else:
            quality_level = "Failed"
        
        return {
            "symbol": symbol,
            "validation_timestamp": get_ist_time().isoformat(),
            "data_quality_score": max(0, quality_score),
            "quality_level": quality_level,
            "warnings": warnings,
            "yahoo_finance": {
                "current_price": round(current_price, 2),
                "volume": int(volume),
                "last_update": last_update.isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Error validating stock data for {symbol}: {e}")
        return {
            "symbol": symbol,
            "validation_timestamp": get_ist_time().isoformat(),
            "data_quality_score": 0,
            "quality_level": "Failed",
            "warnings": [f"Validation error: {str(e)}"],
            "yahoo_finance": None
        }

@app.get("/api/stocks/{symbol}/chart")
async def get_stock_chart(symbol: str, timeframe: str = "1mo"):
    """Get stock chart data for different timeframes"""
    try:
        symbol = symbol.upper()
        if symbol not in NSE_STOCK_UNIVERSE:
            raise HTTPException(status_code=404, detail=f"Stock symbol {symbol} not found")
        
        # Validate timeframe
        valid_timeframes = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y"]
        if timeframe not in valid_timeframes:
            timeframe = "1mo"
        
        yahoo_symbol = f"{symbol}.NS"
        stock = yf.Ticker(yahoo_symbol)
        hist = stock.history(period=timeframe)
        
        if hist.empty:
            raise HTTPException(status_code=404, detail=f"No chart data found for {symbol}")
        
        # Calculate indicators for the chart
        indicators = calculate_technical_indicators(hist)
        
        # Format chart data
        chart_data = []
        for date, row in hist.iterrows():
            chart_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "open": round(row['Open'], 2),
                "high": round(row['High'], 2),
                "low": round(row['Low'], 2),
                "close": round(row['Close'], 2),
                "volume": int(row['Volume'])
            })
        
        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "data": chart_data,
            "indicators": indicators,
            "data_points": len(chart_data)
        }
        
    except Exception as e:
        logger.error(f"Error fetching chart data for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch chart data: {str(e)}")

@app.get("/api/stocks/breakouts/scan")
async def scan_breakouts(
    sector: Optional[str] = None,
    min_confidence: float = 0.5,
    risk_level: Optional[str] = None,
    limit: int = 100
):
    """Scan for breakout opportunities across NSE stocks"""
    try:
        logger.info(f"Starting breakout scan with filters - Sector: {sector}, Min Confidence: {min_confidence}, Risk: {risk_level}, Limit: {limit}")
        
        # Get symbols to scan
        symbols_to_scan = list(NSE_STOCK_UNIVERSE.keys())
        
        # Filter by sector if specified
        if sector and sector != "All":
            symbols_to_scan = [
                symbol for symbol, data in NSE_STOCK_UNIVERSE.items()
                if data["sector"] == sector
            ]
        
        # Limit the scan for performance
        symbols_to_scan = symbols_to_scan[:min(limit, 300)]  # Cap at 300 for performance
        
        breakout_stocks = []
        total_scanned = 0
        
        # Scan stocks for breakouts
        for symbol in symbols_to_scan:
            try:
                total_scanned += 1
                logger.info(f"Scanning {symbol} ({total_scanned}/{len(symbols_to_scan)})")
                
                stock_data = await get_stock_data(symbol)
                
                # Check if stock has breakout
                if stock_data.get("breakout_data"):
                    confidence = stock_data["breakout_data"]["confidence"]
                    
                    # Apply confidence filter
                    if confidence >= min_confidence:
                        # Apply risk filter if specified
                        if risk_level and risk_level != "All":
                            stock_risk = stock_data["risk_assessment"]["risk_level"]
                            if stock_risk != risk_level:
                                continue
                        
                        # Create breakout stock object
                        breakout_stock = BreakoutStock(
                            symbol=stock_data["symbol"],
                            name=stock_data["name"],
                            current_price=stock_data["current_price"],
                            change_percent=stock_data["change_percent"],
                            breakout_type=stock_data["breakout_data"]["type"],
                            confidence_score=confidence,
                            sector=stock_data["sector"],
                            trading_recommendation=stock_data["trading_recommendation"],
                            technical_data=stock_data["technical_indicators"],
                            risk_assessment=stock_data["risk_assessment"]
                        )
                        
                        breakout_stocks.append(breakout_stock.dict())
                
                # Add small delay to avoid rate limiting
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error scanning {symbol}: {e}")
                continue
        
        # Sort by confidence score
        breakout_stocks.sort(key=lambda x: x["confidence_score"], reverse=True)
        
        logger.info(f"Breakout scan completed. Found {len(breakout_stocks)} breakouts from {total_scanned} stocks")
        
        return {
            "breakout_stocks": breakout_stocks,
            "breakouts_found": len(breakout_stocks),
            "total_scanned": total_scanned,
            "scan_timestamp": get_ist_time().isoformat(),
            "filters_applied": {
                "sector": sector,
                "min_confidence": min_confidence,
                "risk_level": risk_level
            }
        }
        
    except Exception as e:
        logger.error(f"Error during breakout scan: {e}")
        raise HTTPException(status_code=500, detail=f"Breakout scan failed: {str(e)}")

@app.get("/api/stocks/market-overview")
async def get_market_overview():
    """Get comprehensive market overview"""
    try:
        # Get NIFTY 50 data
        nifty = yf.Ticker("^NSEI")
        nifty_hist = nifty.history(period="1d")
        
        if not nifty_hist.empty:
            nifty_current = nifty_hist['Close'].iloc[-1]
            nifty_prev = nifty_hist['Close'].iloc[-2] if len(nifty_hist) > 1 else nifty_current
            nifty_change = ((nifty_current - nifty_prev) / nifty_prev) * 100
        else:
            nifty_current = 24000  # Fallback value
            nifty_change = 0
        
        # Market status
        is_open, status_message = is_market_open()
        current_time = get_ist_time()
        
        market_status = {
            "status": "OPEN" if is_open else ("PRE_OPEN" if "Pre-open" in status_message else "CLOSED"),
            "message": status_message,
            "current_time": current_time.strftime("%Y-%m-%d %H:%M:%S IST"),
            "is_trading_hours": is_open
        }
        
        # Add time-specific information
        if is_open:
            market_close = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            time_to_close = int((market_close - current_time).total_seconds())
            market_status["time_to_close"] = time_to_close
        else:
            # Calculate next market open
            next_day = current_time + timedelta(days=1)
            while next_day.weekday() >= 5:  # Skip weekends
                next_day += timedelta(days=1)
            next_open = next_day.replace(hour=9, minute=15, second=0, microsecond=0)
            market_status["next_open"] = next_open.strftime("%Y-%m-%d %H:%M:%S IST")
        
        # Calculate market sentiment (simplified)
        sentiment = "Neutral"
        if nifty_change > 1:
            sentiment = "Bullish"
        elif nifty_change < -1:
            sentiment = "Bearish"
        
        # Sector performance (mock data - in production, calculate from actual sector indices)
        sector_performance = {
            "IT": round(np.random.uniform(-2, 3), 2),
            "Banking": round(np.random.uniform(-1.5, 2.5), 2),
            "Auto": round(np.random.uniform(-2, 2), 2),
            "Pharma": round(np.random.uniform(-1, 2), 2),
            "FMCG": round(np.random.uniform(-0.5, 1.5), 2)
        }
        
        return {
            "nifty_50": {
                "current": round(nifty_current, 2),
                "change_percent": round(nifty_change, 2)
            },
            "market_status": market_status,
            "market_sentiment": sentiment,
            "sector_performance": sector_performance,
            "timestamp": get_ist_time().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching market overview: {e}")
        # Return fallback data
        return {
            "nifty_50": {"current": 24000, "change_percent": 0},
            "market_status": {
                "status": "UNKNOWN",
                "message": "Unable to fetch market status",
                "current_time": get_ist_time().strftime("%Y-%m-%d %H:%M:%S IST"),
                "is_trading_hours": False
            },
            "market_sentiment": "Neutral",
            "timestamp": get_ist_time().isoformat()
        }

# Watchlist endpoints
@app.get("/api/watchlist")
async def get_watchlist():
    """Get user's watchlist"""
    try:
        if not db:
            return {"watchlist": [], "message": "Database not available"}
        
        watchlist_collection = db.watchlist
        watchlist_items = await watchlist_collection.find().to_list(length=100)
        
        # Convert ObjectId to string and format
        watchlist = []
        for item in watchlist_items:
            watchlist.append({
                "symbol": item["symbol"],
                "added_at": item["added_at"].isoformat() if isinstance(item["added_at"], datetime) else item["added_at"]
            })
        
        return {"watchlist": watchlist}
        
    except Exception as e:
        logger.error(f"Error fetching watchlist: {e}")
        return {"watchlist": [], "error": str(e)}

@app.post("/api/watchlist")
async def add_to_watchlist(symbol: str = Query(...)):
    """Add stock to watchlist"""
    try:
        symbol = symbol.upper()
        if symbol not in NSE_STOCK_UNIVERSE:
            raise HTTPException(status_code=404, detail=f"Stock symbol {symbol} not found")
        
        if not db:
            raise HTTPException(status_code=503, detail="Database not available")
        
        watchlist_collection = db.watchlist
        
        # Check if already in watchlist
        existing = await watchlist_collection.find_one({"symbol": symbol})
        if existing:
            return {"message": f"{symbol} is already in watchlist"}
        
        # Add to watchlist
        await watchlist_collection.insert_one({
            "symbol": symbol,
            "added_at": get_ist_time()
        })
        
        return {"message": f"Added {symbol} to watchlist"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding to watchlist: {e}")
        raise HTTPException(status_code=500, detail="Failed to add to watchlist")

@app.delete("/api/watchlist/{symbol}")
async def remove_from_watchlist(symbol: str):
    """Remove stock from watchlist"""
    try:
        symbol = symbol.upper()
        
        if not db:
            raise HTTPException(status_code=503, detail="Database not available")
        
        watchlist_collection = db.watchlist
        result = await watchlist_collection.delete_one({"symbol": symbol})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"{symbol} not found in watchlist")
        
        return {"message": f"Removed {symbol} from watchlist"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing from watchlist: {e}")
        raise HTTPException(status_code=500, detail="Failed to remove from watchlist")

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db_status = "connected" if db else "disconnected"
        if db:
            try:
                await db.admin.command('ping')
                db_status = "connected"
            except:
                db_status = "error"
        
        # Check market data availability
        try:
            nifty = yf.Ticker("^NSEI")
            nifty_hist = nifty.history(period="1d")
            data_status = "available" if not nifty_hist.empty else "unavailable"
        except:
            data_status = "error"
        
        return {
            "status": "healthy",
            "timestamp": get_ist_time().isoformat(),
            "database": db_status,
            "market_data": data_status,
            "total_stocks": len(NSE_STOCK_UNIVERSE),
            "version": "2.0.0"
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": get_ist_time().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)