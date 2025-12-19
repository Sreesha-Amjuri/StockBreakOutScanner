import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_BASE_URL } from '@env';

const API_URL = API_BASE_URL || 'https://breakout-dash.preview.emergentagent.com/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  async (config) => {
    try {
      const token = await AsyncStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (error) {
      console.error('Error getting auth token:', error);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid, clear storage
      await AsyncStorage.removeItem('authToken');
      await AsyncStorage.removeItem('user');
    }
    return Promise.reject(error);
  }
);

// Authentication APIs
export const authAPI = {
  register: (email, password, name) =>
    api.post('/auth/register', { email, password, name }),
  
  login: (email, password) =>
    api.post('/auth/login', { email, password }),
  
  getProfile: () =>
    api.get('/auth/me'),
  
  logout: async () => {
    await AsyncStorage.removeItem('authToken');
    await AsyncStorage.removeItem('user');
  },
};

// Stock APIs
export const stockAPI = {
  getSymbols: () =>
    api.get('/stocks/symbols'),
  
  scanBreakouts: (params = {}) =>
    api.get('/stocks/breakouts/scan', { params }),
  
  getStockDetails: (symbol) =>
    api.get(`/stocks/${symbol}`),
  
  getChart: (symbol, timeframe = '6mo') =>
    api.get(`/stocks/${symbol}/chart`, { params: { timeframe } }),
  
  searchStocks: (query) =>
    api.get('/stocks/search', { params: { q: query } }),
  
  getMarketOverview: () =>
    api.get('/stocks/market-overview'),
  
  getLargeCap: () =>
    api.get('/stocks/large-cap'),
};

// Watchlist APIs
export const watchlistAPI = {
  getWatchlist: () =>
    api.get('/watchlist'),
  
  addToWatchlist: (symbol, name, price, notes = '') =>
    api.post('/watchlist', { symbol, name, added_price: price, notes }),
  
  removeFromWatchlist: (id) =>
    api.delete(`/watchlist/${id}`),
  
  updateWatchlist: (id, data) =>
    api.put(`/watchlist/${id}`, data),
};

// Market APIs
export const marketAPI = {
  getNews: () =>
    api.get('/market/news'),
  
  getPerformance: () =>
    api.get('/analytics/performance'),
  
  getSystemHealth: () =>
    api.get('/system/health'),
};

// Helper function to save auth data
export const saveAuthData = async (token, user) => {
  try {
    await AsyncStorage.setItem('authToken', token);
    await AsyncStorage.setItem('user', JSON.stringify(user));
  } catch (error) {
    console.error('Error saving auth data:', error);
    throw error;
  }
};

// Helper function to get auth data
export const getAuthData = async () => {
  try {
    const token = await AsyncStorage.getItem('authToken');
    const userString = await AsyncStorage.getItem('user');
    const user = userString ? JSON.parse(userString) : null;
    return { token, user };
  } catch (error) {
    console.error('Error getting auth data:', error);
    return { token: null, user: null };
  }
};

export default api;
