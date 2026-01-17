# 🚀 Offline LLM Program Generator Setup Guide

## Overview
This guide helps you set up the **Offline Program Generator** feature for the Windows Automation Chatbot. This feature uses a locally hosted LLM to generate programs in Python, Java, C, and C++ without requiring internet connectivity.

---

## 📋 Prerequisites

### 1. Python Environment
- Python 3.8 or higher
- Virtual environment (automation_env) already created

### 2. System Requirements
- **RAM**: Minimum 8GB (16GB recommended for larger models)
- **Disk Space**: ~10GB free space for LLM models
- **OS**: Windows 10/11

### 3. Required Compilers (for validation)

#### Python (Required) ✅
Already installed with your Python environment.

#### Java (Optional)
- **Download**: [Oracle JDK](https://www.oracle.com/java/technologies/downloads/) or [OpenJDK](https://adoptium.net/)
- **Install**: Follow installer instructions
- **Verify**: Open cmd and run `javac -version`

#### C/C++ (Optional)
- **Download**: [MinGW-w64](https://sourceforge.net/projects/mingw-w64/)
- **Install**: Follow installer instructions, add to PATH
- **Verify**: Open cmd and run `gcc --version`

---

## 🔧 Installation Steps

### Step 1: Install Ollama

Ollama is the local LLM runtime that enables offline code generation.

1. **Download Ollama**:
   - Visit: [https://ollama.ai](https://ollama.ai)
   - Click "Download for Windows"
   - Run the installer

2. **Verify Installation**:
   ```powershell
   ollama --version
   ```

3. **Start Ollama Service**:
   ```powershell
   ollama serve
   ```
   
   Keep this terminal window open. Ollama runs in the background.

### Step 2: Download Code Generation Model

1. **Download CodeLlama** (Recommended for code generation):
   ```powershell
   ollama pull codellama
   ```
   
   This downloads a 3.8GB model optimized for code generation.
   
   **Alternative Models** (Optional):
   - `ollama pull deepseek-coder` - Specialized for coding (6.7GB)
   - `ollama pull mistral` - General purpose, fast (4.1GB)
   - `ollama pull llama2` - Fallback option (3.8GB)

2. **Verify Model Installation**:
   ```powershell
   ollama list
   ```
   
   You should see `codellama` in the list.

### Step 3: Install Python Dependencies

Already included in your project, but verify:

```powershell
cd "C:\Users\m6793\Downloads\MY PROJECTS\automation_project"
.\automation_env\Scripts\activate
pip install requests psutil python-dotenv
```

### Step 4: Test the Installation

1. **Test Ollama Connection**:
   ```powershell
   python offline_llm_client.py
   ```
   
   Expected output:
   ```
   ✅ Ollama is running
   Available models: ['codellama']
   📝 Generating sample Python code...
   ```

2. **Test Code Validator**:
   ```powershell
   python code_validator.py
   ```
   
   Shows which compilers are available.

3. **Test Program Generator**:
   ```powershell
   python program_generator.py
   ```
   
   Generates a sample factorial program.

---

## 🎯 Usage Examples

### From the Chatbot

Start the chatbot:
```powershell
python hybrid_launcher.py
```

Or use the GUI:
```powershell
start_hybrid_gui.bat
```

### Example Commands

#### Python Programs
```
write a python program to calculate factorial
create a python program for fibonacci series
generate python code for bubble sort
make a python calculator program
```

#### Java Programs
```
write a java program for palindrome check
create a java program to find prime numbers
generate java code for binary search
```

#### C Programs
```
write a c program to reverse a string
create a c program for matrix multiplication
```

#### C++ Programs
```
write a cpp program for linked list
generate c++ code for stack implementation
```

---

## 📁 Output Location

Generated programs are saved to:
```
C:\Users\<YourUsername>\Desktop\GeneratedPrograms\
```

Each program is automatically:
1. Generated using the LLM
2. Validated (syntax check/compilation)
3. Auto-corrected if errors found (up to 3 attempts)
4. Saved with timestamp in filename

---

## 🔍 How It Works

### Architecture

```
User Request
    ↓
Language Detection (Python/Java/C/C++)
    ↓
LLM Code Generation (Ollama)
    ↓
Code Validation (Syntax Check/Compilation)
    ↓
    ├─ Valid? → Save File → Done ✅
    └─ Errors? → Send to LLM for Fix → Re-validate (up to 3 attempts)
```

### Features

✅ **Completely Offline** - No internet required  
✅ **Multi-language Support** - Python, Java, C, C++  
✅ **Auto-Validation** - Ensures code compiles  
✅ **Auto-Correction** - Fixes errors automatically  
✅ **Smart Language Detection** - Detects language from request  
✅ **Detailed Logging** - Tracks generation process  

---

## 🛠️ Troubleshooting

### Issue: "Ollama is not running"

**Solution**:
1. Open a new terminal
2. Run: `ollama serve`
3. Keep it running in the background

### Issue: "Model not found"

**Solution**:
```powershell
ollama pull codellama
```

### Issue: "Java compiler not found"

**Solution**:
- Install JDK: [https://adoptium.net/](https://adoptium.net/)
- Add to PATH: `C:\Program Files\Java\jdk-XX\bin`
- Restart terminal

### Issue: "GCC compiler not found"

**Solution**:
- Install MinGW: [https://sourceforge.net/projects/mingw-w64/](https://sourceforge.net/projects/mingw-w64/)
- Add to PATH: `C:\mingw\bin`
- Restart terminal

### Issue: Generation is slow

**Solutions**:
- Use smaller models (mistral instead of codellama)
- Close other applications to free RAM
- Ensure Ollama has sufficient resources

### Issue: Code has errors after 3 attempts

**Explanation**: Complex programs may require manual review.

**Solution**:
- Generated code is still saved to Desktop
- Open and review manually
- Error messages are included in chatbot response

---

## ⚙️ Configuration

### Change Save Directory

Edit [program_generator.py](program_generator.py):

```python
generator = ProgramGenerator(save_dir="D:/MyPrograms")
```

### Change LLM Model

Edit [offline_llm_client.py](offline_llm_client.py):

```python
client = OfflineLLMClient(model="deepseek-coder")
```

### Adjust Retry Attempts

Edit [program_generator.py](program_generator.py):

```python
self.max_retries = 5  # Default is 3
```

---

## 📊 Supported Program Types

### ✅ Data Structures & Algorithms
- Sorting (bubble, quick, merge, insertion)
- Searching (binary, linear)
- Arrays, strings, linked lists
- Stacks, queues, trees
- Graphs, hash tables

### ✅ Programming Concepts
- Loops, recursion, patterns
- Functions, classes, OOP
- File handling, I/O
- Exception handling
- Regular expressions

### ✅ Problem Solving
- Mathematical problems
- String manipulation
- Number theory
- Dynamic programming
- Greedy algorithms

### ✅ Practical Applications
- Calculators, converters
- Data validators
- Simple games
- Utility scripts

---

## 🚀 Advanced Usage

### Specify Language Explicitly

```python
from program_generator import program_generator

result = program_generator.generate_program(
    "Calculate factorial",
    language="java"
)
```

### Custom Output Directory

```python
result = program_generator.generate_program(
    "Fibonacci series",
    output_dir="C:/Projects"
)
```

### Check Compiler Status

```python
from code_validator import code_validator

status = code_validator.get_compiler_info()
print(status)
```

---

## 📚 Additional Resources

- **Ollama Documentation**: [https://github.com/ollama/ollama](https://github.com/ollama/ollama)
- **CodeLlama Model**: [https://ollama.ai/library/codellama](https://ollama.ai/library/codellama)
- **Python Documentation**: [https://docs.python.org/](https://docs.python.org/)
- **Java Documentation**: [https://docs.oracle.com/en/java/](https://docs.oracle.com/en/java/)

---

## 🎓 Tips for Best Results

1. **Be Specific**: "Write a Python program to sort an array using bubble sort" is better than "write a sort program"

2. **Include Details**: Mention input/output requirements, edge cases, etc.

3. **Start Simple**: Test with simple programs before complex ones

4. **Check Output**: Always review generated code before running

5. **Use Comments**: Request "with comments" for documented code

---

## 📝 Example Session

```
You: write a python program to check if a number is prime

Bot: ✅ Program generated successfully!

     📝 Language: PYTHON
     📄 Filename: prime_20260112_143052.py
     📁 Location: C:\Users\...\Desktop\GeneratedPrograms\prime_20260112_143052.py
     ✅ Validation: Passed (Error-free code)
     🔄 Attempts: 1/3
     
     You can now run the program from: C:\Users\...\Desktop\GeneratedPrograms\prime_20260112_143052.py
```

---

## ✅ Setup Checklist

- [ ] Ollama installed
- [ ] Ollama service running (`ollama serve`)
- [ ] CodeLlama model downloaded (`ollama pull codellama`)
- [ ] Python environment activated
- [ ] Test scripts run successfully
- [ ] (Optional) Java JDK installed
- [ ] (Optional) MinGW GCC installed

---

## 🆘 Support

If you encounter issues:

1. Check Ollama is running: `ollama serve`
2. Verify model is downloaded: `ollama list`
3. Test individual components (llm client, validator, generator)
4. Check logs in the automation project folder
5. Ensure sufficient disk space and RAM

---

**Happy Coding! 🎉**
