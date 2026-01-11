"""
Test script for NLP Intent Recognition Module
Demonstrates fuzzy matching, spelling correction, and natural language understanding
"""

from nlp_intent_parser import nlp_parser, parse_with_nlp
from command_parser import parse_command


def test_nlp_variations():
    """Test various command variations and spelling mistakes."""
    
    print("=" * 80)
    print("🧪 NLP INTENT RECOGNITION - TEST SUITE")
    print("=" * 80)
    print()
    
    # Test cases with variations, typos, and natural language
    test_cases = [
        # Settings variations (the example from requirements)
        ("open settings", "open_settings"),
        ("open setting", "open_settings"),  # singular
        ("open setings", "open_settings"),  # typo
        ("settings open", "open_settings"),  # reversed
        ("go to settings", "open_settings"),  # natural variation
        ("open my settings", "open_settings"),  # with possessive
        ("launch settings", "open_settings"),  # synonym
        
        # File operations with typos
        ("list files", "list_files"),
        ("list file", "list_files"),  # singular
        ("show fils", "list_files"),  # typo
        ("display files", "list_files"),  # synonym
        ("what files are here", "list_files"),  # natural language
        ("show me the files", "list_files"),
        
        # Calculator variations
        ("open calculator", "open_calculator"),
        ("open calculater", "open_calculator"),  # typo
        ("open calc", "open_calculator"),  # abbreviation
        ("start calculator", "open_calculator"),  # synonym
        ("launch calc", "open_calculator"),
        
        # Notepad variations
        ("open notepad", "open_notepad"),
        ("open notpad", "open_notepad"),  # typo
        ("launch notepad", "open_notepad"),
        ("start notepade", "open_notepad"),  # typo
        
        # System info variations
        ("cpu usage", "cpu_usage"),
        ("cpu usag", "cpu_usage"),  # typo
        ("check cpu", "cpu_usage"),
        ("processor usage", "cpu_usage"),  # synonym
        ("how much cpu", "cpu_usage"),  # natural language
        
        # Memory variations
        ("memory usage", "memory_usage"),
        ("ram usage", "memory_usage"),  # synonym
        ("check memory", "memory_usage"),
        ("how much ram", "memory_usage"),  # natural language
        ("memry usage", "memory_usage"),  # typo
        
        # Time/date variations
        ("what time is it", "show_datetime"),
        ("show time", "show_datetime"),
        ("current time", "show_datetime"),
        ("show date", "show_datetime"),
        ("what's the time", "show_datetime"),
        
        # Battery variations
        ("battery status", "battery_status"),
        ("check battery", "battery_status"),
        ("battery level", "battery_status"),
        ("power status", "battery_status"),
        ("baterry status", "battery_status"),  # typo
        
        # Chrome variations
        ("open chrome", "open_chrome"),
        ("launch chrome", "open_chrome"),
        ("start chrome", "open_chrome"),
        ("open chrom", "open_chrome"),  # typo
        
        # Volume control
        ("mute volume", "mute_volume"),
        ("mute sound", "mute_volume"),
        ("increase volume", "increase_volume"),
        ("volume up", "increase_volume"),
        ("make it louder", "increase_volume"),
        ("decrease volume", "decrease_volume"),
        ("volume down", "decrease_volume"),
        
        # Folder operations with parameters
        ("create folder MyData", "create_folder"),
        ("make folder test123", "create_folder"),
        ("create foldr Documents", "create_folder"),  # typo
        
        # Bluetooth
        ("turn on bluetooth", "turn_on_bluetooth"),
        ("enable bluetooth", "turn_on_bluetooth"),
        ("turn off bluetooth", "turn_off_bluetooth"),
        ("disable bluetooth", "turn_off_bluetooth"),
    ]
    
    print(f"Testing {len(test_cases)} command variations...\n")
    
    passed = 0
    failed = 0
    
    for test_input, expected_intent in test_cases:
        result = parse_with_nlp(test_input, confidence_threshold=0.5)
        
        if result:
            detected_intent = result["intent"]
            confidence = result["confidence"]
            
            if detected_intent == expected_intent:
                status = "✅ PASS"
                passed += 1
                confidence_indicator = "🎯" if confidence >= 0.85 else "✓"
            else:
                status = "❌ FAIL"
                failed += 1
                confidence_indicator = "✗"
            
            print(f"{status} {confidence_indicator} '{test_input}'")
            print(f"    Expected: {expected_intent}")
            print(f"    Detected: {detected_intent} (confidence: {confidence:.2%})")
            
            if result.get("parameters"):
                print(f"    Parameters: {result['parameters']}")
            print()
        else:
            print(f"❌ FAIL ✗ '{test_input}'")
            print(f"    Expected: {expected_intent}")
            print(f"    Detected: No confident match found")
            print()
            failed += 1
    
    # Print summary
    print("=" * 80)
    print(f"📊 TEST RESULTS SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {len(test_cases)}")
    print(f"✅ Passed: {passed} ({(passed/len(test_cases)*100):.1f}%)")
    print(f"❌ Failed: {failed} ({(failed/len(test_cases)*100):.1f}%)")
    print("=" * 80)
    print()
    
    return passed, failed


