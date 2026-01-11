"""
Test script for Windows Automation Chatbot
Tests various command parsing scenarios
"""

from command_parser import parse_command
import sys

def test_command(description, command, expected_keyword=None):
    """Test a single command"""
    print(f"\nTesting: {description}")
    print(f"Command: '{command}'")
    response = parse_command(command)
    print(f"Response: {response[:100]}...")  # Show first 100 chars
    
    if expected_keyword and expected_keyword.lower() not in response.lower():
        print(f"❌ FAILED - Expected keyword '{expected_keyword}' not found")
        return False
    else:
        print("✅ PASSED")
        return True

def run_tests():
    print("=" * 70)
    print("🧪 WINDOWS AUTOMATION CHATBOT - TEST SUITE")
    print("=" * 70)
    
    tests_passed = 0
    tests_total = 0
    
    # Test cases
    test_cases = [
        # Natural language greetings
        ("Greeting - hello", "hello", "Hello"),
        ("Greeting - hi", "hi", "Hello"),
        ("Casual - how are you", "how are you", "functioning"),
        ("Thanks", "thank you", "welcome"),
        ("Identity", "who are you", "Automation Assistant"),
        
        # System info with natural language
        ("CPU natural", "what's my CPU usage?", "CPU"),
        ("Memory natural", "how much RAM am I using?", "Memory"),
        ("Time natural", "what time is it?", "Date & Time"),
        ("Battery natural", "check battery", "Battery"),
        
        # File operations
        ("List files natural", "show me the files", "Files"),
        ("Create folder", "create folder TestBot", "created"),
        
        # Application launching
        ("Open notepad", "open notepad", "Notepad"),
        ("Launch calculator", "launch calculator", "Calculator"),
        
        # Shortcuts
        ("Shortcut 4", "4", "CPU"),
        ("Shortcut 5", "5", "Memory"),
        ("Shortcut 9", "9", "SYSTEM SUMMARY"),
        
        # Help
        ("Help command", "help", "Available Commands"),
        
        # Unknown command
        ("Unknown command", "xyz123abc", "understand"),
    ]
    
    for description, command, expected in test_cases:
        tests_total += 1
        if test_command(description, command, expected):
            tests_passed += 1
    
    # Summary
    print("\n" + "=" * 70)
    print(f"📊 TEST RESULTS: {tests_passed}/{tests_total} tests passed")
    if tests_passed == tests_total:
        print("✅ All tests PASSED!")
    else:
        print(f"❌ {tests_total - tests_passed} test(s) FAILED")
    print("=" * 70)
    
    return tests_passed == tests_total

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
