"""
Enhanced Offline NLP Handler with Fuzzy Matching and Spell Correction

This module provides robust offline natural language processing for Windows automation
commands with support for typos, spelling mistakes, and natural variations.
"""

import re
from difflib import SequenceMatcher, get_close_matches
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


class OfflineNLPHandler:
    """
    Handles offline NLP with fuzzy matching and spell correction.
    """
    
    def __init__(self):
        """Initialize offline NLP with intent definitions and fuzzy matching."""
        
        # Define intents with keywords and common variations
        self.intents = {
            # Applications
            "open_notepad": {
                "keywords": ["notepad", "notpad", "notepadd", "text editor", "editor"],
                "actions": ["open", "launch", "start", "run", "opn", "oepn", "lauch"],
            },
            "open_calculator": {
                "keywords": ["calculator", "calc", "calulator", "calculater", "caculator", "claculator"],
                "actions": ["open", "launch", "start", "run", "opn"],
            },
            "open_chrome": {
                "keywords": ["chrome", "browser", "chrom", "crome", "chromee"],
                "actions": ["open", "launch", "start", "run", "opn"],
            },
            "open_cmd": {
                "keywords": ["cmd", "command prompt", "terminal", "command", "comand prompt"],
                "actions": ["open", "launch", "start", "run", "opn"],
            },
            "open_whatsapp": {
                "keywords": ["whatsapp", "whatsap", "watsapp", "whats app", "chat"],
                "actions": ["open", "launch", "start", "run", "opn"],
            },
            "open_task_manager": {
                "keywords": ["task manager", "taskmanager", "task manger", "process manager"],
                "actions": ["open", "launch", "start", "run", "show", "opn"],
            },
            
            # Settings
            "open_settings": {
                "keywords": ["settings", "setting", "setings", "seting", "preferences", "config"],
                "actions": ["open", "launch", "go to", "show", "opn", "goto"],
            },
            "open_network_settings": {
                "keywords": ["network settings", "network setting", "wifi settings", "internet settings"],
                "actions": ["open", "launch", "show", "opn"],
            },
            
            # System Info
            "cpu_usage": {
                "keywords": ["cpu", "processor", "cpu usage", "processor usage", "cpu load"],
                "actions": ["show", "check", "display", "what", "how much", "get"],
            },
            "memory_usage": {
                "keywords": ["memory", "ram", "memory usage", "ram usage", "memry", "mem"],
                "actions": ["show", "check", "display", "what", "how much", "get"],
            },
            "battery_status": {
                "keywords": ["battery", "power", "battery level", "charge", "baterry", "batery"],
                "actions": ["show", "check", "display", "what", "status", "get"],
            },
            "check_storage": {
                "keywords": ["storage", "disk", "disk space", "drive", "space", "storag"],
                "actions": ["show", "check", "display", "what", "get"],
            },
            "system_info": {
                "keywords": ["system info", "system information", "pc info", "computer info", "system", "systeminfo"],
                "actions": ["show", "display", "get", "what"],
            },
            "system_summary": {
                "keywords": ["system summary", "summary", "overview", "status"],
                "actions": ["show", "display", "get"],
            },
            "show_ip": {
                "keywords": ["ip", "ip address", "ip addr", "network address", "my ip"],
                "actions": ["show", "display", "what", "get", "whats"],
            },
            "show_datetime": {
                "keywords": ["time", "date", "datetime", "clock", "what time"],
                "actions": ["show", "display", "what", "get", "tell", "whats"],
            },
            "show_running_processes": {
                "keywords": ["processes", "running processes", "process", "tasks", "running tasks"],
                "actions": ["show", "display", "list", "get"],
            },
            
            # Files and Folders
            "list_files": {
                "keywords": ["files", "file", "directory", "folder", "folders"],
                "actions": ["list", "show", "display", "what", "see"],
            },
            "create_folder": {
                "keywords": ["folder", "directory", "dir"],
                "actions": ["create", "make", "new"],
                "needs_param": True,
            },
            "delete_folder": {
                "keywords": ["folder", "directory", "dir"],
                "actions": ["delete", "remove", "erase"],
                "needs_param": True,
            },
            "open_folder": {
                "keywords": ["folder", "directory", "dir"],
                "actions": ["open", "show", "go to", "navigate"],
                "needs_param": True,
            },
            
            # Volume Control
            "mute_volume": {
                "keywords": ["volume", "sound", "audio"],
                "actions": ["mute", "silence", "turn off"],
            },
            "increase_volume": {
                "keywords": ["volume", "sound"],
                "actions": ["increase", "up", "raise", "louder", "increse", "increese"],
            },
            "decrease_volume": {
                "keywords": ["volume", "sound"],
                "actions": ["decrease", "down", "lower", "quieter", "decrese", "decreese"],
            },
            
            # Bluetooth
            "turn_on_bluetooth": {
                "keywords": ["bluetooth", "bt", "bluetoth", "blutooth"],
                "actions": ["turn on", "enable", "activate", "on", "start"],
            },
            "turn_off_bluetooth": {
                "keywords": ["bluetooth", "bt", "bluetoth", "blutooth"],
                "actions": ["turn off", "disable", "deactivate", "off", "stop"],
            },
            
            # Themes
            "enable_night_theme": {
                "keywords": ["night", "dark", "night mode", "dark mode", "dark theme"],
                "actions": ["enable", "turn on", "activate", "on", "make"],
            },
            "disable_night_theme": {
                "keywords": ["light", "light mode", "day mode", "light theme"],
                "actions": ["enable", "turn on", "activate", "on", "make"],
            },
            
            # Power Commands
            "lock_pc": {
                "keywords": ["lock", "lock screen", "lock pc", "lock computer"],
                "actions": ["", "please"],
            },
            "shutdown_pc": {
                "keywords": ["shutdown", "shut down", "turn off", "power off", "shutdwn", "shutdwon"],
                "actions": ["", "please", "computer", "pc"],
            },
            "restart_pc": {
                "keywords": ["restart", "reboot", "reset", "restat", "restrart"],
                "actions": ["", "please", "computer", "pc"],
            },
            "cancel_shutdown": {
                "keywords": ["cancel", "stop", "abort"],
                "actions": ["shutdown", "restart", "shutdwn"],
            },
            
            # Program Generation (LLM-powered)
            "generate_program": {
                "keywords": ["write", "create", "generate", "make", "code", "program", "script"],
                "actions": ["program", "code", "script", "function", "application"],
                "needs_param": True,
            },
        }
        
        # Common word corrections
        self.corrections = {
            "opn": "open",
            "oepn": "open",
            "lauch": "launch",
            "calcalator": "calculator",
            "calulator": "calculator",
            "calculater": "calculator",
            "caculator": "calculator",
            "claculator": "calculator",
            "notpad": "notepad",
            "notepadd": "notepad",
            "setings": "settings",
            "seting": "settings",
            "chrom": "chrome",
            "crome": "chrome",
            "baterry": "battery",
            "batery": "battery",
            "memry": "memory",
            "storag": "storage",
            "increse": "increase",
            "increese": "increase",
            "decrese": "decrease",
            "decreese": "decrease",
            "bluetoth": "bluetooth",
            "blutooth": "bluetooth",
            "shutdwn": "shutdown",
            "shutdwon": "shutdown",
            "restat": "restart",
            "restrart": "restart",
            "comand": "command",
            "watsapp": "whatsapp",
            "whatsap": "whatsapp",
        }
    
    def correct_spelling(self, text: str) -> str:
        """Apply spell correction to text."""
        words = text.lower().split()
        corrected_words = [self.corrections.get(word, word) for word in words]
        return " ".join(corrected_words)
    
    def fuzzy_match(self, word: str, candidates: List[str], threshold: float = 0.6) -> Optional[str]:
        """
        Find best fuzzy match for a word from candidates.
        
        Args:
            word: Word to match
            candidates: List of candidate words
            threshold: Minimum similarity threshold (0.0 to 1.0)
            
        Returns:
            Best matching candidate or None
        """
        best_match = None
        best_score = threshold
        
        for candidate in candidates:
            # Calculate similarity
            similarity = SequenceMatcher(None, word.lower(), candidate.lower()).ratio()
            
            if similarity > best_score:
                best_score = similarity
                best_match = candidate
        
        return best_match
    
    def extract_parameter(self, text: str, intent: str) -> Optional[str]:
        """Extract parameter (like folder name) from text."""
        # For program generation, return the full request
        if intent == "generate_program":
            # Remove the trigger words but keep the program description
            cleaned = text
            for trigger in ["write", "create", "generate", "make", "code"]:
                cleaned = re.sub(rf'\b{trigger}\b', '', cleaned, flags=re.IGNORECASE)
            for filler in ["a", "the", "me", "please", "can you", "could you"]:
                cleaned = re.sub(rf'\b{filler}\b', '', cleaned, flags=re.IGNORECASE)
            cleaned = cleaned.strip()
            return cleaned if cleaned else text
        
        # For folder operations
        # Remove common action words
        cleaned = text
        for action in ["create", "make", "delete", "remove", "open", "show", "new"]:
            cleaned = re.sub(rf'\b{action}\b', '', cleaned, flags=re.IGNORECASE)
        
        # Remove intent keywords
        for keyword in ["folder", "directory", "file"]:
            cleaned = re.sub(rf'\b{keyword}\b', '', cleaned, flags=re.IGNORECASE)
        
        # Remove filler words
        for filler in ["a", "the", "called", "named", "please", "can you", "could you"]:
            cleaned = re.sub(rf'\b{filler}\b', '', cleaned, flags=re.IGNORECASE)
        
        cleaned = cleaned.strip()
        return cleaned if cleaned else None
    
    def parse_command(self, user_input: str) -> Dict:
        """
        Parse user command using offline NLP with fuzzy matching.
        
        Args:
            user_input: User's natural language command
            
        Returns:
            Dict with intent, parameters, confidence, and response
        """
        # Step 1: Correct spelling
        corrected_input = self.correct_spelling(user_input)
        lower_input = corrected_input.lower()
        
        # Step 2: Score each intent
        best_intent = None
        best_score = 0.0
        
        for intent, config in self.intents.items():
            score = 0.0
            keyword_matches = 0
            action_matches = 0
            
            # Check keyword matches
            for keyword in config["keywords"]:
                if keyword in lower_input:
                    keyword_matches += 1
                    score += 2.0
                else:
                    # Try fuzzy matching
                    for word in lower_input.split():
                        if self.fuzzy_match(word, [keyword], threshold=0.75):
                            keyword_matches += 1
                            score += 1.5
                            break
            
            # Check action matches
            for action in config["actions"]:
                if action and action in lower_input:
                    action_matches += 1
                    score += 1.0
                else:
                    # Try fuzzy matching for actions
                    for word in lower_input.split():
                        if action and self.fuzzy_match(word, [action], threshold=0.75):
                            action_matches += 1
                            score += 0.8
                            break
            
            # Bonus for having both keywords and actions
            if keyword_matches > 0 and action_matches > 0:
                score += 1.0
            
            # Update best match
            if score > best_score:
                best_score = score
                best_intent = intent
        
        # Step 3: Prepare result
        if best_intent and best_score >= 1.5:
            confidence = min(best_score / 5.0, 1.0)  # Normalize to 0-1
            
            # Extract parameters if needed
            parameters = {}
            intent_config = self.intents[best_intent]
            if intent_config.get("needs_param", False):
                param = self.extract_parameter(user_input, best_intent)
                if param:
                    if best_intent == "generate_program":
                        parameters["program_request"] = param
                    else:
                        parameters["folder_name"] = param
            
            return {
                "intent": best_intent,
                "parameters": parameters,
                "confidence": confidence,
                "response": f"✅ Understood (offline): {best_intent.replace('_', ' ').title()}",
                "mode": "offline"
            }
        
        else:
            return {
                "intent": "unknown",
                "parameters": {},
                "confidence": 0.0,
                "response": "❓ I didn't understand that command. Type 'help' to see available commands.",
                "mode": "offline"
            }


