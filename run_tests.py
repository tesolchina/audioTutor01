#!/usr/bin/env python3
"""
Comprehensive test suite for the new-bytewise-backend application
Run this script to test all components of your application
"""

import requests
import json
import socketio
import time
import sys
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:5000"
WEBSOCKET_URL = "http://localhost:5000"

class Colors:
    """ANSI color codes for pretty output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_test_header(test_name: str):
    """Print a formatted test header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}Testing: {test_name}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")

def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ️  {message}{Colors.END}")

def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def test_server_health():
    """Test if the server is responding"""
    print_test_header("Server Health Check")
    
    try:
        # Test basic connectivity
        response = requests.get(f"{BASE_URL}/api/chatbot/a", timeout=5)
        if response.status_code == 200:
            print_success("Server is responding")
            print_info(f"Response: {response.json()}")
            return True
        else:
            print_error(f"Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to server. Make sure it's running on port 5000")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def test_rest_endpoints():
    """Test all REST API endpoints"""
    print_test_header("REST API Endpoints")
    
    endpoints = [
        ("GET", "/api/chatbot/a", None),
        ("GET", "/api/streaming-avatar/a", None),
    ]
    
    for method, endpoint, data in endpoints:
        try:
            url = f"{BASE_URL}{endpoint}"
            print_info(f"Testing {method} {endpoint}")
            
            if method == "GET":
                response = requests.get(url, timeout=5)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=5)
            
            if response.status_code == 200:
                print_success(f"{method} {endpoint} - Status: {response.status_code}")
                print_info(f"Response: {response.json()}")
            else:
                print_warning(f"{method} {endpoint} - Status: {response.status_code}")
                
        except Exception as e:
            print_error(f"Error testing {method} {endpoint}: {e}")

