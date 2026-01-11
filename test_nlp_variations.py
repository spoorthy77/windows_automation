"""
Test Script for NLP Intent Recognition Module
Tests spelling mistakes, grammatical variations, and word order differences
"""

from nlp_intent_parser import nlp_parser

def test_variations():
    """Test various command variations to verify NLP robustness."""
    
    print("=" * 80)
    print("🧪 NLP INTENT RECOGNITION - VARIATION TESTING")
    print("=" * 80)
    print()
    
    # Test cases: various ways to say the same thing
    test_cases = {
        "Open Settings": [
            "open settings",        # Correct
            "open setting",         # Singular form
            "open setings",         # Spelling mistake
            "settings open",        # Word order change
            "go to settings",       # Synonym
            "open my settings",     # Extra words
            "launch settings",      # Synonym
            "settingz",            # Typo
        ],
        "List Files": [
            "list files",
            "list file",           # Singular
            "show files",          # Synonym
            "display files",       # Synonym
            "what files are here",
            "show me files",
            "files",               # Minimal
        ],
        "CPU Usage": [
            "cpu usage",
            "check cpu",
            "cpu",
            "show cpu usage",
            "how much cpu",
            "processor usage",
            "check my cpu",
        ],
        "Memory Usage": [
            "memory usage",
            "ram usage",
            "check memory",
            "how much ram",
            "show memory",
            "memory",
        ],
        "Open Notepad": [
            "open notepad",
            "launch notepad",
            "start notepad",
            "notepad",
            "open notpad",         # Typo
            "notepad open",        # Word order
        ],
        "Open Calculator": [
            "open calculator",
            "calculator",
            "open calc",
            "launch calculator",
            "start calc",
            "calcuator",          # Typo
        ],
        "Battery Status": [
            "battery status",
            "check battery",
            "battery",
            "show battery",
            "how much battery",
            "battry status",      # Typo
        ],
        "System Info": [
            "system info",
            "system information",
            "pc info",
            "computer info",
            "system details",
            "systm info",         # Typo
        ],
        "Create Folder": [
            "create folder test",
            "make folder test",
            "new folder test",
            "create a folder test",
            "make a folder called test",
        ],
        "Open Chrome": [
            "open chrome",
            "launch chrome",
            "start chrome",
            "chrome",
            "open browser",
            "start browser",
        ],
    }
    
    # Run tests
    results = {
        "passed": 0,
        "failed": 0,
        "total": 0
    }
    
    for command_category, variations in test_cases.items():
        print(f"\n📋 Testing: {command_category}")
        print("-" * 80)
        
        for variation in variations:
            results["total"] += 1
            result = nlp_parser.parse_intent(variation)
            
            intent = result["intent"]
            confidence = result["confidence"]
            
            # Determine if this is a reasonable match
            # (We expect confidence > 0.5 for valid variations)
            status = "✅ PASS" if confidence >= 0.5 else "❌ FAIL"
            
            if confidence >= 0.5:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            print(f"  {status} | Input: '{variation:30s}' → Intent: {intent:20s} | Confidence: {confidence:.2%}")
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {results['total']}")
    print(f"✅ Passed: {results['passed']} ({results['passed']/results['total']*100:.1f}%)")
    print(f"❌ Failed: {results['failed']} ({results['failed']/results['total']*100:.1f}%)")
    print("=" * 80)
    
    return results


def test_specific_requirement():
    """Test the specific requirement from the project: 'open settings' variations."""
    
    print("\n" + "=" * 80)
    print("🎯 SPECIFIC REQUIREMENT TEST: 'Open Settings' Variations")
    print("=" * 80)
    print()
    
    variations = [
        "open settings",
        "open setting",
        "open setings",
        "settings open",
        "go to settings",
        "open my settings",
    ]
    
    expected_intent = "open_settings"
    
    print("Expected Intent: open_settings")
    print("-" * 80)
    
    all_passed = True
    for variation in variations:
        result = nlp_parser.parse_intent(variation)
        intent = result["intent"]
        confidence = result["confidence"]
        
        # Check if intent matches and confidence is reasonable
        passed = intent == expected_intent and confidence >= 0.5
        status = "✅" if passed else "❌"
        
        if not passed:
            all_passed = False
        
        print(f"{status} '{variation:25s}' → {intent:20s} (confidence: {confidence:.2%})")
    
    print("-" * 80)
    if all_passed:
        print("✅ ALL TESTS PASSED! NLP handles all variations correctly.")
    else:
        print("⚠️ Some tests failed. Review NLP configuration.")
    print("=" * 80)


