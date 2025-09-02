#!/usr/bin/env python3
"""
Comprehensive Testing Suite for StockBreak Pro
Tests all functionality including the expanded NSE stock coverage
"""

import requests
import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

class StockBreakProTester:
    def __init__(self, base_url="http://localhost:8001"):
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
        url = f"{self.api_url}/{endpoint}" if endpoint else self.api_url
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

    def test_backend_health(self):
        """Test backend health and connectivity"""
        print("🏥 BACKEND HEALTH TESTS")
        print("-" * 40)
        
        # Test API root
        success1, data1 = self.test_api_endpoint("API Root", "GET", "")
        
        # Test health endpoint
        success2, data2 = self.test_api_endpoint("Health Check", "GET", "health")
        
        if success2:
            db_status = data2.get('database', 'unknown')
            data_status = data2.get('market_data', 'unknown')
            total_stocks = data2.get('total_stocks', 0)
            
            self.log_test("Database Connection", db_status == 'connected', f"Status: {db_status}")
            self.log_test("Market Data Access", data_status == 'available', f"Status: {data_status}")
            self.log_test("Stock Universe Size", total_stocks >= 200, f"Total stocks: {total_stocks}")
        
        return success1 and success2

    def test_expanded_stock_coverage(self):
        """Test the expanded NSE stock coverage"""
        print("📈 EXPANDED STOCK COVERAGE TESTS")
        print("-" * 40)
        
        # Test symbols endpoint
        success, data = self.test_api_endpoint("NSE Symbols - Expanded", "GET", "stocks/symbols")
        
        if success:
            symbols = data.get('symbols', [])
            sectors = data.get('sectors', [])
            count = data.get('count', 0)
            
            # Test coverage expansion
            self.log_test("Stock Count Expansion", count >= 200, f"Found {count} stocks (target: 200+)")
            self.log_test("Sector Diversity", len(sectors) >= 15, f"Found {len(sectors)} sectors")
            
            # Test for key sectors
            expected_sectors = ['IT', 'Banking', 'Auto', 'Pharma', 'FMCG', 'Telecom', 'Real Estate', 'Power']
            found_sectors = [s for s in expected_sectors if s in sectors]
            self.log_test("Key Sectors Present", len(found_sectors) >= 6, 
                        f"Found {len(found_sectors)}/{len(expected_sectors)} key sectors")
            
            # Test for specific expanded stocks
            expanded_stocks = ['MPHASIS', 'HDFCLIFE', 'MINDTREE', 'PERSISTENT', 'COFORGE', 'LUPIN', 'BIOCON']
            found_expanded = [s for s in expanded_stocks if s in symbols]
            self.log_test("Expanded Stock Coverage", len(found_expanded) >= 5, 
                        f"Found {len(found_expanded)}/{len(expanded_stocks)} expanded stocks")
        
        return success

    def test_breakout_scanning_performance(self):
        """Test breakout scanning with expanded stock universe"""
        print("🔍 BREAKOUT SCANNING PERFORMANCE TESTS")
        print("-" * 40)
        
        # Test basic scan with increased limit
        start_time = time.time()
        success1, data1 = self.test_api_endpoint("Breakout Scan - 200 Stocks", "GET", "stocks/breakouts/scan", 
                                                params={"limit": "200"}, timeout=120)
        scan_time = time.time() - start_time
        
        if success1:
            breakouts_found = data1.get('breakouts_found', 0)
            total_scanned = data1.get('total_scanned', 0)
            
            self.log_test("Scan Performance", scan_time < 120, f"Scanned {total_scanned} stocks in {scan_time:.1f}s")
            self.log_test("Breakout Detection", breakouts_found > 0, f"Found {breakouts_found} breakouts")
            
            # Test breakout quality
            breakout_stocks = data1.get('breakout_stocks', [])
            if breakout_stocks:
                high_confidence = [s for s in breakout_stocks if s.get('confidence_score', 0) >= 0.7]
                self.log_test("High Confidence Breakouts", len(high_confidence) > 0, 
                            f"Found {len(high_confidence)} high-confidence breakouts")
        
        # Test sector-specific scans
        test_sectors = ['IT', 'Banking', 'Auto', 'Pharma']
        for sector in test_sectors:
            success, data = self.test_api_endpoint(f"Sector Scan - {sector}", "GET", "stocks/breakouts/scan", 
                                                 params={"sector": sector, "limit": "50"}, timeout=60)
            if success:
                scanned = data.get('total_scanned', 0)
                found = data.get('breakouts_found', 0)
                self.log_test(f"{sector} Sector Coverage", scanned > 0, f"Scanned {scanned} {sector} stocks, found {found} breakouts")
        
        return success1

    def test_individual_stock_validation(self):
        """Test individual stock data accuracy"""
        print("📊 INDIVIDUAL STOCK VALIDATION")
        print("-" * 40)
        
        # Test stocks from different sectors and market caps
        test_stocks = {
            'RELIANCE': 'Large Cap Oil & Gas',
            'TCS': 'Large Cap IT',
            'MPHASIS': 'Mid Cap IT',
            'HDFCLIFE': 'Large Cap Insurance',
            'MINDTREE': 'Mid Cap IT',
            'PERSISTENT': 'Mid Cap IT',
            'LUPIN': 'Large Cap Pharma',
            'FEDERALBNK': 'Mid Cap Banking'
        }
        
        successful_validations = 0
        
        for symbol, description in test_stocks.items():
            # Test basic stock data
            success1, stock_data = self.test_api_endpoint(f"Stock Data - {symbol}", "GET", f"stocks/{symbol}")
            
            if success1:
                successful_validations += 1
                
                # Validate data structure
                required_fields = ['symbol', 'name', 'current_price', 'technical_indicators', 'risk_assessment']
                missing_fields = [f for f in required_fields if f not in stock_data]
                
                if not missing_fields:
                    self.log_test(f"Data Structure - {symbol}", True, 
                                f"{description}: ₹{stock_data['current_price']:.2f}")
                else:
                    self.log_test(f"Data Structure - {symbol}", False, f"Missing: {missing_fields}")
                
                # Test data validation endpoint
                success2, validation_data = self.test_api_endpoint(f"Data Validation - {symbol}", "GET", f"stocks/{symbol}/validate")
                
                if success2:
                    quality_score = validation_data.get('data_quality_score', 0)
                    quality_level = validation_data.get('quality_level', 'Unknown')
                    
                    self.log_test(f"Data Quality - {symbol}", quality_score >= 60, 
                                f"Score: {quality_score}/100, Level: {quality_level}")
        
        self.log_test("Overall Stock Validation", successful_validations >= 6, 
                    f"{successful_validations}/{len(test_stocks)} stocks validated successfully")
        
        return successful_validations > 0

    def test_market_data_accuracy(self):
        """Test market overview and real-time data"""
        print("📈 MARKET DATA ACCURACY TESTS")
        print("-" * 40)
        
        success, data = self.test_api_endpoint("Market Overview", "GET", "stocks/market-overview")
        
        if success:
            nifty_data = data.get('nifty_50', {})
            market_status = data.get('market_status', {})
            
            # Test NIFTY data
            nifty_price = nifty_data.get('current', 0)
            nifty_change = nifty_data.get('change_percent', 0)
            
            self.log_test("NIFTY Data Validity", nifty_price > 20000, 
                        f"NIFTY: {nifty_price:.2f} ({nifty_change:+.2f}%)")
            
            # Test market status
            status = market_status.get('status', 'UNKNOWN')
            current_time = market_status.get('current_time', '')
            
            self.log_test("Market Status Detection", status in ['OPEN', 'CLOSED', 'PRE_OPEN'], 
                        f"Status: {status}, Time: {current_time}")
            
            # Test IST time format
            ist_valid = 'IST' in current_time
            self.log_test("IST Time Format", ist_valid, f"Time format includes IST: {current_time}")
        
        return success

    def test_watchlist_functionality(self):
        """Test watchlist CRUD operations"""
        print("⭐ WATCHLIST FUNCTIONALITY TESTS")
        print("-" * 40)
        
        test_symbol = 'RELIANCE'
        
        # Get initial watchlist
        success1, data1 = self.test_api_endpoint("Watchlist - Get Initial", "GET", "watchlist")
        initial_count = len(data1.get('watchlist', [])) if success1 else 0
        
        # Add to watchlist
        success2, data2 = self.test_api_endpoint("Watchlist - Add Stock", "POST", "watchlist", 
                                                params={"symbol": test_symbol})
        
        # Verify addition
        success3, data3 = self.test_api_endpoint("Watchlist - Verify Add", "GET", "watchlist")
        new_count = len(data3.get('watchlist', [])) if success3 else 0
        
        add_successful = new_count > initial_count if success3 else False
        self.log_test("Watchlist Add Operation", add_successful, 
                    f"Count: {initial_count} → {new_count}")
        
        # Remove from watchlist
        success4, data4 = self.test_api_endpoint("Watchlist - Remove Stock", "DELETE", f"watchlist/{test_symbol}")
        
        # Verify removal
        success5, data5 = self.test_api_endpoint("Watchlist - Verify Remove", "GET", "watchlist")
        final_count = len(data5.get('watchlist', [])) if success5 else 0
        
        remove_successful = final_count == initial_count if success5 else False
        self.log_test("Watchlist Remove Operation", remove_successful, 
                    f"Count: {new_count} → {final_count}")
        
        return success1 and success2 and success4

    def test_error_handling(self):
        """Test error handling and edge cases"""
        print("🚨 ERROR HANDLING TESTS")
        print("-" * 40)
        
        # Test invalid stock symbol
        success1, data1 = self.test_api_endpoint("Invalid Stock Symbol", "GET", "stocks/INVALID123", 
                                                expected_status=404)
        
        # Test invalid chart timeframe
        success2, data2 = self.test_api_endpoint("Invalid Chart Timeframe", "GET", "stocks/RELIANCE/chart", 
                                                params={"timeframe": "invalid"})
        
        # Test invalid sector filter
        success3, data3 = self.test_api_endpoint("Invalid Sector Filter", "GET", "stocks/breakouts/scan", 
                                                params={"sector": "INVALID_SECTOR"})
        
        # Test empty search query
        success4, data4 = self.test_api_endpoint("Empty Search Query", "GET", "stocks/search", 
                                                params={"q": ""})
        
        return success1 and success3 and success4

    def test_performance_benchmarks(self):
        """Test performance benchmarks for the expanded system"""
        print("⚡ PERFORMANCE BENCHMARK TESTS")
        print("-" * 40)
        
        # Test individual stock fetch speed
        start_time = time.time()
        success1, data1 = self.test_api_endpoint("Single Stock Speed", "GET", "stocks/RELIANCE")
        single_stock_time = time.time() - start_time
        
        self.log_test("Single Stock Fetch Speed", single_stock_time < 5, 
                    f"Fetched in {single_stock_time:.2f}s (target: <5s)")
        
        # Test chart data speed
        start_time = time.time()
        success2, data2 = self.test_api_endpoint("Chart Data Speed", "GET", "stocks/TCS/chart", 
                                                params={"timeframe": "1mo"})
        chart_time = time.time() - start_time
        
        self.log_test("Chart Data Speed", chart_time < 8, 
                    f"Chart fetched in {chart_time:.2f}s (target: <8s)")
        
        # Test search speed
        start_time = time.time()
        success3, data3 = self.test_api_endpoint("Search Speed", "GET", "stocks/search", 
                                                params={"q": "REL"})
        search_time = time.time() - start_time
        
        self.log_test("Search Speed", search_time < 2, 
                    f"Search completed in {search_time:.2f}s (target: <2s)")
        
        return success1 and success2 and success3

    def test_data_accuracy_validation(self):
        """Test data accuracy and validation features"""
        print("🎯 DATA ACCURACY VALIDATION TESTS")
        print("-" * 40)
        
        test_symbols = ['RELIANCE', 'TCS', 'MPHASIS', 'HDFCLIFE']
        accurate_data_count = 0
        
        for symbol in test_symbols:
            # Test data validation endpoint
            success, validation_data = self.test_api_endpoint(f"Data Accuracy - {symbol}", "GET", f"stocks/{symbol}/validate")
            
            if success:
                quality_score = validation_data.get('data_quality_score', 0)
                quality_level = validation_data.get('quality_level', 'Unknown')
                warnings = validation_data.get('warnings', [])
                
                # Check if data is suitable for trading
                trading_suitable = quality_score >= 70
                if trading_suitable:
                    accurate_data_count += 1
                
                self.log_test(f"Trading Data Quality - {symbol}", trading_suitable, 
                            f"Score: {quality_score}/100, Level: {quality_level}")
                
                # Test warning system
                if warnings:
                    self.log_test(f"Data Warnings - {symbol}", True, f"Warnings: {len(warnings)} - {warnings[0] if warnings else 'None'}")
                else:
                    self.log_test(f"Data Freshness - {symbol}", True, "No data quality warnings")
        
        # Overall accuracy assessment
        accuracy_rate = (accurate_data_count / len(test_symbols)) * 100
        self.log_test("Overall Data Accuracy", accuracy_rate >= 75, 
                    f"{accurate_data_count}/{len(test_symbols)} stocks have trading-grade data ({accuracy_rate:.1f}%)")
        
        return accurate_data_count > 0

    def test_trading_recommendations(self):
        """Test trading recommendation accuracy and logic"""
        print("💰 TRADING RECOMMENDATION TESTS")
        print("-" * 40)
        
        # Test stocks that should have breakouts
        test_symbols = ['RELIANCE', 'TCS', 'MPHASIS']
        valid_recommendations = 0
        
        for symbol in test_symbols:
            success, stock_data = self.test_api_endpoint(f"Trading Rec - {symbol}", "GET", f"stocks/{symbol}")
            
            if success:
                trading_rec = stock_data.get('trading_recommendation')
                
                if trading_rec:
                    valid_recommendations += 1
                    
                    # Validate recommendation structure
                    required_fields = ['entry_price', 'stop_loss', 'target_price', 'action', 'risk_reward_ratio']
                    missing_fields = [f for f in required_fields if f not in trading_rec]
                    
                    if not missing_fields:
                        entry = trading_rec['entry_price']
                        stop = trading_rec['stop_loss']
                        target = trading_rec['target_price']
                        action = trading_rec['action']
                        rr_ratio = trading_rec['risk_reward_ratio']
                        
                        # Validate trading logic
                        logic_valid = (
                            stop < entry < target and  # Proper price ordering
                            action in ['BUY', 'WAIT', 'AVOID'] and  # Valid actions
                            1.5 <= rr_ratio <= 4.0  # Reasonable risk-reward
                        )
                        
                        self.log_test(f"Trading Logic - {symbol}", logic_valid, 
                                    f"Entry: ₹{entry}, Stop: ₹{stop}, Target: ₹{target}, Action: {action}")
                    else:
                        self.log_test(f"Trading Structure - {symbol}", False, f"Missing: {missing_fields}")
                else:
                    self.log_test(f"Trading Recommendation - {symbol}", False, "No trading recommendation generated")
        
        self.log_test("Trading Recommendation Coverage", valid_recommendations > 0, 
                    f"{valid_recommendations}/{len(test_symbols)} stocks have valid recommendations")
        
        return valid_recommendations > 0

    def run_comprehensive_tests(self):
        """Run all tests"""
        print("🚀 STOCKBREAK PRO COMPREHENSIVE TESTING")
        print("=" * 60)
        print(f"Testing API at: {self.api_url}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print()

        # Run all test suites
        self.test_backend_health()
        print()
        self.test_expanded_stock_coverage()
        print()
        self.test_breakout_scanning_performance()
        print()
        self.test_individual_stock_validation()
        print()
        self.test_market_data_accuracy()
        print()
        self.test_watchlist_functionality()
        print()
        self.test_error_handling()
        print()
        self.test_performance_benchmarks()
        print()
        self.test_data_accuracy_validation()
        print()
        self.test_trading_recommendations()
        
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
        else:
            print("\n🎉 ALL TESTS PASSED!")
        
        print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        return self.tests_passed == self.tests_run

def main():
    """Main test execution"""
    print("Waiting for backend server to start...")
    time.sleep(3)  # Give server time to start
    
    tester = StockBreakProTester()
    
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