# Global instance
offline_nlp = OfflineNLPHandler()


def parse_offline(user_input: str) -> Dict:
    """
    Parse user command using offline NLP.
    
    This function now uses BOTH the old handler (for backward compatibility)
    and attempts to use the enhanced NLP module if available.
    
    Args:
        user_input: User's natural language command
        
    Returns:
        Dict with intent, parameters, confidence, and response
    """
    # Try using enhanced NLP module first
    try:
        from enhanced_nlp_module import EnhancedNLPProcessor
        enhanced_nlp = EnhancedNLPProcessor()
        result = enhanced_nlp.process(user_input)
        
        # Convert NLPResult to dict format
        return {
            "intent": result.intent,
            "parameters": result.entities,
            "confidence": result.confidence,
            "response": result.user_message,
            "mode": "offline_enhanced"
        }
    except ImportError:
        # Fallback to old handler if enhanced module not available
        return offline_nlp.parse_command(user_input)


if __name__ == "__main__":
    # Test the offline NLP handler
    print("🧪 Testing Offline NLP Handler with Fuzzy Matching...")
    print("=" * 60)
    
    test_commands = [
        "opn calcalator",  # Typos
        "open setings",    # Typo in settings
        "show me the baterry status",  # Battery typo
        "lauch notpad",    # Multiple typos
        "increse volume",  # Increase typo
        "shutdwn the computer",  # Shutdown typo
        "show cpu usag",   # Incomplete word
        "opn chrom",       # Multiple typos
        "create folder named MyData",  # With parameter
        "turn on bluetoth",  # Bluetooth typo
    ]
    
    for cmd in test_commands:
        print(f"\n📝 Testing: '{cmd}'")
        result = parse_offline(cmd)
        print(f"   Intent: {result['intent']}")
        print(f"   Confidence: {result['confidence']:.2%}")
        print(f"   Parameters: {result.get('parameters', {})}")
        print(f"   Response: {result['response']}")
    
    print("\n" + "=" * 60)
    print("✅ Offline NLP test complete!")
