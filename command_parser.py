import re
from nlp_intent_parser import parse_with_nlp, nlp_parser
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
    turn_off_bluetooth
)


HELP_TEXT = """
🤖 Windows Automation Chatbot - Available Commands

📋 Quick Shortcuts:
  0) Toggle voice on/off
  1) List files in directory
  2) Show IP address
  3) System info (detailed)
  4) CPU usage
  5) Memory/RAM usage
  6) Clear screen
  7) Help menu
  8) Exit program
  9) System summary

🚀 Natural Language Commands (Examples):
  📁 Files & Folders:
     - "show me the files" / "what files are here?"
     - "create a folder called MyData"
     - "delete the folder named temp"
     - "open the Downloads folder"
  
  🖥️ System Info:
     - "how much RAM am I using?" / "memory usage"
     - "what's my CPU usage?" / "check cpu"
     - "show me system information"
     - "what's my IP address?"
     - "check battery" / "battery status"
     - "check storage" / "show disk space"
     - "what time is it?" / "show date and time"
  
  🔧 Open Applications:
     - "open notepad" / "launch notepad"
     - "open calculator" / "start calculator"
     - "open chrome" / "launch browser"
     - "open command prompt" / "start cmd"
     - "open whatsapp" / "launch whatsapp"
     - "open task manager"
     - "show running processes"
  
  🎨 System Settings:
     - "enable night theme" / "make my screen dark"
     - "open settings"
     - "open network settings"
     - "turn on bluetooth" / "turn off bluetooth"
  
  🔊 Volume Control:
     - "mute volume"
     - "increase volume" / "decrease volume"
  
  ⚡ Power Commands:
     - "shutdown the computer" / "turn off pc"
     - "restart my computer" / "reboot"
     - "lock my screen" / "lock pc"
     - "cancel shutdown"

💡 Pro Tip: Just type naturally! The bot understands conversational commands.
"""


