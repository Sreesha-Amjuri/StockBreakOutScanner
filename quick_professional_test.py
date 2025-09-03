#!/usr/bin/env python3
"""
Quick Professional Endpoints Test for StockBreak Pro v2.0
"""

import requests
import json
from datetime import datetime

def test_endpoint(name, url, method="GET", params=None, timeout=30):
    """Test a single endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, params=params, timeout=timeout)
        
        print(f"\n🔍 Testing {name}")
        print(f"URL: {url}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ SUCCESS - Response received")
                
                # Show key information based on endpoint
                if "market/news" in url:
                    news_count = len(data.get('news', []))
                    print(f"   📰 Found {news_count} news items")
                    if news_count > 0:
                        print(f"   📰 Latest: {data['news'][0].get('title', 'N/A')}")
                
                elif "analytics/performance" in url:
                    system_stats = data.get('system_stats', {})
                    total_stocks = system_stats.get('total_nse_stocks', 0)
                    sectors = data.get('market_coverage', {}).get('sectors_covered', 0)
                    print(f"   📊 Tracking {total_stocks} stocks across {sectors} sectors")
                    
                    indicators = data.get('technical_indicators', [])
                    active_indicators = [ind for ind in indicators if ind.get('status') == 'Active']
                    print(f"   📈 {len(active_indicators)} technical indicators active")
                
                elif "alerts/price" in url:
                    active_count = data.get('active_count', 0)
                    message = data.get('message', '')
                    print(f"   🔔 Active alerts: {active_count}")
                    print(f"   🔔 Status: {message}")
                
                elif "export/data" in url:
                    export_records = data.get('export_data', [])
                    total_records = data.get('total_records', 0)
                    print(f"   📤 Exported {total_records} records")
                    if export_records:
                        print(f"   📤 Sample: {export_records[0].get('Symbol', 'N/A')}")
                
                elif "system/health" in url:
                    status = data.get('status', '')
                    services = data.get('services', {})
                    data_quality = data.get('data_quality', {})
                    print(f"   🏥 System status: {status}")
                    print(f"   🏥 Stock coverage: {data_quality.get('stock_coverage', 'N/A')}")
                    print(f"   🏥 Active indicators: {data_quality.get('indicators_active', 0)}")
                
                elif "breakouts/scan" in url:
                    total_scanned = data.get('total_scanned', 0)
                    breakouts_found = data.get('breakouts_found', 0)
                    scan_stats = data.get('scan_statistics', {})
                    scan_time = scan_stats.get('scan_time_seconds', 0)
                    print(f"   🔍 Scanned {total_scanned} stocks, found {breakouts_found} breakouts")
                    if scan_time > 0:
                        print(f"   ⏱️  Scan time: {scan_time:.2f} seconds")
                
                return True, data
            except Exception as e:
                print(f"❌ ERROR parsing JSON: {str(e)}")
                print(f"Raw response: {response.text[:200]}")
                return False, {}
        else:
            print(f"❌ FAILED - Status {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False, {}
            
    except requests.exceptions.Timeout:
        print(f"❌ TIMEOUT after {timeout}s")
        return False, {}
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False, {}

def main():
    base_url = "https://tradepulse-app-1.preview.emergentagent.com/api"
    
    print("🚀 StockBreak Pro v2.0 - Quick Professional Features Test")
    print("=" * 65)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)
    
    tests = [
        # Test 1: Market News Integration
        ("Market News Integration", f"{base_url}/market/news"),
        
        # Test 2: Performance Analytics
        ("Performance Analytics", f"{base_url}/analytics/performance"),
        
        # Test 3: Price Alerts
        ("Price Alerts", f"{base_url}/alerts/price"),
        
        # Test 4: Data Export (with query params)
        ("Data Export", f"{base_url}/export/data", "POST", {"format": "csv", "stocks": "RELIANCE,TCS"}),
        
        # Test 5: System Health Check
        ("System Health Check", f"{base_url}/system/health"),
        
        # Test 6: Full NSE Scanning (smaller limit for quick test)
        ("NSE Scanning (100 stocks)", f"{base_url}/stocks/breakouts/scan", "GET", {"limit": "100"}),
        
        # Test 7: Enhanced Technical Indicators
        ("Enhanced Technical Indicators", f"{base_url}/stocks/RELIANCE"),
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        name = test[0]
        url = test[1]
        method = test[2] if len(test) > 2 else "GET"
        params = test[3] if len(test) > 3 else None
        
        success, data = test_endpoint(name, url, method, params, timeout=60)
        if success:
            passed += 1
    
    print("\n" + "=" * 65)
    print("📊 QUICK TEST RESULTS")
    print("=" * 65)
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("✅ ALL PROFESSIONAL FEATURES ARE WORKING!")
    else:
        print(f"❌ {total - passed} tests failed")
    
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

if __name__ == "__main__":
    main()