import React, { useState, useEffect, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import {
  Newspaper, TrendingUp, TrendingDown, Minus, RefreshCw,
  ExternalLink, Clock
} from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const NewsPanel = ({ symbol = null }) => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sentiment, setSentiment] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchNews = useCallback(async () => {
    setLoading(true);
    try {
      const endpoint = symbol
        ? `${API}/stocks/${symbol}/news`
        : `${API}/news/market`;

      const response = await fetch(endpoint);
      const data = await response.json();

      if (symbol) {
        setNews(data.news || []);
        setSentiment({
          overall: data.overall_sentiment,
          score: data.sentiment_score,
          breakdown: data.sentiment_breakdown
        });
      } else {
        setNews(data.headlines || []);
        setSentiment({
          overall: data.market_mood,
          score: data.sentiment_score
        });
      }
      setLastUpdated(data.last_updated);
    } catch (error) {
      console.error("Error fetching news:", error);
      setNews([]);
    } finally {
      setLoading(false);
    }
  }, [symbol]);

  useEffect(() => {
    fetchNews();
  }, [fetchNews]);

  const getSentimentIcon = (sentimentType) => {
    switch (sentimentType?.toLowerCase()) {
      case "positive":
      case "bullish":
        return <TrendingUp className="w-4 h-4 text-emerald-500" />;
      case "negative":
      case "bearish":
        return <TrendingDown className="w-4 h-4 text-red-500" />;
      default:
        return <Minus className="w-4 h-4 text-amber-500" />;
    }
  };

  const getSentimentColor = (sentimentType) => {
    switch (sentimentType?.toLowerCase()) {
      case "positive":
      case "bullish":
        return "bg-emerald-100 text-emerald-800";
      case "negative":
      case "bearish":
        return "bg-red-100 text-red-800";
      default:
        return "bg-amber-100 text-amber-800";
    }
  };

  const getSentimentBorderColor = (sentimentType) => {
    switch (sentimentType?.toLowerCase()) {
      case "positive":
        return "border-l-emerald-500";
      case "negative":
        return "border-l-red-500";
      default:
        return "border-l-amber-500";
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return "";
    try {
      const date = new Date(dateString);
      const now = new Date();
      const diff = now - date;

      if (diff < 3600000) {
        return `${Math.floor(diff / 60000)}m ago`;
      } else if (diff < 86400000) {
        return `${Math.floor(diff / 3600000)}h ago`;
      } else {
        return date.toLocaleDateString();
      }
    } catch {
      return dateString;
    }
  };

  return (
    <Card className="bg-white/60 backdrop-blur-sm border-slate-200">
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Newspaper className="w-5 h-5 text-blue-600" />
            <span>{symbol ? `${symbol} News` : "Market News"}</span>
          </div>
          <div className="flex items-center space-x-2">
            {sentiment && (
              <Badge className={getSentimentColor(sentiment.overall)}>
                {getSentimentIcon(sentiment.overall)}
                <span className="ml-1">{sentiment.overall}</span>
              </Badge>
            )}
            <Button
              size="sm"
              variant="ghost"
              onClick={fetchNews}
              disabled={loading}
            >
              <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            </Button>
          </div>
        </CardTitle>

        {/* Sentiment Breakdown */}
        {sentiment?.breakdown && (
          <div className="flex items-center space-x-4 mt-2 text-xs">
            <span className="text-emerald-600">
              ↑ {sentiment.breakdown.positive} positive
            </span>
            <span className="text-amber-600">
              → {sentiment.breakdown.neutral} neutral
            </span>
            <span className="text-red-600">
              ↓ {sentiment.breakdown.negative} negative
            </span>
          </div>
        )}
      </CardHeader>

      <CardContent className="pt-2">
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <RefreshCw className="w-5 h-5 animate-spin text-blue-500 mr-2" />
            <span className="text-slate-500">Loading news...</span>
          </div>
        ) : news.length === 0 ? (
          <div className="text-center py-8 text-slate-500">
            <Newspaper className="w-10 h-10 mx-auto mb-2 text-slate-400" />
            <p>No news available</p>
          </div>
        ) : (
          <div className="space-y-3 max-h-[400px] overflow-y-auto">
            {news.map((item, index) => (
              <a
                key={index}
                href={item.url}
                target="_blank"
                rel="noopener noreferrer"
                className={`block p-3 bg-white rounded-lg border-l-4 ${getSentimentBorderColor(
                  item.sentiment
                )} hover:bg-slate-50 transition-colors`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 pr-2">
                    <h4 className="text-sm font-medium text-slate-900 leading-tight">
                      {item.title}
                    </h4>
                    <div className="flex items-center mt-2 space-x-2 text-xs text-slate-500">
                      <span>{item.source}</span>
                      {item.published && (
                        <>
                          <span>•</span>
                          <span className="flex items-center">
                            <Clock className="w-3 h-3 mr-1" />
                            {formatDate(item.published)}
                          </span>
                        </>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Badge
                      variant="outline"
                      className={`text-xs ${getSentimentColor(item.sentiment)}`}
                    >
                      {item.sentiment}
                    </Badge>
                    <ExternalLink className="w-4 h-4 text-slate-400" />
                  </div>
                </div>
              </a>
            ))}
          </div>
        )}

        {lastUpdated && (
          <p className="text-xs text-slate-400 mt-3 text-center">
            Last updated: {formatDate(lastUpdated)}
          </p>
        )}
      </CardContent>
    </Card>
  );
};

export default NewsPanel;
