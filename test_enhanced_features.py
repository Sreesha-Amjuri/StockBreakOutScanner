#!/usr/bin/env python3
"""
Test StockBreak Pro Enhanced Features
Focus on the specific APIs requested in the review
"""

import requests
import sys
import json
from datetime import datetime

class EnhancedFeaturesTest:
    def __init__(self, base_url="https://stockport-3.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
        if details:
            print(f"    Details: {details}")
        print()

    def test_api_endpoint(self, name: str, method: str, endpoint: str, 
                         expected_status: int = 200, params: dict = None, 
                         data: dict = None, timeout: int = 30) -> tuple:
        """Generic API endpoint tester"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, params=params, timeout=timeout)
            else:
                raise ValueError(f"Unsupported method: {method}")

            success = response.status_code == expected_status
            
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text[:500]}
            
            details = f"Status: {response.status_code} (expected {expected_status})"
            if not success:
                details += f", Response: {response.text[:200]}"
            
            self.log_test(name, success, details)
            return success, response_data

        except requests.exceptions.Timeout:
            self.log_test(name, False, f"Request timeout after {timeout}s")
            return False, {}
        except Exception as e:
            self.log_test(name, False, f"Error: {str(e)}")
            return False, {}

    def test_enhanced_search_api(self):
        """Test Enhanced Search API with include_price parameter"""
        print("🔍 ENHANCED SEARCH API")
        print("-" * 25)
        
        # Test with include_price=true
        success, data = self.test_api_endpoint(
            "Enhanced Search - REL with price", 
            "GET", 
            "stocks/search", 
            params={"q": "REL", "include_price": "true"}
        )
        
        if success:
            results = data.get('results', [])
            if results:
                first_result = results[0]
                has_price = 'current_price' in first_result
                symbol = first_result.get('symbol', 'N/A')
                price = first_result.get('current_price', 'Missing')
                
                self.log_test(
                    "Search includes price data", 
                    has_price, 
                    f"Symbol: {symbol}, Price: ₹{price}" if has_price else f"Symbol: {symbol}, Price: Missing"
                )
        
        return success

    def test_fundamentals_api(self):
        """Test Fundamentals API"""
        print("📊 FUNDAMENTALS API")
        print("-" * 20)
        
        success, data = self.test_api_endpoint(
            "Fundamentals - RELIANCE", 
            "GET", 
            "stocks/RELIANCE/fundamentals"
        )
        
        if success:
            required_fields = ['pe_ratio', 'roe', 'debt_to_equity', 'fundamental_score', 'rating']
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                pe_ratio = data.get('pe_ratio')
                roe = data.get('roe')
                rating = data.get('rating')
                
                self.log_test(
                    "Fundamentals data complete", 
                    True, 
                    f"P/E: {pe_ratio}, ROE: {roe}%, Rating: {rating}"
                )
            else:
                self.log_test(
                    "Fundamentals data complete", 
                    False, 
                    f"Missing fields: {missing_fields}"
                )
        
        return success

    def test_news_api(self):
        """Test News API with sentiment"""
        print("📰 NEWS API")
        print("-" * 12)
        
        success, data = self.test_api_endpoint(
            "News - RELIANCE", 
            "GET", 
            "stocks/RELIANCE/news",
            timeout=30
        )
        
        if success:
            news_items = data.get('news', [])
            overall_sentiment = data.get('overall_sentiment')
            
            if news_items:
                first_news = news_items[0]
                has_sentiment = 'sentiment' in first_news
                sentiment = first_news.get('sentiment', 'Missing')
                
                self.log_test(
                    "News with sentiment", 
                    has_sentiment, 
                    f"Found {len(news_items)} news items, Overall: {overall_sentiment}, First sentiment: {sentiment}"
                )
            else:
                self.log_test(
                    "News with sentiment", 
                    True, 
                    "No news items found (acceptable)"
                )
        
        return success

    def test_market_news_api(self):
        """Test Market News API"""
        print("📈 MARKET NEWS API")
        print("-" * 18)
        
        success, data = self.test_api_endpoint(
            "Market News", 
            "GET", 
            "news/market",
            timeout=30
        )
        
        if success:
            headlines = data.get('headlines', [])
            market_mood = data.get('market_mood')
            
            self.log_test(
                "Market news data", 
                True, 
                f"Found {len(headlines)} headlines, Market mood: {market_mood}"
            )
        
        return success

    def test_quick_scan_api(self):
        """Test Quick Scan API"""
        print("⚡ QUICK SCAN API")
        print("-" * 17)
        
        success, data = self.test_api_endpoint(
            "Quick Scan", 
            "GET", 
            "stocks/breakouts/quick-scan",
            params={"min_confidence": "0.5"},
            timeout=30
        )
        
        if success:
            breakouts = data.get('breakouts', [])
            scan_info = data.get('scan_info', {})
            
            stocks_scanned = scan_info.get('stocks_scanned', 0)
            scan_time = scan_info.get('scan_time_seconds', 0)
            
            self.log_test(
                "Quick scan performance", 
                stocks_scanned > 0, 
                f"Scanned {stocks_scanned} stocks in {scan_time:.2f}s, Found {len(breakouts)} breakouts"
            )
        
        return success

    def test_watchlist_api(self):
        """Test Enhanced Watchlist API"""
        print("⭐ WATCHLIST API")
        print("-" * 16)
        
        # Add to watchlist
        success, data = self.test_api_endpoint(
            "Add to Watchlist - HDFCBANK", 
            "POST", 
            "watchlist",
            params={"symbol": "HDFCBANK"}
        )
        
        if success:
            has_price = 'current_price' in data or 'added_price' in data
            
            self.log_test(
                "Watchlist with price", 
                has_price, 
                f"Added HDFCBANK with price data: {has_price}"
            )
            
            # Clean up
            requests.delete(f"{self.api_url}/watchlist/HDFCBANK")
        
        return success

    def test_scan_progress_api(self):
        """Test Scan Progress API"""
        print("📊 SCAN PROGRESS API")
        print("-" * 20)
        
        success, data = self.test_api_endpoint(
            "Scan Progress", 
            "GET", 
            "stocks/scan/progress"
        )
        
        if success:
            status = data.get('status')
            progress = data.get('progress_percentage', 0)
            
            self.log_test(
                "Scan progress info", 
                True, 
                f"Status: {status}, Progress: {progress}%"
            )
        
        return success

    def run_all_tests(self):
        """Run all enhanced feature tests"""
        print("🚀 STOCKBREAK PRO ENHANCED FEATURES TEST")
        print("=" * 45)
        print(f"Testing API at: {self.api_url}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 45)
        print()
        
        # Test all enhanced features
        results = []
        results.append(self.test_enhanced_search_api())
        results.append(self.test_fundamentals_api())
        results.append(self.test_news_api())
        results.append(self.test_market_news_api())
        results.append(self.test_quick_scan_api())
        results.append(self.test_watchlist_api())
        results.append(self.test_scan_progress_api())
        
        # Summary
        print("=" * 45)
        print("📊 TEST SUMMARY")
        print("=" * 45)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        successful_features = sum(results)
        print(f"Enhanced Features Working: {successful_features}/7")
        
        if successful_features >= 5:
            print("✅ ENHANCED FEATURES TEST PASSED")
        else:
            print("❌ ENHANCED FEATURES TEST FAILED")
        
        return successful_features >= 5

if __name__ == "__main__":
    tester = EnhancedFeaturesTest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)