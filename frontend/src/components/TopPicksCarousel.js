import React, { useState, useEffect, useCallback } from "react";
import { Card, CardContent } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { 
  TrendingUp, TrendingDown, ChevronLeft, ChevronRight, 
  Target, Shield, Sparkles, RefreshCw 
} from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const TopPicksCarousel = ({ onStockClick }) => {
  const [topPicks, setTopPicks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [autoPlay, setAutoPlay] = useState(true);

  const fetchTopPicks = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API}/signals/top-picks`);
      const data = await response.json();
      if (data.top_picks && data.top_picks.length > 0) {
        setTopPicks(data.top_picks);
      }
    } catch (error) {
      console.error("Error fetching top picks:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTopPicks();
    // Refresh top picks every 15 minutes
    const interval = setInterval(fetchTopPicks, 15 * 60 * 1000);
    return () => clearInterval(interval);
  }, [fetchTopPicks]);

  // Auto-rotate carousel every 5 seconds
  useEffect(() => {
    if (!autoPlay || topPicks.length === 0) return;
    
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % topPicks.length);
    }, 5000);
    
    return () => clearInterval(interval);
  }, [autoPlay, topPicks.length]);

  const nextSlide = () => {
    setAutoPlay(false);
    setCurrentIndex((prev) => (prev + 1) % topPicks.length);
  };

  const prevSlide = () => {
    setAutoPlay(false);
    setCurrentIndex((prev) => (prev - 1 + topPicks.length) % topPicks.length);
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 2
    }).format(price);
  };

  const getSignalColor = (signal) => {
    switch (signal) {
      case 'BUY': return 'bg-emerald-500 hover:bg-emerald-600';
      case 'SELL': return 'bg-red-500 hover:bg-red-600';
      default: return 'bg-amber-500 hover:bg-amber-600';
    }
  };

  const getRiskColor = (risk) => {
    switch (risk?.toLowerCase()) {
      case 'low': return 'bg-emerald-100 text-emerald-800';
      case 'high': return 'bg-red-100 text-red-800';
      default: return 'bg-amber-100 text-amber-800';
    }
  };

  if (loading) {
    return (
      <Card className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white">
        <CardContent className="p-6">
          <div className="flex items-center justify-center space-x-2">
            <RefreshCw className="w-5 h-5 animate-spin" />
            <span>Loading top picks...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (topPicks.length === 0) {
    return (
      <Card className="bg-gradient-to-r from-slate-700 to-slate-800 text-white">
        <CardContent className="p-6">
          <div className="flex items-center justify-center space-x-2">
            <Sparkles className="w-5 h-5" />
            <span>No top picks available right now. Add stocks to your watchlist to get personalized recommendations!</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  const currentPick = topPicks[currentIndex];

  return (
    <Card className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white overflow-hidden">
      <CardContent className="p-0">
        {/* Header */}
        <div className="bg-black/20 px-4 py-2 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Sparkles className="w-5 h-5 text-yellow-300" />
            <span className="font-semibold">AI Top Picks</span>
            <Badge variant="secondary" className="bg-white/20 text-white text-xs">
              Updated every 15 min
            </Badge>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-sm text-white/70">
              {currentIndex + 1} / {topPicks.length}
            </span>
            <Button
              size="sm"
              variant="ghost"
              className="text-white hover:bg-white/20 h-7 w-7 p-0"
              onClick={() => setAutoPlay(!autoPlay)}
            >
              {autoPlay ? "⏸" : "▶"}
            </Button>
          </div>
        </div>

        {/* Main Content */}
        <div className="relative p-6">
          {/* Navigation Arrows */}
          <Button
            size="icon"
            variant="ghost"
            className="absolute left-2 top-1/2 -translate-y-1/2 text-white hover:bg-white/20 z-10"
            onClick={prevSlide}
          >
            <ChevronLeft className="w-6 h-6" />
          </Button>
          <Button
            size="icon"
            variant="ghost"
            className="absolute right-2 top-1/2 -translate-y-1/2 text-white hover:bg-white/20 z-10"
            onClick={nextSlide}
          >
            <ChevronRight className="w-6 h-6" />
          </Button>

          {/* Stock Card */}
          <div 
            className="mx-8 cursor-pointer transition-transform hover:scale-[1.02]"
            onClick={() => onStockClick && onStockClick(currentPick.symbol)}
          >
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Left: Stock Info */}
              <div className="space-y-2">
                <div className="flex items-center space-x-3">
                  <Badge className={`${getSignalColor(currentPick.signal)} text-white font-bold px-3 py-1`}>
                    {currentPick.signal}
                  </Badge>
                  <Badge className={getRiskColor(currentPick.risk_level)}>
                    <Shield className="w-3 h-3 mr-1" />
                    {currentPick.risk_level}
                  </Badge>
                </div>
                <h3 className="text-2xl font-bold">{currentPick.symbol}</h3>
                <p className="text-white/80 text-sm">{currentPick.name}</p>
                <Badge variant="outline" className="text-white border-white/30">
                  {currentPick.sector}
                </Badge>
              </div>

              {/* Center: Price Info */}
              <div className="space-y-3 text-center">
                <div>
                  <p className="text-white/70 text-sm">Current Price</p>
                  <p className="text-3xl font-bold">{formatPrice(currentPick.current_price)}</p>
                </div>
                <div className="flex items-center justify-center space-x-4">
                  <div>
                    <p className="text-white/70 text-xs">Target</p>
                    <p className="text-lg font-semibold text-emerald-300 flex items-center">
                      <Target className="w-4 h-4 mr-1" />
                      {formatPrice(currentPick.target_price)}
                    </p>
                  </div>
                  <div className="text-3xl font-bold text-yellow-300">
                    +{currentPick.potential_upside?.toFixed(1)}%
                    <TrendingUp className="w-5 h-5 inline ml-1" />
                  </div>
                </div>
                <div className="flex items-center justify-center">
                  <div className="bg-white/20 rounded-full px-3 py-1">
                    <span className="text-sm">Confidence: </span>
                    <span className="font-bold">{(currentPick.confidence * 100).toFixed(0)}%</span>
                  </div>
                </div>
              </div>

              {/* Right: Reasoning */}
              <div className="bg-white/10 rounded-lg p-4">
                <p className="text-sm font-medium text-white/90 mb-2 flex items-center">
                  <Sparkles className="w-4 h-4 mr-1 text-yellow-300" />
                  Why {currentPick.signal}?
                </p>
                <p className="text-sm text-white/80 leading-relaxed">
                  {currentPick.reasoning}
                </p>
              </div>
            </div>
          </div>

          {/* Dots Indicator */}
          <div className="flex justify-center mt-4 space-x-2">
            {topPicks.map((_, index) => (
              <button
                key={index}
                className={`w-2 h-2 rounded-full transition-all ${
                  index === currentIndex ? 'bg-white w-6' : 'bg-white/40'
                }`}
                onClick={() => {
                  setAutoPlay(false);
                  setCurrentIndex(index);
                }}
              />
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default TopPicksCarousel;
