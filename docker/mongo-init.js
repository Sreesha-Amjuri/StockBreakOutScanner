// MongoDB initialization script for StockBreak Pro
db = db.getSiblingDB('stock-screener');

// Create collections
db.createCollection('watchlist');
db.createCollection('chat_messages');
db.createCollection('stock_cache');
db.createCollection('user_preferences');

// Create indexes for better performance
db.watchlist.createIndex({ "symbol": 1 }, { "unique": true });
db.chat_messages.createIndex({ "session_id": 1 });
db.chat_messages.createIndex({ "timestamp": 1 });
db.stock_cache.createIndex({ "symbol": 1 });
db.stock_cache.createIndex({ "timestamp": 1 });

// Insert default data
db.user_preferences.insertOne({
  "preference_id": "default",
  "theme": "light",
  "default_confidence": 0.5,
  "default_limit": 50,
  "created_at": new Date()
});

print('StockBreak Pro database initialized successfully!');