def parse_command(user_input: str):
    user_input = user_input.strip()
    lower_input = user_input.lower().strip()

    # ---------- SHORTCUT COMMANDS ----------
    if lower_input == "0":
        return "VOICE_TOGGLE"

    if lower_input == "1":
        return list_files()

    if lower_input == "2":
        return show_ip()

    if lower_input == "3":
        return system_info()

    if lower_input == "4":
        return cpu_usage()

    if lower_input == "5":
        return memory_usage()

    if lower_input == "6":
        return "CLEAR"

    if lower_input == "7":
        return HELP_TEXT

    if lower_input == "8":
        return "EXIT"

    if lower_input == "9":
        return system_summary()

    # ========== NLP-BASED INTENT RECOGNITION ==========
    # Try to parse the command using NLP with fuzzy matching
    nlp_result = parse_with_nlp(user_input, confidence_threshold=0.6)
    
    if nlp_result and nlp_result["confidence"] >= 0.6:
        intent = nlp_result["intent"]
        confidence = nlp_result["confidence"]
        parameters = nlp_result["parameters"]
        
        # Debug info (can be commented out in production)
        # print(f"🎯 NLP Match: {intent} (confidence: {confidence:.2%})")
        
        # Map intents to actions
        intent_action_map = {
            "list_files": list_files,
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "system_info": system_info,
            "system_summary": system_summary,
            "show_ip": show_ip,
            "battery_status": battery_status,
            "check_storage": check_storage,
            "show_datetime": show_datetime,
            "open_notepad": open_notepad,
            "open_calculator": open_calculator,
            "open_chrome": open_chrome,
            "open_cmd": open_cmd,
            "open_whatsapp": open_whatsapp,
            "open_task_manager": open_task_manager,
            "show_running_processes": show_running_processes,
            "open_settings": open_settings,
            "open_network_settings": open_network_settings,
            "enable_night_theme": enable_night_theme,
            "mute_volume": mute_volume,
            "increase_volume": increase_volume,
            "decrease_volume": decrease_volume,
            "turn_on_bluetooth": turn_on_bluetooth,
            "turn_off_bluetooth": turn_off_bluetooth,
            "lock_pc": lock_pc,
            "cancel_shutdown": cancel_shutdown,
        }
        
        # Intents that require parameters
        if intent == "create_folder":
            if parameters:
                return create_folder(parameters)
            else:
                return "❌ Please specify a folder name. Example: create folder MyData"
        
        elif intent == "delete_folder":
            if parameters:
                return delete_folder(parameters)
            else:
                return "❌ Please specify a folder name. Example: delete folder temp"
        
        elif intent == "open_folder":
            if parameters:
                return open_folder(parameters)
            else:
                return "❌ Please specify a folder path. Example: open folder Downloads"
        
        # Power commands need confirmation
        elif intent == "shutdown_pc":
            return "CONFIRM_SHUTDOWN"
        
        elif intent == "restart_pc":
            return "CONFIRM_RESTART"
        
        # Execute action for other intents
        elif intent in intent_action_map:
            action_function = intent_action_map[intent]
            return action_function()
    
    # ========== FALLBACK TO LEGACY PARSING ==========
    # If NLP didn't find a confident match, use the old exact matching logic
    
    # ---------- VOICE CONTROL ----------
    if lower_input in ["voice on", "speak on"]:
        return "VOICE_ON"

    if lower_input in ["voice off", "speak off", "mute"]:
        return "VOICE_OFF"

    # ---------- BASIC ----------
    if lower_input in ["exit", "quit"]:
        return "EXIT"

    if lower_input in ["help", "commands"]:
        return HELP_TEXT

    if lower_input in ["clear", "cls"]:
        return "CLEAR"

    # ---------- OPEN APPS ----------
    if "open notepad" in lower_input or "create a text file" in lower_input:
        return open_notepad()

    if "open calculator" in lower_input or "open calc" in lower_input or "start calculator" in lower_input:
        return open_calculator()

    if "open chrome" in lower_input:
        return open_chrome()

    if "open cmd" in lower_input or "open command prompt" in lower_input:
        return open_cmd()
    
    if "open whatsapp" in lower_input or "launch whatsapp" in lower_input or "go to whatsapp" in lower_input:
        return open_whatsapp()
    
    if "open task manager" in lower_input:
        return open_task_manager()
    
    if "show running processes" in lower_input or "show processes" in lower_input:
        return show_running_processes()
    
    # ---------- SYSTEM SETTINGS ----------
    if "night theme" in lower_input or "dark mode" in lower_input or "make my screen dark" in lower_input:
        return enable_night_theme()
    
    if "open network settings" in lower_input:
        return open_network_settings()
    
    if "open settings" in lower_input:
        return open_settings()
    
    # ---------- STORAGE & DISK ----------
    if "check storage" in lower_input or "show disk space" in lower_input or "disk space" in lower_input:
        return check_storage()
    
    # ---------- VOLUME CONTROL ----------
    if "mute volume" in lower_input or "mute sound" in lower_input:
        return mute_volume()
    
    if "increase volume" in lower_input or "volume up" in lower_input or "louder" in lower_input:
        return increase_volume()
    
    if "decrease volume" in lower_input or "volume down" in lower_input or "quieter" in lower_input:
        return decrease_volume()
    
    # ---------- BLUETOOTH ----------
    if "turn on bluetooth" in lower_input or "enable bluetooth" in lower_input:
        return turn_on_bluetooth()
    
    if "turn off bluetooth" in lower_input or "disable bluetooth" in lower_input:
        return turn_off_bluetooth()

    # ---------- FOLDER AUTOMATION ----------
    if lower_input.startswith("create folder"):
        folder_name = user_input[len("create folder"):].strip()
        return create_folder(folder_name)

    if lower_input.startswith("delete folder"):
        folder_name = user_input[len("delete folder"):].strip()
        return delete_folder(folder_name)

    if lower_input.startswith("open folder"):
        path = user_input[len("open folder"):].strip()
        return open_folder(path)

    # ---------- UTILITIES ----------
    if lower_input in ["date time", "time", "date"]:
        return show_datetime()

    if lower_input in ["battery", "battery status"]:
        return battery_status()

    # ---------- POWER COMMANDS ----------
    if lower_input in ["shutdown", "shutdown pc", "turn off pc"]:
        return "CONFIRM_SHUTDOWN"

    if lower_input in ["restart", "restart pc", "reboot"]:
        return "CONFIRM_RESTART"

    if lower_input in ["cancel", "cancel shutdown", "stop shutdown"]:
        return cancel_shutdown()

    if lower_input in ["lock pc", "lock", "lock screen"]:
        return lock_pc()

    # ---------- OLD COMMANDS ----------
    if "list files" in lower_input or "show files" in lower_input:
        return list_files()

    if "show ip" in lower_input or "ip address" in lower_input or lower_input == "ip":
        return show_ip()

    if "system info" in lower_input or "pc info" in lower_input:
        return system_info()

    if "cpu" in lower_input:
        return cpu_usage()

    if "memory" in lower_input or "ram" in lower_input:
        return memory_usage()

    # ---------- NATURAL LANGUAGE PATTERNS ----------
    # File listing patterns
    if any(phrase in lower_input for phrase in ["show files", "what files", "display files", "view files"]):
        return list_files()
    
    # System info patterns
    if any(phrase in lower_input for phrase in ["pc info", "computer info", "system details", "my system"]):
        return system_summary()
    
    # Time/Date patterns
    if any(phrase in lower_input for phrase in ["what time", "current time", "what's the time", "show time"]):
        return show_datetime()
    
    # Battery patterns
    if any(phrase in lower_input for phrase in ["check battery", "battery level", "power status"]):
        return battery_status()
    
    # CPU patterns
    if any(phrase in lower_input for phrase in ["check cpu", "cpu load", "processor usage", "how much cpu"]):
        return cpu_usage()
    
    # Memory patterns
    if any(phrase in lower_input for phrase in ["check memory", "how much ram", "memory status", "ram status"]):
        return memory_usage()
    
    # Launch/Start patterns for apps
    if any(word in lower_input for word in ["launch", "start", "run"]) and "notepad" in lower_input:
        return open_notepad()
    
    if any(word in lower_input for word in ["launch", "start", "run"]) and ("calc" in lower_input or "calculator" in lower_input):
        return open_calculator()
    
    if any(word in lower_input for word in ["launch", "start", "run"]) and "chrome" in lower_input:
        return open_chrome()
    
    # Folder creation with natural language
    create_match = re.search(r'(?:create|make|new)\s+(?:a\s+)?folder\s+(?:called|named)?\s*(.+)', lower_input)
    if create_match:
        folder_name = create_match.group(1).strip()
        return create_folder(folder_name)
    
    # Folder deletion with natural language
    delete_match = re.search(r'(?:delete|remove)\s+(?:the\s+)?folder\s+(?:called|named)?\s*(.+)', lower_input)
    if delete_match:
        folder_name = delete_match.group(1).strip()
        return delete_folder(folder_name)
    
    # Storage patterns
    if any(phrase in lower_input for phrase in ["storage", "disk", "drive space", "hard drive"]):
        return check_storage()
    
    # Battery percentage patterns
    if any(phrase in lower_input for phrase in ["battery percentage", "show battery", "battery percent"]):
        return battery_status()
    
    # WhatsApp patterns
    if any(word in lower_input for word in ["launch", "start", "open"]) and "whatsapp" in lower_input:
        return open_whatsapp()
    
    # Task manager patterns
    if any(phrase in lower_input for phrase in ["task manager", "process manager"]):
        return open_task_manager()
    
    # Greetings and casual responses
    if any(greeting in lower_input for greeting in ["hello", "hi", "hey", "greetings"]):
        return "Hello! I'm your Windows automation assistant. How can I help you today? Type 'help' to see what I can do."
    
    if any(phrase in lower_input for phrase in ["how are you", "how do you do", "what's up", "whats up"]):
        return "I'm functioning perfectly and ready to help! What task would you like me to perform?"
    
    if any(phrase in lower_input for phrase in ["thank you", "thanks", "appreciate it"]):
        return "You're welcome! Happy to help. Is there anything else you need?"
    
    if "your name" in lower_input or "who are you" in lower_input:
        return "I'm your Windows Automation Assistant! I can help you manage files, check system info, open apps, and much more. Type 'help' for details."

    # Default response with suggestions
    return "🤔 I didn't quite understand that. Try:\n  • Type 'help' to see all commands\n  • Ask naturally like 'show my files' or 'what's my CPU usage?'\n  • Use shortcuts 0-9 for quick actions"
