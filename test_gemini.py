import os
import google.generativeai as genai
from dotenv import load_dotenv

def test_gemini_connection():
    """
    A simple, standalone script to test the connection to the Google Gemini API.
    It loads the API key from the .env file and attempts a single API call.
    """
    print("--- Starting Google Gemini API Connection Test ---")

    # 1. Load environment variables from your .env file
    try:
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        print(f"Found API Key in .env file: {'Yes' if api_key else 'No'}")
        print(api_key)

        if not api_key:
            print("\n❌ CRITICAL ERROR: 'GEMINI_API_KEY' not found in your .env file.")
            print("   Please ensure the .env file exists in the same folder and contains the correct key.")
            print("--- Test Failed ---")
            return
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: Could not load the .env file. Error: {e}")
        print("--- Test Failed ---")
        return

    # 2. Attempt to configure and call the Gemini API
    try:
        # Configure the library with your key
        print("\n1. Configuring the API with your key...")
        genai.configure(api_key=api_key)

        # Initialize the specific model that was causing errors
        print("2. Initializing the 'gemini-2.5-flash' model...")
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Send a simple, harmless prompt to the API
        print("3. Sending a test prompt to the API...")
        response = model.generate_content("Why is the sky blue? Explain briefly.")

        # 3. If we get here, it worked. Print the response.
        print("\n--- Gemini AI Response ---")
        print(response.text)
        print("--------------------------")
        
        print("\n✅ SUCCESS: The connection to the Gemini API is working correctly!")
        print("This confirms your API key is valid and your 'google-generativeai' library is up-to-date.")

    except Exception as e:
        # 4. If any part of the 'try' block failed, print the exact error.
        print(f"\n❌ FAILED: An error occurred while communicating with the Gemini API.")
        print(f"\n--- ERROR DETAILS ---")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {e}")
        print("---------------------")
        
        print("\n--- LIKELY CAUSE & SOLUTION ---")
        print("The error message '404 models/gemini-1.5-flash is not found' almost always means your 'google-generativeai' library is outdated.")
        print("Please run this command in your activated virtual environment:")
        print("\n   pip install --upgrade google-generativeai\n")
        print("Then, run this test script again.")

    finally:
        print("\n--- Test Finished ---")

if __name__ == "__main__":
    test_gemini_connection()