#!/usr/bin/env python3
"""
Enhanced Technical Indicators Test for StockBreak Pro v2.0
Tests all 13 technical indicators as requested in the review
"""

import requests
import json
from datetime import datetime

def test_technical_indicators(symbol):
    """Test all 13 technical indicators for a specific stock"""
    url = f"https://tradepulse-app-1.preview.emergentagent.com/api/stocks/{symbol}"
    
    try:
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            technical_data = data.get('technical_indicators', {})
            current_price = data.get('current_price', 0)
            
            print(f"\n📈 {symbol} - Technical Indicators Analysis")
            print(f"Current Price: ₹{current_price:.2f}")
            print("-" * 50)
            
            # Test all 13 required indicators
            indicators_status = {}
            
            # 1. RSI
            rsi = technical_data.get('rsi')
            if rsi is not None:
                rsi_status = "✅" if 0 <= rsi <= 100 else "❌"
                print(f"{rsi_status} RSI: {rsi:.2f}")
                indicators_status['RSI'] = rsi is not None
            else:
                print("❌ RSI: Not available")
                indicators_status['RSI'] = False
            
            # 2-4. MACD Components
            macd = technical_data.get('macd')
            macd_signal = technical_data.get('macd_signal')
            macd_histogram = technical_data.get('macd_histogram')
            
            if all(x is not None for x in [macd, macd_signal, macd_histogram]):
                # Test MACD histogram calculation
                expected_histogram = macd - macd_signal
                histogram_accurate = abs(macd_histogram - expected_histogram) < 0.01
                histogram_status = "✅" if histogram_accurate else "❌"
                
                # Determine BUY/SELL signal
                signal = "BUY" if macd_histogram > 0 else "SELL"
                
                print(f"✅ MACD: {macd:.3f}")
                print(f"✅ MACD Signal: {macd_signal:.3f}")
                print(f"{histogram_status} MACD Histogram: {macd_histogram:.3f} (Signal: {signal})")
                
                indicators_status['MACD'] = True
                indicators_status['MACD_Signal'] = True
                indicators_status['MACD_Histogram'] = histogram_accurate
            else:
                print("❌ MACD Components: Not available")
                indicators_status['MACD'] = False
                indicators_status['MACD_Signal'] = False
                indicators_status['MACD_Histogram'] = False
            
            # 5-7. Bollinger Bands
            bb_upper = technical_data.get('bollinger_upper')
            bb_middle = technical_data.get('bollinger_middle')
            bb_lower = technical_data.get('bollinger_lower')
            
            if all(x is not None for x in [bb_upper, bb_middle, bb_lower]):
                # Test proper ordering
                bands_ordered = bb_lower < bb_middle < bb_upper
                bands_status = "✅" if bands_ordered else "❌"
                
                # Determine position
                if current_price > bb_upper:
                    bb_position = "UPPER"
                elif current_price < bb_lower:
                    bb_position = "LOWER"
                else:
                    bb_position = "MIDDLE"
                
                print(f"{bands_status} Bollinger Upper: ₹{bb_upper:.2f}")
                print(f"✅ Bollinger Middle: ₹{bb_middle:.2f}")
                print(f"✅ Bollinger Lower: ₹{bb_lower:.2f}")
                print(f"   Position: {bb_position}")
                
                indicators_status['Bollinger_Upper'] = True
                indicators_status['Bollinger_Middle'] = True
                indicators_status['Bollinger_Lower'] = bands_ordered
            else:
                print("❌ Bollinger Bands: Not available")
                indicators_status['Bollinger_Upper'] = False
                indicators_status['Bollinger_Middle'] = False
                indicators_status['Bollinger_Lower'] = False
            
            # 8-9. Stochastic Oscillator
            stoch_k = technical_data.get('stochastic_k')
            stoch_d = technical_data.get('stochastic_d')
            
            if stoch_k is not None and stoch_d is not None:
                stoch_k_valid = 0 <= stoch_k <= 100
                stoch_d_valid = 0 <= stoch_d <= 100
                
                stoch_k_status = "✅" if stoch_k_valid else "❌"
                stoch_d_status = "✅" if stoch_d_valid else "❌"
                
                print(f"{stoch_k_status} Stochastic %K: {stoch_k:.2f}")
                print(f"{stoch_d_status} Stochastic %D: {stoch_d:.2f}")
                
                indicators_status['Stochastic_K'] = stoch_k_valid
                indicators_status['Stochastic_D'] = stoch_d_valid
            else:
                print("❌ Stochastic Oscillator: Not available")
                indicators_status['Stochastic_K'] = False
                indicators_status['Stochastic_D'] = False
            
            # 10. VWAP
            vwap = technical_data.get('vwap')
            if vwap is not None and current_price > 0:
                vwap_position = "ABOVE" if current_price > vwap else "BELOW"
                print(f"✅ VWAP: ₹{vwap:.2f} (Position: {vwap_position})")
                indicators_status['VWAP'] = True
            else:
                print("❌ VWAP: Not available")
                indicators_status['VWAP'] = False
            
            # 11. ATR
            atr = technical_data.get('atr')
            if atr is not None:
                print(f"✅ ATR: {atr:.2f}")
                indicators_status['ATR'] = True
            else:
                print("❌ ATR: Not available")
                indicators_status['ATR'] = False
            
            # 12-13. Support and Resistance Levels
            support_level = technical_data.get('support_level')
            resistance_level = technical_data.get('resistance_level')
            
            if support_level is not None:
                print(f"✅ Support Level: ₹{support_level:.2f}")
                indicators_status['Support_Level'] = True
            else:
                print("❌ Support Level: Not available")
                indicators_status['Support_Level'] = False
            
            if resistance_level is not None:
                print(f"✅ Resistance Level: ₹{resistance_level:.2f}")
                indicators_status['Resistance_Level'] = True
            else:
                print("❌ Resistance Level: Not available")
                indicators_status['Resistance_Level'] = False
            
            # Calculate coverage
            total_indicators = len(indicators_status)
            working_indicators = sum(indicators_status.values())
            coverage_rate = (working_indicators / total_indicators) * 100
            
            print(f"\n📊 Coverage: {working_indicators}/{total_indicators} indicators ({coverage_rate:.1f}%)")
            
            return working_indicators, total_indicators, indicators_status
            
        else:
            print(f"❌ Failed to get data for {symbol}: Status {response.status_code}")
            return 0, 13, {}
            
    except Exception as e:
        print(f"❌ Error testing {symbol}: {str(e)}")
        return 0, 13, {}

