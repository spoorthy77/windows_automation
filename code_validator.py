"""
Code Validator and Compiler Module

This module validates and compiles generated code to ensure it's error-free.
Supports Python, Java, C, and C++ with automatic error detection.
"""

import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Tuple, Optional, Dict
from logger import log_event


class CodeValidator:
    """
    Validates and compiles code for multiple programming languages.
    """
    
    def __init__(self):
        """Initialize code validator with compiler paths."""
        self.temp_dir = tempfile.mkdtemp(prefix="code_validation_")
        self.compilers = self._detect_compilers()
        
    def _detect_compilers(self) -> Dict[str, Optional[str]]:
        """
        Detect available compilers on the system.
        
        Returns:
            Dictionary mapping language to compiler path
        """
        compilers = {
            'python': self._find_executable('python') or self._find_executable('python3'),
            'java': self._find_executable('javac'),
            'c': self._find_executable('gcc'),
            'cpp': self._find_executable('g++'),
            'c++': self._find_executable('g++')
        }
        
        log_event(f"Detected compilers: {compilers}")
        return compilers
    
    def _find_executable(self, name: str) -> Optional[str]:
        """Find executable in PATH."""
        return shutil.which(name)
    
    def validate_python(self, code: str, filename: str = "program.py") -> Tuple[bool, str]:
        """
        Validate Python code for syntax errors.
        
        Args:
            code: Python source code
            filename: Name for the temporary file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.compilers['python']:
            return False, "❌ Python interpreter not found"
        
        # Write code to temporary file
        temp_file = os.path.join(self.temp_dir, filename)
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Use py_compile to check syntax
            result = subprocess.run(
                [self.compilers['python'], '-m', 'py_compile', temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                log_event(f"✅ Python validation successful: {filename}")
                return True, "✅ Python code is syntactically correct"
            else:
                error_msg = result.stderr.strip() or result.stdout.strip()
                log_event(f"❌ Python validation failed: {error_msg[:100]}")
                return False, f"❌ Syntax error:\n{error_msg}"
                
        except subprocess.TimeoutExpired:
            return False, "❌ Validation timeout"
        except Exception as e:
            return False, f"❌ Validation error: {str(e)}"
    
    def validate_java(self, code: str, filename: str = "Program.java") -> Tuple[bool, str]:
        """
        Validate and compile Java code.
        
        Args:
            code: Java source code
            filename: Name for the Java file (must match class name)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.compilers['java']:
            return False, "❌ Java compiler (javac) not found. Please install JDK."
        
        # Extract class name from code
        import re
        class_match = re.search(r'public\s+class\s+(\w+)', code)
        if class_match:
            class_name = class_match.group(1)
            filename = f"{class_name}.java"
        
        temp_file = os.path.join(self.temp_dir, filename)
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Compile Java code
            result = subprocess.run(
                [self.compilers['java'], temp_file],
                capture_output=True,
                text=True,
                cwd=self.temp_dir,
                timeout=30
            )
            
            if result.returncode == 0:
                log_event(f"✅ Java compilation successful: {filename}")
                return True, "✅ Java code compiled successfully"
            else:
                error_msg = result.stderr.strip() or result.stdout.strip()
                log_event(f"❌ Java compilation failed: {error_msg[:100]}")
                return False, f"❌ Compilation error:\n{error_msg}"
                
        except subprocess.TimeoutExpired:
            return False, "❌ Compilation timeout"
        except Exception as e:
            return False, f"❌ Compilation error: {str(e)}"
    
    def validate_c(self, code: str, filename: str = "program.c") -> Tuple[bool, str]:
        """
        Validate and compile C code.
        
        Args:
            code: C source code
            filename: Name for the C file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.compilers['c']:
            return False, "❌ GCC compiler not found. Please install MinGW or GCC."
        
        temp_file = os.path.join(self.temp_dir, filename)
        output_file = os.path.join(self.temp_dir, "program.exe")
        
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Compile C code
            result = subprocess.run(
                [self.compilers['c'], temp_file, '-o', output_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                log_event(f"✅ C compilation successful: {filename}")
                return True, "✅ C code compiled successfully"
            else:
                error_msg = result.stderr.strip() or result.stdout.strip()
                log_event(f"❌ C compilation failed: {error_msg[:100]}")
                return False, f"❌ Compilation error:\n{error_msg}"
                
        except subprocess.TimeoutExpired:
            return False, "❌ Compilation timeout"
        except Exception as e:
            return False, f"❌ Compilation error: {str(e)}"
    
    def validate_cpp(self, code: str, filename: str = "program.cpp") -> Tuple[bool, str]:
        """
        Validate and compile C++ code.
        
        Args:
            code: C++ source code
            filename: Name for the C++ file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.compilers['cpp']:
            return False, "❌ G++ compiler not found. Please install MinGW or GCC."
        
        temp_file = os.path.join(self.temp_dir, filename)
        output_file = os.path.join(self.temp_dir, "program.exe")
        
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Compile C++ code
            result = subprocess.run(
                [self.compilers['cpp'], temp_file, '-o', output_file, '-std=c++11'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                log_event(f"✅ C++ compilation successful: {filename}")
                return True, "✅ C++ code compiled successfully"
            else:
                error_msg = result.stderr.strip() or result.stdout.strip()
                log_event(f"❌ C++ compilation failed: {error_msg[:100]}")
                return False, f"❌ Compilation error:\n{error_msg}"
                
        except subprocess.TimeoutExpired:
            return False, "❌ Compilation timeout"
        except Exception as e:
            return False, f"❌ Compilation error: {str(e)}"
    
    def validate(self, code: str, language: str, filename: Optional[str] = None) -> Tuple[bool, str]:
        """
        Validate code for the specified language.
        
        Args:
            code: Source code
            language: Programming language (python, java, c, cpp)
            filename: Optional custom filename
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        language = language.lower()
        
        validators = {
            'python': self.validate_python,
            'py': self.validate_python,
            'java': self.validate_java,
            'c': self.validate_c,
            'cpp': self.validate_cpp,
            'c++': self.validate_cpp
        }
        
        validator = validators.get(language)
        if not validator:
            return False, f"❌ Unsupported language: {language}"
        
        # Use custom filename if provided
        if filename:
            return validator(code, filename)
        else:
            return validator(code)
    
    def get_compiler_info(self) -> Dict[str, str]:
        """
        Get information about available compilers.
        
        Returns:
            Dictionary with compiler availability status
        """
        info = {}
        for lang, compiler_path in self.compilers.items():
            if compiler_path:
                info[lang] = f"✅ Available ({compiler_path})"
            else:
                info[lang] = "❌ Not found"
        return info
    
    def cleanup(self):
        """Clean up temporary files."""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                log_event(f"🧹 Cleaned up temp directory: {self.temp_dir}")
        except Exception as e:
            log_event(f"⚠️ Cleanup warning: {str(e)}")
    
    def __del__(self):
        """Cleanup on deletion."""
        self.cleanup()


# Global instance
code_validator = CodeValidator()


if __name__ == "__main__":
    # Test the code validator
    print("🧪 Testing Code Validator...")
    print("=" * 60)
    
    validator = CodeValidator()
    
    # Show compiler info
    print("\n📊 Compiler Availability:")
    for lang, status in validator.get_compiler_info().items():
        print(f"  {lang}: {status}")
    
    # Test Python validation
    print("\n📝 Testing Python validation...")
    python_code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))
"""
    is_valid, msg = validator.validate_python(python_code)
    print(f"Result: {msg}")
    
    # Test with syntax error
    print("\n📝 Testing Python with error...")
    bad_python = """
def test(:
    print("missing closing paren"
"""
    is_valid, msg = validator.validate_python(bad_python)
    print(f"Result: {msg}")
    
    # Test Java validation (if available)
    if validator.compilers['java']:
        print("\n📝 Testing Java validation...")
        java_code = """
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
"""
        is_valid, msg = validator.validate_java(java_code)
        print(f"Result: {msg}")
    
    # Test C validation (if available)
    if validator.compilers['c']:
        print("\n📝 Testing C validation...")
        c_code = """
#include <stdio.h>

int main() {
    printf("Hello, World!\\n");
    return 0;
}
"""
        is_valid, msg = validator.validate_c(c_code)
        print(f"Result: {msg}")
    
    print("\n" + "=" * 60)
    print("✅ Validation tests complete!")
