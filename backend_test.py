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
        """Test individual stock data endpoints with trading recommendations"""
        # Test specific stocks mentioned in the review request with expected values
        test_symbols_with_expected = {
            'RELIANCE': {'expected_price': 1384.90, 'expected_change': -1.96},
            'TCS': {'expected_price': 3157.20, 'expected_change': 0.53},
            'MPHASIS': {'expected_price': 2873.20, 'expected_change': -1.53},
            'HDFCLIFE': {'expected_price': 776.60, 'expected_change': -1.32},
            'HINDUNILVR': {'expected_price': 2692.60, 'expected_change': 2.32}
        }
        
        successful_tests = 0
        
        for symbol, expected in test_symbols_with_expected.items():
            success, data = self.test_api_endpoint(f"Stock Data - {symbol}", "GET", f"stocks/{symbol}")
            
            if success:
                successful_tests += 1
                # Validate response structure
                required_keys = ['symbol', 'name', 'current_price', 'change_percent', 'technical_indicators', 'fundamental_data', 'risk_assessment']
                missing_keys = [key for key in required_keys if key not in data]
                
                if missing_keys:
                    self.log_test(f"{symbol} Data Structure", False, f"Missing keys: {missing_keys}")
                else:
                    current_price = data['current_price']
                    change_percent = data['change_percent']
                    
                    # Test price accuracy against expected values (allow 5% variance for market movements)
                    price_tolerance = 0.05  # 5% tolerance
                    change_tolerance = 2.0   # 2% absolute tolerance for change
                    
                    price_diff = abs(current_price - expected['expected_price']) / expected['expected_price']
                    change_diff = abs(change_percent - expected['expected_change'])
                    
                    price_accurate = price_diff <= price_tolerance
                    change_reasonable = change_diff <= change_tolerance
                    
                    self.log_test(f"{symbol} Price Accuracy", price_accurate, 
                                f"Current: ₹{current_price:.2f}, Expected: ₹{expected['expected_price']:.2f}, Diff: {price_diff*100:.2f}%")
                    
                    self.log_test(f"{symbol} Change Accuracy", change_reasonable, 
                                f"Current: {change_percent:.2f}%, Expected: {expected['expected_change']:.2f}%, Diff: {change_diff:.2f}%")
                    
                    self.log_test(f"{symbol} Data Structure", True, 
                                f"Price: ₹{current_price:.2f} ({change_percent:+.2f}%), Sector: {data.get('sector', 'N/A')}")
                    
                    # Test data validation info
                    data_validation = data.get('data_validation', {})
                    if data_validation:
                        self.test_data_validation_info(symbol, data_validation)
                    
                    # Test trading recommendation if present
                    trading_rec = data.get('trading_recommendation')
                    if trading_rec:
                        self.test_individual_trading_recommendation(symbol, trading_rec)
        
        return successful_tests > 0

    def test_individual_trading_recommendation(self, symbol, trading_rec):
        """Test individual stock trading recommendation"""
        required_fields = ['entry_price', 'stop_loss', 'target_price', 'risk_reward_ratio', 
                         'position_size_percent', 'action', 'entry_rationale', 'stop_loss_rationale']
        
        missing_fields = [field for field in required_fields if field not in trading_rec]
        
        if missing_fields:
            self.log_test(f"Trading Recommendation - {symbol}", False, f"Missing fields: {missing_fields}")
        else:
            entry_price = trading_rec['entry_price']
            stop_loss = trading_rec['stop_loss']
            target_price = trading_rec['target_price']
            action = trading_rec['action']
            
            self.log_test(f"Trading Recommendation - {symbol}", True, 
                        f"Entry ₹{entry_price}, Stop ₹{stop_loss}, Target ₹{target_price}, Action {action}")

    def test_data_validation_info(self, symbol, data_validation):
        """Test data validation information structure and content"""
        required_fields = ['source', 'timestamp']
        missing_fields = [field for field in required_fields if field not in data_validation]
        
        if missing_fields:
            self.log_test(f"Data Validation Info - {symbol}", False, f"Missing fields: {missing_fields}")
        else:
            source = data_validation.get('source', '')
            timestamp = data_validation.get('timestamp', '')
            data_age_warning = data_validation.get('data_age_warning')
            
            # Check if data source is valid
            valid_sources = ['Yahoo Finance', 'Yahoo Finance Real-time', 'Yahoo Finance Historical']
            source_valid = any(valid_source in source for valid_source in valid_sources)
            
            # Check timestamp format
            timestamp_valid = len(timestamp) > 0
            
            details = f"Source: {source}, Timestamp: {timestamp}"
            if data_age_warning:
                details += f", Warning: {data_age_warning}"
            
            self.log_test(f"Data Validation Info - {symbol}", source_valid and timestamp_valid, details)

    def test_stock_data_validation_endpoint(self):
        """Test the new validation endpoint for cross-source data validation"""
        test_symbols = ['RELIANCE', 'TCS', 'MPHASIS', 'HDFCLIFE', 'HINDUNILVR']
        successful_validations = 0
        
        for symbol in test_symbols:
            success, data = self.test_api_endpoint(f"Data Validation - {symbol}", "GET", f"stocks/{symbol}/validate", timeout=45)
            
            if success:
                successful_validations += 1
                
                # Test validation result structure
                required_keys = ['symbol', 'validation_timestamp', 'data_quality_score', 'quality_level']
                missing_keys = [key for key in required_keys if key not in data]
                
                if missing_keys:
                    self.log_test(f"Validation Structure - {symbol}", False, f"Missing keys: {missing_keys}")
                else:
                    quality_score = data.get('data_quality_score', 0)
                    quality_level = data.get('quality_level', 'Unknown')
                    warnings = data.get('warnings', [])
                    
                    # Test data quality score range (should be 0-100)
                    score_valid = 0 <= quality_score <= 100
                    
                    # Test quality level values
                    valid_levels = ['Excellent', 'Good', 'Fair', 'Poor', 'Failed']
                    level_valid = quality_level in valid_levels
                    
                    self.log_test(f"Validation Quality - {symbol}", score_valid and level_valid, 
                                f"Score: {quality_score}/100, Level: {quality_level}, Warnings: {len(warnings)}")
                    
                    # Test cross-source validation if available
                    yahoo_data = data.get('yahoo_finance')
                    nse_data = data.get('nse_crosscheck')
                    
                    if yahoo_data and nse_data:
                        self.test_cross_source_validation(symbol, yahoo_data, nse_data)
                    
                    # Test data freshness warnings
                    if warnings:
                        self.test_data_freshness_warnings(symbol, warnings)
        
        return successful_validations > 0

    def test_cross_source_validation(self, symbol, yahoo_data, nse_data):
        """Test cross-source price validation"""
        yahoo_price = yahoo_data.get('current_price')
        nse_price = nse_data.get('current_price')
        
        if yahoo_price and nse_price:
            price_diff = abs(yahoo_price - nse_price)
            price_diff_percent = (price_diff / yahoo_price) * 100
            
            # Acceptable variance is 5% as mentioned in requirements
            acceptable_variance = price_diff_percent <= 5.0
            
            self.log_test(f"Cross-Source Price Validation - {symbol}", acceptable_variance, 
                        f"Yahoo: ₹{yahoo_price:.2f}, NSE: ₹{nse_price:.2f}, Diff: {price_diff_percent:.2f}%")
        else:
            self.log_test(f"Cross-Source Price Validation - {symbol}", False, 
                        "Missing price data from one or both sources")

    def test_data_freshness_warnings(self, symbol, warnings):
        """Test data freshness warning system"""
        freshness_warnings = [w for w in warnings if 'hours old' in w or 'stale' in w.lower()]
        
        if freshness_warnings:
            self.log_test(f"Data Freshness Warnings - {symbol}", True, 
                        f"Found {len(freshness_warnings)} freshness warnings: {freshness_warnings[0]}")
        else:
            self.log_test(f"Data Freshness - {symbol}", True, "Data appears fresh (no age warnings)")

    def test_real_time_data_accuracy(self):
        """Test real-time data accuracy against expected market conditions"""
        print("\n🔍 REAL-TIME DATA ACCURACY TESTS")
        print("-" * 40)
        
        # Test during different market conditions
        success, market_data = self.test_api_endpoint("Market Status Check", "GET", "stocks/market-overview")
        
        if success:
            market_status = market_data.get('market_status', {})
            is_trading_hours = market_status.get('is_trading_hours', False)
            
            self.log_test("Market Hours Detection", True, 
                        f"Trading Hours: {is_trading_hours}, Status: {market_status.get('status', 'Unknown')}")
            
            # Test data accuracy expectations based on market hours
            if is_trading_hours:
                self.log_test("Real-time Data Expectation", True, 
                            "Market is open - expecting real-time or near real-time data")
            else:
                self.log_test("Delayed Data Expectation", True, 
                            "Market is closed - delayed data is acceptable")
        
        # Test specific stocks for data quality during current market conditions
        test_symbols = ['RELIANCE', 'TCS', 'MPHASIS']
        for symbol in test_symbols:
            success, validation_data = self.test_api_endpoint(f"Real-time Validation - {symbol}", "GET", f"stocks/{symbol}/validate")
            
            if success:
                quality_score = validation_data.get('data_quality_score', 0)
                warnings = validation_data.get('warnings', [])
                
                # For trading decisions, we need quality score >= 60 as mentioned in requirements
                trading_suitable = quality_score >= 60
                
                self.log_test(f"Trading Suitability - {symbol}", trading_suitable, 
                            f"Quality Score: {quality_score}/100 ({'Suitable' if trading_suitable else 'Not suitable'} for trading)")
                
                # Check for stale data warnings (should warn if data > 1 hour old)
                stale_warnings = [w for w in warnings if 'hour' in w and ('old' in w or 'stale' in w)]
                if stale_warnings:
                    self.log_test(f"Stale Data Warning - {symbol}", True, f"Properly warned about stale data: {stale_warnings[0]}")

    def test_trading_impact_analysis(self):
        """Test if data accuracy would affect trading recommendations"""
        print("\n📊 TRADING IMPACT ANALYSIS")
        print("-" * 40)
        
        test_symbols = ['RELIANCE', 'TCS', 'MPHASIS', 'HDFCLIFE', 'HINDUNILVR']
        reliable_recommendations = 0
        total_recommendations = 0
        
        for symbol in test_symbols:
            # Get stock data with trading recommendation
            success, stock_data = self.test_api_endpoint(f"Trading Data - {symbol}", "GET", f"stocks/{symbol}")
            
            if success:
                trading_rec = stock_data.get('trading_recommendation')
                data_validation = stock_data.get('data_validation', {})
                
                if trading_rec:
                    total_recommendations += 1
                    
                    # Get validation data
                    val_success, validation_data = self.test_api_endpoint(f"Trading Validation - {symbol}", "GET", f"stocks/{symbol}/validate")
                    
                    if val_success:
                        quality_score = validation_data.get('data_quality_score', 0)
                        quality_level = validation_data.get('quality_level', 'Unknown')
                        warnings = validation_data.get('warnings', [])
                        
                        # Check if recommendation is based on reliable data
                        data_reliable = quality_score >= 70 and quality_level in ['Excellent', 'Good']
                        
                        if data_reliable:
                            reliable_recommendations += 1
                        
                        # Test if entry/stop/target prices are calculated from accurate base data
                        entry_price = trading_rec.get('entry_price', 0)
                        current_price = stock_data.get('current_price', 0)
                        
                        # Entry price should be reasonably close to current price (within 5%)
                        price_alignment = abs(entry_price - current_price) / current_price <= 0.05 if current_price > 0 else False
                        
                        self.log_test(f"Trading Price Alignment - {symbol}", price_alignment, 
                                    f"Entry: ₹{entry_price:.2f}, Current: ₹{current_price:.2f}, Quality: {quality_level}")
                        
                        # Test if poor data quality affects system confidence
                        action = trading_rec.get('action', 'UNKNOWN')
                        if quality_score < 60:
                            conservative_action = action in ['WAIT', 'AVOID']
                            self.log_test(f"Low Quality Response - {symbol}", conservative_action, 
                                        f"Low quality data (Score: {quality_score}) should result in conservative action, got: {action}")
        
        # Overall trading reliability assessment
        reliability_rate = (reliable_recommendations / total_recommendations * 100) if total_recommendations > 0 else 0
        
        self.log_test("Overall Trading Reliability", reliability_rate >= 60, 
                    f"{reliable_recommendations}/{total_recommendations} recommendations based on reliable data ({reliability_rate:.1f}%)")

    def test_technical_indicator_validation(self):
        """Test technical indicator calculations using accurate price data"""
        print("\n📈 TECHNICAL INDICATOR VALIDATION")
        print("-" * 40)
        
        test_symbols = ['RELIANCE', 'TCS']
        
        for symbol in test_symbols:
            success, data = self.test_api_endpoint(f"Technical Indicators - {symbol}", "GET", f"stocks/{symbol}")
            
            if success:
                technical_data = data.get('technical_indicators', {})
                current_price = data.get('current_price', 0)
                
                # Test RSI calculation validity (should be 0-100)
                rsi = technical_data.get('rsi')
                if rsi is not None:
                    rsi_valid = 0 <= rsi <= 100
                    self.log_test(f"RSI Validity - {symbol}", rsi_valid, f"RSI: {rsi:.2f}")
                
                # Test moving averages (should be reasonable compared to current price)
                sma_20 = technical_data.get('sma_20')
                sma_50 = technical_data.get('sma_50')
                sma_200 = technical_data.get('sma_200')
                
                if sma_20 and current_price:
                    # SMA should be within reasonable range of current price (±50%)
                    sma_reasonable = 0.5 <= (sma_20 / current_price) <= 1.5
                    self.log_test(f"SMA-20 Reasonableness - {symbol}", sma_reasonable, 
                                f"SMA-20: ₹{sma_20:.2f}, Current: ₹{current_price:.2f}")
                
                # Test volume data accuracy
                volume = data.get('volume', 0)
                volume_ratio = technical_data.get('volume_ratio')
                
                if volume > 0:
                    self.log_test(f"Volume Data - {symbol}", True, f"Volume: {volume:,}, Ratio: {volume_ratio:.2f}" if volume_ratio else f"Volume: {volume:,}")
                
                # Test breakout detection reliability
                breakout_data = data.get('breakout_data')
                if breakout_data:
                    confidence = breakout_data.get('confidence', 0)
                    breakout_type = breakout_data.get('type', 'unknown')
                    
                    # High confidence breakouts should have supporting volume
                    if confidence > 0.8 and volume_ratio:
                        volume_support = volume_ratio > 1.2  # Above average volume
                        self.log_test(f"Breakout Volume Support - {symbol}", volume_support, 
                                    f"High confidence ({confidence:.2f}) breakout with volume ratio: {volume_ratio:.2f}")

    def test_comprehensive_data_validation(self):
        """Run comprehensive data validation tests as requested"""
        print("\n🔍 COMPREHENSIVE DATA VALIDATION TESTING")
        print("=" * 50)
        
        # Test 1: Stock Price Accuracy Testing
        self.test_real_time_data_accuracy()
        
        # Test 2: Cross-Source Validation
        self.test_stock_data_validation_endpoint()
        
        # Test 3: Technical Indicator Validation
        self.test_technical_indicator_validation()
        
        # Test 4: Trading Impact Analysis
        self.test_trading_impact_analysis()
        
        return True

    def test_individual_trading_recommendation(self, symbol, trading_rec):
        """Test individual stock trading recommendation"""
        required_fields = ['entry_price', 'stop_loss', 'target_price', 'risk_reward_ratio', 
                         'position_size_percent', 'action', 'entry_rationale', 'stop_loss_rationale']
        
        missing_fields = [field for field in required_fields if field not in trading_rec]
        
        if missing_fields:
            self.log_test(f"Trading Recommendation - {symbol}", False, f"Missing fields: {missing_fields}")
        else:
            entry_price = trading_rec['entry_price']
            stop_loss = trading_rec['stop_loss']
            target_price = trading_rec['target_price']
            action = trading_rec['action']
            
            # Check if this matches expected values from review request
            expected_values = {
                'MPHASIS': {'entry': 2873.20, 'stop': 2730.71, 'target': 3300.66, 'action': 'BUY'},
                'HDFCLIFE': {'entry': 776.60, 'stop': 747.99, 'target': 862.42, 'action': 'BUY'},
                'HINDUNILVR': {'entry': 2692.60, 'stop': 2585.47, 'target': 3013.99, 'action': 'BUY'}
            }
            
            if symbol in expected_values:
                expected = expected_values[symbol]
                tolerance = 0.05  # 5% tolerance for price variations
                
                entry_match = abs(entry_price - expected['entry']) / expected['entry'] <= tolerance
                stop_match = abs(stop_loss - expected['stop']) / expected['stop'] <= tolerance
                target_match = abs(target_price - expected['target']) / expected['target'] <= tolerance
                action_match = action == expected['action']
                
                if entry_match and stop_match and target_match and action_match:
                    self.log_test(f"Expected Trading Values - {symbol}", True, 
                                f"Values match expected: Entry ₹{entry_price}, Stop ₹{stop_loss}, Target ₹{target_price}, Action {action}")
                else:
                    self.log_test(f"Expected Trading Values - {symbol}", False, 
                                f"Values differ from expected. Got: Entry ₹{entry_price}, Stop ₹{stop_loss}, Target ₹{target_price}, Action {action}")
            else:
                self.log_test(f"Trading Recommendation - {symbol}", True, 
                            f"Entry ₹{entry_price}, Stop ₹{stop_loss}, Target ₹{target_price}, Action {action}")

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

    def test_new_action_and_breakout_type_filters(self):
        """Test the new Action and Breakout Type filters as requested in review"""
        print("\n🎯 NEW ACTION & BREAKOUT TYPE FILTER TESTING")
        print("-" * 50)
        
        # Test 1: Action Filter Tests
        action_tests = [
            {"action": "BUY", "name": "BUY Action Filter"},
            {"action": "SELL", "name": "SELL Action Filter"}, 
            {"action": "HOLD", "name": "HOLD Action Filter"}
        ]
        
        action_results = {}
        
        for test in action_tests:
            action = test["action"]
            name = test["name"]
            
            success, data = self.test_api_endpoint(name, "GET", "stocks/breakouts/scan", 
                                                 params={"action": action, "limit": "50"}, timeout=60)
            
            if success:
                breakout_stocks = data.get('breakout_stocks', [])
                filters_applied = data.get('filters_applied', {})
                
                # Verify filter was applied correctly
                applied_action = filters_applied.get('action')
                filter_applied_correctly = applied_action == action
                
                self.log_test(f"Action Filter Applied - {action}", filter_applied_correctly, 
                            f"Requested: {action}, Applied: {applied_action}")
                
                # Verify all returned stocks have the correct action
                correct_action_count = 0
                total_with_recommendations = 0
                
                for stock in breakout_stocks:
                    trading_rec = stock.get('trading_recommendation', {})
                    if trading_rec:
                        total_with_recommendations += 1
                        stock_action = trading_rec.get('action', 'UNKNOWN')
                        if stock_action == action:
                            correct_action_count += 1
                
                if total_with_recommendations > 0:
                    action_accuracy = (correct_action_count / total_with_recommendations) * 100
                    self.log_test(f"Action Filter Accuracy - {action}", action_accuracy >= 95, 
                                f"{correct_action_count}/{total_with_recommendations} stocks have correct action ({action_accuracy:.1f}%)")
                    
                    action_results[action] = {
                        'total_results': len(breakout_stocks),
                        'with_recommendations': total_with_recommendations,
                        'correct_action': correct_action_count
                    }
                else:
                    self.log_test(f"Action Filter Results - {action}", True, 
                                f"Found {len(breakout_stocks)} results, no trading recommendations to verify")
                    action_results[action] = {'total_results': len(breakout_stocks)}
        
        # Test 2: Breakout Type Filter Tests
        breakout_type_tests = [
            {"breakout_type": "200_dma", "name": "200 DMA Breakout Filter"},
            {"breakout_type": "resistance", "name": "Resistance Breakout Filter"},
            {"breakout_type": "momentum", "name": "Momentum Breakout Filter"}
        ]
        
        breakout_type_results = {}
        
        for test in breakout_type_tests:
            breakout_type = test["breakout_type"]
            name = test["name"]
            
            success, data = self.test_api_endpoint(name, "GET", "stocks/breakouts/scan", 
                                                 params={"breakout_type": breakout_type, "limit": "50"}, timeout=60)
            
            if success:
                breakout_stocks = data.get('breakout_stocks', [])
                filters_applied = data.get('filters_applied', {})
                
                # Verify filter was applied correctly
                applied_breakout_type = filters_applied.get('breakout_type')
                filter_applied_correctly = applied_breakout_type == breakout_type
                
                self.log_test(f"Breakout Type Filter Applied - {breakout_type}", filter_applied_correctly, 
                            f"Requested: {breakout_type}, Applied: {applied_breakout_type}")
                
                # Verify all returned stocks have the correct breakout type
                correct_type_count = 0
                
                for stock in breakout_stocks:
                    stock_breakout_type = stock.get('breakout_type', 'unknown')
                    if stock_breakout_type == breakout_type:
                        correct_type_count += 1
                
                if len(breakout_stocks) > 0:
                    type_accuracy = (correct_type_count / len(breakout_stocks)) * 100
                    self.log_test(f"Breakout Type Filter Accuracy - {breakout_type}", type_accuracy >= 95, 
                                f"{correct_type_count}/{len(breakout_stocks)} stocks have correct type ({type_accuracy:.1f}%)")
                    
                    breakout_type_results[breakout_type] = {
                        'total_results': len(breakout_stocks),
                        'correct_type': correct_type_count
                    }
                else:
                    self.log_test(f"Breakout Type Filter Results - {breakout_type}", True, 
                                f"No results found for {breakout_type} breakout type")
                    breakout_type_results[breakout_type] = {'total_results': 0}
        
        # Test 3: Combined Filter Tests
        combined_tests = [
            {"action": "BUY", "breakout_type": "200_dma", "name": "BUY + 200 DMA Combined"},
            {"action": "BUY", "breakout_type": "resistance", "name": "BUY + Resistance Combined"},
            {"action": "HOLD", "breakout_type": "momentum", "name": "HOLD + Momentum Combined"}
        ]
        
        for test in combined_tests:
            action = test["action"]
            breakout_type = test["breakout_type"]
            name = test["name"]
            
            success, data = self.test_api_endpoint(name, "GET", "stocks/breakouts/scan", 
                                                 params={"action": action, "breakout_type": breakout_type, "limit": "30"}, timeout=60)
            
            if success:
                breakout_stocks = data.get('breakout_stocks', [])
                filters_applied = data.get('filters_applied', {})
                
                # Verify both filters were applied
                applied_action = filters_applied.get('action')
                applied_breakout_type = filters_applied.get('breakout_type')
                
                both_filters_applied = (applied_action == action and applied_breakout_type == breakout_type)
                
                self.log_test(f"Combined Filters Applied - {name}", both_filters_applied, 
                            f"Action: {applied_action} (req: {action}), Type: {applied_breakout_type} (req: {breakout_type})")
                
                # Verify results match both criteria
                matching_stocks = 0
                for stock in breakout_stocks:
                    trading_rec = stock.get('trading_recommendation', {})
                    stock_action = trading_rec.get('action', 'UNKNOWN') if trading_rec else 'UNKNOWN'
                    stock_breakout_type = stock.get('breakout_type', 'unknown')
                    
                    if stock_action == action and stock_breakout_type == breakout_type:
                        matching_stocks += 1
                
                if len(breakout_stocks) > 0:
                    combined_accuracy = (matching_stocks / len(breakout_stocks)) * 100
                    self.log_test(f"Combined Filter Accuracy - {name}", combined_accuracy >= 95, 
                                f"{matching_stocks}/{len(breakout_stocks)} stocks match both criteria ({combined_accuracy:.1f}%)")
                else:
                    self.log_test(f"Combined Filter Results - {name}", True, 
                                f"No results found for combined filters")
        
        # Test 4: Verify filters_applied section includes new filters
        success, data = self.test_api_endpoint("Filters Applied Section Test", "GET", "stocks/breakouts/scan", 
                                             params={"action": "BUY", "breakout_type": "200_dma"}, timeout=60)
        
        if success:
            filters_applied = data.get('filters_applied', {})
            required_filter_keys = ['action', 'breakout_type', 'sector', 'min_confidence', 'risk_level', 'limit']
            
            missing_keys = [key for key in required_filter_keys if key not in filters_applied]
            
            if not missing_keys:
                self.log_test("Filters Applied Section Complete", True, 
                            f"All required filter keys present: {list(filters_applied.keys())}")
            else:
                self.log_test("Filters Applied Section Complete", False, 
                            f"Missing filter keys: {missing_keys}")
        
        # Summary of filter testing
        print(f"\n📊 FILTER TESTING SUMMARY")
        print(f"Action Filter Results: {action_results}")
        print(f"Breakout Type Filter Results: {breakout_type_results}")
        
        return True

    def test_full_nse_coverage_scanning(self):
        """Test Full NSE Coverage - scan ALL NSE stocks (600+) as requested"""
        print("\n🔍 FULL NSE COVERAGE TESTING")
        print("-" * 40)
        
        # Test 1: Scan with limit=600 to get ALL NSE stocks
        success1, data1 = self.test_api_endpoint("Full NSE Scan - 600 stocks", "GET", "stocks/breakouts/scan", 
                                                params={"limit": "600"}, timeout=120)
        
        if success1:
            total_scanned = data1.get('total_scanned', 0)
            breakouts_found = data1.get('breakouts_found', 0)
            scan_stats = data1.get('scan_statistics', {})
            
            # Verify we're scanning 594+ stocks (as mentioned in requirements)
            full_coverage = total_scanned >= 594
            self.log_test("Full NSE Coverage", full_coverage, 
                        f"Scanned {total_scanned} stocks (expected 594+)")
            
            # Test scan statistics
            if scan_stats:
                sectors_scanned = scan_stats.get('sectors_scanned', 0)
                self.log_test("Sector Coverage", sectors_scanned >= 35, 
                            f"Scanned {sectors_scanned} sectors")
        
        # Test 2: Test with different sector filters to ensure full coverage works
        test_sectors = ['IT', 'Banking', 'Pharma', 'Auto', 'Energy']
        sector_results = {}
        
        for sector in test_sectors:
            success, data = self.test_api_endpoint(f"Full Coverage - {sector} Sector", "GET", "stocks/breakouts/scan", 
                                                 params={"limit": "600", "sector": sector}, timeout=90)
            if success:
                sector_results[sector] = data.get('breakouts_found', 0)
                total_in_sector = data.get('total_scanned', 0)
                self.log_test(f"{sector} Sector Full Scan", True, 
                            f"Found {sector_results[sector]} breakouts from {total_in_sector} {sector} stocks")
        
        # Test 3: Performance with large dataset
        success3, data3 = self.test_api_endpoint("Performance - Large Dataset", "GET", "stocks/breakouts/scan", 
                                                params={"limit": "500"}, timeout=100)
        
        if success3:
            scan_time = data3.get('scan_statistics', {}).get('scan_time_seconds', 0)
            if scan_time > 0:
                self.log_test("Large Dataset Performance", scan_time < 120, 
                            f"Scan completed in {scan_time:.2f} seconds (should be < 120s)")
        
        return success1

    def test_enhanced_technical_indicators(self):
        """Test all enhanced technical indicators as requested"""
        print("\n📈 ENHANCED TECHNICAL INDICATORS TESTING")
        print("-" * 45)
        
        # Test symbols with various market conditions
        test_symbols = ['RELIANCE', 'TCS', 'MPHASIS', 'HDFCLIFE', 'HINDUNILVR']
        
        for symbol in test_symbols:
            success, data = self.test_api_endpoint(f"Enhanced Indicators - {symbol}", "GET", f"stocks/{symbol}")
            
            if success:
                technical_data = data.get('technical_indicators', {})
                current_price = data.get('current_price', 0)
                
                # Test all required indicators from the review request
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
                
                missing_indicators = []
                present_indicators = []
                
                for key, name in required_indicators.items():
                    value = technical_data.get(key)
                    if value is not None:
                        present_indicators.append(name)
                        
                        # Validate indicator values are reasonable
                        if key == 'rsi' and not (0 <= value <= 100):
                            self.log_test(f"{symbol} RSI Range", False, f"RSI {value} outside 0-100 range")
                        elif key in ['bollinger_upper', 'bollinger_middle', 'bollinger_lower', 'support_level', 'resistance_level', 'vwap'] and current_price > 0:
                            # Price-based indicators should be within reasonable range of current price
                            ratio = value / current_price
                            if not (0.5 <= ratio <= 2.0):
                                self.log_test(f"{symbol} {name} Range", False, f"{name} {value} seems unreasonable vs price {current_price}")
                        elif key in ['stochastic_k', 'stochastic_d'] and not (0 <= value <= 100):
                            self.log_test(f"{symbol} {name} Range", False, f"{name} {value} outside 0-100 range")
                    else:
                        missing_indicators.append(name)
                
                # Log results
                coverage_rate = len(present_indicators) / len(required_indicators) * 100
                self.log_test(f"{symbol} Indicator Coverage", coverage_rate >= 80, 
                            f"{len(present_indicators)}/{len(required_indicators)} indicators present ({coverage_rate:.1f}%)")
                
                if missing_indicators:
                    self.log_test(f"{symbol} Missing Indicators", False, f"Missing: {', '.join(missing_indicators)}")
                
                # Test MACD components consistency
                macd = technical_data.get('macd')
                macd_signal = technical_data.get('macd_signal')
                macd_histogram = technical_data.get('macd_histogram')
                
                if all(x is not None for x in [macd, macd_signal, macd_histogram]):
                    expected_histogram = macd - macd_signal
                    histogram_accurate = abs(macd_histogram - expected_histogram) < 0.01
                    self.log_test(f"{symbol} MACD Consistency", histogram_accurate, 
                                f"MACD: {macd:.3f}, Signal: {macd_signal:.3f}, Histogram: {macd_histogram:.3f}")
                
                # Test Bollinger Bands consistency
                bb_upper = technical_data.get('bollinger_upper')
                bb_middle = technical_data.get('bollinger_middle')
                bb_lower = technical_data.get('bollinger_lower')
                
                if all(x is not None for x in [bb_upper, bb_middle, bb_lower]):
                    bands_ordered = bb_lower < bb_middle < bb_upper
                    self.log_test(f"{symbol} Bollinger Bands Order", bands_ordered, 
                                f"Lower: {bb_lower:.2f}, Middle: {bb_middle:.2f}, Upper: {bb_upper:.2f}")
        
        return True

    def test_enhanced_watchlist_backend(self):
        """Test enhanced watchlist backend with full technical analysis"""
        print("\n⭐ ENHANCED WATCHLIST BACKEND TESTING")
        print("-" * 42)
        
        # Test adding multiple stocks to watchlist
        test_symbols = ['RELIANCE', 'TCS', 'MPHASIS']
        
        # Clear watchlist first
        self.test_api_endpoint("Clear Watchlist", "GET", "watchlist")
        
        # Add stocks to watchlist
        for symbol in test_symbols:
            success, data = self.test_api_endpoint(f"Add to Watchlist - {symbol}", "POST", "watchlist", 
                                                 params={"symbol": symbol})
            if success:
                self.log_test(f"Watchlist Add - {symbol}", True, f"Added {symbol} to watchlist")
        
        # Get watchlist with full technical analysis
        success, watchlist_data = self.test_api_endpoint("Enhanced Watchlist - Full Data", "GET", "watchlist")
        
        if success:
            watchlist_items = watchlist_data.get('watchlist', [])
            
            # Test that watchlist includes full technical analysis for each stock
            for item in watchlist_items:
                symbol = item.get('symbol')
                
                # Check if technical data is included
                if 'technical_indicators' in item:
                    technical_data = item['technical_indicators']
                    
                    # Verify key indicators are present
                    key_indicators = ['rsi', 'macd', 'bollinger_upper', 'bollinger_lower', 'vwap']
                    present_indicators = [ind for ind in key_indicators if technical_data.get(ind) is not None]
                    
                    coverage = len(present_indicators) / len(key_indicators) * 100
                    self.log_test(f"Watchlist Technical Data - {symbol}", coverage >= 60, 
                                f"Technical coverage: {coverage:.1f}% ({len(present_indicators)}/{len(key_indicators)} indicators)")
                else:
                    # Test individual stock endpoint to verify technical data is available
                    stock_success, stock_data = self.test_api_endpoint(f"Watchlist Stock Data - {symbol}", "GET", f"stocks/{symbol}")
                    if stock_success and 'technical_indicators' in stock_data:
                        self.log_test(f"Watchlist Technical Access - {symbol}", True, 
                                    "Technical data available via individual endpoint")
        
        # Test multiple stocks in watchlist simultaneously
        if len(test_symbols) > 1:
            self.log_test("Multiple Stocks Watchlist", len(watchlist_items) >= 2, 
                        f"Watchlist contains {len(watchlist_items)} stocks")
        
        # Clean up - remove test stocks
        for symbol in test_symbols:
            self.test_api_endpoint(f"Remove from Watchlist - {symbol}", "DELETE", f"watchlist/{symbol}")
        
        return success

    def test_performance_and_scaling(self):
        """Test backend performance with increased load (600 vs 100 stocks)"""
        print("\n⚡ PERFORMANCE & SCALING TESTING")
        print("-" * 35)
        
        # Test 1: Compare performance between different limits
        performance_tests = [
            {"limit": 100, "name": "Standard Load"},
            {"limit": 300, "name": "Medium Load"}, 
            {"limit": 600, "name": "Full Load"}
        ]
        
        performance_results = {}
        
        for test in performance_tests:
            limit = test["limit"]
            name = test["name"]
            
            success, data = self.test_api_endpoint(f"Performance - {name} ({limit} stocks)", "GET", "stocks/breakouts/scan", 
                                                 params={"limit": str(limit)}, timeout=150)
            
            if success:
                scan_stats = data.get('scan_statistics', {})
                scan_time = scan_stats.get('scan_time_seconds', 0)
                total_scanned = data.get('total_scanned', 0)
                
                if scan_time > 0:
                    stocks_per_second = total_scanned / scan_time
                    performance_results[limit] = {
                        'time': scan_time,
                        'stocks': total_scanned,
                        'rate': stocks_per_second
                    }
                    
                    # Performance benchmarks
                    acceptable_time = limit * 0.2  # 0.2 seconds per stock max
                    performance_good = scan_time <= acceptable_time
                    
                    self.log_test(f"Performance Benchmark - {name}", performance_good, 
                                f"{total_scanned} stocks in {scan_time:.2f}s ({stocks_per_second:.1f} stocks/sec)")
        
        # Test 2: Caching system effectiveness
        if 100 in performance_results:
            # First call (cold cache)
            success1, data1 = self.test_api_endpoint("Cache Test - Cold", "GET", "stocks/breakouts/scan", 
                                                   params={"limit": "100"}, timeout=60)
            
            # Second call (warm cache)
            success2, data2 = self.test_api_endpoint("Cache Test - Warm", "GET", "stocks/breakouts/scan", 
                                                   params={"limit": "100"}, timeout=60)
            
            if success1 and success2:
                time1 = data1.get('scan_statistics', {}).get('scan_time_seconds', 0)
                time2 = data2.get('scan_statistics', {}).get('scan_time_seconds', 0)
                
                if time1 > 0 and time2 > 0:
                    cache_improvement = (time1 - time2) / time1 * 100
                    cache_effective = cache_improvement > 10  # At least 10% improvement
                    
                    self.log_test("Caching System Effectiveness", cache_effective, 
                                f"Cache improved performance by {cache_improvement:.1f}% ({time1:.2f}s → {time2:.2f}s)")
        
        # Test 3: Concurrent requests stability
        import threading
        import time
        
        concurrent_results = []
        
        def concurrent_request():
            try:
                success, data = self.test_api_endpoint("Concurrent Request", "GET", "stocks/breakouts/scan", 
                                                     params={"limit": "50"}, timeout=30)
                concurrent_results.append(success)
            except:
                concurrent_results.append(False)
        
        # Launch 3 concurrent requests
        threads = []
        for i in range(3):
            thread = threading.Thread(target=concurrent_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        concurrent_success_rate = sum(concurrent_results) / len(concurrent_results) * 100
        self.log_test("Concurrent Request Stability", concurrent_success_rate >= 80, 
                    f"{sum(concurrent_results)}/{len(concurrent_results)} concurrent requests succeeded ({concurrent_success_rate:.1f}%)")
        
        return True

    def test_data_quality_comprehensive(self):
        """Test data quality - verify all technical indicators have reasonable values"""
        print("\n🔍 COMPREHENSIVE DATA QUALITY TESTING")
        print("-" * 42)
        
        # Test a diverse set of stocks across different sectors and market caps
        test_symbols = ['RELIANCE', 'TCS', 'MPHASIS', 'HDFCLIFE', 'HINDUNILVR', 'BAJFINANCE', 'ASIANPAINT']
        
        quality_scores = []
        
        for symbol in test_symbols:
            success, data = self.test_api_endpoint(f"Data Quality - {symbol}", "GET", f"stocks/{symbol}")
            
            if success:
                symbol_quality_score = 0
                max_possible_score = 0
                
                # Test 1: Basic data completeness
                basic_fields = ['current_price', 'change_percent', 'volume', 'symbol', 'name']
                basic_complete = all(data.get(field) is not None for field in basic_fields)
                if basic_complete:
                    symbol_quality_score += 20
                max_possible_score += 20
                
                # Test 2: Technical indicators quality
                technical_data = data.get('technical_indicators', {})
                if technical_data:
                    # RSI quality (should be 0-100)
                    rsi = technical_data.get('rsi')
                    if rsi is not None and 0 <= rsi <= 100:
                        symbol_quality_score += 10
                    max_possible_score += 10
                    
                    # Moving averages quality (should be reasonable vs current price)
                    current_price = data.get('current_price', 0)
                    sma_20 = technical_data.get('sma_20')
                    if sma_20 and current_price > 0:
                        ratio = sma_20 / current_price
                        if 0.7 <= ratio <= 1.3:  # Within 30% of current price
                            symbol_quality_score += 10
                    max_possible_score += 10
                    
                    # Bollinger Bands quality (proper ordering)
                    bb_upper = technical_data.get('bollinger_upper')
                    bb_middle = technical_data.get('bollinger_middle')
                    bb_lower = technical_data.get('bollinger_lower')
                    if all(x is not None for x in [bb_upper, bb_middle, bb_lower]):
                        if bb_lower < bb_middle < bb_upper:
                            symbol_quality_score += 10
                    max_possible_score += 10
                    
                    # VWAP quality (should be reasonable vs current price)
                    vwap = technical_data.get('vwap')
                    if vwap and current_price > 0:
                        vwap_ratio = vwap / current_price
                        if 0.8 <= vwap_ratio <= 1.2:  # Within 20% of current price
                            symbol_quality_score += 10
                    max_possible_score += 10
                    
                    # Stochastic quality (should be 0-100)
                    stoch_k = technical_data.get('stochastic_k')
                    stoch_d = technical_data.get('stochastic_d')
                    if stoch_k is not None and 0 <= stoch_k <= 100:
                        symbol_quality_score += 5
                    if stoch_d is not None and 0 <= stoch_d <= 100:
                        symbol_quality_score += 5
                    max_possible_score += 10
                
                # Test 3: No null/undefined values in critical fields
                critical_fields = ['current_price', 'change_percent', 'volume']
                no_nulls = all(data.get(field) is not None and str(data.get(field)) != 'null' for field in critical_fields)
                if no_nulls:
                    symbol_quality_score += 20
                max_possible_score += 20
                
                # Test 4: Trading recommendation quality (if present)
                trading_rec = data.get('trading_recommendation')
                if trading_rec:
                    entry_price = trading_rec.get('entry_price', 0)
                    stop_loss = trading_rec.get('stop_loss', 0)
                    target_price = trading_rec.get('target_price', 0)
                    
                    # Logical consistency: stop < entry < target
                    if stop_loss > 0 and entry_price > 0 and target_price > 0:
                        if stop_loss < entry_price < target_price:
                            symbol_quality_score += 10
                max_possible_score += 10
                
                # Calculate quality percentage
                quality_percentage = (symbol_quality_score / max_possible_score * 100) if max_possible_score > 0 else 0
                quality_scores.append(quality_percentage)
                
                # Quality assessment
                if quality_percentage >= 90:
                    quality_level = "Excellent"
                elif quality_percentage >= 75:
                    quality_level = "Good"
                elif quality_percentage >= 60:
                    quality_level = "Fair"
                else:
                    quality_level = "Poor"
                
                self.log_test(f"Data Quality Score - {symbol}", quality_percentage >= 75, 
                            f"{quality_percentage:.1f}% ({quality_level}) - {symbol_quality_score}/{max_possible_score} points")
        
        # Overall data quality assessment
        if quality_scores:
            avg_quality = sum(quality_scores) / len(quality_scores)
            self.log_test("Overall Data Quality", avg_quality >= 75, 
                        f"Average quality score: {avg_quality:.1f}% across {len(quality_scores)} stocks")
        
        return True

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
        """Test enhanced market overview endpoint with detailed market status"""
        success, data = self.test_api_endpoint("Market Overview", "GET", "stocks/market-overview")
        
        if success:
            required_keys = ['nifty_50', 'market_status', 'market_sentiment']
            missing_keys = [key for key in required_keys if key not in data]
            
            if missing_keys:
                self.log_test("Market Overview Structure", False, f"Missing keys: {missing_keys}")
            else:
                nifty_data = data.get('nifty_50', {})
                market_status = data.get('market_status', {})
                
                self.log_test("Market Overview Structure", True, 
                            f"NIFTY: {nifty_data.get('current', 'N/A')}, Sentiment: {data.get('market_sentiment', 'N/A')}")
                
                # Test enhanced market status structure
                self.test_enhanced_market_status(market_status)
        
        return success

    def test_enhanced_market_status(self, market_status):
        """Test enhanced market status structure"""
        required_status_fields = ['status', 'message', 'current_time', 'is_trading_hours']
        missing_fields = [field for field in required_status_fields if field not in market_status]
        
        if missing_fields:
            self.log_test("Market Status Structure", False, f"Missing fields: {missing_fields}")
        else:
            status = market_status.get('status')
            current_time = market_status.get('current_time')
            is_trading = market_status.get('is_trading_hours')
            message = market_status.get('message')
            
            # Validate status values
            valid_statuses = ['OPEN', 'CLOSED', 'PRE_OPEN']
            status_valid = status in valid_statuses
            
            # Validate IST time format
            ist_valid = 'IST' in current_time if current_time else False
            
            self.log_test("Market Status Values", status_valid and ist_valid, 
                        f"Status: {status}, Time: {current_time}, Trading: {is_trading}")
            
            # Test additional fields based on status
            if status == 'OPEN' and 'time_to_close' in market_status:
                self.log_test("Market Open Details", True, f"Time to close: {market_status['time_to_close']}s")
            elif status in ['CLOSED', 'PRE_OPEN'] and 'next_open' in market_status:
                self.log_test("Market Closed Details", True, f"Next open: {market_status['next_open']}")
            
            self.log_test("Market Status Message", len(message) > 0 if message else False, 
                        f"Message: {message}")

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
        
        print("\n🎯 NEW FILTER TESTS (Action & Breakout Type)")
        print("-" * 50)
        self.test_new_action_and_breakout_type_filters()
        
        print("\n📈 MARKET DATA TESTS")
        print("-" * 30)
        self.test_market_overview()
        
        print("\n⭐ WATCHLIST TESTS")
        print("-" * 30)
        self.test_watchlist_operations()
        
        print("\n🚨 ERROR HANDLING TESTS")
        print("-" * 30)
        self.test_error_handling()
        
        # NEW: Enhanced StockBreak Pro Testing (as per review request)
        print("\n🚀 ENHANCED STOCKBREAK PRO TESTING")
        print("-" * 50)
        self.test_full_nse_coverage_scanning()
        self.test_enhanced_technical_indicators()
        self.test_enhanced_watchlist_backend()
        self.test_performance_and_scaling()
        self.test_data_quality_comprehensive()
        
        # Original comprehensive data validation tests
        print("\n🔍 COMPREHENSIVE DATA VALIDATION TESTING")
        print("-" * 50)
        self.test_comprehensive_data_validation()
        
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