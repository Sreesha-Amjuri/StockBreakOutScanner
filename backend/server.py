from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
import yfinance as yf
import pandas as pd
import numpy as np
import asyncio
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Thread pool for blocking operations
executor = ThreadPoolExecutor(max_workers=10)

# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

class StockData(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    symbol: str
    name: str
    current_price: float
    change_percent: float
    volume: int
    market_cap: Optional[float] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TechnicalIndicators(BaseModel):
    symbol: str
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    rsi: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    volume_ratio: Optional[float] = None
    breakout_level: Optional[float] = None
    support_level: Optional[float] = None
    resistance_level: Optional[float] = None
    pattern: Optional[str] = None

class FundamentalData(BaseModel):
    symbol: str
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    roe: Optional[float] = None
    roce: Optional[float] = None
    debt_to_equity: Optional[float] = None
    promoter_holding: Optional[float] = None
    earnings_growth: Optional[float] = None
    revenue_growth: Optional[float] = None
    dividend_yield: Optional[float] = None

class BreakoutStock(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    symbol: str
    name: str
    current_price: float
    breakout_price: float
    breakout_type: str  # "200_dma", "resistance", "pattern"
    confidence_score: float
    technical_data: TechnicalIndicators
    fundamental_data: Optional[FundamentalData] = None
    reason: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# NSE stock symbols (top 100 liquid stocks)
NSE_SYMBOLS = [
    "RELIANCE", "TCS", "HDFCBANK", "BHARTIARTL", "ICICIBANK", "INFOSYS", 
    "SBIN", "LICI", "HINDUNILVR", "ITC", "LT", "AXISBANK", "KOTAKBANK",
    "BAJFINANCE", "ASIANPAINT", "NESTLEIND", "MARUTI", "HCLTECH", "SUNPHARMA",
    "TITAN", "WIPRO", "ULTRACEMCO", "ONGC", "NTPC", "POWERGRID", "M&M",
    "TECHM", "TATAMOTORS", "COALINDIA", "BAJAJFINSV", "ADANIENTS", "HDFCLIFE",
    "SBILIFE", "JSWSTEEL", "TATACONSUM", "IOC", "BAJAJ-AUTO", "GRASIM",
    "HINDALCO", "BRITANNIA", "APOLLOHOSP", "CIPLA", "DIVISLAB", "DRREDDY",
    "EICHERMOT", "HEROMOTOCO", "INDUSINDBK", "SHREECEM", "TATASTEEL",
    "GODREJCP", "VEDL", "BPCL", "ADANIPORTS", "PIDILITIND", "PAGEIND"
]

def calculate_technical_indicators(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate technical indicators for a stock"""
    try:
        # Simple Moving Averages
        sma_20 = df['Close'].rolling(window=20).mean().iloc[-1] if len(df) >= 20 else None
        sma_50 = df['Close'].rolling(window=50).mean().iloc[-1] if len(df) >= 50 else None
        sma_200 = df['Close'].rolling(window=200).mean().iloc[-1] if len(df) >= 200 else None
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1] if len(df) >= 14 else None
        
        # MACD
        exp1 = df['Close'].ewm(span=12).mean()
        exp2 = df['Close'].ewm(span=26).mean()
        macd = (exp1 - exp2).iloc[-1] if len(df) >= 26 else None
        signal = (exp1 - exp2).ewm(span=9).mean().iloc[-1] if len(df) >= 35 else None
        
        # Volume analysis
        avg_volume = df['Volume'].rolling(window=20).mean().iloc[-1] if len(df) >= 20 else None
        current_volume = df['Volume'].iloc[-1]
        volume_ratio = current_volume / avg_volume if avg_volume and avg_volume > 0 else None
        
        # Support and Resistance
        high_20 = df['High'].rolling(window=20).max().iloc[-1] if len(df) >= 20 else None
        low_20 = df['Low'].rolling(window=20).min().iloc[-1] if len(df) >= 20 else None
        
        return {
            "sma_20": float(sma_20) if sma_20 and not pd.isna(sma_20) else None,
            "sma_50": float(sma_50) if sma_50 and not pd.isna(sma_50) else None,
            "sma_200": float(sma_200) if sma_200 and not pd.isna(sma_200) else None,
            "rsi": float(rsi) if rsi and not pd.isna(rsi) else None,
            "macd": float(macd) if macd and not pd.isna(macd) else None,
            "macd_signal": float(signal) if signal and not pd.isna(signal) else None,
            "volume_ratio": float(volume_ratio) if volume_ratio and not pd.isna(volume_ratio) else None,
            "resistance_level": float(high_20) if high_20 and not pd.isna(high_20) else None,
            "support_level": float(low_20) if low_20 and not pd.isna(low_20) else None,
        }
    except Exception as e:
        logger.error(f"Error calculating technical indicators: {str(e)}")
        return {}

def detect_breakout(symbol: str, df: pd.DataFrame, technical_data: Dict) -> Optional[Dict]:
    """Detect if a stock is showing breakout signals"""
    try:
        current_price = df['Close'].iloc[-1]
        
        # Check for 200 DMA breakout
        if technical_data.get('sma_200'):
            if current_price > technical_data['sma_200'] * 1.02:  # 2% above 200 DMA
                if technical_data.get('volume_ratio', 0) > 1.5:  # High volume
                    return {
                        "type": "200_dma",
                        "breakout_price": technical_data['sma_200'],
                        "confidence": 0.8
                    }
        
        # Check for resistance breakout
        if technical_data.get('resistance_level'):
            if current_price > technical_data['resistance_level'] * 1.01:
                if technical_data.get('volume_ratio', 0) > 1.3:
                    return {
                        "type": "resistance",
                        "breakout_price": technical_data['resistance_level'],
                        "confidence": 0.7
                    }
        
        # Check for RSI and MACD confirmation
        rsi = technical_data.get('rsi', 0)
        macd = technical_data.get('macd', 0)
        macd_signal = technical_data.get('macd_signal', 0)
        
        if 50 < rsi < 80 and macd > macd_signal:
            if current_price > technical_data.get('sma_50', 0):
                return {
                    "type": "momentum",
                    "breakout_price": technical_data.get('sma_50', current_price),
                    "confidence": 0.6
                }
        
        return None
    except Exception as e:
        logger.error(f"Error detecting breakout for {symbol}: {str(e)}")
        return None

async def fetch_stock_data(symbol: str) -> Optional[Dict]:
    """Fetch stock data using yfinance"""
    try:
        # Add .NS suffix for NSE stocks
        ticker_symbol = f"{symbol}.NS"
        
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        
        def get_stock_info():
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period="1y")  # Get 1 year of data
            info = ticker.info
            return hist, info
        
        hist, info = await loop.run_in_executor(executor, get_stock_info)
        
        if hist.empty:
            return None
            
        current_price = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        change_percent = ((current_price - prev_close) / prev_close) * 100
        
        technical_indicators = calculate_technical_indicators(hist)
        breakout_data = detect_breakout(symbol, hist, technical_indicators)
        
        return {
            "symbol": symbol,
            "name": info.get('longName', symbol),
            "current_price": float(current_price),
            "change_percent": float(change_percent),
            "volume": int(hist['Volume'].iloc[-1]),
            "market_cap": info.get('marketCap'),
            "technical_indicators": technical_indicators,
            "breakout_data": breakout_data,
            "info": info
        }
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {str(e)}")
        return None

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Indian Stock Breakout Screener API"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

@api_router.get("/stocks/symbols")
async def get_nse_symbols():
    """Get list of NSE symbols being tracked"""
    return {"symbols": NSE_SYMBOLS, "count": len(NSE_SYMBOLS)}

@api_router.get("/stocks/{symbol}")
async def get_stock_data(symbol: str):
    """Get detailed data for a specific stock"""
    symbol = symbol.upper()
    stock_data = await fetch_stock_data(symbol)
    
    if not stock_data:
        raise HTTPException(status_code=404, detail=f"Stock data not found for {symbol}")
    
    return stock_data

@api_router.get("/stocks/breakouts/scan")
async def scan_breakout_stocks():
    """Scan NSE stocks for breakout opportunities"""
    breakout_stocks = []
    
    # Limit to first 20 stocks for demo to avoid timeout
    symbols_to_scan = NSE_SYMBOLS[:20]
    
    # Fetch data for all symbols concurrently
    tasks = [fetch_stock_data(symbol) for symbol in symbols_to_scan]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, dict) and result.get('breakout_data'):
            symbol = symbols_to_scan[i]
            breakout_data = result['breakout_data']
            technical_indicators = result['technical_indicators']
            
            # Create breakout stock entry
            breakout_stock = {
                "symbol": symbol,
                "name": result['name'],
                "current_price": result['current_price'],
                "breakout_price": breakout_data['breakout_price'],
                "breakout_type": breakout_data['type'],
                "confidence_score": breakout_data['confidence'],
                "change_percent": result['change_percent'],
                "volume": result['volume'],
                "technical_data": technical_indicators,
                "reason": f"Breakout above {breakout_data['type']} level with {breakout_data['confidence']*100:.0f}% confidence"
            }
            
            breakout_stocks.append(breakout_stock)
    
    # Sort by confidence score
    breakout_stocks.sort(key=lambda x: x['confidence_score'], reverse=True)
    
    return {
        "breakout_stocks": breakout_stocks,
        "total_scanned": len(symbols_to_scan),
        "breakouts_found": len(breakout_stocks),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@api_router.get("/stocks/market-overview")
async def get_market_overview():
    """Get market overview with key indices"""
    try:
        # Fetch NIFTY 50 data
        nifty_data = await fetch_stock_data("^NSEI")
        
        return {
            "nifty_50": {
                "current": nifty_data['current_price'] if nifty_data else 0,
                "change_percent": nifty_data['change_percent'] if nifty_data else 0
            },
            "market_status": "Open" if datetime.now().hour < 16 else "Closed",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching market overview: {str(e)}")
        return {
            "nifty_50": {"current": 0, "change_percent": 0},
            "market_status": "Unknown",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    executor.shutdown(wait=True)