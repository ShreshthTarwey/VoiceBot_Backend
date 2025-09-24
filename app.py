# # app.py - Main Flask Application for Sarathi Voice Bot

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# import json
# import google.generativeai as genai
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)  # Enable CORS for React frontend to access this API

# # Configure Gemini AI
# genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
# model = genai.GenerativeModel('gemini-1.5-flash')

# # Health check endpoint
# @app.route('/health', methods=['GET'])
# def health_check():
#     """
#     Simple health check to verify the API is working
#     Returns: JSON response confirming API status
#     """
#     return jsonify({
#         "status": "healthy",
#         "message": "Sarathi Voice Bot API is running!",
#         "timestamp": "2025-09-22"
#     })

# # Main voice command processing endpoint
# @app.route('/process-command', methods=['POST'])
# def process_voice_command():
#     """
#     Main endpoint that receives text from frontend and processes it with Gemini AI
    
#     Expected Input:
#     {
#         "text": "scroll down to about section"
#     }
    
#     Returns:
#     {
#         "action": "scroll",
#         "direction": "down", 
#         "target": "about",
#         "original_text": "scroll down to about section"
#     }
#     """
#     try:
#         # Get JSON data from request
#         data = request.get_json()
        
#         # Validate input
#         if not data or 'text' not in data:
#             return jsonify({
#                 "error": "Missing 'text' field in request"
#             }), 400
        
#         user_text = data['text'].strip()
        
#         if not user_text:
#             return jsonify({
#                 "error": "Text field is empty"
#             }), 400
        
#         # Process with Gemini AI
#         response = analyze_with_gemini(user_text)
        
#         return jsonify(response)
    
#     except Exception as e:
#         return jsonify({
#             "error": f"Internal server error: {str(e)}"
#         }), 500
    
# def analyze_with_gemini(user_text):
#     """
#     Refined prompt for clearer intent recognition and better structured JSON responses.
#     """
#     prompt = f"""
# You are a smart voice assistant for the accessibility website "Sarathi". The website has these sections: Header, About, Services, Contact, Footer.

# The user said: "{user_text}"

# Analyze this user command carefully and return a single valid JSON object ONLY (no extra explanation or notes) with the following fields:

# - action: One of ["scroll", "navigate", "read", "unknown"]
# - target: The specific website section if applicable (one of "about", "services", "contact", "header", "footer") or null if not applicable
# - direction: For scroll actions, one of ["up", "down", "top", "bottom"] or null if not applicable
# - original_text: The exact original user input

# Instructions:
# - If the user command is a scrolling action, set action to "scroll" and direction accordingly.  
# Examples:  
#     "scroll down" -> {{"action": "scroll", "direction": "down", "target": null}}  
#     "scroll to top" -> {{"action": "scroll", "direction": "top", "target": null}}

# - If the user command is about navigating to a section, set action to "navigate" and target accordingly.  
# Examples:  
#     "go to about section" -> {{"action": "navigate", "target": "about", "direction": null}}  
#     "navigate to contact" -> {{"action": "navigate", "target": "contact", "direction": null}}

# - If the user command is about reading content aloud, set action to "read" and target accordingly.  
# Examples:  
#     "read the services" -> {{"action": "read", "target": "services", "direction": null}}  
#     "read contact info" -> {{"action": "read", "target": "contact", "direction": null}}

# - If the command is ambiguous, invalid, or not understood, set action to "unknown" and target/direction to null.

# Make sure the JSON output is properly formed, compliant with JSON syntax, and contains no trailing commas or comments. Return ONLY the JSON object, nothing else.
# """

#     try:
#         response = model.generate_content(prompt)
#         ai_text = response.text.strip()

#         # Debug print to verify AI output
#         print(f"AI Response: {ai_text}")

#         gemini_response = json.loads(ai_text)
#         gemini_response["original_text"] = user_text
#         return gemini_response
#     except json.JSONDecodeError:
#         return {
#             "action": "unknown",
#             "target": None,
#             "direction": None,
#             "original_text": user_text,
#             "error": "Could not parse AI response"
#         }
#     except Exception as e:
#         return {
#             "action": "error",
#             "target": None,
#             "direction": None,
#             "original_text": user_text,
#             "error": str(e)
#         }