def test_spelling_mistakes():
    """Test specific spelling mistakes and typos."""
    
    print("=" * 80)
    print("📝 SPELLING MISTAKE TOLERANCE TEST")
    print("=" * 80)
    print()
    
    spelling_tests = [
        ("open setings", "open settings"),  # missing 't'
        ("open settigns", "open settings"),  # transposed letters
        ("calculater", "calculator"),  # extra 'e'
        ("notpad", "notepad"),  # missing 'e'
        ("memry", "memory"),  # missing 'o'
        ("baterry", "battery"),  # wrong vowel
        ("chrom", "chrome"),  # missing 'e'
        ("foldr", "folder"),  # missing 'e'
        ("shoutdown", "shutdown"),  # wrong letter
        ("restar", "restart"),  # missing 't'
    ]
    
    for misspelled, correct in spelling_tests:
        result = parse_with_nlp(f"open {misspelled}" if not misspelled.startswith("open") else misspelled, confidence_threshold=0.5)
        
        if result:
            print(f"✅ '{misspelled}' → Recognized as '{result['intent']}' (confidence: {result['confidence']:.2%})")
        else:
            print(f"❌ '{misspelled}' → Not recognized")
    
    print()


def test_natural_language():
    """Test natural language variations."""
    
    print("=" * 80)
    print("💬 NATURAL LANGUAGE UNDERSTANDING TEST")
    print("=" * 80)
    print()
    
    natural_tests = [
        "show me the files in this directory",
        "what's my CPU usage right now",
        "how much memory am I using",
        "can you open the calculator please",
        "I need to check my battery level",
        "what time is it",
        "turn the volume up",
        "make my screen darker",
        "go to my settings",
        "launch chrome browser",
    ]
    
    for test_input in natural_tests:
        result = parse_with_nlp(test_input, confidence_threshold=0.5)
        
        if result:
            print(f"✅ '{test_input}'")
            print(f"    → Intent: {result['intent']} (confidence: {result['confidence']:.2%})")
            if result.get("parameters"):
                print(f"    → Parameters: {result['parameters']}")
        else:
            print(f"❌ '{test_input}'")
            print(f"    → Not recognized")
        print()
    
    print()


def test_edge_cases():
    """Test edge cases and ambiguous commands."""
    
    print("=" * 80)
    print("🔍 EDGE CASES TEST")
    print("=" * 80)
    print()
    
    edge_cases = [
        "settings",  # single word
        "open",  # incomplete command
        "setttings",  # multiple typos
        "what files",  # abbreviated
        "cpu",  # single word
        "calculator",  # without action verb
    ]
    
    for test_input in edge_cases:
        result = parse_with_nlp(test_input, confidence_threshold=0.5)
        
        if result:
            print(f"✅ '{test_input}'")
            print(f"    → Intent: {result['intent']} (confidence: {result['confidence']:.2%})")
        else:
            print(f"⚠️  '{test_input}'")
            print(f"    → No confident match (ambiguous)")
        print()
    
    print()


def interactive_test():
    """Interactive mode to test custom inputs."""
    
    print("=" * 80)
    print("🎮 INTERACTIVE TEST MODE")
    print("=" * 80)
    print("Type commands to test NLP recognition (or 'quit' to exit)")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Exiting interactive mode...")
                break
            
            if not user_input:
                continue
            
            # Parse with NLP
            result = parse_with_nlp(user_input, confidence_threshold=0.5)
            
            if result:
                print(f"🎯 Intent: {result['intent']}")
                print(f"   Confidence: {result['confidence']:.2%}")
                if result.get("parameters"):
                    print(f"   Parameters: {result['parameters']}")
                
                # Show top 3 matching intents
                sorted_scores = sorted(result["all_scores"].items(), key=lambda x: x[1], reverse=True)[:3]
                print(f"   Top matches:")
                for intent, score in sorted_scores:
                    print(f"      - {intent}: {score:.2%}")
            else:
                print("❌ No confident match found")
            
            print()
        
        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    # Run all tests
    test_nlp_variations()
    test_spelling_mistakes()
    test_natural_language()
    test_edge_cases()
    
    # Optionally run interactive mode
    print("\n" + "=" * 80)
    response = input("Run interactive test mode? (y/n): ").strip().lower()
    if response == "y":
        interactive_test()
    
    print("\n✅ All tests completed!")
