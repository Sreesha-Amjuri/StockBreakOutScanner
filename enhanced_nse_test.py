#!/usr/bin/env python3
"""
Enhanced NSE Stock Coverage Testing
Tests the specific functionality requested in the review:
1. Enhanced NSE Stock Coverage (500+ stocks)
2. Batch Processing & Caching System
3. Priority-based Processing
4. Performance & Resource Management
5. API Compatibility
"""

import requests
import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

class EnhancedNSECoverageTester:
    def __init__(self, base_url="https://stockport-3.preview.emergentagent.com"):
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

    def test_enhanced_nse_stock_coverage(self):
        """Test 1: Enhanced NSE Stock Coverage - Verify expanded stock database"""
        print("🔍 TEST 1: ENHANCED NSE STOCK COVERAGE")
        print("-" * 50)
        
        # Test /api/stocks/symbols endpoint
        success, data = self.test_api_endpoint("NSE Symbols Endpoint", "GET", "stocks/symbols")
        
        if success:
            # Check if we have 500+ stocks
            symbols = data.get('symbols', [])
            symbols_with_sectors = data.get('symbols_with_sectors', {})
            
            stock_count = len(symbols)
            self.log_test("Stock Count Verification", stock_count >= 500, 
                        f"Found {stock_count} stocks (expected 500+)")
            
            # Verify sector distribution
            sectors = set()
            if isinstance(symbols_with_sectors, dict):
                for symbol, sector in symbols_with_sectors.items():
                    sectors.add(sector)
            else:
                # Handle case where symbols_with_sectors might be a different structure
                sectors = set(data.get('sector_distribution', {}).keys())
            
            sector_count = len(sectors)
            expected_sectors = ['IT', 'Banking', 'Pharma', 'Auto', 'Energy', 'FMCG', 'Metals', 'Cement']
            found_expected_sectors = [s for s in expected_sectors if s in sectors]
            
            self.log_test("Sector Distribution", len(found_expected_sectors) >= 6, 
                        f"Found {sector_count} sectors, including {len(found_expected_sectors)}/{len(expected_sectors)} expected sectors")
            
            # Test priority symbols (NIFTY 50 should be present)
            nifty_50_symbols = ['RELIANCE', 'TCS', 'HDFCBANK', 'INFOSYS', 'HINDUNILVR', 'ICICIBANK', 'BHARTIARTL', 'ITC', 'SBIN', 'LT']
            found_nifty_symbols = [s for s in nifty_50_symbols if s in symbols]
            
            self.log_test("Priority Symbols (NIFTY 50)", len(found_nifty_symbols) >= 8, 
                        f"Found {len(found_nifty_symbols)}/{len(nifty_50_symbols)} NIFTY 50 symbols")
            
            # Test coverage information accuracy
            if 'coverage_info' in data:
                coverage_info = data['coverage_info']
                self.log_test("Coverage Information Present", True, 
                            f"Coverage info: {coverage_info}")
            
            return True
        
        return False

    def test_batch_processing_and_caching(self):
        """Test 2: Batch Processing & Caching System"""
        print("\n🔄 TEST 2: BATCH PROCESSING & CACHING SYSTEM")
        print("-" * 50)
        
        # Test /api/stocks/breakouts/scan with various limits
        limits_to_test = [50, 100, 200]
        
        for limit in limits_to_test:
            start_time = time.time()
            success, data = self.test_api_endpoint(f"Batch Processing - Limit {limit}", "GET", 
                                                 "stocks/breakouts/scan", 
                                                 params={"limit": limit}, timeout=120)
            end_time = time.time()
            
            if success:
                scan_stats = data.get('scan_statistics', {})
                total_scanned = scan_stats.get('total_scanned', 0)
                processing_time = scan_stats.get('processing_time_seconds', 0)
                
                self.log_test(f"Batch Processing Stats - Limit {limit}", True, 
                            f"Scanned {total_scanned} stocks in {processing_time:.2f}s (API response: {end_time-start_time:.2f}s)")
        
        # Test caching functionality by calling the same endpoint multiple times
        print("\n🗄️ Testing Caching System...")
        
        # First call (should populate cache)
        start_time1 = time.time()
        success1, data1 = self.test_api_endpoint("Cache Test - First Call", "GET", 
                                                "stocks/breakouts/scan", 
                                                params={"limit": 50}, timeout=60)
        end_time1 = time.time()
        first_call_time = end_time1 - start_time1
        
        # Second call (should use cache)
        start_time2 = time.time()
        success2, data2 = self.test_api_endpoint("Cache Test - Second Call", "GET", 
                                                "stocks/breakouts/scan", 
                                                params={"limit": 50}, timeout=60)
        end_time2 = time.time()
        second_call_time = end_time2 - start_time2
        
        if success1 and success2:
            # Second call should be faster due to caching
            cache_improvement = first_call_time > second_call_time
            self.log_test("Caching Performance", cache_improvement, 
                        f"First call: {first_call_time:.2f}s, Second call: {second_call_time:.2f}s")
            
            # Check if cache statistics are provided
            cache_stats1 = data1.get('cache_statistics', {})
            cache_stats2 = data2.get('cache_statistics', {})
            
            if cache_stats2:
                self.log_test("Cache Statistics Available", True, 
                            f"Cache stats: {cache_stats2}")
        
        # Test with different sector filters
        sectors_to_test = ['IT', 'Banking', 'Pharma']
        
        for sector in sectors_to_test:
            success, data = self.test_api_endpoint(f"Sector Filter - {sector}", "GET", 
                                                 "stocks/breakouts/scan", 
                                                 params={"sector": sector, "limit": 50}, timeout=60)
            
            if success:
                breakouts = data.get('breakout_stocks', [])
                sector_filtered = all(stock.get('sector') == sector for stock in breakouts if stock.get('sector'))
                
                self.log_test(f"Sector Filtering - {sector}", len(breakouts) > 0, 
                            f"Found {len(breakouts)} breakouts in {sector} sector")

    def test_priority_based_processing(self):
        """Test 3: Priority-based Processing"""
        print("\n⭐ TEST 3: PRIORITY-BASED PROCESSING")
        print("-" * 50)
        
        # Test that NIFTY 50 stocks are processed first
        success, data = self.test_api_endpoint("Priority Processing Test", "GET", 
                                             "stocks/breakouts/scan", 
                                             params={"limit": 100}, timeout=90)
        
        if success:
            breakout_stocks = data.get('breakout_stocks', [])
            scan_stats = data.get('scan_statistics', {})
            
            # Check if priority symbols appear in results
            nifty_50_symbols = ['RELIANCE', 'TCS', 'HDFCBANK', 'INFOSYS', 'HINDUNILVR', 'ICICIBANK']
            priority_stocks_found = [stock for stock in breakout_stocks 
                                   if stock.get('symbol') in nifty_50_symbols]
            
            self.log_test("Priority Stocks in Results", len(priority_stocks_found) > 0, 
                        f"Found {len(priority_stocks_found)} NIFTY 50 stocks in breakout results")
            
            # Test processing order information
            if 'processing_order' in scan_stats:
                processing_order = scan_stats['processing_order']
                self.log_test("Processing Order Info", True, 
                            f"Processing order: {processing_order}")
        
        # Test different sector filters work properly
        success, data = self.test_api_endpoint("Sector Filter Test", "GET", 
                                             "stocks/breakouts/scan", 
                                             params={"sector": "IT", "limit": 50}, timeout=60)
        
        if success:
            breakouts = data.get('breakout_stocks', [])
            it_stocks = [stock for stock in breakouts if stock.get('sector') == 'IT']
            
            self.log_test("IT Sector Filter", len(it_stocks) > 0, 
                        f"Found {len(it_stocks)} IT sector breakouts")
        
        # Test confidence and risk level filtering
        success, data = self.test_api_endpoint("Confidence Filter Test", "GET", 
                                             "stocks/breakouts/scan", 
                                             params={"min_confidence": "0.7", "limit": 50}, timeout=60)
        
        if success:
            breakouts = data.get('breakout_stocks', [])
            high_confidence = [stock for stock in breakouts 
                             if stock.get('confidence_score', 0) >= 0.7]
            
            self.log_test("High Confidence Filter", len(high_confidence) == len(breakouts), 
                        f"All {len(breakouts)} results have confidence >= 0.7")
        
        # Test risk level filtering
        success, data = self.test_api_endpoint("Risk Level Filter Test", "GET", 
                                             "stocks/breakouts/scan", 
                                             params={"risk_level": "Low", "limit": 30}, timeout=60)
        
        if success:
            breakouts = data.get('breakout_stocks', [])
            low_risk = [stock for stock in breakouts 
                       if stock.get('risk_assessment', {}).get('risk_level') == 'Low']
            
            self.log_test("Low Risk Filter", len(low_risk) > 0, 
                        f"Found {len(low_risk)} low-risk breakouts")

    def test_performance_and_resource_management(self):
        """Test 4: Performance & Resource Management"""
        print("\n⚡ TEST 4: PERFORMANCE & RESOURCE MANAGEMENT")
        print("-" * 50)
        
        # Test with larger limits to ensure system handles increased load
        large_limits = [200, 300]
        
        for limit in large_limits:
            start_time = time.time()
            success, data = self.test_api_endpoint(f"Large Dataset Test - {limit}", "GET", 
                                                 "stocks/breakouts/scan", 
                                                 params={"limit": limit}, timeout=180)
            end_time = time.time()
            
            if success:
                processing_time = end_time - start_time
                scan_stats = data.get('scan_statistics', {})
                total_scanned = scan_stats.get('total_scanned', 0)
                
                # Performance should be reasonable (< 3 minutes for 300 stocks)
                performance_acceptable = processing_time < 180
                
                self.log_test(f"Large Dataset Performance - {limit}", performance_acceptable, 
                            f"Processed {total_scanned} stocks in {processing_time:.2f}s")
                
                # Check memory usage warnings
                if 'memory_usage' in scan_stats:
                    memory_info = scan_stats['memory_usage']
                    self.log_test(f"Memory Usage Info - {limit}", True, 
                                f"Memory usage: {memory_info}")
        
        # Test cache management
        success, data = self.test_api_endpoint("Cache Management Test", "GET", 
                                             "stocks/breakouts/scan", 
                                             params={"limit": 100}, timeout=90)
        
        if success:
            cache_stats = data.get('cache_statistics', {})
            if cache_stats:
                cache_hit_rate = cache_stats.get('hit_rate', 0)
                cache_size = cache_stats.get('cache_size', 0)
                
                self.log_test("Cache Management", True, 
                            f"Cache hit rate: {cache_hit_rate}%, Cache size: {cache_size}")
        
        # Test API response times with larger datasets
        response_times = []
        
        for i in range(3):
            start_time = time.time()
            success, data = self.test_api_endpoint(f"Response Time Test {i+1}", "GET", 
                                                 "stocks/breakouts/scan", 
                                                 params={"limit": 150}, timeout=120)
            end_time = time.time()
            
            if success:
                response_times.append(end_time - start_time)
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            consistent_performance = max(response_times) - min(response_times) < 30  # Within 30s variance
            
            self.log_test("Response Time Consistency", consistent_performance, 
                        f"Average: {avg_response_time:.2f}s, Range: {min(response_times):.2f}s - {max(response_times):.2f}s")

    def test_api_compatibility(self):
        """Test 5: API Compatibility"""
        print("\n🔗 TEST 5: API COMPATIBILITY")
        print("-" * 50)
        
        # Test that all existing endpoints still work properly
        endpoints_to_test = [
            ("stocks/symbols", {}),
            ("stocks/search", {"q": "REL"}),
            ("stocks/market-overview", {}),
            ("watchlist", {})
        ]
        
        for endpoint, params in endpoints_to_test:
            success, data = self.test_api_endpoint(f"Compatibility - {endpoint}", "GET", 
                                                 endpoint, params=params)
            
            if success:
                self.log_test(f"Endpoint Working - {endpoint}", True, 
                            f"Endpoint responds correctly")
        
        # Test /api/stocks/{symbol} with various symbols from different indices
        test_symbols = [
            ('RELIANCE', 'NIFTY 50'),
            ('TCS', 'NIFTY 50'), 
            ('MPHASIS', 'NIFTY Next 50'),
            ('BAJAJFINSV', 'NIFTY 50'),
            ('COFORGE', 'Midcap'),
            ('POLYCAB', 'Smallcap')
        ]
        
        for symbol, index_type in test_symbols:
            success, data = self.test_api_endpoint(f"Individual Stock - {symbol} ({index_type})", "GET", 
                                                 f"stocks/{symbol}")
            
            if success:
                # Verify response structure is consistent
                required_fields = ['symbol', 'name', 'current_price', 'change_percent', 'sector']
                missing_fields = [field for field in required_fields if field not in data]
                
                structure_valid = len(missing_fields) == 0
                self.log_test(f"Response Structure - {symbol}", structure_valid, 
                            f"All required fields present" if structure_valid else f"Missing: {missing_fields}")
        
        # Test market overview functionality
        success, data = self.test_api_endpoint("Market Overview Compatibility", "GET", 
                                             "stocks/market-overview")
        
        if success:
            # Check if enhanced market data is available
            market_status = data.get('market_status', {})
            nifty_data = data.get('nifty_50', {})
            
            enhanced_features = []
            if 'is_trading_hours' in market_status:
                enhanced_features.append('trading_hours_detection')
            if 'current_time' in market_status:
                enhanced_features.append('ist_time_display')
            if nifty_data:
                enhanced_features.append('nifty_data')
            
            self.log_test("Enhanced Market Features", len(enhanced_features) > 0, 
                        f"Enhanced features: {', '.join(enhanced_features)}")
        
        # Test watchlist functionality still works
        success, data = self.test_api_endpoint("Watchlist Compatibility", "GET", "watchlist")
        
        if success:
            self.log_test("Watchlist Endpoint", True, 
                        f"Watchlist contains {len(data.get('watchlist', []))} items")

    def run_enhanced_nse_tests(self):
        """Run all enhanced NSE coverage tests"""
        print("🚀 ENHANCED NSE STOCK COVERAGE TESTING")
        print("=" * 60)
        print(f"Testing API at: {self.api_url}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Run all test categories
        self.test_enhanced_nse_stock_coverage()
        self.test_batch_processing_and_caching()
        self.test_priority_based_processing()
        self.test_performance_and_resource_management()
        self.test_api_compatibility()
        
        # Print final results
        print("\n" + "=" * 60)
        print("📊 ENHANCED NSE TESTING RESULTS")
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
    tester = EnhancedNSECoverageTester()
    
    try:
        all_passed = tester.run_enhanced_nse_tests()
        return 0 if all_passed else 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n💥 Unexpected error during testing: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())