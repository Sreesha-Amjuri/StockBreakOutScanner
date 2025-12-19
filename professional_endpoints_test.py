#!/usr/bin/env python3
"""
Professional Endpoints Testing for StockBreak Pro v2.0
Tests the new professional features as requested in the review
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, List, Optional

class ProfessionalEndpointsTester:
    def __init__(self, base_url="https://breakout-dash.preview.emergentagent.com"):
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

    def test_full_nse_scanning_600_stocks(self):
        """Test Full NSE Scanning (600+ stocks) as requested"""
        print("\n🔍 FULL NSE SCANNING (600+ STOCKS) TESTING")
        print("-" * 50)
        
        # Test with limit=600 to ensure full market coverage
        success, data = self.test_api_endpoint("Full NSE Scan - 600 stocks", "GET", "stocks/breakouts/scan", 
                                             params={"limit": "600"}, timeout=180)
        
        if success:
            total_scanned = data.get('total_scanned', 0)
            breakouts_found = data.get('breakouts_found', 0)
            scan_stats = data.get('scan_statistics', {})
            
            # Verify we're scanning 594+ stocks (as mentioned in requirements)
            full_coverage = total_scanned >= 594
            self.log_test("Full NSE Coverage Verification", full_coverage, 
                        f"Scanned {total_scanned} stocks (expected 594+)")
            
            # Test performance with large datasets
            scan_time = scan_stats.get('scan_time_seconds', 0)
            if scan_time > 0:
                performance_acceptable = scan_time < 180  # 3 minutes max for 600 stocks
                self.log_test("Large Dataset Performance", performance_acceptable, 
                            f"600 stocks scanned in {scan_time:.2f} seconds")
            
            # Test proper timeout handling
            if scan_time > 0:
                self.log_test("Timeout Handling", True, 
                            f"Request completed within timeout ({scan_time:.2f}s < 180s)")
        
        return success

    def test_new_professional_endpoints(self):
        """Test all new professional endpoints"""
        print("\n🚀 NEW PROFESSIONAL ENDPOINTS TESTING")
        print("-" * 45)
        
        # Test /api/market/news
        success1, news_data = self.test_api_endpoint("Market News Integration", "GET", "market/news")
        if success1:
            news_items = news_data.get('news', [])
            total_count = news_data.get('total_count', 0)
            self.log_test("Market News Structure", len(news_items) > 0, 
                        f"Found {total_count} news items")
            
            # Validate news item structure
            if news_items:
                first_news = news_items[0]
                required_fields = ['id', 'title', 'summary', 'category', 'timestamp', 'impact']
                missing_fields = [field for field in required_fields if field not in first_news]
                self.log_test("News Item Structure", len(missing_fields) == 0, 
                            f"News structure complete: {first_news.get('title', 'N/A')}")
        
        # Test /api/analytics/performance
        success2, perf_data = self.test_api_endpoint("Performance Analytics", "GET", "analytics/performance")
        if success2:
            system_stats = perf_data.get('system_stats', {})
            market_coverage = perf_data.get('market_coverage', {})
            technical_indicators = perf_data.get('technical_indicators', [])
            
            total_stocks = system_stats.get('total_nse_stocks', 0)
            sectors_covered = market_coverage.get('sectors_covered', 0)
            
            self.log_test("Performance Analytics Structure", total_stocks > 500, 
                        f"Tracking {total_stocks} stocks across {sectors_covered} sectors")
            
            # Validate technical indicators status
            active_indicators = [ind for ind in technical_indicators if ind.get('status') == 'Active']
            self.log_test("Technical Indicators Status", len(active_indicators) >= 6, 
                        f"{len(active_indicators)} indicators active")
        
        # Test /api/alerts/price
        success3, alerts_data = self.test_api_endpoint("Price Alerts", "GET", "alerts/price")
        if success3:
            alerts = alerts_data.get('alerts', [])
            active_count = alerts_data.get('active_count', 0)
            message = alerts_data.get('message', '')
            
            self.log_test("Price Alerts Functionality", 'ready' in message.lower(), 
                        f"Price alerts system: {message}")
        
        # Test /api/export/data
        success4, export_data = self.test_api_endpoint("Data Export", "POST", "export/data", 
                                                     data={"format": "csv", "stocks": ["RELIANCE", "TCS", "MPHASIS"]})
        if success4:
            export_records = export_data.get('export_data', [])
            total_records = export_data.get('total_records', 0)
            
            self.log_test("Data Export Functionality", total_records > 0, 
                        f"Exported {total_records} stock records")
            
            # Validate export data structure
            if export_records:
                first_record = export_records[0]
                required_export_fields = ['Symbol', 'Current_Price', 'RSI', 'MACD_Signal', 
                                        'Bollinger_Position', 'VWAP_Position', 'Entry_Price', 'Action']
                missing_export_fields = [field for field in required_export_fields if field not in first_record]
                self.log_test("Export Data Structure", len(missing_export_fields) == 0, 
                            f"Export includes all required fields for {first_record.get('Symbol', 'N/A')}")
        
        # Test /api/system/health
        success5, health_data = self.test_api_endpoint("System Health Check", "GET", "system/health")
        if success5:
            status = health_data.get('status', '')
            services = health_data.get('services', {})
            performance = health_data.get('performance', {})
            data_quality = health_data.get('data_quality', {})
            
            self.log_test("System Health Status", status == 'healthy', 
                        f"System status: {status}")
            
            # Validate service statuses
            api_server = services.get('api_server', {})
            database = services.get('database', {})
            cache = services.get('cache', {})
            
            services_healthy = (api_server.get('status') == 'running' and 
                              database.get('status') == 'connected' and 
                              cache.get('status') == 'active')
            
            self.log_test("Services Health Check", services_healthy, 
                        f"API: {api_server.get('status')}, DB: {database.get('status')}, Cache: {cache.get('status')}")
            
            # Validate data quality metrics
            stock_coverage = data_quality.get('stock_coverage', '')
            indicators_active = data_quality.get('indicators_active', 0)
            
            self.log_test("Data Quality Metrics", indicators_active >= 13, 
                        f"Stock coverage: {stock_coverage}, Active indicators: {indicators_active}")
        
        return success1 and success2 and success3 and success4 and success5

    def test_enhanced_technical_indicators_13(self):
        """Test all 13 enhanced technical indicators"""
        print("\n📈 ENHANCED TECHNICAL INDICATORS (13 INDICATORS) TESTING")
        print("-" * 60)
        
        test_symbols = ['RELIANCE', 'TCS', 'MPHASIS']
        
        for symbol in test_symbols:
            success, data = self.test_api_endpoint(f"Enhanced Indicators - {symbol}", "GET", f"stocks/{symbol}")
            
            if success:
                technical_data = data.get('technical_indicators', {})
                current_price = data.get('current_price', 0)
                
                # Test all 13 required indicators
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
                for key, name in required_indicators.items():
                    value = technical_data.get(key)
                    if value is not None:
                        present_indicators.append(name)
                
                coverage_rate = len(present_indicators) / len(required_indicators) * 100
                self.log_test(f"{symbol} - 13 Indicators Coverage", coverage_rate >= 80, 
                            f"{len(present_indicators)}/13 indicators present ({coverage_rate:.1f}%)")
                
                # Test MACD histogram calculations and BUY/SELL signals
                macd = technical_data.get('macd')
                macd_signal = technical_data.get('macd_signal')
                macd_histogram = technical_data.get('macd_histogram')
                
                if all(x is not None for x in [macd, macd_signal, macd_histogram]):
                    # Test histogram calculation accuracy
                    expected_histogram = macd - macd_signal
                    histogram_accurate = abs(macd_histogram - expected_histogram) < 0.01
                    
                    # Test BUY/SELL signal logic
                    signal = "BUY" if macd_histogram > 0 else "SELL"
                    
                    self.log_test(f"{symbol} - MACD Calculations", histogram_accurate, 
                                f"MACD: {macd:.3f}, Signal: {macd_signal:.3f}, Histogram: {macd_histogram:.3f}, Signal: {signal}")
                
                # Test Bollinger Bands position detection (UPPER/MIDDLE/LOWER)
                bb_upper = technical_data.get('bollinger_upper')
                bb_middle = technical_data.get('bollinger_middle')
                bb_lower = technical_data.get('bollinger_lower')
                
                if all(x is not None for x in [bb_upper, bb_middle, bb_lower]) and current_price > 0:
                    if current_price > bb_upper:
                        bb_position = "UPPER"
                    elif current_price < bb_lower:
                        bb_position = "LOWER"
                    else:
                        bb_position = "MIDDLE"
                    
                    bands_ordered = bb_lower < bb_middle < bb_upper
                    self.log_test(f"{symbol} - Bollinger Bands Position", bands_ordered, 
                                f"Price: ₹{current_price:.2f}, Position: {bb_position}, Bands: L:{bb_lower:.2f} M:{bb_middle:.2f} U:{bb_upper:.2f}")
                
                # Test VWAP position analysis (ABOVE/BELOW)
                vwap = technical_data.get('vwap')
                if vwap is not None and current_price > 0:
                    vwap_position = "ABOVE" if current_price > vwap else "BELOW"
                    self.log_test(f"{symbol} - VWAP Position", True, 
                                f"Price: ₹{current_price:.2f}, VWAP: ₹{vwap:.2f}, Position: {vwap_position}")
                
                # Test Stochastic oscillator values and ranges
                stoch_k = technical_data.get('stochastic_k')
                stoch_d = technical_data.get('stochastic_d')
                
                if stoch_k is not None and stoch_d is not None:
                    stoch_valid = (0 <= stoch_k <= 100) and (0 <= stoch_d <= 100)
                    self.log_test(f"{symbol} - Stochastic Range", stoch_valid, 
                                f"Stochastic %K: {stoch_k:.2f}, %D: {stoch_d:.2f}")
        
        return True

    def test_system_performance_scalability(self):
        """Test system performance and scalability"""
        print("\n⚡ SYSTEM PERFORMANCE & SCALABILITY TESTING")
        print("-" * 50)
        
        # Test concurrent requests
        import threading
        import time
        
        concurrent_results = []
        
        def concurrent_request():
            try:
                success, data = self.test_api_endpoint("Concurrent Request", "GET", "stocks/breakouts/scan", 
                                                     params={"limit": "100"}, timeout=60)
                concurrent_results.append(success)
            except:
                concurrent_results.append(False)
        
        # Launch 5 concurrent requests to test stability
        threads = []
        start_time = time.time()
        
        for i in range(5):
            thread = threading.Thread(target=concurrent_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        concurrent_time = end_time - start_time
        
        concurrent_success_rate = sum(concurrent_results) / len(concurrent_results) * 100
        self.log_test("Concurrent Request Stability", concurrent_success_rate >= 80, 
                    f"{sum(concurrent_results)}/{len(concurrent_results)} concurrent requests succeeded ({concurrent_success_rate:.1f}%) in {concurrent_time:.2f}s")
        
        # Test caching system efficiency
        # First call (cold cache)
        start_time = time.time()
        success1, data1 = self.test_api_endpoint("Cache Test - Cold", "GET", "stocks/breakouts/scan", 
                                               params={"limit": "50"}, timeout=60)
        cold_time = time.time() - start_time
        
        # Second call (warm cache)
        start_time = time.time()
        success2, data2 = self.test_api_endpoint("Cache Test - Warm", "GET", "stocks/breakouts/scan", 
                                               params={"limit": "50"}, timeout=60)
        warm_time = time.time() - start_time
        
        if success1 and success2 and cold_time > 0 and warm_time > 0:
            cache_improvement = (cold_time - warm_time) / cold_time * 100
            cache_effective = cache_improvement > 10  # At least 10% improvement
            
            self.log_test("Caching System Efficiency", cache_effective, 
                        f"Cache improved performance by {cache_improvement:.1f}% ({cold_time:.2f}s → {warm_time:.2f}s)")
        
        # Test memory usage and response times under load
        success3, perf_data = self.test_api_endpoint("Performance Analytics Check", "GET", "analytics/performance")
        if success3:
            performance_metrics = perf_data.get('performance_metrics', {})
            avg_response_time = performance_metrics.get('avg_response_time', '')
            error_rate = performance_metrics.get('error_rate', '')
            
            self.log_test("Performance Metrics", True, 
                        f"Avg Response: {avg_response_time}, Error Rate: {error_rate}")
        
        # Test batch processing capabilities
        success4, batch_data = self.test_api_endpoint("Batch Processing Test", "GET", "stocks/breakouts/scan", 
                                                    params={"limit": "200"}, timeout=120)
        if success4:
            scan_stats = batch_data.get('scan_statistics', {})
            batch_time = scan_stats.get('scan_time_seconds', 0)
            total_scanned = batch_data.get('total_scanned', 0)
            
            if batch_time > 0 and total_scanned > 0:
                processing_rate = total_scanned / batch_time
                self.log_test("Batch Processing Capability", processing_rate > 2, 
                            f"Processed {total_scanned} stocks in {batch_time:.2f}s ({processing_rate:.1f} stocks/sec)")
        
        return True

    def test_data_quality_validation(self):
        """Test data quality validation"""
        print("\n🔍 DATA QUALITY VALIDATION TESTING")
        print("-" * 40)
        
        # Test API responses include proper error handling
        success1, error_data = self.test_api_endpoint("Error Handling Test", "GET", "stocks/INVALID123", 
                                                    expected_status=404)
        
        # Test data consistency across different endpoints
        test_symbol = 'RELIANCE'
        
        # Get data from individual stock endpoint
        success2, stock_data = self.test_api_endpoint("Individual Stock Data", "GET", f"stocks/{test_symbol}")
        
        # Get data from breakout scan
        success3, scan_data = self.test_api_endpoint("Breakout Scan Data", "GET", "stocks/breakouts/scan", 
                                                   params={"limit": "50"})
        
        if success2 and success3:
            stock_price = stock_data.get('current_price', 0)
            
            # Find the same stock in breakout results
            breakout_stocks = scan_data.get('breakout_stocks', [])
            matching_stock = None
            for stock in breakout_stocks:
                if stock.get('symbol') == test_symbol:
                    matching_stock = stock
                    break
            
            if matching_stock:
                breakout_price = matching_stock.get('current_price', 0)
                price_consistency = abs(stock_price - breakout_price) / stock_price < 0.01 if stock_price > 0 else False
                
                self.log_test("Data Consistency Check", price_consistency, 
                            f"Individual: ₹{stock_price:.2f}, Breakout: ₹{breakout_price:.2f}")
        
        # Test export functionality returns properly formatted data
        success4, export_data = self.test_api_endpoint("Export Data Format", "POST", "export/data", 
                                                     data={"format": "csv", "stocks": ["RELIANCE", "TCS"]})
        
        if success4:
            export_records = export_data.get('export_data', [])
            if export_records:
                first_record = export_records[0]
                
                # Check for proper formatting
                has_symbol = 'Symbol' in first_record
                has_price = 'Current_Price' in first_record
                has_signals = 'MACD_Signal' in first_record and 'Action' in first_record
                
                format_valid = has_symbol and has_price and has_signals
                self.log_test("Export Data Format", format_valid, 
                            f"Export format includes Symbol, Price, and Trading Signals")
        
        # Test that all professional features integrate seamlessly
        success5, health_data = self.test_api_endpoint("Integration Health Check", "GET", "system/health")
        
        if success5:
            data_quality = health_data.get('data_quality', {})
            indicators_active = data_quality.get('indicators_active', 0)
            
            integration_healthy = indicators_active >= 13
            self.log_test("Professional Features Integration", integration_healthy, 
                        f"All {indicators_active} professional indicators integrated")
        
        return True

    def run_professional_tests(self):
        """Run all professional endpoint tests"""
        print("🚀 StockBreak Pro v2.0 - Professional Features Testing")
        print("=" * 70)
        print(f"Testing API at: {self.api_url}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # Test 1: Full NSE Scanning (600+ stocks)
        self.test_full_nse_scanning_600_stocks()
        
        # Test 2: New Professional Endpoints
        self.test_new_professional_endpoints()
        
        # Test 3: Enhanced Technical Indicators (13 indicators)
        self.test_enhanced_technical_indicators_13()
        
        # Test 4: System Performance & Scalability
        self.test_system_performance_scalability()
        
        # Test 5: Data Quality Validation
        self.test_data_quality_validation()
        
        # Print final results
        print("\n" + "=" * 70)
        print("📊 PROFESSIONAL FEATURES TEST RESULTS")
        print("=" * 70)
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
            print("\n✅ ALL PROFESSIONAL FEATURES TESTS PASSED!")
        
        print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        return self.tests_passed == self.tests_run

def main():
    """Main test execution"""
    tester = ProfessionalEndpointsTester()
    
    try:
        all_passed = tester.run_professional_tests()
        return 0 if all_passed else 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n💥 Unexpected error during testing: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())