#!/bin/bash

# StockBreak Pro Production Startup Script

echo "🚀 Starting StockBreak Pro..."

# Set production environment
export ENVIRONMENT=production

# Create logs directory
mkdir -p logs

# Start the FastAPI backend server
echo "📊 Starting StockBreak Pro Backend..."
cd backend

# Install dependencies if needed
echo "📦 Installing backend dependencies..."
pip install -r requirements.txt

# Start the server
echo "🌟 StockBreak Pro is starting on port ${PORT:-8000}..."
python -m uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1