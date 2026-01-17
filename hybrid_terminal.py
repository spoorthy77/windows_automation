"""
Hybrid Chatbot Terminal Version

Terminal/console version of the hybrid chatbot with automatic online/offline mode switching.
"""

import os
from hybrid_chatbot_core import process_user_input, get_current_mode
from logger import log_event


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    """Print the chatbot header."""
    print("=" * 70)
    print("🤖 WINDOWS AUTOMATION CHATBOT (HYBRID MODE)")
    print("=" * 70)
    print("💡 Automatic Online/Offline Mode Switching")
    print("🟢 Online Mode: Uses Grok AI for intelligent responses")
    print("🔴 Offline Mode: Uses local NLP with fuzzy matching")
    print("=" * 70)
    
    # Show current mode
    mode, status = get_current_mode()
    print(f"\n{status}")
    print("=" * 70)
    print()


def print_help():
    """Print help information."""
    help_text = """
╔═══════════════════════════════════════════════════════════════╗
║                    AVAILABLE COMMANDS                         ║
╚═══════════════════════════════════════════════════════════════╝

📁 FILES & FOLDERS:
   • list files, show files
   • create folder [name]
   • delete folder [name]
   • open folder [path]

🖥️  SYSTEM INFORMATION:
   • cpu usage, memory usage, ram usage
   • battery status, check battery
   • check storage, disk space
   • system info, system summary
   • show ip, ip address
   • what time is it?, show date

🚀 OPEN APPLICATIONS:
   • open notepad, calculator, chrome, cmd
   • open whatsapp, task manager
   • open settings, network settings

⚙️  SYSTEM CONTROLS:
   • enable dark mode / night theme
   • mute volume, increase volume, decrease volume
   • turn on/off bluetooth
   • lock pc, shutdown pc, restart pc
   • cancel shutdown

💡 SPECIAL COMMANDS:
   • help - Show this help menu
   • clear - Clear screen
   • mode - Show current mode
   • refresh - Refresh connection status
   • exit - Exit chatbot

✨ HYBRID FEATURES:
   • Works 100% offline for automation
   • Auto-switches between online/offline modes
   • Understands typos: "opn setings" → "open settings"
   • Fuzzy matching: "lauch notpad" → "launch notepad"

Type naturally! I understand conversational commands.
"""
    print(help_text)


def main():
    """Main function to run the hybrid terminal chatbot."""
    clear_screen()
    print_header()
    
    print("💬 Chat naturally with me to automate your Windows tasks!")
    print("📖 Type 'help' to see commands | Type 'exit' to quit")
    print("=" * 70)
    print()
    
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() in ["exit", "quit", "bye", "8"]:
                print("\n🤖 Bot: Goodbye! Have a great day! 👋")
                log_event(user_input, "Goodbye! (Program Exit)")
                break
            
            if user_input.lower() in ["clear", "cls", "6"]:
                clear_screen()
                print_header()
                print("🤖 Bot: Screen cleared ✨")
                log_event(user_input, "Screen cleared")
                continue
            
            if user_input.lower() in ["help", "?", "7"]:
                print_help()
                log_event(user_input, "Help displayed")
                continue
            
            if user_input.lower() in ["mode", "status", "refresh", "check mode"]:
                mode, status = get_current_mode()
                print(f"\n🤖 Bot: {status}")
                log_event(user_input, status)
                continue
            
            # Process command through hybrid core
            response, mode = process_user_input(user_input)
            
            # Display response with mode indicator
            mode_indicator = "🟢 [ONLINE]" if mode == "online" else "🔴 [OFFLINE]"
            print(f"\n🤖 Bot {mode_indicator}: {response}")
        
        except KeyboardInterrupt:
            print("\n\n🤖 Bot: Goodbye! Have a great day! 👋")
            break
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("💡 Type 'help' for assistance or 'exit' to quit")


if __name__ == "__main__":
    main()