# # def analyze_with_gemini(user_text):
#     """
#     Hybrid approach: AI understanding + keyword extraction
#     """
#     # First, let Gemini AI understand the user's intent
#     prompt = f"""
# You are a voice assistant for an accessibility website called "Sarathi".
# The website has sections: Header, About, Services, Contact, Footer.

# The user said: "{user_text}"

# Analyze what the user wants to do and respond in simple English describing the action.

# Examples:
# - If user wants to scroll down: "The user wants to scroll down the page"
# - If user wants to go to about section: "The user wants to navigate to the about section"
# - If user wants to read services: "The user wants to read the services section"
# - If user wants to go to top: "The user wants to scroll to the top of the page"
# - If unclear: "The user's command is not clear"

# Respond in simple, clear English describing the intended action.
# """
    
#     try:
#         # Get AI analysis
#         response = model.generate_content(prompt)
#         ai_response = response.text.strip().lower()
        
#         print(f"AI Response: {ai_response}")  # Debug: see what AI says
        
#         # Now extract keywords from AI response
#         return extract_action_from_ai_response(ai_response, user_text)
    
#     except Exception as e:
#         # Fallback to rule-based if AI fails
#         return extract_action_from_user_text(user_text)

# def extract_action_from_ai_response(ai_response, original_text):
#     """
#     Extract structured actions from AI's text response
#     """
#     ai_response = ai_response.lower()
    
#     # Scrolling actions
#     if "scroll down" in ai_response or "scroll downward" in ai_response:
#         return {"action": "scroll", "direction": "down", "target": None, "original_text": original_text}
#     elif "scroll up" in ai_response or "scroll upward" in ai_response:
#         return {"action": "scroll", "direction": "up", "target": None, "original_text": original_text}
#     elif "scroll to top" in ai_response or "go to top" in ai_response or "top of" in ai_response:
#         return {"action": "scroll", "direction": "top", "target": None, "original_text": original_text}
#     elif "scroll to bottom" in ai_response or "bottom of" in ai_response:
#         return {"action": "scroll", "direction": "bottom", "target": None, "original_text": original_text}
    
#     # Navigation actions
#     elif "navigate to about" in ai_response or "go to about" in ai_response or "about section" in ai_response:
#         return {"action": "navigate", "target": "about", "direction": None, "original_text": original_text}
#     elif "navigate to services" in ai_response or "go to services" in ai_response or "services section" in ai_response:
#         return {"action": "navigate", "target": "services", "direction": None, "original_text": original_text}
#     elif "navigate to contact" in ai_response or "go to contact" in ai_response or "contact section" in ai_response:
#         return {"action": "navigate", "target": "contact", "direction": None, "original_text": original_text}
#     elif "navigate to header" in ai_response or "go to header" in ai_response or "header section" in ai_response:
#         return {"action": "navigate", "target": "header", "direction": None, "original_text": original_text}
    
#     # Reading actions
#     elif "read about" in ai_response or "read the about" in ai_response:
#         return {"action": "read", "target": "about", "direction": None, "original_text": original_text}
#     elif "read services" in ai_response or "read the services" in ai_response:
#         return {"action": "read", "target": "services", "direction": None, "original_text": original_text}
#     elif "read contact" in ai_response or "read the contact" in ai_response:
#         return {"action": "read", "target": "contact", "direction": None, "original_text": original_text}
#     elif "read" in ai_response:
#         return {"action": "read", "target": "current", "direction": None, "original_text": original_text}
    
#     # Unknown/unclear
#     else:
#         # Fallback to direct user text analysis
#         return extract_action_from_user_text(original_text)

# def extract_action_from_user_text(user_text):
#     """
#     Fallback: Direct rule-based analysis of user text
#     """
#     user_text = user_text.lower().strip()
    
#     # Same rule-based logic as before (as backup)
#     if "scroll down" in user_text:
#         return {"action": "scroll", "direction": "down", "target": None, "original_text": user_text}
#     elif "scroll up" in user_text:
#         return {"action": "scroll", "direction": "up", "target": None, "original_text": user_text}
#     elif "about" in user_text:
#         return {"action": "navigate", "target": "about", "direction": None, "original_text": user_text}
#     elif "services" in user_text:
#         return {"action": "navigate", "target": "services", "direction": None, "original_text": user_text}
#     elif "contact" in user_text:
#         return {"action": "navigate", "target": "contact", "direction": None, "original_text": user_text}
#     else:
#         return {"action": "unknown", "target": None, "direction": None, "original_text": user_text, "error": "Command not recognized"}

