# test_deployed_api.py - Test the deployed API on Render

import requests
import json

# Your deployed API URL
API_BASE_URL = "https://voicebot-backend-6hfd.onrender.com"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🔍 Testing Deployed Health Endpoint...")
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
    """Test the deployed API"""
    print("🚀 Testing DEPLOYED Sarathi Voice Bot API")
    print("=" * 50)
    print(f"API URL: {API_BASE_URL}")
    print("=" * 50)
    
    # Test 1: Health check
    health_ok = test_health_endpoint()
    
    if not health_ok:
        print("❌ Health check failed on deployed API!")
        return
    
    print("✅ Deployed API health check passed!")
    
    # Test 2: Voice commands
    test_commands = [
        "scroll down",
        "go to about section", 
        "navigate to services",
        "read the contact info",
        "scroll to top"
    ]
    
    for command in test_commands:
        success = test_voice_command(command)
        if success:
            print("✅ Command processed successfully!")
        else:
            print("❌ Command processing failed!")
    
    print("\n🎉 Deployed API testing completed!")
    print("\n💡 Your API is ready for React integration!")
    print(f"API URL to use in React: {API_BASE_URL}")

if __name__ == "__main__":
    main()
