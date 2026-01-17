"""
Offline Program Generator with Auto-Correction Pipeline

This module generates programs using local LLM and automatically validates
and corrects errors to ensure the final code is runnable and error-free.
"""

import os
import re
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime

from offline_llm_client import OfflineLLMClient
from code_validator import CodeValidator
from logger import log_event


class ProgramGenerator:
    """
    Generates programs with automatic validation and error correction.
    """
    
    def __init__(self, save_dir: Optional[str] = None):
        """
        Initialize program generator.
        
        Args:
            save_dir: Directory to save generated programs (default: Desktop)
        """
        self.llm_client = OfflineLLMClient()
        self.validator = CodeValidator()
        
        # Set default save directory to Desktop
        if save_dir is None:
            desktop = Path.home() / "Desktop"
            self.save_dir = desktop / "GeneratedPrograms"
        else:
            self.save_dir = Path(save_dir)
        
        # Create save directory if it doesn't exist
        self.save_dir.mkdir(parents=True, exist_ok=True)
        log_event(f"📁 Program save directory: {self.save_dir}")
        
        # Language file extensions
        self.extensions = {
            'python': '.py',
            'py': '.py',
            'java': '.java',
            'c': '.c',
            'cpp': '.cpp',
            'c++': '.cpp'
        }
        
        # Maximum retry attempts for error correction
        self.max_retries = 3
    
    def detect_language(self, user_request: str) -> str:
        """
        Detect programming language from user request.
        
        Args:
            user_request: User's natural language request
            
        Returns:
            Detected language (default: python)
        """
        request_lower = user_request.lower()
        
        # Check for explicit language mentions
        if any(word in request_lower for word in ['java program', 'in java', 'using java']):
            return 'java'
        elif any(word in request_lower for word in ['c++ program', 'cpp program', 'in c++', 'using c++']):
            return 'cpp'
        elif any(word in request_lower for word in ['c program', 'in c', 'using c']) and 'c++' not in request_lower:
            return 'c'
        elif any(word in request_lower for word in ['python program', 'in python', 'using python', 'py program']):
            return 'python'
        
        # Default to Python
        return 'python'
    
    def extract_program_name(self, user_request: str, language: str) -> str:
        """
        Extract or generate program name from request.
        
        Args:
            user_request: User's request
            language: Programming language
            
        Returns:
            Program filename
        """
        # Try to extract name from patterns like "called X" or "named X"
        patterns = [
            r'called\s+["\']?(\w+)["\']?',
            r'named\s+["\']?(\w+)["\']?',
            r'name\s+it\s+["\']?(\w+)["\']?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_request, re.IGNORECASE)
            if match:
                name = match.group(1)
                return f"{name}{self.extensions[language]}"
        
        # Generate default name based on content
        if 'factorial' in user_request.lower():
            base_name = 'factorial'
        elif 'fibonacci' in user_request.lower():
            base_name = 'fibonacci'
        elif 'prime' in user_request.lower():
            base_name = 'prime'
        elif 'sort' in user_request.lower():
            base_name = 'sort'
        elif 'search' in user_request.lower():
            base_name = 'search'
        elif 'calculator' in user_request.lower():
            base_name = 'calculator'
        elif 'palindrome' in user_request.lower():
            base_name = 'palindrome'
        elif 'pattern' in user_request.lower():
            base_name = 'pattern'
        else:
            base_name = 'program'
        
        # Add timestamp to make unique
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{base_name}_{timestamp}{self.extensions[language]}"
    
    def generate_program(self, user_request: str, language: Optional[str] = None,
                        output_dir: Optional[str] = None) -> Dict:
        """
        Generate a complete, validated program from user request.
        
        This is the main function that orchestrates:
        1. Language detection
        2. Code generation via LLM
        3. Validation
        4. Auto-correction if errors found
        5. Saving to file
        
        Args:
            user_request: Natural language description of program
            language: Programming language (auto-detected if None)
            output_dir: Custom output directory (uses default if None)
            
        Returns:
            Dictionary with status, code, filename, and messages
        """
        log_event(f"🚀 Starting program generation: {user_request[:50]}...")
        
        # Step 1: Check if Ollama is running
        if not self.llm_client.check_ollama_running():
            return {
                'success': False,
                'error': 'Ollama is not running',
                'message': '❌ Ollama LLM service is not running.\n\nPlease start it with: ollama serve',
                'code': None,
                'filename': None,
                'filepath': None
            }
        
        # Step 2: Detect language
        if language is None:
            language = self.detect_language(user_request)
        language = language.lower()
        
        log_event(f"🔍 Detected language: {language}")
        
        # Step 3: Generate initial code
        code, gen_message = self.llm_client.generate_code(user_request, language)
        
        if code is None:
            return {
                'success': False,
                'error': 'Code generation failed',
                'message': f'❌ {gen_message}',
                'code': None,
                'filename': None,
                'filepath': None
            }
        
        log_event(f"✅ Initial code generated ({len(code)} chars)")
        
        # Step 4: Validate and auto-correct
        attempts = 0
        is_valid = False
        validation_msg = ""
        
        while attempts < self.max_retries and not is_valid:
            attempts += 1
            log_event(f"🔍 Validation attempt {attempts}/{self.max_retries}")
            
            is_valid, validation_msg = self.validator.validate(code, language)
            
            if is_valid:
                log_event("✅ Code is valid!")
                break
            else:
                log_event(f"❌ Validation failed: {validation_msg[:50]}...")
                
                # If not the last attempt, try to fix
                if attempts < self.max_retries:
                    log_event("🔧 Attempting auto-correction...")
                    fixed_code, fix_msg = self.llm_client.fix_code(code, validation_msg, language)
                    
                    if fixed_code:
                        code = fixed_code
                        log_event("✅ Code corrected, re-validating...")
                    else:
                        log_event(f"❌ Auto-correction failed: {fix_msg}")
                        break
        
        # Step 5: Save the program
        filename = self.extract_program_name(user_request, language)
        
        if output_dir:
            save_path = Path(output_dir) / filename
        else:
            save_path = self.save_dir / filename
        
        # Ensure directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(code)
            log_event(f"💾 Program saved: {save_path}")
        except Exception as e:
            return {
                'success': False,
                'error': f'File save error: {str(e)}',
                'message': f'❌ Could not save file: {str(e)}',
                'code': code,
                'filename': filename,
                'filepath': None
            }
        
        # Step 6: Prepare result
        if is_valid:
            message = f"""✅ Program generated successfully!

📝 Language: {language.upper()}
📄 Filename: {filename}
📁 Location: {save_path}
✅ Validation: Passed (Error-free code)
🔄 Attempts: {attempts}/{self.max_retries}

You can now run the program from: {save_path}
"""
        else:
            message = f"""⚠️ Program generated with warnings

📝 Language: {language.upper()}
📄 Filename: {filename}
📁 Location: {save_path}
⚠️ Validation: Failed after {attempts} attempts

Warning: {validation_msg}

Code has been saved but may contain errors. Please review manually.
"""
        
        return {
            'success': is_valid,
            'warning': not is_valid,
            'code': code,
            'filename': filename,
            'filepath': str(save_path),
            'language': language,
            'attempts': attempts,
            'message': message,
            'validation_message': validation_msg
        }
    
    def set_save_directory(self, directory: str):
        """
        Change the default save directory for generated programs.
        
        Args:
            directory: New directory path
        """
        self.save_dir = Path(directory)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        log_event(f"📁 Save directory updated: {self.save_dir}")
    
    def get_compiler_status(self) -> Dict[str, str]:
        """
        Get status of available compilers.
        
        Returns:
            Dictionary with compiler availability
        """
        return self.validator.get_compiler_info()
    
    def cleanup(self):
        """Clean up temporary files."""
        self.validator.cleanup()


# Global instance
program_generator = ProgramGenerator()


def generate_program_command(user_request: str, language: Optional[str] = None,
                             output_dir: Optional[str] = None) -> str:
    """
    Command-line interface for program generation.
    
    Args:
        user_request: User's program request
        language: Programming language (auto-detected if None)
        output_dir: Output directory (default: Desktop/GeneratedPrograms)
        
    Returns:
        Result message
    """
    result = program_generator.generate_program(user_request, language, output_dir)
    return result['message']


if __name__ == "__main__":
    # Test the program generator
    print("🧪 Testing Program Generator...")
    print("=" * 60)
    
    generator = ProgramGenerator()
    
    # Show compiler status
    print("\n📊 Compiler Status:")
    for lang, status in generator.get_compiler_status().items():
        print(f"  {lang}: {status}")
    
    # Test program generation
    print("\n🔧 Generating test program...")
    result = generator.generate_program(
        "Write a Python program to calculate factorial of a number using recursion"
    )
    
    print(f"\n{result['message']}")
    
    if result['success']:
        print(f"\n📄 Generated Code Preview:")
        print("-" * 60)
        print(result['code'][:500] + "..." if len(result['code']) > 500 else result['code'])
        print("-" * 60)
    
    print("\n" + "=" * 60)
    print("✅ Program generator test complete!")
