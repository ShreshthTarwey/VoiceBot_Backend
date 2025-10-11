# # # # # # # app.py - Main Flask Application for Sarathi Voice Bot

# # # # # # from flask import Flask, request, jsonify
# # # # # # from flask_cors import CORS
# # # # # # import os
# # # # # # import json
# # # # # # import google.generativeai as genai
# # # # # # from dotenv import load_dotenv

# # # # # # # Load environment variables from .env file
# # # # # # load_dotenv()

# # # # # # # Initialize Flask app
# # # # # # app = Flask(__name__)
# # # # # # CORS(app)  # Enable CORS for React frontend to access this API

# # # # # # # Configure Gemini AI
# # # # # # genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
# # # # # # model = genai.GenerativeModel('gemini-1.5-flash')

# # # # # # # Health check endpoint
# # # # # # @app.route('/health', methods=['GET'])
# # # # # # def health_check():
# # # # # #     """
# # # # # #     Simple health check to verify the API is working
# # # # # #     Returns: JSON response confirming API status
# # # # # #     """
# # # # # #     return jsonify({
# # # # # #         "status": "healthy",
# # # # # #         "message": "Sarathi Voice Bot API is running!",
# # # # # #         "timestamp": "2025-09-22"
# # # # # #     })

# # # # # # # Main voice command processing endpoint
# # # # # # @app.route('/process-command', methods=['POST'])
# # # # # # def process_voice_command():
# # # # # #     """
# # # # # #     Main endpoint that receives text from frontend and processes it with Gemini AI
    
# # # # # #     Expected Input:
# # # # # #     {
# # # # # #         "text": "scroll down to about section"
# # # # # #     }
    
# # # # # #     Returns:
# # # # # #     {
# # # # # #         "action": "scroll",
# # # # # #         "direction": "down", 
# # # # # #         "target": "about",
# # # # # #         "original_text": "scroll down to about section"
# # # # # #     }
# # # # # #     """
# # # # # #     try:
# # # # # #         # Get JSON data from request
# # # # # #         data = request.get_json()
        
# # # # # #         # Validate input
# # # # # #         if not data or 'text' not in data:
# # # # # #             return jsonify({
# # # # # #                 "error": "Missing 'text' field in request"
# # # # # #             }), 400
        
# # # # # #         user_text = data['text'].strip()
        
# # # # # #         if not user_text:
# # # # # #             return jsonify({
# # # # # #                 "error": "Text field is empty"
# # # # # #             }), 400
        
# # # # # #         # Process with Gemini AI
# # # # # #         response = analyze_with_gemini(user_text)
        
# # # # # #         return jsonify(response)
    
# # # # # #     except Exception as e:
# # # # # #         return jsonify({
# # # # # #             "error": f"Internal server error: {str(e)}"
# # # # # #         }), 500
    
# # # # # # def analyze_with_gemini(user_text):
# # # # # #     """
# # # # # #     Refined prompt for clearer intent recognition and better structured JSON responses.
# # # # # #     """
# # # # # #     prompt = f"""
# # # # # # You are a smart voice assistant for the accessibility website "Sarathi". The website has these sections: Header, About, Services, Contact, Footer.

# # # # # # The user said: "{user_text}"

# # # # # # Analyze this user command carefully and return a single valid JSON object ONLY (no extra explanation or notes) with the following fields:

# # # # # # - action: One of ["scroll", "navigate", "read", "unknown"]
# # # # # # - target: The specific website section if applicable (one of "about", "services", "contact", "header", "footer") or null if not applicable
# # # # # # - direction: For scroll actions, one of ["up", "down", "top", "bottom"] or null if not applicable
# # # # # # - original_text: The exact original user input

# # # # # # Instructions:
# # # # # # - If the user command is a scrolling action, set action to "scroll" and direction accordingly.  
# # # # # # Examples:  
# # # # # #     "scroll down" -> {{"action": "scroll", "direction": "down", "target": null}}  
# # # # # #     "scroll to top" -> {{"action": "scroll", "direction": "top", "target": null}}

# # # # # # - If the user command is about navigating to a section, set action to "navigate" and target accordingly.  
# # # # # # Examples:  
# # # # # #     "go to about section" -> {{"action": "navigate", "target": "about", "direction": null}}  
# # # # # #     "navigate to contact" -> {{"action": "navigate", "target": "contact", "direction": null}}

# # # # # # - If the user command is about reading content aloud, set action to "read" and target accordingly.  
# # # # # # Examples:  
# # # # # #     "read the services" -> {{"action": "read", "target": "services", "direction": null}}  
# # # # # #     "read contact info" -> {{"action": "read", "target": "contact", "direction": null}}

# # # # # # - If the command is ambiguous, invalid, or not understood, set action to "unknown" and target/direction to null.

# # # # # # Make sure the JSON output is properly formed, compliant with JSON syntax, and contains no trailing commas or comments. Return ONLY the JSON object, nothing else.
# # # # # # """

# # # # # #     try:
# # # # # #         response = model.generate_content(prompt)
# # # # # #         ai_text = response.text.strip()

# # # # # #         # Debug print to verify AI output
# # # # # #         print(f"AI Response: {ai_text}")

# # # # # #         gemini_response = json.loads(ai_text)
# # # # # #         gemini_response["original_text"] = user_text
# # # # # #         return gemini_response
# # # # # #     except json.JSONDecodeError:
# # # # # #         return {
# # # # # #             "action": "unknown",
# # # # # #             "target": None,
# # # # # #             "direction": None,
# # # # # #             "original_text": user_text,
# # # # # #             "error": "Could not parse AI response"
# # # # # #         }
# # # # # #     except Exception as e:
# # # # # #         return {
# # # # # #             "action": "error",
# # # # # #             "target": None,
# # # # # #             "direction": None,
# # # # # #             "original_text": user_text,
# # # # # #             "error": str(e)
# # # # # #         }

# # # # # # # def analyze_with_gemini(user_text):
# # # # # #     """
# # # # # #     Hybrid approach: AI understanding + keyword extraction
# # # # # #     """
# # # # # #     # First, let Gemini AI understand the user's intent
# # # # # #     prompt = f"""
# # # # # # You are a voice assistant for an accessibility website called "Sarathi".
# # # # # # The website has sections: Header, About, Services, Contact, Footer.

# # # # # # The user said: "{user_text}"

# # # # # # Analyze what the user wants to do and respond in simple English describing the action.

# # # # # # Examples:
# # # # # # - If user wants to scroll down: "The user wants to scroll down the page"
# # # # # # - If user wants to go to about section: "The user wants to navigate to the about section"
# # # # # # - If user wants to read services: "The user wants to read the services section"
# # # # # # - If user wants to go to top: "The user wants to scroll to the top of the page"
# # # # # # - If unclear: "The user's command is not clear"

# # # # # # Respond in simple, clear English describing the intended action.
# # # # # # """
    
# # # # # #     try:
# # # # # #         # Get AI analysis
# # # # # #         response = model.generate_content(prompt)
# # # # # #         ai_response = response.text.strip().lower()
        
# # # # # #         print(f"AI Response: {ai_response}")  # Debug: see what AI says
        
# # # # # #         # Now extract keywords from AI response
# # # # # #         return extract_action_from_ai_response(ai_response, user_text)
    
# # # # # #     except Exception as e:
# # # # # #         # Fallback to rule-based if AI fails
# # # # # #         return extract_action_from_user_text(user_text)

# # # # # # def extract_action_from_ai_response(ai_response, original_text):
# # # # # #     """
# # # # # #     Extract structured actions from AI's text response
# # # # # #     """
# # # # # #     ai_response = ai_response.lower()
    
# # # # # #     # Scrolling actions
# # # # # #     if "scroll down" in ai_response or "scroll downward" in ai_response:
# # # # # #         return {"action": "scroll", "direction": "down", "target": None, "original_text": original_text}
# # # # # #     elif "scroll up" in ai_response or "scroll upward" in ai_response:
# # # # # #         return {"action": "scroll", "direction": "up", "target": None, "original_text": original_text}
# # # # # #     elif "scroll to top" in ai_response or "go to top" in ai_response or "top of" in ai_response:
# # # # # #         return {"action": "scroll", "direction": "top", "target": None, "original_text": original_text}
# # # # # #     elif "scroll to bottom" in ai_response or "bottom of" in ai_response:
# # # # # #         return {"action": "scroll", "direction": "bottom", "target": None, "original_text": original_text}
    
# # # # # #     # Navigation actions
# # # # # #     elif "navigate to about" in ai_response or "go to about" in ai_response or "about section" in ai_response:
# # # # # #         return {"action": "navigate", "target": "about", "direction": None, "original_text": original_text}
# # # # # #     elif "navigate to services" in ai_response or "go to services" in ai_response or "services section" in ai_response:
# # # # # #         return {"action": "navigate", "target": "services", "direction": None, "original_text": original_text}
# # # # # #     elif "navigate to contact" in ai_response or "go to contact" in ai_response or "contact section" in ai_response:
# # # # # #         return {"action": "navigate", "target": "contact", "direction": None, "original_text": original_text}
# # # # # #     elif "navigate to header" in ai_response or "go to header" in ai_response or "header section" in ai_response:
# # # # # #         return {"action": "navigate", "target": "header", "direction": None, "original_text": original_text}
    
# # # # # #     # Reading actions
# # # # # #     elif "read about" in ai_response or "read the about" in ai_response:
# # # # # #         return {"action": "read", "target": "about", "direction": None, "original_text": original_text}
# # # # # #     elif "read services" in ai_response or "read the services" in ai_response:
# # # # # #         return {"action": "read", "target": "services", "direction": None, "original_text": original_text}
# # # # # #     elif "read contact" in ai_response or "read the contact" in ai_response:
# # # # # #         return {"action": "read", "target": "contact", "direction": None, "original_text": original_text}
# # # # # #     elif "read" in ai_response:
# # # # # #         return {"action": "read", "target": "current", "direction": None, "original_text": original_text}
    
# # # # # #     # Unknown/unclear
# # # # # #     else:
# # # # # #         # Fallback to direct user text analysis
# # # # # #         return extract_action_from_user_text(original_text)

# # # # # # def extract_action_from_user_text(user_text):
# # # # # #     """
# # # # # #     Fallback: Direct rule-based analysis of user text
# # # # # #     """
# # # # # #     user_text = user_text.lower().strip()
    
# # # # # #     # Same rule-based logic as before (as backup)
# # # # # #     if "scroll down" in user_text:
# # # # # #         return {"action": "scroll", "direction": "down", "target": None, "original_text": user_text}
# # # # # #     elif "scroll up" in user_text:
# # # # # #         return {"action": "scroll", "direction": "up", "target": None, "original_text": user_text}
# # # # # #     elif "about" in user_text:
# # # # # #         return {"action": "navigate", "target": "about", "direction": None, "original_text": user_text}
# # # # # #     elif "services" in user_text:
# # # # # #         return {"action": "navigate", "target": "services", "direction": None, "original_text": user_text}
# # # # # #     elif "contact" in user_text:
# # # # # #         return {"action": "navigate", "target": "contact", "direction": None, "original_text": user_text}
# # # # # #     else:
# # # # # #         return {"action": "unknown", "target": None, "direction": None, "original_text": user_text, "error": "Command not recognized"}

# # # # # # # def analyze_with_gemini(user_text):
# # # # # # #     """
# # # # # # #     Send user text to Gemini AI and get structured command response
    
# # # # # # #     Args:
# # # # # # #         user_text (str): The text spoken by user
        
# # # # # # #     Returns:
# # # # # # #         dict: Structured command for frontend to execute
# # # # # # #     """
# # # # # # #     # Create a detailed prompt for Gemini AI
# # # # # # #     prompt = f"""
# # # # # # # You are a JSON response generator for a voice-controlled website called "Sarathi".

# # # # # # # User command: "{user_text}"

# # # # # # # Analyze the command and respond with ONLY a valid JSON object (no other text):

# # # # # # # For scrolling commands like "scroll down", "scroll up", "scroll to top":
# # # # # # # {{"action": "scroll", "direction": "down", "target": null}}

# # # # # # # For navigation commands like "go to about", "navigate to services":
# # # # # # # {{"action": "navigate", "target": "about", "direction": null}}

# # # # # # # For reading commands like "read the services", "read contact info":
# # # # # # # {{"action": "read", "target": "services", "direction": null}}

# # # # # # # Available targets: about, services, contact, header, footer
# # # # # # # Available directions: up, down, top, bottom

# # # # # # # Respond with ONLY valid JSON, no explanations or additional text.
# # # # # # # """
    
# # # # # # #     try:
# # # # # # #         response = model.generate_content(prompt)
        
# # # # # # #         # Parse the JSON response from Gemini
# # # # # # #         gemini_response = json.loads(response.text.strip())
# # # # # # #         gemini_response["original_text"] = user_text
        
# # # # # # #         return gemini_response
    
# # # # # # #     except json.JSONDecodeError:
# # # # # # #         # Fallback if Gemini doesn't return valid JSON
# # # # # # #         return {
# # # # # # #             "action": "unknown",
# # # # # # #             "target": None,
# # # # # # #             "direction": None,
# # # # # # #             "original_text": user_text,
# # # # # # #             "error": "Could not understand command"
# # # # # # #         }
# # # # # # #     except Exception as e:
# # # # # # #         return {
# # # # # # #             "action": "error",
# # # # # # #             "target": None,
# # # # # # #             "direction": None,
# # # # # # #             "original_text": user_text,
# # # # # # #             "error": str(e)
# # # # # # #         }


# # # # # # if __name__ == '__main__':
# # # # # #     app.run(host='0.0.0.0', port=5000, debug=True)

# # # # # # app.py - Main Flask Application for Sarathi Voice Bot

# # # # # # from flask import Flask, request, jsonify
# # # # # # from flask_cors import CORS
# # # # # # import os
# # # # # # import google.generativeai as genai
# # # # # # from dotenv import load_dotenv

# # # # # # # Load environment variables from .env file
# # # # # # load_dotenv()

# # # # # # # Initialize Flask app
# # # # # # app = Flask(__name__)
# # # # # # CORS(app)  # Enable CORS for React frontend

# # # # # # # Configure Gemini AI
# # # # # # genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
# # # # # # model = genai.GenerativeModel('gemini-1.5-flash')

