from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks, Depends
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import pytz
import yfinance as yf
import pandas as pd
import numpy as np
import asyncio
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import json


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
executor = ThreadPoolExecutor(max_workers=15)

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
    ema_12: Optional[float] = None
    ema_26: Optional[float] = None
    rsi: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    bollinger_upper: Optional[float] = None
    bollinger_lower: Optional[float] = None
    bollinger_middle: Optional[float] = None
    stochastic_k: Optional[float] = None
    stochastic_d: Optional[float] = None
    vwap: Optional[float] = None
    atr: Optional[float] = None
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
    market_cap: Optional[float] = None
    book_value: Optional[float] = None
    eps: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None

class RiskAssessment(BaseModel):
    symbol: str
    risk_score: float  # 1-10 scale
    volatility: Optional[float] = None
    beta: Optional[float] = None
    risk_factors: List[str] = []
    risk_level: str  # Low, Medium, High

class TradingRecommendation(BaseModel):
    entry_price: float
    stop_loss: float
    target_price: float
    risk_reward_ratio: float
    position_size_percent: float  # Suggested position size as % of portfolio
    action: str  # "BUY", "WAIT", "AVOID"
    entry_rationale: str
    stop_loss_rationale: str

class BreakoutStock(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    symbol: str
    name: str
    current_price: float
    breakout_price: float
    breakout_type: str  # "200_dma", "resistance", "pattern", "momentum"
    confidence_score: float
    technical_data: TechnicalIndicators
    fundamental_data: Optional[FundamentalData] = None
    risk_assessment: Optional[RiskAssessment] = None
    trading_recommendation: Optional[TradingRecommendation] = None
    reason: str
    sector: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class WatchlistItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    symbol: str
    name: str
    added_price: float
    target_price: Optional[float] = None
    stop_loss: Optional[float] = None
    notes: Optional[str] = None
    added_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChartData(BaseModel):
    symbol: str
    timeframe: str  # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y
    data: List[Dict[str, Any]]
    indicators: Dict[str, List[float]]

class AlertRequest(BaseModel):
    symbol: str
    price: float
    condition: str  # "above", "below"
    email: Optional[str] = None

# NSE stock symbols with sectors
NSE_SYMBOLS = {
    # IT Sector
    "TCS": "IT", "INFOSYS": "IT", "HCLTECH": "IT", "WIPRO": "IT", "TECHM": "IT",
    "LTIM": "IT", "PERSISTENT": "IT", "MPHASIS": "IT", "LTTS": "IT",
    
    # Banking & Financial
    "HDFCBANK": "Banking", "ICICIBANK": "Banking", "SBIN": "Banking", "AXISBANK": "Banking",
    "KOTAKBANK": "Banking", "INDUSINDBK": "Banking", "BAJFINANCE": "Finance",
    "BAJAJFINSV": "Finance", "HDFCLIFE": "Insurance", "SBILIFE": "Insurance", "LICI": "Insurance",
    
    # FMCG
    "HINDUNILVR": "FMCG", "ITC": "FMCG", "NESTLEIND": "FMCG", "BRITANNIA": "FMCG",
    "TATACONSUM": "FMCG", "GODREJCP": "FMCG", "MARICO": "FMCG", "DABUR": "FMCG",
    
    # Auto
    "MARUTI": "Auto", "TATAMOTORS": "Auto", "M&M": "Auto", "BAJAJ-AUTO": "Auto",
    "EICHERMOT": "Auto", "HEROMOTOCO": "Auto", "TVSMOTORS": "Auto",
    
    # Pharma
    "SUNPHARMA": "Pharma", "DRREDDY": "Pharma", "CIPLA": "Pharma", "DIVISLAB": "Pharma",
    "APOLLOHOSP": "Healthcare", "FORTIS": "Healthcare",
    
    # Energy & Power
    "RELIANCE": "Energy", "ONGC": "Energy", "IOC": "Energy", "BPCL": "Energy",
    "NTPC": "Power", "POWERGRID": "Power", "COALINDIA": "Mining",
    
    # Metals & Mining
    "TATASTEEL": "Metals", "JSWSTEEL": "Metals", "HINDALCO": "Metals", "VEDL": "Metals",
    "SAIL": "Metals", "NMDC": "Mining",
    
    # Cement
    "ULTRACEMCO": "Cement", "SHREECEM": "Cement", "GRASIM": "Cement", "RAMCOCEM": "Cement",
    
    # Telecom
    "BHARTIARTL": "Telecom", "IDEA": "Telecom",
    
    # Others
    "LT": "Infrastructure", "ASIANPAINT": "Paints", "TITAN": "Jewelry",
    "PIDILITIND": "Chemicals", "PAGEIND": "FMCG", "ADANIPORTS": "Infrastructure",
    "ADANIENTS": "Diversified"
}

def calculate_advanced_technical_indicators(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate comprehensive technical indicators"""
    try:
        indicators = {}
        
        # Basic Moving Averages
        indicators['sma_20'] = df['Close'].rolling(window=20).mean().iloc[-1] if len(df) >= 20 else None
        indicators['sma_50'] = df['Close'].rolling(window=50).mean().iloc[-1] if len(df) >= 50 else None
        indicators['sma_200'] = df['Close'].rolling(window=200).mean().iloc[-1] if len(df) >= 200 else None
        
        # Exponential Moving Averages
        indicators['ema_12'] = df['Close'].ewm(span=12).mean().iloc[-1] if len(df) >= 12 else None
        indicators['ema_26'] = df['Close'].ewm(span=26).mean().iloc[-1] if len(df) >= 26 else None
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        indicators['rsi'] = 100 - (100 / (1 + rs)).iloc[-1] if len(df) >= 14 else None
        
        # MACD
        if indicators['ema_12'] and indicators['ema_26']:
            exp1 = df['Close'].ewm(span=12).mean()
            exp2 = df['Close'].ewm(span=26).mean()
            macd_line = exp1 - exp2
            indicators['macd'] = macd_line.iloc[-1]
            signal_line = macd_line.ewm(span=9).mean()
            indicators['macd_signal'] = signal_line.iloc[-1] if len(df) >= 35 else None
            indicators['macd_histogram'] = (macd_line - signal_line).iloc[-1] if len(df) >= 35 else None
        
        # Bollinger Bands
        if indicators['sma_20']:
            std_20 = df['Close'].rolling(window=20).std().iloc[-1]
            indicators['bollinger_middle'] = indicators['sma_20']
            indicators['bollinger_upper'] = indicators['sma_20'] + (2 * std_20)
            indicators['bollinger_lower'] = indicators['sma_20'] - (2 * std_20)
        
        # Stochastic Oscillator
        if len(df) >= 14:
            low_14 = df['Low'].rolling(window=14).min()
            high_14 = df['High'].rolling(window=14).max()
            k_percent = 100 * ((df['Close'] - low_14) / (high_14 - low_14))
            indicators['stochastic_k'] = k_percent.iloc[-1]
            indicators['stochastic_d'] = k_percent.rolling(window=3).mean().iloc[-1]
        
        # VWAP (Volume Weighted Average Price)
        if len(df) >= 20:
            typical_price = (df['High'] + df['Low'] + df['Close']) / 3
            vwap = (typical_price * df['Volume']).rolling(window=20).sum() / df['Volume'].rolling(window=20).sum()
            indicators['vwap'] = vwap.iloc[-1]
        
        # ATR (Average True Range)
        if len(df) >= 14:
            high_low = df['High'] - df['Low']
            high_close = np.abs(df['High'] - df['Close'].shift())
            low_close = np.abs(df['Low'] - df['Close'].shift())
            true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            indicators['atr'] = true_range.rolling(window=14).mean().iloc[-1]
        
        # Volume analysis
        avg_volume = df['Volume'].rolling(window=20).mean().iloc[-1] if len(df) >= 20 else None
        current_volume = df['Volume'].iloc[-1]
        indicators['volume_ratio'] = current_volume / avg_volume if avg_volume and avg_volume > 0 else None
        
        # Support and Resistance
        indicators['resistance_level'] = df['High'].rolling(window=20).max().iloc[-1] if len(df) >= 20 else None
        indicators['support_level'] = df['Low'].rolling(window=20).min().iloc[-1] if len(df) >= 20 else None
        
        # Convert numpy values to Python native types and handle NaN
        for key, value in indicators.items():
            if value is not None and not pd.isna(value):
                indicators[key] = float(value)
            else:
                indicators[key] = None
                
        return indicators
    except Exception as e:
        logger.error(f"Error calculating technical indicators: {str(e)}")
        return {}

def calculate_trading_recommendation(symbol: str, current_price: float, breakout_data: Dict, 
                                   technical_data: Dict, risk_assessment: Dict) -> Dict:
    """Calculate optimal entry points, stop loss, and target prices for trading"""
    try:
        breakout_price = breakout_data['breakout_price']
        breakout_type = breakout_data['type']
        confidence = breakout_data['confidence']
        
        # Calculate Entry Price
        if breakout_type == '200_dma':
            # Enter slightly above 200 DMA breakout
            entry_price = max(current_price, breakout_price * 1.005)  # 0.5% above breakout
            entry_rationale = f"Enter above 200 DMA breakout level of ₹{breakout_price:.2f}"
        elif breakout_type == 'resistance':
            # Enter above resistance with confirmation
            entry_price = max(current_price, breakout_price * 1.01)  # 1% above resistance
            entry_rationale = f"Enter above resistance breakout at ₹{breakout_price:.2f}"
        elif breakout_type == 'momentum':
            # Enter at current price for momentum plays
            entry_price = current_price * 1.002  # Slight buffer for market orders
            entry_rationale = f"Enter on momentum breakout near current price"
        else:
            # Default entry strategy
            entry_price = max(current_price, breakout_price * 1.005)
            entry_rationale = f"Enter above breakout level with confirmation"
        
        # Calculate Stop Loss using multiple methods
        support_level = technical_data.get('support_level')
        sma_20 = technical_data.get('sma_20')
        atr = technical_data.get('atr')
        
        # Method 1: Support-based stop loss
        support_stop = support_level * 0.98 if support_level else None
        
        # Method 2: ATR-based stop loss (2x ATR below entry)
        atr_stop = entry_price - (2 * atr) if atr else None
        
        # Method 3: Percentage-based stop loss (5-8% based on volatility)
        volatility = risk_assessment.get('volatility', 0.25)
        pct_stop_distance = min(max(volatility * 0.3, 0.05), 0.08)  # 5-8% range
        pct_stop = entry_price * (1 - pct_stop_distance)
        
        # Choose the most conservative (highest) stop loss
        stop_options = [s for s in [support_stop, atr_stop, pct_stop] if s is not None]
        stop_loss = max(stop_options) if stop_options else entry_price * 0.95
        
        # Stop loss rationale
        if support_stop and stop_loss == support_stop:
            stop_rationale = f"Support-based stop at ₹{stop_loss:.2f} (2% below support)"
        elif atr_stop and stop_loss == atr_stop:
            stop_rationale = f"ATR-based stop at ₹{stop_loss:.2f} (2x ATR)"
        else:
            stop_rationale = f"Volatility-based stop at ₹{stop_loss:.2f} ({pct_stop_distance*100:.1f}% risk)"
        
        # Calculate Target Price (Risk-Reward ratio approach)
        risk_amount = entry_price - stop_loss
        
        # Adjust target based on breakout strength and confidence
        if confidence >= 0.8:
            reward_ratio = 3.0  # 1:3 risk reward for high confidence
        elif confidence >= 0.7:
            reward_ratio = 2.5  # 1:2.5 risk reward
        else:
            reward_ratio = 2.0  # 1:2 risk reward
        
        target_price = entry_price + (risk_amount * reward_ratio)
        
        # Calculate position sizing (% of portfolio)
        risk_score = risk_assessment.get('risk_score', 5.0)
        base_position = 0.1  # Base 10% position
        
        # Adjust based on confidence and risk
        confidence_multiplier = confidence  # 0.5 to 1.0
        risk_multiplier = max(0.3, 1.0 - (risk_score - 1) * 0.1)  # Lower for higher risk
        
        position_size_percent = min(base_position * confidence_multiplier * risk_multiplier, 0.15) * 100
        
        # Trading Action Recommendation
        if confidence >= 0.75 and risk_score <= 6:
            action = "BUY"
        elif confidence >= 0.6 and risk_score <= 7:
            action = "WAIT"  # Wait for better entry or more confirmation
        else:
            action = "AVOID"  # Too risky or low confidence
        
        risk_reward_ratio = (target_price - entry_price) / (entry_price - stop_loss)
        
        return {
            "entry_price": round(entry_price, 2),
            "stop_loss": round(stop_loss, 2),
            "target_price": round(target_price, 2),
            "risk_reward_ratio": round(risk_reward_ratio, 1),
            "position_size_percent": round(position_size_percent, 1),
            "action": action,
            "entry_rationale": entry_rationale,
            "stop_loss_rationale": stop_rationale
        }
        
    except Exception as e:
        logger.error(f"Error calculating trading recommendation for {symbol}: {str(e)}")
        # Return safe defaults
        return {
            "entry_price": round(current_price * 1.01, 2),
            "stop_loss": round(current_price * 0.95, 2),
            "target_price": round(current_price * 1.1, 2),
            "risk_reward_ratio": 2.0,
            "position_size_percent": 5.0,
            "action": "WAIT",
            "entry_rationale": "Enter with caution",
            "stop_loss_rationale": "5% stop loss"
        }

def get_market_status() -> Dict[str, Any]:
    """Get detailed NSE market status with timings"""
    try:
        # Indian timezone
        ist = pytz.timezone('Asia/Kolkata')
        now_ist = datetime.now(ist)
        
        # NSE market hours: 9:15 AM to 3:30 PM IST (Monday to Friday)
        market_open_time = now_ist.replace(hour=9, minute=15, second=0, microsecond=0)
        market_close_time = now_ist.replace(hour=15, minute=30, second=0, microsecond=0)
        pre_open_start = now_ist.replace(hour=9, minute=0, second=0, microsecond=0)
        
        # Check if it's a weekday
        is_weekday = now_ist.weekday() < 5  # Monday = 0, Friday = 4
        
        current_time_str = now_ist.strftime("%I:%M %p IST")
        
        if not is_weekday:
            return {
                "status": "CLOSED",
                "message": "Market Closed - Weekend",
                "current_time": current_time_str,
                "next_open": "Monday 9:15 AM IST",
                "is_trading_hours": False,
                "time_to_open": None,
                "time_to_close": None
            }
        
        if now_ist < pre_open_start:
            # Before pre-open
            time_to_open = (pre_open_start - now_ist).total_seconds()
            hours, remainder = divmod(time_to_open, 3600)
            minutes, _ = divmod(remainder, 60)
            return {
                "status": "CLOSED",
                "message": f"Pre-Market opens in {int(hours)}h {int(minutes)}m",
                "current_time": current_time_str,
                "next_open": "9:00 AM IST (Pre-Market)",
                "is_trading_hours": False,
                "time_to_open": int(time_to_open),
                "time_to_close": None
            }
        
        elif pre_open_start <= now_ist < market_open_time:
            # Pre-open session
            time_to_open = (market_open_time - now_ist).total_seconds()
            minutes, _ = divmod(time_to_open, 60)
            return {
                "status": "PRE_OPEN",
                "message": f"Pre-Market Session (Trading starts in {int(minutes)}m)",
                "current_time": current_time_str,
                "next_open": "9:15 AM IST",
                "is_trading_hours": False,
                "time_to_open": int(time_to_open),
                "time_to_close": None
            }
        
        elif market_open_time <= now_ist <= market_close_time:
            # Market is open
            time_to_close = (market_close_time - now_ist).total_seconds()
            hours, remainder = divmod(time_to_close, 3600)
            minutes, _ = divmod(remainder, 60)
            return {
                "status": "OPEN",
                "message": f"Market Open (Closes in {int(hours)}h {int(minutes)}m)",
                "current_time": current_time_str,
                "next_close": "3:30 PM IST",
                "is_trading_hours": True,
                "time_to_open": None,
                "time_to_close": int(time_to_close)
            }
        
        else:
            # After market close
            next_day = now_ist + timedelta(days=1)
            next_open = next_day.replace(hour=9, minute=0, second=0, microsecond=0)
            
            # Skip weekend
            while next_open.weekday() >= 5:
                next_open += timedelta(days=1)
            
            return {
                "status": "CLOSED",
                "message": "Market Closed for the day",
                "current_time": current_time_str,
                "next_open": next_open.strftime("%A 9:00 AM IST"),
                "is_trading_hours": False,
                "time_to_open": None,
                "time_to_close": None
            }
            
    except Exception as e:
        logger.error(f"Error getting market status: {str(e)}")
        return {
            "status": "UNKNOWN",
            "message": "Unable to determine market status",
            "current_time": "N/A",
            "next_open": "N/A",
            "is_trading_hours": False,
            "time_to_open": None,
            "time_to_close": None
        }

def calculate_risk_assessment(symbol: str, df: pd.DataFrame, technical_data: Dict, info: Dict) -> Dict:
    """Calculate risk assessment for a stock"""
    try:
        risk_factors = []
        risk_score = 5.0  # Start with neutral risk
        
        # Volatility check
        returns = df['Close'].pct_change().dropna()
        volatility = returns.std() * np.sqrt(252)  # Annualized volatility
        
        if volatility > 0.4:
            risk_factors.append("High volatility (>40%)")
            risk_score += 1.5
        elif volatility > 0.25:
            risk_factors.append("Moderate volatility (25-40%)")
            risk_score += 0.5
        
        # RSI overbought/oversold
        rsi = technical_data.get('rsi')
        if rsi:
            if rsi > 80:
                risk_factors.append("Overbought (RSI > 80)")
                risk_score += 1.0
            elif rsi < 20:
                risk_factors.append("Oversold (RSI < 20)")
                risk_score += 0.5
        
        # Price vs Moving Averages
        current_price = df['Close'].iloc[-1]
        sma_200 = technical_data.get('sma_200')
        if sma_200 and current_price < sma_200:
            risk_factors.append("Below 200-day SMA")
            risk_score += 0.5
        
        # Volume analysis
        volume_ratio = technical_data.get('volume_ratio', 1)
        if volume_ratio < 0.5:
            risk_factors.append("Low volume activity")
            risk_score += 0.5
        
        # Market cap consideration
        market_cap = info.get('marketCap', 0)
        if market_cap and market_cap < 1e9:  # Less than 1 billion
            risk_factors.append("Small cap stock")
            risk_score += 1.0
        
        # Beta consideration
        beta = info.get('beta')
        if beta and beta > 1.5:
            risk_factors.append(f"High beta ({beta:.2f})")
            risk_score += 0.5
        
        # Determine risk level
        if risk_score <= 3:
            risk_level = "Low"
        elif risk_score <= 6:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return {
            "risk_score": min(10.0, max(1.0, risk_score)),
            "volatility": float(volatility) if not pd.isna(volatility) else None,
            "beta": float(beta) if beta and not pd.isna(beta) else None,
            "risk_factors": risk_factors,
            "risk_level": risk_level
        }
    except Exception as e:
        logger.error(f"Error calculating risk assessment for {symbol}: {str(e)}")
        return {
            "risk_score": 5.0,
            "volatility": None,
            "beta": None,
            "risk_factors": ["Unable to assess risk"],
            "risk_level": "Medium"
        }

def extract_fundamental_data(info: Dict) -> Dict:
    """Extract fundamental data from yfinance info"""
    try:
        return {
            "pe_ratio": info.get('trailingPE'),
            "pb_ratio": info.get('priceToBook'),
            "roe": info.get('returnOnEquity'),
            "debt_to_equity": info.get('debtToEquity'),
            "dividend_yield": info.get('dividendYield'),
            "market_cap": info.get('marketCap'),
            "book_value": info.get('bookValue'),
            "eps": info.get('trailingEps'),
            "sector": info.get('sector'),
            "industry": info.get('industry'),
            "earnings_growth": info.get('earningsGrowth'),
            "revenue_growth": info.get('revenueGrowth')
        }
    except Exception as e:
        logger.error(f"Error extracting fundamental data: {str(e)}")
        return {}

def detect_advanced_breakout(symbol: str, df: pd.DataFrame, technical_data: Dict) -> Optional[Dict]:
    """Enhanced breakout detection with multiple patterns"""
    try:
        current_price = df['Close'].iloc[-1]
        breakouts = []
        
        # 200 DMA breakout
        sma_200 = technical_data.get('sma_200')
        if sma_200 and current_price > sma_200 * 1.02:
            if technical_data.get('volume_ratio', 0) > 1.5:
                breakouts.append({
                    "type": "200_dma",
                    "breakout_price": sma_200,
                    "confidence": 0.85
                })
        
        # Resistance breakout
        resistance = technical_data.get('resistance_level')
        if resistance and current_price > resistance * 1.01:
            if technical_data.get('volume_ratio', 0) > 1.3:
                breakouts.append({
                    "type": "resistance",
                    "breakout_price": resistance,
                    "confidence": 0.75
                })
        
        # Bollinger Band breakout
        bb_upper = technical_data.get('bollinger_upper')
        if bb_upper and current_price > bb_upper:
            if technical_data.get('volume_ratio', 0) > 1.2:
                breakouts.append({
                    "type": "bollinger_upper",
                    "breakout_price": bb_upper,
                    "confidence": 0.65
                })
        
        # MACD bullish crossover
        macd = technical_data.get('macd', 0)
        macd_signal = technical_data.get('macd_signal', 0)
        rsi = technical_data.get('rsi', 0)
        
        if macd > macd_signal and 50 < rsi < 80:
            sma_50 = technical_data.get('sma_50', current_price)
            if current_price > sma_50:
                breakouts.append({
                    "type": "momentum",
                    "breakout_price": sma_50,
                    "confidence": 0.70
                })
        
        # Stochastic breakout
        stoch_k = technical_data.get('stochastic_k', 0)
        stoch_d = technical_data.get('stochastic_d', 0)
        if stoch_k > stoch_d and stoch_k > 20 and stoch_k < 80:
            breakouts.append({
                "type": "stochastic",
                "breakout_price": current_price * 0.98,
                "confidence": 0.60
            })
        
        # Return the highest confidence breakout
        if breakouts:
            best_breakout = max(breakouts, key=lambda x: x['confidence'])
            return best_breakout
        
        return None
    except Exception as e:
        logger.error(f"Error detecting breakout for {symbol}: {str(e)}")
        return None

async def fetch_comprehensive_stock_data(symbol: str) -> Optional[Dict]:
    """Fetch comprehensive stock data with all indicators"""
    try:
        ticker_symbol = f"{symbol}.NS"
        
        loop = asyncio.get_event_loop()
        
        def get_stock_info():
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period="1y")
            info = ticker.info
            return hist, info
        
        hist, info = await loop.run_in_executor(executor, get_stock_info)
        
        if hist.empty:
            return None
            
        current_price = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        change_percent = ((current_price - prev_close) / prev_close) * 100
        
        # Calculate all technical indicators
        technical_indicators = calculate_advanced_technical_indicators(hist)
        
        # Extract fundamental data
        fundamental_data = extract_fundamental_data(info)
        
        # Calculate risk assessment
        risk_assessment = calculate_risk_assessment(symbol, hist, technical_indicators, info)
        
        # Detect breakouts
        breakout_data = detect_advanced_breakout(symbol, hist, technical_indicators)
        
        # Calculate trading recommendations if breakout detected
        trading_recommendation = None
        if breakout_data:
            trading_recommendation = calculate_trading_recommendation(
                symbol, current_price, breakout_data, technical_indicators, risk_assessment
            )
        
        # Get sector information
        sector = NSE_SYMBOLS.get(symbol, "Unknown")
        
        # Prepare chart data for different timeframes
        chart_data = {
            "1mo": hist.tail(30).reset_index().to_dict('records'),
            "3mo": hist.tail(90).reset_index().to_dict('records'),
            "6mo": hist.tail(180).reset_index().to_dict('records'),
            "1y": hist.reset_index().to_dict('records')
        }
        
        return {
            "symbol": symbol,
            "name": info.get('longName', symbol),
            "current_price": float(current_price),
            "change_percent": float(change_percent),
            "volume": int(hist['Volume'].iloc[-1]),
            "market_cap": info.get('marketCap'),
            "sector": sector,
            "technical_indicators": technical_indicators,
            "fundamental_data": fundamental_data,
            "risk_assessment": risk_assessment,
            "breakout_data": breakout_data,
            "trading_recommendation": trading_recommendation,
            "chart_data": chart_data,
            "info": info
        }
    except Exception as e:
        logger.error(f"Error fetching comprehensive data for {symbol}: {str(e)}")
        return None

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Indian Stock Breakout Screener API - Enhanced Version"}

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
    """Get list of NSE symbols with sectors"""
    symbols_with_sectors = [{"symbol": symbol, "sector": sector} for symbol, sector in NSE_SYMBOLS.items()]
    return {
        "symbols": list(NSE_SYMBOLS.keys()), 
        "symbols_with_sectors": symbols_with_sectors,
        "count": len(NSE_SYMBOLS),
        "sectors": list(set(NSE_SYMBOLS.values()))
    }

@api_router.get("/stocks/search")
async def search_stocks(q: str):
    """Search stocks by symbol or name"""
    query = q.upper()
    matching_symbols = [
        {"symbol": symbol, "sector": sector} 
        for symbol, sector in NSE_SYMBOLS.items() 
        if query in symbol
    ]
    return {"results": matching_symbols[:10], "query": q}

@api_router.get("/stocks/{symbol}")
async def get_stock_data(symbol: str):
    """Get detailed data for a specific stock"""
    symbol = symbol.upper()
    stock_data = await fetch_comprehensive_stock_data(symbol)
    
    if not stock_data:
        raise HTTPException(status_code=404, detail=f"Stock data not found for {symbol}")
    
    return stock_data

@api_router.get("/stocks/{symbol}/chart")
async def get_stock_chart(symbol: str, timeframe: str = "1mo"):
    """Get chart data for a specific stock and timeframe"""
    symbol = symbol.upper()
    
    try:
        ticker_symbol = f"{symbol}.NS"
        
        period_map = {
            "1d": "1d",
            "5d": "5d", 
            "1mo": "1mo",
            "3mo": "3mo",
            "6mo": "6mo",
            "1y": "1y",
            "2y": "2y"
        }
        
        period = period_map.get(timeframe, "1mo")
        
        loop = asyncio.get_event_loop()
        
        def get_chart_data():
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period=period, interval="1d")
            return hist
        
        hist = await loop.run_in_executor(executor, get_chart_data)
        
        if hist.empty:
            raise HTTPException(status_code=404, detail=f"Chart data not found for {symbol}")
        
        # Calculate indicators for chart
        technical_indicators = calculate_advanced_technical_indicators(hist)
        
        # Prepare chart data
        chart_data = []
        for index, row in hist.iterrows():
            chart_data.append({
                "date": index.strftime("%Y-%m-%d"),
                "open": float(row['Open']),
                "high": float(row['High']),
                "low": float(row['Low']),
                "close": float(row['Close']),
                "volume": int(row['Volume'])
            })
        
        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "data": chart_data,
            "indicators": technical_indicators
        }
        
    except Exception as e:
        logger.error(f"Error fetching chart data for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching chart data")

@api_router.get("/stocks/breakouts/scan")
async def scan_breakout_stocks(
    sector: Optional[str] = None,
    min_confidence: float = 0.5,
    risk_level: Optional[str] = None,
    limit: int = 50
):
    """Enhanced breakout scanning with filters"""
    breakout_stocks = []
    
    # Filter symbols by sector if specified
    symbols_to_scan = list(NSE_SYMBOLS.keys())[:limit]
    if sector and sector != "All":
        symbols_to_scan = [s for s, sect in NSE_SYMBOLS.items() if sect == sector][:limit]
    
    # Fetch data for all symbols concurrently
    tasks = [fetch_comprehensive_stock_data(symbol) for symbol in symbols_to_scan]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    sector_breakouts = {}
    
    for i, result in enumerate(results):
        if isinstance(result, dict) and result.get('breakout_data'):
            symbol = symbols_to_scan[i]
            breakout_data = result['breakout_data']
            
            # Apply confidence filter
            if breakout_data['confidence'] < min_confidence:
                continue
            
            # Apply risk level filter
            if risk_level and result.get('risk_assessment', {}).get('risk_level') != risk_level:
                continue
            
            stock_sector = result.get('sector', 'Unknown')
            technical_indicators = result['technical_indicators']
            fundamental_data = result['fundamental_data']
            risk_assessment = result['risk_assessment']
            
            # Count breakouts by sector
            sector_breakouts[stock_sector] = sector_breakouts.get(stock_sector, 0) + 1
            
            breakout_stock = {
                "symbol": symbol,
                "name": result['name'],
                "current_price": result['current_price'],
                "breakout_price": breakout_data['breakout_price'],
                "breakout_type": breakout_data['type'],
                "confidence_score": breakout_data['confidence'],
                "change_percent": result['change_percent'],
                "volume": result['volume'],
                "sector": stock_sector,
                "technical_data": technical_indicators,
                "fundamental_data": fundamental_data,
                "risk_assessment": risk_assessment,
                "trading_recommendation": result.get('trading_recommendation'),
                "reason": f"Breakout above {breakout_data['type']} level with {breakout_data['confidence']*100:.0f}% confidence"
            }
            
            breakout_stocks.append(breakout_stock)
    
    # Sort by confidence score
    breakout_stocks.sort(key=lambda x: x['confidence_score'], reverse=True)
    
    return {
        "breakout_stocks": breakout_stocks,
        "total_scanned": len(symbols_to_scan),
        "breakouts_found": len(breakout_stocks),
        "sector_breakdown": sector_breakouts,
        "filters_applied": {
            "sector": sector,
            "min_confidence": min_confidence,
            "risk_level": risk_level
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@api_router.get("/stocks/market-overview")
async def get_market_overview():
    """Enhanced market overview with detailed market status"""
    try:
        # Get detailed market status
        market_status = get_market_status()
        
        # Try to fetch NIFTY 50 data - use a fallback approach
        nifty_data = None
        try:
            nifty_data = await fetch_comprehensive_stock_data("NIFTYBEES")  # Fallback to NIFTY BeES
        except:
            try:
                # Another fallback - fetch a major stock as proxy
                nifty_data = await fetch_comprehensive_stock_data("RELIANCE")
            except:
                pass
        
        # Calculate sector performance (simplified)
        sector_performance = {}
        top_sectors = ["IT", "Banking", "FMCG", "Auto", "Pharma"]
        
        for sector in top_sectors:
            sector_symbols = [s for s, sect in NSE_SYMBOLS.items() if sect == sector][:3]
            sector_changes = []
            
            for symbol in sector_symbols:
                try:
                    stock_data = await fetch_comprehensive_stock_data(symbol)
                    if stock_data:
                        sector_changes.append(stock_data['change_percent'])
                except:
                    continue
            
            if sector_changes:
                sector_performance[sector] = sum(sector_changes) / len(sector_changes)
        
        market_sentiment = "Neutral"
        nifty_change = 0
        nifty_current = 24000  # Default fallback
        
        if nifty_data:
            nifty_change = nifty_data['change_percent']
            nifty_current = nifty_data['current_price']
            
            if nifty_change > 1:
                market_sentiment = "Bullish"
            elif nifty_change < -1:
                market_sentiment = "Bearish"
        
        return {
            "nifty_50": {
                "current": nifty_current,
                "change_percent": nifty_change
            },
            "market_status": market_status,
            "market_sentiment": market_sentiment,
            "sector_performance": sector_performance,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching market overview: {str(e)}")
        # Return fallback data with current market status
        try:
            market_status = get_market_status()
        except:
            market_status = {
                "status": "UNKNOWN",
                "message": "Unable to determine market status",
                "current_time": "N/A",
                "is_trading_hours": False
            }
        
        return {
            "nifty_50": {"current": 24000, "change_percent": 0.5},
            "market_status": market_status,
            "market_sentiment": "Neutral",
            "sector_performance": {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

@api_router.get("/watchlist")
async def get_watchlist():
    """Get user's watchlist"""
    try:
        watchlist_items = await db.watchlist.find().to_list(1000)
        # Convert ObjectId to string for JSON serialization
        watchlist = []
        for item in watchlist_items:
            if '_id' in item:
                del item['_id']  # Remove MongoDB ObjectId
            # Convert datetime to ISO string
            if 'added_date' in item and hasattr(item['added_date'], 'isoformat'):
                item['added_date'] = item['added_date'].isoformat()
            watchlist.append(item)
        return {"watchlist": watchlist, "count": len(watchlist)}
    except Exception as e:
        logger.error(f"Error fetching watchlist: {str(e)}")
        return {"watchlist": [], "count": 0}

@api_router.post("/watchlist")
async def add_to_watchlist(symbol: str, target_price: Optional[float] = None, stop_loss: Optional[float] = None, notes: Optional[str] = None):
    """Add stock to watchlist"""
    try:
        symbol = symbol.upper()
        
        # Get current stock data
        stock_data = await fetch_comprehensive_stock_data(symbol)
        if not stock_data:
            raise HTTPException(status_code=404, detail=f"Stock not found: {symbol}")
        
        # Check if already in watchlist
        existing = await db.watchlist.find_one({"symbol": symbol})
        if existing:
            raise HTTPException(status_code=400, detail=f"{symbol} is already in watchlist")
        
        watchlist_item = {
            "id": str(uuid.uuid4()),
            "symbol": symbol,
            "name": stock_data['name'],
            "added_price": stock_data['current_price'],
            "target_price": target_price,
            "stop_loss": stop_loss,
            "notes": notes,
            "added_date": datetime.now(timezone.utc).isoformat()  # Store as ISO string
        }
        
        await db.watchlist.insert_one(watchlist_item)
        return {"message": f"Added {symbol} to watchlist", "item": watchlist_item}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding to watchlist: {str(e)}")
        raise HTTPException(status_code=500, detail="Error adding to watchlist")

@api_router.delete("/watchlist/{symbol}")
async def remove_from_watchlist(symbol: str):
    """Remove stock from watchlist"""
    try:
        symbol = symbol.upper()
        result = await db.watchlist.delete_one({"symbol": symbol})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"{symbol} not found in watchlist")
        
        return {"message": f"Removed {symbol} from watchlist"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing from watchlist: {str(e)}")
        raise HTTPException(status_code=500, detail="Error removing from watchlist")

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