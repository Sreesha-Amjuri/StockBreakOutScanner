"""
Pydantic models for stock data structures
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class TechnicalIndicators(BaseModel):
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
    bollinger_middle: Optional[float] = None
    bollinger_lower: Optional[float] = None
    stochastic_k: Optional[float] = None
    stochastic_d: Optional[float] = None
    vwap: Optional[float] = None
    atr: Optional[float] = None
    support_level: Optional[float] = None
    resistance_level: Optional[float] = None
    volume_ratio: Optional[float] = None

class FundamentalData(BaseModel):
    market_cap: Optional[int] = None
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    eps: Optional[float] = None
    book_value: Optional[float] = None
    roe: Optional[float] = None
    debt_to_equity: Optional[float] = None
    dividend_yield: Optional[float] = None
    earnings_growth: Optional[float] = None

class RiskAssessment(BaseModel):
    risk_level: str = Field(..., description="Low, Medium, or High")
    risk_score: float = Field(..., ge=0, le=10, description="Risk score from 0-10")
    risk_factors: List[str] = Field(default_factory=list)
    volatility: Optional[float] = None
    beta: Optional[float] = None

class BreakoutData(BaseModel):
    type: str = Field(..., description="Type of breakout detected")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score 0-1")
    breakout_price: float = Field(..., description="Price level of breakout")
    description: str = Field(..., description="Human readable breakout description")

class TradingRecommendation(BaseModel):
    entry_price: float = Field(..., description="Recommended entry price")
    stop_loss: float = Field(..., description="Stop loss price")
    target_price: float = Field(..., description="Target price")
    risk_reward_ratio: float = Field(..., description="Risk to reward ratio")
    position_size_percent: float = Field(..., ge=1, le=20, description="Position size as % of portfolio")
    action: str = Field(..., description="BUY, WAIT, or AVOID")
    entry_rationale: str = Field(..., description="Reason for entry recommendation")
    stop_loss_rationale: str = Field(..., description="Reason for stop loss level")

class DataValidation(BaseModel):
    source: str = Field(..., description="Data source name")
    timestamp: str = Field(..., description="Data timestamp")
    data_age_warning: Optional[str] = None

class StockData(BaseModel):
    symbol: str
    name: str
    sector: str
    current_price: float
    change_percent: float
    volume: int
    market_cap: Optional[int] = None
    technical_indicators: TechnicalIndicators
    fundamental_data: FundamentalData
    risk_assessment: RiskAssessment
    breakout_data: Optional[BreakoutData] = None
    trading_recommendation: Optional[TradingRecommendation] = None
    data_validation: DataValidation

class BreakoutStock(BaseModel):
    symbol: str
    name: str
    current_price: float
    change_percent: float
    breakout_type: str
    confidence_score: float
    sector: str
    trading_recommendation: Optional[TradingRecommendation]
    technical_data: Dict[str, Any]
    risk_assessment: Dict[str, Any]

class MarketStatus(BaseModel):
    status: str = Field(..., description="OPEN, CLOSED, or PRE_OPEN")
    message: str
    current_time: str
    is_trading_hours: bool
    time_to_close: Optional[int] = None
    next_open: Optional[str] = None

class MarketOverview(BaseModel):
    nifty_50: Dict[str, float]
    market_status: MarketStatus
    market_sentiment: str
    sector_performance: Optional[Dict[str, float]] = None
    timestamp: str

class WatchlistItem(BaseModel):
    symbol: str
    added_at: datetime

class BreakoutScanResult(BaseModel):
    breakout_stocks: List[BreakoutStock]
    breakouts_found: int
    total_scanned: int
    scan_timestamp: str
    filters_applied: Dict[str, Any]

class ValidationResult(BaseModel):
    symbol: str
    validation_timestamp: str
    data_quality_score: int = Field(..., ge=0, le=100)
    quality_level: str
    warnings: List[str]
    yahoo_finance: Optional[Dict[str, Any]] = None
    nse_crosscheck: Optional[Dict[str, Any]] = None