# # def analyze_with_gemini(user_text):
# #     """
# #     Send user text to Gemini AI and get structured command response
    
# #     Args:
# #         user_text (str): The text spoken by user
        
# #     Returns:
# #         dict: Structured command for frontend to execute
# #     """
# #     # Create a detailed prompt for Gemini AI
# #     prompt = f"""
# # You are a JSON response generator for a voice-controlled website called "Sarathi".

# # User command: "{user_text}"

# # Analyze the command and respond with ONLY a valid JSON object (no other text):

# # For scrolling commands like "scroll down", "scroll up", "scroll to top":
# # {{"action": "scroll", "direction": "down", "target": null}}

# # For navigation commands like "go to about", "navigate to services":
# # {{"action": "navigate", "target": "about", "direction": null}}

# # For reading commands like "read the services", "read contact info":
# # {{"action": "read", "target": "services", "direction": null}}

# # Available targets: about, services, contact, header, footer
# # Available directions: up, down, top, bottom

# # Respond with ONLY valid JSON, no explanations or additional text.
# # """
    
# #     try:
# #         response = model.generate_content(prompt)
        
# #         # Parse the JSON response from Gemini
# #         gemini_response = json.loads(response.text.strip())
# #         gemini_response["original_text"] = user_text
        
# #         return gemini_response
    
# #     except json.JSONDecodeError:
# #         # Fallback if Gemini doesn't return valid JSON
# #         return {
# #             "action": "unknown",
# #             "target": None,
# #             "direction": None,
# #             "original_text": user_text,
# #             "error": "Could not understand command"
# #         }
# #     except Exception as e:
# #         return {
# #             "action": "error",
# #             "target": None,
# #             "direction": None,
# #             "original_text": user_text,
# #             "error": str(e)
# #         }


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

# app.py - Main Flask Application for Sarathi Voice Bot

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# import google.generativeai as genai
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)  # Enable CORS for React frontend

# # Configure Gemini AI
# genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
# model = genai.GenerativeModel('gemini-1.5-flash')

# # Health check endpoint
# @app.route('/health', methods=['GET'])
# def health_check():
#     return jsonify({
#         "status": "healthy",
#         "message": "Sarathi Voice Bot API is running!"
#     })

# # Main voice command processing endpoint
# @app.route('/process-command', methods=['POST'])
# def process_voice_command():
#     try:
#         data = request.get_json()
#         if not data or 'text' not in data:
#             return jsonify({"error": "Missing 'text' field in request"}), 400

#         user_text = data['text'].strip()
#         if not user_text:
#             return jsonify({"error": "Text field is empty"}), 400

#         response = analyze_with_gemini(user_text)
#         return jsonify(response)

#     except Exception as e:
#         return jsonify({
#             "error": f"Internal server error: {str(e)}"
#         }), 500

# def analyze_with_gemini(user_text):
#     """
#     Ask Gemini to output a simple English explanation (string),
#     then extract structured action with keyword rules.
#     """
#     prompt = f"""
# You are a smart voice assistant for the accessibility website "Sarathi".
# The website has these sections: Header, About, Services, Contact, Footer.

# The user said: "{user_text}"

# Your task:
# - Carefully analyze the users command.
# - Respond ONLY with one short English sentence describing the action.
# - Do NOT return JSON, lists, or explanations. Just one sentence in plain English.

# Rules for responses:

# 1. **Scrolling actions**
#    - If the user wants to scroll down:
#      → "The user wants to scroll down the page"
#    - If the user wants to scroll up:
#      → "The user wants to scroll up the page"
#    - If the user wants to scroll to the top:
#      → "The user wants to scroll to the top of the page"
#    - If the user wants to scroll to the bottom:
#      → "The user wants to scroll to the bottom of the page"

# 2. **Navigation actions**
#    - If the user wants to go to a section (about, services, contact, header, footer):
#      → "The user wants to navigate to the about section"
#      → "The user wants to navigate to the services section"
#      → "The user wants to navigate to the contact section"
#      → "The user wants to navigate to the header section"
#      → "The user wants to navigate to the footer section"

# 3. **Reading actions**
#    - If the user wants the bot to read a section aloud:
#      → "The user wants to read the about section"
#      → "The user wants to read the services section"
#      → "The user wants to read the contact section"
#      → "The user wants to read the header section"
#      → "The user wants to read the footer section"
#    - If the user says something like "read this" or "read here":
#      → "The user wants to read the current section"

