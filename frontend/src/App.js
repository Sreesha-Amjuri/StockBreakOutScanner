import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card";
import { Button } from "./components/ui/button";
import { Badge } from "./components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./components/ui/table";
import { RefreshCw, TrendingUp, BarChart3, DollarSign, Activity, AlertCircle } from "lucide-react";
import { Toaster } from "./components/ui/sonner";
import { toast } from "sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [breakoutStocks, setBreakoutStocks] = useState([]);
  const [marketOverview, setMarketOverview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchMarketOverview = async () => {
    try {
      const response = await axios.get(`${API}/stocks/market-overview`);
      setMarketOverview(response.data);
    } catch (error) {
      console.error('Error fetching market overview:', error);
      toast.error("Failed to fetch market overview");
    }
  };

  const scanBreakouts = async () => {
    setLoading(true);
    try {
      toast.info("Scanning stocks for breakout opportunities...");
      const response = await axios.get(`${API}/stocks/breakouts/scan`);
      setBreakoutStocks(response.data.breakout_stocks);
      setLastUpdated(new Date().toLocaleTimeString());
      toast.success(`Found ${response.data.breakouts_found} breakout opportunities!`);
    } catch (error) {
      console.error('Error scanning breakouts:', error);
      toast.error("Failed to scan for breakouts");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMarketOverview();
    scanBreakouts();
  }, []);

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

  const getBreakoutTypeColor = (type) => {
    switch (type) {
      case '200_dma': return 'bg-emerald-100 text-emerald-800 border-emerald-200';
      case 'resistance': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'momentum': return 'bg-purple-100 text-purple-800 border-purple-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getBreakoutTypeLabel = (type) => {
    switch (type) {
      case '200_dma': return '200 DMA Breakout';
      case 'resistance': return 'Resistance Breakout';
      case 'momentum': return 'Momentum Breakout';
      default: return type;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <Toaster />
      
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-slate-900">StockBreak Pro</h1>
                <p className="text-sm text-slate-600">NSE Breakout Screener</p>
              </div>
            </div>
            
            {marketOverview && (
              <div className="flex items-center space-x-6">
                <div className="text-right">
                  <p className="text-sm text-slate-600">NIFTY 50</p>
                  <div className="flex items-center space-x-2">
                    <span className="font-semibold text-slate-900">
                      {marketOverview.nifty_50.current.toFixed(2)}
                    </span>
                    <span className={`text-sm font-medium ${
                      marketOverview.nifty_50.change_percent >= 0 ? 'text-emerald-600' : 'text-red-600'
                    }`}>
                      {marketOverview.nifty_50.change_percent >= 0 ? '+' : ''}
                      {marketOverview.nifty_50.change_percent.toFixed(2)}%
                    </span>
                  </div>
                </div>
                
                <Badge variant={marketOverview.market_status === 'Open' ? 'default' : 'secondary'}>
                  <Activity className="w-3 h-3 mr-1" />
                  {marketOverview.market_status}
                </Badge>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Breakouts Found</p>
                  <p className="text-2xl font-bold text-slate-900">{breakoutStocks.length}</p>
                </div>
                <div className="w-12 h-12 bg-emerald-100 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-emerald-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Stocks Scanned</p>
                  <p className="text-2xl font-bold text-slate-900">20</p>
                </div>
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <BarChart3 className="w-6 h-6 text-blue-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Success Rate</p>
                  <p className="text-2xl font-bold text-slate-900">
                    {breakoutStocks.length > 0 ? ((breakoutStocks.length / 20) * 100).toFixed(0) : 0}%
                  </p>
                </div>
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                  <DollarSign className="w-6 h-6 text-purple-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Last Updated</p>
                  <p className="text-lg font-semibold text-slate-900">{lastUpdated || '--:--'}</p>
                </div>
                <Button 
                  onClick={scanBreakouts} 
                  disabled={loading}
                  size="sm"
                  className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
                >
                  <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Breakout Stocks Table */}
        <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <TrendingUp className="w-5 h-5 text-emerald-600" />
              <span>Breakout Opportunities</span>
              {loading && <RefreshCw className="w-4 h-4 animate-spin" />}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {breakoutStocks.length > 0 ? (
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Symbol</TableHead>
                      <TableHead>Current Price</TableHead>
                      <TableHead>Change %</TableHead>
                      <TableHead>Breakout Type</TableHead>
                      <TableHead>Breakout Level</TableHead>
                      <TableHead>Confidence</TableHead>
                      <TableHead>Volume</TableHead>
                      <TableHead>RSI</TableHead>
                      <TableHead>Action</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {breakoutStocks.map((stock, index) => (
                      <TableRow key={index} className="hover:bg-slate-50/50">
                        <TableCell>
                          <div>
                            <span className="font-semibold text-slate-900">{stock.symbol}</span>
                            <p className="text-sm text-slate-600 truncate max-w-32">{stock.name}</p>
                          </div>
                        </TableCell>
                        <TableCell className="font-semibold">
                          {formatPrice(stock.current_price)}
                        </TableCell>
                        <TableCell>
                          <span className={`font-medium ${
                            stock.change_percent >= 0 ? 'text-emerald-600' : 'text-red-600'
                          }`}>
                            {stock.change_percent >= 0 ? '+' : ''}
                            {stock.change_percent.toFixed(2)}%
                          </span>
                        </TableCell>
                        <TableCell>
                          <Badge className={getBreakoutTypeColor(stock.breakout_type)}>
                            {getBreakoutTypeLabel(stock.breakout_type)}
                          </Badge>
                        </TableCell>
                        <TableCell className="font-medium">
                          {formatPrice(stock.breakout_price)}
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center space-x-2">
                            <div className="w-full bg-slate-200 rounded-full h-2">
                              <div 
                                className="bg-gradient-to-r from-emerald-500 to-emerald-600 h-2 rounded-full" 
                                style={{ width: `${stock.confidence_score * 100}%` }}
                              ></div>
                            </div>
                            <span className="text-sm font-medium text-slate-700">
                              {(stock.confidence_score * 100).toFixed(0)}%
                            </span>
                          </div>
                        </TableCell>
                        <TableCell className="text-sm">
                          {formatLargeNumber(stock.volume)}
                        </TableCell>
                        <TableCell>
                          <span className={`font-medium ${
                            stock.technical_data.rsi > 70 ? 'text-red-600' : 
                            stock.technical_data.rsi > 50 ? 'text-emerald-600' : 'text-slate-600'
                          }`}>
                            {stock.technical_data.rsi ? stock.technical_data.rsi.toFixed(1) : '-'}
                          </span>
                        </TableCell>
                        <TableCell>
                          <Button size="sm" variant="outline" className="text-xs">
                            View Details
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            ) : (
              <div className="text-center py-12">
                <AlertCircle className="w-12 h-12 text-slate-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-slate-900 mb-2">No Breakouts Found</h3>
                <p className="text-slate-600 mb-4">
                  {loading ? "Scanning stocks for breakout opportunities..." : "No stocks are showing breakout signals at the moment."}
                </p>
                <Button 
                  onClick={scanBreakouts} 
                  disabled={loading}
                  className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
                >
                  <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                  {loading ? 'Scanning...' : 'Scan Now'}
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Disclaimer */}
        <Card className="mt-8 bg-amber-50/50 border-amber-200">
          <CardContent className="p-4">
            <div className="flex items-start space-x-3">
              <AlertCircle className="w-5 h-5 text-amber-600 mt-0.5" />
              <div>
                <h4 className="font-semibold text-amber-900 mb-1">Investment Disclaimer</h4>
                <p className="text-sm text-amber-800">
                  This tool is for educational purposes only. Past performance does not guarantee future results. 
                  Always consult with a qualified financial advisor before making investment decisions. 
                  Invest only what you can afford to lose.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}

export default App;