# # # # # # # Health check endpoint
# # # # # # @app.route('/health', methods=['GET'])
# # # # # # def health_check():
# # # # # #     return jsonify({
# # # # # #         "status": "healthy",
# # # # # #         "message": "Sarathi Voice Bot API is running!"
# # # # # #     })

# # # # # # # Main voice command processing endpoint
# # # # # # @app.route('/process-command', methods=['POST'])
# # # # # # def process_voice_command():
# # # # # #     try:
# # # # # #         data = request.get_json()
# # # # # #         if not data or 'text' not in data:
# # # # # #             return jsonify({"error": "Missing 'text' field in request"}), 400

# # # # # #         user_text = data['text'].strip()
# # # # # #         if not user_text:
# # # # # #             return jsonify({"error": "Text field is empty"}), 400

# # # # # #         response = analyze_with_gemini(user_text)
# # # # # #         return jsonify(response)

# # # # # #     except Exception as e:
# # # # # #         return jsonify({
# # # # # #             "error": f"Internal server error: {str(e)}"
# # # # # #         }), 500

# # # # # # def analyze_with_gemini(user_text):
# # # # # #     """
# # # # # #     Ask Gemini to output a simple English explanation (string),
# # # # # #     then extract structured action with keyword rules.
# # # # # #     """
# # # # # #     prompt = f"""
# # # # # # You are a smart voice assistant for the accessibility website "Sarathi".
# # # # # # The website has these sections: Header, About, Services, Contact, Footer.

# # # # # # The user said: "{user_text}"

# # # # # # Your task:
# # # # # # - Carefully analyze the users command.
# # # # # # - Respond ONLY with one short English sentence describing the action.
# # # # # # - Do NOT return JSON, lists, or explanations. Just one sentence in plain English.

# # # # # # Rules for responses:

# # # # # # 1. **Scrolling actions**
# # # # # #    - If the user wants to scroll down:
# # # # # #      → "The user wants to scroll down the page"
# # # # # #    - If the user wants to scroll up:
# # # # # #      → "The user wants to scroll up the page"
# # # # # #    - If the user wants to scroll to the top:
# # # # # #      → "The user wants to scroll to the top of the page"
# # # # # #    - If the user wants to scroll to the bottom:
# # # # # #      → "The user wants to scroll to the bottom of the page"

# # # # # # 2. **Navigation actions**
# # # # # #    - If the user wants to go to a section (about, services, contact, header, footer):
# # # # # #      → "The user wants to navigate to the about section"
# # # # # #      → "The user wants to navigate to the services section"
# # # # # #      → "The user wants to navigate to the contact section"
# # # # # #      → "The user wants to navigate to the header section"
# # # # # #      → "The user wants to navigate to the footer section"

# # # # # # 3. **Reading actions**
# # # # # #    - If the user wants the bot to read a section aloud:
# # # # # #      → "The user wants to read the about section"
# # # # # #      → "The user wants to read the services section"
# # # # # #      → "The user wants to read the contact section"
# # # # # #      → "The user wants to read the header section"
# # # # # #      → "The user wants to read the footer section"
# # # # # #    - If the user says something like "read this" or "read here":
# # # # # #      → "The user wants to read the current section"

# # # # # # 4. **Unclear actions**
# # # # # #    - If the command cannot be understood:
# # # # # #      → "The user's command is not clear"

# # # # # # Important:
# # # # # # - Use the exact sentence formats above.
# # # # # # - Do not invent new words, synonyms, or extra text.
# # # # # # - Always stick to one clear sentence.
# # # # # # """


# # # # # #     try:
# # # # # #         response = model.generate_content(prompt)
# # # # # #         ai_response = response.text.strip()
# # # # # #         print(f"AI Response: {ai_response}")  # Debug

# # # # # #         return extract_action_from_ai_response(ai_response, user_text)

# # # # # #     except Exception as e:
# # # # # #         return extract_action_from_user_text(user_text)

# # # # # # def extract_action_from_ai_response(ai_response, original_text):
# # # # # #     ai_response = ai_response.lower()

# # # # # #     # Scrolling actions
# # # # # #     if "scroll down" in ai_response:
# # # # # #         return {"action": "scroll", "direction": "down", "target": None, "original_text": original_text}
# # # # # #     elif "scroll up" in ai_response:
# # # # # #         return {"action": "scroll", "direction": "up", "target": None, "original_text": original_text}
# # # # # #     elif "scroll to top" in ai_response or "top of" in ai_response:
# # # # # #         return {"action": "scroll", "direction": "top", "target": None, "original_text": original_text}
# # # # # #     elif "scroll to bottom" in ai_response or "bottom of" in ai_response:
# # # # # #         return {"action": "scroll", "direction": "bottom", "target": None, "original_text": original_text}

# # # # # #     # 👉 Reading actions FIRST (before navigation)
# # # # # #     elif "read" in ai_response and "about" in ai_response:
# # # # # #         return {"action": "read", "target": "about", "direction": None, "original_text": original_text}
# # # # # #     elif "read" in ai_response and "service" in ai_response:
# # # # # #         return {"action": "read", "target": "services", "direction": None, "original_text": original_text}
# # # # # #     elif "read" in ai_response and "contact" in ai_response:
# # # # # #         return {"action": "read", "target": "contact", "direction": None, "original_text": original_text}
# # # # # #     elif "read" in ai_response and "header" in ai_response:
# # # # # #         return {"action": "read", "target": "header", "direction": None, "original_text": original_text}
# # # # # #     elif "read" in ai_response and "footer" in ai_response:
# # # # # #         return {"action": "read", "target": "footer", "direction": None, "original_text": original_text}
# # # # # #     elif "read" in ai_response:
# # # # # #         return {"action": "read", "target": "current", "direction": None, "original_text": original_text}

# # # # # #     # Navigation actions
# # # # # #     elif "about" in ai_response and "navigate" in ai_response or "go to about" in ai_response:
# # # # # #         return {"action": "navigate", "target": "about", "direction": None, "original_text": original_text}
# # # # # #     elif "service" in ai_response and "navigate" in ai_response or "go to services" in ai_response:
# # # # # #         return {"action": "navigate", "target": "services", "direction": None, "original_text": original_text}
# # # # # #     elif "contact" in ai_response and "navigate" in ai_response or "go to contact" in ai_response:
# # # # # #         return {"action": "navigate", "target": "contact", "direction": None, "original_text": original_text}
# # # # # #     elif "header" in ai_response and "navigate" in ai_response:
# # # # # #         return {"action": "navigate", "target": "header", "direction": None, "original_text": original_text}
# # # # # #     elif "footer" in ai_response and "navigate" in ai_response:
# # # # # #         return {"action": "navigate", "target": "footer", "direction": None, "original_text": original_text}

# # # # # #     # Unknown → fallback
# # # # # #     return extract_action_from_user_text(original_text)



# # # # # # def extract_action_from_user_text(user_text):
# # # # # #     user_text = user_text.lower().strip()

# # # # # #     # Scrolling actions
# # # # # #     if "scroll down" in user_text:
# # # # # #         return {"action": "scroll", "direction": "down", "target": None, "original_text": user_text}
# # # # # #     elif "scroll up" in user_text:
# # # # # #         return {"action": "scroll", "direction": "up", "target": None, "original_text": user_text}
# # # # # #     elif "top" in user_text:
# # # # # #         return {"action": "scroll", "direction": "top", "target": None, "original_text": user_text}
# # # # # #     elif "bottom" in user_text:
# # # # # #         return {"action": "scroll", "direction": "bottom", "target": None, "original_text": user_text}

# # # # # #     # 👉 Reading actions FIRST
# # # # # #     elif "read about" in user_text:
# # # # # #         return {"action": "read", "target": "about", "direction": None, "original_text": user_text}
# # # # # #     elif "read services" in user_text:
# # # # # #         return {"action": "read", "target": "services", "direction": None, "original_text": user_text}
# # # # # #     elif "read contact" in user_text or "read the contact info" in user_text:
# # # # # #         return {"action": "read", "target": "contact", "direction": None, "original_text": user_text}
# # # # # #     elif "read header" in user_text:
# # # # # #         return {"action": "read", "target": "header", "direction": None, "original_text": user_text}
# # # # # #     elif "read footer" in user_text:
# # # # # #         return {"action": "read", "target": "footer", "direction": None, "original_text": user_text}
# # # # # #     elif "read" in user_text:
# # # # # #         return {"action": "read", "target": "current", "direction": None, "original_text": user_text}

# # # # # #     # Navigation actions
# # # # # #     elif "about" in user_text:
# # # # # #         return {"action": "navigate", "target": "about", "direction": None, "original_text": user_text}
# # # # # #     elif "services" in user_text:
# # # # # #         return {"action": "navigate", "target": "services", "direction": None, "original_text": user_text}
# # # # # #     elif "contact" in user_text:
# # # # # #         return {"action": "navigate", "target": "contact", "direction": None, "original_text": user_text}
# # # # # #     elif "header" in user_text:
# # # # # #         return {"action": "navigate", "target": "header", "direction": None, "original_text": user_text}
# # # # # #     elif "footer" in user_text:
# # # # # #         return {"action": "navigate", "target": "footer", "direction": None, "original_text": user_text}

# # # # # #     else:
# # # # # #         return {"action": "unknown", "target": None, "direction": None, "original_text": user_text}


# # # # # # if __name__ == '__main__':
# # # # # #     app.run(host='0.0.0.0', port=5000, debug=True)

# # # # # # from flask import Flask, request, jsonify
# # # # # # from flask_cors import CORS
# # # # # # import os
# # # # # # import google.generativeai as genai
# # # # # # from dotenv import load_dotenv
# # # # # # import json # Import the json library

# # # # # # # Load environment variables from .env file
# # # # # # load_dotenv()

# # # # # # # Initialize Flask app
# # # # # # app = Flask(__name__)
# # # # # # CORS(app)  # Enable CORS for React frontend

# # # # # # # Configure Gemini AI
# # # # # # try:
# # # # # #     genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
# # # # # #     model = genai.GenerativeModel('gemini-1.5-flash')
# # # # # # except Exception as e:
# # # # # #     print(f"Error configuring Gemini AI: {e}")
# # # # # #     model = None

# # # # # # # Health check endpoint
# # # # # # @app.route('/health', methods=['GET'])
# # # # # # def health_check():
# # # # # #     return jsonify({
# # # # # #         "status": "healthy",
# # # # # #         "message": "Sarathi Voice Bot API is running!"
# # # # # #     })

# # # # # # # Main voice command processing endpoint
# # # # # # @app.route('/process-command', methods=['POST'])
# # # # # # def process_voice_command():
# # # # # #     if not model:
# # # # # #         return jsonify({"error": "Gemini AI model is not configured"}), 500
        
# # # # # #     try:
# # # # # #         data = request.get_json()
# # # # # #         if not data or 'text' not in data:
# # # # # #             return jsonify({"error": "Missing 'text' field in request"}), 400

# # # # # #         user_text = data['text'].strip()
# # # # # #         if not user_text:
# # # # # #             return jsonify({"error": "Text field is empty"}), 400

# # # # # #         # The new function does all the work
# # # # # #         response_json = analyze_and_get_json(user_text)
        
# # # # # #         # Add the original text to the final response for the frontend
# # # # # #         response_json['original_text'] = user_text
        
# # # # # #         return jsonify(response_json)

# # # # # #     except Exception as e:
# # # # # #         return jsonify({
# # # # # #             "error": f"Internal server error: {str(e)}"
# # # # # #         }), 500

# # # # # # def analyze_and_get_json(user_text):
# # # # # #     """
# # # # # #     Asks Gemini to directly output a JSON object based on the user's command.
# # # # # #     Includes robust parsing and a fallback.
# # # # # #     """
    
# # # # # #     # The prompt remains the same
# # # # # #     prompt = f"""
# # # # # # You are a highly intelligent voice command interpreter for a web accessibility application named "Sarathi".
# # # # # # Your ONLY job is to convert the user's spoken command into a structured JSON object.
# # # # # # Do NOT respond with any explanations, pleasantries, or text outside of the JSON object.

# # # # # # The website has the following sections: "header", "about", "services", "contact", "footer".

# # # # # # The JSON object MUST have the following structure:
# # # # # # {{
# # # # # #   "action": "string",
# # # # # #   "target": "string or null",
# # # # # #   "direction": "string or null"
# # # # # # }}

# # # # # # Here are the rules for the JSON values:

# # # # # # 1.  **"action"** (string): Must be one of the following:
# # # # # #     - "navigate": For moving to a specific section.
# # # # # #     - "scroll": For scrolling the page.
# # # # # #     - "read": For reading a section's content aloud.
# # # # # #     - "unknown": If the user's intent is unclear.

# # # # # # 2.  **"target"** (string or null):
# # # # # #     - If action is "navigate" or "read", this MUST be one of: "header", "about", "services", "contact", "footer".
# # # # # #     - If action is "scroll", this MUST be null.
# # # # # #     - For ambiguous commands like "read this", use "current".

# # # # # # 3.  **"direction"** (string or null):
# # # # # #     - If action is "scroll", this MUST be one of: "up", "down", "top", "bottom".
# # # # # #     - Otherwise, it MUST be null.

# # # # # # ---
# # # # # # Here are some examples:

# # # # # # User command: "scroll down a little bit"
# # # # # # {{
# # # # # #   "action": "scroll",
# # # # # #   "target": null,
# # # # # #   "direction": "down"
# # # # # # }}

# # # # # # User command: "tell me about the services"
# # # # # # {{
# # # # # #   "action": "read",
# # # # # #   "target": "services",
# # # # # #   "direction": null
# # # # # # }}

# # # # # # User command: "Uhh, I want to go to the contact stuff"
# # # # # # {{
# # # # # #   "action": "navigate",
# # # # # #   "target": "contact",
# # # # # #   "direction": null
# # # # # # }}

# # # # # # User command: "what is the price of gold"
# # # # # # {{
# # # # # #   "action": "unknown",
# # # # # #   "target": null,
# # # # # #   "direction": null
# # # # # # }}
# # # # # # ---

# # # # # # Now, analyze the following user command and provide ONLY the JSON response.

# # # # # # User command: "{user_text}"
# # # # # # """

