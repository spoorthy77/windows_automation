"""
Flask Backend Server - Bridges React frontend with Python automation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path to import automation modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from command_parser import parse_command

app = Flask(__name__)
CORS(app)

# Frok API Configuration - SECURE: Use environment variable
FROK_API_KEY = os.getenv('FROK_API_KEY')
FROK_API_URL = 'https://api.frok.ai/v1/chat/completions'

# Validate API key is loaded
if not FROK_API_KEY:
    print("⚠️ WARNING: FROK_API_KEY not found in environment variables!")
    print("Please create a .env file with your API key.")
else:
    print(f"✅ Frok API Key loaded: {FROK_API_KEY[:10]}...{FROK_API_KEY[-10:]}")

# Chat history for context
chat_history = []

def enhance_response_with_frok(user_message, automation_response):
    """
    Enhance automation response using Frok AI API
    Falls back to automation response if Frok API fails
    """
    if not FROK_API_KEY:
        return automation_response
    
    try:
        headers = {
            'Authorization': f'Bearer {FROK_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'gpt-4',
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a helpful Windows automation assistant. Keep responses concise and friendly.'
                },
                {
                    'role': 'user',
                    'content': f"User asked: '{user_message}'\nAutomation response: '{automation_response}'\nProvide a brief, friendly enhancement or explanation."
                }
            ],
            'temperature': 0.7,
            'max_tokens': 150
        }
        
        response = requests.post(
            FROK_API_URL,
            headers=headers,
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            frok_response = response.json()
            enhanced = frok_response['choices'][0]['message']['content'].strip()
            return f"{automation_response}\n\n💡 {enhanced}"
        else:
            print(f"⚠️ Frok API returned status {response.status_code}")
            return automation_response
            
    except Exception as e:
        print(f"⚠️ Frok API error: {str(e)}")
        return automation_response

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint - processes user messages
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'status': 'error',
                'response': '❌ Please enter a message'
            }), 400
        
        # Log the message
        print(f"\n📥 Received: {user_message}")
        
        # Process command with Windows automation
        automation_response = parse_command(user_message)
        
        # Enhance with Frok AI (if available)
        final_response = enhance_response_with_frok(user_message, automation_response)
        
        # Add to chat history
        chat_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_message,
            'assistant': final_response,
            'frok_enhanced': final_response != automation_response
        })
        
        # Keep only last 50 messages
        if len(chat_history) > 50:
            chat_history.pop(0)
        
        print(f"📤 Response: {final_response[:100]}...")
        
        return jsonify({
            'status': 'success',
            'response': final_response,
            'frok_api_integrated': FROK_API_KEY is not None,
            'frok_enhanced': final_response != automation_response
        })
        
    except Exception as e:
        error_msg = f"❌ Error processing message: {str(e)}"
        print(error_msg)
        return jsonify({
            'status': 'error',
            'response': error_msg
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'Windows Automation Backend is running',
        'frok_api_configured': FROK_API_KEY is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/help', methods=['GET'])
def help_endpoint():
    """Return help information"""
    help_text = """
🤖 Windows Automation Assistant - Available Commands:

📂 File Operations:
  • open file explorer / open explorer
  • open downloads / open documents
  • create folder [name]
  • delete file [name]

⚙️ System Commands:
  • check battery / battery status
  • check disk space / disk info
  • check memory / ram info
  • system info / os info
  • shutdown / restart / sleep

🌐 Applications:
  • open [app name] - calculator, notepad, chrome, etc.
  • close [app name]
  • list running apps

🔧 Settings:
  • open settings / control panel
  • wifi settings / bluetooth settings
  • display settings / sound settings

📊 Monitoring:
  • cpu usage / network usage
  • list processes
  • task manager

💬 Chat:
  • help - show this message
  • clear history - clear chat history

Just type naturally - I understand variations! ✨
    """
    return jsonify({
        'status': 'success',
        'help_text': help_text
    })

@app.route('/api/history', methods=['GET'])
def get_history():
    """Return chat history"""
    return jsonify({
        'status': 'success',
        'history': chat_history
    })

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear chat history"""
    global chat_history
    chat_history = []
    return jsonify({
        'status': 'success',
        'message': 'Chat history cleared'
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("\n" + "="*70)
    print("🚀 Windows Automation Backend Server")
    print("="*70)
    print(f"📡 Running on: http://127.0.0.1:{port}")
    print(f"🔑 Frok API: {'✅ Configured' if FROK_API_KEY else '❌ Not configured'}")
    print(f"🐛 Debug mode: {'✅ Enabled' if debug else '❌ Disabled'}")
    print("="*70)
    print("Press CTRL+C to quit\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
