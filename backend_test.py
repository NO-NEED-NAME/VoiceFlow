import requests
import sys
import json
import base64
from datetime import datetime

class VoiceFlowAPITester:
    def __init__(self, base_url="https://speakify-39.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)

            success = response.status_code == expected_status
            details = f"Status: {response.status_code}"
            
            if success:
                try:
                    response_data = response.json()
                    details += f", Response: {json.dumps(response_data, indent=2)[:200]}..."
                except:
                    details += f", Response: {response.text[:200]}..."
            else:
                details += f", Expected: {expected_status}, Response: {response.text[:200]}..."

            self.log_test(name, success, details)
            return success, response.json() if success and response.text else {}

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.log_test(name, False, error_msg)
            return False, {}

    def test_root_endpoint(self):
        """Test API root endpoint"""
        return self.run_test("API Root", "GET", "", 200)

    def test_voices_endpoint(self):
        """Test voices endpoint"""
        success, response = self.run_test("Get Voices", "GET", "voices", 200)
        
        if success:
            # Validate voice structure
            voices = response.get('voices', [])
            expected_voices = ['alloy', 'ash', 'coral', 'echo', 'fable', 'nova', 'onyx', 'sage', 'shimmer']
            
            if len(voices) == 9:
                voice_ids = [v.get('id') for v in voices]
                if all(vid in voice_ids for vid in expected_voices):
                    self.log_test("Voice Structure Validation", True, f"All 9 voices present: {voice_ids}")
                else:
                    self.log_test("Voice Structure Validation", False, f"Missing voices. Found: {voice_ids}")
            else:
                self.log_test("Voice Structure Validation", False, f"Expected 9 voices, got {len(voices)}")
        
        return success, response

    def test_generate_speech_valid(self):
        """Test speech generation with valid input"""
        test_data = {
            "text": "Hello, this is a test of the text-to-speech functionality.",
            "voice": "alloy",
            "speed": 1.0,
            "model": "tts-1"
        }
        
        success, response = self.run_test("Generate Speech - Valid", "POST", "generate-speech", 200, test_data)
        
        if success:
            # Validate response structure
            if 'audio_base64' in response and response['audio_base64']:
                # Try to decode base64 to verify it's valid
                try:
                    audio_data = base64.b64decode(response['audio_base64'])
                    if len(audio_data) > 0:
                        self.log_test("Audio Base64 Validation", True, f"Audio data size: {len(audio_data)} bytes")
                    else:
                        self.log_test("Audio Base64 Validation", False, "Empty audio data")
                except Exception as e:
                    self.log_test("Audio Base64 Validation", False, f"Invalid base64: {str(e)}")
            else:
                self.log_test("Audio Base64 Validation", False, "No audio_base64 in response")
        
        return success, response

    def test_generate_speech_empty_text(self):
        """Test speech generation with empty text"""
        test_data = {
            "text": "",
            "voice": "alloy",
            "speed": 1.0,
            "model": "tts-1"
        }
        
        return self.run_test("Generate Speech - Empty Text", "POST", "generate-speech", 400, test_data)

    def test_generate_speech_long_text(self):
        """Test speech generation with text exceeding 4096 characters"""
        long_text = "A" * 4097  # Exceeds 4096 character limit
        test_data = {
            "text": long_text,
            "voice": "alloy",
            "speed": 1.0,
            "model": "tts-1"
        }
        
        return self.run_test("Generate Speech - Long Text", "POST", "generate-speech", 400, test_data)

    def test_generate_speech_different_voices(self):
        """Test speech generation with different voices"""
        voices_to_test = ["alloy", "echo", "nova", "shimmer"]
        
        for voice in voices_to_test:
            test_data = {
                "text": f"Testing voice {voice}",
                "voice": voice,
                "speed": 1.0,
                "model": "tts-1"
            }
            
            success, _ = self.run_test(f"Generate Speech - Voice {voice}", "POST", "generate-speech", 200, test_data)
            if not success:
                return False
        
        return True

    def test_generate_speech_different_speeds(self):
        """Test speech generation with different speeds"""
        speeds_to_test = [0.25, 1.0, 2.0, 4.0]
        
        for speed in speeds_to_test:
            test_data = {
                "text": f"Testing speed {speed}x",
                "voice": "alloy",
                "speed": speed,
                "model": "tts-1"
            }
            
            success, _ = self.run_test(f"Generate Speech - Speed {speed}x", "POST", "generate-speech", 200, test_data)
            if not success:
                return False
        
        return True

    def test_status_endpoints(self):
        """Test status check endpoints"""
        # Test POST status
        status_data = {"client_name": "test_client"}
        success, response = self.run_test("Create Status Check", "POST", "status", 200, status_data)
        
        if success:
            # Test GET status
            self.run_test("Get Status Checks", "GET", "status", 200)
        
        return success

    def run_all_tests(self):
        """Run all backend API tests"""
        print("🚀 Starting VoiceFlow Backend API Tests")
        print("=" * 50)
        
        # Basic connectivity tests
        self.test_root_endpoint()
        
        # Voice-related tests
        self.test_voices_endpoint()
        
        # Speech generation tests
        self.test_generate_speech_valid()
        self.test_generate_speech_empty_text()
        self.test_generate_speech_long_text()
        self.test_generate_speech_different_voices()
        self.test_generate_speech_different_speeds()
        
        # Status endpoint tests
        self.test_status_endpoints()
        
        # Print summary
        print("\n" + "=" * 50)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return 0
        else:
            print("⚠️  Some tests failed. Check the details above.")
            return 1

def main():
    tester = VoiceFlowAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())