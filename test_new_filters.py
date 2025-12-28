#!/usr/bin/env python3
"""
Focused testing for new Action and Breakout Type filters
"""

import requests
import sys
import json
from datetime import datetime

class NewFilterTester:
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
                         timeout: int = 30) -> tuple:
        """Generic API endpoint tester"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=timeout)
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

    def test_action_filters(self):
        """Test Action filter functionality"""
        print("🎯 TESTING ACTION FILTERS")
        print("-" * 30)
        
        action_tests = [
            {"action": "BUY", "name": "Action Filter - BUY"},
            {"action": "SELL", "name": "Action Filter - SELL"}, 
            {"action": "HOLD", "name": "Action Filter - HOLD"}
        ]
        
        for test in action_tests:
            action = test["action"]
            name = test["name"]
            
            success, data = self.test_api_endpoint(name, "GET", "stocks/breakouts/scan", 
                                                 params={"action": action, "limit": "20"}, timeout=45)
            
            if success:
                breakout_stocks = data.get('breakout_stocks', [])
                filters_applied = data.get('filters_applied', {})
                
                # Verify filter was applied correctly
                applied_action = filters_applied.get('action')
                filter_applied_correctly = applied_action == action
                
                self.log_test(f"Action Filter Applied - {action}", filter_applied_correctly, 
                            f"Requested: {action}, Applied: {applied_action}")
                
                # Check if results match the filter
                if breakout_stocks:
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
                        accuracy = (correct_action_count / total_with_recommendations) * 100
                        self.log_test(f"Action Filter Accuracy - {action}", accuracy >= 90, 
                                    f"{correct_action_count}/{total_with_recommendations} stocks have correct action ({accuracy:.1f}%)")
                    else:
                        self.log_test(f"Action Filter Results - {action}", True, 
                                    f"Found {len(breakout_stocks)} results, no trading recommendations to verify")
                else:
                    self.log_test(f"Action Filter Results - {action}", True, 
                                f"No breakout stocks found for action: {action}")

    def test_breakout_type_filters(self):
        """Test Breakout Type filter functionality"""
        print("📈 TESTING BREAKOUT TYPE FILTERS")
        print("-" * 35)
        
        breakout_type_tests = [
            {"breakout_type": "200_dma", "name": "Breakout Type - 200 DMA"},
            {"breakout_type": "resistance", "name": "Breakout Type - Resistance"},
            {"breakout_type": "momentum", "name": "Breakout Type - Momentum"}
        ]
        
        for test in breakout_type_tests:
            breakout_type = test["breakout_type"]
            name = test["name"]
            
            success, data = self.test_api_endpoint(name, "GET", "stocks/breakouts/scan", 
                                                 params={"breakout_type": breakout_type, "limit": "20"}, timeout=45)
            
            if success:
                breakout_stocks = data.get('breakout_stocks', [])
                filters_applied = data.get('filters_applied', {})
                
                # Verify filter was applied correctly
                applied_breakout_type = filters_applied.get('breakout_type')
                filter_applied_correctly = applied_breakout_type == breakout_type
                
                self.log_test(f"Breakout Type Filter Applied - {breakout_type}", filter_applied_correctly, 
                            f"Requested: {breakout_type}, Applied: {applied_breakout_type}")
                
                # Check if results match the filter
                if breakout_stocks:
                    correct_type_count = 0
                    
                    for stock in breakout_stocks:
                        stock_breakout_type = stock.get('breakout_type', 'unknown')
                        if stock_breakout_type == breakout_type:
                            correct_type_count += 1
                    
                    accuracy = (correct_type_count / len(breakout_stocks)) * 100
                    self.log_test(f"Breakout Type Filter Accuracy - {breakout_type}", accuracy >= 90, 
                                f"{correct_type_count}/{len(breakout_stocks)} stocks have correct type ({accuracy:.1f}%)")
                else:
                    self.log_test(f"Breakout Type Filter Results - {breakout_type}", True, 
                                f"No breakout stocks found for type: {breakout_type}")

    def test_combined_filters(self):
        """Test combined Action and Breakout Type filters"""
        print("🔄 TESTING COMBINED FILTERS")
        print("-" * 28)
        
        combined_tests = [
            {"action": "BUY", "breakout_type": "200_dma", "name": "Combined - BUY + 200 DMA"},
            {"action": "BUY", "breakout_type": "resistance", "name": "Combined - BUY + Resistance"}
        ]
        
        for test in combined_tests:
            action = test["action"]
            breakout_type = test["breakout_type"]
            name = test["name"]
            
            success, data = self.test_api_endpoint(name, "GET", "stocks/breakouts/scan", 
                                                 params={"action": action, "breakout_type": breakout_type, "limit": "15"}, timeout=45)
            
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
                if breakout_stocks:
                    matching_stocks = 0
                    for stock in breakout_stocks:
                        trading_rec = stock.get('trading_recommendation', {})
                        stock_action = trading_rec.get('action', 'UNKNOWN') if trading_rec else 'UNKNOWN'
                        stock_breakout_type = stock.get('breakout_type', 'unknown')
                        
                        if stock_action == action and stock_breakout_type == breakout_type:
                            matching_stocks += 1
                    
                    accuracy = (matching_stocks / len(breakout_stocks)) * 100
                    self.log_test(f"Combined Filter Accuracy - {name}", accuracy >= 90, 
                                f"{matching_stocks}/{len(breakout_stocks)} stocks match both criteria ({accuracy:.1f}%)")
                else:
                    self.log_test(f"Combined Filter Results - {name}", True, 
                                f"No results found for combined filters")

    def test_filters_applied_section(self):
        """Test that filters_applied section includes new filter information"""
        print("📋 TESTING FILTERS_APPLIED SECTION")
        print("-" * 35)
        
        success, data = self.test_api_endpoint("Filters Applied Section", "GET", "stocks/breakouts/scan", 
                                             params={"action": "BUY", "breakout_type": "200_dma"}, timeout=30)
        
        if success:
            filters_applied = data.get('filters_applied', {})
            required_filter_keys = ['action', 'breakout_type', 'sector', 'min_confidence', 'risk_level', 'limit']
            
            missing_keys = [key for key in required_filter_keys if key not in filters_applied]
            
            if not missing_keys:
                self.log_test("Filters Applied Section Complete", True, 
                            f"All required filter keys present: {list(filters_applied.keys())}")
                
                # Verify the new filter values are correctly reported
                action_value = filters_applied.get('action')
                breakout_type_value = filters_applied.get('breakout_type')
                
                self.log_test("New Filter Values Reported", 
                            action_value == "BUY" and breakout_type_value == "200_dma", 
                            f"Action: {action_value}, Breakout Type: {breakout_type_value}")
            else:
                self.log_test("Filters Applied Section Complete", False, 
                            f"Missing filter keys: {missing_keys}")

    def run_tests(self):
        """Run all new filter tests"""
        print("🚀 TESTING NEW ACTION & BREAKOUT TYPE FILTERS")
        print("=" * 55)
        print(f"Testing API at: {self.api_url}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 55)
        print()

        # Run all tests
        self.test_action_filters()
        self.test_breakout_type_filters()
        self.test_combined_filters()
        self.test_filters_applied_section()
        
        # Print final results
        print("\n" + "=" * 55)
        print("📊 FINAL TEST RESULTS")
        print("=" * 55)
        print(f"Total Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 55)
        
        return self.tests_passed == self.tests_run

def main():
    """Main test execution"""
    tester = NewFilterTester()
    
    try:
        all_passed = tester.run_tests()
        return 0 if all_passed else 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n💥 Unexpected error during testing: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())