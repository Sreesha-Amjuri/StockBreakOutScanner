import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, CandlestickChart } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { TrendingUp, TrendingDown, BarChart3 } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_BASE = BACKEND_URL || 'http://localhost:8001';
const API = `${API_BASE}/api`;

const StockChart = ({ symbol, height = 400 }) => {
  const [chartData, setChartData] = useState([]);
  const [timeframe, setTimeframe] = useState('1mo');
  const [loading, setLoading] = useState(false);
  const [indicators, setIndicators] = useState({});

  const timeframes = [
    { value: '5d', label: '5D' },
    { value: '1mo', label: '1M' },
    { value: '3mo', label: '3M' },
    { value: '6mo', label: '6M' },
    { value: '1y', label: '1Y' },
    { value: '2y', label: '2Y' }
  ];

  const fetchChartData = async (tf) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/stocks/${symbol}/chart?timeframe=${tf}`);
      const data = response.data.data.map(item => ({
        ...item,
        date: new Date(item.date).toLocaleDateString(),
        sma20: response.data.indicators.sma_20,
        sma50: response.data.indicators.sma_50,
        sma200: response.data.indicators.sma_200
      }));
      setChartData(data);
      setIndicators(response.data.indicators);
    } catch (error) {
      console.error('Error fetching chart data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (symbol) {
      fetchChartData(timeframe);
    }
  }, [symbol, timeframe]);

  const handleTimeframeChange = (tf) => {
    setTimeframe(tf);
    fetchChartData(tf);
  };

  const formatPrice = (value) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 2
    }).format(value);
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white/95 backdrop-blur-sm p-4 rounded-lg border border-slate-200 shadow-lg">
          <p className="font-semibold text-slate-900 mb-2">{label}</p>
          <div className="space-y-1">
            <p className="text-sm">
              <span className="text-slate-600">Open: </span>
              <span className="font-medium">{formatPrice(data.open)}</span>
            </p>
            <p className="text-sm">
              <span className="text-slate-600">High: </span>
              <span className="font-medium text-emerald-600">{formatPrice(data.high)}</span>
            </p>
            <p className="text-sm">
              <span className="text-slate-600">Low: </span>
              <span className="font-medium text-red-600">{formatPrice(data.low)}</span>
            </p>
            <p className="text-sm">
              <span className="text-slate-600">Close: </span>
              <span className="font-medium">{formatPrice(data.close)}</span>
            </p>
            <p className="text-sm">
              <span className="text-slate-600">Volume: </span>
              <span className="font-medium">{data.volume.toLocaleString()}</span>
            </p>
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center space-x-2">
            <BarChart3 className="w-5 h-5 text-blue-600" />
            <span>{symbol} Chart</span>
          </CardTitle>
          
          <div className="flex items-center space-x-2">
            {/* Technical Indicators */}
            {indicators.rsi && (
              <Badge variant="outline" className={`${
                indicators.rsi > 70 ? 'border-red-200 text-red-700' :
                indicators.rsi > 50 ? 'border-emerald-200 text-emerald-700' :
                'border-slate-200 text-slate-700'
              }`}>
                RSI: {indicators.rsi.toFixed(1)}
              </Badge>
            )}
            
            {indicators.macd && indicators.macd_signal && (
              <Badge variant="outline" className={`${
                indicators.macd > indicators.macd_signal ? 
                'border-emerald-200 text-emerald-700' : 
                'border-red-200 text-red-700'
              }`}>
                MACD: {indicators.macd > indicators.macd_signal ? 'Bullish' : 'Bearish'}
              </Badge>
            )}
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          {timeframes.map((tf) => (
            <Button
              key={tf.value}
              size="sm"
              variant={timeframe === tf.value ? "default" : "outline"}
              onClick={() => handleTimeframeChange(tf.value)}
              className="text-xs"
              disabled={loading}
            >
              {tf.label}
            </Button>
          ))}
        </div>
      </CardHeader>
      
      <CardContent>
        {loading ? (
          <div className="flex items-center justify-center" style={{ height }}>
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <ResponsiveContainer width="100%" height={height}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis 
                dataKey="date" 
                stroke="#64748b"
                fontSize={12}
              />
              <YAxis 
                stroke="#64748b"
                fontSize={12}
                tickFormatter={(value) => `₹${value}`}
              />
              <Tooltip content={<CustomTooltip />} />
              
              {/* Price line */}
              <Line 
                type="monotone" 
                dataKey="close" 
                stroke="#3b82f6" 
                strokeWidth={2}
                dot={false}
                name="Close Price"
              />
              
              {/* Moving averages */}
              {indicators.sma_20 && (
                <Line 
                  type="monotone" 
                  dataKey="sma20" 
                  stroke="#10b981" 
                  strokeWidth={1}
                  strokeDasharray="5 5"
                  dot={false}
                  name="SMA 20"
                />
              )}
              
              {indicators.sma_50 && (
                <Line 
                  type="monotone" 
                  dataKey="sma50" 
                  stroke="#f59e0b" 
                  strokeWidth={1}
                  strokeDasharray="5 5"
                  dot={false}
                  name="SMA 50"
                />
              )}
              
              {indicators.sma_200 && (
                <Line 
                  type="monotone" 
                  dataKey="sma200" 
                  stroke="#ef4444" 
                  strokeWidth={1}
                  strokeDasharray="5 5"
                  dot={false}
                  name="SMA 200"
                />
              )}
            </LineChart>
          </ResponsiveContainer>
        )}
        
        {/* Moving Average Legend */}
        <div className="flex items-center justify-center space-x-6 mt-4 text-sm">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-0.5 bg-blue-600"></div>
            <span className="text-slate-600">Close</span>
          </div>
          {indicators.sma_20 && (
            <div className="flex items-center space-x-2">
              <div className="w-4 h-0.5 bg-emerald-600 border-dashed"></div>
              <span className="text-slate-600">SMA 20</span>
            </div>
          )}
          {indicators.sma_50 && (
            <div className="flex items-center space-x-2">
              <div className="w-4 h-0.5 bg-amber-600 border-dashed"></div>
              <span className="text-slate-600">SMA 50</span>
            </div>
          )}
          {indicators.sma_200 && (
            <div className="flex items-center space-x-2">
              <div className="w-4 h-0.5 bg-red-600 border-dashed"></div>
              <span className="text-slate-600">SMA 200</span>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default StockChart;