import React, { useState, useRef, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Badge } from "./ui/badge";
import { MessageCircle, Send, Loader2, Bot, User, TrendingUp, AlertCircle } from "lucide-react";
import { useTheme } from '../contexts/ThemeContext';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AIChat = ({ selectedStock = null, isOpen = false, onToggle }) => {
  const { isDarkMode } = useTheme();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Generate session ID on component mount
  useEffect(() => {
    if (!sessionId) {
      setSessionId(`session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
    }
  }, [sessionId]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setIsLoading(true);

    // Add user message to chat
    const newUserMessage = {
      id: Date.now(),
      role: 'user',
      message: userMessage,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, newUserMessage]);

    try {
      // Prepare stock context if available
      let stockContext = null;
      if (selectedStock) {
        stockContext = {
          symbol: selectedStock.symbol,
          current_price: selectedStock.current_price,
          change_percent: selectedStock.change_percent,
          rsi: selectedStock.technical_data?.rsi,
          sector: selectedStock.sector,
          technical_indicators: selectedStock.technical_data
        };
      }

      // Send message to AI
      const response = await axios.post(`${API}/chat`, {
        message: userMessage,
        session_id: sessionId,
        stock_context: stockContext
      });

      // Add AI response to chat
      const aiMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        message: response.data.response,
        timestamp: new Date(response.data.timestamp)
      };
      setMessages(prev => [...prev, aiMessage]);

    } catch (error) {
      console.error('Chat error:', error);
      toast.error('Failed to get AI response. Please try again.');
      
      // Add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        message: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatMessage = (text) => {
    // Simple formatting for better readability
    return text.split('\n').map((line, index) => (
      <p key={index} className="mb-1 last:mb-0">
        {line}
      </p>
    ));
  };

  const getQuickActions = () => {
    const actions = [
      "Analyze current market trends",
      "Explain technical indicators",
      "Risk assessment guidance",
      "Portfolio diversification tips"
    ];

    if (selectedStock) {
      actions.unshift(
        `Analyze ${selectedStock.symbol}`,
        `Entry/exit strategy for ${selectedStock.symbol}`,
        `Risk level of ${selectedStock.symbol}`
      );
    }

    return actions;
  };

  if (!isOpen) {
    return (
      <Button
        onClick={onToggle}
        className="fixed bottom-6 right-6 h-14 w-14 rounded-full shadow-lg bg-indigo-600 hover:bg-indigo-700 text-white z-50"
        size="icon"
      >
        <MessageCircle className="h-6 w-6" />
      </Button>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 w-96 h-[500px] z-50">
      <Card className={`h-full flex flex-col shadow-xl border-2 ${
        isDarkMode 
          ? 'bg-slate-800 border-slate-600' 
          : 'bg-white border-slate-200'
      }`}>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full flex items-center justify-center">
                <Bot className="w-4 h-4 text-white" />
              </div>
              <div>
                <CardTitle className="text-sm font-semibold">
                  StockBreak Pro AI
                </CardTitle>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Your Investment Assistant
                </p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={onToggle}
              className="h-8 w-8 p-0"
            >
              ×
            </Button>
          </div>
          
          {selectedStock && (
            <div className="mt-2 p-2 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 border border-indigo-200 dark:border-indigo-700">
              <div className="flex items-center space-x-2">
                <TrendingUp className="w-4 h-4 text-indigo-600" />
                <span className="text-sm font-medium text-indigo-700 dark:text-indigo-300">
                  {selectedStock.symbol}
                </span>
                <Badge variant={selectedStock.change_percent >= 0 ? "default" : "destructive"} className="text-xs">
                  {selectedStock.change_percent >= 0 ? '+' : ''}{selectedStock.change_percent?.toFixed(2)}%
                </Badge>
              </div>
              <p className="text-xs text-indigo-600 dark:text-indigo-400 mt-1">
                Current: ₹{selectedStock.current_price?.toFixed(2)} | Sector: {selectedStock.sector}
              </p>
            </div>
          )}
        </CardHeader>

        <CardContent className="flex-1 flex flex-col overflow-hidden">
          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto space-y-3 mb-4 pr-2">
            {messages.length === 0 && (
              <div className="text-center py-8">
                <Bot className="w-12 h-12 text-slate-400 mx-auto mb-3" />
                <p className="text-sm text-slate-500 dark:text-slate-400 mb-4">
                  Hi! I'm your AI stock market analyst. Ask me anything about Indian equity markets, technical analysis, or investment strategies.
                </p>
                
                {/* Quick Actions */}
                <div className="space-y-2">
                  <p className="text-xs text-slate-400 dark:text-slate-500 mb-2">Quick actions:</p>
                  {getQuickActions().slice(0, 3).map((action, index) => (
                    <Button
                      key={index}
                      variant="outline"
                      size="sm"
                      className="w-full text-xs h-8"
                      onClick={() => setInputMessage(action)}
                    >
                      {action}
                    </Button>
                  ))}
                </div>
              </div>
            )}

            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-[80%] p-3 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-indigo-600 text-white'
                    : message.isError
                    ? 'bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-700'
                    : 'bg-slate-100 dark:bg-slate-700 text-slate-900 dark:text-slate-100'
                }`}>
                  <div className="flex items-start space-x-2">
                    {message.role === 'assistant' && (
                      <div className="flex-shrink-0 mt-1">
                        {message.isError ? (
                          <AlertCircle className="w-4 h-4 text-red-500" />
                        ) : (
                          <Bot className="w-4 h-4 text-indigo-600" />
                        )}
                      </div>
                    )}
                    <div className="flex-1">
                      <div className="text-sm">
                        {formatMessage(message.message)}
                      </div>
                      <p className="text-xs opacity-70 mt-1">
                        {message.timestamp.toLocaleTimeString()}
                      </p>
                    </div>
                    {message.role === 'user' && (
                      <User className="w-4 h-4 flex-shrink-0 mt-1" />
                    )}
                  </div>
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-slate-100 dark:bg-slate-700 p-3 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <Loader2 className="w-4 h-4 animate-spin text-indigo-600" />
                    <span className="text-sm text-slate-600 dark:text-slate-300">
                      Analyzing...
                    </span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="flex space-x-2">
            <Input
              ref={inputRef}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about stocks, markets, or strategies..."
              className="flex-1"
              disabled={isLoading}
            />
            <Button
              onClick={sendMessage}
              disabled={!inputMessage.trim() || isLoading}
              size="icon"
              className="bg-indigo-600 hover:bg-indigo-700"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AIChat;