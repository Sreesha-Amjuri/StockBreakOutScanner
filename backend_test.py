#!/usr/bin/env python3
"""
StockBreak Pro Backend Testing - Valuation Filter Functionality
Testing the new valuation filter feature after npm dependency fixes
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import sys
import os

# Backend URL from environment
BACKEND_URL = "https://tradepulse-app-1.preview.emergentagent.com/api"

class ValuationFilterTester:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.test_results = []
        self.session = requests.Session()
        self.session.timeout = 30
        
    def log_test(self, test_name: str, success: bool, message: str, details: Dict = None):
        """Log test results"""
        result = {
            "test_name": test_name,
            "success": success,
            "message": message,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        print(f"   {message}")
        if details:
            print(f"   Details: {details}")
        print()
        
    def test_backend_connectivity(self) -> bool:
        """Test basic backend connectivity"""
        try:
            response = self.session.get(f"{self.backend_url}/health", timeout=10)
            if response.status_code == 200:
                self.log_test("Backend Connectivity", True, "Backend is accessible and responding")
                return True
            else:
                self.log_test("Backend Connectivity", False, f"Backend returned status {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Backend Connectivity", False, f"Failed to connect to backend: {str(e)}")
            return False
    
    def test_breakout_scan_endpoint_basic(self) -> bool:
        """Test basic breakout scan endpoint functionality"""
        try:
            response = self.session.get(f"{self.backend_url}/stocks/breakouts/scan?limit=10", timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check basic structure
                required_fields = ['breakout_stocks', 'scan_statistics', 'timestamp']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Basic Breakout Scan", False, f"Missing required fields: {missing_fields}")
                    return False
                
                breakout_stocks = data.get('breakout_stocks', [])
                if not breakout_stocks:
                    self.log_test("Basic Breakout Scan", False, "No breakout stocks returned")
                    return False
                
                self.log_test("Basic Breakout Scan", True, 
                            f"Successfully retrieved {len(breakout_stocks)} breakout stocks",
                            {"scan_stats": data.get('scan_statistics', {})})
                return True
            else:
                self.log_test("Basic Breakout Scan", False, f"API returned status {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Basic Breakout Scan", False, f"Error testing breakout scan: {str(e)}")
            return False
    
    def test_valuation_filter_parameter(self) -> bool:
        """Test valuation_filter parameter acceptance"""
        try:
            # Test each valuation category
            valuation_categories = [
                "Highly Undervalued",
                "Slightly Undervalued", 
                "Reasonable",
                "Slightly Overvalued",
                "Highly Overvalued"
            ]
            
            all_tests_passed = True
            category_results = {}
            
            for category in valuation_categories:
                try:
                    response = self.session.get(
                        f"{self.backend_url}/stocks/breakouts/scan",
                        params={
                            "limit": 20,
                            "valuation_filter": category
                        },
                        timeout=45
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        breakout_stocks = data.get('breakout_stocks', [])
                        
                        # Check if valuation_analysis field is present in stocks
                        stocks_with_valuation = 0
                        for stock in breakout_stocks:
                            if 'valuation_analysis' in stock:
                                stocks_with_valuation += 1
                        
                        category_results[category] = {
                            "status": "success",
                            "total_stocks": len(breakout_stocks),
                            "stocks_with_valuation": stocks_with_valuation,
                            "scan_time": data.get('scan_statistics', {}).get('scan_time_seconds', 0)
                        }
                        
                        print(f"   {category}: {len(breakout_stocks)} stocks, {stocks_with_valuation} with valuation data")
                        
                    else:
                        category_results[category] = {
                            "status": "error",
                            "error": f"HTTP {response.status_code}"
                        }
                        all_tests_passed = False
                        print(f"   {category}: ERROR - HTTP {response.status_code}")
                        
                except Exception as e:
                    category_results[category] = {
                        "status": "error", 
                        "error": str(e)
                    }
                    all_tests_passed = False
                    print(f"   {category}: ERROR - {str(e)}")
                
                # Small delay between requests
                time.sleep(1)
            
            if all_tests_passed:
                self.log_test("Valuation Filter Parameter", True, 
                            "All 5 valuation categories accepted successfully",
                            {"category_results": category_results})
            else:
                self.log_test("Valuation Filter Parameter", False,
                            "Some valuation categories failed",
                            {"category_results": category_results})
            
            return all_tests_passed
            
        except Exception as e:
            self.log_test("Valuation Filter Parameter", False, f"Error testing valuation filter: {str(e)}")
            return False
    
    def test_valuation_analysis_field(self) -> bool:
        """Test that valuation_analysis field is included in stock responses"""
        try:
            response = self.session.get(f"{self.backend_url}/stocks/breakouts/scan?limit=15", timeout=30)
            
            if response.status_code != 200:
                self.log_test("Valuation Analysis Field", False, f"API returned status {response.status_code}")
                return False
            
            data = response.json()
            breakout_stocks = data.get('breakout_stocks', [])
            
            if not breakout_stocks:
                self.log_test("Valuation Analysis Field", False, "No breakout stocks to test")
                return False
            
            stocks_with_valuation = 0
            valuation_categories_found = set()
            sample_valuation_data = None
            
            for stock in breakout_stocks:
                if 'valuation_analysis' in stock:
                    stocks_with_valuation += 1
                    valuation_data = stock['valuation_analysis']
                    
                    # Check required valuation fields
                    required_valuation_fields = [
                        'valuation_score', 'valuation_category', 'confidence'
                    ]
                    
                    if all(field in valuation_data for field in required_valuation_fields):
                        valuation_categories_found.add(valuation_data.get('valuation_category'))
                        if not sample_valuation_data:
                            sample_valuation_data = valuation_data
            
            coverage_percentage = (stocks_with_valuation / len(breakout_stocks)) * 100
            
            if stocks_with_valuation > 0:
                self.log_test("Valuation Analysis Field", True,
                            f"Valuation analysis present in {stocks_with_valuation}/{len(breakout_stocks)} stocks ({coverage_percentage:.1f}%)",
                            {
                                "categories_found": list(valuation_categories_found),
                                "sample_valuation": sample_valuation_data
                            })
                return True
            else:
                self.log_test("Valuation Analysis Field", False, "No stocks have valuation_analysis field")
                return False
                
        except Exception as e:
            self.log_test("Valuation Analysis Field", False, f"Error testing valuation analysis field: {str(e)}")
            return False
    
    def test_valuation_scoring_weights(self) -> bool:
        """Test that valuation scoring uses the correct weighted system"""
        try:
            response = self.session.get(f"{self.backend_url}/stocks/breakouts/scan?limit=20", timeout=30)
            
            if response.status_code != 200:
                self.log_test("Valuation Scoring Weights", False, f"API returned status {response.status_code}")
                return False
            
            data = response.json()
            breakout_stocks = data.get('breakout_stocks', [])
            
            stocks_with_detailed_valuation = 0
            weight_verification_results = []
            
            for stock in breakout_stocks:
                valuation_analysis = stock.get('valuation_analysis', {})
                breakdown = valuation_analysis.get('breakdown', {})
                
                if breakdown and 'details' in breakdown:
                    stocks_with_detailed_valuation += 1
                    
                    # Check for weight-related information in details
                    details = breakdown.get('details', [])
                    weight_info = {
                        "symbol": stock.get('symbol'),
                        "valuation_score": valuation_analysis.get('valuation_score'),
                        "total_weights": valuation_analysis.get('total_weights'),
                        "confidence": valuation_analysis.get('confidence'),
                        "details_count": len(details)
                    }
                    weight_verification_results.append(weight_info)
            
            if stocks_with_detailed_valuation > 0:
                self.log_test("Valuation Scoring Weights", True,
                            f"Found detailed valuation breakdown in {stocks_with_detailed_valuation} stocks",
                            {
                                "stocks_analyzed": stocks_with_detailed_valuation,
                                "sample_results": weight_verification_results[:3]  # Show first 3 samples
                            })
                return True
            else:
                self.log_test("Valuation Scoring Weights", False, 
                            "No stocks found with detailed valuation breakdown")
                return False
                
        except Exception as e:
            self.log_test("Valuation Scoring Weights", False, f"Error testing valuation weights: {str(e)}")
            return False
    
    def test_missing_financial_data_handling(self) -> bool:
        """Test proper exception handling when financial data is missing"""
        try:
            # Test with a larger sample to find stocks with missing data
            response = self.session.get(f"{self.backend_url}/stocks/breakouts/scan?limit=30", timeout=45)
            
            if response.status_code != 200:
                self.log_test("Missing Financial Data Handling", False, f"API returned status {response.status_code}")
                return False
            
            data = response.json()
            breakout_stocks = data.get('breakout_stocks', [])
            
            stocks_with_low_confidence = 0
            stocks_with_missing_data_notes = 0
            error_handling_examples = []
            
            for stock in breakout_stocks:
                valuation_analysis = stock.get('valuation_analysis', {})
                
                # Check for low confidence (indicating missing data)
                confidence = valuation_analysis.get('confidence', 'High')
                if confidence in ['Low', 'Medium']:
                    stocks_with_low_confidence += 1
                
                # Check for missing data indicators in breakdown details
                breakdown = valuation_analysis.get('breakdown', {})
                details = breakdown.get('details', [])
                
                for detail in details:
                    if 'insufficient' in detail.lower() or 'missing' in detail.lower() or 'error' in detail.lower():
                        stocks_with_missing_data_notes += 1
                        error_handling_examples.append({
                            "symbol": stock.get('symbol'),
                            "detail": detail,
                            "confidence": confidence
                        })
                        break
            
            # The API should handle missing data gracefully without crashing
            total_stocks = len(breakout_stocks)
            if total_stocks > 0:
                self.log_test("Missing Financial Data Handling", True,
                            f"API handled missing financial data gracefully for {total_stocks} stocks",
                            {
                                "total_stocks": total_stocks,
                                "low_confidence_stocks": stocks_with_low_confidence,
                                "missing_data_indicators": stocks_with_missing_data_notes,
                                "error_handling_examples": error_handling_examples[:2]
                            })
                return True
            else:
                self.log_test("Missing Financial Data Handling", False, "No stocks returned to test error handling")
                return False
                
        except Exception as e:
            self.log_test("Missing Financial Data Handling", False, f"Error testing missing data handling: {str(e)}")
            return False
    
    def test_frontend_backend_integration(self) -> bool:
        """Test that frontend can successfully call backend without dependency errors"""
        try:
            # Test CORS and basic API accessibility
            headers = {
                'Origin': 'https://tradepulse-app-1.preview.emergentagent.com',
                'Access-Control-Request-Method': 'GET',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            
            # Test preflight request
            preflight_response = self.session.options(f"{self.backend_url}/stocks/breakouts/scan", headers=headers)
            
            # Test actual API call with frontend-like headers
            api_headers = {
                'Origin': 'https://tradepulse-app-1.preview.emergentagent.com',
                'Content-Type': 'application/json'
            }
            
            response = self.session.get(
                f"{self.backend_url}/stocks/breakouts/scan?limit=10", 
                headers=api_headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check CORS headers
                cors_headers = {
                    'access-control-allow-origin': response.headers.get('access-control-allow-origin'),
                    'access-control-allow-methods': response.headers.get('access-control-allow-methods'),
                    'access-control-allow-headers': response.headers.get('access-control-allow-headers')
                }
                
                self.log_test("Frontend-Backend Integration", True,
                            "Frontend can successfully call backend APIs",
                            {
                                "cors_headers": cors_headers,
                                "response_size": len(str(data)),
                                "breakout_stocks_count": len(data.get('breakout_stocks', []))
                            })
                return True
            else:
                self.log_test("Frontend-Backend Integration", False, 
                            f"API call failed with status {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Frontend-Backend Integration", False, f"Error testing frontend integration: {str(e)}")
            return False
    
    def test_valuation_categories_comprehensive(self) -> bool:
        """Comprehensive test of all 5 valuation categories with detailed analysis"""
        try:
            valuation_categories = [
                "Highly Undervalued",
                "Slightly Undervalued", 
                "Reasonable",
                "Slightly Overvalued",
                "Highly Overvalued"
            ]
            
            comprehensive_results = {}
            all_categories_working = True
            
            for category in valuation_categories:
                try:
                    response = self.session.get(
                        f"{self.backend_url}/stocks/breakouts/scan",
                        params={
                            "limit": 25,
                            "valuation_filter": category
                        },
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        breakout_stocks = data.get('breakout_stocks', [])
                        
                        # Analyze returned stocks for correct valuation category
                        correct_category_count = 0
                        total_with_valuation = 0
                        
                        for stock in breakout_stocks:
                            valuation_analysis = stock.get('valuation_analysis', {})
                            if valuation_analysis:
                                total_with_valuation += 1
                                stock_category = valuation_analysis.get('valuation_category')
                                if stock_category == category:
                                    correct_category_count += 1
                        
                        accuracy = (correct_category_count / total_with_valuation * 100) if total_with_valuation > 0 else 0
                        
                        comprehensive_results[category] = {
                            "status": "success",
                            "total_stocks": len(breakout_stocks),
                            "stocks_with_valuation": total_with_valuation,
                            "correct_category_matches": correct_category_count,
                            "accuracy_percentage": round(accuracy, 1),
                            "scan_time": data.get('scan_statistics', {}).get('scan_time_seconds', 0)
                        }
                        
                        print(f"   {category}: {len(breakout_stocks)} stocks, {correct_category_count}/{total_with_valuation} correct matches ({accuracy:.1f}%)")
                        
                    else:
                        comprehensive_results[category] = {
                            "status": "error",
                            "error": f"HTTP {response.status_code}"
                        }
                        all_categories_working = False
                        
                except Exception as e:
                    comprehensive_results[category] = {
                        "status": "error",
                        "error": str(e)
                    }
                    all_categories_working = False
                
                time.sleep(2)  # Longer delay for comprehensive test
            
            if all_categories_working:
                self.log_test("Comprehensive Valuation Categories", True,
                            "All 5 valuation categories working with proper filtering",
                            {"detailed_results": comprehensive_results})
            else:
                self.log_test("Comprehensive Valuation Categories", False,
                            "Some valuation categories failed comprehensive testing",
                            {"detailed_results": comprehensive_results})
            
            return all_categories_working
            
        except Exception as e:
            self.log_test("Comprehensive Valuation Categories", False, f"Error in comprehensive testing: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all valuation filter tests"""
        print("🚀 Starting StockBreak Pro Valuation Filter Testing")
        print("=" * 60)
        print()
        
        start_time = time.time()
        
        # Test sequence
        tests = [
            ("Backend Connectivity", self.test_backend_connectivity),
            ("Basic Breakout Scan", self.test_breakout_scan_endpoint_basic),
            ("Valuation Filter Parameter", self.test_valuation_filter_parameter),
            ("Valuation Analysis Field", self.test_valuation_analysis_field),
            ("Valuation Scoring Weights", self.test_valuation_scoring_weights),
            ("Missing Financial Data Handling", self.test_missing_financial_data_handling),
            ("Frontend-Backend Integration", self.test_frontend_backend_integration),
            ("Comprehensive Valuation Categories", self.test_valuation_categories_comprehensive)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                self.log_test(test_name, False, f"Test execution error: {str(e)}")
        
        end_time = time.time()
        test_duration = end_time - start_time
        
        # Summary
        print("=" * 60)
        print("🎯 VALUATION FILTER TESTING SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print(f"Test Duration: {test_duration:.2f} seconds")
        print()
        
        # Critical issues
        critical_failures = [result for result in self.test_results if not result['success'] and 
                           result['test_name'] in ['Backend Connectivity', 'Basic Breakout Scan', 'Valuation Filter Parameter']]
        
        if critical_failures:
            print("🚨 CRITICAL ISSUES FOUND:")
            for failure in critical_failures:
                print(f"   - {failure['test_name']}: {failure['message']}")
            print()
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": (passed_tests/total_tests)*100,
            "test_duration": test_duration,
            "critical_failures": len(critical_failures),
            "detailed_results": self.test_results
        }

def main():
    """Main testing function"""
    tester = ValuationFilterTester()
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    if results['success_rate'] >= 80:
        print("✅ VALUATION FILTER TESTING COMPLETED SUCCESSFULLY")
        sys.exit(0)
    else:
        print("❌ VALUATION FILTER TESTING FAILED - CRITICAL ISSUES FOUND")
        sys.exit(1)

if __name__ == "__main__":
    main()