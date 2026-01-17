"""
Hybrid Chatbot Core - Automatic Online/Offline Mode Switching

This is the core engine that automatically detects internet connectivity
and switches between online (Grok API) and offline (local NLP) modes seamlessly.
"""

import os
from typing import Dict, Tuple
from network_detector import check_internet, get_connection_status
from online_mode_handler import parse_with_grok, is_grok_configured
from offline_mode_handler import parse_offline
from logger import log_event

# Import all automation actions
from actions import (
    list_files,
    show_ip,
    system_info,
    system_summary,
    cpu_usage,
    memory_usage,
    open_notepad,
    open_calculator,
    open_cmd,
    open_chrome,
    create_folder,
    delete_folder,
    open_folder,
    show_datetime,
    battery_status,
    shutdown_pc,
    restart_pc,
    cancel_shutdown,
    lock_pc,
    enable_night_theme,
    open_whatsapp,
    check_storage,
    open_task_manager,
    show_running_processes,
    mute_volume,
    increase_volume,
    decrease_volume,
    open_settings,
    open_network_settings,
    turn_on_bluetooth,
    turn_off_bluetooth,
    generate_program
)


class HybridChatbot:
    """
    Hybrid chatbot that automatically switches between online and offline modes.
    """
    
    def __init__(self):
        """Initialize the hybrid chatbot."""
        self.current_mode = None
        self.online_available = False
        self.grok_configured = is_grok_configured()
        
        # Map intents to action functions
        self.action_map = {
            "list_files": list_files,
            "show_ip": show_ip,
            "system_info": system_info,
            "system_summary": system_summary,
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "open_notepad": open_notepad,
            "open_calculator": open_calculator,
            "open_cmd": open_cmd,
            "open_chrome": open_chrome,
            "create_folder": create_folder,
            "delete_folder": delete_folder,
            "open_folder": open_folder,
            "show_datetime": show_datetime,
            "battery_status": battery_status,
            "shutdown_pc": shutdown_pc,
            "restart_pc": restart_pc,
            "cancel_shutdown": cancel_shutdown,
            "lock_pc": lock_pc,
            "enable_night_theme": enable_night_theme,
            "open_whatsapp": open_whatsapp,
            "check_storage": check_storage,
            "open_task_manager": open_task_manager,
            "show_running_processes": show_running_processes,
            "mute_volume": mute_volume,
            "increase_volume": increase_volume,
            "decrease_volume": decrease_volume,
            "open_settings": open_settings,
            "open_network_settings": open_network_settings,
            "turn_on_bluetooth": turn_on_bluetooth,
            "turn_off_bluetooth": turn_off_bluetooth,
            "generate_program": generate_program,
        }
        
        # Detect initial mode
        self.detect_mode()
    
    def detect_mode(self) -> str:
        """
        Detect internet connectivity and determine which mode to use.
        
        Returns:
            str: "online" or "offline"
        """
        self.online_available = check_internet()
        
        if self.online_available and self.grok_configured:
            self.current_mode = "online"
        else:
            self.current_mode = "offline"
        
        return self.current_mode
    
    def get_mode_status(self) -> Tuple[str, str]:
        """
        Get current mode and status message.
        
        Returns:
            Tuple[str, str]: (mode, status_message)
        """
        self.detect_mode()
        
        if self.current_mode == "online":
            status = "🟢 Online Mode Active - Using Grok AI"
        else:
            if not self.online_available:
                status = "🔴 Offline Mode Active - No Internet Connection"
            elif not self.grok_configured:
                status = "🟡 Offline Mode Active - API Key Not Configured"
            else:
                status = "🔴 Offline Mode Active - Using Local NLP"
        
        return self.current_mode, status
    
    def parse_command(self, user_input: str) -> Dict:
        """
        Parse user command using appropriate mode (online or offline).
        
        Args:
            user_input: User's natural language command
            
        Returns:
            Dict with intent, parameters, response, and mode information
        """
        # Detect current mode
        self.detect_mode()
        
        # Try online mode first if available
        if self.current_mode == "online":
            try:
                result = parse_with_grok(user_input)
                
                # If online mode failed, fall back to offline
                if result.get("intent") == "error":
                    print("⚠️  Online mode failed, falling back to offline mode...")
                    self.current_mode = "offline"
                    result = parse_offline(user_input)
                else:
                    result["mode"] = "online"
                
                return result
            
            except Exception as e:
                print(f"⚠️  Online mode error: {e}, falling back to offline mode...")
                self.current_mode = "offline"
                result = parse_offline(user_input)
                return result
        
        # Use offline mode
        else:
            result = parse_offline(user_input)
            return result
    
    def execute_action(self, intent: str, parameters: Dict = None) -> str:
        """
        Execute the automation action based on intent.
        
        Args:
            intent: The action intent
            parameters: Optional parameters for the action
            
        Returns:
            str: Result message
        """
        if parameters is None:
            parameters = {}
        
        # Get action function
        action_func = self.action_map.get(intent)
        
        if action_func is None:
            return f"❌ Unknown action: {intent}"
        
        try:
            # Execute action with parameters if needed
            if parameters:
                # Check if action requires parameters
                param_value = parameters.get("folder_name")
                if param_value:
                    result = action_func(param_value)
                # For program generation, pass the full user request
                elif intent == "generate_program":
                    # Extract the program request from parameters or use original input
                    user_request = parameters.get("program_request", parameters.get("folder_name", ""))
                    result = action_func(user_request)
                else:
                    result = action_func()
            else:
                result = action_func()
            
            return result
        
        except TypeError:
            # Action doesn't take parameters, try without
            try:
                result = action_func()
                return result
            except Exception as e:
                return f"❌ Error executing action: {str(e)}"
        
        except Exception as e:
            return f"❌ Error executing action: {str(e)}"
    
    def process_command(self, user_input: str) -> Tuple[str, str]:
        """
        Process user command end-to-end: parse + execute.
        
        Args:
            user_input: User's natural language command
            
        Returns:
            Tuple[str, str]: (bot_response, mode_used)
        """
        # Parse the command
        parse_result = self.parse_command(user_input)
        
        intent = parse_result.get("intent")
        parameters = parse_result.get("parameters", {})
        ai_response = parse_result.get("response", "")
        mode = parse_result.get("mode", self.current_mode)
        
        # If unknown intent, return the AI response
        if intent == "unknown" or intent == "error":
            log_event(user_input, ai_response)
            return ai_response, mode
        
        # Execute the action
        action_result = self.execute_action(intent, parameters)
        
        # Combine AI response with action result
        if ai_response and action_result:
            # If online mode, use AI response + action result
            if mode == "online":
                full_response = f"{ai_response}\n{action_result}"
            else:
                # Offline mode: just show action result
                full_response = action_result
        else:
            full_response = action_result or ai_response or "❌ No response generated"
        
        # Log the interaction
        log_event(user_input, full_response)
        
        return full_response, mode


# Global chatbot instance
chatbot = HybridChatbot()


def process_user_input(user_input: str) -> Tuple[str, str]:
    """
    Process user input and return response.
    
    Args:
        user_input: User's command
        
    Returns:
        Tuple[str, str]: (response, mode)
    """
    return chatbot.process_command(user_input)


def get_current_mode() -> Tuple[str, str]:
    """
    Get current mode and status.
    
    Returns:
        Tuple[str, str]: (mode, status_message)
    """
    return chatbot.get_mode_status()


if __name__ == "__main__":
    # Test the hybrid chatbot
    print("🤖 Testing Hybrid Chatbot Core...")
    print("=" * 60)
    
    # Show current mode
    mode, status = get_current_mode()
    print(status)
    print("=" * 60)
    
    # Test commands
    test_commands = [
        "open calculator",
        "show me cpu usage",
        "opn setings",  # Typo test
        "what's my battery status",
        "lauch notpad",  # Typo test
    ]
    
    print("\n📝 Testing commands:\n")
    for cmd in test_commands:
        print(f"User: {cmd}")
        response, mode_used = process_user_input(cmd)
        print(f"Bot [{mode_used.upper()}]: {response}")
        print("-" * 60)
    
    print("\n✅ Hybrid chatbot test complete!")