# # # # # #     # --- THE FIX IS IN THIS TRY/EXCEPT BLOCK ---
# # # # # #     response = None # Initialize response to None
# # # # # #     try:
# # # # # #         response = model.generate_content(prompt)
# # # # # #         ai_response_text = response.text.strip()
        
# # # # # #         if ai_response_text.startswith("```json"):
# # # # # #             ai_response_text = ai_response_text[7:-3].strip()
        
# # # # # #         parsed_json = json.loads(ai_response_text)
# # # # # #         return parsed_json

# # # # # #     except Exception as e:
# # # # # #         # The corrected error logging:
# # # # # #         # It no longer tries to access 'response.text' if 'response' might not exist.
# # # # # #         if response:
# # # # # #              print(f"Error processing Gemini response: {e}\nResponse was: {response.text}")
# # # # # #         else:
# # # # # #              print(f"Failed to get response from Gemini API: {e}")
       
# # # # # #         return {
# # # # # #             "action": "unknown",
# # # # # #             "target": None,
# # # # # #             "direction": None
# # # # # #         }

# # # # # # if __name__ == '__main__':
# # # # # #     app.run(host='0.0.0.0', port=5000, debug=True)
# # # # # # app.py - Final Version

# # # # # from flask import Flask, request, jsonify
# # # # # from flask_cors import CORS
# # # # # import os
# # # # # import google.generativeai as genai
# # # # # from dotenv import load_dotenv
# # # # # import json

# # # # # # Load environment variables from .env file
# # # # # load_dotenv()

# # # # # # Initialize Flask app
# # # # # app = Flask(__name__)
# # # # # CORS(app)  # Enable CORS for React frontend

# # # # # # Configure Gemini AI
# # # # # try:
# # # # #     genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
# # # # #     model = genai.GenerativeModel('gemini-1.5-flash')
# # # # # except Exception as e:
# # # # #     print(f"Error configuring Gemini AI: {e}")
# # # # #     model = None

# # # # # # Health check endpoint
# # # # # @app.route('/health', methods=['GET'])
# # # # # def health_check():
# # # # #     return jsonify({
# # # # #         "status": "healthy",
# # # # #         "message": "Sarathi Voice Bot API is running!"
# # # # #     })

# # # # # # Main voice command processing endpoint
# # # # # @app.route('/process-command', methods=['POST'])
# # # # # def process_voice_command():
# # # # #     if not model:
# # # # #         return jsonify({"error": "Gemini AI model is not configured"}), 500
        
# # # # #     try:
# # # # #         data = request.get_json()
# # # # #         if not data or 'text' not in data:
# # # # #             return jsonify({"error": "Missing 'text' field in request"}), 400

# # # # #         user_text = data['text'].strip()
# # # # #         if not user_text:
# # # # #             return jsonify({"error": "Text field is empty"}), 400

# # # # #         # The new function does all the work
# # # # #         response_json = analyze_and_get_json(user_text)
        
# # # # #         # Add the original text to the final response for the frontend
# # # # #         response_json['original_text'] = user_text
        
# # # # #         return jsonify(response_json)

# # # # #     except Exception as e:
# # # # #         return jsonify({
# # # # #             "error": f"Internal server error: {str(e)}"
# # # # #         }), 500

# # # # # def analyze_and_get_json(user_text):
# # # # #     """
# # # # #     Asks Gemini to directly output a JSON object based on the user's command.
# # # # #     Includes robust parsing and a fallback.
# # # # #     """
    
# # # # #     prompt = f"""
# # # # # You are a highly intelligent voice command interpreter for a web accessibility application named "Sarathi".
# # # # # Your ONLY job is to convert the user's spoken command into a structured JSON object.
# # # # # Do NOT respond with any explanations, pleasantries, or text outside of the JSON object.

# # # # # The website has the following sections: "header", "about", "services", "contact", "footer".

# # # # # The JSON object MUST have the following structure:
# # # # # {{
# # # # #   "action": "string",
# # # # #   "target": "string or null",
# # # # #   "direction": "string or null"
# # # # # }}

# # # # # Here are the rules for the JSON values:

# # # # # 1.  **"action"** (string): Must be one of the following:
# # # # #     - "navigate": For moving to a specific section.
# # # # #     - "scroll": For scrolling the page.
# # # # #     - "read": For reading a section's content aloud.
# # # # #     - "unknown": If the user's intent is unclear.

# # # # # 2.  **"target"** (string or null):
# # # # #     - If action is "navigate" or "read", this MUST be one of: "header", "about", "services", "contact", "footer".
# # # # #     - If action is "scroll", this MUST be null.
# # # # #     - For ambiguous commands like "read this", use "current".

# # # # # 3.  **"direction"** (string or null):
# # # # #     - If action is "scroll", this MUST be one of: "up", "down", "top", "bottom".
# # # # #     - Otherwise, it MUST be null.

# # # # # ---
# # # # # Here are some examples:

# # # # # User command: "scroll down a little bit"
# # # # # {{
# # # # #   "action": "scroll",
# # # # #   "target": null,
# # # # #   "direction": "down"
# # # # # }}

# # # # # User command: "tell me about the services"
# # # # # {{
# # # # #   "action": "read",
# # # # #   "target": "services",
# # # # #   "direction": null
# # # # # }}

# # # # # User command: "Uhh, I want to go to the contact stuff"
# # # # # {{
# # # # #   "action": "navigate",
# # # # #   "target": "contact",
# # # # #   "direction": null
# # # # # }}

# # # # # User command: "what is the price of gold"
# # # # # {{
# # # # #   "action": "unknown",
# # # # #   "target": null,
# # # # #   "direction": null
# # # # # }}
# # # # # ---

# # # # # Now, analyze the following user command and provide ONLY the JSON response.

# # # # # User command: "{user_text}"
# # # # # """

# # # # #     response = None 
# # # # #     try:
# # # # #         response = model.generate_content(prompt)
# # # # #         ai_response_text = response.text.strip()
        
# # # # #         if ai_response_text.startswith("```json"):
# # # # #             ai_response_text = ai_response_text[7:-3].strip()
        
# # # # #         parsed_json = json.loads(ai_response_text)
# # # # #         return parsed_json

# # # # #     except Exception as e:
# # # # #         if response:
# # # # #              print(f"Error processing Gemini response: {e}\nResponse was: {response.text}")
# # # # #         else:
# # # # #              print(f"Failed to get response from Gemini API: {e}")
       
# # # # #         return {
# # # # #             "action": "unknown",
# # # # #             "target": None,
# # # # #             "direction": None
# # # # #         }

# # # # # if __name__ == '__main__':
# # # # #     app.run(host='0.0.0.0', port=5000, debug=True)
# # # # from flask import Flask, request, jsonify
# # # # from flask_cors import CORS
# # # # import os
# # # # import google.generativeai as genai
# # # # from dotenv import load_dotenv
# # # # import json

# # # # load_dotenv()
# # # # app = Flask(__name__)
# # # # CORS(app)

# # # # try:
# # # #     genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
# # # #     model = genai.GenerativeModel('gemini-1.5-flash')
# # # # except Exception as e:
# # # #     print(f"Error configuring Gemini AI: {e}")
# # # #     model = None

# # # # @app.route('/health', methods=['GET'])
# # # # def health_check():
# # # #     return jsonify({"status": "healthy", "message": "Sarathi Voice Bot API is running!"})

# # # # @app.route('/process-command', methods=['POST'])
# # # # def process_voice_command():
# # # #     if not model:
# # # #         return jsonify({"error": "Gemini AI model is not configured"}), 500
        
# # # #     try:
# # # #         data = request.get_json()
# # # #         user_text = data.get('text', '').strip()
# # # #         page_commands = data.get('page_commands', [])

# # # #         if not user_text:
# # # #             return jsonify({"error": "Text field is empty"}), 400

# # # #         #
# # # #         # --- NEW LOGIC STARTS HERE ---
# # # #         #
        
# # # #         # 1. First, classify the user's intent
# # # #         intent = classify_intent(user_text)
        
# # # #         # 2. Then, execute the correct action based on the intent
# # # #         if intent == "WEBSITE_COMMAND":
# # # #             command_payload = get_website_command_json(user_text, page_commands)
# # # #             response = {
# # # #                 "type": "WEBSITE_COMMAND",
# # # #                 "payload": command_payload
# # # #             }
# # # #         elif intent == "GENERAL_QUESTION":
# # # #             answer_text = get_general_answer(user_text)
# # # #             response = {
# # # #                 "type": "GENERAL_ANSWER",
# # # #                 "payload": {"text_to_speak": answer_text}
# # # #             }
# # # #         else: # Fallback for unknown intents
# # # #             response = {
# # # #                 "type": "GENERAL_ANSWER",
# # # #                 "payload": {"text_to_speak": "I'm not sure how to handle that request."}
# # # #             }
        
# # # #         return jsonify(response)

# # # #     except Exception as e:
# # # #         return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# # # # def classify_intent(user_text):
# # # #     """
# # # #     NEW: Uses Gemini to classify the user's text into a specific category.
# # # #     """
# # # #     prompt = f"""
# # # # You are an intent classification system. Your only job is to categorize the user's command.
# # # # The two possible categories are:
# # # # 1.  WEBSITE_COMMAND: For any command related to navigating, scrolling, or reading the content of the current webpage.
# # # # 2.  GENERAL_QUESTION: For any question about facts, people, places, or general knowledge that is not related to the website.

# # # # Analyze the user's text and respond with ONLY the category name. Do not add any other words or explanation.

# # # # ---
# # # # Examples:
# # # # User: "scroll down" -> WEBSITE_COMMAND
# # # # User: "who is the president of the United States?" -> GENERAL_QUESTION
# # # # User: "navigate to the features section" -> WEBSITE_COMMAND
# # # # User: "what is the capital of France?" -> GENERAL_QUESTION
# # # # ---

# # # # User text: "{user_text}"
# # # # """
# # # #     try:
# # # #         response = model.generate_content(prompt)
# # # #         return response.text.strip()
# # # #     except Exception as e:
# # # #         print(f"Error in intent classification: {e}")
# # # #         return "UNKNOWN"

# # # # def get_general_answer(user_text):
# # # #     """
# # # #     NEW: Asks Gemini to provide a direct answer to a general question.
# # # #     """
# # # #     prompt = f"""
# # # # You are a helpful and concise AI assistant. Directly answer the user's question in a single, clear sentence.

# # # # User question: "{user_text}"
# # # # Answer:"""
# # # #     try:
# # # #         response = model.generate_content(prompt)
# # # #         return response.text.strip()
# # # #     except Exception as e:
# # # #         print(f"Error getting general answer: {e}")
# # # #         return "I'm sorry, I encountered an error while trying to answer that."


# # # # def get_website_command_json(user_text, page_commands):
# # # #     """
# # # #     This is our old `analyze_and_get_json` function, now repurposed for website commands.
# # # #     """
# # # #     valid_targets_str = ", ".join([f'"{cmd}"' for cmd in page_commands]) if page_commands else '"none"'

# # # #     prompt = f"""
# # # # You are a highly intelligent voice command interpreter for a web accessibility application named "Sarathi".
# # # # Your ONLY job is to convert the user's spoken command into a structured JSON object for controlling the website.
# # # # The website currently has these specific sections available for navigation or reading: {valid_targets_str}.

# # # # The JSON object MUST have the following structure:
# # # # {{
# # # #   "action": "string",
# # # #   "target": "string or null",
# # # #   "direction": "string or null"
# # # # }}

# # # # Here are the rules for the JSON values:
# # # # 1. "action": Must be "navigate", "scroll", "read", or "unknown".
# # # # 2. "target": If action is "navigate" or "read", this MUST be one of the available sections: {valid_targets_str}. Otherwise, it is null.
# # # # 3. "direction": If action is "scroll", this MUST be "up", "down", "top", or "bottom". Otherwise, it is null.
# # # # ---
# # # # User command: "{user_text}"
# # # # """
# # # #     response = None 
# # # #     try:
# # # #         response = model.generate_content(prompt)
# # # #         ai_response_text = response.text.strip()
# # # #         if ai_response_text.startswith("```json"):
# # # #             ai_response_text = ai_response_text[7:-3].strip()
# # # #         parsed_json = json.loads(ai_response_text)
# # # #         return parsed_json
# # # #     except Exception as e:
# # # #         # Error handling remains the same
# # # #         return {"action": "unknown", "target": None, "direction": None}

# # # # if __name__ == '__main__':
# # # #     app.run(host='0.0.0.0', port=5000, debug=True)











# # vbdvhjvdshv shvd                     dhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
















# # # # from flask import Flask, request, jsonify
# # # # from flask_cors import CORS
# # # # import os
# # # # import google.generativeai as genai
# # # # from dotenv import load_dotenv
# # # # import json
# # # # # 1. Import our new mail sender function
# # # # from mail_sender import send_emergency_email 

# # # # # Load environment variables
# # # # load_dotenv()
# # # # app = Flask(__name__)
# # # # CORS(app)

# # # # # Configure Gemini AI
# # # # try:
# # # #     genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
# # # #     model = genai.GenerativeModel('gemini-2.5-flash')
# # # # except Exception as e:
# # # #     print(f"Error configuring Gemini AI: {e}")
# # # #     model = None

# # # # @app.route('/health', methods=['GET'])
# # # # def health_check():
# # # #     return jsonify({"status": "healthy", "message": "Sarathi Voice Bot API is running!"})

# # # # @app.route('/process-command', methods=['POST'])
# # # # def process_voice_command():
# # # #     if not model:
# # # #         return jsonify({"error": "Gemini AI model is not configured"}), 500
# # # #     try:
# # # #         data = request.get_json()
# # # #         user_text = data.get('text', '').strip()
# # # #         page_commands = data.get('page_commands', [])
# # # #         # 2. Receive the location data from the frontend
# # # #         location = data.get('location', None) 

# # # #         if not user_text:
# # # #             return jsonify({"error": "Text field is empty"}), 400

# # # #         # --- THIS IS THE CORE DISPATCHER LOGIC ---
        
# # # #         # First, classify the user's intent to decide what to do
# # # #         intent = classify_intent(user_text)
        
