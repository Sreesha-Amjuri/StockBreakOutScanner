"""
News and Sentiment Service for Indian Stocks
Uses Google News RSS and Yahoo Finance - No API key required
"""

import asyncio
import aiohttp
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
from datetime import datetime, timezone
import re
import logging

logger = logging.getLogger(__name__)

# Sentiment keywords for analysis
POSITIVE_KEYWORDS = [
    'surge', 'rally', 'gain', 'jump', 'soar', 'rise', 'boost', 'profit', 'growth',
    'bullish', 'outperform', 'beat', 'upgrade', 'buy', 'strong', 'positive', 'record',
    'breakthrough', 'expand', 'success', 'win', 'deal', 'partnership', 'dividend',
    'acquisition', 'launch', 'innovation', 'highest', 'best', 'exceed', 'optimistic'
]

NEGATIVE_KEYWORDS = [
    'fall', 'drop', 'decline', 'crash', 'plunge', 'loss', 'bearish', 'sell', 'weak',
    'downgrade', 'miss', 'cut', 'negative', 'concern', 'risk', 'warning', 'fear',
    'lawsuit', 'investigation', 'fraud', 'scandal', 'bankruptcy', 'debt', 'layoff',
    'closure', 'fine', 'penalty', 'worst', 'low', 'underperform', 'recession'
]


def analyze_sentiment(text: str) -> Dict:
    """Analyze sentiment of text using keyword matching"""
    text_lower = text.lower()
    
    positive_count = sum(1 for word in POSITIVE_KEYWORDS if word in text_lower)
    negative_count = sum(1 for word in NEGATIVE_KEYWORDS if word in text_lower)
    
    total = positive_count + negative_count
    if total == 0:
        return {"sentiment": "Neutral", "score": 0, "confidence": 0.5}
    
    score = (positive_count - negative_count) / total
    
    if score > 0.2:
        sentiment = "Positive"
    elif score < -0.2:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    confidence = min(abs(score) + 0.5, 1.0)
    
    return {
        "sentiment": sentiment,
        "score": round(score, 2),
        "confidence": round(confidence, 2),
        "positive_signals": positive_count,
        "negative_signals": negative_count
    }


