# 🤖 Windows Automation Chatbot (Python)

## Description
A conversational AI-powered Python chatbot that automates Windows system tasks through natural language commands. Available in both **Terminal** and **GUI** versions (like ChatGPT/Gemini)!

## 🎨 Two Ways to Use

### 🖥️ **GUI Version** (Recommended) - ChatGPT-like Interface
Beautiful, modern chat window with dark theme:
- Run: `python gui_chatbot.py` or double-click `start_gui.bat`
- See [README_GUI.md](README_GUI.md) for details

### 💻 **Terminal Version** - Classic Command Line
Traditional terminal-based chatbot:
- Run: `python main.py`

## ✨ Features
- **Natural Language Understanding**: Chat naturally like "show me my files" or "what's my CPU usage?"
- **Modern GUI Interface**: ChatGPT-style window with color-coded messages
- **Conversational Interface**: Friendly chatbot-style interaction with emojis and helpful responses
- **🤖 Offline AI Program Generator**: Generate complete programs (Python, Java, C, C++) using local LLM - NO INTERNET REQUIRED!
- **System Monitoring**: CPU, memory, disk usage, battery status, and storage
- **File Management**: Create, delete, and open folders with simple commands
- **Application Launcher**: Open WhatsApp, Notepad, Calculator, Chrome, Task Manager, and more
- **System Settings**: Dark mode, network settings, Bluetooth control
- **Volume Control**: Mute, increase, or decrease volume
- **Power Management**: Shutdown, restart, and lock your PC with safety confirmations
- **Voice Support**: Optional text-to-speech output (pyttsx3) in terminal version
- **Activity Logging**: All commands and responses are logged to logs.txt

## 🛠️ Technologies Used
- **Python 3**
- **Tkinter** - GUI framework (built-in)
- **psutil** - System and process monitoring
- **subprocess** - Execute Windows commands
- **pyttsx3** - Text-to-speech (optional)
- **comtypes** - Windows automation
- **Threading** - Non-blocking GUI operations
- **Regular Expressions** - Natural language parsing

## 🚀 How to Run

### Quick Start (GUI Version):
```bash
# Double-click this file:
start_gui.bat

# Or run manually:
automation_env\Scripts\activate
python gui_chatbot.py
```

### Terminal Version:
```bash
# 1. Activate the virtual environment:
automation_env\Scripts\activate
```

### 2. Run the chatbot:
```bash
python main.py
```

### 3. Start chatting!
Type your commands naturally or use shortcuts (0-9)

## 💬 Example Conversations

### Natural Language Commands:
```
You: hello
Bot: Hello! I'm your Windows automation assistant. How can I help you today?

You: show me the files in this folder
Bot: 📁 Files and folders in current directory:
     [lists files...]

You: what's my CPU usage?
Bot: ⚡ CPU Usage: 15.2%

You: how much RAM am I using?
Bot: 🧠 Memory Usage: 45.3% (7.26 GB / 16.0 GB)

You: create a folder called TestProject
Bot: ✅ Folder created successfully: 📁 TestProject

You: open notepad
Bot: ✅ Notepad opened successfully! 📝

You: what time is it?
Bot: 🕐 Current Date & Time: 11-01-2026 02:30 PM

You: check my battery
Bot: 🔋 Battery Level: 85% | Plugged in: 🔌 Yes

You: thank you
Bot: You're welcome! Happy to help. Is there anything else you need?
```

### Quick Shortcuts:
```
You: 9
Bot: 📊 SYSTEM SUMMARY
     ⚡ CPU Usage       : 12.5%
     🧠 Memory Usage    : 42.1%
     💾 Total RAM       : 16.0 GB
     💿 Disk C: Used    : 245.67 GB
     📁 Disk C: Free    : 210.33 GB
     📈 Disk C: Usage   : 53.9%
```

## 📖 Available Commands