# # # #         # If it's an emergency, call the mail sender and stop
# # # #         if intent == "EMERGENCY_HELP":
# # # #             success = send_emergency_email(location)
# # # #             response = {
# # # #                 "type": "HELP_ACTION",
# # # #                 "payload": {"status": "success" if success else "failed"}
# # # #             }
# # # #         # If it's a website command, get the navigation JSON
# # # #         elif intent == "WEBSITE_COMMAND":
# # # #             command_payload = get_website_command_json(user_text, page_commands)
# # # #             response = {
# # # #                 "type": "WEBSITE_COMMAND",
# # # #                 "payload": command_payload
# # # #             }
# # # #         # Otherwise, assume it's a general question and answer it
# # # #         else: # GENERAL_QUESTION or UNKNOWN
# # # #             answer_text = get_general_answer(user_text)
# # # #             response = {
# # # #                 "type": "GENERAL_ANSWER",
# # # #                 "payload": {"text_to_speak": answer_text}
# # # #             }
        
# # # #         return jsonify(response)
        
# # # #     except Exception as e:
# # # #         return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# # # # def classify_intent(user_text):
# # # #     """
# # # #     Uses Gemini to classify the user's text into one of three categories.
# # # #     This is the "triage nurse" of the backend.
# # # #     """
# # # #     prompt = f"""
# # # # You are an intent classification system. Your only job is to categorize the user's command.
# # # # The three possible categories are:
# # # # 1.  WEBSITE_COMMAND: For navigating, scrolling, or reading the current webpage.
# # # # 2.  GENERAL_QUESTION: For questions about facts, people, or general knowledge.
# # # # 3.  EMERGENCY_HELP: For urgent requests for help, using keywords like "help" or "mayday".

# # # # Analyze the user's text and respond with ONLY the category name.
# # # # ---
# # # # Examples:
# # # # User: "scroll down" -> WEBSITE_COMMAND
# # # # User: "who is the president?" -> GENERAL_QUESTION
# # # # User: "help help help" -> EMERGENCY_HELP
# # # # User: "mayday mayday" -> EMERGENCY_HELP
# # # # User: "navigate to features" -> WEBSITE_COMMAND
# # # # ---
# # # # User text: "{user_text}"
# # # # """
# # # #     try:
# # # #         response = model.generate_content(prompt)
# # # #         return response.text.strip()
# # # #     except Exception as e:
# # # #         print(f"Error in intent classification: {e}")
# # # #         return "UNKNOWN"

# # # # def get_general_answer(user_text):
# # # #     """Asks Gemini to provide a direct answer to a general question."""
# # # #     prompt = f"""You are a helpful and concise AI assistant. Directly answer the user's question in a single, clear sentence. User question: "{user_text}" Answer:"""
# # # #     try:
# # # #         response = model.generate_content(prompt)
# # # #         return response.text.strip()
# # # #     except Exception as e:
# # # #         print(f"Error getting general answer: {e}")
# # # #         return "I'm sorry, I can't answer that right now."

# # # # def get_website_command_json(user_text, page_commands):
# # # #     """
# # # #     Generates the specific JSON for website navigation commands.
# # # #     """
# # # #     valid_targets_str = ", ".join([f'"{cmd}"' for cmd in page_commands]) if page_commands else '"none"'
# # # #     prompt = f"""
# # # # You are a highly intelligent voice command interpreter for a web accessibility application named "Sarathi".
# # # # Your ONLY job is to convert the user's spoken command into a structured JSON object for controlling the website.
# # # # The website currently has these specific sections available for navigation or reading: {valid_targets_str}.

# # # # The JSON object MUST have the following structure:
# # # # {{
# # # #   "action": "string",
# # # #   "target": "string or null",
# # # #   "direction": "string or null"
# # # # }}

# # # # Here are the rules for the JSON values:
# # # # 1. "action": Must be "navigate", "scroll", "read", or "unknown".
# # # # 2. "target": If action is "navigate" or "read", this MUST be one of the available sections: {valid_targets_str}. Otherwise, it is null.
# # # # 3. "direction": If action is "scroll", this MUST be "up", "down", "top", or "bottom". Otherwise, it is null.
# # # # ---
# # # # User command: "{user_text}"
# # # # """
# # # #     response = None 
# # # #     try:
# # # #         response = model.generate_content(prompt)
# # # #         ai_response_text = response.text.strip()
# # # #         if ai_response_text.startswith("```json"):
# # # #             ai_response_text = ai_response_text[7:-3].strip()
# # # #         parsed_json = json.loads(ai_response_text)
# # # #         return parsed_json
# # # #     except Exception as e:
# # # #         print(f"Error parsing website command JSON: {e}")
# # # #         return {"action": "unknown", "target": None, "direction": None}

# # # # if __name__ == '__main__':
# # # #     app.run(host='0.0.0.0', port=5000, debug=True)

# # # from flask import Flask, request, jsonify
# # # from flask_cors import CORS
# # # import os
# # # import google.generativeai as genai
# # # from dotenv import load_dotenv
# # # import json
# # # import random
# # # from mail_sender import send_emergency_email

# # # load_dotenv()
# # # app = Flask(__name__)
# # # CORS(app)

# # # # --- UPDATED: Load and configure both API keys ---
# # # voice_model = None
# # # game_model = None
# # # try:
# # #     # Configure the first model for the voice bot using the primary key
# # #     voice_api_key = os.getenv('GEMINI_API_KEY')
# # #     if voice_api_key:
# # #         genai.configure(api_key=voice_api_key)
# # #         voice_model = genai.GenerativeModel('gemini-2.5-flash')
# # #         print("Voice Bot AI model configured successfully.")
# # #     else:
# # #         print("Warning: GEMINI_API_KEY not found in .env file.")

# # #     # Configure the second model for the game generator using the secondary key
# # #     # We use a different configuration method to handle the second key
# # #     game_api_key = os.getenv('GAME_GEN_API_KEY')
# # #     if game_api_key:
# # #         game_model = genai.GenerativeModel(
# # #             model_name='gemini-2.5-flash',
# # #             generation_config={'temperature': 0.8}, # Example of different config for this model
# # #             safety_settings=None,
# # #             client_options={'api_key': game_api_key}
# # #         )
# # #         print("Game Generator AI model configured successfully.")
# # #     else:
# # #         print("Warning: GAME_GEN_API_KEY not found in .env file. Game generation will fail.")

# # # except Exception as e:
# # #     print(f"An error occurred during Gemini AI model configuration: {e}")


# # # @app.route('/health', methods=['GET'])
# # # def health_check():
# # #     return jsonify({"status": "healthy", "message": "Sarathi Voice Bot API is running!"})


# # # @app.route('/generate-game', methods=['POST'])
# # # def generate_game():
# # #     if not game_model: # Use the game_model
# # #         return jsonify({"error": "Game Generator AI model is not configured"}), 500
    
# # #     try:
# # #         data = request.get_json()
# # #         disability = data.get('disability', 'general').strip()
# # #         prompt = f"""
# # # You are an expert web developer specializing in creating simple, accessible, single-file HTML/CSS/JS educational games for children.
# # # Your task is to generate the complete code for a children's game specifically designed for a user with: **{disability}**.
# # # **CRITICAL INSTRUCTIONS:**
# # # 1.  **Single File Only:** All HTML, CSS (in `<style>`), and JavaScript (in `<script>`) MUST be in one file.
# # # 2.  **Accessibility First:** Mechanics must be appropriate for the disability (e.g., high contrast for visual impairment, large click targets for motor disability).
# # # 3.  **No External Libraries:** Use only vanilla JavaScript, HTML, and CSS.
# # # 4.  **Raw HTML Output:** Respond ONLY with the raw HTML code, starting with `<!DOCTYPE html>`. Do not use markdown.
# # # """
# # #         print(f"Generating a game for disability profile: {disability}...")
# # #         response = game_model.generate_content(prompt) # Use the game_model
# # #         game_html = response.text.replace("```html", "").replace("```", "").strip()
# # #         return jsonify({"game_html": game_html})

# # #     except Exception as e:
# # #         print(f"Error generating game: {e}")
# # #         return jsonify({"error": f"Internal server error while generating game: {str(e)}"}), 500


# # # @app.route('/process-command', methods=['POST'])
# # # def process_voice_command():
# # #     if not voice_model: # Use the voice_model
# # #         return jsonify({"error": "Voice Bot AI model is not configured"}), 500
# # #     try:
# # #         data = request.get_json()
# # #         user_text = data.get('text', '').strip()
# # #         page_commands = data.get('page_commands', [])
# # #         location = data.get('location', None)

# # #         if not user_text:
# # #             return jsonify({"error": "Text field is empty"}), 400

# # #         intent = classify_intent(user_text, voice_model) # Pass the model
        
# # #         if intent == "EMERGENCY_HELP":
# # #             success = send_emergency_email(location)
# # #             response = {"type": "HELP_ACTION", "payload": {"status": "success" if success else "failed"}}
# # #         elif intent == "WEBSITE_COMMAND":
# # #             command_payload = get_website_command_json(user_text, page_commands, voice_model) # Pass the model
# # #             response = {"type": "WEBSITE_COMMAND", "payload": command_payload}
# # #         else: # GENERAL_QUESTION or UNKNOWN
# # #             answer_text = get_general_answer(user_text, voice_model) # Pass the model
# # #             response = {"type": "GENERAL_ANSWER", "payload": {"text_to_speak": answer_text}}
        
# # #         return jsonify(response)
# # #     except Exception as e:
# # #         return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# # # # UPDATED: All helper functions now accept a 'model' argument to specify which AI to use


# # # def classify_intent(user_text, model):
# # #     prompt = f"""You are an intent classification system. Categorize the user's command as WEBSITE_COMMAND, GENERAL_QUESTION, or EMERGENCY_HELP. Respond with ONLY the category name. User text: "{user_text}" """
# # #     try:
# # #         response = model.generate_content(prompt)
# # #         return response.text.strip()
# # #     except Exception as e:
# # #         print(f"Error in intent classification: {e}")
# # #         return "UNKNOWN"

# # # def get_general_answer(user_text, model):
# # #     prompt = f"""Directly answer the user's question in a single, clear sentence. User question: "{user_text}" Answer:"""
# # #     try:
# # #         return model.generate_content(prompt).text.strip()
# # #     except Exception as e:
# # #         print(f"Error getting general answer: {e}")
# # #         return "I'm sorry, I can't answer that right now."

# # # def get_website_command_json(user_text, page_commands, model):
# # #     valid_targets_str = ", ".join([f'"{cmd}"' for cmd in page_commands]) if page_commands else '"none"'
# # #     prompt = f"""You are a JSON interpreter for a website. The user said: "{user_text}". The available sections are: {valid_targets_str}. Return ONLY a JSON object with keys "action", "target", and "direction"."""
# # #     try:
# # #         response = model.generate_content(prompt)
# # #         ai_response_text = response.text.strip().replace("```json", "").replace("```", "")
# # #         return json.loads(ai_response_text)
# # #     except Exception as e:
# # #         print(f"Error parsing website command JSON: {e}")
# # #         return {"action": "unknown", "target": None, "direction": None}


# # # if __name__ == '__main__':
# # #     app.run(host='0.0.0.0', port=5000, debug=True)


# # # from flask import Flask, request, jsonify
# # # from flask_cors import CORS
# # # import os
# # # import google.generativeai as genai
# # # from dotenv import load_dotenv
# # # import json
# # # import random
# # # from mail_sender import send_emergency_email

# # # load_dotenv()
# # # app = Flask(__name__)
# # # CORS(app)

# # # # --- SIMPLIFIED: We go back to a single model for all AI tasks ---
# # # model = None
# # # try:
# # #     # Configure the single, primary model using the standard method
# # #     api_key = os.getenv('GEMINI_API_KEY')
# # #     if api_key:
# # #         genai.configure(api_key=api_key)
# # #         # We will use 'gemini-1.5-flash' as it is fast and capable
# # #         model = genai.GenerativeModel('gemini-2.5-flash')
# # #         print("✅ Gemini AI model configured successfully.")
# # #     else:
# # #         print("❌ CRITICAL: GEMINI_API_KEY not found in .env file. AI features will fail.")

# # # except Exception as e:
# # #     print(f"❌ CRITICAL: An error occurred during Gemini AI model configuration: {e}")


# # # @app.route('/health', methods=['GET'])
# # # def health_check():
# # #     return jsonify({"status": "healthy", "message": "Sarathi Voice Bot API is running!"})


# # # @app.route('/generate-game', methods=['POST'])
# # # def generate_game():
# # #     if not model:
# # #         return jsonify({"error": "AI model is not configured"}), 500
    
# # #     try:
# # #         data = request.get_json()
# # #         disability = data.get('disability', 'general').strip()
# # #         prompt = f"""
# # # You are an expert web developer specializing in creating simple, accessible, single-file HTML/CSS/JS educational games for children.
# # # Your task is to generate the complete code for a children's game specifically for a user with: **{disability}**.
# # # **CRITICAL INSTRUCTIONS:**
# # # 1.  **Single File Only:** All HTML, CSS (in `<style>`), and JavaScript (in `<script>`) MUST be in one file.
# # # 2.  **Accessibility First:** Mechanics must be appropriate for the disability.
# # # 3.  **No External Libraries:** Use only vanilla JavaScript, HTML, and CSS.
# # # 4.  **Raw HTML Output:** Respond ONLY with the raw HTML code, starting with `<!DOCTYPE html>`.
# # # """
# # #         print(f"Generating a game for disability profile: {disability}...")
# # #         response = model.generate_content(prompt) # Use the single 'model'
# # #         game_html = response.text.replace("```html", "").replace("```", "").strip()
# # #         return jsonify({"game_html": game_html})

# # #     except Exception as e:
# # #         print(f"Error generating game: {e}")
# # #         return jsonify({"error": f"Internal server error while generating game: {str(e)}"}), 500


# # # @app.route('/process-command', methods=['POST'])
# # # def process_voice_command():
# # #     if not model:
# # #         return jsonify({"error": "AI model is not configured"}), 500
# # #     try:
# # #         data = request.get_json()
# # #         user_text = data.get('text', '').strip()
# # #         page_commands = data.get('page_commands', [])
# # #         location = data.get('location', None)

# # #         intent = classify_intent(user_text) # No need to pass model anymore
        
