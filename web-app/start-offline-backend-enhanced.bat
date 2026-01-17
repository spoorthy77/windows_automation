@echo off
REM Enhanced Offline Backend Server with AI Code Generation
REM Starts the Flask server with LLM integration

echo ============================================================
echo   OFFLINE CHATBOT WITH AI CODE GENERATION - STARTING
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "..\automation_env\Scripts\activate.bat" (
    echo [WARNING] Virtual environment not found
    echo Creating virtual environment...
    python -m venv ..\automation_env
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call ..\automation_env\Scripts\activate.bat

REM Install/update requirements
echo [INFO] Checking dependencies...
pip install -r offline_requirements.txt --quiet

REM Check if Ollama is running
echo [INFO] Checking Ollama status...
curl -s http://localhost:11434 >nul 2>&1
if errorlevel 1 (
    echo.
    echo ============================================================
    echo   WARNING: OLLAMA IS NOT RUNNING!
    echo ============================================================
    echo   AI Code Generation will NOT work without Ollama.
    echo.
    echo   Quick Setup:
    echo   1. Download Ollama from: https://ollama.ai
    echo   2. Install and start Ollama
    echo   3. Run: ollama pull codellama:7b
    echo   4. Restart this script
    echo ============================================================
    echo.
    echo Press any key to continue without Ollama (basic features only)
    echo Or press Ctrl+C to exit and set up Ollama first
    pause >nul
)

REM Start the server
echo.
echo ============================================================
echo   Starting Offline Backend Server...
echo ============================================================
echo.
python offline_app.py

pause
