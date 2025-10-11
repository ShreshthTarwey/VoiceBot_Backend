import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

# Load all environment variables
load_dotenv()
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
RECIPIENT_PHONE_NUMBER = os.getenv('RECIPIENT_PHONE_NUMBER')

# Initialize the Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def _send_email_alert(location_info):
    """Sends an emergency email via SendGrid."""
    subject = "EMERGENCY HELP REQUEST - Sarathi User"
    html_content = f"<h3>This is an automated emergency request from a Sarathi user.</h3>{location_info}"
    
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=RECEIVER_EMAIL,
        subject=subject,
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        if 200 <= response.status_code < 300:
            print("✅ Email alert sent successfully!")
            return True
    except Exception as e:
        print(f"❌ Failed to send email alert: {e}")
    return False

def _send_sms_alert(location_info):
    """Sends an emergency SMS via Twilio."""
    # --- THIS IS THE UPDATED MESSAGE ---
    # We've added emojis and a clear SOS header.
    sms_body = f"🆘 SOS - URGENT ALERT 🆘\n\nEmergency help request from a Sarathi user.\n\n{location_info}"
    # ------------------------------------
    try:
        message = twilio_client.messages.create(
            body=sms_body,
            from_=TWILIO_PHONE_NUMBER,
            to=RECIPIENT_PHONE_NUMBER
        )
        print(f"✅ SMS alert sent successfully! SID: {message.sid}")
        return True
    except Exception as e:
        print(f"❌ Failed to send SMS alert: {e}")
    return False

def send_emergency_alerts(location=None):
    """
    The main function to trigger all emergency alerts (Email and SMS).
    Returns True if at least one alert was sent successfully.
    """
    print("--- Triggering Emergency Alerts ---")
    location_info_text = "User location was not provided or denied."
    location_info_html = "<p>User location was not provided or denied.</p>"

    if location:
        lat = location.get('latitude')
        lon = a=location.get('longitude')
        maps_link = f"http://www.google.com/maps/place/{lat},{lon}"
        location_info_text = f"Last known location: {maps_link}"
        location_info_html = f'<p>Last known location: <strong><a href="{maps_link}">View on Google Maps</a></strong></p>'

    # Send both alerts
    email_sent = _send_email_alert(location_info_html)
    sms_sent = _send_sms_alert(location_info_text)

    # Return True if either one was successful
    return email_sent or sms_sent