# # #         if intent == "EMERGENCY_HELP":
# # #             success = send_emergency_email(location)
# # #             response = {"type": "HELP_ACTION", "payload": {"status": "success" if success else "failed"}}
# # #         elif intent == "PLAY_GAME":
# # #             # This logic can now be removed as game generation is handled by the new endpoint
# # #             # We'll default to a general answer for "play game" voice commands for now.
# # #              answer_text = get_general_answer("The user wants to play a game.")
# # #              response = {"type": "GENERAL_ANSWER", "payload": {"text_to_speak": answer_text}}
# # #         elif intent == "WEBSITE_COMMAND":
# # #             command_payload = get_website_command_json(user_text, page_commands)
# # #             response = {"type": "WEBSITE_COMMAND", "payload": command_payload}
# # #         else: # GENERAL_QUESTION
# # #             answer_text = get_general_answer(user_text)
# # #             response = {"type": "GENERAL_ANSWER", "payload": {"text_to_speak": answer_text}}
        
# # #         return jsonify(response)
# # #     except Exception as e:
# # #         return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# # # # All helper functions now use the global 'model'
# # # def classify_intent(user_text):
# # #     prompt = f"""You are an intent classification system... User text: "{user_text}" """
# # #     try:
# # #         response = model.generate_content(prompt)
# # #         return response.text.strip()
# # #     except Exception as e:
# # #         print(f"Error in intent classification: {e}")
# # #         return "UNKNOWN"

# # # def get_general_answer(user_text):
# # #     prompt = f"""Directly answer the user's question in a single sentence. User question: "{user_text}" Answer:"""
# # #     try:
# # #         return model.generate_content(prompt).text.strip()
# # #     except Exception as e:
# # #         print(f"Error getting general answer: {e}")
# # #         return "I'm sorry, I can't answer that right now."

# # # def get_website_command_json(user_text, page_commands):
# # #     valid_targets_str = ", ".join([f'"{cmd}"' for cmd in page_commands]) if page_commands else '"none"'
# # #     prompt = f"""You are a JSON interpreter... User said: "{user_text}". Available sections are: {valid_targets_str}."""
# # #     try:
# # #         response = model.generate_content(prompt)
# # #         ai_response_text = response.text.strip().replace("```json", "").replace("```", "")
# # #         return json.loads(ai_response_text)
# # #     except Exception as e:
# # #         print(f"Error parsing website command JSON: {e}")
# # #         return {"action": "unknown", "target": None, "direction": None}


# # # if __name__ == '__main__':
# # #     app.run(host='0.0.0.0', port=5000, debug=True)

# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # import os
# # import google.generativeai as genai
# # from dotenv import load_dotenv
# # import json
# # import random
# # from mail_sender import send_emergency_email

# # load_dotenv()
# # app = Flask(__name__)
# # CORS(app)

# # # --- UPDATED: Load and configure two separate models ---
# # voice_model = None
# # game_model = None
# # try:
# #     # Configure the first model for the voice bot
# #     voice_api_key = os.getenv('VOICE_BOT_API_KEY')
# #     if voice_api_key:
# #         # This configures the default client for the voice bot
# #         genai.configure(api_key=voice_api_key)
# #         voice_model = genai.GenerativeModel('gemini-2.5-flash') # Still a great, fast choice for this
# #         print("✅ Voice Bot AI model configured successfully.")
# #     else:
# #         print("⚠️ Warning: VOICE_BOT_API_KEY not found. Voice features will fail.")

# #     # Configure the second model for the game generator with its own key
# #     game_api_key = os.getenv('GAME_GEN_API_KEY')
# #     if game_api_key:
# #         # By passing the key directly here, we use it for this model instance only
# #         game_model = genai.GenerativeModel(
# #             model_name='gemini-2.5-flash', # Using the newer model as you suggested
# #             client_options={'api_key': game_api_key}
# #         )
# #         print("✅ Game Generator AI model configured successfully.")
# #     else:
# #         print("⚠️ Warning: GAME_GEN_API_KEY not found. Game generation will fail.")

# # except Exception as e:
# #     print(f"❌ CRITICAL: An error occurred during Gemini AI model configuration: {e}")


# # @app.route('/health', methods=['GET'])
# # def health_check():
# #     return jsonify({"status": "healthy", "message": "Sarathi Voice Bot API is running!"})


# # @app.route('/generate-game', methods=['POST'])
# # def generate_game():
# #     if not game_model: # Check for the specific game_model
# #         return jsonify({"error": "Game Generator AI model is not configured"}), 500
    
# #     try:
# #         data = request.get_json()
# #         disability = data.get('disability', 'general').strip()
# #         prompt = f"""You are an expert web developer specializing in creating simple, accessible, single-file HTML/CSS/JS educational games for children...""" # (Prompt is the same)
        
# #         print(f"Generating a game for disability profile: {disability}...")
# #         response = game_model.generate_content(prompt) # Use the game_model
# #         game_html = response.text.replace("```html", "").replace("```", "").strip()
# #         return jsonify({"game_html": game_html})

# #     except Exception as e:
# #         print(f"Error generating game: {e}")
# #         return jsonify({"error": f"Internal server error while generating game: {str(e)}"}), 500


# # @app.route('/process-command', methods=['POST'])
# # def process_voice_command():
# #     if not voice_model: # Check for the specific voice_model
# #         return jsonify({"error": "Voice Bot AI model is not configured"}), 500
# #     try:
# #         data = request.get_json()
# #         user_text = data.get('text', '').strip()
# #         page_commands = data.get('page_commands', [])
# #         location = data.get('location', None)

# #         intent = classify_intent(user_text) # Uses the default (voice) model
        
# #         if intent == "EMERGENCY_HELP":
# #             success = send_emergency_email(location)
# #             response = {"type": "HELP_ACTION", "payload": {"status": "success" if success else "failed"}}
# #         elif intent == "PLAY_GAME":
# #              answer_text = get_general_answer("The user wants to play a game. They should use the Game Generator feature on the education page.")
# #              response = {"type": "GENERAL_ANSWER", "payload": {"text_to_speak": answer_text}}
# #         elif intent == "WEBSITE_COMMAND":
# #             command_payload = get_website_command_json(user_text, page_commands)
# #             response = {"type": "WEBSITE_COMMAND", "payload": command_payload}
# #         else: # GENERAL_QUESTION
# #             answer_text = get_general_answer(user_text)
# #             response = {"type": "GENERAL_ANSWER", "payload": {"text_to_speak": answer_text}}
        
# #         return jsonify(response)
# #     except Exception as e:
# #         return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# # # Helper functions will now use the default 'voice_model'
# # def classify_intent(user_text):
# #     prompt = f"""You are an intent classification system...""" # (Prompt is the same)
# #     try:
# #         response = voice_model.generate_content(prompt) # Use voice_model
# #         return response.text.strip()
# #     except Exception as e:
# #         print(f"Error in intent classification: {e}")
# #         return "UNKNOWN"

# # def get_general_answer(user_text):
# #     prompt = f"""Directly answer the user's question...""" # (Prompt is the same)
# #     try:
# #         return voice_model.generate_content(prompt).text.strip() # Use voice_model
# #     except Exception as e:
# #         print(f"Error getting general answer: {e}")
# #         return "I'm sorry, I can't answer that right now."

# # def get_website_command_json(user_text, page_commands):
# #     valid_targets_str = ", ".join([f'"{cmd}"' for cmd in page_commands]) if page_commands else '"none"'
# #     prompt = f"""You are a JSON interpreter...""" # (Prompt is the same)
# #     try:
# #         response = voice_model.generate_content(prompt) # Use voice_model
# #         ai_response_text = response.text.strip().replace("```json", "").replace("```", "")
# #         return json.loads(ai_response_text)
# #     except Exception as e:
# #         print(f"Error parsing website command JSON: {e}")
# #         return {"action": "unknown", "target": None, "direction": None}


# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=5000, debug=True)


# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # import os
# # import google.generativeai as genai
# # from dotenv import load_dotenv
# # import json
# # import random
# # from mail_sender import send_emergency_email

# # load_dotenv()
# # app = Flask(__name__)
# # CORS(app)

# # # --- UPDATED: Configure two separate models for each feature ---
# # voice_model = None
# # game_model = None
# # try:
# #     # 1. Configure the Voice Bot model using its dedicated key
# #     voice_api_key = os.getenv('VOICE_BOT_API_KEY')
# #     if voice_api_key:
# #         # This configures the default client, which we'll use for the voice bot
# #         genai.configure(api_key=voice_api_key)
# #         voice_model = genai.GenerativeModel('gemini-2.5-flash')
# #         print("✅ Voice Bot AI model configured successfully.")
# #     else:
# #         print("⚠️ WARNING: VOICE_BOT_API_KEY not found. Voice features will fail.")

# #     # 2. Configure the Game Generator model using its own key
# #     # This method is now supported by your updated library and won't cause an error.
# #     game_api_key = os.getenv('GAME_GEN_API_KEY')
# #     if game_api_key:
# #         game_model = genai.GenerativeModel('gemini-2.5-flash')
# #         print("✅ Game Generator AI model configured successfully.")
# #     else:
# #         print("⚠️ WARNING: GAME_GEN_API_KEY not found. Game generation will fail.")

# # except Exception as e:
# #     print(f"❌ CRITICAL: An error occurred during Gemini AI model configuration: {e}")


# # @app.route('/health', methods=['GET'])
# # def health_check():
# #     return jsonify({"status": "healthy", "message": "Sarathi Voice Bot API is running!"})


# # @app.route('/generate-game', methods=['POST'])
# # def generate_game():
# #     # This endpoint now uses the specific 'game_model'
# #     if not game_model:
# #         return jsonify({"error": "Game Generator AI model is not configured"}), 500
    
# #     try:
# #         data = request.get_json()
# #         disability = data.get('disability', 'general').strip()
# #         prompt = f"""
# # You are an expert web developer specializing in creating simple, accessible, single-file HTML/CSS/JS educational games for children.
# # Your task is to generate the complete code for a children's game specifically for a user with: **{disability}**.
# # **CRITICAL INSTRUCTIONS:**
# # 1.  **Single File Only:** All HTML, CSS (in `<style>`), and JavaScript (in `<script>`) MUST be in one file.
# # 2.  **Accessibility First:** Mechanics must be appropriate for the disability.
# # 3.  **No External Libraries:** Use only vanilla JavaScript, HTML, and CSS.
# # 4.  **Raw HTML Output:** Respond ONLY with the raw HTML code, starting with `<!DOCTYPE html>`.
# # """
# #         print(f"Generating a game for disability profile: {disability}...")
# #         response = game_model.generate_content(prompt) # Use the game_model
# #         game_html = response.text.replace("```html", "").replace("```", "").strip()
# #         return jsonify({"game_html": game_html})

# #     except Exception as e:
# #         print(f"Error generating game: {e}")
# #         return jsonify({"error": f"Internal server error while generating game: {str(e)}"}), 500


# # @app.route('/process-command', methods=['POST'])
# # def process_voice_command():
# #     # This endpoint now uses the specific 'voice_model'
# #     if not voice_model:
# #         return jsonify({"error": "Voice Bot AI model is not configured"}), 500
# #     try:
# #         data = request.get_json()
# #         user_text = data.get('text', '').strip()
# #         page_commands = data.get('page_commands', [])
# #         location = data.get('location', None)

# #         intent = classify_intent(user_text)
        
# #         if intent == "EMERGENCY_HELP":
# #             success = send_emergency_email(location)
# #             response = {"type": "HELP_ACTION", "payload": {"status": "success" if success else "failed"}}
# #         elif intent == "PLAY_GAME":
# #              answer_text = get_general_answer("The user wants to play a game. They can use the Game Generator feature on the education page.")
# #              response = {"type": "GENERAL_ANSWER", "payload": {"text_to_speak": answer_text}}
# #         elif intent == "WEBSITE_COMMAND":
# #             command_payload = get_website_command_json(user_text, page_commands)
# #             response = {"type": "WEBSITE_COMMAND", "payload": command_payload}
# #         else: # GENERAL_QUESTION
# #             answer_text = get_general_answer(user_text)
# #             response = {"type": "GENERAL_ANSWER", "payload": {"text_to_speak": answer_text}}
        
# #         return jsonify(response)
# #     except Exception as e:
# #         return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# # # All voice-related helper functions now use the 'voice_model' by default
# # def classify_intent(user_text):
# #     prompt = f"""You are an intent classification system. Your only job is to categorize the user's command. The four possible categories are: WEBSITE_COMMAND, GENERAL_QUESTION, EMERGENCY_HELP, PLAY_GAME. Analyze the user's text and respond with ONLY the category name. User text: "{user_text}" """
# #     try:
# #         response = voice_model.generate_content(prompt)
# #         return response.text.strip()
# #     except Exception as e:
# #         print(f"Error in intent classification: {e}")
# #         return "UNKNOWN"

# # def get_general_answer(user_text):
# #     prompt = f"""Directly answer the user's question in a single sentence. User question: "{user_text}" Answer:"""
# #     try:
# #         return voice_model.generate_content(prompt).text.strip()
# #     except Exception as e:
# #         print(f"Error getting general answer: {e}")
# #         return "I'm sorry, I can't answer that right now."

# # def get_website_command_json(user_text, page_commands):
# #     valid_targets_str = ", ".join([f'"{cmd}"' for cmd in page_commands]) if page_commands else '"none"'
# #     prompt = f"""You are a JSON interpreter for a website. The user said: "{user_text}". The available sections are: {valid_targets_str}. Return ONLY a JSON object with keys "action", "target", and "direction"."""
# #     try:
# #         response = voice_model.generate_content(prompt)
# #         ai_response_text = response.text.strip().replace("```json", "").replace("```", "")
# #         return json.loads(ai_response_text)
# #     except Exception as e:
# #         print(f"Error parsing website command JSON: {e}")
# #         return {"action": "unknown", "target": None, "direction": None}


# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=5000, debug=True)


# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # import os
# # import google.generativeai as genai
# # from dotenv import load_dotenv
# # import json
# # import random
# # from mail_sender import send_emergency_email

# # load_dotenv()
# # app = Flask(__name__)
# # CORS(app)

