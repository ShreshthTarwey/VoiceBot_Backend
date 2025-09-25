import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Load environment variables
load_dotenv()
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

def send_emergency_email(location=None):
    """
    Sends an emergency email using the SendGrid API.
    
    Args:
        location (dict): A dictionary containing 'latitude' and 'longitude'.
    
    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    if not all([SENDER_EMAIL, RECEIVER_EMAIL, SENDGRID_API_KEY]):
        print("Error: SendGrid credentials are not set in the .env file.")
        return False

    subject = "EMERGENCY HELP REQUEST - Sarathi User"
    
    # Create a more detailed message with HTML for a clickable link
    message_body = "<h3>This is an automated emergency request from a Sarathi user.</h3>"
    
    if location and 'latitude' in location and 'longitude' in location:
        lat = location['latitude']
        lon = location['longitude']
        maps_link = f"http://www.google.com/maps/place/{lat},{lon}"
        message_body += f"<p>The user's last known location is:</p>"
        message_body += f"<ul><li>Latitude: {lat}</li><li>Longitude: {lon}</li></ul>"
        message_body += f'<p><strong><a href="{maps_link}">View on Google Maps</a></strong></p>'
    else:
        message_body += "<p>User location was not available or permission was denied.</p>"

    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=RECEIVER_EMAIL,
        subject=subject,
        html_content=message_body
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        # A successful send will have a 2xx status code
        if 200 <= response.status_code < 300:
            print(f"Emergency email sent successfully! Status Code: {response.status_code}")
            return True
        else:
            print(f"Failed to send email. Status Code: {response.status_code}")
            print(response.body)
            return False
    except Exception as e:
        print(f"An error occurred with SendGrid: {e}")
        return False