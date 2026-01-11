"""
Script to remove hardcoded API keys from documentation files
"""

import os
import re

# The API key patterns to remove (using regex patterns, not actual keys)
API_KEY_PATTERNS = [
    r'xai-[a-zA-Z0-9]{70,}',  # Match xAI API key pattern
    r'xai-tCak[^\s]+',  # Specific pattern without showing full key
    r'xai-Eyvp[^\s]+',  # Another pattern
]

# Files to clean
FILES_TO_CLEAN = [
    'FROK_INTEGRATION_COMPLETE.txt',
    'QUICK_FIX.txt',
    'web-app/FROK_INTEGRATION.txt'
]

# Replacement text
REPLACEMENT = 'xai-****************************** (See .env file)'

def clean_file(filepath):
    """Remove API key from a file and replace with placeholder"""
    try:
        if not os.path.exists(filepath):
            print(f"⚠️  File not found: {filepath}")
            return False
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check if any API key exists in file
        found = False
        for pattern in API_KEY_PATTERNS:
            if re.search(pattern, content):
                content = re.sub(pattern, REPLACEMENT, content)
                found = True
        
        if not found:
            print(f"✅ {filepath} - No API key found")
            return True
        
        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"🧹 {filepath} - API key removed and replaced with placeholder")
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning {filepath}: {str(e)}")
        return False

def main():
    print("\n" + "="*70)
    print("🔐 Cleaning API Keys from Documentation Files")
    print("="*70 + "\n")
    
    success_count = 0
    total_count = len(FILES_TO_CLEAN)
    
    for filepath in FILES_TO_CLEAN:
        if clean_file(filepath):
            success_count += 1
    
    print("\n" + "="*70)
    print(f"✅ Cleaned {success_count}/{total_count} files successfully")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()