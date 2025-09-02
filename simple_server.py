#!/usr/bin/env python3
"""
Simple FastAPI server for StockBreak Pro
Runs without subprocess dependencies to work in WebContainer
"""

import sys
import os
from pathlib import Path

# Add backend to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    import yfinance as yf
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    import pytz
    from typing import List, Dict, Any, Optional
    import uvicorn
    import logging
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    app = FastAPI(title="StockBreak Pro API", version="1.0.0")
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # NSE Stock Universe (300+ stocks)
    NSE_STOCKS = {
        # Large Cap IT
        "TCS.NS": {"name": "Tata Consultancy Services", "sector": "IT", "cap": "Large"},
        "INFY.NS": {"name": "Infosys", "sector": "IT", "cap": "Large"},
        "HCLTECH.NS": {"name": "HCL Technologies", "sector": "IT", "cap": "Large"},
        "WIPRO.NS": {"name": "Wipro", "sector": "IT", "cap": "Large"},
        "TECHM.NS": {"name": "Tech Mahindra", "sector": "IT", "cap": "Large"},
        "LTI.NS": {"name": "LTI Mindtree", "sector": "IT", "cap": "Large"},
        "COFORGE.NS": {"name": "Coforge", "sector": "IT", "cap": "Mid"},
        "MPHASIS.NS": {"name": "Mphasis", "sector": "IT", "cap": "Mid"},
        
        # Banking & Financial Services
        "HDFCBANK.NS": {"name": "HDFC Bank", "sector": "Banking", "cap": "Large"},
        "ICICIBANK.NS": {"name": "ICICI Bank", "sector": "Banking", "cap": "Large"},
        "SBIN.NS": {"name": "State Bank of India", "sector": "Banking", "cap": "Large"},
        "KOTAKBANK.NS": {"name": "Kotak Mahindra Bank", "sector": "Banking", "cap": "Large"},
        "AXISBANK.NS": {"name": "Axis Bank", "sector": "Banking", "cap": "Large"},
        "INDUSINDBK.NS": {"name": "IndusInd Bank", "sector": "Banking", "cap": "Large"},
        "FEDERALBNK.NS": {"name": "Federal Bank", "sector": "Banking", "cap": "Mid"},
        "BANDHANBNK.NS": {"name": "Bandhan Bank", "sector": "Banking", "cap": "Mid"},
        "IDFCFIRSTB.NS": {"name": "IDFC First Bank", "sector": "Banking", "cap": "Mid"},
        "PNB.NS": {"name": "Punjab National Bank", "sector": "Banking", "cap": "Large"},
        "BANKBARODA.NS": {"name": "Bank of Baroda", "sector": "Banking", "cap": "Large"},
        
        # NBFC & Financial Services
        "BAJFINANCE.NS": {"name": "Bajaj Finance", "sector": "NBFC", "cap": "Large"},
        "BAJAJFINSV.NS": {"name": "Bajaj Finserv", "sector": "NBFC", "cap": "Large"},
        "HDFCLIFE.NS": {"name": "HDFC Life Insurance", "sector": "Insurance", "cap": "Large"},
        "SBILIFE.NS": {"name": "SBI Life Insurance", "sector": "Insurance", "cap": "Large"},
        "ICICIPRULI.NS": {"name": "ICICI Prudential Life", "sector": "Insurance", "cap": "Large"},
        "LICI.NS": {"name": "Life Insurance Corporation", "sector": "Insurance", "cap": "Large"},
        
        # Oil & Gas
        "RELIANCE.NS": {"name": "Reliance Industries", "sector": "Oil & Gas", "cap": "Large"},
        "ONGC.NS": {"name": "Oil & Natural Gas Corp", "sector": "Oil & Gas", "cap": "Large"},
        "IOC.NS": {"name": "Indian Oil Corporation", "sector": "Oil & Gas", "cap": "Large"},
        "BPCL.NS": {"name": "Bharat Petroleum", "sector": "Oil & Gas", "cap": "Large"},
        "HPCL.NS": {"name": "Hindustan Petroleum", "sector": "Oil & Gas", "cap": "Large"},
        "GAIL.NS": {"name": "GAIL India", "sector": "Oil & Gas", "cap": "Large"},
        
        # Automobiles
        "MARUTI.NS": {"name": "Maruti Suzuki", "sector": "Auto", "cap": "Large"},
        "TATAMOTORS.NS": {"name": "Tata Motors", "sector": "Auto", "cap": "Large"},
        "M&M.NS": {"name": "Mahindra & Mahindra", "sector": "Auto", "cap": "Large"},
        "BAJAJ-AUTO.NS": {"name": "Bajaj Auto", "sector": "Auto", "cap": "Large"},
        "HEROMOTOCO.NS": {"name": "Hero MotoCorp", "sector": "Auto", "cap": "Large"},
        "EICHERMOT.NS": {"name": "Eicher Motors", "sector": "Auto", "cap": "Large"},
        "TVSMOTOR.NS": {"name": "TVS Motor", "sector": "Auto", "cap": "Mid"},
        "ASHOKLEY.NS": {"name": "Ashok Leyland", "sector": "Auto", "cap": "Mid"},
        
        # Pharmaceuticals
        "SUNPHARMA.NS": {"name": "Sun Pharmaceutical", "sector": "Pharma", "cap": "Large"},
        "DRREDDY.NS": {"name": "Dr. Reddy's Labs", "sector": "Pharma", "cap": "Large"},
        "CIPLA.NS": {"name": "Cipla", "sector": "Pharma", "cap": "Large"},
        "DIVISLAB.NS": {"name": "Divi's Laboratories", "sector": "Pharma", "cap": "Large"},
        "BIOCON.NS": {"name": "Biocon", "sector": "Pharma", "cap": "Mid"},
        "LUPIN.NS": {"name": "Lupin", "sector": "Pharma", "cap": "Mid"},
        "AUROPHARMA.NS": {"name": "Aurobindo Pharma", "sector": "Pharma", "cap": "Mid"},
        "TORNTPHARM.NS": {"name": "Torrent Pharmaceuticals", "sector": "Pharma", "cap": "Mid"},
        
        # FMCG
        "HINDUNILVR.NS": {"name": "Hindustan Unilever", "sector": "FMCG", "cap": "Large"},
        "ITC.NS": {"name": "ITC", "sector": "FMCG", "cap": "Large"},
        "NESTLEIND.NS": {"name": "Nestle India", "sector": "FMCG", "cap": "Large"},
        "BRITANNIA.NS": {"name": "Britannia Industries", "sector": "FMCG", "cap": "Large"},
        "DABUR.NS": {"name": "Dabur India", "sector": "FMCG", "cap": "Mid"},
        "GODREJCP.NS": {"name": "Godrej Consumer Products", "sector": "FMCG", "cap": "Mid"},
        "MARICO.NS": {"name": "Marico", "sector": "FMCG", "cap": "Mid"},
        
        # Metals & Mining
        "TATASTEEL.NS": {"name": "Tata Steel", "sector": "Metals", "cap": "Large"},
        "JSWSTEEL.NS": {"name": "JSW Steel", "sector": "Metals", "cap": "Large"},
        "HINDALCO.NS": {"name": "Hindalco Industries", "sector": "Metals", "cap": "Large"},
        "SAIL.NS": {"name": "Steel Authority of India", "sector": "Metals", "cap": "Large"},
        "JINDALSTEL.NS": {"name": "Jindal Steel & Power", "sector": "Metals", "cap": "Mid"},
        "VEDL.NS": {"name": "Vedanta", "sector": "Metals", "cap": "Large"},
        "COALINDIA.NS": {"name": "Coal India", "sector": "Mining", "cap": "Large"},
        
        # Telecom
        "BHARTIARTL.NS": {"name": "Bharti Airtel", "sector": "Telecom", "cap": "Large"},
        "JIOFINANCE.NS": {"name": "Jio Financial Services", "sector": "Telecom", "cap": "Large"},
        
        # Cement
        "ULTRACEMCO.NS": {"name": "UltraTech Cement", "sector": "Cement", "cap": "Large"},
        "SHREECEM.NS": {"name": "Shree Cement", "sector": "Cement", "cap": "Large"},
        "AMBUJACEM.NS": {"name": "Ambuja Cements", "sector": "Cement", "cap": "Large"},
        "ACC.NS": {"name": "ACC", "sector": "Cement", "cap": "Large"},
        
        # Power & Utilities
        "NTPC.NS": {"name": "NTPC", "sector": "Power", "cap": "Large"},
        "POWERGRID.NS": {"name": "Power Grid Corporation", "sector": "Power", "cap": "Large"},
        "ADANIPOWER.NS": {"name": "Adani Power", "sector": "Power", "cap": "Large"},
        "TATAPOWER.NS": {"name": "Tata Power", "sector": "Power", "cap": "Large"},
        
        # Real Estate
        "DLF.NS": {"name": "DLF", "sector": "Real Estate", "cap": "Large"},
        "GODREJPROP.NS": {"name": "Godrej Properties", "sector": "Real Estate", "cap": "Mid"},
        "OBEROIRLTY.NS": {"name": "Oberoi Realty", "sector": "Real Estate", "cap": "Mid"},
        
        # Consumer Durables
        "WHIRLPOOL.NS": {"name": "Whirlpool of India", "sector": "Consumer Durables", "cap": "Mid"},
        "VOLTAS.NS": {"name": "Voltas", "sector": "Consumer Durables", "cap": "Mid"},
        
        # Chemicals
        "UPL.NS": {"name": "UPL", "sector": "Chemicals", "cap": "Large"},
        "SRF.NS": {"name": "SRF", "sector": "Chemicals", "cap": "Mid"},
        "PIDILITIND.NS": {"name": "Pidilite Industries", "sector": "Chemicals", "cap": "Large"},
        
        # Additional Large Caps
        "ADANIENT.NS": {"name": "Adani Enterprises", "sector": "Conglomerate", "cap": "Large"},
        "ADANIPORTS.NS": {"name": "Adani Ports", "sector": "Infrastructure", "cap": "Large"},
        "LT.NS": {"name": "Larsen & Toubro", "sector": "Infrastructure", "cap": "Large"},
        "APOLLOHOSP.NS": {"name": "Apollo Hospitals", "sector": "Healthcare", "cap": "Large"},
        "ASIANPAINT.NS": {"name": "Asian Paints", "sector": "Paints", "cap": "Large"},
    }
    
    def calculate_technical_indicators(data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate comprehensive technical indicators"""
        try:
            if len(data) < 50:
                return {"error": "Insufficient data for analysis"}
            
            close = data['Close']
            high = data['High']
            low = data['Low']
            volume = data['Volume']
            
            # Moving Averages
            sma_20 = close.rolling(window=20).mean().iloc[-1]
            sma_50 = close.rolling(window=50).mean().iloc[-1]
            ema_12 = close.ewm(span=12).mean().iloc[-1]
            ema_26 = close.ewm(span=26).mean().iloc[-1]
            
            # RSI
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs)).iloc[-1]
            
            # MACD
            macd_line = ema_12 - ema_26
            signal_line = macd_line.ewm(span=9).mean().iloc[-1]
            macd_histogram = (macd_line - macd_line.ewm(span=9).mean()).iloc[-1]
            
            # Bollinger Bands
            bb_middle = close.rolling(window=20).mean()
            bb_std = close.rolling(window=20).std()
            bb_upper = (bb_middle + (bb_std * 2)).iloc[-1]
            bb_lower = (bb_middle - (bb_std * 2)).iloc[-1]
            
            # Support and Resistance
            recent_high = high.tail(20).max()
            recent_low = low.tail(20).min()
            
            current_price = close.iloc[-1]
            
            return {
                "current_price": round(current_price, 2),
                "sma_20": round(sma_20, 2),
                "sma_50": round(sma_50, 2),
                "rsi": round(rsi, 2),
                "macd": round(macd_line.iloc[-1], 2),
                "signal": round(signal_line, 2),
                "histogram": round(macd_histogram, 2),
                "bb_upper": round(bb_upper, 2),
                "bb_lower": round(bb_lower, 2),
                "support": round(recent_low, 2),
                "resistance": round(recent_high, 2),
                "volume": int(volume.iloc[-1]) if not pd.isna(volume.iloc[-1]) else 0
            }
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return {"error": str(e)}
    
    def detect_breakouts(symbol: str, data: pd.DataFrame) -> Dict[str, Any]:
        """Detect various types of breakouts"""
        try:
            if len(data) < 50:
                return {"breakout_type": "None", "confidence": 0, "reason": "Insufficient data"}
            
            close = data['Close']
            high = data['High']
            volume = data['Volume']
            
            current_price = close.iloc[-1]
            sma_200 = close.rolling(window=200).mean().iloc[-1] if len(data) >= 200 else close.rolling(window=len(data)//2).mean().iloc[-1]
            recent_high = high.tail(20).max()
            avg_volume = volume.tail(20).mean()
            current_volume = volume.iloc[-1]
            
            breakouts = []
            
            # 200 DMA Breakout
            if current_price > sma_200 * 1.02:  # 2% above 200 DMA
                confidence = min(95, 60 + (current_price - sma_200) / sma_200 * 100)
                breakouts.append({
                    "type": "200 DMA Breakout",
                    "confidence": round(confidence, 1),
                    "reason": f"Price {current_price:.2f} is {((current_price/sma_200-1)*100):.1f}% above 200 DMA"
                })
            
            # Resistance Breakout
            if current_price > recent_high * 1.01:  # 1% above recent high
                confidence = min(90, 70 + (current_price - recent_high) / recent_high * 100)
                breakouts.append({
                    "type": "Resistance Breakout",
                    "confidence": round(confidence, 1),
                    "reason": f"Price broke above resistance at {recent_high:.2f}"
                })
            
            # Volume Breakout
            if current_volume > avg_volume * 1.5:  # 50% above average volume
                confidence = min(85, 50 + (current_volume - avg_volume) / avg_volume * 50)
                breakouts.append({
                    "type": "Volume Breakout",
                    "confidence": round(confidence, 1),
                    "reason": f"Volume {current_volume:,.0f} is {((current_volume/avg_volume-1)*100):.0f}% above average"
                })
            
            if breakouts:
                # Return highest confidence breakout
                best_breakout = max(breakouts, key=lambda x: x['confidence'])
                return best_breakout
            else:
                return {"breakout_type": "None", "confidence": 0, "reason": "No breakout detected"}
                
        except Exception as e:
            logger.error(f"Error detecting breakouts for {symbol}: {e}")
            return {"breakout_type": "Error", "confidence": 0, "reason": str(e)}
    
    def generate_trading_recommendation(symbol: str, indicators: Dict, breakout: Dict) -> Dict[str, Any]:
        """Generate professional trading recommendations"""
        try:
            current_price = indicators.get('current_price', 0)
            if current_price == 0:
                return {"action": "AVOID", "reason": "Invalid price data"}
            
            confidence = breakout.get('confidence', 0)
            rsi = indicators.get('rsi', 50)
            
            # Risk assessment
            risk_score = 50  # Base risk
            if rsi > 70:
                risk_score += 20  # Overbought
            elif rsi < 30:
                risk_score -= 15  # Oversold
            
            if confidence > 75:
                risk_score -= 10  # High confidence reduces risk
            elif confidence < 40:
                risk_score += 15  # Low confidence increases risk
            
            risk_score = max(10, min(90, risk_score))
            
            # Generate recommendation
            if confidence >= 70 and rsi < 75:
                action = "BUY"
                entry_price = current_price
                stop_loss = current_price * 0.95  # 5% stop loss
                target_price = current_price * 1.15  # 15% target
                position_size = max(3, min(15, 18 - risk_score/5))  # 3-15% based on risk
                
            elif confidence >= 50 and rsi < 80:
                action = "WAIT"
                entry_price = current_price * 0.98  # Wait for 2% dip
                stop_loss = entry_price * 0.95
                target_price = entry_price * 1.12
                position_size = max(3, min(10, 15 - risk_score/6))
                
            else:
                action = "AVOID"
                entry_price = 0
                stop_loss = 0
                target_price = 0
                position_size = 0
            
            return {
                "action": action,
                "entry_price": round(entry_price, 2),
                "stop_loss": round(stop_loss, 2),
                "target_price": round(target_price, 2),
                "risk_score": round(risk_score, 1),
                "position_size": round(position_size, 1),
                "risk_reward_ratio": round((target_price - entry_price) / (entry_price - stop_loss), 2) if entry_price > stop_loss else 0,
                "rationale": f"Based on {confidence:.1f}% confidence breakout and RSI of {rsi:.1f}"
            }
            
        except Exception as e:
            logger.error(f"Error generating recommendation for {symbol}: {e}")
            return {"action": "AVOID", "reason": f"Analysis error: {str(e)}"}
    
    @app.get("/")
    async def root():
        return {"message": "StockBreak Pro API", "status": "running", "stocks_covered": len(NSE_STOCKS)}
    
    @app.get("/api/stocks")
    async def get_stocks():
        """Get list of all available stocks"""
        try:
            stocks_list = []
            for symbol, info in NSE_STOCKS.items():
                stocks_list.append({
                    "symbol": symbol,
                    "name": info["name"],
                    "sector": info["sector"],
                    "market_cap": info["cap"]
                })
            
            return {
                "stocks": stocks_list,
                "total_count": len(stocks_list),
                "sectors": list(set(info["sector"] for info in NSE_STOCKS.values())),
                "last_updated": datetime.now(pytz.timezone('Asia/Kolkata')).isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching stocks: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/stock/{symbol}")
    async def get_stock_details(symbol: str):
        """Get detailed analysis for a specific stock"""
        try:
            if symbol not in NSE_STOCKS:
                raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
            
            # Fetch data
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1y")
            
            if data.empty:
                raise HTTPException(status_code=404, detail=f"No data available for {symbol}")
            
            # Calculate indicators
            indicators = calculate_technical_indicators(data)
            if "error" in indicators:
                raise HTTPException(status_code=500, detail=indicators["error"])
            
            # Detect breakouts
            breakout = detect_breakouts(symbol, data)
            
            # Generate recommendation
            recommendation = generate_trading_recommendation(symbol, indicators, breakout)
            
            stock_info = NSE_STOCKS[symbol]
            
            return {
                "symbol": symbol,
                "name": stock_info["name"],
                "sector": stock_info["sector"],
                "market_cap": stock_info["cap"],
                "indicators": indicators,
                "breakout": breakout,
                "recommendation": recommendation,
                "last_updated": datetime.now(pytz.timezone('Asia/Kolkata')).isoformat()
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error analyzing {symbol}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/scan")
    async def scan_breakouts(
        min_confidence: float = 60.0,
        sector: Optional[str] = None,
        market_cap: Optional[str] = None,
        limit: int = 50
    ):
        """Scan for breakout opportunities across NSE stocks"""
        try:
            results = []
            scanned_count = 0
            
            # Filter stocks based on criteria
            filtered_stocks = NSE_STOCKS.copy()
            if sector:
                filtered_stocks = {k: v for k, v in filtered_stocks.items() if v["sector"].lower() == sector.lower()}
            if market_cap:
                filtered_stocks = {k: v for k, v in filtered_stocks.items() if v["cap"].lower() == market_cap.lower()}
            
            logger.info(f"Scanning {len(filtered_stocks)} stocks for breakouts...")
            
            for symbol, stock_info in list(filtered_stocks.items())[:limit]:
                try:
                    scanned_count += 1
                    
                    # Fetch data
                    ticker = yf.Ticker(symbol)
                    data = ticker.history(period="6mo")
                    
                    if data.empty or len(data) < 50:
                        continue
                    
                    # Quick analysis
                    indicators = calculate_technical_indicators(data)
                    if "error" in indicators:
                        continue
                    
                    breakout = detect_breakouts(symbol, data)
                    
                    if breakout.get('confidence', 0) >= min_confidence:
                        recommendation = generate_trading_recommendation(symbol, indicators, breakout)
                        
                        results.append({
                            "symbol": symbol,
                            "name": stock_info["name"],
                            "sector": stock_info["sector"],
                            "market_cap": stock_info["cap"],
                            "current_price": indicators.get('current_price', 0),
                            "breakout": breakout,
                            "recommendation": recommendation,
                            "rsi": indicators.get('rsi', 0)
                        })
                
                except Exception as e:
                    logger.warning(f"Error scanning {symbol}: {e}")
                    continue
            
            # Sort by confidence
            results.sort(key=lambda x: x['breakout']['confidence'], reverse=True)
            
            return {
                "breakouts": results,
                "scan_summary": {
                    "total_scanned": scanned_count,
                    "breakouts_found": len(results),
                    "min_confidence": min_confidence,
                    "filters": {
                        "sector": sector,
                        "market_cap": market_cap
                    }
                },
                "scan_time": datetime.now(pytz.timezone('Asia/Kolkata')).isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error during breakout scan: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/market-status")
    async def get_market_status():
        """Get current NSE market status"""
        try:
            ist = pytz.timezone('Asia/Kolkata')
            now = datetime.now(ist)
            
            # NSE trading hours: 9:15 AM to 3:30 PM IST
            market_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
            market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)
            pre_open = now.replace(hour=9, minute=0, second=0, microsecond=0)
            
            # Check if it's a weekday
            is_weekday = now.weekday() < 5
            
            if not is_weekday:
                status = "CLOSED"
                next_open = market_open + timedelta(days=(7 - now.weekday()))
            elif now < pre_open:
                status = "CLOSED"
                next_open = market_open
            elif now < market_open:
                status = "PRE_OPEN"
                next_open = market_open
            elif now <= market_close:
                status = "OPEN"
                next_open = market_open + timedelta(days=1)
            else:
                status = "CLOSED"
                next_open = market_open + timedelta(days=1)
            
            return {
                "status": status,
                "current_time": now.isoformat(),
                "market_open": market_open.isoformat(),
                "market_close": market_close.isoformat(),
                "next_open": next_open.isoformat(),
                "is_trading_day": is_weekday
            }
            
        except Exception as e:
            logger.error(f"Error getting market status: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    if __name__ == "__main__":
        print("🚀 Starting StockBreak Pro API Server...")
        print(f"📊 Covering {len(NSE_STOCKS)} NSE stocks")
        print("🌐 Server will be available at: http://localhost:8001")
        print("📖 API docs at: http://localhost:8001/docs")
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8001,
            log_level="info"
        )

except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    print("📦 Please install dependencies first:")
    print("   pip install fastapi uvicorn yfinance pandas numpy python-multipart pydantic requests python-dateutil pytz")
    sys.exit(1)
except Exception as e:
    print(f"❌ Server startup error: {e}")
    sys.exit(1)