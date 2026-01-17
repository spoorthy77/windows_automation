"""
Hybrid Chatbot Launcher

Main entry point for the Windows Automation Hybrid Chatbot.
Allows users to choose between GUI and Terminal modes.
"""

import sys
import os


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    """Print the welcome banner."""
    banner = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║       🤖 WINDOWS AUTOMATION CHATBOT (HYBRID MODE)             ║
║                                                                ║
║       Automatic Online/Offline Mode Switching                 ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

✨ FEATURES:
   🟢 Online Mode  : Uses Grok AI for intelligent responses
   🔴 Offline Mode : Uses local NLP with fuzzy matching
   🔄 Auto-Switch  : Seamlessly switches based on internet
   💪 100% Offline : Works completely without internet
   🎯 Typo-Tolerant: Understands spelling mistakes

📌 REQUIREMENTS:
   ✅ Python 3.7+
   ✅ Required packages (see requirements.txt)
   ⚠️  Grok API key (optional, for online mode)

════════════════════════════════════════════════════════════════
"""
    print(banner)


def main():
    """Main launcher function."""
    clear_screen()
    print_banner()
    
    print("SELECT MODE:")
    print()
    print("  1. 🖥️  GUI Mode (Graphical Interface)")
    print("  2. 💻 Terminal Mode (Command Line)")
    print("  3. 🧪 Test Network Detection")
    print("  4. 🔧 Test Offline NLP")
    print("  5. ❌ Exit")
    print()
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice == "1":
        print("\n🚀 Launching GUI mode...")
        try:
            from hybrid_gui import launch_gui
            launch_gui()
        except ImportError as e:
            print(f"❌ Error: {e}")
            print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
        except Exception as e:
            print(f"❌ Error launching GUI: {e}")
    
    elif choice == "2":
        print("\n🚀 Launching Terminal mode...")
        try:
            from hybrid_terminal import main as terminal_main
            terminal_main()
        except ImportError as e:
            print(f"❌ Error: {e}")
            print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
        except Exception as e:
            print(f"❌ Error launching terminal: {e}")
    
    elif choice == "3":
        print("\n🧪 Testing Network Detection...")
        print("-" * 60)
        try:
            from network_detector import check_internet, get_connection_status
            
            is_online, message = get_connection_status()
            print(message)
            
            if is_online:
                print("✅ Internet connection detected!")
                print("📡 Chatbot will use Grok API for online mode")
            else:
                print("⚠️  No internet connection detected!")
                print("💾 Chatbot will use offline NLP mode")
            
            print("-" * 60)
            input("\nPress Enter to return to menu...")
            main()
        
        except Exception as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to return to menu...")
            main()
    
    elif choice == "4":
        print("\n🧪 Testing Offline NLP with Fuzzy Matching...")
        print("-" * 60)
        try:
            from offline_mode_handler import parse_offline
            
            test_commands = [
                "opn calcalator",  # Typos
                "open setings",    # Typo in settings
                "show me the baterry status",  # Battery typo
                "lauch notpad",    # Multiple typos
                "increse volume",  # Increase typo
                "shutdwn the computer",  # Shutdown typo
            ]
            
            for cmd in test_commands:
                print(f"\n📝 Testing: '{cmd}'")
                result = parse_offline(cmd)
                print(f"   ✅ Intent: {result['intent']}")
                print(f"   📊 Confidence: {result['confidence']:.2%}")
            
            print("\n" + "-" * 60)
            print("✅ Offline NLP test complete!")
            input("\nPress Enter to return to menu...")
            main()
        
        except Exception as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to return to menu...")
            main()
    
    elif choice == "5":
        print("\n👋 Goodbye! Have a great day!")
        sys.exit(0)
    
    else:
        print("\n❌ Invalid choice. Please select 1-5.")
        input("\nPress Enter to try again...")
        main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Have a great day!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