async def fetch_google_news_rss(query: str, max_results: int = 10) -> List[Dict]:
    """Fetch news from Google News RSS feed for Indian stocks"""
    news_items = []
    
    # Format query for Indian stock news
    search_query = f"{query} stock NSE India"
    encoded_query = search_query.replace(' ', '+')
    
    # Google News RSS URL
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(rss_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Parse XML
                    root = ET.fromstring(content)
                    
                    # Find all items in the RSS feed
                    for item in root.findall('.//item')[:max_results]:
                        title = item.find('title')
                        link = item.find('link')
                        pub_date = item.find('pubDate')
                        source = item.find('source')
                        
                        if title is not None:
                            title_text = title.text or ""
                            # Clean up title (remove source name at end)
                            clean_title = re.sub(r' - [^-]+$', '', title_text)
                            
                            sentiment_analysis = analyze_sentiment(clean_title)
                            
                            news_items.append({
                                "title": clean_title,
                                "url": link.text if link is not None else "",
                                "published": pub_date.text if pub_date is not None else "",
                                "source": source.text if source is not None else "Google News",
                                "sentiment": sentiment_analysis["sentiment"],
                                "sentiment_score": sentiment_analysis["score"]
                            })
    except asyncio.TimeoutError:
        logger.warning(f"Timeout fetching Google News for {query}")
    except Exception as e:
        logger.error(f"Error fetching Google News RSS for {query}: {str(e)}")
    
    return news_items


async def fetch_yahoo_finance_news(symbol: str) -> List[Dict]:
    """Fetch news from Yahoo Finance for a stock"""
    import yfinance as yf
    
    news_items = []
    
    try:
        # Get ticker with .NS suffix for NSE stocks
        ticker = yf.Ticker(f"{symbol}.NS")
        
        # Get news
        news = ticker.news
        
        if news:
            for item in news[:5]:  # Limit to 5 items
                title = item.get('title', '')
                sentiment_analysis = analyze_sentiment(title)
                
                # Convert timestamp to readable format
                timestamp = item.get('providerPublishTime', 0)
                if timestamp:
                    pub_date = datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()
                else:
                    pub_date = datetime.now(timezone.utc).isoformat()
                
                news_items.append({
                    "title": title,
                    "url": item.get('link', ''),
                    "published": pub_date,
                    "source": item.get('publisher', 'Yahoo Finance'),
                    "sentiment": sentiment_analysis["sentiment"],
                    "sentiment_score": sentiment_analysis["score"],
                    "thumbnail": item.get('thumbnail', {}).get('resolutions', [{}])[0].get('url', '') if item.get('thumbnail') else ''
                })
    except Exception as e:
        logger.error(f"Error fetching Yahoo Finance news for {symbol}: {str(e)}")
    
    return news_items


async def get_stock_news(symbol: str, company_name: str = None) -> Dict:
    """Get comprehensive news for a stock from multiple sources"""
    
    # Fetch from both sources concurrently
    search_term = company_name if company_name else symbol
    
    google_news_task = fetch_google_news_rss(search_term, max_results=5)
    yahoo_news_task = fetch_yahoo_finance_news(symbol)
    
    google_news, yahoo_news = await asyncio.gather(
        google_news_task,
        yahoo_news_task,
        return_exceptions=True
    )
    
    # Handle exceptions
    if isinstance(google_news, Exception):
        logger.error(f"Google News error: {google_news}")
        google_news = []
    
    if isinstance(yahoo_news, Exception):
        logger.error(f"Yahoo News error: {yahoo_news}")
        yahoo_news = []
    
    # Combine and deduplicate news
    all_news = []
    seen_titles = set()
    
    for item in yahoo_news + google_news:
        title_key = item['title'].lower()[:50]
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            all_news.append(item)
    
    # Calculate overall sentiment
    if all_news:
        total_score = sum(item.get('sentiment_score', 0) for item in all_news)
        avg_score = total_score / len(all_news)
        
        positive_count = sum(1 for item in all_news if item.get('sentiment') == 'Positive')
        negative_count = sum(1 for item in all_news if item.get('sentiment') == 'Negative')
        neutral_count = len(all_news) - positive_count - negative_count
        
        if avg_score > 0.1:
            overall_sentiment = "Bullish"
        elif avg_score < -0.1:
            overall_sentiment = "Bearish"
        else:
            overall_sentiment = "Neutral"
    else:
        overall_sentiment = "No News"
        avg_score = 0
        positive_count = negative_count = neutral_count = 0
    
    return {
        "symbol": symbol,
        "news": all_news[:10],  # Limit to 10 items
        "news_count": len(all_news),
        "overall_sentiment": overall_sentiment,
        "sentiment_score": round(avg_score, 2),
        "sentiment_breakdown": {
            "positive": positive_count,
            "negative": negative_count,
            "neutral": neutral_count
        },
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


async def get_market_news() -> Dict:
    """Get general Indian stock market news"""
    
    queries = [
        "Nifty 50 stock market",
        "Sensex BSE India",
        "Indian stock market"
    ]
    
    all_news = []
    
    for query in queries:
        news = await fetch_google_news_rss(query, max_results=3)
        all_news.extend(news)
    
    # Deduplicate
    seen_titles = set()
    unique_news = []
    for item in all_news:
        title_key = item['title'].lower()[:50]
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            unique_news.append(item)
    
    # Calculate market sentiment
    if unique_news:
        total_score = sum(item.get('sentiment_score', 0) for item in unique_news)
        avg_score = total_score / len(unique_news)
        
        if avg_score > 0.15:
            market_mood = "Bullish"
        elif avg_score < -0.15:
            market_mood = "Bearish"
        else:
            market_mood = "Mixed"
    else:
        market_mood = "Unknown"
        avg_score = 0
    
    return {
        "headlines": unique_news[:10],
        "market_mood": market_mood,
        "sentiment_score": round(avg_score, 2),
        "last_updated": datetime.now(timezone.utc).isoformat()
    }