# 4. **Unclear actions**
#    - If the command cannot be understood:
#      → "The user's command is not clear"

# Important:
# - Use the exact sentence formats above.
# - Do not invent new words, synonyms, or extra text.
# - Always stick to one clear sentence.
# """


#     try:
#         response = model.generate_content(prompt)
#         ai_response = response.text.strip()
#         print(f"AI Response: {ai_response}")  # Debug

#         return extract_action_from_ai_response(ai_response, user_text)

#     except Exception as e:
#         return extract_action_from_user_text(user_text)

# def extract_action_from_ai_response(ai_response, original_text):
#     ai_response = ai_response.lower()

#     # Scrolling actions
#     if "scroll down" in ai_response:
#         return {"action": "scroll", "direction": "down", "target": None, "original_text": original_text}
#     elif "scroll up" in ai_response:
#         return {"action": "scroll", "direction": "up", "target": None, "original_text": original_text}
#     elif "scroll to top" in ai_response or "top of" in ai_response:
#         return {"action": "scroll", "direction": "top", "target": None, "original_text": original_text}
#     elif "scroll to bottom" in ai_response or "bottom of" in ai_response:
#         return {"action": "scroll", "direction": "bottom", "target": None, "original_text": original_text}

#     # 👉 Reading actions FIRST (before navigation)
#     elif "read" in ai_response and "about" in ai_response:
#         return {"action": "read", "target": "about", "direction": None, "original_text": original_text}
#     elif "read" in ai_response and "service" in ai_response:
#         return {"action": "read", "target": "services", "direction": None, "original_text": original_text}
#     elif "read" in ai_response and "contact" in ai_response:
#         return {"action": "read", "target": "contact", "direction": None, "original_text": original_text}
#     elif "read" in ai_response and "header" in ai_response:
#         return {"action": "read", "target": "header", "direction": None, "original_text": original_text}
#     elif "read" in ai_response and "footer" in ai_response:
#         return {"action": "read", "target": "footer", "direction": None, "original_text": original_text}
#     elif "read" in ai_response:
#         return {"action": "read", "target": "current", "direction": None, "original_text": original_text}

#     # Navigation actions
#     elif "about" in ai_response and "navigate" in ai_response or "go to about" in ai_response:
#         return {"action": "navigate", "target": "about", "direction": None, "original_text": original_text}
#     elif "service" in ai_response and "navigate" in ai_response or "go to services" in ai_response:
#         return {"action": "navigate", "target": "services", "direction": None, "original_text": original_text}
#     elif "contact" in ai_response and "navigate" in ai_response or "go to contact" in ai_response:
#         return {"action": "navigate", "target": "contact", "direction": None, "original_text": original_text}
#     elif "header" in ai_response and "navigate" in ai_response:
#         return {"action": "navigate", "target": "header", "direction": None, "original_text": original_text}
#     elif "footer" in ai_response and "navigate" in ai_response:
#         return {"action": "navigate", "target": "footer", "direction": None, "original_text": original_text}

#     # Unknown → fallback
#     return extract_action_from_user_text(original_text)



# def extract_action_from_user_text(user_text):
#     user_text = user_text.lower().strip()

#     # Scrolling actions
#     if "scroll down" in user_text:
#         return {"action": "scroll", "direction": "down", "target": None, "original_text": user_text}
#     elif "scroll up" in user_text:
#         return {"action": "scroll", "direction": "up", "target": None, "original_text": user_text}
#     elif "top" in user_text:
#         return {"action": "scroll", "direction": "top", "target": None, "original_text": user_text}
#     elif "bottom" in user_text:
#         return {"action": "scroll", "direction": "bottom", "target": None, "original_text": user_text}

#     # 👉 Reading actions FIRST
#     elif "read about" in user_text:
#         return {"action": "read", "target": "about", "direction": None, "original_text": user_text}
#     elif "read services" in user_text:
#         return {"action": "read", "target": "services", "direction": None, "original_text": user_text}
#     elif "read contact" in user_text or "read the contact info" in user_text:
#         return {"action": "read", "target": "contact", "direction": None, "original_text": user_text}
#     elif "read header" in user_text:
#         return {"action": "read", "target": "header", "direction": None, "original_text": user_text}
#     elif "read footer" in user_text:
#         return {"action": "read", "target": "footer", "direction": None, "original_text": user_text}
#     elif "read" in user_text:
#         return {"action": "read", "target": "current", "direction": None, "original_text": user_text}

