"""
NLP-Based Intent Recognition Module for Windows Automation Chatbot

This module provides intelligent command parsing with:
- Fuzzy string matching for typos and spelling mistakes
- Singular/plural word normalization
- Synonym mapping
- Intent scoring and confidence matching
- Natural language preprocessing
"""

import re
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Optional


class NLPIntentParser:
    """
    Handles natural language processing and intent recognition for automation commands.
    Uses fuzzy matching to understand commands even with spelling mistakes or variations.
    """
    
    def __init__(self):
        """Initialize the NLP parser with intent definitions and variations."""
        
        # Define all intents with their patterns and variations
        self.intents = {
            # File and folder operations
            "list_files": {
                "keywords": ["list", "show", "display", "view", "files", "file", "directory", "folder", "folders"],
                "patterns": [
                    r"(?:list|show|display|view)\s+(?:the\s+)?(?:files?|folders?|directory)",
                    r"what\s+files?",
                    r"files?\s+(?:in|here)",
                ],
                "aliases": ["show files", "list files", "display files", "what files are here", "view files"]
            },
            "create_folder": {
                "keywords": ["create", "make", "new", "folder", "directory"],
                "patterns": [
                    r"(?:create|make|new)\s+(?:a\s+)?(?:folder|directory)\s+(?:called|named)?\s*(.+)",
                ],
                "aliases": ["create folder", "make folder", "new folder"]
            },
            "delete_folder": {
                "keywords": ["delete", "remove", "erase", "folder", "directory"],
                "patterns": [
                    r"(?:delete|remove|erase)\s+(?:the\s+)?(?:folder|directory)\s+(?:called|named)?\s*(.+)",
                ],
                "aliases": ["delete folder", "remove folder"]
            },
            "open_folder": {
                "keywords": ["open", "launch", "go", "folder", "directory"],
                "patterns": [
                    r"open\s+(?:the\s+)?(?:folder|directory)\s*(.+)",
                ],
                "aliases": ["open folder", "go to folder"]
            },
            
            # System information
            "cpu_usage": {
                "keywords": ["cpu", "processor", "usage", "load"],
                "patterns": [
                    r"(?:cpu|processor)\s+(?:usage|load)",
                    r"how\s+much\s+cpu",
                    r"check\s+cpu",
                ],
                "aliases": ["cpu usage", "check cpu", "processor usage", "cpu load"]
            },
            "memory_usage": {
                "keywords": ["memory", "ram", "usage"],
                "patterns": [
                    r"(?:memory|ram)\s+(?:usage|status)",
                    r"how\s+much\s+(?:ram|memory)",
                    r"check\s+(?:ram|memory)",
                ],
                "aliases": ["memory usage", "ram usage", "check memory", "how much ram"]
            },
            "system_info": {
                "keywords": ["system", "info", "information", "computer", "pc", "details"],
                "patterns": [
                    r"system\s+(?:info|information|details)",
                    r"(?:pc|computer)\s+(?:info|details)",
                ],
                "aliases": ["system info", "system information", "pc info", "computer info"]
            },
            "system_summary": {
                "keywords": ["system", "summary", "overview"],
                "patterns": [
                    r"system\s+summary",
                ],
                "aliases": ["system summary", "system overview"]
            },
            "show_ip": {
                "keywords": ["ip", "address", "network"],
                "patterns": [
                    r"(?:show|what|display)\s+(?:my\s+)?ip(?:\s+address)?",
                    r"ip\s+address",
                ],
                "aliases": ["show ip", "ip address", "my ip"]
            },
            "battery_status": {
                "keywords": ["battery", "power", "status", "level", "charge"],
                "patterns": [
                    r"battery\s+(?:status|level|charge)",
                    r"check\s+battery",
                ],
                "aliases": ["battery status", "check battery", "power status"]
            },
            "check_storage": {
                "keywords": ["storage", "disk", "space", "drive"],
                "patterns": [
                    r"(?:check|show)\s+storage",
                    r"disk\s+space",
                    r"drive\s+space",
                ],
                "aliases": ["check storage", "disk space", "storage info"]
            },
            "show_datetime": {
                "keywords": ["time", "date", "datetime", "clock"],
                "patterns": [
                    r"(?:what|show|display)\s+(?:time|date)",
                    r"what'?s\s+the\s+time",
                    r"current\s+(?:time|date)",
                ],
                "aliases": ["show time", "what time", "current time", "date time"]
            },
            
            # Open applications
            "open_notepad": {
                "keywords": ["open", "launch", "start", "notepad", "text", "editor"],
                "patterns": [
                    r"(?:open|launch|start)\s+notepad",
                ],
                "aliases": ["open notepad", "launch notepad", "start notepad"]
            },
            "open_calculator": {
                "keywords": ["open", "launch", "start", "calculator", "calc"],
                "patterns": [
                    r"(?:open|launch|start)\s+(?:calculator|calc)",
                ],
                "aliases": ["open calculator", "launch calc", "start calculator"]
            },
            "open_chrome": {
                "keywords": ["open", "launch", "start", "chrome", "browser"],
                "patterns": [
                    r"(?:open|launch|start)\s+chrome",
                ],
                "aliases": ["open chrome", "launch chrome", "start browser"]
            },
            "open_cmd": {
                "keywords": ["open", "launch", "start", "cmd", "command", "prompt", "terminal"],
                "patterns": [
                    r"(?:open|launch|start)\s+(?:cmd|command\s+prompt|terminal)",
                ],
                "aliases": ["open cmd", "launch command prompt", "open terminal"]
            },
            "open_whatsapp": {
                "keywords": ["open", "launch", "start", "whatsapp", "chat"],
                "patterns": [
                    r"(?:open|launch|start)\s+whatsapp",
                ],
                "aliases": ["open whatsapp", "launch whatsapp"]
            },
            "open_task_manager": {
                "keywords": ["open", "launch", "task", "manager", "process"],
                "patterns": [
                    r"(?:open|launch)\s+task\s+manager",
                ],
                "aliases": ["open task manager", "launch task manager"]
            },
            "show_running_processes": {
                "keywords": ["show", "running", "process", "processes", "tasks"],
                "patterns": [
                    r"(?:show|display)\s+(?:running\s+)?processes?",
                ],
                "aliases": ["show processes", "running processes", "show tasks"]
            },
            
            # Settings
            "open_settings": {
                "keywords": ["open", "launch", "settings", "setting", "preferences", "config"],
                "patterns": [
                    r"(?:open|launch|go\s+to)\s+(?:settings?|preferences)",
                ],
                "aliases": ["open settings", "open setting", "launch settings", "go to settings", "settings", "setting"]
            },
            "open_network_settings": {
                "keywords": ["open", "network", "settings", "wifi"],
                "patterns": [
                    r"(?:open|launch)\s+network\s+settings?",
                ],
                "aliases": ["open network settings", "network settings"]
            },
            "enable_night_theme": {
                "keywords": ["enable", "night", "theme", "dark", "mode"],
                "patterns": [
                    r"(?:enable|turn\s+on)\s+(?:night\s+theme|dark\s+mode)",
                    r"make\s+(?:my\s+)?screen\s+dark",
                ],
                "aliases": ["enable night theme", "dark mode", "night theme"]
            },
            
            # Volume control
            "mute_volume": {
                "keywords": ["mute", "volume", "sound", "silent"],
                "patterns": [
                    r"mute\s+(?:volume|sound)",
                ],
                "aliases": ["mute volume", "mute sound"]
            },
            "increase_volume": {
                "keywords": ["increase", "volume", "up", "louder", "raise"],
                "patterns": [
                    r"(?:increase|raise)\s+volume",
                    r"volume\s+up",
                    r"make\s+it\s+louder",
                ],
                "aliases": ["increase volume", "volume up", "louder"]
            },
            "decrease_volume": {
                "keywords": ["decrease", "volume", "down", "quieter", "lower"],
                "patterns": [
                    r"(?:decrease|lower)\s+volume",
                    r"volume\s+down",
                    r"make\s+it\s+quieter",
                ],
                "aliases": ["decrease volume", "volume down", "quieter"]
            },
            
            # Bluetooth
            "turn_on_bluetooth": {
                "keywords": ["turn", "on", "enable", "bluetooth"],
                "patterns": [
                    r"(?:turn\s+on|enable)\s+bluetooth",
                ],
                "aliases": ["turn on bluetooth", "enable bluetooth"]
            },
            "turn_off_bluetooth": {
                "keywords": ["turn", "off", "disable", "bluetooth"],
                "patterns": [
                    r"(?:turn\s+off|disable)\s+bluetooth",
                ],
                "aliases": ["turn off bluetooth", "disable bluetooth"]
            },
            
            # Power commands
            "shutdown_pc": {
                "keywords": ["shutdown", "turn", "off", "pc", "computer"],
                "patterns": [
                    r"(?:shutdown|turn\s+off)\s+(?:the\s+)?(?:pc|computer)",
                ],
                "aliases": ["shutdown", "shutdown pc", "turn off pc"]
            },
            "restart_pc": {
                "keywords": ["restart", "reboot", "pc", "computer"],
                "patterns": [
                    r"(?:restart|reboot)\s+(?:the\s+)?(?:pc|computer)?",
                ],
                "aliases": ["restart", "restart pc", "reboot"]
            },
            "lock_pc": {
                "keywords": ["lock", "screen", "pc", "computer"],
                "patterns": [
                    r"lock\s+(?:the\s+)?(?:screen|pc|computer)?",
                ],
                "aliases": ["lock", "lock pc", "lock screen"]
            },
            "cancel_shutdown": {
                "keywords": ["cancel", "stop", "shutdown"],
                "patterns": [
                    r"(?:cancel|stop)\s+shutdown",
                ],
                "aliases": ["cancel shutdown", "stop shutdown"]
            },
        }
        
        # Common word variations for normalization
        self.word_normalizations = {
            # Singular/plural
            "files": "file",
            "folders": "folder",
            "directories": "directory",
            "settings": "setting",
            "processes": "process",
            "tasks": "task",
            
            # Synonyms
            "show": "open",
            "display": "show",
            "view": "show",
            "launch": "open",
            "start": "open",
            "run": "open",
            
            "pc": "computer",
            "shutdown": "shutoff",
            "poweroff": "shutoff",
        }
        
        # Threshold for fuzzy matching
        self.fuzzy_threshold = 0.7
        self.high_confidence_threshold = 0.85
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize text by:
        - Converting to lowercase
        - Removing extra whitespace
        - Removing punctuation (except spaces and alphanumeric)
        """
        text = text.lower().strip()
        # Remove special characters but keep spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        return text.split()
    
    def normalize_words(self, words: List[str]) -> List[str]:
        """Normalize words using the normalization dictionary."""
        normalized = []
        for word in words:
            normalized.append(self.word_normalizations.get(word, word))
        return normalized
    
    def fuzzy_match(self, str1: str, str2: str) -> float:
        """
        Calculate similarity between two strings using SequenceMatcher.
        Returns a score between 0 and 1.
        """
        return SequenceMatcher(None, str1, str2).ratio()
    
    def fuzzy_match_list(self, word: str, word_list: List[str]) -> Tuple[Optional[str], float]:
        """
        Find the best fuzzy match for a word in a list of words.
        Returns the best match and its score.
        """
        best_match = None
        best_score = 0.0
        
        for candidate in word_list:
            score = self.fuzzy_match(word, candidate)
            if score > best_score:
                best_score = score
                best_match = candidate
        
        return best_match, best_score
    
    def score_intent(self, user_tokens: List[str], intent_name: str) -> float:
        """
        Score how well user input matches an intent.
        Returns a confidence score between 0 and 1.
        """
        intent = self.intents[intent_name]
        keywords = intent["keywords"]
        
        # Check how many keywords match
        matches = 0
        fuzzy_matches = 0
        
        for user_token in user_tokens:
            # Exact match
            if user_token in keywords:
                matches += 1
            else:
                # Fuzzy match
                best_match, score = self.fuzzy_match_list(user_token, keywords)
                if score >= self.fuzzy_threshold:
                    fuzzy_matches += 1
        
        # Calculate score based on matches
        total_matches = matches + (fuzzy_matches * 0.9)  # Fuzzy matches count slightly less
        
        # Normalize by the minimum of user tokens or keywords
        denominator = min(len(user_tokens), len(keywords))
        if denominator == 0:
            return 0.0
        
        score = total_matches / denominator
        
        # Bonus for exact keyword sequence
        user_text = " ".join(user_tokens)
        for alias in intent["aliases"]:
            alias_score = self.fuzzy_match(user_text, alias)
            if alias_score > score:
                score = alias_score
        
        return min(score, 1.0)
    
    def extract_parameters(self, user_input: str, intent_name: str) -> Optional[str]:
        """
        Extract parameters from user input based on intent patterns.
        For example, extract folder name from "create folder MyFolder"
        """
        intent = self.intents.get(intent_name)
        if not intent or "patterns" not in intent:
            return None
        
        for pattern in intent["patterns"]:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match and match.groups():
                # Return the first captured group (parameter)
                return match.group(1).strip()
        
        return None
    
    def parse_intent(self, user_input: str) -> Dict:
        """
        Parse user input and return the best matching intent with confidence score.
        
        Returns:
            Dict with keys: intent, confidence, parameters
        """
        # Normalize and tokenize
        normalized_text = self.normalize_text(user_input)
        tokens = self.tokenize(normalized_text)
        normalized_tokens = self.normalize_words(tokens)
        
        # Score all intents
        intent_scores = {}
        for intent_name in self.intents.keys():
            score = self.score_intent(normalized_tokens, intent_name)
            intent_scores[intent_name] = score
        
        # Get best intent
        best_intent = max(intent_scores, key=intent_scores.get)
        best_score = intent_scores[best_intent]
        
        # Extract parameters if applicable
        parameters = self.extract_parameters(normalized_text, best_intent)
        
        return {
            "intent": best_intent,
            "confidence": best_score,
            "parameters": parameters,
            "normalized_input": normalized_text,
            "all_scores": intent_scores
        }
    
    def get_intent_variations(self, intent_name: str) -> List[str]:
        """Get all variations/aliases for a given intent."""
        intent = self.intents.get(intent_name)
        if intent and "aliases" in intent:
            return intent["aliases"]
        return []


# Create a singleton instance
nlp_parser = NLPIntentParser()


def parse_with_nlp(user_input: str, confidence_threshold: float = 0.6) -> Optional[Dict]:
    """
    Convenience function to parse user input with NLP.
    
    Args:
        user_input: The user's command
        confidence_threshold: Minimum confidence score to accept (default 0.6)
    
    Returns:
        Dictionary with intent information if confidence is high enough, None otherwise
    """
    result = nlp_parser.parse_intent(user_input)
    
    if result["confidence"] >= confidence_threshold:
        return result
    
    return None