### 🔢 Quick Shortcuts:
- `0` - Toggle voice on/off
- `1` - List files in directory
- `2` - Show IP address
- `3` - System info (detailed)
- `4` - CPU usage
- `5` - Memory/RAM usage
- `6` - Clear screen
- `7` - Help menu
- `8` - Exit program
- `9` - System summary

### 🗣️ Natural Language Commands:

#### 📁 File & Folder Management:
- "show me the files" / "what files are here?"
- "create a folder called MyData"
- "delete the folder named temp"
- "open the Downloads folder"

#### 🖥️ System Information:
- "how much RAM am I using?" / "memory usage"
- "what's my CPU usage?" / "check cpu"
- "show me system information"
- "what's my IP address?"
- "check battery" / "battery status"
- "what time is it?" / "show date and time"

#### 🔧 Open Applications:
- "open notepad" / "launch notepad"
- "open calculator" / "start calculator"
- "open chrome" / "launch browser"
- "open command prompt" / "start cmd"

#### ⚡ Power Commands:
- "shutdown the computer" / "turn off pc"
- "restart my computer" / "reboot"
- "lock my screen" / "lock pc"
- "cancel shutdown"

#### 💬 Social Commands:
- "hello" / "hi" / "hey"
- "how are you?"
- "thank you" / "thanks"
- "who are you?" / "what's your name?"

#### 🤖 AI Program Generation (NEW!):
- "write a python program to calculate factorial"
- "create a java program for bubble sort"
- "generate python code for fibonacci series"
- "make a c program to reverse a string"
- "write cpp code for linked list implementation"

**Note**: Requires Ollama installed. See [OFFLINE_LLM_SETUP.md](OFFLINE_LLM_SETUP.md) for setup instructions.

## 📝 Project Structure
```
automation_project/
├── main.py                    # Main chatbot interface
├── hybrid_launcher.py         # Hybrid online/offline launcher
├── hybrid_chatbot_core.py     # Core chatbot logic
├── offline_mode_handler.py    # Offline NLP handler
├── command_parser.py          # Natural language command parser
├── actions.py                 # Windows automation functions
├── offline_llm_client.py      # 🆕 Local LLM integration (Ollama)
├── code_validator.py          # 🆕 Multi-language code validator
├── program_generator.py       # 🆕 AI program generation pipeline
├── test_offline_llm.py        # 🆕 Test suite for LLM features
├── voice.py                   # Text-to-speech functionality
├── logger.py                  # Activity logging
├── logs.txt                   # Command history log
├── README.md                  # This file
├── OFFLINE_LLM_SETUP.md       # 🆕 Setup guide for AI features
├── OFFLINE_LLM_FEATURE.md     # 🆕 Detailed feature documentation
├── setup_offline_llm.bat      # 🆕 Automated setup script
├── start_program_generator.bat # 🆕 Quick start script
└── automation_env/            # Virtual environment
```

## 🎯 Key Features Explained

### Natural Language Processing
The chatbot uses pattern matching and keyword recognition to understand conversational commands. You don't need to memorize exact syntax - just ask naturally!

### Safety Features
- **Confirmation prompts** for destructive actions (shutdown, restart)
- **30-second delay** on shutdown/restart with cancel option
- **Error handling** for invalid paths and missing folders

### Logging
All interactions are automatically logged to `logs.txt` with timestamps for tracking and debugging.

## 🔮 Future Enhancements
- ✅ **Offline AI Program Generator** (COMPLETED!)
- Web scraping and automation
- Email sending capabilities
- Scheduled task automation
- More advanced NLP with ML models
- Custom command macros
- Program explanation and documentation generation
- Unit test generation for programs
- Support for more programming languages (Go, Rust, JavaScript)

## 📄 License
This is an educational project for learning Python automation.

## 👨‍💻 Author
Created as a beginner-friendly Windows automation learning project.

---
**💡 Pro Tip:** Just type naturally! The chatbot understands conversational commands. Type 'help' anytime to see all available features.
