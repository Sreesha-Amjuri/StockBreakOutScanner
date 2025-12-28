#!/usr/bin/env python3
"""
Focused testing for StockBreak Pro new features
"""

import requests
import json
from datetime import datetime

class StockBreakProTester:
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

    def test_stockbreak_pro_features(self):
        """Test the new StockBreak Pro features"""
        print("🌟 STOCKBREAK PRO NEW FEATURES TESTING")
        print("-" * 45)
        
        # Test 1: Top Picks API
        print("Testing Top Picks API...")
        success1, data1 = self.test_api_endpoint("Top Picks API", "GET", "signals/top-picks")
        
        if success1:
            print(f"Top Picks Response: {json.dumps(data1, indent=2)[:500]}...")
            
            # Validate top picks structure
            if 'top_picks' in data1:
                top_picks = data1['top_picks']
                self.log_test("Top Picks Structure", len(top_picks) > 0, 
                            f"Found {len(top_picks)} top picks")
                
                # Validate each top pick has required fields
                if top_picks:
                    first_pick = top_picks[0]
                    required_fields = ['symbol', 'name', 'signal', 'confidence', 'reasoning', 'potential_upside']
                    missing_fields = [field for field in required_fields if field not in first_pick]
                    
                    if not missing_fields:
                        confidence = first_pick.get('confidence', 0)
                        if isinstance(confidence, (int, float)):
                            confidence_pct = f"{confidence:.1%}" if confidence <= 1 else f"{confidence:.1f}%"
                        else:
                            confidence_pct = str(confidence)
                        
                        self.log_test("Top Picks Fields", True, 
                                    f"Sample: {first_pick['symbol']} - {first_pick['signal']} ({confidence_pct} confidence)")
                    else:
                        self.log_test("Top Picks Fields", False, f"Missing fields: {missing_fields}")
            else:
                self.log_test("Top Picks Structure", False, "No 'top_picks' field in response")
        
        # Test 2: Watchlist Signals API
        print("Testing Watchlist Signals API...")
        success2, data2 = self.test_api_endpoint("Watchlist Signals API", "GET", "signals/watchlist")
        
        if success2:
            print(f"Watchlist Signals Response: {json.dumps(data2, indent=2)[:500]}...")
            
            # Validate watchlist signals structure
            if 'signals' in data2:
                signals = data2['signals']
                self.log_test("Watchlist Signals Structure", True, 
                            f"Found {len(signals)} watchlist signals")
                
                # Check for TCS signal as mentioned in review request
                tcs_signal = next((s for s in signals if s.get('symbol') == 'TCS'), None)
                if tcs_signal:
                    signal_type = tcs_signal.get('signal')
                    reasoning = tcs_signal.get('reasoning', '')
                    self.log_test("TCS Signal Present", True, 
                                f"TCS signal: {signal_type}, Reasoning: {reasoning[:50]}...")
                else:
                    self.log_test("TCS Signal Present", False, "TCS signal not found in watchlist")
            else:
                self.log_test("Watchlist Signals Structure", False, "No 'signals' field in response")
        
        # Test 3: Alerts API
        print("Testing Alerts API...")
        success3, data3 = self.test_api_endpoint("Alerts API", "GET", "alerts")
        
        if success3:
            print(f"Alerts Response: {json.dumps(data3, indent=2)[:500]}...")
            
            # Validate alerts structure
            if 'alerts' in data3:
                alerts = data3['alerts']
                unread_count = data3.get('unread_count', 0)
                self.log_test("Alerts Structure", True, 
                            f"Found {len(alerts)} alerts, {unread_count} unread")
                
                # Check for TCS breakout alert as mentioned in review request
                tcs_alert = next((a for a in alerts if 'TCS' in a.get('symbol', '') or 'TCS' in a.get('message', '')), None)
                if tcs_alert:
                    alert_type = tcs_alert.get('alert_type', 'unknown')
                    message = tcs_alert.get('message', '')
                    self.log_test("TCS Breakout Alert", True, 
                                f"TCS alert: {alert_type}, Message: {message[:50]}...")
                else:
                    self.log_test("TCS Breakout Alert", False, "TCS breakout alert not found")
            else:
                self.log_test("Alerts Structure", False, "No 'alerts' field in response")
        
        # Test 4: Signal Refresh API
        print("Testing Signal Refresh API...")
        success4, data4 = self.test_api_endpoint("Signal Refresh API", "POST", "signals/refresh")
        
        if success4:
            print(f"Signal Refresh Response: {json.dumps(data4, indent=2)[:500]}...")
            
            # Validate refresh response - check for actual response structure
            if 'success' in data4:
                signals_count = data4.get('signals_count', 0)
                alerts_count = data4.get('alerts_count', 0)
                self.log_test("Signal Refresh Success", True, 
                            f"Refreshed {signals_count} signals, {alerts_count} alerts")
            else:
                self.log_test("Signal Refresh Success", False, "Missing 'success' field in response")
        
        # Test 5: Mark Alerts as Read API
        print("Testing Mark Alerts as Read API...")
        success5, data5 = self.test_api_endpoint("Mark Alerts Read API", "POST", "alerts/read-all")
        
        if success5:
            print(f"Mark Alerts Read Response: {json.dumps(data5, indent=2)[:500]}...")
            
            # Validate mark read response - check for actual response structure
            if 'success' in data5:
                # Check for either 'modified_count' or 'updated_count'
                modified_count = data5.get('modified_count', data5.get('updated_count', 0))
                self.log_test("Mark Alerts Read Success", True, 
                            f"Marked {modified_count} alerts as read")
            else:
                self.log_test("Mark Alerts Read Success", False, "Missing 'success' field in response")
        
        # Test 6: Verify watchlist has expected stocks (RELIANCE, TCS, INFOSYS)
        print("Testing Watchlist Verification...")
        success6, watchlist_data = self.test_api_endpoint("Watchlist Verification", "GET", "watchlist")
        
        if success6:
            print(f"Watchlist Response: {json.dumps(watchlist_data, indent=2)[:500]}...")
            
            watchlist = watchlist_data.get('watchlist', [])
            expected_stocks = ['RELIANCE', 'TCS', 'INFOSYS']
            found_stocks = [item.get('symbol') for item in watchlist if item.get('symbol') in expected_stocks]
            
            self.log_test("Expected Watchlist Stocks", len(found_stocks) >= 2, 
                        f"Found {len(found_stocks)}/{len(expected_stocks)} expected stocks: {found_stocks}")
        
        return all([success1, success2, success3, success4, success5])

    def run_tests(self):
        """Run all tests"""
        print("🚀 STOCKBREAK PRO FEATURES TESTING")
        print("=" * 50)
        print(f"Testing API at: {self.api_url}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        print()

        self.test_stockbreak_pro_features()
        
        # Print final results
        print("\n" + "=" * 50)
        print("📊 FINAL TEST RESULTS")
        print("=" * 50)
        print(f"Total Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL TESTS PASSED!")
        else:
            print("⚠️  Some tests failed. Check details above.")
        
        print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        return self.tests_passed == self.tests_run

if __name__ == "__main__":
    tester = StockBreakProTester()
    tester.run_tests()