#     # Navigation actions
#     elif "about" in user_text:
#         return {"action": "navigate", "target": "about", "direction": None, "original_text": user_text}
#     elif "services" in user_text:
#         return {"action": "navigate", "target": "services", "direction": None, "original_text": user_text}
#     elif "contact" in user_text:
#         return {"action": "navigate", "target": "contact", "direction": None, "original_text": user_text}
#     elif "header" in user_text:
#         return {"action": "navigate", "target": "header", "direction": None, "original_text": user_text}
#     elif "footer" in user_text:
#         return {"action": "navigate", "target": "footer", "direction": None, "original_text": user_text}

#     else:
#         return {"action": "unknown", "target": None, "direction": None, "original_text": user_text}


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json # Import the json library

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configure Gemini AI
try:
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Error configuring Gemini AI: {e}")
    model = None

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Sarathi Voice Bot API is running!"
    })

# Main voice command processing endpoint
@app.route('/process-command', methods=['POST'])
def process_voice_command():
    if not model:
        return jsonify({"error": "Gemini AI model is not configured"}), 500
        
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field in request"}), 400

        user_text = data['text'].strip()
        if not user_text:
            return jsonify({"error": "Text field is empty"}), 400

        # The new function does all the work
        response_json = analyze_and_get_json(user_text)
        
        # Add the original text to the final response for the frontend
        response_json['original_text'] = user_text
        
        return jsonify(response_json)

    except Exception as e:
        return jsonify({
            "error": f"Internal server error: {str(e)}"
        }), 500

def analyze_and_get_json(user_text):
    """
    Asks Gemini to directly output a JSON object based on the user's command.
    Includes robust parsing and a fallback.
    """
    
    # The prompt remains the same
    prompt = f"""
You are a highly intelligent voice command interpreter for a web accessibility application named "Sarathi".
Your ONLY job is to convert the user's spoken command into a structured JSON object.
Do NOT respond with any explanations, pleasantries, or text outside of the JSON object.

The website has the following sections: "header", "about", "services", "contact", "footer".

The JSON object MUST have the following structure:
{{
  "action": "string",
  "target": "string or null",
  "direction": "string or null"
}}

Here are the rules for the JSON values:

1.  **"action"** (string): Must be one of the following:
    - "navigate": For moving to a specific section.
    - "scroll": For scrolling the page.
    - "read": For reading a section's content aloud.
    - "unknown": If the user's intent is unclear.

2.  **"target"** (string or null):
    - If action is "navigate" or "read", this MUST be one of: "header", "about", "services", "contact", "footer".
    - If action is "scroll", this MUST be null.
    - For ambiguous commands like "read this", use "current".

3.  **"direction"** (string or null):
    - If action is "scroll", this MUST be one of: "up", "down", "top", "bottom".
    - Otherwise, it MUST be null.

---
Here are some examples:

User command: "scroll down a little bit"
{{
  "action": "scroll",
  "target": null,
  "direction": "down"
}}

User command: "tell me about the services"
{{
  "action": "read",
  "target": "services",
  "direction": null
}}

User command: "Uhh, I want to go to the contact stuff"
{{
  "action": "navigate",
  "target": "contact",
  "direction": null
}}

User command: "what is the price of gold"
{{
  "action": "unknown",
  "target": null,
  "direction": null
}}
---

Now, analyze the following user command and provide ONLY the JSON response.

User command: "{user_text}"
"""

    # --- THE FIX IS IN THIS TRY/EXCEPT BLOCK ---
    response = None # Initialize response to None
    try:
        response = model.generate_content(prompt)
        ai_response_text = response.text.strip()
        
        if ai_response_text.startswith("```json"):
            ai_response_text = ai_response_text[7:-3].strip()
        
        parsed_json = json.loads(ai_response_text)
        return parsed_json

    except Exception as e:
        # The corrected error logging:
        # It no longer tries to access 'response.text' if 'response' might not exist.
        if response:
             print(f"Error processing Gemini response: {e}\nResponse was: {response.text}")
        else:
             print(f"Failed to get response from Gemini API: {e}")
       
        return {
            "action": "unknown",
            "target": None,
            "direction": None
        }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)