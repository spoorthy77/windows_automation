"""
Offline LLM Client for Local Code Generation

This module handles communication with a locally hosted LLM (Ollama)
to generate programs completely offline without internet connectivity.
"""

import json
import subprocess
import requests
from typing import Dict, Optional, Tuple
from logger import log_event


class OfflineLLMClient:
    """
    Client for interacting with locally hosted Ollama LLM.
    """
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "codellama"):
        """
        Initialize the offline LLM client.
        
        Args:
            base_url: Base URL for Ollama API (default: localhost:11434)
            model: Model name to use (default: codellama for code generation)
        """
        self.base_url = base_url
        self.model = model
        self.api_url = f"{base_url}/api/generate"
        self.available_models = ["codellama", "llama2", "mistral", "deepseek-coder"]
        
    def check_ollama_running(self) -> bool:
        """
        Check if Ollama service is running locally.
        
        Returns:
            True if Ollama is accessible, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def list_available_models(self) -> list:
        """
        Get list of models available in local Ollama installation.
        
        Returns:
            List of model names
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=3)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except requests.exceptions.RequestException:
            return []
    
    def generate_code(self, prompt: str, language: str = "python", max_retries: int = 3) -> Tuple[Optional[str], str]:
        """
        Generate code using the offline LLM.
        
        Args:
            prompt: Natural language description of the program to generate
            language: Target programming language
            max_retries: Maximum number of generation attempts
            
        Returns:
            Tuple of (generated_code, status_message)
        """
        # Check if Ollama is running
        if not self.check_ollama_running():
            return None, "❌ Error: Ollama is not running. Please start Ollama service."
        
        # Build a code-focused prompt
        system_prompt = self._build_system_prompt(language)
        full_prompt = f"{system_prompt}\n\n{prompt}\n\nProvide ONLY the complete, runnable code without explanations:"
        
        log_event(f"Generating {language} code with offline LLM: {prompt[:50]}...")
        
        for attempt in range(max_retries):
            try:
                # Make request to Ollama API
                payload = {
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2,  # Lower temperature for more deterministic code
                        "top_p": 0.9,
                        "top_k": 40
                    }
                }
                
                response = requests.post(
                    self.api_url,
                    json=payload,
                    timeout=120  # 2 minutes timeout for code generation
                )
                
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result.get('response', '').strip()
                    
                    # Extract code from response
                    code = self._extract_code(generated_text, language)
                    
                    if code:
                        log_event(f"✅ Code generated successfully on attempt {attempt + 1}")
                        return code, "✅ Code generated successfully"
                    else:
                        log_event(f"⚠️ No valid code extracted on attempt {attempt + 1}")
                        
                else:
                    log_event(f"❌ API error: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                log_event(f"⏱️ Request timeout on attempt {attempt + 1}")
            except Exception as e:
                log_event(f"❌ Generation error: {str(e)}")
        
        return None, "❌ Failed to generate code after multiple attempts"
    
    def fix_code(self, code: str, error_message: str, language: str) -> Tuple[Optional[str], str]:
        """
        Fix code based on compilation/syntax errors.
        
        Args:
            code: Original code with errors
            error_message: Compilation/syntax error message
            language: Programming language
            
        Returns:
            Tuple of (fixed_code, status_message)
        """
        if not self.check_ollama_running():
            return None, "❌ Ollama is not running"
        
        fix_prompt = f"""The following {language} code has errors:

```{language}
{code}
```

Error message:
{error_message}

Please provide the CORRECTED code that fixes these errors. Return ONLY the complete, corrected code without explanations:"""
        
        log_event(f"Attempting to fix {language} code...")
        
        try:
            payload = {
                "model": self.model,
                "prompt": fix_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Very low temperature for precise fixes
                    "top_p": 0.9
                }
            }
            
            response = requests.post(self.api_url, json=payload, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get('response', '').strip()
                fixed_code = self._extract_code(generated_text, language)
                
                if fixed_code:
                    log_event("✅ Code fixed successfully")
                    return fixed_code, "✅ Code fixed"
                    
        except Exception as e:
            log_event(f"❌ Fix error: {str(e)}")
        
        return None, "❌ Failed to fix code"
    
    def _build_system_prompt(self, language: str) -> str:
        """Build language-specific system prompt."""
        prompts = {
            "python": "You are an expert Python programmer. Generate clean, runnable Python code.",
            "java": "You are an expert Java programmer. Generate complete, compilable Java code with proper class structure.",
            "c": "You are an expert C programmer. Generate complete, compilable C code with necessary includes.",
            "cpp": "You are an expert C++ programmer. Generate complete, compilable C++ code with necessary includes.",
            "c++": "You are an expert C++ programmer. Generate complete, compilable C++ code with necessary includes."
        }
        return prompts.get(language.lower(), f"You are an expert {language} programmer.")
    
    def _extract_code(self, text: str, language: str) -> Optional[str]:
        """
        Extract code from LLM response.
        Handles markdown code blocks and plain text.
        """
        # Try to find code blocks first
        import re
        
        # Pattern for markdown code blocks with language specifier
        pattern = rf"```(?:{language}|{language.lower()}|{language.upper()})\s*\n(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # Pattern for generic code blocks
        pattern = r"```\s*\n(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # If no code blocks, check if the entire response looks like code
        lines = text.strip().split('\n')
        
        # Heuristics: if most lines look like code, return the whole thing
        code_indicators = {
            'python': ['def ', 'class ', 'import ', 'from ', 'if ', 'for ', 'while ', 'print('],
            'java': ['public class', 'public static', 'private ', 'void ', 'System.out'],
            'c': ['#include', 'int main', 'printf(', 'scanf(', 'void '],
            'cpp': ['#include', 'int main', 'std::', 'cout', 'cin', 'namespace'],
            'c++': ['#include', 'int main', 'std::', 'cout', 'cin', 'namespace']
        }
        
        indicators = code_indicators.get(language.lower(), [])
        code_line_count = sum(1 for line in lines if any(ind in line for ind in indicators))
        
        if code_line_count > len(lines) * 0.3:  # If 30%+ lines look like code
            return text.strip()
        
        return None
    
    def start_ollama_service(self) -> bool:
        """
        Attempt to start Ollama service (Windows).
        
        Returns:
            True if started successfully, False otherwise
        """
        try:
            # Try to start Ollama in background
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            import time
            time.sleep(3)  # Wait for service to start
            return self.check_ollama_running()
        except Exception as e:
            log_event(f"❌ Could not start Ollama: {str(e)}")
            return False
    
    def pull_model(self, model_name: str) -> bool:
        """
        Download/pull a model to local Ollama.
        
        Args:
            model_name: Name of model to pull (e.g., 'codellama')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            log_event(f"📥 Downloading model: {model_name}...")
            result = subprocess.run(
                ["ollama", "pull", model_name],
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes timeout
            )
            success = result.returncode == 0
            if success:
                log_event(f"✅ Model {model_name} downloaded successfully")
            return success
        except Exception as e:
            log_event(f"❌ Failed to download model: {str(e)}")
            return False


# Global instance
offline_llm = OfflineLLMClient()


if __name__ == "__main__":
    # Test the offline LLM client
    print("🧪 Testing Offline LLM Client...")
    print("=" * 60)
    
    client = OfflineLLMClient()
    
    # Check if Ollama is running
    print(f"Checking Ollama status...")
    if client.check_ollama_running():
        print("✅ Ollama is running")
        
        # List available models
        models = client.list_available_models()
        print(f"Available models: {models}")
        
        # Test code generation
        print("\n📝 Generating sample Python code...")
        code, msg = client.generate_code(
            "Write a Python function to calculate factorial of a number",
            language="python"
        )
        
        if code:
            print(f"\n{msg}")
            print(f"\nGenerated code:\n{'-'*40}")
            print(code)
            print('-'*40)
        else:
            print(f"❌ {msg}")
    else:
        print("❌ Ollama is not running")
        print("Please start Ollama by running: ollama serve")
    
    print("\n" + "=" * 60)
