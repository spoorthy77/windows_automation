"""
Online Mode Handler - Grok API Integration

This module handles online mode using xAI's Grok API for natural language understanding
and intelligent command processing when internet is available.
"""

import os
import json
import requests
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GrokAPIHandler:
    """
    Handles communication with Grok (xAI) API for online mode.
    """
    
    def __init__(self):
        """Initialize Grok API handler with credentials."""
        self.api_key = os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY")
        self.base_url = "https://api.x.ai/v1"
        self.model = "grok-beta"
        
        # System prompt for Windows automation
        self.system_prompt = """You are a Windows automation assistant. Your job is to understand user commands and extract the automation intent.

When the user asks you to do something, respond with a JSON object containing:
{
    "intent": "<action_name>",
    "parameters": {<optional parameters>},
    "response": "<friendly response to user>"
}

Available intents:
- open_notepad, open_calculator, open_chrome, open_cmd, open_whatsapp, open_task_manager
- open_settings, open_network_settings
- list_files, create_folder, delete_folder, open_folder
- cpu_usage, memory_usage, battery_status, check_storage, system_info, system_summary
- show_ip, show_datetime, show_running_processes
- mute_volume, increase_volume, decrease_volume
- turn_on_bluetooth, turn_off_bluetooth
- enable_night_theme, disable_night_theme
- lock_pc, shutdown_pc, restart_pc, cancel_shutdown

For folder operations, extract the folder name in parameters as "folder_name".
For unclear commands, set intent to "unknown" and provide a helpful response.

Examples:
User: "open settings please"
Response: {"intent": "open_settings", "parameters": {}, "response": "Opening Windows settings for you!"}

User: "can you check my RAM usage?"
Response: {"intent": "memory_usage", "parameters": {}, "response": "Checking your memory usage now!"}

User: "create a folder named MyFiles"
Response: {"intent": "create_folder", "parameters": {"folder_name": "MyFiles"}, "response": "Creating folder MyFiles for you!"}

Always respond with valid JSON only."""
    
    def is_configured(self) -> bool:
        """Check if API key is configured."""
        return self.api_key is not None and len(self.api_key) > 0
    
    def parse_command(self, user_input: str) -> Dict:
        """
        Send user command to Grok API and parse the intent.
        
        Args:
            user_input: User's natural language command
            
        Returns:
            Dict with intent, parameters, and response
        """
        if not self.is_configured():
            return {
                "intent": "error",
                "parameters": {},
                "response": "⚠️ Grok API key not configured. Using offline mode.",
                "error": "API key missing"
            }
        
        try:
            # Prepare API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.3,
                "max_tokens": 500
            }
            
            # Make API request
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"].strip()
                
                # Parse JSON response
                try:
                    parsed = json.loads(content)
                    return parsed
                except json.JSONDecodeError:
                    # Try to extract JSON from markdown code blocks
                    if "```json" in content:
                        json_start = content.find("```json") + 7
                        json_end = content.find("```", json_start)
                        content = content[json_start:json_end].strip()
                        parsed = json.loads(content)
                        return parsed
                    elif "```" in content:
                        json_start = content.find("```") + 3
                        json_end = content.find("```", json_start)
                        content = content[json_start:json_end].strip()
                        parsed = json.loads(content)
                        return parsed
                    else:
                        return {
                            "intent": "unknown",
                            "parameters": {},
                            "response": content,
                            "raw_response": content
                        }
            
            elif response.status_code == 401:
                return {
                    "intent": "error",
                    "parameters": {},
                    "response": "⚠️ Invalid API key. Please check your Grok API key.",
                    "error": "Authentication failed"
                }
            
            else:
                return {
                    "intent": "error",
                    "parameters": {},
                    "response": f"⚠️ API error (status {response.status_code}). Using offline mode.",
                    "error": f"HTTP {response.status_code}"
                }
        
        except requests.Timeout:
            return {
                "intent": "error",
                "parameters": {},
                "response": "⚠️ API request timed out. Using offline mode.",
                "error": "Timeout"
            }
        
        except requests.RequestException as e:
            return {
                "intent": "error",
                "parameters": {},
                "response": f"⚠️ Network error: {str(e)}. Using offline mode.",
                "error": str(e)
            }
        
        except Exception as e:
            return {
                "intent": "error",
                "parameters": {},
                "response": f"⚠️ Unexpected error: {str(e)}",
                "error": str(e)
            }
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Test if Grok API is accessible and working.
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if not self.is_configured():
            return False, "API key not configured"
        
        try:
            test_result = self.parse_command("test connection")
            
            if "error" in test_result:
                return False, test_result.get("error", "Unknown error")
            else:
                return True, "Grok API connected successfully"
        
        except Exception as e:
            return False, str(e)


# Global instance
grok_handler = GrokAPIHandler()


def parse_with_grok(user_input: str) -> Dict:
    """
    Parse user command using Grok API.
    
    Args:
        user_input: User's natural language command
        
    Returns:
        Dict with intent, parameters, and response
    """
    return grok_handler.parse_command(user_input)


def is_grok_configured() -> bool:
    """Check if Grok API is configured."""
    return grok_handler.is_configured()


if __name__ == "__main__":
    # Test the Grok API handler
    print("🧪 Testing Grok API Handler...")
    print("=" * 50)
    
    if not is_grok_configured():
        print("⚠️  Grok API key not found in environment variables")
        print("💡 Set GROK_API_KEY or XAI_API_KEY in .env file")
    else:
        print("✅ API key found!")
        print("\n🔍 Testing connection...")
        
        success, message = grok_handler.test_connection()
        if success:
            print(f"✅ {message}")
            
            # Test a sample command
            print("\n📝 Testing sample command: 'open calculator'")
            result = parse_with_grok("open calculator")
            print(f"Intent: {result.get('intent')}")
            print(f"Response: {result.get('response')}")
        else:
            print(f"❌ Connection failed: {message}")
    
    print("=" * 50)