def demo_fuzzy_matching():
    """Demonstrate fuzzy matching capabilities."""
    
    print("\n" + "=" * 80)
    print("🔍 FUZZY MATCHING DEMONSTRATION")
    print("=" * 80)
    print()
    
    # Examples with typos
    typo_examples = [
        ("open notepd", "open_notepad"),
        ("calcuator", "open_calculator"),
        ("battry status", "battery_status"),
        ("systm info", "system_info"),
        ("memry usage", "memory_usage"),
        ("shut down pc", "shutdown_pc"),
        ("increese volume", "increase_volume"),
        ("netwrk settings", "open_network_settings"),
    ]
    
    print("Testing commands with spelling mistakes:")
    print("-" * 80)
    
    for typo_input, expected_intent in typo_examples:
        result = nlp_parser.parse_intent(typo_input)
        intent = result["intent"]
        confidence = result["confidence"]
        
        status = "✅" if intent == expected_intent else "⚠️"
        
        print(f"{status} '{typo_input:25s}' → {intent:25s} (confidence: {confidence:.2%})")
    
    print("=" * 80)


def test_word_order():
    """Test that word order doesn't break intent recognition."""
    
    print("\n" + "=" * 80)
    print("🔄 WORD ORDER VARIATION TEST")
    print("=" * 80)
    print()
    
    word_order_tests = [
        ("open settings", "settings open", "open_settings"),
        ("check battery", "battery check", "battery_status"),
        ("list files", "files list", "list_files"),
        ("show ip", "ip show", "show_ip"),
        ("open notepad", "notepad open", "open_notepad"),
    ]
    
    print("Testing commands with different word orders:")
    print("-" * 80)
    
    for normal_order, reversed_order, expected_intent in word_order_tests:
        result1 = nlp_parser.parse_intent(normal_order)
        result2 = nlp_parser.parse_intent(reversed_order)
        
        match1 = result1["intent"] == expected_intent
        match2 = result2["intent"] == expected_intent
        
        status = "✅" if (match1 and match2) else "⚠️"
        
        print(f"{status} '{normal_order}' vs '{reversed_order}'")
        print(f"   → Intent1: {result1['intent']} ({result1['confidence']:.2%})")
        print(f"   → Intent2: {result2['intent']} ({result2['confidence']:.2%})")
        print()
    
    print("=" * 80)


def test_singular_plural():
    """Test singular/plural handling."""
    
    print("\n" + "=" * 80)
    print("📝 SINGULAR/PLURAL NORMALIZATION TEST")
    print("=" * 80)
    print()
    
    singular_plural_tests = [
        ("list files", "list file", "list_files"),
        ("show processes", "show process", "show_running_processes"),
        ("open settings", "open setting", "open_settings"),
    ]
    
    print("Testing singular vs plural forms:")
    print("-" * 80)
    
    for plural_form, singular_form, expected_intent in singular_plural_tests:
        result1 = nlp_parser.parse_intent(plural_form)
        result2 = nlp_parser.parse_intent(singular_form)
        
        match1 = result1["intent"] == expected_intent
        match2 = result2["intent"] == expected_intent
        
        status = "✅" if (match1 and match2) else "⚠️"
        
        print(f"{status} '{plural_form}' vs '{singular_form}'")
        print(f"   → Plural:   {result1['intent']} ({result1['confidence']:.2%})")
        print(f"   → Singular: {result2['intent']} ({result2['confidence']:.2%})")
        print()
    
    print("=" * 80)


if __name__ == "__main__":
    print()
    print("🚀 Starting NLP Intent Recognition Tests...")
    print()
    
    # Run all tests
    test_variations()
    test_specific_requirement()
    demo_fuzzy_matching()
    test_word_order()
    test_singular_plural()
    
    print("\n✅ All tests completed!")
    print()