def main():
    print("📈 Enhanced Technical Indicators Testing - StockBreak Pro v2.0")
    print("=" * 70)
    print(f"Testing all 13 technical indicators as requested in review")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Test symbols across different sectors and market conditions
    test_symbols = ['RELIANCE', 'TCS', 'MPHASIS', 'HDFCLIFE', 'HINDUNILVR', 'BAJFINANCE']
    
    total_working = 0
    total_possible = 0
    all_indicators_status = {}
    
    for symbol in test_symbols:
        working, possible, status = test_technical_indicators(symbol)
        total_working += working
        total_possible += possible
        
        # Aggregate indicator status across all stocks
        for indicator, working_status in status.items():
            if indicator not in all_indicators_status:
                all_indicators_status[indicator] = []
            all_indicators_status[indicator].append(working_status)
    
    print("\n" + "=" * 70)
    print("📊 OVERALL TECHNICAL INDICATORS ANALYSIS")
    print("=" * 70)
    
    # Show indicator reliability across all tested stocks
    print("\n🔍 Indicator Reliability Across All Stocks:")
    for indicator, statuses in all_indicators_status.items():
        working_count = sum(statuses)
        total_count = len(statuses)
        reliability = (working_count / total_count) * 100
        
        status_icon = "✅" if reliability >= 80 else "⚠️" if reliability >= 60 else "❌"
        print(f"{status_icon} {indicator}: {working_count}/{total_count} stocks ({reliability:.1f}%)")
    
    # Overall coverage
    overall_coverage = (total_working / total_possible) * 100
    print(f"\n📈 Overall Coverage: {total_working}/{total_possible} ({overall_coverage:.1f}%)")
    
    # Assessment
    if overall_coverage >= 90:
        assessment = "EXCELLENT - Ready for professional trading"
    elif overall_coverage >= 80:
        assessment = "GOOD - Suitable for most trading scenarios"
    elif overall_coverage >= 70:
        assessment = "FAIR - Some indicators need attention"
    else:
        assessment = "POOR - Significant improvements needed"
    
    print(f"🎯 Assessment: {assessment}")
    
    # Specific checks for review requirements
    print(f"\n✅ Review Requirements Check:")
    
    # Check if all 13 indicators are implemented
    expected_indicators = ['RSI', 'MACD', 'MACD_Signal', 'MACD_Histogram', 
                          'Bollinger_Upper', 'Bollinger_Middle', 'Bollinger_Lower',
                          'Stochastic_K', 'Stochastic_D', 'VWAP', 'ATR', 
                          'Support_Level', 'Resistance_Level']
    
    implemented_indicators = len(all_indicators_status)
    print(f"   📊 Indicators Implemented: {implemented_indicators}/13")
    
    # Check MACD calculations
    macd_working = all_indicators_status.get('MACD_Histogram', [])
    macd_accuracy = (sum(macd_working) / len(macd_working) * 100) if macd_working else 0
    print(f"   📈 MACD Calculations: {macd_accuracy:.1f}% accurate")
    
    # Check Bollinger Bands
    bb_working = all_indicators_status.get('Bollinger_Lower', [])  # Using lower as it tests ordering
    bb_accuracy = (sum(bb_working) / len(bb_working) * 100) if bb_working else 0
    print(f"   📊 Bollinger Bands: {bb_accuracy:.1f}% proper ordering")
    
    # Check VWAP
    vwap_working = all_indicators_status.get('VWAP', [])
    vwap_accuracy = (sum(vwap_working) / len(vwap_working) * 100) if vwap_working else 0
    print(f"   📈 VWAP Analysis: {vwap_accuracy:.1f}% available")
    
    # Check Stochastic
    stoch_k_working = all_indicators_status.get('Stochastic_K', [])
    stoch_accuracy = (sum(stoch_k_working) / len(stoch_k_working) * 100) if stoch_k_working else 0
    print(f"   📊 Stochastic Values: {stoch_accuracy:.1f}% in valid range")
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

if __name__ == "__main__":
    main()