"""
Offline Flask Backend Server - 100% Offline Windows Automation Chatbot
No internet required - Uses local NLP and Windows automation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import offline NLP and Windows automation
from offline_nlp import parse_with_fuzzy_nlp
from windows_automation import execute_automation, automation

# Import LLM-based program generator
try:
    from llm_program_generator import LLMProgramGenerator
    LLM_AVAILABLE = True
except Exception as e:
    print(f"⚠️ LLM Program Generator not available: {e}")
    LLM_AVAILABLE = False

# Import template-based fallback generator
try:
    from offline_program_generator import generate_program as template_generate_program
    TEMPLATE_GENERATOR_AVAILABLE = True
    print("✅ Template-based Program Generator loaded")
except Exception as e:
    print(f"⚠️ Template generator not available: {e}")
    TEMPLATE_GENERATOR_AVAILABLE = False
    template_generate_program = None

# Initialize LLM generator if available
llm_generator = None
if LLM_AVAILABLE:
    try:
        llm_generator = LLMProgramGenerator()
        # Check if Ollama is actually running
        if llm_generator.llm.is_available():
            print("✅ LLM Program Generator initialized (Ollama running)")
        else:
            print("⚠️ LLM available but Ollama not running - will use template fallback")
            llm_generator = None
    except Exception as e:
        print(f"⚠️ Could not initialize LLM generator: {e}")
        llm_generator = None

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Chat history
chat_history = []

# Welcome message
WELCOME_MESSAGE = """
🤖 Welcome to Windows Automation Chatbot with AI Code Generation!

✅ 100% Offline - No internet required
✅ Fuzzy matching - Typos are okay!
✅ Natural language understanding
✅ Smart Code Generation - Templates + Optional AI!

System Commands:
• "open calculator"
• "check battery"
• "show cpu usage"

🆕 Code Generation:
• "write python program for sum of two numbers"
• "generate java program for prime number"
• "create c program to calculate factorial"
• "write cpp program for fibonacci sequence"

💡 Available Templates:
   ✓ Sum of 2/3 numbers, Prime number, Factorial
   ✓ Fibonacci, Palindrome, Reverse string
   ✓ Array sum, Bubble sort, Binary search
   ✓ GCD, LCM

Type 'help' to see all available commands!
"""


@app.route('/', methods=['GET'])
def home():
    """Home route - API status"""
    return jsonify({
        'status': 'online',
        'message': 'Offline Windows Automation Chatbot API with AI Code Generation',
        'version': '2.0.1',
        'mode': 'offline',
        'features': {
            'windows_automation': True,
            'llm_code_generation': llm_generator is not None,
            'template_code_generation': TEMPLATE_GENERATOR_AVAILABLE,
            'auto_validation': llm_generator is not None,
            'multi_language': True
        },
        'endpoints': {
            'chat': '/api/chat',
            'status': '/api/status',
            'history': '/api/history',
            'clear': '/api/clear',
            'generate_program': '/api/generate-program',
            'llm_status': '/api/llm-status',
            'validate_code': '/api/validate-code'
        }
    })


@app.route('/api/status', methods=['GET'])
def status():
    """Get system status"""
    return jsonify({
        'status': 'online',
        'mode': 'offline',
        'internet_required': False,
        'nlp_engine': 'RapidFuzz (Offline)',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint - Process user messages with offline NLP
    
    Request body:
    {
        "message": "user command"
    }
    
    Response:
    {
        "status": "success",
        "response": "bot response",
        "intent": "detected_intent",
        "confidence": 95,
        "mode": "offline"
    }
    """
    try:
        # Get user message
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'status': 'error',
                'response': '❌ Please provide a message'
            })
        
        user_message = data['message']
        
        # Check if this is a program generation request
        is_program_request = any(keyword in user_message.lower() for keyword in [
            'write', 'generate', 'create', 'make', 'program', 'code', 'script'
        ]) and any(lang in user_message.lower() for lang in [
            'python', 'java', 'c++', 'cpp', ' c ', 'program'
        ])
        
        # Try LLM program generation first if it's a program request
        if is_program_request and llm_generator:
            print("🤖 Detected program generation request - trying LLM")
            try:
                result = llm_generator.generate_program(user_message)
                
                if result['success']:
                    bot_response = result['message']
                    intent = 'generate_program_llm'
                    confidence = 95
                    params = {'language': result.get('language'), 'filepath': result.get('filepath')}
                else:
                    # Fall back to template-based if LLM fails
                    print("⚠️ LLM failed, falling back to template generator")
                    raise Exception("LLM generation failed")
                    
            except Exception as e:
                print(f"⚠️ LLM generation error: {e}, trying template generator")
                # Fallback to template-based generator
                if TEMPLATE_GENERATOR_AVAILABLE and template_generate_program:
                    try:
                        # Extract language and topic from message
                        from offline_program_generator import normalize_language, fuzzy_topic
                        language = normalize_language(user_message)
                        topic = fuzzy_topic(user_message)
                        
                        # Get Desktop as default location
                        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
                        
                        result = template_generate_program(
                            user_text=user_message,
                            language=language,
                            topic=topic,
                            base_dir=desktop_path
                        )
                        
                        if result.get('ok'):
                            bot_response = result['message']
                            intent = 'generate_program_template'
                            confidence = 85
                            params = {'language': language, 'topic': topic}
                        else:
                            bot_response = result.get('message', '❌ Failed to generate program')
                            intent = 'generate_program_error'
                            confidence = 0
                            params = None
                    except Exception as template_error:
                        print(f"❌ Template generation also failed: {template_error}")
                        bot_response = f"❌ Unable to generate program. Error: {str(template_error)}"
                        intent = 'generate_program_error'
                        confidence = 0
                        params = None
                else:
                    bot_response = "❌ Program generation is not available. Please install Ollama and pull a code model."
                    intent = 'generate_program_error'
                    confidence = 0
                    params = None
        else:
            # Parse command with offline NLP for system commands
            nlp_result = parse_with_fuzzy_nlp(user_message)
            
            intent = nlp_result['intent']
            confidence = nlp_result['confidence']
            params = nlp_result.get('params', None)
            
            print(f"🧠 Intent: {intent} (confidence: {confidence}%)")
            if params:
                print(f"📋 Params: {params}")
            
            # Execute automation if intent detected
            if intent:
                bot_response = execute_automation(intent, params)
            else:
                bot_response = (
                    "❓ I didn't understand that command.\n\n"
                    "System commands:\n"
                    "• 'open calculator'\n"
                    "• 'check battery'\n"
                    "• 'create folder test'\n\n"
                    "AI Code Generation:\n"
                    "• 'write python program for [task]'\n"
                    "• 'generate java program for [task]'\n"
                    "• 'create c++ program for [task]'\n\n"
                    "Type 'help' to see all available commands!"
                )
        
        # Add to chat history
        chat_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_message,
            'bot': bot_response,
            'intent': intent,
            'confidence': confidence
        })
        
        # Keep only last 100 messages
        if len(chat_history) > 100:
            chat_history.pop(0)
        
        print(f"📤 Response: {bot_response[:100]}...")
        
        # Return response
        return jsonify({
            'status': 'success',
            'response': bot_response,
            'intent': intent,
            'confidence': confidence,
            'mode': 'offline',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            'status': 'error',
            'response': f'❌ Server error: {str(e)}'
        }), 500


