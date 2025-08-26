import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { ArrowLeft, TrendingUp, TrendingDown, Heart, AlertTriangle, DollarSign, BarChart3, Activity, Shield } from 'lucide-react';
import axios from 'axios';
import StockChart from './StockChart';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const StockDetails = () => {
  const { symbol } = useParams();
  const navigate = useNavigate();
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isInWatchlist, setIsInWatchlist] = useState(false);

  useEffect(() => {
    fetchStockData();
    checkWatchlistStatus();
  }, [symbol]);

  const fetchStockData = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/stocks/${symbol}`);
      setStockData(response.data);
    } catch (error) {
      console.error('Error fetching stock data:', error);
      toast.error('Failed to fetch stock data');
    } finally {
      setLoading(false);
    }
  };

  const checkWatchlistStatus = async () => {
    try {
      const response = await axios.get(`${API}/watchlist`);
      const watchlist = response.data.watchlist;
      setIsInWatchlist(watchlist.some(item => item.symbol === symbol));
    } catch (error) {
      console.error('Error checking watchlist status:', error);
    }
  };

  const toggleWatchlist = async () => {
    try {
      if (isInWatchlist) {
        await axios.delete(`${API}/watchlist/${symbol}`);
        setIsInWatchlist(false);
        toast.success(`Removed ${symbol} from watchlist`);
      } else {
        await axios.post(`${API}/watchlist?symbol=${symbol}`);
        setIsInWatchlist(true);
        toast.success(`Added ${symbol} to watchlist`);
      }
    } catch (error) {
      console.error('Error updating watchlist:', error);
      toast.error('Failed to update watchlist');
    }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 2
    }).format(price);
  };

  const formatLargeNumber = (num) => {
    if (!num) return '-';
    if (num >= 10000000) return `${(num / 10000000).toFixed(1)}Cr`;
    if (num >= 100000) return `${(num / 100000).toFixed(1)}L`;
    return num.toLocaleString();
  };

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'Low': return 'bg-emerald-100 text-emerald-800 border-emerald-200';
      case 'Medium': return 'bg-amber-100 text-amber-800 border-amber-200';
      case 'High': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!stockData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="w-12 h-12 text-amber-600 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-slate-900 mb-2">Stock Not Found</h2>
          <p className="text-slate-600 mb-4">Unable to fetch data for {symbol}</p>
          <Button onClick={() => navigate('/')}>Back to Dashboard</Button>
        </div>
      </div>
    );
  }

  const technical = stockData.technical_indicators;
  const fundamental = stockData.fundamental_data;
  const risk = stockData.risk_assessment;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="sm" onClick={() => navigate('/')}>
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back
              </Button>
              
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-slate-900">{stockData.symbol}</h1>
                  <p className="text-sm text-slate-600">{stockData.name}</p>
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-2xl font-bold text-slate-900">
                  {formatPrice(stockData.current_price)}
                </p>
                <div className="flex items-center space-x-2">
                  {stockData.change_percent >= 0 ? (
                    <TrendingUp className="w-4 h-4 text-emerald-600" />
                  ) : (
                    <TrendingDown className="w-4 h-4 text-red-600" />
                  )}
                  <span className={`font-medium ${
                    stockData.change_percent >= 0 ? 'text-emerald-600' : 'text-red-600'
                  }`}>
                    {stockData.change_percent >= 0 ? '+' : ''}
                    {stockData.change_percent.toFixed(2)}%
                  </span>
                </div>
              </div>
              
              <Button
                onClick={toggleWatchlist}
                variant={isInWatchlist ? "default" : "outline"}
                size="sm"
              >
                <Heart className={`w-4 h-4 mr-2 ${isInWatchlist ? 'fill-current' : ''}`} />
                {isInWatchlist ? 'In Watchlist' : 'Add to Watchlist'}
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Key Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Market Cap</p>
                  <p className="text-lg font-bold text-slate-900">
                    {formatLargeNumber(stockData.market_cap)}
                  </p>
                </div>
                <DollarSign className="w-8 h-8 text-blue-600" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Volume</p>
                  <p className="text-lg font-bold text-slate-900">
                    {formatLargeNumber(stockData.volume)}
                  </p>
                </div>
                <BarChart3 className="w-8 h-8 text-emerald-600" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Sector</p>
                  <p className="text-lg font-bold text-slate-900">{stockData.sector}</p>
                </div>
                <Activity className="w-8 h-8 text-purple-600" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Risk Level</p>
                  <Badge className={getRiskColor(risk?.risk_level)}>
                    {risk?.risk_level || 'Unknown'}
                  </Badge>
                </div>
                <Shield className="w-8 h-8 text-amber-600" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Chart */}
        <div className="mb-8">
          <StockChart symbol={stockData.symbol} height={500} />
        </div>

        {/* Detailed Analysis Tabs */}
        <Tabs defaultValue="technical" className="space-y-6">
          <TabsList className="grid grid-cols-4 w-full">
            <TabsTrigger value="technical">Technical Analysis</TabsTrigger>
            <TabsTrigger value="fundamental">Fundamental Analysis</TabsTrigger>
            <TabsTrigger value="risk">Risk Assessment</TabsTrigger>
            <TabsTrigger value="breakout">Breakout Analysis</TabsTrigger>
          </TabsList>

          <TabsContent value="technical">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
                <CardHeader>
                  <CardTitle>Moving Averages</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">SMA 20</span>
                    <span className="font-semibold">{technical.sma_20 ? formatPrice(technical.sma_20) : '-'}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">SMA 50</span>
                    <span className="font-semibold">{technical.sma_50 ? formatPrice(technical.sma_50) : '-'}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">SMA 200</span>
                    <span className="font-semibold">{technical.sma_200 ? formatPrice(technical.sma_200) : '-'}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">EMA 12</span>
                    <span className="font-semibold">{technical.ema_12 ? formatPrice(technical.ema_12) : '-'}</span>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
                <CardHeader>
                  <CardTitle>Oscillators</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">RSI (14)</span>
                    <Badge className={`${
                      technical.rsi > 70 ? 'bg-red-100 text-red-800' :
                      technical.rsi > 50 ? 'bg-emerald-100 text-emerald-800' :
                      'bg-slate-100 text-slate-800'
                    }`}>
                      {technical.rsi ? technical.rsi.toFixed(1) : '-'}
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">MACD</span>
                    <span className="font-semibold">{technical.macd ? technical.macd.toFixed(2) : '-'}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">Stochastic %K</span>
                    <span className="font-semibold">{technical.stochastic_k ? technical.stochastic_k.toFixed(1) : '-'}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">VWAP</span>
                    <span className="font-semibold">{technical.vwap ? formatPrice(technical.vwap) : '-'}</span>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
                <CardHeader>
                  <CardTitle>Bollinger Bands</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">Upper Band</span>
                    <span className="font-semibold">{technical.bollinger_upper ? formatPrice(technical.bollinger_upper) : '-'}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">Middle Band</span>
                    <span className="font-semibold">{technical.bollinger_middle ? formatPrice(technical.bollinger_middle) : '-'}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">Lower Band</span>
                    <span className="font-semibold">{technical.bollinger_lower ? formatPrice(technical.bollinger_lower) : '-'}</span>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
                <CardHeader>
                  <CardTitle>Support & Resistance</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">Resistance</span>
                    <span className="font-semibold text-red-600">
                      {technical.resistance_level ? formatPrice(technical.resistance_level) : '-'}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">Support</span>
                    <span className="font-semibold text-emerald-600">
                      {technical.support_level ? formatPrice(technical.support_level) : '-'}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">ATR (14)</span>
                    <span className="font-semibold">{technical.atr ? technical.atr.toFixed(2) : '-'}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">Volume Ratio</span>
                    <span className="font-semibold">
                      {technical.volume_ratio ? `${technical.volume_ratio.toFixed(2)}x` : '-'}
                    </span>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="fundamental">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
                <CardHeader>
                  <CardTitle>Valuation Ratios</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">P/E Ratio</span>
                    <span className="font-semibold">{fundamental.pe_ratio ? fundamental.pe_ratio.toFixed(2) : '-'}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">P/B Ratio</span>
                    <span className="font-semibold">{fundamental.pb_ratio ? fundamental.pb_ratio.toFixed(2) : '-'}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">EPS</span>
                    <span className="font-semibold">{fundamental.eps ? formatPrice(fundamental.eps) : '-'}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">Book Value</span>
                    <span className="font-semibold">{fundamental.book_value ? formatPrice(fundamental.book_value) : '-'}</span>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
                <CardHeader>
                  <CardTitle>Financial Health</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">ROE</span>
                    <span className="font-semibold">
                      {fundamental.roe ? `${(fundamental.roe * 100).toFixed(2)}%` : '-'}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">Debt to Equity</span>
                    <span className="font-semibold">{fundamental.debt_to_equity ? fundamental.debt_to_equity.toFixed(2) : '-'}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">Dividend Yield</span>
                    <span className="font-semibold">
                      {fundamental.dividend_yield ? `${(fundamental.dividend_yield * 100).toFixed(2)}%` : '-'}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">Earnings Growth</span>
                    <span className="font-semibold">
                      {fundamental.earnings_growth ? `${(fundamental.earnings_growth * 100).toFixed(2)}%` : '-'}
                    </span>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="risk">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
                <CardHeader>
                  <CardTitle>Risk Metrics</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">Risk Score</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-24 bg-slate-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${
                            risk?.risk_score <= 3 ? 'bg-emerald-500' :
                            risk?.risk_score <= 6 ? 'bg-amber-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${(risk?.risk_score || 0) * 10}%` }}
                        ></div>
                      </div>
                      <span className="font-semibold">{risk?.risk_score?.toFixed(1) || '-'}/10</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">Volatility</span>
                    <span className="font-semibold">
                      {risk?.volatility ? `${(risk.volatility * 100).toFixed(1)}%` : '-'}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">Beta</span>
                    <span className="font-semibold">{risk?.beta?.toFixed(2) || '-'}</span>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
                <CardHeader>
                  <CardTitle>Risk Factors</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {risk?.risk_factors?.length > 0 ? (
                      risk.risk_factors.map((factor, index) => (
                        <div key={index} className="flex items-center space-x-2">
                          <AlertTriangle className="w-4 h-4 text-amber-600" />
                          <span className="text-sm text-slate-700">{factor}</span>
                        </div>
                      ))
                    ) : (
                      <p className="text-slate-500">No specific risk factors identified</p>
                    )}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="breakout">
            <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
              <CardHeader>
                <CardTitle>Breakout Analysis</CardTitle>
              </CardHeader>
              <CardContent>
                {stockData.breakout_data ? (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-600">Breakout Type</span>
                      <Badge className="bg-emerald-100 text-emerald-800">
                        {stockData.breakout_data.type.replace('_', ' ').toUpperCase()}
                      </Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-slate-600">Breakout Level</span>
                      <span className="font-semibold">{formatPrice(stockData.breakout_data.breakout_price)}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-slate-600">Confidence</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-24 bg-slate-200 rounded-full h-2">
                          <div 
                            className="bg-emerald-500 h-2 rounded-full"
                            style={{ width: `${stockData.breakout_data.confidence * 100}%` }}
                          ></div>
                        </div>
                        <span className="font-semibold">{(stockData.breakout_data.confidence * 100).toFixed(0)}%</span>
                      </div>
                    </div>
                    <div className="mt-4 p-4 bg-emerald-50 rounded-lg">
                      <p className="text-sm text-emerald-800">
                        <strong>Analysis:</strong> This stock is showing strong breakout signals with {(stockData.breakout_data.confidence * 100).toFixed(0)}% confidence. 
                        The breakout above {formatPrice(stockData.breakout_data.breakout_price)} indicates potential for continued upward momentum.
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <AlertTriangle className="w-12 h-12 text-slate-400 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-slate-900 mb-2">No Breakout Detected</h3>
                    <p className="text-slate-600">
                      This stock is not currently showing any breakout patterns. Monitor for future opportunities.
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
};

export default StockDetails;