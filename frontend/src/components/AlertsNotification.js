import React, { useState, useEffect, useCallback } from "react";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import {
  Bell, X, Check, CheckCheck, TrendingUp, AlertTriangle,
  Target, Clock, ChevronRight
} from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AlertsNotification = ({ onStockClick }) => {
  const [alerts, setAlerts] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const fetchAlerts = useCallback(async () => {
    try {
      const response = await fetch(`${API}/alerts?limit=20`);
      const data = await response.json();
      
      if (data.alerts) {
        setAlerts(data.alerts);
        setUnreadCount(data.unread_count || 0);
      }
    } catch (error) {
      console.error("Error fetching alerts:", error);
    }
  }, []);

  useEffect(() => {
    fetchAlerts();
    // Poll for new alerts every minute
    const interval = setInterval(fetchAlerts, 60 * 1000);
    return () => clearInterval(interval);
  }, [fetchAlerts]);

  // Request browser notification permission
  useEffect(() => {
    if ("Notification" in window && Notification.permission === "default") {
      Notification.requestPermission();
    }
  }, []);

  // Show browser notification for new alerts
  useEffect(() => {
    if (unreadCount > 0 && "Notification" in window && Notification.permission === "granted") {
      const latestAlert = alerts.find(a => !a.is_read);
      if (latestAlert) {
        new Notification("StockBreak Pro Alert", {
          body: latestAlert.message,
          icon: "/favicon.ico",
          tag: latestAlert.id,
        });
      }
    }
  }, [unreadCount, alerts]);

  const markAsRead = async (alertId) => {
    try {
      await fetch(`${API}/alerts/${alertId}/read`, { method: 'POST' });
      setAlerts(prev => prev.map(a => 
        a.id === alertId ? { ...a, is_read: true } : a
      ));
      setUnreadCount(prev => Math.max(0, prev - 1));
    } catch (error) {
      console.error("Error marking alert as read:", error);
    }
  };

  const markAllAsRead = async () => {
    try {
      setLoading(true);
      await fetch(`${API}/alerts/read-all`, { method: 'POST' });
      setAlerts(prev => prev.map(a => ({ ...a, is_read: true })));
      setUnreadCount(0);
    } catch (error) {
      console.error("Error marking all alerts as read:", error);
    } finally {
      setLoading(false);
    }
  };

  const getAlertIcon = (type) => {
    switch (type) {
      case 'BREAKOUT_IMMINENT':
        return <AlertTriangle className="w-5 h-5 text-amber-500" />;
      case 'BREAKOUT_CONFIRMED':
        return <TrendingUp className="w-5 h-5 text-emerald-500" />;
      case 'STOP_LOSS_HIT':
        return <AlertTriangle className="w-5 h-5 text-red-500" />;
      case 'TARGET_HIT':
        return <Target className="w-5 h-5 text-emerald-500" />;
      default:
        return <Bell className="w-5 h-5 text-blue-500" />;
    }
  };

  const getAlertBgColor = (type, isRead) => {
    if (isRead) return 'bg-slate-50';
    switch (type) {
      case 'BREAKOUT_IMMINENT':
        return 'bg-amber-50';
      case 'BREAKOUT_CONFIRMED':
        return 'bg-emerald-50';
      case 'STOP_LOSS_HIT':
        return 'bg-red-50';
      case 'TARGET_HIT':
        return 'bg-emerald-50';
      default:
        return 'bg-blue-50';
    }
  };

  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
    return date.toLocaleDateString();
  };

  const formatPrice = (price) => {
    if (!price) return '';
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 2
    }).format(price);
  };

  return (
    <div className="relative">
      {/* Bell Button */}
      <Button
        variant="outline"
        size="icon"
        className="relative"
        onClick={() => setIsOpen(!isOpen)}
      >
        <Bell className="w-5 h-5" />
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center animate-pulse">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </Button>

      {/* Dropdown Panel */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          />
          
          {/* Panel */}
          <div className="absolute right-0 mt-2 w-96 bg-white rounded-lg shadow-xl border border-slate-200 z-50 overflow-hidden">
            {/* Header */}
            <div className="bg-slate-50 px-4 py-3 border-b flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Bell className="w-5 h-5 text-slate-600" />
                <span className="font-semibold text-slate-800">Alerts</span>
                {unreadCount > 0 && (
                  <Badge variant="destructive" className="text-xs">
                    {unreadCount} new
                  </Badge>
                )}
              </div>
              <div className="flex items-center space-x-2">
                {unreadCount > 0 && (
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={markAllAsRead}
                    disabled={loading}
                    className="text-xs h-7"
                  >
                    <CheckCheck className="w-4 h-4 mr-1" />
                    Mark all read
                  </Button>
                )}
                <Button
                  size="icon"
                  variant="ghost"
                  className="h-7 w-7"
                  onClick={() => setIsOpen(false)}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
            </div>

            {/* Alerts List */}
            <div className="max-h-[400px] overflow-y-auto">
              {alerts.length === 0 ? (
                <div className="text-center py-8 text-slate-500">
                  <Bell className="w-10 h-10 mx-auto mb-2 text-slate-400" />
                  <p>No alerts yet</p>
                  <p className="text-sm mt-1">
                    We'll notify you when stocks in your watchlist are about to breakout
                  </p>
                </div>
              ) : (
                alerts.map((alert, index) => (
                  <div
                    key={alert.id || index}
                    className={`px-4 py-3 border-b cursor-pointer transition-colors hover:bg-slate-100 ${getAlertBgColor(alert.alert_type, alert.is_read)}`}
                    onClick={() => {
                      if (!alert.is_read) markAsRead(alert.id);
                      if (onStockClick) onStockClick(alert.symbol);
                      setIsOpen(false);
                    }}
                  >
                    <div className="flex items-start space-x-3">
                      <div className="mt-0.5">
                        {getAlertIcon(alert.alert_type)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between">
                          <span className="font-semibold text-slate-800">
                            {alert.symbol}
                          </span>
                          <span className="text-xs text-slate-400 flex items-center">
                            <Clock className="w-3 h-3 mr-1" />
                            {formatTime(alert.created_at)}
                          </span>
                        </div>
                        <p className="text-sm text-slate-600 mt-1">
                          {alert.message}
                        </p>
                        {alert.current_price && (
                          <div className="flex items-center mt-2 text-xs text-slate-500 space-x-3">
                            <span>Price: {formatPrice(alert.current_price)}</span>
                            {alert.breakout_level && (
                              <span>Level: {formatPrice(alert.breakout_level)}</span>
                            )}
                            <span>
                              Confidence: {(alert.confidence * 100).toFixed(0)}%
                            </span>
                          </div>
                        )}
                      </div>
                      {!alert.is_read && (
                        <div className="w-2 h-2 bg-blue-500 rounded-full mt-2" />
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>

            {/* Footer */}
            {alerts.length > 0 && (
              <div className="bg-slate-50 px-4 py-2 border-t">
                <Button
                  variant="ghost"
                  className="w-full text-sm text-slate-600 hover:text-slate-800"
                  onClick={() => setIsOpen(false)}
                >
                  View All Alerts
                  <ChevronRight className="w-4 h-4 ml-1" />
                </Button>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default AlertsNotification;
