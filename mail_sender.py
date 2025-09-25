import smtplib
import os
from dotenv import load_dotenv

# Load environment variables once when the module is imported
load_dotenv()
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
MAIL_APP_PASSWORD = os.getenv('MAIL_APP_PASSWORD')

def send_emergency_email(location=None):
    """
    Sends an emergency email with optional user location.
    
    Args:
        location (dict): A dictionary containing 'latitude' and 'longitude'.
    
    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    if not all([SENDER_EMAIL, RECEIVER_EMAIL, MAIL_APP_PASSWORD]):
        print("Error: Email credentials are not set in the .env file.")
        return False

    try:
        subject = "EMERGENCY HELP REQUEST - Sarathi User"
        
        # Create a more detailed message
        message_body = "This is an automated emergency request from a Sarathi user.\n\n"
        
        if location and 'latitude' in location and 'longitude' in location:
            lat = location['latitude']
            lon = location['longitude']
            maps_link = f"https://www.google.com/maps?q={lat},{lon}"
            message_body += f"The user's last known location is:\n"
            message_body += f"Latitude: {lat}\n"
            message_body += f"Longitude: {lon}\n"
            message_body += f"View on Google Maps: {maps_link}\n"
        else:
            message_body += "User location was not available or permission was denied.\n"

        text = f"Subject: {subject}\n\n{message_body}"

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, MAIL_APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
            print("Emergency email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False