@app.route('/api/history', methods=['GET'])
def history():
    """Get chat history"""
    limit = request.args.get('limit', 50, type=int)
    return jsonify({
        'status': 'success',
        'history': chat_history[-limit:],
        'count': len(chat_history)
    })


@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear chat history"""
    global chat_history
    chat_history = []
    return jsonify({
        'status': 'success',
        'message': 'Chat history cleared'
    })


@app.route('/api/system', methods=['GET'])
def system_info():
    """Get quick system info"""
    try:
        summary = automation.system_summary()
        return jsonify({
            'status': 'success',
            'summary': summary
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/generate-program', methods=['POST'])
def generate_program_endpoint():
    """
    Generate program using LLM or template fallback
    
    Request body:
    {
        "request": "program description",
        "language": "python|java|c|cpp" (optional),
        "output_dir": "path" (optional, defaults to Desktop),
        "validate": true (optional, default: true)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'request' not in data:
            return jsonify({
                'status': 'error',
                'response': '❌ Please provide a program request'
            }), 400
        
        program_request = data.get('request', '').strip()
        language = data.get('language', None)
        output_dir = data.get('output_dir', None)
        validate = data.get('validate', True)
        
        if not program_request:
            return jsonify({
                'status': 'error',
                'response': '❌ Program request cannot be empty'
            }), 400
        
        print(f"\n🤖 Program Generation Request: {program_request}")
        print(f"   Language: {language or 'auto-detect'}")
        print(f"   Validate: {validate}")
        
        # Try LLM first if available
        if llm_generator:
            try:
                # Generate program
                result = llm_generator.generate_program(
                    program_request,
                    language=language,
                    output_dir=output_dir,
                    validate=validate
                )
                
                if result['success']:
                    return jsonify({
                        'status': 'success',
                        'response': result['message'],
                        'code': result['code'],
                        'filepath': result['filepath'],
                        'language': result['language'],
                        'validated': result.get('validated', False),
                        'attempts': result.get('attempts', 1),
                        'model': result.get('model', 'LLM'),
                        'generator': 'llm'
                    })
                else:
                    # Try template fallback
                    print("⚠️ LLM failed, trying template generator")
                    raise Exception("LLM generation failed")
            except Exception as e:
                print(f"⚠️ LLM error: {e}, falling back to templates")
        
        # Fallback to template-based generator
        if TEMPLATE_GENERATOR_AVAILABLE and template_generate_program:
            try:
                from offline_program_generator import normalize_language, fuzzy_topic
                
                # Detect language and topic
                detected_language = language or normalize_language(program_request)
                topic = fuzzy_topic(program_request)
                
                # Set default output directory
                if not output_dir:
                    output_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
                
                result = template_generate_program(
                    user_text=program_request,
                    language=detected_language,
                    topic=topic,
                    base_dir=output_dir
                )
                
                if result.get('ok'):
                    return jsonify({
                        'status': 'success',
                        'response': result['message'],
                        'code': result.get('code', ''),
                        'filepath': result.get('filepath', ''),
                        'language': detected_language or 'unknown',
                        'validated': False,
                        'attempts': 1,
                        'model': 'template',
                        'generator': 'template'
                    })
                else:
                    return jsonify({
                        'status': 'error',
                        'response': result.get('message', '❌ Template generation failed'),
                        'generator': 'template'
                    }), 422
            except Exception as template_error:
                print(f"❌ Template generation error: {template_error}")
                import traceback
                traceback.print_exc()
                return jsonify({
                    'status': 'error',
                    'response': f'❌ Template generation error: {str(template_error)}'
                }), 500
        else:
            return jsonify({
                'status': 'error',
                'response': '❌ No program generator available. Please install Ollama or ensure template generator is loaded.'
            }), 503
    
    except Exception as e:
        print(f"❌ Error in generate_program: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'response': f'❌ Server error: {str(e)}'
        }), 500


