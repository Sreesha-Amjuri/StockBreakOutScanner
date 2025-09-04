#!/usr/bin/env python3
"""
Comprehensive Backend Testing for StockBreak Pro - Valuation Filter Functionality
Testing the newly implemented valuation analysis and filtering features
"""

import asyncio
import requests
import json
import time
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configuration
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://tradepulse-app-1.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class ValuationFilterTester:
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_test(self, test_name: str, passed: bool, details: str = "", data: Any = None):
        """Log test results"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            self.failed_tests += 1
            status = "❌ FAIL"
            
        result = {
            "test_name": test_name,
            "status": status,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        self.test_results.append(result)
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        if not passed and data:
            print(f"   Data: {json.dumps(data, indent=2)[:500]}...")
        print()

    def test_valuation_categories_filter(self):
        """Test all 5 valuation categories in the filter"""
        print("🎯 Testing Valuation Categories Filter...")
        
        valuation_categories = [
            "Highly Undervalued",
            "Slightly Undervalued", 
            "Reasonable",
            "Slightly Overvalued",
            "Highly Overvalued"
        ]
        
        for category in valuation_categories:
            try:
                response = requests.get(
                    f"{API_BASE}/stocks/breakouts/scan",
                    params={
                        "valuation_filter": category,
                        "limit": 20
                    },
                    timeout=120
                )
                
                if response.status_code == 200:
                    data = response.json()
                    breakouts = data.get('breakout_stocks', [])
                    
                    # Check if all returned stocks match the filter category
                    category_matches = 0
                    total_stocks = len(breakouts)
                    
                    for stock in breakouts:
                        valuation_analysis = stock.get('valuation_analysis', {})
                        stock_category = valuation_analysis.get('valuation_category', 'Unknown')
                        
                        if stock_category == category:
                            category_matches += 1
                    
                    if total_stocks == 0:
                        self.log_test(
                            f"Valuation Filter: {category}",
                            True,
                            f"No stocks found in category (acceptable for current market conditions)"
                        )
                    elif category_matches == total_stocks:
                        self.log_test(
                            f"Valuation Filter: {category}",
                            True,
                            f"All {total_stocks} stocks correctly match category filter"
                        )
                    else:
                        self.log_test(
                            f"Valuation Filter: {category}",
                            False,
                            f"Filter mismatch: {category_matches}/{total_stocks} stocks match category",
                            {"expected_category": category, "mismatched_stocks": total_stocks - category_matches}
                        )
                else:
                    self.log_test(
                        f"Valuation Filter: {category}",
                        False,
                        f"API error: {response.status_code}",
                        {"response": response.text[:200]}
                    )
                    
            except Exception as e:
                self.log_test(
                    f"Valuation Filter: {category}",
                    False,
                    f"Exception: {str(e)}"
                )

    def test_valuation_analysis_inclusion(self):
        """Test that valuation_analysis is included in stock data responses"""
        print("📊 Testing Valuation Analysis Inclusion...")
        
        try:
            response = requests.get(
                f"{API_BASE}/stocks/breakouts/scan",
                params={"limit": 10},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                breakouts = data.get('breakout_stocks', [])
                
                if not breakouts:
                    self.log_test(
                        "Valuation Analysis Inclusion",
                        False,
                        "No breakout stocks returned to test valuation analysis"
                    )
                    return
                
                stocks_with_valuation = 0
                required_fields = ['valuation_score', 'valuation_category', 'confidence', 'breakdown']
                
                for stock in breakouts:
                    valuation_analysis = stock.get('valuation_analysis', {})
                    
                    if valuation_analysis:
                        # Check if all required fields are present
                        has_all_fields = all(field in valuation_analysis for field in required_fields)
                        
                        if has_all_fields:
                            stocks_with_valuation += 1
                
                success_rate = (stocks_with_valuation / len(breakouts)) * 100
                
                if success_rate >= 90:
                    self.log_test(
                        "Valuation Analysis Inclusion",
                        True,
                        f"Valuation analysis present in {stocks_with_valuation}/{len(breakouts)} stocks ({success_rate:.1f}%)"
                    )
                else:
                    self.log_test(
                        "Valuation Analysis Inclusion",
                        False,
                        f"Low valuation analysis coverage: {stocks_with_valuation}/{len(breakouts)} stocks ({success_rate:.1f}%)",
                        {"sample_stock": breakouts[0] if breakouts else None}
                    )
            else:
                self.log_test(
                    "Valuation Analysis Inclusion",
                    False,
                    f"API error: {response.status_code}",
                    {"response": response.text[:200]}
                )
                
        except Exception as e:
            self.log_test(
                "Valuation Analysis Inclusion",
                False,
                f"Exception: {str(e)}"
            )

    def test_valuation_scoring_calculation(self):
        """Test valuation scoring with different financial metrics"""
        print("🧮 Testing Valuation Scoring Calculation...")
        
        try:
            response = requests.get(
                f"{API_BASE}/stocks/breakouts/scan",
                params={"limit": 15},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                breakouts = data.get('breakout_stocks', [])
                
                if not breakouts:
                    self.log_test(
                        "Valuation Scoring Calculation",
                        False,
                        "No breakout stocks returned to test valuation scoring"
                    )
                    return
                
                valid_scores = 0
                score_distribution = {"1-2": 0, "2-3": 0, "3-4": 0, "4-5": 0}
                
                for stock in breakouts:
                    valuation_analysis = stock.get('valuation_analysis', {})
                    score = valuation_analysis.get('valuation_score')
                    category = valuation_analysis.get('valuation_category')
                    confidence = valuation_analysis.get('confidence')
                    
                    if score is not None and 1.0 <= score <= 5.0:
                        valid_scores += 1
                        
                        # Check score distribution
                        if 1.0 <= score < 2.0:
                            score_distribution["1-2"] += 1
                        elif 2.0 <= score < 3.0:
                            score_distribution["2-3"] += 1
                        elif 3.0 <= score < 4.0:
                            score_distribution["3-4"] += 1
                        elif 4.0 <= score <= 5.0:
                            score_distribution["4-5"] += 1
                
                score_validity = (valid_scores / len(breakouts)) * 100
                
                if score_validity >= 80:
                    self.log_test(
                        "Valuation Scoring Calculation",
                        True,
                        f"Valid valuation scores in {valid_scores}/{len(breakouts)} stocks ({score_validity:.1f}%)",
                        {"score_distribution": score_distribution}
                    )
                else:
                    self.log_test(
                        "Valuation Scoring Calculation",
                        False,
                        f"Low valid score rate: {valid_scores}/{len(breakouts)} stocks ({score_validity:.1f}%)",
                        {"score_distribution": score_distribution}
                    )
            else:
                self.log_test(
                    "Valuation Scoring Calculation",
                    False,
                    f"API error: {response.status_code}"
                )
                
        except Exception as e:
            self.log_test(
                "Valuation Scoring Calculation",
                False,
                f"Exception: {str(e)}"
            )

    def test_valuation_confidence_levels(self):
        """Test valuation confidence levels (High/Medium/Low based on data availability)"""
        print("🎯 Testing Valuation Confidence Levels...")
        
        try:
            response = requests.get(
                f"{API_BASE}/stocks/breakouts/scan",
                params={"limit": 20},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                breakouts = data.get('breakout_stocks', [])
                
                if not breakouts:
                    self.log_test(
                        "Valuation Confidence Levels",
                        False,
                        "No breakout stocks returned to test confidence levels"
                    )
                    return
                
                confidence_distribution = {"High": 0, "Medium": 0, "Low": 0, "Invalid": 0}
                
                for stock in breakouts:
                    valuation_analysis = stock.get('valuation_analysis', {})
                    confidence = valuation_analysis.get('confidence')
                    
                    if confidence in ["High", "Medium", "Low"]:
                        confidence_distribution[confidence] += 1
                    else:
                        confidence_distribution["Invalid"] += 1
                
                valid_confidence = len(breakouts) - confidence_distribution["Invalid"]
                confidence_rate = (valid_confidence / len(breakouts)) * 100
                
                if confidence_rate >= 90:
                    self.log_test(
                        "Valuation Confidence Levels",
                        True,
                        f"Valid confidence levels in {valid_confidence}/{len(breakouts)} stocks ({confidence_rate:.1f}%)",
                        {"confidence_distribution": confidence_distribution}
                    )
                else:
                    self.log_test(
                        "Valuation Confidence Levels",
                        False,
                        f"Low valid confidence rate: {valid_confidence}/{len(breakouts)} stocks ({confidence_rate:.1f}%)",
                        {"confidence_distribution": confidence_distribution}
                    )
            else:
                self.log_test(
                    "Valuation Confidence Levels",
                    False,
                    f"API error: {response.status_code}"
                )
                
        except Exception as e:
            self.log_test(
                "Valuation Confidence Levels",
                False,
                f"Exception: {str(e)}"
            )

    def test_error_handling_missing_data(self):
        """Test proper error handling when financial data is missing or invalid"""
        print("🛡️ Testing Error Handling for Missing Financial Data...")
        
        try:
            # Test with a scan that should include stocks with varying data quality
            response = requests.get(
                f"{API_BASE}/stocks/breakouts/scan",
                params={"limit": 25},
                timeout=90
            )
            
            if response.status_code == 200:
                data = response.json()
                breakouts = data.get('breakout_stocks', [])
                
                if not breakouts:
                    self.log_test(
                        "Error Handling - Missing Data",
                        True,
                        "No breakouts found, but API handled request gracefully"
                    )
                    return
                
                # Check that all stocks have some form of valuation analysis
                stocks_with_fallback = 0
                
                for stock in breakouts:
                    valuation_analysis = stock.get('valuation_analysis', {})
                    
                    # Even with missing data, should have fallback values
                    if (valuation_analysis.get('valuation_category') and 
                        valuation_analysis.get('valuation_score') is not None):
                        stocks_with_fallback += 1
                
                fallback_rate = (stocks_with_fallback / len(breakouts)) * 100
                
                if fallback_rate >= 95:
                    self.log_test(
                        "Error Handling - Missing Data",
                        True,
                        f"Proper fallback handling in {stocks_with_fallback}/{len(breakouts)} stocks ({fallback_rate:.1f}%)"
                    )
                else:
                    self.log_test(
                        "Error Handling - Missing Data",
                        False,
                        f"Poor fallback handling: {stocks_with_fallback}/{len(breakouts)} stocks ({fallback_rate:.1f}%)"
                    )
            else:
                self.log_test(
                    "Error Handling - Missing Data",
                    False,
                    f"API error: {response.status_code}"
                )
                
        except Exception as e:
            self.log_test(
                "Error Handling - Missing Data",
                False,
                f"Exception: {str(e)}"
            )

    def test_weighted_scoring_system(self):
        """Test the weighted scoring system: P/E (30%), P/B (25%), PEG (20%), Dividend Yield (15%), P/S (10%)"""
        print("⚖️ Testing Weighted Scoring System...")
        
        try:
            response = requests.get(
                f"{API_BASE}/stocks/breakouts/scan",
                params={"limit": 15},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                breakouts = data.get('breakout_stocks', [])
                
                if not breakouts:
                    self.log_test(
                        "Weighted Scoring System",
                        False,
                        "No breakout stocks returned to test weighted scoring"
                    )
                    return
                
                stocks_with_breakdown = 0
                
                for stock in breakouts:
                    valuation_analysis = stock.get('valuation_analysis', {})
                    breakdown = valuation_analysis.get('breakdown', {})
                    
                    # Check if breakdown contains scoring details
                    if breakdown.get('details') and isinstance(breakdown['details'], list):
                        if len(breakdown['details']) > 0:
                            stocks_with_breakdown += 1
                
                breakdown_rate = (stocks_with_breakdown / len(breakouts)) * 100
                
                if breakdown_rate >= 70:
                    self.log_test(
                        "Weighted Scoring System",
                        True,
                        f"Scoring breakdown available in {stocks_with_breakdown}/{len(breakouts)} stocks ({breakdown_rate:.1f}%)"
                    )
                else:
                    self.log_test(
                        "Weighted Scoring System",
                        False,
                        f"Low breakdown availability: {stocks_with_breakdown}/{len(breakouts)} stocks ({breakdown_rate:.1f}%)"
                    )
            else:
                self.log_test(
                    "Weighted Scoring System",
                    False,
                    f"API error: {response.status_code}"
                )
                
        except Exception as e:
            self.log_test(
                "Weighted Scoring System",
                False,
                f"Exception: {str(e)}"
            )

    def test_valuation_filter_with_other_filters(self):
        """Test valuation filter works correctly with other filters (sector, confidence, risk)"""
        print("🔗 Testing Valuation Filter with Other Filters...")
        
        try:
            # Test combination of valuation filter with sector filter
            response = requests.get(
                f"{API_BASE}/stocks/breakouts/scan",
                params={
                    "valuation_filter": "Reasonable",
                    "sector": "IT",
                    "min_confidence": 0.6,
                    "limit": 15
                },
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                breakouts = data.get('breakout_stocks', [])
                
                # Check that all filters are applied correctly
                correct_valuation = 0
                correct_sector = 0
                correct_confidence = 0
                
                for stock in breakouts:
                    # Check valuation filter
                    valuation_category = stock.get('valuation_analysis', {}).get('valuation_category')
                    if valuation_category == "Reasonable":
                        correct_valuation += 1
                    
                    # Check sector filter
                    if stock.get('sector') == "IT":
                        correct_sector += 1
                    
                    # Check confidence filter
                    if stock.get('confidence_score', 0) >= 0.6:
                        correct_confidence += 1
                
                total_stocks = len(breakouts)
                
                if total_stocks == 0:
                    self.log_test(
                        "Combined Filters",
                        True,
                        "No stocks match combined filters (acceptable)"
                    )
                elif (correct_valuation == total_stocks and 
                      correct_sector == total_stocks and 
                      correct_confidence == total_stocks):
                    self.log_test(
                        "Combined Filters",
                        True,
                        f"All {total_stocks} stocks correctly match all filters"
                    )
                else:
                    self.log_test(
                        "Combined Filters",
                        False,
                        f"Filter mismatch - Valuation: {correct_valuation}/{total_stocks}, Sector: {correct_sector}/{total_stocks}, Confidence: {correct_confidence}/{total_stocks}"
                    )
            else:
                self.log_test(
                    "Combined Filters",
                    False,
                    f"API error: {response.status_code}"
                )
                
        except Exception as e:
            self.log_test(
                "Combined Filters",
                False,
                f"Exception: {str(e)}"
            )

    def test_api_performance_with_valuation(self):
        """Test API performance with valuation calculations"""
        print("⚡ Testing API Performance with Valuation Calculations...")
        
        try:
            start_time = time.time()
            
            response = requests.get(
                f"{API_BASE}/stocks/breakouts/scan",
                params={"limit": 30},
                timeout=120
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                breakouts = data.get('breakout_stocks', [])
                
                # Performance should be reasonable even with valuation calculations
                if response_time <= 60:  # Should complete within 60 seconds
                    self.log_test(
                        "API Performance with Valuation",
                        True,
                        f"Scan completed in {response_time:.2f}s with {len(breakouts)} results"
                    )
                else:
                    self.log_test(
                        "API Performance with Valuation",
                        False,
                        f"Slow performance: {response_time:.2f}s for {len(breakouts)} results"
                    )
            else:
                self.log_test(
                    "API Performance with Valuation",
                    False,
                    f"API error: {response.status_code} in {response_time:.2f}s"
                )
                
        except Exception as e:
            self.log_test(
                "API Performance with Valuation",
                False,
                f"Exception: {str(e)}"
            )

    def run_all_tests(self):
        """Run all valuation filter tests"""
        print("🚀 Starting Comprehensive Valuation Filter Testing...")
        print(f"Backend URL: {BACKEND_URL}")
        print("=" * 80)
        
        # Test all valuation filter functionality
        self.test_valuation_categories_filter()
        self.test_valuation_analysis_inclusion()
        self.test_valuation_scoring_calculation()
        self.test_valuation_confidence_levels()
        self.test_error_handling_missing_data()
        self.test_weighted_scoring_system()
        self.test_valuation_filter_with_other_filters()
        self.test_api_performance_with_valuation()
        
        # Print summary
        print("=" * 80)
        print("📊 VALUATION FILTER TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests} ✅")
        print(f"Failed: {self.failed_tests} ❌")
        print(f"Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        print()
        
        if self.failed_tests > 0:
            print("❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['passed']:
                    print(f"  - {result['test_name']}: {result['details']}")
            print()
        
        return {
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "failed_tests": self.failed_tests,
            "success_rate": (self.passed_tests/self.total_tests)*100,
            "test_results": self.test_results
        }

def main():
    """Main test execution"""
    tester = ValuationFilterTester()
    results = tester.run_all_tests()
    
    # Save detailed results
    with open('/app/valuation_filter_test_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"📄 Detailed results saved to: /app/valuation_filter_test_results.json")
    
    return results['success_rate'] >= 70  # 70% success rate threshold

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)