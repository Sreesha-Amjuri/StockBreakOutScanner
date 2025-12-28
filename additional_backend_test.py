#!/usr/bin/env python3
"""
Additional backend API tests for comprehensive coverage
"""

import requests
import json
from datetime import datetime

class AdditionalBackendTester:
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

    def test_additional_apis(self):
        """Test additional critical APIs"""
        print("🔍 ADDITIONAL BACKEND API TESTING")
        print("-" * 40)
        
        # Test 1: Market Overview API
        success1, data1 = self.test_api_endpoint("Market Overview API", "GET", "stocks/market-overview")
        
        if success1:
            required_keys = ['nifty_50', 'market_status', 'market_sentiment']
            missing_keys = [key for key in required_keys if key not in data1]
            
            if not missing_keys:
                nifty_data = data1.get('nifty_50', {})
                market_status = data1.get('market_status', {})
                sentiment = data1.get('market_sentiment', 'Unknown')
                
                self.log_test("Market Overview Structure", True, 
                            f"NIFTY: {nifty_data.get('current', 'N/A')}, Status: {market_status.get('status', 'N/A')}, Sentiment: {sentiment}")
            else:
                self.log_test("Market Overview Structure", False, f"Missing keys: {missing_keys}")
        
        # Test 2: Stock Search API
        success2, data2 = self.test_api_endpoint("Stock Search API", "GET", "stocks/search", 
                                                params={"q": "TCS"})
        
        if success2:
            if 'results' in data2:
                results = data2['results']
                tcs_found = any(result.get('symbol') == 'TCS' for result in results)
                self.log_test("Stock Search Results", tcs_found, 
                            f"Found {len(results)} results, TCS present: {tcs_found}")
            else:
                self.log_test("Stock Search Results", False, "No 'results' field in response")
        
        # Test 3: Individual Stock Data API
        success3, data3 = self.test_api_endpoint("Individual Stock Data", "GET", "stocks/TCS")
        
        if success3:
            required_fields = ['symbol', 'name', 'current_price', 'change_percent']
            missing_fields = [field for field in required_fields if field not in data3]
            
            if not missing_fields:
                price = data3.get('current_price', 0)
                change = data3.get('change_percent', 0)
                self.log_test("Stock Data Structure", True, 
                            f"TCS: ₹{price:.2f} ({change:+.2f}%)")
            else:
                self.log_test("Stock Data Structure", False, f"Missing fields: {missing_fields}")
        
        # Test 4: Breakout Scanning API
        success4, data4 = self.test_api_endpoint("Breakout Scanning API", "GET", "stocks/breakouts/scan", 
                                                params={"limit": "10"}, timeout=60)
        
        if success4:
            breakouts_found = data4.get('breakouts_found', 0)
            total_scanned = data4.get('total_scanned', 0)
            self.log_test("Breakout Scanning", True, 
                        f"Scanned {total_scanned} stocks, found {breakouts_found} breakouts")
        
        # Test 5: NSE Symbols API
        success5, data5 = self.test_api_endpoint("NSE Symbols API", "GET", "stocks/symbols")
        
        if success5:
            if 'symbols' in data5 and 'count' in data5:
                symbol_count = data5.get('count', 0)
                symbols = data5.get('symbols', [])
                expected_symbols = ['RELIANCE', 'TCS', 'INFOSYS']
                found_symbols = [s for s in expected_symbols if s in symbols]
                
                self.log_test("NSE Symbols", len(found_symbols) == len(expected_symbols), 
                            f"Total symbols: {symbol_count}, Expected symbols found: {len(found_symbols)}/{len(expected_symbols)}")
            else:
                self.log_test("NSE Symbols", False, "Missing 'symbols' or 'count' field")
        
        return all([success1, success2, success3, success4, success5])

    def run_tests(self):
        """Run all additional tests"""
        print("🚀 ADDITIONAL BACKEND API TESTING")
        print("=" * 50)
        print(f"Testing API at: {self.api_url}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        print()

        self.test_additional_apis()
        
        # Print final results
        print("\n" + "=" * 50)
        print("📊 ADDITIONAL TEST RESULTS")
        print("=" * 50)
        print(f"Total Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL ADDITIONAL TESTS PASSED!")
        else:
            print("⚠️  Some additional tests failed.")
        
        print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        return self.tests_passed == self.tests_run

if __name__ == "__main__":
    tester = AdditionalBackendTester()
    tester.run_tests()