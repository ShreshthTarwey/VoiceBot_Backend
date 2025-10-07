import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def test_send_email():
    """
    A standalone script to test sending an email via the SendGrid API.
    It loads credentials from the .env file and prints detailed results.
    """
    print("--- Starting SendGrid Email Test ---")

    # 1. Load environment variables from .env file
    load_dotenv()
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    api_key = os.getenv('SENDGRID_API_KEY')

    # 2. Check if all required variables are present
    print(f"Loaded Sender Email: {sender_email}")
    print(f"Loaded Receiver Email: {receiver_email}")
    print(f"Loaded API Key: {'Yes' if api_key else 'No'}") # Don't print the key itself for security

    if not all([sender_email, receiver_email, api_key]):
        print("\n❌ ERROR: One or more required environment variables (SENDER_EMAIL, RECEIVER_EMAIL, SENDGRID_API_KEY) are missing from your .env file.")
        print("--- Test Failed ---")
        return

    # 3. Construct the email message
    message = Mail(
        from_email=sender_email,
        to_emails=receiver_email,
        subject="[Sarathi Test] SendGrid API Test",
        html_content="""
            <h3>This is a test email from the Sarathi Voice Bot backend.</h3>
            <p>If you are receiving this, it means your SendGrid API key and sender verification are configured correctly.</p>
        """
    )

    # 4. Try to send the email and print detailed results
    try:
        print("\nAttempting to connect to SendGrid and send email...")
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)

        # Print the full response from SendGrid for debugging
        print("\n--- SendGrid Response ---")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.body}")
        print(f"Response Headers: {response.headers}")
        print("------------------------")

        if 200 <= response.status_code < 300:
            print("\n✅ SUCCESS: Email sent successfully! Check the receiver's inbox.")
            print("This confirms your API key and sender verification are working.")
        else:
            print(f"\n❌ FAILED: SendGrid returned a non-success status code ({response.status_code}).")
            print("The 'Response Body' above likely contains the specific reason for the failure (e.g., 'permission denied').")

    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: An exception occurred while trying to send the email.")
        print(f"   Error Details: {e}")
        print("   This could be due to an invalid API key format, a network issue, or a problem with the sendgrid library.")
    
    print("\n--- Test Finished ---")


if __name__ == "__main__":
    test_send_email()