#!/usr/bin/env python3
"""
Focused Backend Testing for Enhanced StockBreak Pro
Tests specific requirements from the review request
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, List, Optional

class FocusedStockBreakoutTester:
    def __init__(self, base_url="https://nse-breakout-scan.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

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
            else:
                raise ValueError(f"Unsupported method: {method}")

            success = response.status_code == expected_status
            
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text[:500]}
            
            details = f"Status: {response.status_code}"
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

    def test_nse_symbols_coverage(self):
        """Test 1: Full NSE Coverage - Verify 594+ stocks available"""
        print("🔍 TEST 1: FULL NSE COVERAGE")
        print("-" * 40)
        
        success, data = self.test_api_endpoint("NSE Symbols Coverage", "GET", "stocks/symbols")
        
        if success:
            symbols = data.get('symbols', [])
            symbols_with_sectors = data.get('symbols_with_sectors', {})
            total_symbols = len(symbols)
            sectors = list(set(symbols_with_sectors.values())) if symbols_with_sectors else []
            
            # Test coverage requirements
            full_coverage = total_symbols >= 594
            sector_coverage = len(sectors) >= 35
            
            self.log_test("Stock Count Coverage", full_coverage, 
                        f"Found {total_symbols} stocks (required: 594+)")
            
            self.log_test("Sector Coverage", sector_coverage, 
                        f"Found {len(sectors)} sectors (required: 35+)")
            
            # Test specific expected symbols
            expected_symbols = ['RELIANCE', 'TCS', 'HDFCBANK', 'INFOSYS', 'HINDUNILVR']
            found_symbols = [s for s in expected_symbols if s in symbols]
            
            self.log_test("Key Symbols Present", len(found_symbols) == len(expected_symbols), 
                        f"Found {len(found_symbols)}/{len(expected_symbols)} key symbols")
        
        return success

    def test_enhanced_technical_indicators(self):
        """Test 2: Enhanced Technical Indicators - All indicators working"""
        print("📈 TEST 2: ENHANCED TECHNICAL INDICATORS")
        print("-" * 45)
        
        # Test key stocks for all required indicators
        test_symbols = ['RELIANCE', 'TCS', 'MPHASIS']
        
        for symbol in test_symbols:
            success, data = self.test_api_endpoint(f"Technical Indicators - {symbol}", "GET", f"stocks/{symbol}")
            
            if success:
                technical_data = data.get('technical_indicators', {})
                
                # Required indicators from review request
                required_indicators = {
                    'rsi': 'RSI',
                    'macd': 'MACD',
                    'macd_signal': 'MACD Signal',
                    'macd_histogram': 'MACD Histogram',
                    'bollinger_upper': 'Bollinger Upper',
                    'bollinger_middle': 'Bollinger Middle',
                    'bollinger_lower': 'Bollinger Lower',
                    'stochastic_k': 'Stochastic %K',
                    'stochastic_d': 'Stochastic %D',
                    'vwap': 'VWAP',
                    'atr': 'ATR',
                    'support_level': 'Support Level',
                    'resistance_level': 'Resistance Level'
                }
                
                present_indicators = []
                missing_indicators = []
                
                for key, name in required_indicators.items():
                    if technical_data.get(key) is not None:
                        present_indicators.append(name)
                    else:
                        missing_indicators.append(name)
                
                coverage_rate = len(present_indicators) / len(required_indicators) * 100
                
                self.log_test(f"{symbol} Indicator Coverage", coverage_rate >= 80, 
                            f"{len(present_indicators)}/{len(required_indicators)} indicators ({coverage_rate:.1f}%)")
                
                if missing_indicators:
                    print(f"    Missing: {', '.join(missing_indicators[:3])}{'...' if len(missing_indicators) > 3 else ''}")
        
        return True

    def test_breakout_scanning_performance(self):
        """Test 3: Breakout Scanning Performance with larger datasets"""
        print("⚡ TEST 3: BREAKOUT SCANNING PERFORMANCE")
        print("-" * 42)
        
        # Test different limits to verify scaling
        test_limits = [50, 100, 200]
        
        for limit in test_limits:
            success, data = self.test_api_endpoint(f"Breakout Scan - {limit} stocks", "GET", "stocks/breakouts/scan", 
                                                 params={"limit": str(limit)}, timeout=60)
            
            if success:
                total_scanned = data.get('total_scanned', 0)
                breakouts_found = data.get('breakouts_found', 0)
                scan_stats = data.get('scan_statistics', {})
                scan_time = scan_stats.get('scan_time_seconds', 0)
                
                # Performance expectations
                expected_scanned = min(limit, 594)  # Can't scan more than available
                scanned_correctly = total_scanned >= expected_scanned * 0.9  # Allow 10% variance
                
                self.log_test(f"Scan Coverage - {limit} limit", scanned_correctly, 
                            f"Scanned {total_scanned} stocks (expected ~{expected_scanned})")
                
                if scan_time > 0:
                    performance_good = scan_time < (limit * 0.3)  # Max 0.3s per stock
                    self.log_test(f"Scan Performance - {limit} stocks", performance_good, 
                                f"Completed in {scan_time:.2f}s ({total_scanned/scan_time:.1f} stocks/sec)")
        
        return True

    def test_watchlist_functionality(self):
        """Test 4: Enhanced Watchlist Backend"""
        print("⭐ TEST 4: ENHANCED WATCHLIST BACKEND")
        print("-" * 37)
        
        # Test basic watchlist operations
        success1, data1 = self.test_api_endpoint("Watchlist - Get Initial", "GET", "watchlist")
        
        if success1:
            initial_count = len(data1.get('watchlist', []))
            
            # Test adding a stock
            success2, data2 = self.test_api_endpoint("Watchlist - Add Stock", "POST", "watchlist", 
                                                   params={"symbol": "RELIANCE"})
            
            # Verify addition
            success3, data3 = self.test_api_endpoint("Watchlist - Verify Add", "GET", "watchlist")
            
            if success3:
                new_count = len(data3.get('watchlist', []))
                add_successful = new_count > initial_count
                
                self.log_test("Watchlist Add Operation", add_successful, 
                            f"Count: {initial_count} → {new_count}")
                
                # Test watchlist data includes technical analysis
                watchlist_items = data3.get('watchlist', [])
                if watchlist_items:
                    item = watchlist_items[0]
                    has_technical_data = 'technical_indicators' in item or 'current_price' in item
                    
                    self.log_test("Watchlist Technical Data", has_technical_data, 
                                "Watchlist items include market data")
                
                # Clean up - remove the test stock
                self.test_api_endpoint("Watchlist - Remove Stock", "DELETE", "watchlist/RELIANCE")
        
        return success1

    def test_data_quality_validation(self):
        """Test 5: Data Quality - No null/undefined values, reasonable indicator values"""
        print("🔍 TEST 5: DATA QUALITY VALIDATION")
        print("-" * 35)
        
        test_symbols = ['RELIANCE', 'TCS', 'HINDUNILVR']
        quality_issues = []
        
        for symbol in test_symbols:
            success, data = self.test_api_endpoint(f"Data Quality - {symbol}", "GET", f"stocks/{symbol}")
            
            if success:
                # Test 1: No null values in critical fields
                critical_fields = ['current_price', 'change_percent', 'volume', 'symbol']
                null_fields = [field for field in critical_fields if data.get(field) is None]
                
                if null_fields:
                    quality_issues.append(f"{symbol}: Null values in {null_fields}")
                
                # Test 2: Technical indicators have reasonable values
                technical_data = data.get('technical_indicators', {})
                current_price = data.get('current_price', 0)
                
                if technical_data and current_price > 0:
                    # RSI should be 0-100
                    rsi = technical_data.get('rsi')
                    if rsi is not None and not (0 <= rsi <= 100):
                        quality_issues.append(f"{symbol}: RSI {rsi} outside 0-100 range")
                    
                    # Bollinger Bands should be ordered correctly
                    bb_upper = technical_data.get('bollinger_upper')
                    bb_middle = technical_data.get('bollinger_middle')
                    bb_lower = technical_data.get('bollinger_lower')
                    
                    if all(x is not None for x in [bb_upper, bb_middle, bb_lower]):
                        if not (bb_lower < bb_middle < bb_upper):
                            quality_issues.append(f"{symbol}: Bollinger Bands not properly ordered")
                
                # Test 3: Trading recommendations have logical values
                trading_rec = data.get('trading_recommendation')
                if trading_rec:
                    entry = trading_rec.get('entry_price', 0)
                    stop = trading_rec.get('stop_loss', 0)
                    target = trading_rec.get('target_price', 0)
                    
                    if entry > 0 and stop > 0 and target > 0:
                        if not (stop < entry < target):
                            quality_issues.append(f"{symbol}: Trading prices not logical (stop: {stop}, entry: {entry}, target: {target})")
        
        # Overall data quality assessment
        data_quality_good = len(quality_issues) == 0
        
        self.log_test("Overall Data Quality", data_quality_good, 
                    f"Found {len(quality_issues)} quality issues" if quality_issues else "No quality issues found")
        
        if quality_issues:
            for issue in quality_issues[:3]:  # Show first 3 issues
                print(f"    Issue: {issue}")
        
        return data_quality_good

    def test_sector_filtering(self):
        """Test 6: Sector filtering works across all sectors"""
        print("🏭 TEST 6: SECTOR FILTERING")
        print("-" * 27)
        
        # Test key sectors
        test_sectors = ['IT', 'Banking', 'Pharma', 'Auto']
        
        for sector in test_sectors:
            success, data = self.test_api_endpoint(f"Sector Filter - {sector}", "GET", "stocks/breakouts/scan", 
                                                 params={"sector": sector, "limit": "100"}, timeout=45)
            
            if success:
                total_scanned = data.get('total_scanned', 0)
                breakouts_found = data.get('breakouts_found', 0)
                
                # Verify sector filtering is working (should scan some stocks in each major sector)
                sector_has_stocks = total_scanned > 0
                
                self.log_test(f"{sector} Sector Filtering", sector_has_stocks, 
                            f"Scanned {total_scanned} {sector} stocks, found {breakouts_found} breakouts")
        
        return True

    def run_focused_tests(self):
        """Run focused tests for Enhanced StockBreak Pro"""
        print("🚀 ENHANCED STOCKBREAK PRO - FOCUSED TESTING")
        print("=" * 55)
        print(f"Testing API at: {self.api_url}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 55)
        print()

        # Run all focused tests
        self.test_nse_symbols_coverage()
        self.test_enhanced_technical_indicators()
        self.test_breakout_scanning_performance()
        self.test_watchlist_functionality()
        self.test_data_quality_validation()
        self.test_sector_filtering()
        
        # Print final results
        print("=" * 55)
        print("📊 FOCUSED TEST RESULTS")
        print("=" * 55)
        print(f"Total Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 55)
        
        return self.tests_passed >= (self.tests_run * 0.8)  # 80% pass rate

def main():
    """Main test execution"""
    tester = FocusedStockBreakoutTester()
    
    try:
        success = tester.run_focused_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n💥 Unexpected error during testing: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())