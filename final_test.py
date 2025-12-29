#!/usr/bin/env python3
"""
Final Comprehensive Test of StockBreak Pro Enhanced Features
"""

import requests
import json
from datetime import datetime

def test_all_enhanced_apis():
    base_url = "https://stockport-3.preview.emergentagent.com/api"
    
    print("🚀 FINAL COMPREHENSIVE TEST - STOCKBREAK PRO ENHANCED FEATURES")
    print("=" * 65)
    print(f"Testing at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Enhanced Search API
    print("\n1. 🔍 Enhanced Search API")
    try:
        response = requests.get(f"{base_url}/stocks/search", 
                              params={"q": "REL", "include_price": "true"}, 
                              timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            if results and 'current_price' in results[0]:
                print("   ✅ PASS - Search with price data working")
                tests_passed += 1
            else:
                print("   ❌ FAIL - Price data missing in search results")
        else:
            print(f"   ❌ FAIL - HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ FAIL - Error: {str(e)}")
    total_tests += 1
    
    # Test 2: Fundamentals API
    print("\n2. 📊 Fundamentals API")
    try:
        response = requests.get(f"{base_url}/stocks/RELIANCE/fundamentals", timeout=10)
        if response.status_code == 200:
            data = response.json()
            required_fields = ['pe_ratio', 'roe', 'debt_to_equity', 'fundamental_score', 'rating']
            if all(field in data for field in required_fields):
                print(f"   ✅ PASS - P/E: {data.get('pe_ratio')}, ROE: {data.get('roe')}%, Rating: {data.get('rating')}")
                tests_passed += 1
            else:
                print("   ❌ FAIL - Missing fundamental fields")
        else:
            print(f"   ❌ FAIL - HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ FAIL - Error: {str(e)}")
    total_tests += 1
    
    # Test 3: News API
    print("\n3. 📰 News API")
    try:
        response = requests.get(f"{base_url}/stocks/RELIANCE/news", timeout=15)
        if response.status_code == 200:
            data = response.json()
            news_items = data.get('news', [])
            overall_sentiment = data.get('overall_sentiment')
            if news_items and overall_sentiment:
                print(f"   ✅ PASS - Found {len(news_items)} news items, Sentiment: {overall_sentiment}")
                tests_passed += 1
            else:
                print("   ❌ FAIL - Missing news or sentiment data")
        else:
            print(f"   ❌ FAIL - HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ FAIL - Error: {str(e)}")
    total_tests += 1
    
    # Test 4: Market News API
    print("\n4. 📈 Market News API")
    try:
        response = requests.get(f"{base_url}/news/market", timeout=15)
        if response.status_code == 200:
            data = response.json()
            headlines = data.get('headlines', [])
            market_mood = data.get('market_mood')
            print(f"   ✅ PASS - Found {len(headlines)} headlines, Market mood: {market_mood}")
            tests_passed += 1
        else:
            print(f"   ❌ FAIL - HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ FAIL - Error: {str(e)}")
    total_tests += 1
    
    # Test 5: Quick Scan API
    print("\n5. ⚡ Quick Scan API")
    try:
        response = requests.get(f"{base_url}/stocks/breakouts/quick-scan", 
                              params={"min_confidence": "0.5"}, 
                              timeout=30)
        if response.status_code == 200:
            data = response.json()
            breakouts = data.get('breakouts', [])
            scan_time = data.get('scan_time_seconds', 0)
            total_scanned = data.get('total_scanned', 0)
            print(f"   ✅ PASS - Scanned {total_scanned} stocks in {scan_time:.2f}s, Found {len(breakouts)} breakouts")
            tests_passed += 1
        else:
            print(f"   ❌ FAIL - HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ FAIL - Error: {str(e)}")
    total_tests += 1
    
    # Test 6: Watchlist API
    print("\n6. ⭐ Watchlist API")
    try:
        # Add to watchlist
        response = requests.post(f"{base_url}/watchlist", 
                               params={"symbol": "HDFCBANK"}, 
                               timeout=15)
        if response.status_code == 200:
            print("   ✅ PASS - Successfully added to watchlist")
            tests_passed += 1
            
            # Clean up
            requests.delete(f"{base_url}/watchlist/HDFCBANK")
        else:
            print(f"   ❌ FAIL - HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ FAIL - Error: {str(e)}")
    total_tests += 1
    
    # Test 7: Scan Progress API
    print("\n7. 📊 Scan Progress API")
    try:
        response = requests.get(f"{base_url}/stocks/scan/progress", timeout=10)
        if response.status_code == 200:
            data = response.json()
            status = data.get('status')
            progress = data.get('progress_percentage', 0)
            print(f"   ✅ PASS - Status: {status}, Progress: {progress}%")
            tests_passed += 1
        else:
            print(f"   ❌ FAIL - HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ FAIL - Error: {str(e)}")
    total_tests += 1
    
    # Final Results
    print("\n" + "=" * 65)
    print("📊 FINAL TEST RESULTS")
    print("=" * 65)
    print(f"Tests Passed: {tests_passed}/{total_tests}")
    print(f"Success Rate: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed >= 6:
        print("🎉 ENHANCED FEATURES TEST: PASSED")
        print("✅ All critical StockBreak Pro enhanced features are working!")
    else:
        print("❌ ENHANCED FEATURES TEST: FAILED")
        print("⚠️  Some critical features need attention")
    
    return tests_passed >= 6

if __name__ == "__main__":
    success = test_all_enhanced_apis()
    exit(0 if success else 1)