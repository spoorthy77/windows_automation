"""
Offline NLP Engine using RapidFuzz for Fuzzy Matching
No internet required - 100% offline command understanding
"""

from rapidfuzz import fuzz, process
from typing import Dict, List, Tuple, Optional


class OfflineNLP:
    """
    Offline Natural Language Processing using fuzzy matching
    Handles typos, abbreviations, and variations in user input
    """
    
    def __init__(self):
        # Define intent patterns with variations
        self.intent_patterns = {
            # App launching intents
            "open_notepad": [
                "open notepad", "launch notepad", "start notepad",
                "notepad", "open note pad", "launch note",
                "opn notepad", "noteapd", "notpad"
            ],
            "open_calculator": [
                "open calculator", "launch calculator", "start calculator",
                "calculator", "calc", "open calc", "launch calc",
                "opn calc", "calculater", "calulator", "open calulator"
            ],
            "open_chrome": [
                "open chrome", "launch chrome", "start chrome",
                "chrome", "browser", "open browser", "launch browser",
                "opn chrome", "crome", "chrom"
            ],
            "open_cmd": [
                "open command prompt", "open cmd", "launch cmd",
                "command prompt", "terminal", "cmd", "command line",
                "opn cmd", "comand prompt"
            ],
            "open_whatsapp": [
                "open whatsapp", "launch whatsapp", "start whatsapp",
                "whatsapp", "whatsap", "watsapp", "open whatsap",
                "opn whatsapp", "open wa"
            ],
            "open_task_manager": [
                "open task manager", "launch task manager",
                "task manager", "taskmanager", "task mgr",
                "opn task manager", "tsk manager"
            ],
            
            # Settings intents
            "open_settings": [
                "open settings", "launch settings", "settings",
                "system settings", "open setting", "setting",
                "opn settings", "settins", "setings"
            ],
            "open_network_settings": [
                "open network settings", "network settings",
                "wifi settings", "internet settings",
                "open network", "network setting",
                "opn network settings", "netwrk settings"
            ],
            
            # System info intents
            "cpu_usage": [
                "cpu usage", "check cpu", "cpu status", "processor usage",
                "how much cpu", "cpu load", "cpu percent",
                "chk cpu", "cpu usge", "cpu"
            ],
            "memory_usage": [
                "memory usage", "ram usage", "check memory", "check ram",
                "how much ram", "memory status", "ram status",
                "chk memory", "chk ram", "ram", "memory"
            ],
            "battery_status": [
                "battery status", "battery level", "check battery",
                "battery", "how much battery", "battery percentage",
                "chk battery", "baterry", "battry"
            ],
            "check_storage": [
                "check storage", "disk space", "storage space",
                "how much storage", "storage status", "disk usage",
                "chk storage", "chk disk", "storag", "storage"
            ],
            "system_info": [
                "system info", "system information", "system details",
                "system specs", "computer info", "pc info",
                "system", "sysinfo", "sys info"
            ],
            "system_summary": [
                "system summary", "summary", "system status",
                "pc status", "computer status", "quick stats",
                "sys summary", "sumary"
            ],
            "show_ip": [
                "show ip", "ip address", "my ip", "network address",
                "what is my ip", "show ip address", "get ip",
                "ip", "ipconfig"
            ],
            "show_datetime": [
                "show date", "show time", "what time", "what date",
                "current time", "current date", "date and time",
                "time", "date", "datetime", "clock"
            ],
            "show_processes": [
                "show processes", "running processes", "list processes",
                "what's running", "active processes", "process list",
                "processes", "running apps", "active apps"
            ],
            
            # Volume control
            "mute_volume": [
                "mute", "mute volume", "silence", "mute sound",
                "turn off sound", "mute audio", "mut volume"
            ],
            "increase_volume": [
                "increase volume", "volume up", "raise volume",
                "louder", "turn up volume", "up volume",
                "increse volume", "volum up"
            ],
            "decrease_volume": [
                "decrease volume", "volume down", "lower volume",
                "quieter", "turn down volume", "down volume",
                "decrese volume", "volum down"
            ],
            
            # Bluetooth
            "bluetooth_on": [
                "turn on bluetooth", "enable bluetooth", "bluetooth on",
                "start bluetooth", "activate bluetooth",
                "bluetooth", "turn bluetooth on"
            ],
            "bluetooth_off": [
                "turn off bluetooth", "disable bluetooth", "bluetooth off",
                "stop bluetooth", "deactivate bluetooth",
                "turn bluetooth off"
            ],
            
            # Theme
            "night_theme": [
                "enable night theme", "night mode", "dark mode",
                "dark theme", "night theme", "enable dark mode",
                "turn on night mode", "nite mode", "dark thme"
            ],
            
            # Power commands
            "lock_pc": [
                "lock", "lock pc", "lock computer", "lock screen",
                "lock my screen", "lock system", "lok pc"
            ],
            "shutdown": [
                "shutdown", "shut down", "turn off", "power off",
                "shutdown pc", "shutdown computer", "shutdwn", "shut down pc"
            ],
            "restart": [
                "restart", "reboot", "restart pc", "restart computer",
                "reboot pc", "reboot computer", "restat", "restart system"
            ],
            "cancel_shutdown": [
                "cancel shutdown", "abort shutdown", "stop shutdown",
                "cancel shut down", "abort shut down", "cancle shutdown"
            ],
            
            # File operations
            "list_files": [
                "list files", "show files", "what files",
                "directory", "files", "ls", "dir",
                "lst files", "show fils"
            ],
            
            # Folder management
            "create_folder": [
                "create folder", "make folder", "new folder",
                "create directory", "make directory", "mkdir",
                "crete folder", "mke folder", "make fldr"
            ],
            "delete_folder": [
                "delete folder", "remove folder", "delete directory",
                "remove directory", "rmdir", "del folder",
                "dlete folder", "remve folder", "delete fldr"
            ],
            
            # File management
            "create_file": [
                "create file", "make file", "new file",
                "touch file", "create document", "make document",
                "crete file", "mke file", "make fil"
            ],
            "delete_file": [
                "delete file", "remove file", "del file",
                "erase file", "rm file", "delete document",
                "dlete file", "remve file", "delete fil"
            ],
            
            # Help
            "help": [
                "help", "commands", "what can you do",
                "show commands", "help me", "hlp"
            ]
            ,
            # Program generation (offline)
            "write_program": [
                "write program", "generate program", "create program",
                "write code", "generate code", "build program",
                "make program", "code a program"
            ]
        }
        
        # Build a flat list for matching
        self.all_patterns = []
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                self.all_patterns.append((pattern, intent))
    
    def preprocess(self, text: str) -> str:
        """Preprocess user input"""
        # Convert to lowercase
        text = text.lower().strip()
        
        # Remove extra spaces
        text = " ".join(text.split())
        
        # Remove common punctuation but keep essential chars
        text = text.replace("?", "").replace("!", "").replace(".", "")
        
        return text
    
    def detect_intent(self, user_input: str, threshold: int = 70) -> Tuple[Optional[str], int]:
        """
        Detect intent using fuzzy matching
        
        Args:
            user_input: Raw user input
            threshold: Minimum confidence score (0-100)
            
        Returns:
            Tuple of (intent, confidence_score)
        """
        # Preprocess input
        processed = self.preprocess(user_input)
        
        if not processed:
            return None, 0
        
        # Special handling for folder/file operations - check for keywords first
        folder_file_keywords = {
            'create_folder': ['create folder', 'make folder', 'new folder', 'mkdir'],
            'delete_folder': ['delete folder', 'remove folder', 'rmdir', 'del folder'],
            'create_file': ['create file', 'make file', 'new file', 'touch file'],
            'delete_file': ['delete file', 'remove file', 'del file', 'rm file']
        }
        
        # Check if any folder/file keyword matches
        for intent, keywords in folder_file_keywords.items():
            for keyword in keywords:
                if keyword in processed:
                    # Return high confidence since we found the exact keyword
                    return intent, 90
        
        # Special handling for program generation
        program_keywords = [
            'write program', 'generate program', 'create program',
            'write code', 'generate code', 'build program',
            'make program', 'code a program'
        ]
        for kw in program_keywords:
            if kw in processed:
                return 'write_program', 90
        # keyword pair heuristics
        tokens = processed.split()
        if ('write' in tokens or 'generate' in tokens or 'make' in tokens or 'build' in tokens) and (
            'program' in tokens or 'code' in tokens
        ):
            return 'write_program', 85

        # Find best match using fuzzy matching
        best_matches = process.extract(
            processed,
            [pattern for pattern, _ in self.all_patterns],
            scorer=fuzz.ratio,
            limit=5
        )
        
        if not best_matches:
            return None, 0
        
        # Get the best match
        best_pattern, best_score, _ = best_matches[0]
        
        # Find the intent for this pattern
        matched_intent = None
        for pattern, intent in self.all_patterns:
            if pattern == best_pattern:
                matched_intent = intent
                break
        
        # Return intent if confidence is above threshold
        if best_score >= threshold:
            return matched_intent, best_score
        
        return None, best_score
    
    def extract_folder_file_params(self, user_input: str) -> Dict:
        """
        Extract folder/file name and location from user input
        Examples:
          - "create folder test" -> name="test", location=None
          - "create folder test in downloads" -> name="test", location="downloads"
          - "delete file notes.txt in documents" -> name="notes.txt", location="documents"
        """
        # Keep original case for name extraction
        original_text = user_input.strip()
        text = user_input.lower().strip()
        
        # Extract location (downloads, documents, desktop)
        location = None
        location_keywords = {
            'downloads': ['downloads', 'download', 'downlds'],
            'documents': ['documents', 'document', 'docs', 'documets'],
            'desktop': ['desktop', 'desktp', 'desk top']
        }
        
        location_end_pos = len(original_text)
        
        for loc_key, variations in location_keywords.items():
            for variant in variations:
                if f' in {variant}' in text or f' to {variant}' in text:
                    location = loc_key
                    # Find the position where location starts in original text
                    location_marker = f' in {variant}'
                    if location_marker in text:
                        location_end_pos = text.index(location_marker)
                    else:
                        location_marker = f' to {variant}'
                        if location_marker in text:
                            location_end_pos = text.index(location_marker)
                    break
                elif text.endswith(variant):
                    location = loc_key
                    location_end_pos = text.rindex(variant)
                    break
            if location:
                break
        
        # Extract name from original text (preserving case)
        text_for_name = original_text[:location_end_pos].strip()
        
        # Remove common command words (case-insensitive)
        command_patterns = [
            r'create\s+folder\s+',
            r'make\s+folder\s+',
            r'new\s+folder\s+',
            r'delete\s+folder\s+',
            r'remove\s+folder\s+',
            r'del\s+folder\s+',
            r'create\s+file\s+',
            r'make\s+file\s+',
            r'new\s+file\s+',
            r'delete\s+file\s+',
            r'remove\s+file\s+',
            r'del\s+file\s+',
            r'mkdir\s+',
            r'rmdir\s+',
            r'touch\s+',
            r'rm\s+'
        ]
        
        import re
        for pattern in command_patterns:
            text_for_name = re.sub(pattern, '', text_for_name, flags=re.IGNORECASE)
        
        name = text_for_name.strip() if text_for_name.strip() else None
        
        return {
            'name': name,
            'location': location
        }

    def extract_program_params(self, user_input: str) -> Dict:
        """
        Extract language, topic, and location for program generation.
        Examples:
          - "write python program for prime number" -> python, prime_number
          - "generate java code palindrome in downloads" -> java, palindrome, downloads
          - "write program factorial" -> default python, factorial
        """
        original_text = user_input.strip()
        text = self.preprocess(user_input)

        # Location (reuse logic)
        location = None
        location_keywords = {
            'downloads': ['downloads', 'download', 'downlds'],
            'documents': ['documents', 'document', 'docs', 'documets'],
            'desktop': ['desktop', 'desktp', 'desk top']
        }
        for loc_key, variations in location_keywords.items():
            for variant in variations:
                if f' in {variant}' in text or f' to {variant}' in text or text.endswith(variant):
                    location = loc_key
                    break
            if location:
                break

        # Language detection
        detected_language = None
        if 'python' in text or ' py ' in f' {text} ':
            detected_language = 'python'
        elif 'java' in text:
            detected_language = 'java'
        elif 'c++' in text or 'cpp' in text or 'c plus plus' in text:
            detected_language = 'cpp'
        else:
            # bare ' c ' token
            if ' c ' in f' {text} ':
                detected_language = 'c'

        # Topic detection via fuzzy matching against synonyms
        from rapidfuzz import fuzz
        topics = {
            'prime_number': ['prime', 'prime number', 'is prime', 'primes', 'check prime'],
            'sum_two_numbers': ['sum of two numbers', 'add two numbers', 'addition of two numbers',
                                'sum two numbers', 'sum 2 numbers', 'add 2 numbers',
                                'add two integers', 'sum of two integers', 'addition of two integers'],
            'sum_three_numbers': ['sum of three numbers', 'add three numbers', 'addition of three numbers',
                                  'sum three numbers', 'sum 3 numbers', 'add 3 numbers',
                                  'add three integers', 'sum of three integers', 'addition of three integers'],
            'factorial': ['factorial', 'fact', 'n!', 'compute factorial'],
            'fibonacci': ['fibonacci', 'fibo', 'fib sequence', 'fibonacci series'],
            'palindrome': ['palindrome', 'is palindrome', 'reverse equals'],
            'reverse_string': ['reverse string', 'string reverse', 'rev string'],
            'sum_array': ['sum array', 'array sum', 'sum of array', 'sum list'],
            'bubble_sort': ['bubble sort', 'sort bubble', 'simple sort'],
            'binary_search': ['binary search', 'bsearch', 'search sorted'],
            'gcd': ['gcd', 'greatest common divisor', 'hcf', 'highest common factor'],
            'lcm': ['lcm', 'least common multiple']
        }

        best_topic, best_score = None, 0
        for topic, syns in topics.items():
            for s in syns:
                score = fuzz.partial_ratio(text, s)
                if score > best_score:
                    best_topic, best_score = topic, score

        return {
            'language': detected_language,
            'topic': best_topic if best_score >= 60 else None,
            'location': location,
            'original_input': original_text
        }
    
    def parse_command(self, user_input: str) -> Dict:
        """
        Parse user command and return structured result
        
        Returns:
            {
                'intent': str or None,
                'confidence': int,
                'original_input': str,
                'understood': bool,
                'params': dict (for folder/file operations)
            }
        """
        intent, confidence = self.detect_intent(user_input)
        
        result = {
            'intent': intent,
            'confidence': confidence,
            'original_input': user_input,
            'understood': intent is not None
        }
        
        # Extract parameters for folder/file operations
        if intent in ['create_folder', 'delete_folder', 'create_file', 'delete_file']:
            result['params'] = self.extract_folder_file_params(user_input)
        elif intent == 'write_program':
            result['params'] = self.extract_program_params(user_input)
        
        return result
    
    def get_all_intents(self) -> List[str]:
        """Get list of all available intents"""
        return list(self.intent_patterns.keys())


# Global NLP engine instance
nlp_engine = OfflineNLP()


def parse_with_fuzzy_nlp(user_input: str) -> Dict:
    """
    Main function to parse user commands with fuzzy matching
    """
    return nlp_engine.parse_command(user_input)


# Test function
if __name__ == "__main__":
    test_commands = [
        "opn calc",           # typo
        "open setting",       # missing 's'
        "chk stroage",        # typo
        "open noteapd",       # typo
        "battry status",      # typo
        "shutdwn pc",         # typo
        "launch crome",       # typo
        "show ip adress",     # typo
        "increse volum",      # typo
        "open whatsap"        # typo
    ]
    
    print("🧪 Testing Offline NLP with Fuzzy Matching\n")
    print("=" * 60)
    
    for cmd in test_commands:
        result = parse_with_fuzzy_nlp(cmd)
        status = "✅" if result['understood'] else "❌"
        print(f"{status} '{cmd}' → {result['intent']} (confidence: {result['confidence']}%)")
    
    print("=" * 60)
