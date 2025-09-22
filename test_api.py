# test_api.py - Test script to verify Flask API is working locally

import requests
import json

# Configuration
API_BASE_URL = "http://localhost:5000"  # Change this when testing deployed version

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🔍 Testing Health Endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error testing health endpoint: {e}")
        return False

def test_voice_command(command_text):
    """Test the voice command processing endpoint"""
    print(f"\n🔍 Testing Voice Command: '{command_text}'")
    try:
        payload = {
            "text": command_text
        }
        response = requests.post(
            f"{API_BASE_URL}/process-command",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error testing voice command: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting API Tests for Sarathi Voice Bot")
    print("=" * 50)
    
    # Test 1: Health check
    health_ok = test_health_endpoint()
    
    if not health_ok:
        print("❌ Health check failed! Make sure the Flask app is running.")
        print("Run: python app.py")
        return
    
    print("✅ Health check passed!")
    
    # Test 2: Various voice commands
    test_commands = [
        "scroll down",
        "go to about section", 
        "read the services",
        "navigate to contact",
        "scroll to top",
        "hello there"  # This should return unknown/error
    ]
    
    for command in test_commands:
        success = test_voice_command(command)
        if success:
            print("✅ Command processed successfully!")
        else:
            print("❌ Command processing failed!")
    
    print("\n🎉 All tests completed!")
    print("\n💡 Next Steps:")
    print("1. If tests pass, your API is working locally")
    print("2. Deploy to Render using the provided configuration")
    print("3. Update API_BASE_URL in your React frontend")

if __name__ == "__main__":
    main()
