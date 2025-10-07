import os
import google.generativeai as genai
from dotenv import load_dotenv

def list_available_models():
    """
    A standalone script to list all available Gemini models that support
    the 'generateContent' method, based on the current library and API key.
    """
    print("--- Starting Gemini Model Availability Test ---")

    # 1. Load environment variables
    try:
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("\n❌ ERROR: 'GEMINI_API_KEY' not found in your .env file.")
            print("--- Test Failed ---")
            return
        print("Successfully loaded API key from .env file.")
    except Exception as e:
        print(f"\n❌ ERROR: Could not load the .env file. Error: {e}")
        print("--- Test Failed ---")
        return

    # 2. Attempt to configure and list models
    try:
        print("\nConfiguring the API with your key...")
        genai.configure(api_key=api_key)

        print("Fetching available models from the API endpoint...")
        print("-------------------------------------------------")
        
        found_models = False
        # Iterate through all available models
        for m in genai.list_models():
            # The error mentions 'generateContent', so let's check for that
            if 'generateContent' in m.supported_generation_methods:
                print(f"  > Found Model: {m.name}")
                found_models = True
        
        if not found_models:
            print("  > No models supporting 'generateContent' were found.")
        
        print("-------------------------------------------------")
        print("\n✅ SUCCESS: Successfully queried the Google AI endpoint.")

    except Exception as e:
        print(f"\n❌ FAILED: An error occurred while trying to list the models.")
        print(f"   Error Details: {e}")
        print("--- Test Failed ---")

    finally:
        print("\n--- Test Finished ---")

if __name__ == "__main__":
    list_available_models()