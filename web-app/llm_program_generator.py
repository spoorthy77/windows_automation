"""
Enhanced Offline Program Generator with LLM Integration
Generates error-free programs dynamically using local LLM
Supports: Python, Java, C, C++
Features: Auto-validation, error correction, multi-language support
"""

from typing import Dict, Optional
import os
import re
from datetime import datetime

# Import our modules
from offline_llm_integration import OfflineLLM, get_default_llm
from code_validator import CodeValidator


class LLMProgramGenerator:
    """
    Enhanced program generator using offline LLM
    Generates complete, validated, error-free programs
    """
    
    def __init__(self, llm: Optional[OfflineLLM] = None):
        """
        Initialize LLM Program Generator
        
        Args:
            llm: OfflineLLM instance (creates default if None)
        """
        self.llm = llm or get_default_llm()
        self.validator = CodeValidator()
        
        # Language detection patterns
        self.language_patterns = {
            'python': ['python', 'py', '.py'],
            'java': ['java', '.java'],
            'c': ['c program', ' c ', '.c', 'language c'],
            'cpp': ['c++', 'cpp', 'c plus plus', '.cpp']
        }
        
        # File extensions
        self.extensions = {
            'python': '.py',
            'java': '.java',
            'c': '.c',
            'cpp': '.cpp'
        }
    
    def detect_language(self, user_input: str) -> str:
        """
        Detect programming language from user input
        
        Args:
            user_input: User's program request
            
        Returns:
            Language name (python, java, c, cpp)
        """
        text = user_input.lower()
        
        # Check for explicit language mentions
        for lang, patterns in self.language_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    # Special handling for C vs C++
                    if lang == 'c' and ('c++' in text or 'cpp' in text):
                        continue
                    return lang
        
        # Default to Python
        return 'python'
    
    def extract_filename(self, code: str, language: str) -> str:
        """
        Extract appropriate filename from code
        
        Args:
            code: Generated code
            language: Programming language
            
        Returns:
            Filename with extension
        """
        if language == 'java':
            # Extract class name for Java
            match = re.search(r'public\s+class\s+(\w+)', code)
            if match:
                return f"{match.group(1)}.java"
            return "Program.java"
        
        elif language == 'python':
            # Look for meaningful function/class names
            match = re.search(r'def\s+(\w+)', code)
            if match and match.group(1) != '__main__':
                return f"{match.group(1)}.py"
            match = re.search(r'class\s+(\w+)', code)
            if match:
                return f"{match.group(1)}.py"
            return "program.py"
        
        elif language == 'c':
            return "program.c"
        
        elif language == 'cpp':
            return "program.cpp"
        
        return f"program{self.extensions.get(language, '.txt')}"
    
    def save_code(self, code: str, language: str, output_dir: Optional[str] = None) -> str:
        """
        Save generated code to file
        
        Args:
            code: Source code
            language: Programming language
            output_dir: Output directory (default: Desktop)
            
        Returns:
            Full path to saved file
        """
        # Default to Desktop
        if not output_dir:
            output_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
        
        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Get filename
        filename = self.extract_filename(code, language)
        
        # Create unique filename if file exists
        base_path = os.path.join(output_dir, filename)
        if os.path.exists(base_path):
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}{ext}"
        
        # Save file
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        
        return filepath
    
    def generate_program(self, user_request: str, language: Optional[str] = None,
                        output_dir: Optional[str] = None, 
                        validate: bool = True) -> Dict:
        """
        Generate complete program from user request
        
        Args:
            user_request: User's program request/description
            language: Target language (auto-detected if None)
            output_dir: Output directory (default: Desktop)
            validate: Whether to validate and auto-fix errors
            
        Returns:
            Dict with generation results
        """
        # Detect language if not specified
        if not language:
            language = self.detect_language(user_request)
        
        language = language.lower()
        
        # Check if LLM is available
        if not self.llm.is_available():
            return {
                'success': False,
                'message': '❌ Ollama service is not running. Please start Ollama first.\n\n'
                          'Setup instructions:\n'
                          '1. Download Ollama from: https://ollama.ai\n'
                          '2. Install and start Ollama\n'
                          '3. Run: ollama pull codellama:7b\n'
                          '4. Try again',
                'code': None,
                'filepath': None,
                'language': language
            }
        
        # Generate code using LLM
        print(f"🤖 Generating {language} code using {self.llm.model}...")
        llm_result = self.llm.generate_code(user_request, language)
        
        if not llm_result['success']:
            return {
                'success': False,
                'message': llm_result['message'],
                'code': None,
                'filepath': None,
                'language': language
            }
        
        code = llm_result['code']
        
        # Validate and fix if requested
        if validate:
            print(f"🔍 Validating {language} code...")
            validation_result = self.validator.validate_and_fix(
                code, language, user_request, self.llm
            )
            
            if validation_result['success']:
                code = validation_result['code']
                validation_msg = validation_result['message']
                attempts = validation_result['attempts']
            else:
                # Return even if validation failed
                code = validation_result['code']
                validation_msg = validation_result['message']
                attempts = validation_result['attempts']
                
                # Still save the code but warn user
                filepath = self.save_code(code, language, output_dir)
                
                return {
                    'success': False,
                    'message': f"{validation_msg}\n\n⚠️ Code saved but may contain errors.\n"
                              f"📁 Location: {filepath}\n\n"
                              f"You may need to fix manually.",
                    'code': code,
                    'filepath': filepath,
                    'language': language,
                    'validated': False,
                    'attempts': attempts
                }
        else:
            validation_msg = "⚠️ Validation skipped"
            attempts = 1
        
        # Save code to file
        filepath = self.save_code(code, language, output_dir)
        
        # Get compiler status
        compiler_status = self.validator.get_compiler_status()
        
        # Build success message
        message = self._build_success_message(
            language, filepath, validation_msg, attempts, compiler_status
        )
        
        return {
            'success': True,
            'message': message,
            'code': code,
            'filepath': filepath,
            'language': language,
            'validated': True,
            'attempts': attempts,
            'model': llm_result['model']
        }
    
    def _build_success_message(self, language: str, filepath: str, 
                              validation_msg: str, attempts: int,
                              compiler_status: Dict[str, bool]) -> str:
        """Build formatted success message"""
        
        # Execution instructions
        exec_instructions = {
            'python': f'python "{filepath}"',
            'java': f'javac "{filepath}" && java {os.path.splitext(os.path.basename(filepath))[0]}',
            'c': f'gcc "{filepath}" -o program.exe && program.exe',
            'cpp': f'g++ "{filepath}" -o program.exe && program.exe'
        }
        
        message = f"""✅ Program Generated Successfully!

📋 Details:
   • Language: {language.upper()}
   • Model: {self.llm.model}
   • Validation: {validation_msg}
   • Attempts: {attempts}
   
📁 File Saved:
   {filepath}

🚀 To Run:
   {exec_instructions.get(language, 'See file for instructions')}

💻 Compiler Status:
   • Python: ✅ Available
   • Java (javac): {'✅ Available' if compiler_status.get('javac') else '❌ Not installed'}
   • C (gcc): {'✅ Available' if compiler_status.get('gcc') else '❌ Not installed'}
   • C++ (g++): {'✅ Available' if compiler_status.get('g++') else '❌ Not installed'}

📄 Generated Code:
{"="*60}
"""
        return message