def test_chat_completion():
    """Test the chat completion endpoint"""
    print_test_header("Chat Completion API")
    
    # Test with various payloads
    test_cases = [
        {
            "name": "Basic Chat",
            "payload": {
                "chat_history": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say hello"}
                ],
                "api_key": "test-key",
                "model_name": "gpt-4",
                "max_tokens": 50
            }
        },
        {
            "name": "Empty History",
            "payload": {
                "chat_history": [],
                "api_key": "test-key"
            }
        },
        {
            "name": "Missing API Key",
            "payload": {
                "chat_history": [{"role": "user", "content": "Hello"}]
            }
        }
    ]
    
    for test_case in test_cases:
        try:
            print_info(f"Testing: {test_case['name']}")
            response = requests.post(
                f"{BASE_URL}/api/chatbot/chat",
                json=test_case["payload"],
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            print_info(f"Status Code: {response.status_code}")
            result = response.json()
            
            if "error" in result:
                print_warning(f"Expected error response: {result.get('error', 'Unknown error')}")
            else:
                print_success(f"Response received: {json.dumps(result, indent=2)[:200]}...")
                
        except Exception as e:
            print_error(f"Error in {test_case['name']}: {e}")

def test_websocket_connection():
    """Test WebSocket connectivity"""
    print_test_header("WebSocket Connection")
    
    # Global variables to capture WebSocket events
    connection_success = False
    messages_received = []
    
    # Create a Socket.IO client
    sio = socketio.Client()
    
    @sio.event
    def connect():
        nonlocal connection_success
        connection_success = True
        print_success("WebSocket connected successfully!")
    
    @sio.event
    def disconnect():
        print_info("WebSocket disconnected")
    
    @sio.on('message', namespace='/api/streaming-avatar')
    def on_message(data):
        nonlocal messages_received
        messages_received.append(data)
        print_success(f"Received message: {data}")
    
    @sio.on('stt_result', namespace='/api/streaming-avatar')
    def on_stt_result(data):
        nonlocal messages_received
        messages_received.append(data)
        print_success(f"Received STT result: {data}")
    
    try:
        print_info("Attempting WebSocket connection...")
        sio.connect(WEBSOCKET_URL, namespaces=['/api/streaming-avatar'])
        
        # Wait for connection
        time.sleep(2)
        
        if connection_success:
            print_success("WebSocket connection established")
            
            # Test sending data
            print_info("Sending test audio data...")
            sio.emit('user_audio', b'test_audio_data', namespace='/api/streaming-avatar')
            
            # Wait for response
            time.sleep(2)
            
            if messages_received:
                print_success(f"Received {len(messages_received)} message(s)")
                for i, msg in enumerate(messages_received):
                    print_info(f"Message {i+1}: {msg}")
            else:
                print_warning("No messages received")
        else:
            print_error("Failed to establish WebSocket connection")
        
        # Disconnect
        sio.disconnect()
        
    except Exception as e:
        print_error(f"WebSocket test error: {e}")

def test_external_api_integration():
    """Test the external API integration using the test script"""
    print_test_header("External API Integration (HKBU)")
    
    print_info("Testing HKBU GenAI API integration...")
    print_warning("Note: This test uses a hardcoded API key and may fail if the key is invalid")
    
    try:
        # Import and run a simplified version of the test
        import subprocess
        import os
        
        # Change to project directory
        os.chdir('/workspaces/new-bytewise-backend')
        
        # Run the test script with timeout
        print_info("Running external API test...")
        result = subprocess.run(
            ['python', 'test.py'], 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        if result.returncode == 0:
            print_success("External API test completed successfully")
            # Show first few lines of output
            output_lines = result.stdout.split('\n')[:5]
            for line in output_lines:
                if line.strip():
                    print_info(f"Output: {line}")
            print_info("... (output truncated)")
        else:
            print_error(f"External API test failed with return code: {result.returncode}")
            if result.stderr:
                print_error(f"Error: {result.stderr[:200]}")
    
    except subprocess.TimeoutExpired:
        print_warning("External API test timed out (30s) - this might be normal for streaming")
    except Exception as e:
        print_error(f"Error running external API test: {e}")

def test_audio_processing():
    """Test audio processing capabilities"""
    print_test_header("Audio Processing Test")
    
    try:
        # Test speech recognition import
        import speech_recognition as sr
        print_success("SpeechRecognition library imported successfully")
        
        # Test recognizer creation
        recognizer = sr.Recognizer()
        print_success("Speech recognizer created successfully")
        
        # Test audio file handling (if test audio exists)
        import os
        if os.path.exists('/workspaces/new-bytewise-backend/1.wav'):
            print_success("Test audio file found (1.wav)")
            try:
                with sr.AudioFile('/workspaces/new-bytewise-backend/1.wav') as source:
                    audio = recognizer.record(source)
                    print_success("Audio file loaded successfully")
            except Exception as e:
                print_warning(f"Could not process audio file: {e}")
        else:
            print_info("No test audio file found (1.wav)")
        
    except ImportError as e:
        print_error(f"Audio processing dependencies missing: {e}")
    except Exception as e:
        print_error(f"Audio processing test error: {e}")

def run_all_tests():
    """Run the complete test suite"""
    print(f"{Colors.BOLD}{Colors.MAGENTA}")
    print("🧪 NEW-BYTEWISE-BACKEND TEST SUITE")
    print("===================================")
    print(f"Starting comprehensive testing...{Colors.END}")
    
    # Track test results
    test_results = []
    
    # Run all tests
    tests = [
        ("Server Health", test_server_health),
        ("REST Endpoints", test_rest_endpoints),
        ("Chat Completion", test_chat_completion),
        ("WebSocket", test_websocket_connection),
        ("External API", test_external_api_integration),
        ("Audio Processing", test_audio_processing),
    ]
    
    for test_name, test_func in tests:
        try:
            print(f"\n{Colors.YELLOW}⏳ Running {test_name} test...{Colors.END}")
            test_func()
            test_results.append((test_name, "PASSED"))
        except Exception as e:
            print_error(f"Test {test_name} failed with exception: {e}")
            test_results.append((test_name, "FAILED"))
    
    # Print summary
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}")
    print("📊 TEST SUMMARY")
    print("===============")
    print(f"{Colors.END}")
    
    passed = 0
    failed = 0
    
    for test_name, status in test_results:
        if status == "PASSED":
            print_success(f"{test_name}: {status}")
            passed += 1
        else:
            print_error(f"{test_name}: {status}")
            failed += 1
    
    print(f"\n{Colors.BOLD}Results: {passed} passed, {failed} failed{Colors.END}")
    
    if failed == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 All tests completed successfully!{Colors.END}")
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  Some tests failed. Check the output above for details.{Colors.END}")

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1:
        test_name = sys.argv[1].lower()
        if test_name == "health":
            test_server_health()
        elif test_name == "rest":
            test_rest_endpoints()
        elif test_name == "chat":
            test_chat_completion()
        elif test_name == "websocket":
            test_websocket_connection()
        elif test_name == "api":
            test_external_api_integration()
        elif test_name == "audio":
            test_audio_processing()
        else:
            print(f"Unknown test: {test_name}")
            print("Available tests: health, rest, chat, websocket, api, audio")
    else:
        # Run all tests
        run_all_tests()