# # # --- This section is UNCHANGED, as you requested ---
# # voice_model = None
# # game_model = None
# # try:
# #     # 1. Configure the Voice Bot model using its dedicated key
# #     voice_api_key = os.getenv('VOICE_BOT_API_KEY')
# #     if voice_api_key:
# #         # This configures the default client, which we'll use for the voice bot
# #         genai.configure(api_key=voice_api_key)
# #         voice_model = genai.GenerativeModel('gemini-2.5-flash')
# #         print("✅ Voice Bot AI model configured successfully.")
# #     else:
# #         print("⚠️ WARNING: VOICE_BOT_API_KEY not found. Voice features will fail.")

# #     # 2. Configure the Game Generator model using its own key
# #     # This method is now supported by your updated library and won't cause an error.
# #     game_api_key = os.getenv('GAME_GEN_API_KEY')
# #     if game_api_key:
# #         game_model = genai.GenerativeModel('gemini-2.5-flash')
# #         print("✅ Game Generator AI model configured successfully.")
# #     else:
# #         print("⚠️ WARNING: GAME_GEN_API_KEY not found. Game generation will fail.")

# # except Exception as e:
# #     print(f"❌ CRITICAL: An error occurred during Gemini AI model configuration: {e}")

# # # --- End of Unchanged Section ---


# # # NEW: A list of themes to ensure variety in game generation
# # GAME_THEMES = ["Jungle Animals", "Space Exploration", "Under the Sea", "Magical Forest", "City Vehicles", "Farm Life", "Dinosaurs", "Superheroes"]


# # @app.route('/health', methods=['GET'])
# # def health_check():
# #     return jsonify({"status": "healthy", "message": "Sarathi Voice Bot API is running!"})


# # @app.route('/generate-game', methods=['POST'])
# # def generate_game():
# #     if not game_model:
# #         return jsonify({"error": "Game Generator AI model is not configured"}), 500
    
# #     try:
# #         data = request.get_json()
# #         disability = data.get('disability', 'general').strip()
# #         # 1. ADDED: Pick a random theme to force variety
# #         random_theme = random.choice(GAME_THEMES) 

# #         # 2. UPDATED: A much more detailed and strict prompt
# #         prompt = f"""
# # You are an expert web developer specializing in creating simple, accessible, single-file HTML/CSS/JS educational games for children.

# # Your task is to generate the complete code for a children's game with the theme "{random_theme}", specifically designed and adapted for a user with: **{disability}**.

# # **CRITICAL INSTRUCTIONS (MUST BE FOLLOWED):**

# # 1.  **Game Structure:** The game MUST follow this exact structure:
# #     - It must have exactly **10 rounds or levels**.
# #     - It must keep a visible **score** (e.g., "Score: X / 10").
# #     - After the 10th round, the game MUST end and hide the game area.
# #     - Upon ending, it MUST display a **final summary screen** showing the total score (e.g., "Game Over! You scored 8 out of 10!").
# #     - The summary screen must include a **"Play Again" button** that restarts the entire game from round 1.

# # 2.  **Single File Only:** All HTML, CSS (in `<style>`), and JavaScript (in `<script>`) MUST be in a single HTML file.

# # 3.  **Accessibility First:** The game mechanics must be appropriate for the specified disability (e.g., high contrast for visual impairment, large click targets for motor disability).

# # 4.  **No External Libraries:** Use only vanilla JavaScript, HTML, and CSS.

# # 5.  **Image Usage (VERY IMPORTANT):** Do not use any external image URLs from random websites as they are unreliable. If your game requires images, you MUST use placeholder images from `placehold.co`. For example, for an image of a moon, use a URL like `https://placehold.co/400x400/CCCCCC/333333?text=Moon`. This ensures the images will always load.

# # 6.  **Raw HTML Output:** Respond ONLY with the raw HTML code for the game, starting with `<!DOCTYPE html>`. Do not use markdown or any other text.
# # """
        
# #         print(f"Generating a '{random_theme}' game for disability profile: {disability}...")
# #         response = game_model.generate_content(prompt)
        
# #         game_html = response.text.replace("```html", "").replace("```", "").strip()
# #         return jsonify({"game_html": game_html})

# #     except Exception as e:
# #         print(f"Error generating game: {e}")
# #         return jsonify({"error": f"Internal server error while generating game: {str(e)}"}), 500


# # # --- The entire voice bot logic below this line is UNHARMED and UNCHANGED ---

# # @app.route('/process-command', methods=['POST'])
# # def process_voice_command():
# #     if not voice_model:
# #         return jsonify({"error": "Voice Bot AI model is not configured"}), 500
# #     try:
# #         data = request.get_json()
# #         user_text = data.get('text', '').strip()
# #         page_commands = data.get('page_commands', [])
# #         location = data.get('location', None)
# #         intent = classify_intent(user_text)
# #         if intent == "EMERGENCY_HELP":
# #             success = send_emergency_email(location)
# #             response = {"type": "HELP_ACTION", "payload": {"status": "success" if success else "failed"}}
# #         elif intent == "PLAY_GAME":
# #              answer_text = get_general_answer("The user wants to play a game. They can use the Game Generator feature on the education page.")
# #              response = {"type": "GENERAL_ANSWER", "payload": {"text_to_speak": answer_text}}
# #         elif intent == "WEBSITE_COMMAND":
# #             command_payload = get_website_command_json(user_text, page_commands)
# #             response = {"type": "WEBSITE_COMMAND", "payload": command_payload}
# #         else:
# #             answer_text = get_general_answer(user_text)
# #             response = {"type": "GENERAL_ANSWER", "payload": {"text_to_speak": answer_text}}
# #         return jsonify(response)
# #     except Exception as e:
# #         return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# # def classify_intent(user_text):
# #     prompt = f"""You are an intent classification system. Your only job is to categorize the user's command. The four possible categories are: WEBSITE_COMMAND, GENERAL_QUESTION, EMERGENCY_HELP, PLAY_GAME. Analyze the user's text and respond with ONLY the category name. User text: "{user_text}" """
# #     try:
# #         response = voice_model.generate_content(prompt)
# #         return response.text.strip()
# #     except Exception as e:
# #         print(f"Error in intent classification: {e}")
# #         return "UNKNOWN"

# # def get_general_answer(user_text):
# #     prompt = f"""Directly answer the user's question in a single sentence. User question: "{user_text}" Answer:"""
# #     try:
# #         return voice_model.generate_content(prompt).text.strip()
# #     except Exception as e:
# #         print(f"Error getting general answer: {e}")
# #         return "I'm sorry, I can't answer that right now."

# # def get_website_command_json(user_text, page_commands):
# #     valid_targets_str = ", ".join([f'"{cmd}"' for cmd in page_commands]) if page_commands else '"none"'
# #     prompt = f"""You are a JSON interpreter for a website. The user said: "{user_text}". The available sections are: {valid_targets_str}. Return ONLY a JSON object with keys "action", "target", and "direction"."""
# #     try:
# #         response = voice_model.generate_content(prompt)
# #         ai_response_text = response.text.strip().replace("```json", "").replace("```", "")
# #         return json.loads(ai_response_text)
# #     except Exception as e:
# #         print(f"Error parsing website command JSON: {e}")
# #         return {"action": "unknown", "target": None, "direction": None}

# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=5000, debug=True)

# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # import os
# # import google.generativeai as genai
# # from dotenv import load_dotenv
# # import json
# # import random
# # from mail_sender import send_emergency_email

# # load_dotenv()
# # app = Flask(__name__)
# # CORS(app)

# # # --- Using a single, unified model for simplicity and stability ---
# # model = None
# # try:
# #     api_key = os.getenv('VOICE_BOT_API_KEY')
# #     if api_key:
# #         genai.configure(api_key=api_key)
# #         model = genai.GenerativeModel('gemini-2.5-flash')
# #         print("✅ Gemini AI model configured successfully.")
# #     else:
# #         print("❌ CRITICAL: GEMINI_API_KEY not found in .env file.")

# # except Exception as e:
# #     print(f"❌ CRITICAL: An error occurred during Gemini AI model configuration: {e}")


# # @app.route('/health', methods=['GET'])
# # def health_check():
# #     return jsonify({"status": "healthy", "message": "Sarathi Voice Bot API is running!"})


# # @app.route('/generate-game', methods=['POST'])
# # def generate_game():
# #     if not model:
# #         return jsonify({"error": "AI model is not configured"}), 500
# #     try:
# #         # ... (Game generation logic remains the same)
# #         data = request.get_json()
# #         disability = data.get('disability', 'general').strip()
# #         random_theme = random.choice(["Jungle", "Space", "Sea"])
# #         prompt = f"""You are an expert game developer... (rest of prompt)"""
# #         response = model.generate_content(prompt)
# #         game_html = response.text.replace("```html", "").replace("```", "").strip()
# #         return jsonify({"game_html": game_html})
# #     except Exception as e:
# #         return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# # @app.route('/process-command', methods=['POST'])
# # def process_voice_command():
# #     if not model:
# #         return jsonify({"error": "AI model is not configured"}), 500
# #     try:
# #         data = request.get_json()
# #         user_text = data.get('text', '').strip()
# #         page_commands = data.get('page_commands', [])
# #         location = data.get('location', None)

# #         intent = classify_intent(user_text)
        
# #         if intent == "EMERGENCY_HELP":
# #             success = send_emergency_email(location)
# #             response = {"type": "HELP_ACTION", "payload": {"status": "success" if success else "failed"}}
# #         elif intent == "PLAY_GAME":
# #              answer_text = get_general_answer("The user wants to play a game...")
# #              response = {"type": "GENERAL_ANSWER", "payload": {"text_to_speak": answer_text}}
# #         elif intent == "WEBSITE_COMMAND":
# #             command_payload = get_website_command_json(user_text, page_commands)
# #             response = {"type": "WEBSITE_COMMAND", "payload": command_payload}
# #         else:
# #             answer_text = get_general_answer(user_text)
# #             response = {"type": "GENERAL_ANSWER", "payload": {"text_to_speak": answer_text}}
        
# #         return jsonify(response)
# #     except Exception as e:
# #         return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# # def classify_intent(user_text):
# #     prompt = f"""Categorize the user's command as WEBSITE_COMMAND, GENERAL_QUESTION, EMERGENCY_HELP, or PLAY_GAME. Respond with ONLY the category name. User text: "{user_text}" """
# #     try:
# #         return model.generate_content(prompt).text.strip()
# #     except Exception as e:
# #         print(f"Error in intent classification: {e}")
# #         return "UNKNOWN"

# # def get_general_answer(user_text):
# #     prompt = f"""Directly answer the user's question in a single sentence. User question: "{user_text}" Answer:"""
# #     try:
# #         return model.generate_content(prompt).text.strip()
# #     except Exception as e:
# #         print(f"Error getting general answer: {e}")
# #         return "I'm sorry, I can't answer that right now."

# # # --- THIS IS THE UPDATED FUNCTION ---
# # def get_website_command_json(user_text, page_commands):
# #     valid_targets_str = ", ".join([f'"{cmd}"' for cmd in page_commands]) if page_commands else '"none"'
    
# #     # UPDATED: A much more strict and detailed prompt
# #     prompt = f"""
# # You are a precise JSON interpreter for a website's voice control system. Your ONLY job is to convert the user's command into a perfectly structured JSON object.

# # **CRITICAL RULES (MUST BE FOLLOWED):**
# # 1.  **`action`**: MUST be one of: `"navigate"`, `"scroll"`, `"read"`, or `"unknown"`.
# # 2.  **`target`**: 
# #     - MUST be one of the available sections: {valid_targets_str}.
# #     - MUST be a single word (e.g., "about", not "about section").
# #     - MUST be `null` if the action is `"scroll"`.
# # 3.  **`direction`**: 
# #     - MUST be one of: `"up"`, `"down"`, `"top"`, `"bottom"`.
# #     - MUST be `null` for any action that is not `"scroll"`. Do NOT use words like "none" or "forward".

# # **COMMAND ANALYSIS:**
# # The user said: "{user_text}"
# # The available sections on the page are: {valid_targets_str}

# # **EXAMPLES OF CORRECT OUTPUT:**

# # User command: "scroll to the top of the page"
# # {{
# #   "action": "scroll",
# #   "target": null,
# #   "direction": "top"
# # }}

# # User command: "go to about section"
# # {{
# #   "action": "navigate",
# #   "target": "about",
# #   "direction": null
# # }}

# # User command: "read the services"
# # {{
# #   "action": "read",
# #   "target": "services",
# #   "direction": null
# # }}

# # Now, generate ONLY the JSON object for the user's command.
# # """
# #     try:
# #         response = model.generate_content(prompt)
# #         ai_response_text = response.text.strip().replace("```json", "").replace("```", "")
# #         return json.loads(ai_response_text)
# #     except Exception as e:
# #         print(f"Error parsing website command JSON: {e}")
# #         return {"action": "unknown", "target": None, "direction": None}

# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=5000, debug=True)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# import google.generativeai as genai
# from dotenv import load_dotenv
# import json
# import random
# from mail_sender import send_emergency_email

# load_dotenv()
# app = Flask(__name__)
# CORS(app)

# # --- Using a single, unified model for simplicity and stability ---
# model = None
# try:
#     api_key = os.getenv('VOICE_BOT_API_KEY')
#     if api_key:
#         genai.configure(api_key=api_key)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         print("✅ Gemini AI model configured successfully.")
#     else:
#         print("❌ CRITICAL: GEMINI_API_KEY not found in .env file.")

# except Exception as e:
#     print(f"❌ CRITICAL: An error occurred during Gemini AI model configuration: {e}")


# @app.route('/health', methods=['GET'])
# def health_check():
#     return jsonify({"status": "healthy", "message": "Sarathi Voice Bot API is running!"})


# @app.route('/generate-game', methods=['POST'])
# def generate_game():
#     if not model:
#         return jsonify({"error": "AI model is not configured"}), 500
#     try:
#         # ... (Game generation logic remains the same)
#         data = request.get_json()
#         disability = data.get('disability', 'general').strip()
#         random_theme = random.choice(["Jungle", "Space", "Sea"])
#         prompt = f"""You are an expert game developer... (rest of prompt)"""
#         response = model.generate_content(prompt)
#         game_html = response.text.replace("```html", "").replace("```", "").strip()
#         return jsonify({"game_html": game_html})
#     except Exception as e:
#         return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# @app.route('/process-command', methods=['POST'])
# def process_voice_command():
#     if not model:
#         return jsonify({"error": "AI model is not configured"}), 500
#     try:
#         data = request.get_json()
#         user_text = data.get('text', '').strip()
#         page_commands = data.get('page_commands', [])
#         location = data.get('location', None)