# Convenience function for quick generation
def generate_program_quick(request: str, language: Optional[str] = None) -> Dict:
    """
    Quick program generation function
    
    Args:
        request: User's program request
        language: Target language (auto-detected if None)
        
    Returns:
        Generation result dictionary
    """
    generator = LLMProgramGenerator()
    return generator.generate_program(request, language)


# Test function
if __name__ == '__main__':
    print("🔍 Testing LLM Program Generator...")
    
    generator = LLMProgramGenerator()
    
    print(f"LLM Available: {generator.llm.is_available()}")
    print(f"Available Models: {generator.llm.list_models()}")
    print(f"Selected Model: {generator.llm.model}")
    print(f"Compilers: {generator.validator.get_compiler_status()}")
    
    if generator.llm.is_available():
        print("\n📝 Testing program generation...")
        
        # Test with a simple request
        result = generator.generate_program(
            "Write a Python program to calculate factorial of a number using recursion",
            language="python"
        )
        
        if result['success']:
            print(f"\n{result['message']}")
            print(result['code'])
            print(f"\n✅ Test successful! File saved at: {result['filepath']}")
        else:
            print(f"\n❌ {result['message']}")
    else:
        print("\n⚠️ Ollama not available. Please install and start Ollama to test.")
        print("\nSetup instructions:")
        print("1. Download from: https://ollama.ai")
        print("2. Install Ollama")
        print("3. Run: ollama pull codellama:7b")
        print("4. Run this script again")
