import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import "./App.css";
import axios from "axios";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card";
import { Button } from "./components/ui/button";
import { Badge } from "./components/ui/badge";
import { Input } from "./components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./components/ui/table";
import { 
  RefreshCw, TrendingUp, BarChart3, DollarSign, Activity, AlertCircle, 
  Search, Filter, Heart, Star, Eye, Zap, Shield
} from "lucide-react";
import { Toaster } from "./components/ui/sonner";
import { toast } from "sonner";
import StockDetails from "./components/StockDetails";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const navigate = useNavigate();
  // Existing state
  const [breakoutStocks, setBreakoutStocks] = useState([]);
  const [watchlist, setWatchlist] = useState([]);
  const [loading, setLoading] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [sectors, setSectors] = useState([]);
  const [marketOverview, setMarketOverview] = useState(null);

  // Filter states
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSector, setSelectedSector] = useState('All');
  const [minConfidence, setMinConfidence] = useState(0.5);
  const [selectedRiskLevel, setSelectedRiskLevel] = useState('All');

  // Advanced sorting state
  const [sortConfig, setSortConfig] = useState([]);
  const [sortField, setSortField] = useState('confidence_score');
  const [sortDirection, setSortDirection] = useState('desc');

  const fetchMarketOverview = async () => {
    try {
      console.log('Fetching market overview...');
      const response = await axios.get(`${API}/stocks/market-overview`);
      console.log('Market overview response:', response.data);
      setMarketOverview(response.data);
    } catch (error) {
      console.error('Error fetching market overview:', error);
      console.error('Error response:', error.response?.data);
      toast.error("Failed to fetch market overview");
      // Set fallback market overview
      setMarketOverview({
        nifty_50: { current: 24000, change_percent: 0 },
        market_status: { status: "UNKNOWN", message: "Unable to fetch market status" },
        market_sentiment: "Neutral"
      });
    }
  };

  const fetchWatchlist = async () => {
    try {
      const response = await axios.get(`${API}/watchlist`);
      setWatchlist(response.data.watchlist);
    } catch (error) {
      console.error('Error fetching watchlist:', error);
    }
  };

  const fetchSectors = async () => {
    try {
      const response = await axios.get(`${API}/stocks/symbols`);
      setSectors(['All', ...response.data.sectors]);
    } catch (error) {
      console.error('Error fetching sectors:', error);
    }
  };

  const scanBreakouts = async () => {
    if (loading) {
      console.log('Scan already in progress, skipping...');
      return;
    }
    
    setLoading(true);
    try {
      toast.info("Scanning stocks for breakout opportunities...");
      
      const params = new URLSearchParams({
        min_confidence: minConfidence.toString(),
        limit: '100'  // Increased to scan 100 stocks (NIFTY 100)
      });
      
      if (selectedSector !== 'All') {
        params.append('sector', selectedSector);
      }
      
      if (selectedRiskLevel !== 'All') {
        params.append('risk_level', selectedRiskLevel);
      }
      
      console.log('Requesting breakout scan with params:', params.toString());
      
      const response = await axios.get(`${API}/stocks/breakouts/scan?${params}`, {
        timeout: 60000 // 60 second timeout
      });
      
      console.log('Breakout scan response:', response.data);
      console.log('Number of breakouts found:', response.data.breakouts_found);
      console.log('Breakout stocks array length:', response.data.breakout_stocks?.length);
      
      if (response.data && Array.isArray(response.data.breakout_stocks)) {
        setBreakoutStocks(response.data.breakout_stocks);
        setLastUpdated(new Date().toLocaleTimeString());
        
        const count = response.data.breakout_stocks.length;
        if (count > 0) {
          toast.success(`Found ${count} breakout opportunities!`);
        } else {
          toast.info("No breakout opportunities found at current settings");
        }
      } else {
        console.error('Invalid response structure:', response.data);
        toast.error("Invalid response from server");
        setBreakoutStocks([]);
      }
    } catch (error) {
      console.error('Error scanning breakouts:', error);
      console.error('Error response:', error.response?.data);
      
      if (error.code === 'ECONNABORTED') {
        toast.error("Request timeout - server is taking too long");
      } else {
        toast.error(`Failed to scan for breakouts: ${error.message}`);
      }
      setBreakoutStocks([]);
    } finally {
      setLoading(false);
    }
  };

  const searchStocks = async (query) => {
    if (!query.trim()) return;
    
    try {
      const response = await axios.get(`${API}/stocks/search?q=${query}`);
      // You could show search results in a dropdown or modal
      console.log('Search results:', response.data.results);
    } catch (error) {
      console.error('Error searching stocks:', error);
    }
  };

  const addToWatchlist = async (symbol) => {
    try {
      await axios.post(`${API}/watchlist?symbol=${symbol}`);
      await fetchWatchlist();
      toast.success(`Added ${symbol} to watchlist`);
    } catch (error) {
      console.error('Error adding to watchlist:', error);
      toast.error("Failed to add to watchlist");
    }
  };

  const removeFromWatchlist = async (symbol) => {
    try {
      await axios.delete(`${API}/watchlist/${symbol}`);
      await fetchWatchlist();
      toast.success(`Removed ${symbol} from watchlist`);
    } catch (error) {
      console.error('Error removing from watchlist:', error);
      toast.error("Failed to remove from watchlist");
    }
  };

  useEffect(() => {
    const initializeApp = async () => {
      console.log('Initializing app...');
      await fetchMarketOverview();
      await fetchWatchlist();
      await fetchSectors();
      await scanBreakouts();
    };
    
    initializeApp();
  }, []);

  // Combined filtering and sorting logic
  const processedBreakoutStocks = React.useMemo(() => {
    // First apply search filter
    const searchFiltered = breakoutStocks.filter(stock =>
      stock.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
      stock.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
    
    // Then apply sector and risk filters
    const fullyFiltered = searchFiltered.filter(stock => {
      const sectorMatch = selectedSector === 'All' || stock.sector === selectedSector;
      const riskMatch = selectedRiskLevel === 'All' || stock.risk_assessment?.risk_level === selectedRiskLevel;
      return sectorMatch && riskMatch;
    });
    
    // Finally apply sorting if configured
    if (sortConfig.length > 0) {
      return applySorting(fullyFiltered);
    } else {
      // Legacy single-column sorting for backward compatibility
      return [...fullyFiltered].sort((a, b) => {
        let aValue, bValue;

        switch (sortField) {
          case 'symbol':
            aValue = a.symbol;
            bValue = b.symbol;
            break;
          case 'current_price':
            aValue = a.current_price;
            bValue = b.current_price;
            break;
          case 'change_percent':
            aValue = a.change_percent;
            bValue = b.change_percent;
            break;
          case 'entry_price':
            aValue = a.trading_recommendation?.entry_price || 0;
            bValue = b.trading_recommendation?.entry_price || 0;
            break;
          case 'stop_loss':
            aValue = a.trading_recommendation?.stop_loss || 0;
            bValue = b.trading_recommendation?.stop_loss || 0;
            break;
          case 'target_price':
            aValue = a.trading_recommendation?.target_price || 0;
            bValue = b.trading_recommendation?.target_price || 0;
            break;
          case 'action':
            aValue = a.trading_recommendation?.action || 'WAIT';
            bValue = b.trading_recommendation?.action || 'WAIT';
            break;
          case 'risk_reward_ratio':
            aValue = a.trading_recommendation?.risk_reward_ratio || 0;
            bValue = b.trading_recommendation?.risk_reward_ratio || 0;
            break;
          case 'position_size_percent':
            aValue = a.trading_recommendation?.position_size_percent || 0;
            bValue = b.trading_recommendation?.position_size_percent || 0;
            break;
          case 'breakout_type':
            aValue = a.breakout_type;
            bValue = b.breakout_type;
            break;
          case 'confidence_score':
            aValue = a.confidence_score;
            bValue = b.confidence_score;
            break;
          case 'risk_level':
            aValue = a.risk_assessment?.risk_level || 'Medium';
            bValue = b.risk_assessment?.risk_level || 'Medium';
            break;
          case 'rsi':
            aValue = a.technical_data?.rsi || 0;
            bValue = b.technical_data?.rsi || 0;
            break;
          case 'support_level':
            aValue = a.technical_data?.support_level || 0;
            bValue = b.technical_data?.support_level || 0;
            break;
          case 'resistance_level':
            aValue = a.technical_data?.resistance_level || 0;
            bValue = b.technical_data?.resistance_level || 0;
            break;
          case 'sector':
            aValue = a.sector;
            bValue = b.sector;
            break;
          default:
            aValue = a.confidence_score;
            bValue = b.confidence_score;
        }

        // Handle string vs number comparison
        if (typeof aValue === 'string' && typeof bValue === 'string') {
          return sortDirection === 'asc' 
            ? aValue.localeCompare(bValue)
            : bValue.localeCompare(aValue);
        }

        return sortDirection === 'asc' ? aValue - bValue : bValue - aValue;
      });
    }
  }, [breakoutStocks, searchTerm, selectedSector, selectedRiskLevel, sortConfig, sortField, sortDirection, applySorting]);

  const fetchSectors = async () => {
    try {
      const response = await axios.get(`${API}/stocks/symbols`);
      setSectors(['All', ...response.data.sectors]);
    } catch (error) {
      console.error('Error fetching sectors:', error);
    }
  };

  const scanBreakouts = async () => {
    if (loading) {
      return;
    }
    
    setLoading(true);
    try {
      toast.info("Scanning stocks for breakout opportunities...");
      
      const params = new URLSearchParams({
        min_confidence: minConfidence.toString(),
        limit: '100'  // Increased to scan 100 stocks (NIFTY 100)
      });
      
      if (selectedSector !== 'All') {
        params.append('sector', selectedSector);
      }
      
      if (selectedRiskLevel !== 'All') {
        params.append('risk_level', selectedRiskLevel);
      }
      
      console.log('Requesting breakout scan with params:', params.toString());
      
      const response = await axios.get(`${API}/stocks/breakouts/scan`, {
        params: Object.fromEntries(params),
        timeout: 120000 // 2 minute timeout
      });
      
      if (response.data && response.data.breakout_stocks) {
        setBreakoutStocks(response.data.breakout_stocks);
        setLastUpdated(new Date().toLocaleTimeString());
        
        const count = response.data.breakout_stocks.length;
        if (count > 0) {
          toast.success(`Found ${count} breakout opportunities!`);
        } else {
          toast.info("No breakout opportunities found with current filters.");
        }
      }
    } catch (error) {
      console.error('Error scanning breakouts:', error);
      if (error.code === 'ECONNABORTED') {
        toast.error('Request timeout. The scan is taking longer than expected.');
      } else if (error.response?.status === 404) {
        toast.error('API endpoint not found. Please check the backend is running.');
      } else if (error.response?.status >= 500) {
        toast.error('Server error. Please try again later.');
      } else {
        toast.error('Error scanning breakouts. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const addToWatchlist = async (symbol) => {
    try {
      await axios.post(`${API}/watchlist`, null, { 
        params: { symbol }
      });
      
      // Refresh watchlist
      const response = await axios.get(`${API}/watchlist`);
      setWatchlist(response.data.watchlist);
      
      toast.success(`${symbol} added to watchlist`);
    } catch (error) {
      console.error('Error adding to watchlist:', error);
      if (error.response?.data?.detail?.includes('already in watchlist')) {
        toast.warning(`${symbol} is already in your watchlist`);
      } else {
        toast.error('Error adding to watchlist');
      }
    }
  };

  const removeFromWatchlist = async (symbol) => {
    try {
      await axios.delete(`${API}/watchlist/${symbol}`);
      
      // Refresh watchlist
      const response = await axios.get(`${API}/watchlist`);
      setWatchlist(response.data.watchlist);
      
      toast.success(`${symbol} removed from watchlist`);
    } catch (error) {
      console.error('Error removing from watchlist:', error);
      toast.error('Error removing from watchlist');
    }
  };

  // Advanced sorting functions
  const handleSort = (field, event) => {
    // Check if Shift key is held for multi-column sorting
    const isMultiSort = event?.shiftKey;
    
    let newSortConfig = [...sortConfig];
    let newSortDirection = { ...sortDirection };
    
    if (isMultiSort) {
      // Multi-column sorting
      const existingIndex = newSortConfig.findIndex(config => config.field === field);
      
      if (existingIndex >= 0) {
        // Field already in sort config - cycle through directions
        const currentDirection = newSortConfig[existingIndex].direction;
        if (currentDirection === 'asc') {
          newSortConfig[existingIndex].direction = 'desc';
          newSortDirection[field] = 'desc';
        } else if (currentDirection === 'desc') {
          // Remove from sort config
          newSortConfig.splice(existingIndex, 1);
          delete newSortDirection[field];
        }
      } else {
        // Add new field to sort config
        newSortConfig.push({ field, direction: 'asc' });
        newSortDirection[field] = 'asc';
      }
    } else {
      // Single column sorting (replace existing)
      const currentDirection = sortDirection[field];
      const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
      
      newSortConfig = [{ field, direction: newDirection }];
      newSortDirection = { [field]: newDirection };
      
      // Update legacy sort states for backward compatibility
      setSortField(field);
      setSortDirection(newDirection);
    }
    
    setSortConfig(newSortConfig);
    setSortDirection(newSortDirection);
  };

  const getSortValue = (stock, field) => {
    switch (field) {
      case 'symbol':
        return stock.symbol;
      case 'current_price':
        return parseFloat(stock.current_price) || 0;
      case 'change_percent':
        return parseFloat(stock.change_percent) || 0;
      case 'entry_price':
        return parseFloat(stock.trading_recommendation?.entry_price) || 0;
      case 'stop_loss':
        return parseFloat(stock.trading_recommendation?.stop_loss) || 0;
      case 'target_price':
        return parseFloat(stock.trading_recommendation?.target_price) || 0;
      case 'action':
        return stock.trading_recommendation?.action || '';
      case 'risk_reward_ratio':
        return parseFloat(stock.trading_recommendation?.risk_reward_ratio) || 0;
      case 'position_size':
        return parseFloat(stock.trading_recommendation?.position_size_percent) || 0;
      case 'breakout_type':
        return stock.breakout_type || '';
      case 'confidence_score':
        return parseFloat(stock.confidence_score) || 0;
      case 'risk_level':
        return stock.risk_assessment?.risk_level || '';
      case 'rsi':
        return parseFloat(stock.technical_data?.rsi) || 0;
      case 'sector':
        return stock.sector || '';
      default:
        return '';
    }
  };

  const applySorting = (stocks) => {
    if (sortConfig.length === 0) {
      return stocks;
    }

    return [...stocks].sort((a, b) => {
      for (const { field, direction } of sortConfig) {
        const aValue = getSortValue(a, field);
        const bValue = getSortValue(b, field);
        
        let comparison = 0;
        
        if (typeof aValue === 'string' && typeof bValue === 'string') {
          comparison = aValue.localeCompare(bValue);
        } else if (typeof aValue === 'number' && typeof bValue === 'number') {
          comparison = aValue - bValue;
        }
        
        if (comparison !== 0) {
          return direction === 'asc' ? comparison : -comparison;
        }
      }
      return 0;
    });
  };
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
      case 'bollinger_upper': return 'bg-amber-100 text-amber-800 border-amber-200';
      case 'stochastic': return 'bg-pink-100 text-pink-800 border-pink-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getBreakoutTypeLabel = (type) => {
    switch (type) {
      case '200_dma': return '200 DMA';
      case 'resistance': return 'Resistance';
      case 'momentum': return 'Momentum';
      case 'bollinger_upper': return 'Bollinger';
      case 'stochastic': return 'Stochastic';
      default: return type;
    }
  };

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'Low': return 'bg-emerald-100 text-emerald-800 border-emerald-200';
      case 'Medium': return 'bg-amber-100 text-amber-800 border-amber-200';
      case 'High': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getActionColor = (action) => {
    switch (action) {
      case 'BUY': return 'bg-emerald-100 text-emerald-800 border-emerald-200';
      case 'WAIT': return 'bg-amber-100 text-amber-800 border-amber-200';
      case 'AVOID': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  // Advanced sorting functions
  const handleSort = (field, event) => {
    // Check if Shift key is held for multi-column sorting
    const isMultiSort = event?.shiftKey;
    
    let newSortConfig = [...sortConfig];
    let newSortDirection = { ...sortDirection };
    
    if (isMultiSort) {
      // Multi-column sorting
      const existingIndex = newSortConfig.findIndex(config => config.field === field);
      
      if (existingIndex >= 0) {
        // Field already in sort config - cycle through directions
        const currentDirection = newSortConfig[existingIndex].direction;
        if (currentDirection === 'asc') {
          newSortConfig[existingIndex].direction = 'desc';
          newSortDirection[field] = 'desc';
        } else if (currentDirection === 'desc') {
          // Remove from sort config
          newSortConfig.splice(existingIndex, 1);
          delete newSortDirection[field];
        }
      } else {
        // Add new field to sort config
        newSortConfig.push({ field, direction: 'asc' });
        newSortDirection[field] = 'asc';
      }
    } else {
      // Single column sorting (replace existing)
      const currentDirection = sortDirection[field];
      const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
      
      newSortConfig = [{ field, direction: newDirection }];
      newSortDirection = { [field]: newDirection };
      
      // Update legacy sort states for backward compatibility
      setSortField(field);
      setSortDirection(newDirection);
    }
    
    setSortConfig(newSortConfig);
    setSortDirection(newSortDirection);
  };

  const getSortValue = (stock, field) => {
    switch (field) {
      case 'symbol':
        return stock.symbol;
      case 'current_price':
        return parseFloat(stock.current_price) || 0;
      case 'change_percent':
        return parseFloat(stock.change_percent) || 0;
      case 'entry_price':
        return parseFloat(stock.trading_recommendation?.entry_price) || 0;
      case 'stop_loss':
        return parseFloat(stock.trading_recommendation?.stop_loss) || 0;
      case 'target_price':
        return parseFloat(stock.trading_recommendation?.target_price) || 0;
      case 'action':
        return stock.trading_recommendation?.action || '';
      case 'risk_reward_ratio':
        return parseFloat(stock.trading_recommendation?.risk_reward_ratio) || 0;
      case 'position_size':
        return parseFloat(stock.trading_recommendation?.position_size_percent) || 0;
      case 'breakout_type':
        return stock.breakout_type || '';
      case 'confidence_score':
        return parseFloat(stock.confidence_score) || 0;
      case 'risk_level':
        return stock.risk_assessment?.risk_level || '';
      case 'rsi':
        return parseFloat(stock.technical_data?.rsi) || 0;
      case 'sector':
        return stock.sector || '';
      default:
        return '';
    }
  };

  const applySorting = (stocks) => {
    if (sortConfig.length === 0) {
      return stocks;
    }

    return [...stocks].sort((a, b) => {
      for (const { field, direction } of sortConfig) {
        const aValue = getSortValue(a, field);
        const bValue = getSortValue(b, field);
        
        let comparison = 0;
        
        if (typeof aValue === 'string' && typeof bValue === 'string') {
          comparison = aValue.localeCompare(bValue);
        } else if (typeof aValue === 'number' && typeof bValue === 'number') {
          comparison = aValue - bValue;
        }
        
        if (comparison !== 0) {
          return direction === 'asc' ? comparison : -comparison;
        }
      }
      return 0;
    });
  };





  // Get sort icon
  const getSortIcon = (field) => {
    const fieldConfig = sortConfig.find(config => config.field === field);
    if (!fieldConfig) return null;
    
    const sortIndex = sortConfig.findIndex(config => config.field === field);
    const priority = sortConfig.length > 1 ? sortIndex + 1 : null;
    
    return (
      <span className="ml-1 inline-flex items-center">
        {fieldConfig.direction === 'asc' ? '↑' : '↓'}
        {priority && <span className="text-xs ml-1 bg-blue-500 text-white rounded-full w-4 h-4 flex items-center justify-center">{priority}</span>}
      </span>
    );
  };

  const isInWatchlist = (symbol) => {
    return watchlist.some(item => item.symbol === symbol);
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
            
            {/* Search Bar */}
            <div className="flex items-center space-x-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-4 h-4" />
                <Input
                  placeholder="Search stocks..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 w-64"
                />
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
                  
                  {marketOverview.market_status && (
                    <Badge variant={
                      marketOverview.market_status.status === 'OPEN' ? 'default' : 
                      marketOverview.market_status.status === 'PRE_OPEN' ? 'secondary' : 'outline'
                    }>
                      <Activity className="w-3 h-3 mr-1" />
                      {marketOverview.market_status.status}
                    </Badge>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Market Status - Enhanced Display */}
        {marketOverview?.market_status && (
          <Card className="mb-8 bg-white/60 backdrop-blur-sm border-slate-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className={`w-4 h-4 rounded-full ${
                    marketOverview.market_status.status === 'OPEN' ? 'bg-emerald-500 animate-pulse' :
                    marketOverview.market_status.status === 'PRE_OPEN' ? 'bg-amber-500 animate-pulse' :
                    'bg-red-500'
                  }`}></div>
                  <div>
                    <h3 className="text-lg font-semibold text-slate-900">
                      NSE Market Status: {marketOverview.market_status.status}
                    </h3>
                    <p className="text-sm text-slate-600">{marketOverview.market_status.message}</p>
                  </div>
                </div>
                
                <div className="text-right">
                  <p className="text-sm text-slate-600">Current Time (IST)</p>
                  <p className="text-lg font-semibold text-slate-900">
                    {marketOverview.market_status.current_time}
                  </p>
                  {marketOverview.market_status.next_open && (
                    <p className="text-xs text-slate-500">
                      Next: {marketOverview.market_status.next_open}
                    </p>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        )}
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
          <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Breakouts Found</p>
                  <p className="text-2xl font-bold text-slate-900">{processedBreakoutStocks.length}</p>
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
                  <p className="text-2xl font-bold text-slate-900">100</p>
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
                  <p className="text-sm text-slate-600 mb-1">Watchlist</p>
                  <p className="text-2xl font-bold text-slate-900">{watchlist.length}</p>
                </div>
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                  <Heart className="w-6 h-6 text-purple-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Market Sentiment</p>
                  <p className="text-lg font-semibold text-slate-900">
                    {marketOverview?.market_sentiment || 'Neutral'}
                  </p>
                </div>
                <div className="w-12 h-12 bg-amber-100 rounded-lg flex items-center justify-center">
                  <Zap className="w-6 h-6 text-amber-600" />
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

        {/* Filters */}
        <Card className="bg-white/60 backdrop-blur-sm border-slate-200 mb-8">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Filter className="w-5 h-5 text-slate-600" />
              <span>Filters</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700">Sector</label>
                <Select value={selectedSector} onValueChange={setSelectedSector}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select sector" />
                  </SelectTrigger>
                  <SelectContent>
                    {sectors.map(sector => (
                      <SelectItem key={sector} value={sector}>{sector}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700">Min Confidence</label>
                <Select value={minConfidence.toString()} onValueChange={(v) => setMinConfidence(parseFloat(v))}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="0.5">50%</SelectItem>
                    <SelectItem value="0.6">60%</SelectItem>
                    <SelectItem value="0.7">70%</SelectItem>
                    <SelectItem value="0.8">80%</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700">Risk Level</label>
                <Select value={selectedRiskLevel} onValueChange={setSelectedRiskLevel}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="All">All Risk Levels</SelectItem>
                    <SelectItem value="Low">Low Risk</SelectItem>
                    <SelectItem value="Medium">Medium Risk</SelectItem>
                    <SelectItem value="High">High Risk</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="flex items-end">
                <Button 
                  onClick={scanBreakouts}
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-700 hover:to-emerald-800"
                >
                  {loading ? (
                    <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                  ) : (
                    <Search className="w-4 h-4 mr-2" />
                  )}
                  {loading ? 'Scanning...' : 'Apply Filters'}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Breakout Stocks Table */}
        <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <TrendingUp className="w-5 h-5 text-emerald-600" />
                <span>Breakout Opportunities</span>
                {loading && <RefreshCw className="w-4 h-4 animate-spin" />}
              </div>
              <div className="text-sm text-slate-600 font-normal">
                💡 Click column headers to sort • Hold Shift for multi-column sorting
              </div>
            </CardTitle>
          </CardHeader>
          <CardContent>
            {processedBreakoutStocks.length > 0 ? (
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead 
                        className="cursor-pointer hover:bg-slate-100 select-none transition-colors"
                        onClick={(e) => handleSort('symbol', e)}
                      >
                        <div className="flex items-center">
                          Symbol
                          {getSortIcon('symbol')}
                        </div>
                      </TableHead>
                      <TableHead 
                        className="cursor-pointer hover:bg-slate-100 select-none transition-colors"
                        onClick={(e) => handleSort('current_price', e)}
                      >
                        <div className="flex items-center">
                          Current Price
                          {getSortIcon('current_price')}
                        </div>
                      </TableHead>
                      <TableHead 
                        className="cursor-pointer hover:bg-slate-100 select-none transition-colors"
                        onClick={(e) => handleSort('change_percent', e)}
                      >
                        <div className="flex items-center">
                          Change %
                          {getSortIcon('change_percent')}
                        </div>
                      </TableHead>
                      <TableHead 
                        className="cursor-pointer hover:bg-slate-100 select-none transition-colors"
                        onClick={(e) => handleSort('entry_price', e)}
                      >
                        <div className="flex items-center">
                          Entry Price
                          {getSortIcon('entry_price')}
                        </div>
                      </TableHead>
                      <TableHead 
                        className="cursor-pointer hover:bg-slate-100 select-none transition-colors"
                        onClick={(e) => handleSort('stop_loss', e)}
                      >
                        <div className="flex items-center">
                          Stop Loss
                          {getSortIcon('stop_loss')}
                        </div>
                      </TableHead>
                      <TableHead 
                        className="cursor-pointer hover:bg-slate-100 select-none transition-colors"
                        onClick={(e) => handleSort('target_price', e)}
                      >
                        <div className="flex items-center">
                          Target
                          {getSortIcon('target_price')}
                        </div>
                      </TableHead>
                      <TableHead 
                        className="cursor-pointer hover:bg-slate-100 select-none transition-colors"
                        onClick={(e) => handleSort('action', e)}
                      >
                        <div className="flex items-center">
                          Action
                          {getSortIcon('action')}
                        </div>
                      </TableHead>
                      <TableHead 
                        className="cursor-pointer hover:bg-slate-100 select-none transition-colors"
                        onClick={(e) => handleSort('risk_reward_ratio', e)}
                      >
                        <div className="flex items-center">
                          Risk:Reward
                          {getSortIcon('risk_reward_ratio')}
                        </div>
                      </TableHead>
                      <TableHead 
                        className="cursor-pointer hover:bg-slate-100 select-none transition-colors"
                        onClick={(e) => handleSort('position_size', e)}
                      >
                        <div className="flex items-center">
                          Position Size
                          {getSortIcon('position_size')}
                        </div>
                      </TableHead>
                      <TableHead 
                        className="cursor-pointer hover:bg-slate-100 select-none transition-colors"
                        onClick={(e) => handleSort('breakout_type', e)}
                      >
                        <div className="flex items-center">
                          Breakout Type
                          {getSortIcon('breakout_type')}
                        </div>
                      </TableHead>
                      <TableHead 
                        className="cursor-pointer hover:bg-slate-100 select-none transition-colors"
                        onClick={(e) => handleSort('confidence_score', e)}
                      >
                        <div className="flex items-center">
                          Confidence
                          {getSortIcon('confidence_score')}
                        </div>
                      </TableHead>
                      <TableHead 
                        className="cursor-pointer hover:bg-slate-100 select-none transition-colors"
                        onClick={(e) => handleSort('risk_level', e)}
                      >
                        <div className="flex items-center">
                          Risk Level
                          {getSortIcon('risk_level')}
                        </div>
                      </TableHead>
                      <TableHead 
                        className="cursor-pointer hover:bg-slate-100 select-none transition-colors"
                        onClick={(e) => handleSort('rsi', e)}
                      >
                        <div className="flex items-center">
                          RSI
                          {getSortIcon('rsi')}
                        </div>
                      </TableHead>
                      <TableHead 
                        className="cursor-pointer hover:bg-slate-100 select-none transition-colors"
                        onClick={(e) => handleSort('sector', e)}
                      >
                        <div className="flex items-center">
                          Sector
                          {getSortIcon('sector')}
                        </div>
                      </TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {processedBreakoutStocks.map((stock, index) => {
                      const trading = stock.trading_recommendation;
                      return (
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
                          <TableCell className="font-semibold text-blue-600">
                            {trading ? formatPrice(trading.entry_price) : '-'}
                          </TableCell>
                          <TableCell className="font-semibold text-red-600">
                            {trading ? formatPrice(trading.stop_loss) : '-'}
                          </TableCell>
                          <TableCell className="font-semibold text-emerald-600">
                            {trading ? formatPrice(trading.target_price) : '-'}
                          </TableCell>
                          <TableCell>
                            {trading ? (
                              <Badge className={getActionColor(trading.action)}>
                                {trading.action}
                              </Badge>
                            ) : '-'}
                          </TableCell>
                          <TableCell className="font-medium">
                            {trading ? `1:${trading.risk_reward_ratio}` : '-'}
                          </TableCell>
                          <TableCell className="font-medium">
                            {trading ? `${trading.position_size_percent}%` : '-'}
                          </TableCell>
                          <TableCell>
                            <Badge className={getBreakoutTypeColor(stock.breakout_type)}>
                              {getBreakoutTypeLabel(stock.breakout_type)}
                            </Badge>
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
                          <TableCell>
                            <Badge className={getRiskColor(stock.risk_assessment?.risk_level)}>
                              <Shield className="w-3 h-3 mr-1" />
                              {stock.risk_assessment?.risk_level || 'Medium'}
                            </Badge>
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
                            <Badge variant="outline" className="text-xs">
                              {stock.sector}
                            </Badge>
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center space-x-2">
                              <Button 
                                size="sm" 
                                variant="outline" 
                                onClick={() => navigate(`/stock/${stock.symbol}`)}
                                className="text-xs"
                              >
                                <Eye className="w-3 h-3 mr-1" />
                                View
                              </Button>
                              <Button
                                size="sm"
                                variant={isInWatchlist(stock.symbol) ? "default" : "outline"}
                                onClick={() => 
                                  isInWatchlist(stock.symbol) 
                                    ? removeFromWatchlist(stock.symbol)
                                    : addToWatchlist(stock.symbol)
                                }
                                className="text-xs"
                              >
                                <Heart className={`w-3 h-3 ${isInWatchlist(stock.symbol) ? 'fill-current' : ''}`} />
                              </Button>
                            </div>
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </div>
            ) : (
              <div className="text-center py-12">
                <AlertCircle className="w-12 h-12 text-slate-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-slate-900 mb-2">No Breakouts Found</h3>
                <p className="text-slate-600 mb-4">
                  {loading ? "Scanning stocks for breakout opportunities..." : "No stocks match your current filters."}
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

        {/* Sector Performance */}
        {marketOverview?.sector_performance && (
          <Card className="mt-8 bg-white/60 backdrop-blur-sm border-slate-200">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BarChart3 className="w-5 h-5 text-blue-600" />
                <span>Sector Performance</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                {Object.entries(marketOverview.sector_performance).map(([sector, performance]) => (
                  <div key={sector} className="text-center">
                    <p className="text-sm font-medium text-slate-700 mb-1">{sector}</p>
                    <p className={`text-lg font-bold ${
                      performance >= 0 ? 'text-emerald-600' : 'text-red-600'
                    }`}>
                      {performance >= 0 ? '+' : ''}{performance.toFixed(2)}%
                    </p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

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
                  Invest only what you can afford to lose. All risk assessments are algorithmic and should not be 
                  considered as professional financial advice.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/stock/:symbol" element={<StockDetails />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;