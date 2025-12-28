import React, { useState, useEffect, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { 
  TrendingUp, TrendingDown, Minus, RefreshCw, Target, 
  Shield, Clock, Eye, Sparkles, ArrowUpRight, ArrowDownRight
} from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const SignalsPanel = ({ onStockClick }) => {
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [nextUpdateIn, setNextUpdateIn] = useState(null);
  const [filter, setFilter] = useState('ALL');

  const fetchSignals = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API}/signals/watchlist`);
      const data = await response.json();
      
      if (data.signals) {
        setSignals(data.signals);
        setLastUpdate(data.timestamp);
        if (data.next_update_in_seconds) {
          setNextUpdateIn(data.next_update_in_seconds);
        }
      }
    } catch (error) {
      console.error("Error fetching signals:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  const refreshSignals = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API}/signals/refresh`, { method: 'POST' });
      const data = await response.json();
      if (data.success) {
        await fetchSignals();
      }
    } catch (error) {
      console.error("Error refreshing signals:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSignals();
    // Refresh every 5 minutes to check for updates
    const interval = setInterval(fetchSignals, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, [fetchSignals]);

  // Countdown timer for next update
  useEffect(() => {
    if (!nextUpdateIn) return;
    
    const interval = setInterval(() => {
      setNextUpdateIn((prev) => {
        if (prev <= 1) {
          fetchSignals();
          return null;
        }
        return prev - 1;
      });
    }, 1000);
    
    return () => clearInterval(interval);
  }, [nextUpdateIn, fetchSignals]);

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 2
    }).format(price);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getSignalIcon = (signal) => {
    switch (signal) {
      case 'BUY': return <TrendingUp className="w-4 h-4" />;
      case 'SELL': return <TrendingDown className="w-4 h-4" />;
      default: return <Minus className="w-4 h-4" />;
    }
  };

  const getSignalColor = (signal) => {
    switch (signal) {
      case 'BUY': return 'bg-emerald-500 text-white';
      case 'SELL': return 'bg-red-500 text-white';
      default: return 'bg-amber-500 text-white';
    }
  };

  const getSignalBgColor = (signal) => {
    switch (signal) {
      case 'BUY': return 'bg-emerald-50 border-emerald-200 hover:bg-emerald-100';
      case 'SELL': return 'bg-red-50 border-red-200 hover:bg-red-100';
      default: return 'bg-amber-50 border-amber-200 hover:bg-amber-100';
    }
  };

  const getRiskColor = (risk) => {
    switch (risk?.toLowerCase()) {
      case 'low': return 'bg-emerald-100 text-emerald-800';
      case 'high': return 'bg-red-100 text-red-800';
      default: return 'bg-amber-100 text-amber-800';
    }
  };

  const filteredSignals = signals.filter(s => {
    if (filter === 'ALL') return true;
    return s.signal === filter;
  });

  const signalCounts = {
    ALL: signals.length,
    BUY: signals.filter(s => s.signal === 'BUY').length,
    SELL: signals.filter(s => s.signal === 'SELL').length,
    HOLD: signals.filter(s => s.signal === 'HOLD').length,
  };

  return (
    <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center space-x-2">
            <Sparkles className="w-5 h-5 text-purple-600" />
            <span>Dynamic Signals</span>
            <Badge variant="secondary" className="text-xs">
              Auto-updates every 15 min
            </Badge>
          </CardTitle>
          <div className="flex items-center space-x-2">
            {nextUpdateIn && (
              <Badge variant="outline" className="text-xs">
                <Clock className="w-3 h-3 mr-1" />
                Next: {formatTime(nextUpdateIn)}
              </Badge>
            )}
            <Button 
              size="sm" 
              variant="outline" 
              onClick={refreshSignals}
              disabled={loading}
            >
              <RefreshCw className={`w-4 h-4 mr-1 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
          </div>
        </div>
        
        {/* Filter Tabs */}
        <div className="flex space-x-2 mt-3">
          {['ALL', 'BUY', 'SELL', 'HOLD'].map((f) => (
            <Button
              key={f}
              size="sm"
              variant={filter === f ? 'default' : 'outline'}
              onClick={() => setFilter(f)}
              className={filter === f ? getSignalColor(f === 'ALL' ? 'default' : f).replace('text-white', '') : ''}
            >
              {f} ({signalCounts[f]})
            </Button>
          ))}
        </div>
      </CardHeader>
      
      <CardContent className="pt-2">
        {loading && signals.length === 0 ? (
          <div className="flex items-center justify-center py-8">
            <RefreshCw className="w-6 h-6 animate-spin text-slate-400 mr-2" />
            <span className="text-slate-500">Analyzing your watchlist...</span>
          </div>
        ) : filteredSignals.length === 0 ? (
          <div className="text-center py-8 text-slate-500">
            <Sparkles className="w-10 h-10 mx-auto mb-2 text-slate-400" />
            <p>No {filter !== 'ALL' ? filter : ''} signals available</p>
            <p className="text-sm mt-1">Add stocks to your watchlist to see signals</p>
          </div>
        ) : (
          <div className="space-y-3 max-h-[500px] overflow-y-auto">
            {filteredSignals.map((signal, index) => (
              <div
                key={signal.symbol + index}
                className={`p-4 rounded-lg border cursor-pointer transition-all ${getSignalBgColor(signal.signal)}`}
                onClick={() => onStockClick && onStockClick(signal.symbol)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <Badge className={`${getSignalColor(signal.signal)} font-bold`}>
                        {getSignalIcon(signal.signal)}
                        <span className="ml-1">{signal.signal}</span>
                      </Badge>
                      <span className="font-bold text-lg">{signal.symbol}</span>
                      <Badge className={getRiskColor(signal.risk_level)}>
                        <Shield className="w-3 h-3 mr-1" />
                        {signal.risk_level}
                      </Badge>
                    </div>
                    
                    <p className="text-sm text-slate-600 mb-2">{signal.name}</p>
                    
                    {/* Reasoning Box */}
                    <div className="bg-white/60 rounded-md p-3 mb-3">
                      <p className="text-sm font-medium text-slate-700 flex items-center mb-1">
                        <Sparkles className="w-4 h-4 mr-1 text-purple-500" />
                        AI Analysis:
                      </p>
                      <p className="text-sm text-slate-600">{signal.reasoning}</p>
                    </div>
                    
                    {/* Technical Summary */}
                    <p className="text-xs text-slate-500">{signal.technical_summary}</p>
                  </div>
                  
                  <div className="text-right ml-4">
                    <p className="text-xl font-bold">{formatPrice(signal.current_price)}</p>
                    <div className="flex items-center justify-end mt-1">
                      <Target className="w-4 h-4 text-emerald-600 mr-1" />
                      <span className="text-sm text-emerald-600 font-medium">
                        {formatPrice(signal.target_price)}
                      </span>
                    </div>
                    {signal.potential_return > 0 ? (
                      <div className="flex items-center justify-end text-emerald-600">
                        <ArrowUpRight className="w-4 h-4" />
                        <span className="text-sm font-bold">+{signal.potential_return}%</span>
                      </div>
                    ) : (
                      <div className="flex items-center justify-end text-red-600">
                        <ArrowDownRight className="w-4 h-4" />
                        <span className="text-sm font-bold">{signal.potential_return}%</span>
                      </div>
                    )}
                    <div className="mt-2">
                      <div className="text-xs text-slate-500">Confidence</div>
                      <div className="flex items-center justify-end">
                        <div className="w-16 bg-slate-200 rounded-full h-2 mr-2">
                          <div 
                            className="bg-purple-500 h-2 rounded-full"
                            style={{ width: `${signal.confidence * 100}%` }}
                          />
                        </div>
                        <span className="text-sm font-medium">{(signal.confidence * 100).toFixed(0)}%</span>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center justify-between mt-3 pt-3 border-t border-slate-200">
                  <span className="text-xs text-slate-400">
                    Stop Loss: {formatPrice(signal.stop_loss)}
                  </span>
                  <Button size="sm" variant="ghost" className="h-7 text-xs">
                    <Eye className="w-3 h-3 mr-1" />
                    View Details
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default SignalsPanel;
