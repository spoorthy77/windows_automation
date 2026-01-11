"""
Demo script to showcase the Windows Automation Chatbot capabilities
This demonstrates various natural language commands the chatbot understands
"""

from command_parser import parse_command

def demo_chatbot():
    print("=" * 70)
    print("🤖 WINDOWS AUTOMATION CHATBOT - DEMO MODE")
    print("=" * 70)
    print("This demo shows various commands the chatbot understands\n")
    
    # List of demo commands
    demo_commands = [
        ("hello", "Greeting the chatbot"),
        ("what's my CPU usage?", "Checking CPU usage with natural language"),
        ("show me system summary", "Getting a complete system overview"),
        ("how much RAM am I using?", "Checking memory usage conversationally"),
        ("what time is it?", "Asking for current date and time"),
        ("who are you?", "Asking about the chatbot"),
        ("create folder TestDemo", "Creating a new folder"),
        ("thank you", "Being polite to the chatbot"),
        ("help", "Viewing all available commands"),
    ]
    
    for command, description in demo_commands:
        print(f"\n{'='*70}")
        print(f"📝 Example: {description}")
        print(f"💬 User: {command}")
        response = parse_command(command)
        print(f"🤖 Bot: {response}")
        print(f"{'='*70}")
        input("\nPress Enter to continue...")
    
    print("\n" + "=" * 70)
    print("✅ Demo complete! Run 'python main.py' to start the chatbot")
    print("=" * 70)

if __name__ == "__main__":
    demo_chatbot()
