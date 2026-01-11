"""
Demo Script - Shows example commands you can try in the GUI

Copy and paste these commands one by one into the chatbot to see what it can do!
"""

DEMO_COMMANDS = [
    # System Information
    "check battery",
    "show disk space", 
    "check cpu usage",
    "show memory usage",
    
    # Open Applications
    "open calculator",
    "open notepad",
    "open task manager",
    
    # System Settings
    "enable night theme",
    "open settings",
    
    # Volume Control
    "mute volume",
    "increase volume",
    
    # File Management
    "create folder TestFolder",
    "delete folder TestFolder",
    
    # Help & Info
    "help",
    "what time is it",
    "show ip address",
    
    # Conversational
    "hello",
    "how are you",
    "thank you",
]

print("=" * 70)
print("🎬 DEMO COMMANDS - Try these in your GUI chatbot!")
print("=" * 70)
print("\nCopy and paste these commands one at a time:\n")

for i, cmd in enumerate(DEMO_COMMANDS, 1):
    print(f"{i:2d}. {cmd}")

print("\n" + "=" * 70)
print("💡 TIP: You can also type your own natural language commands!")
print("=" * 70)
