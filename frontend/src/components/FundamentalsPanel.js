import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Progress } from "./ui/progress";
import {
  TrendingUp, DollarSign, PieChart, BarChart3, 
  AlertCircle, RefreshCw, CheckCircle
} from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const FundamentalsPanel = ({ symbol }) => {
  const [fundamentals, setFundamentals] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!symbol) return;

    const fetchFundamentals = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`${API}/stocks/${symbol}/fundamentals`);
        if (!response.ok) throw new Error("Failed to fetch");
        const data = await response.json();
        setFundamentals(data);
      } catch (err) {
        setError("Unable to fetch fundamentals");
        console.error("Fundamentals error:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchFundamentals();
  }, [symbol]);

  const formatValue = (value, type = "number") => {
    if (value === null || value === undefined) return "—";

    switch (type) {
      case "currency":
        return new Intl.NumberFormat("en-IN", {
          style: "currency",
          currency: "INR",
          notation: "compact",
          maximumFractionDigits: 2,
        }).format(value);
      case "percent":
        return `${value >= 0 ? "+" : ""}${value.toFixed(2)}%`;
      case "ratio":
        return value.toFixed(2);
      default:
        return typeof value === "number" ? value.toFixed(2) : value;
    }
  };

  const getRatingColor = (rating) => {
    switch (rating) {
      case "Excellent":
        return "bg-emerald-500 text-white";
      case "Good":
        return "bg-blue-500 text-white";
      case "Average":
        return "bg-amber-500 text-white";
      default:
        return "bg-red-500 text-white";
    }
  };

  const getMetricColor = (value, metric) => {
    if (value === null || value === undefined) return "text-slate-400";

    switch (metric) {
      case "pe":
        return value < 15 ? "text-emerald-600" : value < 25 ? "text-amber-600" : "text-red-600";
      case "roe":
        return value > 20 ? "text-emerald-600" : value > 15 ? "text-amber-600" : "text-red-600";
      case "debt":
        return value < 50 ? "text-emerald-600" : value < 100 ? "text-amber-600" : "text-red-600";
      case "margin":
        return value > 15 ? "text-emerald-600" : value > 10 ? "text-amber-600" : "text-red-600";
      case "growth":
        return value > 15 ? "text-emerald-600" : value > 0 ? "text-amber-600" : "text-red-600";
      default:
        return "text-slate-700";
    }
  };

  if (loading) {
    return (
      <Card className="bg-white/60 backdrop-blur-sm">
        <CardContent className="flex items-center justify-center py-12">
          <RefreshCw className="w-6 h-6 animate-spin text-blue-500 mr-2" />
          <span className="text-slate-500">Loading fundamentals...</span>
        </CardContent>
      </Card>
    );
  }

  if (error || !fundamentals) {
    return (
      <Card className="bg-white/60 backdrop-blur-sm">
        <CardContent className="flex items-center justify-center py-12">
          <AlertCircle className="w-6 h-6 text-red-500 mr-2" />
          <span className="text-slate-500">{error || "No data available"}</span>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <PieChart className="w-5 h-5 text-purple-600" />
            <span>Fundamentals</span>
          </div>
          <Badge className={getRatingColor(fundamentals.rating)}>
            {fundamentals.rating}
          </Badge>
        </CardTitle>

        {/* Fundamental Score */}
        <div className="mt-3">
          <div className="flex justify-between text-sm mb-1">
            <span className="text-slate-600">Fundamental Score</span>
            <span className="font-semibold">{fundamentals.fundamental_score}/100</span>
          </div>
          <Progress value={fundamentals.fundamental_score} className="h-2" />
        </div>

        {/* Score Factors */}
        {fundamentals.score_factors?.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-1">
            {fundamentals.score_factors.map((factor, idx) => (
              <Badge key={idx} variant="outline" className="text-xs bg-slate-50">
                <CheckCircle className="w-3 h-3 mr-1 text-emerald-500" />
                {factor}
              </Badge>
            ))}
          </div>
        )}
      </CardHeader>

      <CardContent className="pt-3">
        <div className="grid grid-cols-2 gap-4">
          {/* Valuation Metrics */}
          <div className="space-y-3">
            <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider flex items-center">
              <DollarSign className="w-3 h-3 mr-1" />
              Valuation
            </h4>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-slate-600">P/E Ratio</span>
                <span className={`text-sm font-medium ${getMetricColor(fundamentals.pe_ratio, "pe")}`}>
                  {formatValue(fundamentals.pe_ratio, "ratio")}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-slate-600">P/B Ratio</span>
                <span className="text-sm font-medium text-slate-700">
                  {formatValue(fundamentals.pb_ratio, "ratio")}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-slate-600">EPS</span>
                <span className="text-sm font-medium text-slate-700">
                  ₹{formatValue(fundamentals.eps)}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-slate-600">Book Value</span>
                <span className="text-sm font-medium text-slate-700">
                  ₹{formatValue(fundamentals.book_value)}
                </span>
              </div>
            </div>
          </div>

          {/* Profitability Metrics */}
          <div className="space-y-3">
            <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider flex items-center">
              <TrendingUp className="w-3 h-3 mr-1" />
              Profitability
            </h4>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-slate-600">ROE</span>
                <span className={`text-sm font-medium ${getMetricColor(fundamentals.roe, "roe")}`}>
                  {formatValue(fundamentals.roe, "percent")}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-slate-600">ROA</span>
                <span className="text-sm font-medium text-slate-700">
                  {formatValue(fundamentals.roa, "percent")}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-slate-600">Profit Margin</span>
                <span className={`text-sm font-medium ${getMetricColor(fundamentals.profit_margin, "margin")}`}>
                  {formatValue(fundamentals.profit_margin, "percent")}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-slate-600">Operating Margin</span>
                <span className="text-sm font-medium text-slate-700">
                  {formatValue(fundamentals.operating_margin, "percent")}
                </span>
              </div>
            </div>
          </div>

          {/* Debt Metrics */}
          <div className="space-y-3">
            <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider flex items-center">
              <BarChart3 className="w-3 h-3 mr-1" />
              Debt & Liquidity
            </h4>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-slate-600">Debt/Equity</span>
                <span className={`text-sm font-medium ${getMetricColor(fundamentals.debt_to_equity, "debt")}`}>
                  {formatValue(fundamentals.debt_to_equity, "ratio")}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-slate-600">Current Ratio</span>
                <span className="text-sm font-medium text-slate-700">
                  {formatValue(fundamentals.current_ratio, "ratio")}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-slate-600">Total Debt</span>
                <span className="text-sm font-medium text-slate-700">
                  {formatValue(fundamentals.total_debt, "currency")}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-slate-600">Total Cash</span>
                <span className="text-sm font-medium text-slate-700">
                  {formatValue(fundamentals.total_cash, "currency")}
                </span>
              </div>
            </div>
          </div>

          {/* Growth & Dividends */}
          <div className="space-y-3">
            <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider flex items-center">
              <TrendingUp className="w-3 h-3 mr-1" />
              Growth & Dividends
            </h4>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-slate-600">Revenue Growth</span>
                <span className={`text-sm font-medium ${getMetricColor(fundamentals.revenue_growth, "growth")}`}>
                  {formatValue(fundamentals.revenue_growth, "percent")}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-slate-600">Earnings Growth</span>
                <span className={`text-sm font-medium ${getMetricColor(fundamentals.earnings_growth, "growth")}`}>
                  {formatValue(fundamentals.earnings_growth, "percent")}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-slate-600">Dividend Yield</span>
                <span className="text-sm font-medium text-slate-700">
                  {formatValue(fundamentals.dividend_yield, "percent")}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-slate-600">Payout Ratio</span>
                <span className="text-sm font-medium text-slate-700">
                  {formatValue(fundamentals.payout_ratio, "percent")}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Market Info */}
        <div className="mt-4 pt-4 border-t border-slate-200">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-xs text-slate-500">Market Cap</p>
              <p className="text-sm font-semibold text-slate-700">
                {formatValue(fundamentals.market_cap, "currency")}
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-500">52W High</p>
              <p className="text-sm font-semibold text-emerald-600">
                ₹{formatValue(fundamentals.fifty_two_week_high)}
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-500">52W Low</p>
              <p className="text-sm font-semibold text-red-600">
                ₹{formatValue(fundamentals.fifty_two_week_low)}
              </p>
            </div>
          </div>
        </div>

        {/* Analyst Recommendation */}
        {fundamentals.analyst_recommendation && (
          <div className="mt-4 pt-4 border-t border-slate-200 flex items-center justify-between">
            <span className="text-sm text-slate-600">Analyst Recommendation</span>
            <Badge variant="outline" className="uppercase">
              {fundamentals.analyst_recommendation}
            </Badge>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default FundamentalsPanel;
