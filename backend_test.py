#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Indian Stock Breakout Screener
Tests all endpoints with various scenarios and edge cases
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, List, Optional

class StockBreakoutAPITester:
    def __init__(self, base_url="https://breakout-screener.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name: str, success: bool, details: str = "", response_data: Dict = None):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            
        result = {
            "test_name": name,
            "success": success,
            "details": details,
            "response_data": response_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
        if details:
            print(f"    Details: {details}")
        if not success and response_data:
            print(f"    Response: {response_data}")
        print()

    def test_api_endpoint(self, name: str, method: str, endpoint: str, 
                         expected_status: int = 200, params: Dict = None, 
                         data: Dict = None, timeout: int = 30) -> tuple:
        """Generic API endpoint tester"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, params=params, timeout=timeout)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=timeout)
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
            
            self.log_test(name, success, details, response_data if success else None)
            return success, response_data

        except requests.exceptions.Timeout:
            self.log_test(name, False, f"Request timeout after {timeout}s")
            return False, {}
        except Exception as e:
            self.log_test(name, False, f"Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test API root endpoint"""
        return self.test_api_endpoint("API Root", "GET", "")

    def test_nse_symbols(self):
        """Test NSE symbols endpoint"""
        success, data = self.test_api_endpoint("NSE Symbols", "GET", "stocks/symbols")
        
        if success:
            # Validate response structure
            required_keys = ['symbols', 'symbols_with_sectors', 'count', 'sectors']
            missing_keys = [key for key in required_keys if key not in data]
            
            if missing_keys:
                self.log_test("NSE Symbols Structure", False, f"Missing keys: {missing_keys}")
            else:
                self.log_test("NSE Symbols Structure", True, f"Found {data['count']} symbols, {len(data['sectors'])} sectors")
                
                # Test if we have expected symbols
                expected_symbols = ['RELIANCE', 'TCS', 'HDFCBANK', 'INFOSYS']
                found_symbols = [s for s in expected_symbols if s in data['symbols']]
                self.log_test("Expected Symbols Present", len(found_symbols) > 0, 
                            f"Found {len(found_symbols)}/{len(expected_symbols)} expected symbols")
        
        return success, data

    def test_stock_search(self):
        """Test stock search functionality"""
        # Test valid search
        success1, data1 = self.test_api_endpoint("Stock Search - Valid", "GET", "stocks/search", 
                                                params={"q": "REL"})
        
        if success1 and 'results' in data1:
            self.log_test("Search Results Structure", True, f"Found {len(data1['results'])} results")
        
        # Test empty search
        success2, data2 = self.test_api_endpoint("Stock Search - Empty", "GET", "stocks/search", 
                                                params={"q": ""})
        
        return success1 and success2

    def test_individual_stock_data(self):
        """Test individual stock data endpoints"""
        test_symbols = ['RELIANCE', 'TCS', 'HDFCBANK']
        successful_tests = 0
        
        for symbol in test_symbols:
            success, data = self.test_api_endpoint(f"Stock Data - {symbol}", "GET", f"stocks/{symbol}")
            
            if success:
                successful_tests += 1
                # Validate response structure
                required_keys = ['symbol', 'name', 'current_price', 'technical_indicators', 'fundamental_data', 'risk_assessment']
                missing_keys = [key for key in required_keys if key not in data]
                
                if missing_keys:
                    self.log_test(f"{symbol} Data Structure", False, f"Missing keys: {missing_keys}")
                else:
                    self.log_test(f"{symbol} Data Structure", True, 
                                f"Price: ₹{data['current_price']:.2f}, Sector: {data.get('sector', 'N/A')}")
        
        return successful_tests > 0

    def test_stock_chart_data(self):
        """Test stock chart data endpoints"""
        test_symbol = 'RELIANCE'
        timeframes = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y']
        successful_tests = 0
        
        for timeframe in timeframes:
            success, data = self.test_api_endpoint(f"Chart Data - {test_symbol} {timeframe}", "GET", 
                                                 f"stocks/{test_symbol}/chart", 
                                                 params={"timeframe": timeframe})
            
            if success:
                successful_tests += 1
                if 'data' in data and len(data['data']) > 0:
                    self.log_test(f"Chart Data Points - {timeframe}", True, 
                                f"Found {len(data['data'])} data points")
                else:
                    self.log_test(f"Chart Data Points - {timeframe}", False, "No chart data found")
        
        return successful_tests > len(timeframes) // 2

    def test_breakout_scanning(self):
        """Test breakout scanning with enhanced trading features"""
        # Test basic breakout scan
        success1, data1 = self.test_api_endpoint("Breakout Scan - Basic", "GET", "stocks/breakouts/scan", 
                                                timeout=60)  # Longer timeout for scanning
        
        if success1:
            breakouts_found = data1.get('breakouts_found', 0)
            total_scanned = data1.get('total_scanned', 0)
            self.log_test("Breakout Scan Results", True, 
                        f"Found {breakouts_found} breakouts from {total_scanned} stocks scanned")
            
            # Test trading recommendations in breakout results
            breakout_stocks = data1.get('breakout_stocks', [])
            if breakout_stocks:
                self.test_trading_recommendations_in_breakouts(breakout_stocks)
        
        # Test with sector filter
        success2, data2 = self.test_api_endpoint("Breakout Scan - IT Sector", "GET", "stocks/breakouts/scan", 
                                                params={"sector": "IT", "min_confidence": "0.6"}, timeout=60)
        
        # Test with risk filter
        success3, data3 = self.test_api_endpoint("Breakout Scan - Low Risk", "GET", "stocks/breakouts/scan", 
                                                params={"risk_level": "Low", "min_confidence": "0.7"}, timeout=60)
        
        return success1 and success2 and success3

    def test_trading_recommendations_in_breakouts(self, breakout_stocks):
        """Test trading recommendations structure in breakout results"""
        stocks_with_recommendations = 0
        valid_recommendations = 0
        
        for stock in breakout_stocks:
            trading_rec = stock.get('trading_recommendation')
            if trading_rec:
                stocks_with_recommendations += 1
                
                # Validate trading recommendation structure
                required_fields = ['entry_price', 'stop_loss', 'target_price', 'risk_reward_ratio', 
                                 'position_size_percent', 'action', 'entry_rationale', 'stop_loss_rationale']
                
                missing_fields = [field for field in required_fields if field not in trading_rec]
                
                if not missing_fields:
                    valid_recommendations += 1
                    
                    # Validate trading logic
                    entry_price = trading_rec['entry_price']
                    stop_loss = trading_rec['stop_loss']
                    target_price = trading_rec['target_price']
                    action = trading_rec['action']
                    risk_reward = trading_rec['risk_reward_ratio']
                    position_size = trading_rec['position_size_percent']
                    
                    # Test logical constraints
                    logic_valid = True
                    logic_issues = []
                    
                    if stop_loss >= entry_price:
                        logic_valid = False
                        logic_issues.append("Stop loss should be below entry price")
                    
                    if target_price <= entry_price:
                        logic_valid = False
                        logic_issues.append("Target price should be above entry price")
                    
                    if action not in ['BUY', 'WAIT', 'AVOID']:
                        logic_valid = False
                        logic_issues.append(f"Invalid action: {action}")
                    
                    if not (1.5 <= risk_reward <= 4.0):
                        logic_valid = False
                        logic_issues.append(f"Risk:reward ratio {risk_reward} outside expected range (1.5-4.0)")
                    
                    if not (1.0 <= position_size <= 20.0):
                        logic_valid = False
                        logic_issues.append(f"Position size {position_size}% outside expected range (1-20%)")
                    
                    if logic_valid:
                        self.log_test(f"Trading Logic - {stock['symbol']}", True, 
                                    f"Entry: ₹{entry_price}, Stop: ₹{stop_loss}, Target: ₹{target_price}, Action: {action}")
                    else:
                        self.log_test(f"Trading Logic - {stock['symbol']}", False, 
                                    f"Logic issues: {', '.join(logic_issues)}")
                else:
                    self.log_test(f"Trading Recommendation Structure - {stock['symbol']}", False, 
                                f"Missing fields: {missing_fields}")
        
        self.log_test("Trading Recommendations Coverage", stocks_with_recommendations > 0, 
                    f"{stocks_with_recommendations}/{len(breakout_stocks)} stocks have trading recommendations")
        
        self.log_test("Trading Recommendations Validity", valid_recommendations > 0, 
                    f"{valid_recommendations}/{stocks_with_recommendations} recommendations are structurally valid")

    def test_market_overview(self):
        """Test market overview endpoint"""
        success, data = self.test_api_endpoint("Market Overview", "GET", "stocks/market-overview")
        
        if success:
            required_keys = ['nifty_50', 'market_status', 'market_sentiment']
            missing_keys = [key for key in required_keys if key not in data]
            
            if missing_keys:
                self.log_test("Market Overview Structure", False, f"Missing keys: {missing_keys}")
            else:
                nifty_data = data.get('nifty_50', {})
                self.log_test("Market Overview Structure", True, 
                            f"NIFTY: {nifty_data.get('current', 'N/A')}, Status: {data.get('market_status', 'N/A')}")
        
        return success

    def test_watchlist_operations(self):
        """Test watchlist CRUD operations"""
        test_symbol = 'RELIANCE'
        
        # Get initial watchlist
        success1, data1 = self.test_api_endpoint("Watchlist - Get", "GET", "watchlist")
        initial_count = len(data1.get('watchlist', [])) if success1 else 0
        
        # Add to watchlist
        success2, data2 = self.test_api_endpoint("Watchlist - Add", "POST", "watchlist", 
                                                params={"symbol": test_symbol})
        
        # Verify addition
        success3, data3 = self.test_api_endpoint("Watchlist - Verify Add", "GET", "watchlist")
        new_count = len(data3.get('watchlist', [])) if success3 else 0
        
        if success3:
            self.log_test("Watchlist Add Verification", new_count > initial_count, 
                        f"Count changed from {initial_count} to {new_count}")
        
        # Remove from watchlist
        success4, data4 = self.test_api_endpoint("Watchlist - Remove", "DELETE", f"watchlist/{test_symbol}")
        
        # Verify removal
        success5, data5 = self.test_api_endpoint("Watchlist - Verify Remove", "GET", "watchlist")
        final_count = len(data5.get('watchlist', [])) if success5 else 0
        
        if success5:
            self.log_test("Watchlist Remove Verification", final_count == initial_count, 
                        f"Count returned to {final_count} (initial: {initial_count})")
        
        return success1 and success2 and success4

    def test_error_handling(self):
        """Test error handling for invalid requests"""
        # Test invalid stock symbol
        success1, data1 = self.test_api_endpoint("Error - Invalid Stock", "GET", "stocks/INVALID123", 
                                                expected_status=404)
        
        # Test invalid chart timeframe
        success2, data2 = self.test_api_endpoint("Error - Invalid Timeframe", "GET", "stocks/RELIANCE/chart", 
                                                params={"timeframe": "invalid"})
        
        # Test invalid watchlist operation
        success3, data3 = self.test_api_endpoint("Error - Invalid Watchlist Add", "POST", "watchlist", 
                                                params={"symbol": "INVALID123"}, expected_status=404)
        
        return success1 and success2 and success3

    def run_comprehensive_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting Comprehensive Backend API Testing")
        print("=" * 60)
        print(f"Testing API at: {self.api_url}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print()

        # Core API Tests
        print("📋 CORE API TESTS")
        print("-" * 30)
        self.test_root_endpoint()
        self.test_nse_symbols()
        self.test_stock_search()
        
        print("\n📊 STOCK DATA TESTS")
        print("-" * 30)
        self.test_individual_stock_data()
        self.test_stock_chart_data()
        
        print("\n🔍 BREAKOUT ANALYSIS TESTS")
        print("-" * 30)
        self.test_breakout_scanning()
        
        print("\n📈 MARKET DATA TESTS")
        print("-" * 30)
        self.test_market_overview()
        
        print("\n⭐ WATCHLIST TESTS")
        print("-" * 30)
        self.test_watchlist_operations()
        
        print("\n🚨 ERROR HANDLING TESTS")
        print("-" * 30)
        self.test_error_handling()
        
        # Print final results
        print("\n" + "=" * 60)
        print("📊 FINAL TEST RESULTS")
        print("=" * 60)
        print(f"Total Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        # Show failed tests
        failed_tests = [test for test in self.test_results if not test['success']]
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"  • {test['test_name']}: {test['details']}")
        
        print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        return self.tests_passed == self.tests_run

def main():
    """Main test execution"""
    tester = StockBreakoutAPITester()
    
    try:
        all_passed = tester.run_comprehensive_tests()
        return 0 if all_passed else 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n💥 Unexpected error during testing: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())