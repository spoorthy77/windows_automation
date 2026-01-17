"""
Code Validator and Error Correction Pipeline
Validates generated code and auto-fixes errors using LLM feedback loop
Supports: Python, Java, C, C++
"""

import subprocess
import os
import tempfile
import shutil
from typing import Dict, Optional, Tuple
import ast
import re


class CodeValidator:
    """
    Validates and compiles code in multiple languages
    Provides error feedback for auto-correction
    """
    
    def __init__(self):
        self.max_fix_attempts = 3
        self.compilers = self._detect_compilers()
    
    def _detect_compilers(self) -> Dict[str, bool]:
        """Detect available compilers on the system"""
        compilers = {
            'python': True,  # Python is always available if we're running this
            'javac': self._check_command('javac -version'),
            'gcc': self._check_command('gcc --version'),
            'g++': self._check_command('g++ --version')
        }
        return compilers
    
    def _check_command(self, command: str) -> bool:
        """Check if a command is available"""
        try:
            subprocess.run(
                command.split(),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=2
            )
            return True
        except:
            return False
    
    def validate_python(self, code: str) -> Tuple[bool, Optional[str]]:
        """
        Validate Python code
        
        Returns:
            (is_valid, error_message)
        """
        try:
            # Check syntax using ast.parse
            ast.parse(code)
            
            # Try to compile
            compile(code, '<string>', 'exec')
            
            return True, None
        except SyntaxError as e:
            error_msg = f"Syntax Error at line {e.lineno}: {e.msg}"
            return False, error_msg
        except Exception as e:
            return False, f"Compilation Error: {str(e)}"
    
    def validate_java(self, code: str, class_name: str = None) -> Tuple[bool, Optional[str]]:
        """
        Validate Java code by compiling
        
        Returns:
            (is_valid, error_message)
        """
        if not self.compilers['javac']:
            return True, None  # Skip validation if javac not available
        
        # Extract class name if not provided
        if not class_name:
            match = re.search(r'public\s+class\s+(\w+)', code)
            if match:
                class_name = match.group(1)
            else:
                return False, "Could not find public class name in Java code"
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Write code to file
            file_path = os.path.join(temp_dir, f"{class_name}.java")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Try to compile
            result = subprocess.run(
                ['javac', file_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return True, None
            else:
                # Extract error message
                error_output = result.stderr
                return False, f"Java Compilation Error:\n{error_output}"
        
        except subprocess.TimeoutExpired:
            return False, "Compilation timeout"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
        finally:
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def validate_c(self, code: str) -> Tuple[bool, Optional[str]]:
        """
        Validate C code by compiling
        
        Returns:
            (is_valid, error_message)
        """
        if not self.compilers['gcc']:
            return True, None  # Skip validation if gcc not available
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Write code to file
            file_path = os.path.join(temp_dir, "temp.c")
            output_path = os.path.join(temp_dir, "temp.exe")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Try to compile
            result = subprocess.run(
                ['gcc', file_path, '-o', output_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return True, None
            else:
                # Extract error message
                error_output = result.stderr
                return False, f"C Compilation Error:\n{error_output}"
        
        except subprocess.TimeoutExpired:
            return False, "Compilation timeout"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
        finally:
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def validate_cpp(self, code: str) -> Tuple[bool, Optional[str]]:
        """
        Validate C++ code by compiling
        
        Returns:
            (is_valid, error_message)
        """
        if not self.compilers['g++']:
            return True, None  # Skip validation if g++ not available
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Write code to file
            file_path = os.path.join(temp_dir, "temp.cpp")
            output_path = os.path.join(temp_dir, "temp.exe")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Try to compile
            result = subprocess.run(
                ['g++', file_path, '-o', output_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return True, None
            else:
                # Extract error message
                error_output = result.stderr
                return False, f"C++ Compilation Error:\n{error_output}"
        
        except subprocess.TimeoutExpired:
            return False, "Compilation timeout"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
        finally:
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def validate(self, code: str, language: str) -> Tuple[bool, Optional[str]]:
        """
        Validate code for any supported language
        
        Args:
            code: Source code to validate
            language: Language (python, java, c, cpp)
            
        Returns:
            (is_valid, error_message)
        """
        language = language.lower()
        
        if language == 'python':
            return self.validate_python(code)
        elif language == 'java':
            return self.validate_java(code)
        elif language == 'c':
            return self.validate_c(code)
        elif language in ['cpp', 'c++']:
            return self.validate_cpp(code)
        else:
            return False, f"Unsupported language: {language}"
    
    def validate_and_fix(self, code: str, language: str, 
                        original_prompt: str, llm) -> Dict:
        """
        Validate code and auto-fix if errors found
        
        Args:
            code: Generated code
            language: Programming language
            original_prompt: Original user request
            llm: OfflineLLM instance for regeneration
            
        Returns:
            Dict with validation results and fixed code
        """
        # First validation
        is_valid, error = self.validate(code, language)
        
        if is_valid:
            return {
                'success': True,
                'code': code,
                'message': f'✅ Code validated successfully for {language}',
                'attempts': 1,
                'final_valid': True
            }
        
        # Try to fix errors
        current_code = code
        current_error = error
        
        for attempt in range(1, self.max_fix_attempts + 1):
            print(f"⚠️ Validation failed (Attempt {attempt}): {current_error}")
            print(f"🔄 Regenerating code with error feedback...")
            
            # Regenerate with error feedback
            fix_result = llm.regenerate_with_error(
                original_prompt,
                current_code,
                current_error,
                language
            )
            
            if not fix_result['success']:
                return {
                    'success': False,
                    'code': current_code,
                    'message': f"❌ Failed to regenerate code: {fix_result['message']}",
                    'attempts': attempt + 1,
                    'final_valid': False,
                    'last_error': current_error
                }
            
            current_code = fix_result['code']
            
            # Validate again
            is_valid, current_error = self.validate(current_code, language)
            
            if is_valid:
                return {
                    'success': True,
                    'code': current_code,
                    'message': f'✅ Code validated successfully after {attempt + 1} attempts',
                    'attempts': attempt + 1,
                    'final_valid': True
                }
        
        # Max attempts reached
        return {
            'success': False,
            'code': current_code,
            'message': f'❌ Failed to generate valid code after {self.max_fix_attempts} attempts',
            'attempts': self.max_fix_attempts + 1,
            'final_valid': False,
            'last_error': current_error
        }
    
    def get_compiler_status(self) -> Dict[str, bool]:
        """Get status of available compilers"""
        return self.compilers.copy()


# Test function
if __name__ == '__main__':
    validator = CodeValidator()
    
    print("🔍 Testing Code Validator...")
    print(f"Available Compilers: {validator.get_compiler_status()}")
    
    # Test Python validation
    print("\n📝 Testing Python validation...")
    valid_python = """
def hello():
    print("Hello, World!")

if __name__ == '__main__':
    hello()
"""
    is_valid, error = validator.validate_python(valid_python)
    print(f"Valid Python: {is_valid}, Error: {error}")
    
    invalid_python = """
def hello()  # Missing colon
    print("Hello")
"""
    is_valid, error = validator.validate_python(invalid_python)
    print(f"Invalid Python: {is_valid}, Error: {error}")
    
    # Test Java validation (if javac available)
    if validator.compilers['javac']:
        print("\n📝 Testing Java validation...")
        valid_java = """
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
"""
        is_valid, error = validator.validate_java(valid_java, "HelloWorld")
        print(f"Valid Java: {is_valid}, Error: {error}")
    else:
        print("\n⚠️ javac not available, skipping Java tests")
    
    print("\n✅ Validator tests complete!")
