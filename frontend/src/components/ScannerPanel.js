import React, { useState, useEffect, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { Progress } from "./ui/progress";
import {
  Zap, Clock, RefreshCw, TrendingUp, Filter, BarChart3,
  ChevronDown, ChevronUp, AlertCircle
} from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ScannerPanel = ({ onStockClick }) => {
  const [scanType, setScanType] = useState("quick"); // "quick" or "full"
  const [isScanning, setIsScanning] = useState(false);
  const [progress, setProgress] = useState(null);
  const [results, setResults] = useState([]);
  const [scanStats, setScanStats] = useState({ scanned: 0, found: 0, time: 0 });
  const [showFilters, setShowFilters] = useState(false);
  
  // Filters
  const [minConfidence, setMinConfidence] = useState(0.5);
  const [sector, setSector] = useState("All");

  // Poll for progress during full scan
  useEffect(() => {
    let interval;
    if (isScanning && scanType === "full") {
      interval = setInterval(async () => {
        try {
          const response = await fetch(`${API}/stocks/scan/progress`);
          const data = await response.json();
          setProgress(data);
          
          if (!data.is_scanning) {
            // Scan complete, get results
            const resultsResponse = await fetch(`${API}/stocks/breakouts/full-scan/results`);
            const resultsData = await resultsResponse.json();
            setResults(resultsData.breakouts || []);
            setScanStats({
              scanned: resultsData.total_scanned,
              found: resultsData.breakouts_found,
              time: 0
            });
            setIsScanning(false);
            clearInterval(interval);
          }
        } catch (error) {
          console.error("Progress poll error:", error);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [isScanning, scanType]);

  const runQuickScan = async () => {
    setIsScanning(true);
    setResults([]);
    
    try {
      const params = new URLSearchParams({
        min_confidence: minConfidence.toString(),
        ...(sector !== "All" && { sector })
      });
      
      const response = await fetch(`${API}/stocks/breakouts/quick-scan?${params}`);
      const data = await response.json();
      
      setResults(data.breakouts || []);
      setScanStats({
        scanned: data.total_scanned,
        found: data.breakouts_found,
        time: data.scan_time_seconds
      });
    } catch (error) {
      console.error("Quick scan error:", error);
    } finally {
      setIsScanning(false);
    }
  };

  const startFullScan = async () => {
    setIsScanning(true);
    setResults([]);
    setProgress(null);
    
    try {
      const params = new URLSearchParams({
        min_confidence: minConfidence.toString(),
        limit: "150",
        ...(sector !== "All" && { sector })
      });
      
      await fetch(`${API}/stocks/breakouts/full-scan/start?${params}`, {
        method: "POST"
      });
      
      // Progress polling will handle the rest
    } catch (error) {
      console.error("Full scan start error:", error);
      setIsScanning(false);
    }
  };

  const handleScan = () => {
    if (scanType === "quick") {
      runQuickScan();
    } else {
      startFullScan();
    }
  };

  const formatPrice = (price) => {
    if (!price) return "—";
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      minimumFractionDigits: 2,
    }).format(price);
  };

  const getActionColor = (action) => {
    switch (action) {
      case "BUY": return "bg-emerald-500 text-white";
      case "SELL": return "bg-red-500 text-white";
      default: return "bg-amber-500 text-white";
    }
  };

  const getRiskColor = (risk) => {
    switch (risk?.toLowerCase()) {
      case "low": return "bg-emerald-100 text-emerald-800";
      case "high": return "bg-red-100 text-red-800";
      default: return "bg-amber-100 text-amber-800";
    }
  };

  return (
    <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <BarChart3 className="w-5 h-5 text-blue-600" />
            <span>Breakout Scanner</span>
          </div>
          <Button
            size="sm"
            variant="ghost"
            onClick={() => setShowFilters(!showFilters)}
          >
            <Filter className="w-4 h-4 mr-1" />
            Filters
            {showFilters ? <ChevronUp className="w-4 h-4 ml-1" /> : <ChevronDown className="w-4 h-4 ml-1" />}
          </Button>
        </CardTitle>

        {/* Scan Type Toggle */}
        <div className="flex space-x-2 mt-3">
          <Button
            size="sm"
            variant={scanType === "quick" ? "default" : "outline"}
            onClick={() => setScanType("quick")}
            disabled={isScanning}
            className={scanType === "quick" ? "bg-blue-600" : ""}
          >
            <Zap className="w-4 h-4 mr-1" />
            Quick Scan (30 stocks)
          </Button>
          <Button
            size="sm"
            variant={scanType === "full" ? "default" : "outline"}
            onClick={() => setScanType("full")}
            disabled={isScanning}
            className={scanType === "full" ? "bg-purple-600" : ""}
          >
            <Clock className="w-4 h-4 mr-1" />
            Full Scan (150 stocks)
          </Button>
        </div>

        {/* Filters Panel */}
        {showFilters && (
          <div className="mt-3 p-3 bg-slate-50 rounded-lg grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs font-medium text-slate-600">Min Confidence</label>
              <select
                value={minConfidence}
                onChange={(e) => setMinConfidence(parseFloat(e.target.value))}
                className="w-full mt-1 px-2 py-1 text-sm border rounded"
              >
                <option value="0.3">30%</option>
                <option value="0.5">50%</option>
                <option value="0.6">60%</option>
                <option value="0.7">70%</option>
              </select>
            </div>
            <div>
              <label className="text-xs font-medium text-slate-600">Sector</label>
              <select
                value={sector}
                onChange={(e) => setSector(e.target.value)}
                className="w-full mt-1 px-2 py-1 text-sm border rounded"
              >
                <option value="All">All Sectors</option>
                <option value="IT">IT</option>
                <option value="Banking">Banking</option>
                <option value="Auto">Auto</option>
                <option value="Pharma">Pharma</option>
                <option value="FMCG">FMCG</option>
              </select>
            </div>
          </div>
        )}

        {/* Scan Button */}
        <Button
          onClick={handleScan}
          disabled={isScanning}
          className="w-full mt-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
        >
          {isScanning ? (
            <>
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
              Scanning...
            </>
          ) : (
            <>
              <TrendingUp className="w-4 h-4 mr-2" />
              Start {scanType === "quick" ? "Quick" : "Full"} Scan
            </>
          )}
        </Button>

        {/* Progress Bar for Full Scan */}
        {isScanning && scanType === "full" && progress && (
          <div className="mt-3 space-y-2">
            <div className="flex justify-between text-sm text-slate-600">
              <span>Scanning {progress.scanned_stocks} / {progress.total_stocks} stocks</span>
              <span>{progress.progress_percent}%</span>
            </div>
            <Progress value={progress.progress_percent} className="h-2" />
            <div className="flex justify-between text-xs text-slate-500">
              <span>Breakouts found: {progress.breakouts_found}</span>
              {progress.estimated_time_remaining && (
                <span>~{Math.ceil(progress.estimated_time_remaining / 60)} min remaining</span>
              )}
            </div>
          </div>
        )}

        {/* Scan Stats */}
        {!isScanning && scanStats.scanned > 0 && (
          <div className="mt-3 flex items-center justify-between text-sm bg-slate-50 rounded-lg p-2">
            <span className="text-slate-600">
              Scanned: <strong>{scanStats.scanned}</strong> stocks
            </span>
            <span className="text-emerald-600">
              Found: <strong>{scanStats.found}</strong> breakouts
            </span>
            {scanStats.time > 0 && (
              <span className="text-slate-500">
                Time: {scanStats.time.toFixed(1)}s
              </span>
            )}
          </div>
        )}
      </CardHeader>

      <CardContent className="pt-0">
        {/* Results */}
        {results.length === 0 && !isScanning ? (
          <div className="text-center py-8 text-slate-500">
            <AlertCircle className="w-10 h-10 mx-auto mb-2 text-slate-400" />
            <p>No breakouts found yet</p>
            <p className="text-sm mt-1">Click scan to find breakout opportunities</p>
          </div>
        ) : (
          <div className="space-y-2 max-h-[400px] overflow-y-auto">
            {results.map((stock, index) => (
              <div
                key={stock.symbol + index}
                onClick={() => onStockClick && onStockClick(stock.symbol)}
                className="p-3 bg-white rounded-lg border border-slate-200 hover:border-blue-300 cursor-pointer transition-all hover:shadow-sm"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className="flex items-center space-x-2">
                      <span className="font-semibold text-slate-900">{stock.symbol}</span>
                      <Badge className={getActionColor(stock.action)}>
                        {stock.action || "WAIT"}
                      </Badge>
                      <Badge className={getRiskColor(stock.risk_level)}>
                        {stock.risk_level}
                      </Badge>
                    </div>
                    <p className="text-xs text-slate-500 mt-1">
                      {stock.breakout_type} • Confidence: {(stock.confidence_score * 100).toFixed(0)}%
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-slate-900">{formatPrice(stock.current_price)}</p>
                    <p className={`text-xs ${stock.change_percent >= 0 ? "text-emerald-600" : "text-red-600"}`}>
                      {stock.change_percent >= 0 ? "+" : ""}{stock.change_percent?.toFixed(2)}%
                    </p>
                    {stock.potential_return > 0 && (
                      <p className="text-xs text-blue-600">
                        Target: +{stock.potential_return?.toFixed(1)}%
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default ScannerPanel;
