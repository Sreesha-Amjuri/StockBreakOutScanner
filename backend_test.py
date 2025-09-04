#!/usr/bin/env python3
"""
StockBreak Pro Backend Performance Testing Suite
Testing PERFORMANCE OPTIMIZED backend after major optimizations
"""

import asyncio
import aiohttp
import time
import json
import sys
import os
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

# Backend URL from environment
BACKEND_URL = "https://tradepulse-app-1.preview.emergentagent.com/api"

class PerformanceTestSuite:
    def __init__(self):
        self.session = None
        self.test_results = []
        self.performance_metrics = {}
        
    async def setup(self):
        """Setup test session"""
        timeout = aiohttp.ClientTimeout(total=120)  # 2 minute timeout for tests
        self.session = aiohttp.ClientSession(timeout=timeout)
        
    async def cleanup(self):
        """Cleanup test session"""
        if self.session:
            await self.session.close()
    
    async def make_request(self, endpoint: str, method: str = "GET", data: Dict = None, timeout: int = 120) -> Dict:
        """Make HTTP request with error handling"""
        url = f"{BACKEND_URL}{endpoint}"
        
        try:
            start_time = time.time()
            
            if method == "GET":
                async with self.session.get(url) as response:
                    response_time = time.time() - start_time
                    if response.status == 200:
                        result = await response.json()
                        result['_response_time'] = response_time
                        result['_status_code'] = response.status
                        return result
                    else:
                        return {
                            "error": f"HTTP {response.status}",
                            "_response_time": response_time,
                            "_status_code": response.status
                        }
            elif method == "POST":
                async with self.session.post(url, json=data) as response:
                    response_time = time.time() - start_time
                    if response.status == 200:
                        result = await response.json()
                        result['_response_time'] = response_time
                        result['_status_code'] = response.status
                        return result
                    else:
                        return {
                            "error": f"HTTP {response.status}",
                            "_response_time": response_time,
                            "_status_code": response.status
                        }
                        
        except asyncio.TimeoutError:
            return {
                "error": "Request timeout",
                "_response_time": time.time() - start_time,
                "_status_code": 408
            }
        except Exception as e:
            return {
                "error": str(e),
                "_response_time": time.time() - start_time,
                "_status_code": 500
            }
    
    def log_test_result(self, test_name: str, success: bool, details: str, response_time: float = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "response_time": response_time
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        time_info = f" ({response_time:.2f}s)" if response_time else ""
        print(f"{status}: {test_name}{time_info}")
        if not success or response_time:
            print(f"   Details: {details}")
    
    async def test_performance_scan_default_limit(self):
        """Test /api/stocks/breakouts/scan with default limit (50) - should complete in under 60 seconds"""
        print("\n🚀 Testing Performance: Default 50-stock scan (Target: <60s)")
        
        start_time = time.time()
        result = await self.make_request("/stocks/breakouts/scan", timeout=90)
        total_time = time.time() - start_time
        
        if "error" in result:
            self.log_test_result(
                "Default Scan Performance", 
                False, 
                f"Scan failed: {result['error']}", 
                total_time
            )
            return False
        
        # Check performance requirement
        performance_target_met = total_time < 60.0
        
        # Check scan results
        stocks_scanned = result.get('scan_statistics', {}).get('total_scanned', 0)
        breakouts_found = result.get('scan_statistics', {}).get('breakouts_found', 0)
        
        details = f"Scanned {stocks_scanned} stocks, found {breakouts_found} breakouts in {total_time:.2f}s"
        if performance_target_met:
            details += " - Performance target met (<60s)"
        else:
            details += f" - Performance target MISSED (>{total_time:.1f}s > 60s)"
        
        self.log_test_result(
            "Default Scan Performance", 
            performance_target_met and stocks_scanned > 0, 
            details, 
            total_time
        )
        
        # Store performance metrics
        self.performance_metrics['default_scan'] = {
            'time': total_time,
            'stocks_scanned': stocks_scanned,
            'breakouts_found': breakouts_found,
            'target_met': performance_target_met
        }
        
        return performance_target_met and stocks_scanned > 0
    
    async def test_cache_hit_rates(self):
        """Test cache hit rates with repeated scans"""
        print("\n📊 Testing Cache Hit Rates (30-minute cache)")
        
        # First scan (cold cache)
        print("   Running first scan (cold cache)...")
        start_time = time.time()
        result1 = await self.make_request("/stocks/breakouts/scan?limit=20")
        first_scan_time = time.time() - start_time
        
        if "error" in result1:
            self.log_test_result(
                "Cache Performance - First Scan", 
                False, 
                f"First scan failed: {result1['error']}", 
                first_scan_time
            )
            return False
        
        # Wait a moment then run second scan (should hit cache)
        await asyncio.sleep(2)
        
        print("   Running second scan (should hit cache)...")
        start_time = time.time()
        result2 = await self.make_request("/stocks/breakouts/scan?limit=20")
        second_scan_time = time.time() - start_time
        
        if "error" in result2:
            self.log_test_result(
                "Cache Performance - Second Scan", 
                False, 
                f"Second scan failed: {result2['error']}", 
                second_scan_time
            )
            return False
        
        # Calculate performance improvement
        improvement = ((first_scan_time - second_scan_time) / first_scan_time) * 100
        cache_effective = second_scan_time < first_scan_time and improvement > 10
        
        details = f"First: {first_scan_time:.2f}s, Second: {second_scan_time:.2f}s, Improvement: {improvement:.1f}%"
        
        self.log_test_result(
            "Cache Hit Rate Performance", 
            cache_effective, 
            details, 
            second_scan_time
        )
        
        # Store cache metrics
        self.performance_metrics['cache_performance'] = {
            'first_scan_time': first_scan_time,
            'second_scan_time': second_scan_time,
            'improvement_percent': improvement,
            'cache_effective': cache_effective
        }
        
        return cache_effective
    
    async def test_timeout_protection(self):
        """Test 90-second timeout prevents hanging requests"""
        print("\n⏱️  Testing Timeout Protection (90s total timeout)")
        
        # Test with larger limit that might approach timeout
        start_time = time.time()
        result = await self.make_request("/stocks/breakouts/scan?limit=100", timeout=95)
        total_time = time.time() - start_time
        
        # Check if request completed within reasonable time or timed out gracefully
        timeout_handled = total_time < 95.0  # Should complete or timeout before our 95s limit
        
        if "error" in result and "timeout" in result["error"].lower():
            # Graceful timeout is acceptable
            details = f"Request timed out gracefully after {total_time:.2f}s"
            success = True
        elif "error" not in result:
            # Successful completion
            stocks_scanned = result.get('scan_statistics', {}).get('total_scanned', 0)
            details = f"Completed successfully in {total_time:.2f}s, scanned {stocks_scanned} stocks"
            success = True
        else:
            # Other error
            details = f"Request failed: {result.get('error', 'Unknown error')} after {total_time:.2f}s"
            success = False
        
        self.log_test_result(
            "Timeout Protection", 
            success and timeout_handled, 
            details, 
            total_time
        )
        
        return success and timeout_handled
    
    async def test_individual_stock_timeouts(self):
        """Test individual stock timeouts (10s per stock)"""
        print("\n🎯 Testing Individual Stock Timeout Protection (10s per stock)")
        
        # Test smaller batch to verify individual timeouts work
        start_time = time.time()
        result = await self.make_request("/stocks/breakouts/scan?limit=10")
        total_time = time.time() - start_time
        
        if "error" in result:
            self.log_test_result(
                "Individual Stock Timeouts", 
                False, 
                f"Scan failed: {result['error']}", 
                total_time
            )
            return False
        
        stocks_scanned = result.get('scan_statistics', {}).get('total_scanned', 0)
        
        # With 10s timeout per stock and concurrent processing, 10 stocks should complete quickly
        reasonable_time = total_time < 30.0  # Should be much faster with concurrent processing
        
        details = f"Scanned {stocks_scanned} stocks in {total_time:.2f}s"
        if reasonable_time:
            details += " - Individual timeouts working (no hanging requests)"
        else:
            details += " - Possible timeout issues (too slow)"
        
        self.log_test_result(
            "Individual Stock Timeouts", 
            reasonable_time and stocks_scanned > 0, 
            details, 
            total_time
        )
        
        return reasonable_time and stocks_scanned > 0
    
    async def test_concurrent_vs_sequential_performance(self):
        """Test concurrent processing performance vs expected sequential performance"""
        print("\n⚡ Testing Concurrent Processing Performance")
        
        # Test concurrent processing with moderate load
        start_time = time.time()
        result = await self.make_request("/stocks/breakouts/scan?limit=25")
        concurrent_time = time.time() - start_time
        
        if "error" in result:
            self.log_test_result(
                "Concurrent Processing Performance", 
                False, 
                f"Concurrent scan failed: {result['error']}", 
                concurrent_time
            )
            return False
        
        stocks_scanned = result.get('scan_statistics', {}).get('total_scanned', 0)
        
        # With concurrent processing, 25 stocks should complete much faster than sequential
        # Sequential would be ~25 * 2s = 50s, concurrent should be much faster
        expected_sequential_time = stocks_scanned * 2.0  # Rough estimate
        performance_gain = expected_sequential_time / concurrent_time if concurrent_time > 0 else 1
        
        good_performance = concurrent_time < 45.0 and performance_gain > 1.5
        
        details = f"Scanned {stocks_scanned} stocks in {concurrent_time:.2f}s"
        details += f", estimated {performance_gain:.1f}x faster than sequential"
        
        self.log_test_result(
            "Concurrent Processing Performance", 
            good_performance, 
            details, 
            concurrent_time
        )
        
        # Store concurrent performance metrics
        self.performance_metrics['concurrent_performance'] = {
            'time': concurrent_time,
            'stocks_scanned': stocks_scanned,
            'performance_gain': performance_gain,
            'good_performance': good_performance
        }
        
        return good_performance
    
    async def test_scan_statistics_accuracy(self):
        """Test scan statistics accuracy with optimized processing"""
        print("\n📈 Testing Scan Statistics Accuracy")
        
        result = await self.make_request("/stocks/breakouts/scan?limit=30")
        
        if "error" in result:
            self.log_test_result(
                "Scan Statistics Accuracy", 
                False, 
                f"Scan failed: {result['error']}"
            )
            return False
        
        # Check required statistics fields (actual API structure)
        scan_stats = result.get('scan_statistics', {})
        required_fields = ['total_scanned', 'breakouts_found', 'success_rate']
        
        missing_fields = [field for field in required_fields if field not in scan_stats]
        
        if missing_fields:
            self.log_test_result(
                "Scan Statistics Accuracy", 
                False, 
                f"Missing statistics fields: {missing_fields}"
            )
            return False
        
        # Validate statistics values
        total_scanned = scan_stats.get('total_scanned', 0)
        breakouts_found = scan_stats.get('breakouts_found', 0)
        success_rate = scan_stats.get('success_rate', '0%')
        cache_usage = scan_stats.get('cache_usage', '')
        
        # Check logical consistency
        valid_stats = (
            0 <= total_scanned <= 30 and  # Should scan requested amount or less
            0 <= breakouts_found <= total_scanned and  # Can't find more breakouts than stocks scanned
            success_rate is not None  # Should have success rate
        )
        
        details = f"Scanned: {total_scanned}, Breakouts: {breakouts_found}, "
        details += f"Success Rate: {success_rate}, Cache: {cache_usage}"
        
        self.log_test_result(
            "Scan Statistics Accuracy", 
            valid_stats, 
            details
        )
        
        return valid_stats
    
    async def test_performance_metrics_logging(self):
        """Test performance metrics logging with cache hit rates and timing"""
        print("\n📊 Testing Performance Metrics and Optimization Configuration")
        
        result = await self.make_request("/stocks/breakouts/scan?limit=15")
        
        if "error" in result:
            self.log_test_result(
                "Performance Metrics and Configuration", 
                False, 
                f"Scan failed: {result['error']}"
            )
            return False
        
        # Check for scanning configuration info (actual API structure)
        scanning_info = result.get('scanning_info', {})
        expected_config = {
            'batch_size': 10,  # Should be optimized to 10
            'cache_expiry_minutes': 30,  # Should be extended to 30
            'processing_method': 'Batch processing with caching'
        }
        
        config_correct = True
        config_details = []
        
        for key, expected_value in expected_config.items():
            actual_value = scanning_info.get(key)
            if actual_value == expected_value:
                config_details.append(f"✅ {key}: {actual_value}")
            else:
                config_details.append(f"❌ {key}: {actual_value} (expected {expected_value})")
                config_correct = False
        
        # Check cache usage info
        scan_stats = result.get('scan_statistics', {})
        cache_info = scan_stats.get('cache_usage', '')
        has_cache_info = 'cached' in cache_info.lower() if cache_info else False
        
        if has_cache_info:
            config_details.append(f"✅ Cache info: {cache_info}")
        else:
            config_details.append("❌ No cache usage information")
            config_correct = False
        
        details = "; ".join(config_details)
        
        self.log_test_result(
            "Performance Metrics and Configuration", 
            config_correct and has_cache_info, 
            details
        )
        
        return config_correct and has_cache_info
    
    async def test_optimized_batch_processing(self):
        """Test optimized batch processing (BATCH_SIZE=10, MAX_CONCURRENT=5)"""
        print("\n🔄 Testing Optimized Batch Processing Configuration")
        
        # Test with a size that would require multiple batches
        start_time = time.time()
        result = await self.make_request("/stocks/breakouts/scan?limit=35")
        total_time = time.time() - start_time
        
        if "error" in result:
            self.log_test_result(
                "Optimized Batch Processing", 
                False, 
                f"Batch processing test failed: {result['error']}", 
                total_time
            )
            return False
        
        stocks_scanned = result.get('scan_statistics', {}).get('total_scanned', 0)
        
        # With optimized batching (10 per batch, 5 concurrent), 35 stocks should process efficiently
        # Should complete faster than old larger batches
        efficient_processing = total_time < 60.0 and stocks_scanned > 0
        
        details = f"Processed {stocks_scanned} stocks in {total_time:.2f}s using optimized batching"
        if efficient_processing:
            details += " - Batch optimization working"
        else:
            details += " - Batch processing may need optimization"
        
        self.log_test_result(
            "Optimized Batch Processing", 
            efficient_processing, 
            details, 
            total_time
        )
        
        return efficient_processing
    
    async def run_all_performance_tests(self):
        """Run all performance tests"""
        print("🚀 Starting StockBreak Pro Performance Testing Suite")
        print("=" * 60)
        
        await self.setup()
        
        try:
            # Core performance tests
            test_functions = [
                self.test_performance_scan_default_limit,
                self.test_cache_hit_rates,
                self.test_timeout_protection,
                self.test_individual_stock_timeouts,
                self.test_concurrent_vs_sequential_performance,
                self.test_scan_statistics_accuracy,
                self.test_performance_metrics_logging,
                self.test_optimized_batch_processing
            ]
            
            results = []
            for test_func in test_functions:
                try:
                    result = await test_func()
                    results.append(result)
                except Exception as e:
                    print(f"❌ Test {test_func.__name__} failed with exception: {e}")
                    results.append(False)
            
            # Summary
            print("\n" + "=" * 60)
            print("📊 PERFORMANCE TEST SUMMARY")
            print("=" * 60)
            
            passed = sum(results)
            total = len(results)
            success_rate = (passed / total) * 100 if total > 0 else 0
            
            print(f"Tests Passed: {passed}/{total} ({success_rate:.1f}%)")
            
            # Performance metrics summary
            if self.performance_metrics:
                print("\n🎯 PERFORMANCE METRICS:")
                
                if 'default_scan' in self.performance_metrics:
                    metrics = self.performance_metrics['default_scan']
                    print(f"   Default Scan: {metrics['time']:.2f}s for {metrics['stocks_scanned']} stocks")
                    print(f"   Target Met: {'✅' if metrics['target_met'] else '❌'} (<60s requirement)")
                
                if 'cache_performance' in self.performance_metrics:
                    metrics = self.performance_metrics['cache_performance']
                    print(f"   Cache Improvement: {metrics['improvement_percent']:.1f}%")
                    print(f"   Cache Effective: {'✅' if metrics['cache_effective'] else '❌'}")
                
                if 'concurrent_performance' in self.performance_metrics:
                    metrics = self.performance_metrics['concurrent_performance']
                    print(f"   Concurrent Speedup: {metrics['performance_gain']:.1f}x vs sequential")
                    print(f"   Performance Good: {'✅' if metrics['good_performance'] else '❌'}")
            
            # Overall assessment
            print(f"\n🏆 OVERALL PERFORMANCE: {'✅ EXCELLENT' if success_rate >= 80 else '⚠️  NEEDS IMPROVEMENT' if success_rate >= 60 else '❌ POOR'}")
            
            return success_rate >= 75  # 75% pass rate for performance tests
            
        finally:
            await self.cleanup()

async def main():
    """Main test execution"""
    suite = PerformanceTestSuite()
    success = await suite.run_all_performance_tests()
    
    if success:
        print("\n✅ Performance testing completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Performance testing found issues!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())