#         intent = classify_intent(user_text)
        
#         if intent == "EMERGENCY_HELP":
#             success = send_emergency_email(location)
#             response = {"type": "HELP_ACTION", "payload": {"status": "success" if success else "failed"}}
#         elif intent == "PLAY_GAME":
#              answer_text = get_general_answer("The user wants to play a game...")
#              response = {"type": "GENERAL_ANSWER", "payload": {"text_to_speak": answer_text}}
#         elif intent == "WEBSITE_COMMAND":
#             command_payload = get_website_command_json(user_text, page_commands)
#             response = {"type": "WEBSITE_COMMAND", "payload": command_payload}
#         else:
#             answer_text = get_general_answer(user_text)
#             response = {"type": "GENERAL_ANSWER", "payload": {"text_to_speak": answer_text}}
        
#         return jsonify(response)
#     except Exception as e:
#         return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# def classify_intent(user_text):
#     prompt = f"""Categorize the user's command as WEBSITE_COMMAND, GENERAL_QUESTION, EMERGENCY_HELP, or PLAY_GAME. Respond with ONLY the category name. User text: "{user_text}" """
#     try:
#         return model.generate_content(prompt).text.strip()
#     except Exception as e:
#         print(f"Error in intent classification: {e}")
#         return "UNKNOWN"

# def get_general_answer(user_text):
#     prompt = f"""Directly answer the user's question in a single sentence. User question: "{user_text}" Answer:"""
#     try:
#         return model.generate_content(prompt).text.strip()
#     except Exception as e:
#         print(f"Error getting general answer: {e}")
#         return "I'm sorry, I can't answer that right now."

# # --- THIS IS THE UPDATED FUNCTION ---
# # def get_website_command_json(user_text, page_commands):
# #     # If page_commands is empty (like in our test script), use a default list.
# #     if not page_commands:
# #         page_commands = ["home", "features", "about", "services", "contact", "community", "join"]

# #     valid_targets_str = ", ".join([f'"{cmd}"' for cmd in page_commands])
    
# #     # The prompt remains the same, but now it will have a valid list of targets.
# #     prompt = f"""
# # You are a precise JSON interpreter for a website's voice control system. Your ONLY job is to convert the user's command into a perfectly structured JSON object.

# # **CRITICAL RULES (MUST BE FOLLOWED):**
# # 1.  **`action`**: MUST be one of: `"navigate"`, `"scroll"`, `"read"`, or `"unknown"`.
# # 2.  **`target`**: 
# #     - MUST be one of the available sections: {valid_targets_str}.
# #     - MUST be a single word (e.g., "about", not "about section").
# #     - MUST be `null` if the action is `"scroll"`.
# # 3.  **`direction`**: 
# #     - MUST be one of: `"up"`, `"down"`, `"top"`, `"bottom"`.
# #     - MUST be `null` for any action that is not `"scroll"`. Do NOT use words like "none" or "forward".

# # **COMMAND ANALYSIS:**
# # The user said: "{user_text}"
# # The available sections on the page are: {valid_targets_str}

# # **EXAMPLES OF CORRECT OUTPUT:**

# # User command: "scroll to the top of the page"
# # {{
# #   "action": "scroll",
# #   "target": null,
# #   "direction": "top"
# # }}

# # User command: "go to about section"
# # {{
# #   "action": "navigate",
# #   "target": "about",
# #   "direction": null
# # }}

# # User command: "read the services"
# # {{
# #   "action": "read",
# #   "target": "services",
# #   "direction": null
# # }}

# # Now, generate ONLY the JSON object for the user's command.
# # """
# #     try:
# #         response = model.generate_content(prompt)
# #         ai_response_text = response.text.strip().replace("```json", "").replace("```", "")
# #         return json.loads(ai_response_text)
# #     except Exception as e:
# #         print(f"Error parsing website command JSON: {e}")
# #         return {"action": "unknown", "target": None, "direction": None}
# # In app.py, replace ONLY this function

# def get_website_command_json(user_text, page_commands):
#     # If page_commands is empty (like in our test script), use a default list.
#     if not page_commands:
#         page_commands = ["home", "features", "about", "services", "contact", "community", "join"]

#     # Define the global links that are always available in the navbar
#     global_links = ["Communication", "Education", "Stories", "Mission", "Profile", "Logout"]
    
#     valid_targets_str = ", ".join([f'"{cmd}"' for cmd in page_commands])
#     global_links_str = ", ".join([f'"{link}"' for link in global_links])

#     # UPDATED: A much more powerful prompt that understands different action types
#     prompt = f"""
# You are a precise JSON interpreter for a website's voice control system. Your ONLY job is to convert the user's command into a perfectly structured JSON object.

# **AVAILABLE ACTIONS & TARGETS:**
# 1.  **Scroll to a section on the current page:** Use `action: "scrollTo"`. The `target` must be one of the Current Page Sections.
# 2.  **Navigate to a different page:** Use `action: "goToPage"`. The `target` must be a URL path (e.g., "/communication").
# 3.  **Click a button or link:** Use `action: "click"`. The `target` must be the text on the button (e.g., "Logout").
# 4.  **General Scrolling:** Use `action: "scroll"` with `direction`.

# **CONTEXT:**
# -   **Global Navigation Links (available on all pages):** {global_links_str}
# -   **Current Page Sections:** {valid_targets_str}

# **CRITICAL RULES:**
# -   For `action: "goToPage"`, the `target` must be a lowercase URL path, like "/stories".
# -   For `action: "click"`, the `target` must be the exact text of the button, like "Profile".
# -   For `action: "scrollTo"`, the `target` must be a single word ID, like "features".
# -   `direction` must be `null` unless the action is `"scroll"`.

# **COMMAND ANALYSIS:**
# The user said: "{user_text}"

# **EXAMPLES:**
# - User command: "scroll to the features" -> {{"action": "scrollTo", "target": "features", "direction": null}}
# - User command: "go to the communication page" -> {{"action": "goToPage", "target": "/communication", "direction": null}}
# - User command: "click the logout button" -> {{"action": "click", "target": "Logout", "direction": null}}

# Now, generate ONLY the JSON object for the user's command.
# """
#     try:
#         response = model.generate_content(prompt)
#         ai_response_text = response.text.strip().replace("```json", "").replace("```", "")
#         # Rename the action for consistency on the frontend
#         parsed_json = json.loads(ai_response_text)
#         if parsed_json.get("action") == "scrollTo":
#             parsed_json["action"] = "navigate"
#         return parsed_json
#     except Exception as e:
#         print(f"Error parsing website command JSON: {e}")
#         return {"action": "unknown", "target": None, "direction": None}

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)



# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# import google.generativeai as genai
# from dotenv import load_dotenv
# import json
# import random
# from mail_sender import send_emergency_email

# load_dotenv()
# app = Flask(__name__)
# CORS(app)

# # --- Using a single, unified model for simplicity and stability ---
# model = None
# try:
#     api_key = os.getenv('VOICE_BOT_API_KEY')
#     if api_key:
#         genai.configure(api_key=api_key)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         print("✅ Gemini AI model configured successfully.")
#     else:
#         print("❌ CRITICAL: GEMINI_API_KEY not found in .env file.")

# except Exception as e:
#     print(f"❌ CRITICAL: An error occurred during Gemini AI model configuration: {e}")


# @app.route('/health', methods=['GET'])
# def health_check():
#     return jsonify({"status": "healthy", "message": "Sarathi Voice Bot API is running!"})


# # All other endpoints like /generate-game remain unchanged...
# @app.route('/generate-game', methods=['POST'])
# def generate_game():
#     if not model: return jsonify({"error": "AI model is not configured"}), 500
#     # ... (code for game generation is unchanged)
#     return jsonify({"game_html": "..."}) 


# @app.route('/process-command', methods=['POST'])
# def process_voice_command():
#     if not model:
#         return jsonify({"error": "AI model is not configured"}), 500
#     try:
#         data = request.get_json()
#         user_text = data.get('text', '').strip()
#         page_commands = data.get('page_commands', [])
#         location = data.get('location', None)

#         intent = classify_intent(user_text)
        
#         if intent == "EMERGENCY_HELP":
#             success = send_emergency_email(location)
#             response = {"type": "HELP_ACTION", "payload": {"status": "success" if success else "failed"}}
#         elif intent == "WEBSITE_COMMAND":
#             # This function is the one we are updating
#             command_payload = get_website_command_json(user_text, page_commands)
#             response = {"type": "WEBSITE_COMMAND", "payload": command_payload}
#         else:
#             answer_text = get_general_answer(user_text)
#             response = {"type": "GENERAL_ANSWER", "payload": {"text_to_speak": answer_text}}
        
#         return jsonify(response)
#     except Exception as e:
#         return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# def classify_intent(user_text):
#     prompt = f"""Categorize the user's command as WEBSITE_COMMAND, GENERAL_QUESTION, or EMERGENCY_HELP. Respond with ONLY the category name. User text: "{user_text}" """
#     try:
#         return model.generate_content(prompt).text.strip()
#     except Exception as e:
#         print(f"Error in intent classification: {e}")
#         return "UNKNOWN"

# def get_general_answer(user_text):
#     prompt = f"""Directly answer the user's question in a single sentence. User question: "{user_text}" Answer:"""
#     try:
#         return model.generate_content(prompt).text.strip()
#     except Exception as e:
#         print(f"Error getting general answer: {e}")
#         return "I'm sorry, I can't answer that right now."


# # --- THIS IS THE UPDATED, MORE POWERFUL FUNCTION ---
# # def get_website_command_json(user_text, page_commands):
# #     # If page_commands is empty (e.g., during testing), use a default list.
# #     if not page_commands:
# #         page_commands = ["home", "features", "about", "services", "contact", "community", "join"]

# #     # Define the global links that are always available in the navigation bar
# #     global_links = ["Communication", "Education", "Stories", "Mission", "Profile", "Logout"]
    
# #     valid_targets_str = ", ".join([f'"{cmd}"' for cmd in page_commands])
# #     global_links_str = ", ".join([f'"{link}"' for link in global_links])

# #     # A more powerful prompt that teaches the AI about different action types
# #     prompt = f"""
# # You are a precise JSON interpreter for a website's voice control system. Your ONLY job is to convert the user's command into a perfectly structured JSON object.

# # **AVAILABLE ACTIONS & TARGETS:**
# # 1.  **Scroll to a section ON THE CURRENT PAGE:** Use `action: "navigate"`. The `target` must be one of the Current Page Sections.
# # 2.  **Navigate to a DIFFERENT PAGE:** Use `action: "goToPage"`. The `target` must be a URL path (e.g., "/communication").
# # 3.  **Click a button or link:** Use `action: "click"`. The `target` must be the text on the button (e.g., "Logout").
# # 4.  **General Scrolling:** Use `action: "scroll"` with a `direction`.

# # **CONTEXT:**
# # -   **Global Navigation Links (available on all pages):** {global_links_str}
# # -   **Current Page Sections (only on this page):** {valid_targets_str}

# # **CRITICAL RULES:**
# # -   For `action: "goToPage"`, the `target` MUST be a lowercase URL path, like "/stories".
# # -   For `action: "click"`, the `target` MUST be the exact text of the button, like "Profile".
# # -   For `action: "navigate"`, the `target` MUST be a single word ID from the current page sections, like "features".
# # -   `direction` MUST be `null` unless the action is `"scroll"`.

# # **COMMAND ANALYSIS:**
# # The user said: "{user_text}"

# # **EXAMPLES:**
# # - User command: "scroll to the features" -> {{"action": "navigate", "target": "features", "direction": null}}
# # - User command: "go to the communication page" -> {{"action": "goToPage", "target": "/communication", "direction": null}}
# # - User command: "click the logout button" -> {{"action": "click", "target": "Logout", "direction": null}}

# # Now, generate ONLY the JSON object for the user's command.
# # """
# #     try:
# #         response = model.generate_content(prompt)
# #         ai_response_text = response.text.strip().replace("```json", "").replace("```", "")
# #         parsed_json = json.loads(ai_response_text)
# #         return parsed_json
# #     except Exception as e:
# #         print(f"Error parsing website command JSON: {e}")
# #         return {"action": "unknown", "target": None, "direction": None}

# # In app.py, replace ONLY this function

# # def get_website_command_json(user_text, page_commands):
# #     # This logic now also needs to know about the inputs on the page
# #     # For now, we'll add them directly to the prompt.
    
# #     # Define global elements and pages
# #     global_links = ["Communication", "Education", "Stories", "Mission", "Profile", "Logout", "Sign Up"]
# #     # Define common form field labels
# #     form_fields = ["Full Name", "Email Address", "Password", "Confirm Password"]

# #     valid_targets_str = ", ".join([f'"{cmd}"' for cmd in page_commands]) if page_commands else '"none"'
# #     global_links_str = ", ".join([f'"{link}"' for link in global_links])
# #     form_fields_str = ", ".join([f'"{field}"' for field in form_fields])

# #     prompt = f"""
# # You are a precise JSON interpreter for a website's voice control system. Your ONLY job is to convert the user's command into a perfectly structured JSON object.

# # **AVAILABLE ACTIONS & TARGETS:**
# # 1.  **Fill a form field:** Use `action: "fillInput"`.
# #     - `target`: The label of the form field (e.g., "Full Name").
# #     - `value`: The text to fill into the field (e.g., "John Doe").
# # 2.  **Click a button or link:** Use `action: "click"`. The `target` must be the text on the button.
# # 3.  **Navigate to a different page:** Use `action: "goToPage"`. The `target` must be a URL path.
# # 4.  **Scroll to a section on the current page:** Use `action: "navigate"`. The `target` must be a section ID.
# # 5.  **General Scrolling:** Use `action: "scroll"` with a `direction`.

# # **CONTEXT:**
# # -   **Global Clickable Elements:** {global_links_str}
# # -   **Form Fields on This Page:** {form_fields_str}
# # -   **Scrollable Sections on This Page:** {valid_targets_str}

