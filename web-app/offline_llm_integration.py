"""
Offline LLM Integration Module
Integrates with locally hosted Ollama for code generation
100% Offline - No internet required
"""

import requests
import json
from typing import Optional, Dict, List
import time


class OfflineLLM:
    """
    Offline Large Language Model Integration
    Uses Ollama API running locally for code generation
    """
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "codellama:7b"):
        """
        Initialize Offline LLM client
        
        Args:
            base_url: Ollama API base URL (default: http://localhost:11434)
            model: Model name to use (default: codellama:7b)
                   Options: codellama:7b, codellama:13b, deepseek-coder, mistral, etc.
        """
        self.base_url = base_url
        self.model = model
        self.api_generate = f"{base_url}/api/generate"
        self.api_chat = f"{base_url}/api/chat"
        self.api_tags = f"{base_url}/api/tags"
        
    def is_available(self) -> bool:
        """Check if Ollama service is running and available"""
        try:
            response = requests.get(self.base_url, timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> List[str]:
        """List all available models in Ollama"""
        try:
            response = requests.get(self.api_tags, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except:
            return []
    
    def generate_code(self, prompt: str, language: str = "python", 
                     temperature: float = 0.2, max_retries: int = 3) -> Dict:
        """
        Generate code using the offline LLM
        
        Args:
            prompt: User's program request
            language: Target programming language
            temperature: Model temperature (lower = more deterministic)
            max_retries: Maximum retry attempts
            
        Returns:
            Dict with 'success', 'code', 'message', 'model'
        """
        # Check if Ollama is available
        if not self.is_available():
            return {
                'success': False,
                'code': None,
                'message': '❌ Ollama service is not running. Please start Ollama first.',
                'model': None
            }
        
        # Construct system prompt for code generation
        system_prompt = self._build_system_prompt(language)
        
        # Build the complete prompt
        full_prompt = f"{system_prompt}\n\n{prompt}\n\nGenerate only the complete, runnable {language} code without any explanations:"
        
        # Prepare request payload
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "temperature": temperature,
            "options": {
                "num_predict": 2048,  # Max tokens to generate
                "top_p": 0.9,
                "top_k": 40
            }
        }
        
        # Try to generate code with retries
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.api_generate,
                    json=payload,
                    timeout=60  # 60 second timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result.get('response', '').strip()
                    
                    # Extract code from response
                    code = self._extract_code(generated_text, language)
                    
                    if code:
                        return {
                            'success': True,
                            'code': code,
                            'message': f'✅ Code generated successfully using {self.model}',
                            'model': self.model
                        }
                    else:
                        # Retry if no valid code extracted
                        if attempt < max_retries - 1:
                            time.sleep(1)
                            continue
                        return {
                            'success': False,
                            'code': None,
                            'message': '❌ Failed to extract valid code from LLM response',
                            'model': self.model
                        }
                else:
                    error_msg = f"API returned status {response.status_code}"
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                    return {
                        'success': False,
                        'code': None,
                        'message': f'❌ {error_msg}',
                        'model': self.model
                    }
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return {
                    'success': False,
                    'code': None,
                    'message': '❌ Request timeout. Try with a smaller model or increase timeout.',
                    'model': self.model
                }
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return {
                    'success': False,
                    'code': None,
                    'message': f'❌ Error: {str(e)}',
                    'model': self.model
                }
        
        return {
            'success': False,
            'code': None,
            'message': '❌ Failed after maximum retries',
            'model': self.model
        }
    
    def _build_system_prompt(self, language: str) -> str:
        """Build system prompt based on language"""
        base_prompt = f"""You are an expert {language} programmer. Generate complete, runnable, error-free {language} code.

Requirements:
1. Write ONLY executable code - no explanations, comments, or markdown
2. Include all necessary imports/headers
3. Follow best practices and proper syntax
4. Include proper error handling
5. Make code production-ready and bug-free
6. For Python: use proper indentation
7. For Java: include complete class with main method
8. For C/C++: include all headers and main function"""
        
        return base_prompt
    
    def _extract_code(self, text: str, language: str) -> Optional[str]:
        """
        Extract clean code from LLM response
        Removes markdown code blocks and explanatory text
        """
        # Remove common markdown code block markers
        text = text.strip()
        
        # Remove markdown code blocks
        if '```' in text:
            parts = text.split('```')
            for i, part in enumerate(parts):
                # Skip even indices (text outside code blocks)
                if i % 2 == 0:
                    continue
                # Remove language identifier
                lines = part.strip().split('\n')
                if lines and lines[0].lower() in ['python', 'java', 'c', 'cpp', 'c++', language.lower()]:
                    lines = lines[1:]
                code = '\n'.join(lines).strip()
                if code:
                    return code
        
        # If no code blocks found, try to extract based on language patterns
        if language.lower() == 'python':
            # Look for Python patterns
            if 'def ' in text or 'import ' in text or 'if __name__' in text:
                return text
        elif language.lower() == 'java':
            # Look for Java patterns
            if 'public class' in text or 'class ' in text:
                return text
        elif language.lower() in ['c', 'cpp', 'c++']:
            # Look for C/C++ patterns
            if '#include' in text or 'int main' in text:
                return text
        
        # Return as-is if it looks like code
        if text and len(text) > 20:
            return text
        
        return None
    
    def regenerate_with_error(self, original_prompt: str, code: str, 
                             error_message: str, language: str) -> Dict:
        """
        Regenerate code with error feedback
        
        Args:
            original_prompt: Original user request
            code: Previously generated code that failed
            error_message: Compilation/validation error
            language: Programming language
            
        Returns:
            Dict with 'success', 'code', 'message'
        """
        fix_prompt = f"""The following {language} code has errors:

```{language}
{code}
```

Error message:
{error_message}

Fix the error and generate corrected, runnable {language} code. Output only the complete corrected code:"""
        
        return self.generate_code(fix_prompt, language, temperature=0.1)


def get_default_llm() -> OfflineLLM:
    """Get default LLM instance with best available model"""
    llm = OfflineLLM()
    
    # Try to find the best available model
    if llm.is_available():
        models = llm.list_models()
        # Prefer code-specialized models
        preferred_models = [
            'codellama:7b', 'codellama:13b', 'codellama',
            'deepseek-coder:6.7b', 'deepseek-coder',
            'mistral:7b', 'mistral',
            'llama2:7b', 'llama2'
        ]
        
        for preferred in preferred_models:
            for model in models:
                if preferred in model.lower():
                    llm.model = model
                    return llm
        
        # Use first available model if no preferred found
        if models:
            llm.model = models[0]
    
    return llm


# Test function
if __name__ == '__main__':
    llm = get_default_llm()
    
    print("🔍 Testing Offline LLM Integration...")
    print(f"Ollama Available: {llm.is_available()}")
    
    if llm.is_available():
        print(f"Available Models: {llm.list_models()}")
        print(f"Selected Model: {llm.model}")
        
        # Test code generation
        print("\n📝 Testing code generation...")
        result = llm.generate_code("Write a Python function to check if a number is prime", "python")
        
        if result['success']:
            print(f"\n✅ {result['message']}")
            print(f"\n📄 Generated Code:\n{'-'*50}")
            print(result['code'])
        else:
            print(f"\n❌ {result['message']}")
    else:
        print("❌ Ollama is not running. Please install and start Ollama first.")
        print("\nInstallation instructions:")
        print("1. Download Ollama from: https://ollama.ai")
        print("2. Install Ollama on your system")
        print("3. Run: ollama pull codellama:7b")
        print("4. Ollama service should start automatically")