@app.route('/api/llm-status', methods=['GET'])
def llm_status():
    """Get LLM service status"""
    if not LLM_AVAILABLE or not llm_generator:
        return jsonify({
            'status': 'unavailable',
            'message': 'LLM Program Generator is not loaded',
            'available': False
        })
    
    try:
        is_available = llm_generator.llm.is_available()
        models = llm_generator.llm.list_models() if is_available else []
        compilers = llm_generator.validator.get_compiler_status()
        
        return jsonify({
            'status': 'online' if is_available else 'offline',
            'available': is_available,
            'current_model': llm_generator.llm.model if is_available else None,
            'available_models': models,
            'compilers': compilers,
            'message': 'LLM service is running' if is_available else 'Ollama service is not running'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'available': False
        }), 500


@app.route('/api/validate-code', methods=['POST'])
def validate_code():
    """
    Validate code without saving
    
    Request body:
    {
        "code": "source code",
        "language": "python|java|c|cpp"
    }
    """
    if not LLM_AVAILABLE or not llm_generator:
        return jsonify({
            'status': 'error',
            'response': '❌ Code validator is not available'
        }), 503
    
    try:
        data = request.get_json()
        
        if not data or 'code' not in data or 'language' not in data:
            return jsonify({
                'status': 'error',
                'response': '❌ Please provide code and language'
            }), 400
        
        code = data['code']
        language = data['language'].lower()
        
        # Validate code
        is_valid, error_message = llm_generator.validator.validate(code, language)
        
        return jsonify({
            'status': 'success',
            'valid': is_valid,
            'error': error_message,
            'language': language
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'response': f'❌ Validation error: {str(e)}'
        }), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("=" * 70)
    print("🤖 OFFLINE WINDOWS AUTOMATION CHATBOT SERVER WITH AI CODE GENERATION")
    print("=" * 70)
    print("✅ Mode: 100% OFFLINE")
    print("✅ NLP Engine: RapidFuzz (Fuzzy Matching)")
    print("✅ AI Code Generation: " + ("ENABLED" if LLM_AVAILABLE else "DISABLED"))
    if LLM_AVAILABLE and llm_generator:
        print(f"✅ LLM Model: {llm_generator.llm.model if llm_generator.llm.is_available() else 'Not running'}")
        print(f"✅ Ollama Status: {'Running' if llm_generator.llm.is_available() else 'Not running'}")
        compilers = llm_generator.validator.get_compiler_status()
        print(f"✅ Compilers: Python={'✓' if compilers.get('python') else '✗'}, "
              f"Java={'✓' if compilers.get('javac') else '✗'}, "
              f"C={'✓' if compilers.get('gcc') else '✗'}, "
              f"C++={'✓' if compilers.get('g++') else '✗'}")
    print("✅ Internet Required: NO")
    print("=" * 70)
    print(f"🌐 Server starting on: http://localhost:5000")
    print(f"📱 Frontend URL: http://localhost:3000")
    print("=" * 70)
    if not LLM_AVAILABLE or (llm_generator and not llm_generator.llm.is_available()):
        print("\n⚠️  OLLAMA NOT RUNNING - AI Code Generation will not work!")
        print("📖 Setup instructions:")
        print("   1. Download Ollama from: https://ollama.ai")
        print("   2. Install and start Ollama")
        print("   3. Run: ollama pull codellama:7b")
        print("   4. Restart this server")
        print("=" * 70)
    print("🤖 OFFLINE WINDOWS AUTOMATION CHATBOT SERVER")
    print("=" * 60)
    print("✅ Mode: 100% OFFLINE")
    print("✅ NLP Engine: RapidFuzz (Fuzzy Matching)")
    print("✅ Internet Required: NO")
    print("=" * 60)
    print(f"🌐 Server starting on: http://localhost:5000")
    print(f"📱 Frontend URL: http://localhost:3000")
    print("=" * 60)
    print("\n🚀 Server is ready! Open http://localhost:3000 in your browser\n")
    
    # Run Flask server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
