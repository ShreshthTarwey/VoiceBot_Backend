# 1. Import the main function from our new alert sender file
from alert_sender import send_emergency_alerts
import time

def run_alert_test():
    """
    A standalone script to test the emergency alert system (Email and SMS).
    """
    print("--- Starting Emergency Alert System Test ---")
    print("\nThis script will attempt to send both an email and an SMS alert.")
    
    # 2. Define mock location data, as if it came from the frontend
    mock_location = {
        "latitude": "23.2599",  # Example: Bhopal
        "longitude": "77.4126"
    }
    
    print(f"\nUsing mock location data: {mock_location}")
    print("Preparing to send alerts...")
    time.sleep(2) # A small delay for dramatic effect

    # 3. Call the main alert function
    success = send_emergency_alerts(location=mock_location)

    # 4. Print the final result
    print("\n--- Test Result ---")
    if success:
        print("✅ SUCCESS: The alert function reported that at least one alert (Email or SMS) was sent successfully.")
        print("Please check your email inbox and your mobile phone for the messages.")
    else:
        print("❌ FAILED: The alert function reported a failure.")
        print("Check the console logs above for specific error messages from SendGrid or Twilio.")
    
    print("\n--- Test Finished ---")


if __name__ == "__main__":
    run_alert_test()

    
