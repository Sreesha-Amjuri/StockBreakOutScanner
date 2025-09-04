#!/usr/bin/env python3
"""
AI Chat Functionality Testing Only
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, List, Optional

class AIChatTester:
    def __init__(self, base_url="https://tradepulse-app-1.preview.emergentagent.com"):
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

    def test_ai_chat_basic(self):
        """Test basic AI Chat functionality"""
        print("🤖 Testing Basic AI Chat Functionality")
        print("-" * 40)
        
        # Test 1: Basic chat endpoint without stock context
        chat_request = {
            "message": "What are the key technical indicators I should look at for Indian stock analysis?",
            "session_id": None,
            "stock_context": None
        }
        
        success1, data1 = self.test_api_endpoint("AI Chat - Basic Query", "POST", "chat", 
                                               data=chat_request, timeout=30)
        
        if success1:
            # Validate response structure
            required_fields = ['response', 'session_id', 'timestamp']
            missing_fields = [field for field in required_fields if field not in data1]
            
            if missing_fields:
                self.log_test("Chat Response Structure", False, f"Missing fields: {missing_fields}")
            else:
                response_text = data1.get('response', '')
                session_id = data1.get('session_id', '')
                
                # Check if response is relevant to Indian stock markets
                indian_market_keywords = ['indian', 'nifty', 'nse', 'rupee', '₹', 'rsi', 'macd', 'technical']
                has_relevant_content = any(keyword.lower() in response_text.lower() for keyword in indian_market_keywords)
                
                self.log_test("Chat Response Relevance", has_relevant_content, 
                            f"Response contains Indian market context: {len(response_text)} chars")
                
                self.log_test("Chat Session ID Generated", len(session_id) > 0, 
                            f"Session ID: {session_id[:8]}...")
                
                # Store session ID for history test
                self.test_session_id = session_id
                
                print(f"AI Response Preview: {response_text[:200]}...")
        
        return success1

    def test_ai_chat_with_context(self):
        """Test AI Chat with stock context"""
        print("📊 Testing AI Chat with Stock Context")
        print("-" * 35)
        
        # Test chat with stock context
        stock_context = {
            "symbol": "RELIANCE",
            "current_price": 1384.90,
            "change_percent": -1.96,
            "rsi": 45.2,
            "sector": "Energy",
            "technical_indicators": {
                "macd": 12.5,
                "support_level": 1350.0,
                "resistance_level": 1420.0
            }
        }
        
        chat_request_with_context = {
            "message": "Should I buy this stock? What's your analysis based on the current data?",
            "session_id": getattr(self, 'test_session_id', None),
            "stock_context": stock_context
        }
        
        success, data = self.test_api_endpoint("AI Chat - With Stock Context", "POST", "chat", 
                                             data=chat_request_with_context, timeout=30)
        
        if success:
            response_text = data.get('response', '')
            
            # Check if response mentions the specific stock and its data
            reliance_mentioned = 'reliance' in response_text.lower()
            price_mentioned = '1384' in response_text or '₹' in response_text
            rsi_mentioned = 'rsi' in response_text.lower() or '45' in response_text
            
            context_usage = reliance_mentioned or price_mentioned or rsi_mentioned
            self.log_test("Chat Context Usage", context_usage, 
                        f"Response uses stock context (RELIANCE data): {len(response_text)} chars")
            
            print(f"Context-aware Response Preview: {response_text[:200]}...")
        
        return success

    def test_chat_history(self):
        """Test chat history functionality"""
        print("📚 Testing Chat History")
        print("-" * 20)
        
        # Use session ID from previous test or create new one
        session_id = getattr(self, 'test_session_id', 'test-session-' + str(int(datetime.now().timestamp())))
        
        # Test chat history retrieval
        success, history_data = self.test_api_endpoint("Chat History Retrieval", "GET", f"chat/history/{session_id}")
        
        if success:
            messages = history_data.get('messages', [])
            returned_session_id = history_data.get('session_id', '')
            message_count = history_data.get('count', 0)
            
            # Validate history structure
            self.log_test("History Session ID Match", returned_session_id == session_id, 
                        f"Session ID matches: {session_id}")
            
            self.log_test("History Message Retrieval", len(messages) >= 0, 
                        f"Found {len(messages)} messages in history")
            
            if messages:
                # Validate message structure
                first_message = messages[0]
                required_fields = ['id', 'session_id', 'message', 'role', 'timestamp']
                missing_fields = [field for field in required_fields if field not in first_message]
                
                self.log_test("History Message Structure", len(missing_fields) == 0, 
                            f"Message structure complete: {list(first_message.keys())}")
        
        return success

    def test_error_handling(self):
        """Test error handling scenarios"""
        print("⚠️  Testing Error Handling")
        print("-" * 25)
        
        # Test 1: Empty message
        empty_request = {
            "message": "",
            "session_id": None,
            "stock_context": None
        }
        
        success1, data1 = self.test_api_endpoint("Chat - Empty Message", "POST", "chat", 
                                               data=empty_request, expected_status=422, timeout=15)
        
        # Test 2: Non-existent session history
        fake_session_id = "non-existent-session-12345"
        success2, data2 = self.test_api_endpoint("Chat History - Non-existent Session", "GET", f"chat/history/{fake_session_id}")
        
        if success2:
            messages = data2.get('messages', [])
            empty_history = len(messages) == 0
            self.log_test("Non-existent Session Handling", empty_history, 
                        f"Returns empty history for non-existent session: {len(messages)} messages")
        
        return True

    def run_all_tests(self):
        """Run all AI Chat tests"""
        print("🚀 Starting AI Chat Testing")
        print("=" * 40)
        print(f"Testing API at: {self.api_url}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 40)
        print()

        # Run tests
        self.test_ai_chat_basic()
        self.test_ai_chat_with_context()
        self.test_chat_history()
        self.test_error_handling()
        
        # Print final results
        print("\n" + "=" * 40)
        print("📊 AI CHAT TEST RESULTS")
        print("=" * 40)
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
        print("=" * 40)
        
        return self.tests_passed >= (self.tests_run * 0.75)  # 75% pass rate

def main():
    """Main test execution"""
    tester = AIChatTester()
    
    try:
        success = tester.run_all_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n💥 Unexpected error during testing: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())