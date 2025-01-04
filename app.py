import google.generativeai as genai
import os
from flask import Flask, render_template, request, jsonify
from difflib import SequenceMatcher
from dotenv import load_dotenv  # Import dotenv

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Fetch the Google API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Google API key not found. Ensure GOOGLE_API_KEY is set in the .env file.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-1.5-pro")

# Global variables to store conversation history and context
conversation_history = []

# Voice assistance function with enhanced topic management
def voice_assistance(user_input):
    global conversation_history

    # Improved prompt with focus on concise and direct answers
    prompt = f"""
    You are an AI assistant in an engaging conversation with a user. The user just asked the following question:
    '{user_input}'
    Provide a direct and informative answer, focusing on the exact details the user is asking for. Avoid unnecessary elaboration or asking follow-up questions unless essential to the user’s inquiry. Keep the response clear, concise, and to the point. If the topic is complex, briefly summarize the key aspects.
    """

    response = model.generate_content(prompt).text

    # Update conversation history
    conversation_history.append({
        'user': user_input,
        'ai': response
    })

    return response


# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle voice input and return model response with conversation history
@app.route('/process_voice', methods=['POST'])
def process_voice():
    user_input = request.json.get("user_input")
    response = voice_assistance(user_input)

    # Return the updated conversation history
    return jsonify({'response': response, 'conversation_history': conversation_history})


if __name__ == '__main__':
    app.run(debug=True)
