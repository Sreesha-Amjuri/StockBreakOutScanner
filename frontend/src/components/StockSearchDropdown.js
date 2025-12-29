import React, { useState, useEffect, useRef, useCallback } from "react";
import { Input } from "./ui/input";
import { Badge } from "./ui/badge";
import { Search, TrendingUp, TrendingDown, Loader2, X } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const StockSearchDropdown = ({ onSelectStock, onAddToWatchlist }) => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);
  const inputRef = useRef(null);

  // Debounced search
  const searchStocks = useCallback(async (searchQuery) => {
    if (searchQuery.length < 1) {
      setResults([]);
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API}/stocks/search?q=${searchQuery}&include_price=true`);
      const data = await response.json();
      setResults(data.results || []);
    } catch (error) {
      console.error("Search error:", error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      searchStocks(query);
    }, 300); // 300ms debounce

    return () => clearTimeout(timer);
  }, [query, searchStocks]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSelect = (stock) => {
    setIsOpen(false);
    setQuery("");
    if (onSelectStock) {
      onSelectStock(stock.symbol);
    }
  };

  const handleAddToWatchlist = (e, stock) => {
    e.stopPropagation();
    if (onAddToWatchlist) {
      onAddToWatchlist(stock.symbol);
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

  return (
    <div ref={dropdownRef} className="relative w-full max-w-md">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-4 h-4" />
        <Input
          ref={inputRef}
          placeholder="Search stocks (e.g., RELIANCE, TCS)..."
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          className="pl-10 pr-10 bg-white/80 border-slate-200 focus:border-blue-500"
        />
        {query && (
          <button
            onClick={() => {
              setQuery("");
              setResults([]);
              inputRef.current?.focus();
            }}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-slate-600"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Dropdown Results */}
      {isOpen && (query.length >= 1 || results.length > 0) && (
        <div className="absolute z-50 w-full mt-1 bg-white rounded-lg shadow-lg border border-slate-200 max-h-80 overflow-y-auto">
          {loading ? (
            <div className="flex items-center justify-center py-4">
              <Loader2 className="w-5 h-5 animate-spin text-blue-500 mr-2" />
              <span className="text-slate-500">Searching...</span>
            </div>
          ) : results.length === 0 ? (
            <div className="py-4 px-4 text-center text-slate-500">
              {query.length >= 1 ? "No stocks found" : "Start typing to search"}
            </div>
          ) : (
            <ul className="py-1">
              {results.map((stock, index) => (
                <li
                  key={stock.symbol}
                  onClick={() => handleSelect(stock)}
                  className={`px-4 py-3 cursor-pointer hover:bg-blue-50 transition-colors ${
                    index !== results.length - 1 ? "border-b border-slate-100" : ""
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="font-semibold text-slate-900">{stock.symbol}</span>
                        <Badge variant="outline" className="text-xs">
                          {stock.sector}
                        </Badge>
                      </div>
                    </div>
                    <div className="flex items-center space-x-3">
                      {stock.current_price && (
                        <div className="text-right">
                          <p className="font-medium text-slate-900">
                            {formatPrice(stock.current_price)}
                          </p>
                          {stock.change_percent !== null && (
                            <p
                              className={`text-xs flex items-center justify-end ${
                                stock.change_percent >= 0 ? "text-emerald-600" : "text-red-600"
                              }`}
                            >
                              {stock.change_percent >= 0 ? (
                                <TrendingUp className="w-3 h-3 mr-1" />
                              ) : (
                                <TrendingDown className="w-3 h-3 mr-1" />
                              )}
                              {stock.change_percent >= 0 ? "+" : ""}
                              {stock.change_percent?.toFixed(2)}%
                            </p>
                          )}
                        </div>
                      )}
                      <button
                        onClick={(e) => handleAddToWatchlist(e, stock)}
                        className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200 transition-colors"
                      >
                        + Watchlist
                      </button>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

export default StockSearchDropdown;