# # **CRITICAL RULES:**
# # -   For "fill" commands, you MUST extract both the target field label and the value.
# # -   `direction` MUST be `null` unless the action is `"scroll"`.

# # **COMMAND ANALYSIS:**
# # The user said: "{user_text}"

# # **EXAMPLES:**
# # - User command: "go to the communication page" -> {{"action": "goToPage", "target": "/communication"}}
# # - User command: "click the logout button" -> {{"action": "click", "target": "Logout"}}
# # - User command: "fill the Full Name field with John Doe" -> {{"action": "fillInput", "target": "Full Name", "value": "John Doe"}}
# # - User command: "my email address is example@test.com" -> {{"action": "fillInput", "target": "Email Address", "value": "example@test.com"}}

# # Now, generate ONLY the JSON object for the user's command.
# # """
# #     try:
# #         response = model.generate_content(prompt)
# #         ai_response_text = response.text.strip().replace("```json", "").replace("```", "")
# #         parsed_json = json.loads(ai_response_text)
# #         return parsed_json
# #     except Exception as e:
# #         print(f"Error parsing website command JSON: {e}")
# #         return {"action": "unknown"}

# def get_website_command_json(user_text, page_commands):
#     # This logic now also needs to know about the inputs on the page
#     # For now, we'll add them directly to the prompt.
    
#     # Define global elements and pages
#     global_links = ["Communication", "Education", "Stories", "Mission", "Profile", "Logout", "Sign Up"]
#     # Define common form field labels
#     form_fields = ["Full Name", "Email Address", "Password", "Confirm Password"]

#     valid_targets_str = ", ".join([f'"{cmd}"' for cmd in page_commands]) if page_commands else '"none"'
#     global_links_str = ", ".join([f'"{link}"' for link in global_links])
#     form_fields_str = ", ".join([f'"{field}"' for field in form_fields])

#     # UPDATED: The prompt now has a specific rule for handling emails.
#     prompt = f"""
# You are a precise JSON interpreter for a website's voice control system. Your ONLY job is to convert the user's command into a perfectly structured JSON object.

# **AVAILABLE ACTIONS & TARGETS:**
# 1.  **Fill a form field:** Use `action: "fillInput"`.
#     - `target`: The label of the form field (e.g., "Full Name").
#     - `value`: The text to fill into the field (e.g., "John Doe").
# 2.  **Click a button or link:** Use `action: "click"`. The `target` must be the text on the button.
# 3.  **Navigate to a different page:** Use `action: "goToPage"`. The `target` must be a URL path.
# 4.  **Scroll to a section on the current page:** Use `action: "navigate"`. The `target` must be a section ID.
# 5.  **General Scrolling:** Use `action: "scroll"` with a `direction`.

# **CONTEXT:**
# -   **Global Clickable Elements:** {global_links_str}
# -   **Form Fields on This Page:** {form_fields_str}
# -   **Scrollable Sections on This Page:** {valid_targets_str}

# **CRITICAL RULES:**
# -   For "fill" commands, you MUST extract both the target field label and the value.
# -   **When extracting an email address, be literal and convert spoken words to symbols. For example, "my email is test at example dot com" MUST result in "value": "test@example.com".**
# -   `direction` MUST be `null` unless the action is `"scroll"`.

# **COMMAND ANALYSIS:**
# The user said: "{user_text}"

# **EXAMPLES:**
# - User command: "go to the communication page" -> {{"action": "goToPage", "target": "/communication"}}
# - User command: "click the logout button" -> {{"action": "click", "target": "Logout"}}
# - User command: "fill the Full Name field with John Doe" -> {{"action": "fillInput", "target": "Full Name", "value": "John Doe"}}
# - User command: "my email address is example at test dot com" -> {{"action": "fillInput", "target": "Email Address", "value": "example@test.com"}}

# Now, generate ONLY the JSON object for the user's command.
# """
#     try:
#         response = model.generate_content(prompt)
#         ai_response_text = response.text.strip().replace("```json", "").replace("```", "")
#         parsed_json = json.loads(ai_response_text)
#         return parsed_json
#     except Exception as e:
#         print(f"Error parsing website command JSON: {e}")
#         return {"action": "unknown"}

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# import google.generativeai as genai
# from dotenv import load_dotenv
# import json
# from mail_sender import send_emergency_email

# load_dotenv()
# app = Flask(__name__)
# CORS(app)

# # --- Using a single, unified model for simplicity and stability ---
# model = None
# try:
#     # This is the stable configuration method you requested
#     api_key = os.getenv('VOICE_BOT_API_KEY')
#     if api_key:
#         genai.configure(api_key=api_key)
#         # We will use 'gemini-1.5-flash' as it is fast and has proven to be stable with your library version
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         print("✅ Gemini AI model configured successfully.")
#     else:
#         print("❌ CRITICAL: GEMINI_API_KEY not found in .env file. AI features will fail.")

# except Exception as e:
#     print(f"❌ CRITICAL: An error occurred during Gemini AI model configuration: {e}")


# @app.route('/health', methods=['GET'])
# def health_check():
#     return jsonify({"status": "healthy", "message": "Sarathi Voice Bot API is running!"})


# # The /generate-game endpoint has been removed.

# @app.route('/process-command', methods=['POST'])
# def process_voice_command():
#     if not model:
#         return jsonify({"error": "AI model is not configured"}), 500
#     try:
#         data = request.get_json()
#         user_text = data.get('text', '').strip()
#         page_commands = data.get('page_commands', [])
#         location = data.get('location', None)

#         intent = classify_intent(user_text)
        
#         if intent == "EMERGENCY_HELP":
#             success = send_emergency_email(location)
#             response = {"type": "HELP_ACTION", "payload": {"status": "success" if success else "failed"}}
#         elif intent == "WEBSITE_COMMAND":
#             command_payload = get_website_command_json(user_text, page_commands)
#             response = {"type": "WEBSITE_COMMAND", "payload": command_payload}
#         else:
#             answer_text = get_general_answer(user_text)
#             response = {"type": "GENERAL_ANSWER", "payload": {"text_to_speak": answer_text}}
        
#         return jsonify(response)
#     except Exception as e:
#         return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# def classify_intent(user_text):
#     # Removed PLAY_GAME from the prompt categories
#     prompt = f"""Categorize the user's command as WEBSITE_COMMAND, GENERAL_QUESTION, or EMERGENCY_HELP. Respond with ONLY the category name. User text: "{user_text}" """
#     try:
#         return model.generate_content(prompt).text.strip()
#     except Exception as e:
#         print(f"Error in intent classification: {e}")
#         return "UNKNOWN"

# def get_general_answer(user_text):
#     prompt = f"""Directly answer the user's question in a single sentence. User question: "{user_text}" Answer:"""
#     try:
#         return model.generate_content(prompt).text.strip()
#     except Exception as e:
#         print(f"Error getting general answer: {e}")
#         return "I'm sorry, I can't answer that right now."


# def get_website_command_json(user_text, page_commands):
#     if not page_commands:
#         page_commands = ["home", "features", "about", "services", "contact", "community", "join"]

#     global_links = ["Communication", "Education", "Stories", "Mission", "Profile", "Logout", "Sign Up", "Create Account"]
#     valid_targets_str = ", ".join([f'"{cmd}"' for cmd in page_commands])
#     global_links_str = ", ".join([f'"{link}"' for link in global_links])
#     form_fields = ["Full Name", "Email Address", "Password", "Confirm Password"]
#     form_fields_str = ", ".join([f'"{field}"' for field in form_fields])

#     prompt = f"""
# You are a precise JSON interpreter for a website's voice control system. Your ONLY job is to convert the user's command into a perfectly structured JSON object.

# **AVAILABLE ACTIONS & TARGETS:**
# 1.  **Fill a form field:** Use `action: "fillInput"`.
# 2.  **Click a button or link:** Use `action: "click"`.
# 3.  **Navigate to a different page:** Use `action: "goToPage"`.
# 4.  **Scroll to a section on the current page:** Use `action: "navigate"`.
# 5.  **General Scrolling:** Use `action: "scroll"`.

# **CONTEXT:**
# -   **Global Clickable Elements:** {global_links_str}
# -   **Form Fields on This Page:** {form_fields_str}
# -   **Scrollable Sections on This Page:** {valid_targets_str}

# **CRITICAL RULES:**
# -   For "fill" commands, extract both the target field label and the value.
# -   When extracting an email, convert spoken words like "at" and "dot" to symbols (e.g., "test@example.com").

# **COMMAND ANALYSIS:**
# The user said: "{user_text}"

# **EXAMPLES:**
# - User command: "go to the communication page" -> {{"action": "goToPage", "target": "/communication"}}
# - User command: "click the logout button" -> {{"action": "click", "target": "Logout"}}
# - User command: "my email is example at test dot com" -> {{"action": "fillInput", "target": "Email Address", "value": "example@test.com"}}
# - User command: "click Create Account" -> {{"action": "click", "target": "Create Account"}}

# Now, generate ONLY the JSON object for the user's command.
# """
#     try:
#         response = model.generate_content(prompt)
#         ai_response_text = response.text.strip().replace("```json", "").replace("```", "")
#         parsed_json = json.loads(ai_response_text)
#         return parsed_json
#     except Exception as e:
#         print(f"Error parsing website command JSON: {e}")
#         return {"action": "unknown"}

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
# 1. UPDATED: Import the new, more powerful alert function
from alert_sender import send_emergency_alerts 

load_dotenv()
app = Flask(__name__)
CORS(app)

# --- Using a single, unified model for simplicity and stability ---
model = None
try:
    # This is the stable configuration method you requested
    api_key = os.getenv('VOICE_BOT_API_KEY')
    if api_key:
        genai.configure(api_key=api_key)
        # We will use 'gemini-2.5-flash' as it is fast and has proven to be stable with library version
        model = genai.GenerativeModel('gemini-2.5-flash')
        print("✅ Gemini AI model configured successfully.")
    else:
        print("❌ CRITICAL: GEMINI_API_KEY not found in .env file. AI features will fail.")

except Exception as e:
    print(f"❌ CRITICAL: An error occurred during Gemini AI model configuration: {e}")


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Sarathi Voice Bot API is running!"})


# The /generate-game endpoint has been removed.

@app.route('/process-command', methods=['POST'])
def process_voice_command():
    if not model:
        return jsonify({"error": "AI model is not configured"}), 500
    try:
        data = request.get_json()
        user_text = data.get('text', '').strip()
        page_commands = data.get('page_commands', [])
        location = data.get('location', None)

        intent = classify_intent(user_text)
        
        if intent == "EMERGENCY_HELP":
            # 2. UPDATED: Call the new multi-channel alert function
            success = send_emergency_alerts(location)
            response = {"type": "HELP_ACTION", "payload": {"status": "success" if success else "failed"}}
        elif intent == "WEBSITE_COMMAND":
            command_payload = get_website_command_json(user_text, page_commands)
            response = {"type": "WEBSITE_COMMAND", "payload": command_payload}
        else:
            answer_text = get_general_answer(user_text)
            response = {"type": "GENERAL_ANSWER", "payload": {"text_to_speak": answer_text}}
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


def classify_intent(user_text):
    # Removed PLAY_GAME from the prompt categories
    prompt = f"""Categorize the user's command as WEBSITE_COMMAND, GENERAL_QUESTION, or EMERGENCY_HELP. Respond with ONLY the category name. User text: "{user_text}" """
    try:
        return model.generate_content(prompt).text.strip()
    except Exception as e:
        print(f"Error in intent classification: {e}")
        return "UNKNOWN"

def get_general_answer(user_text):
    prompt = f"""Directly answer the user's question in a single sentence. User question: "{user_text}" Answer:"""
    try:
        return model.generate_content(prompt).text.strip()
    except Exception as e:
        print(f"Error getting general answer: {e}")
        return "I'm sorry, I can't answer that right now."


def get_website_command_json(user_text, page_commands):
    if not page_commands:
        page_commands = ["home", "features", "about", "services", "contact", "community", "join"]

    global_links = ["Communication", "Education", "Stories", "Mission", "Profile", "Logout", "Sign Up", "Create Account"]
    valid_targets_str = ", ".join([f'"{cmd}"' for cmd in page_commands])
    global_links_str = ", ".join([f'"{link}"' for link in global_links])
    form_fields = ["Full Name", "Email Address", "Password", "Confirm Password"]
    form_fields_str = ", ".join([f'"{field}"' for field in form_fields])

    prompt = f"""
You are a precise JSON interpreter for a website's voice control system. Your ONLY job is to convert the user's command into a perfectly structured JSON object.

**AVAILABLE ACTIONS & TARGETS:**
1.  **Fill a form field:** Use `action: "fillInput"`.
2.  **Click a button or link:** Use `action: "click"`.
3.  **Navigate to a different page:** Use `action: "goToPage"`.
4.  **Scroll to a section on the current page:** Use `action: "navigate"`.
5.  **General Scrolling:** Use `action: "scroll"`.

**CONTEXT:**
-   **Global Clickable Elements:** {global_links_str}
-   **Form Fields on This Page:** {form_fields_str}
-   **Scrollable Sections on This Page:** {valid_targets_str}

**CRITICAL RULES:**
-   For "fill" commands, extract both the target field label and the value.
-   When extracting an email, convert spoken words like "at" and "dot" to symbols (e.g., "test@example.com").

**COMMAND ANALYSIS:**
The user said: "{user_text}"

**EXAMPLES:**
- User command: "go to the communication page" -> {{"action": "goToPage", "target": "/communication"}}
- User command: "click the logout button" -> {{"action": "click", "target": "Logout"}}
- User command: "my email is example at test dot com" -> {{"action": "fillInput", "target": "Email Address", "value": "example@test.com"}}
- User command: "click Create Account" -> {{"action": "click", "target": "Create Account"}}

Now, generate ONLY the JSON object for the user's command.
"""
    try:
        response = model.generate_content(prompt)
        ai_response_text = response.text.strip().replace("```json", "").replace("```", "")
        parsed_json = json.loads(ai_response_text)
        return parsed_json
    except Exception as e:
        print(f"Error parsing website command JSON: {e}")
        return {"action": "unknown"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



