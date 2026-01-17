@echo off
echo ============================================
echo   Offline LLM Setup - Quick Installer
echo ============================================
echo.

REM Check if Ollama is installed
where ollama >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [X] Ollama is not installed!
    echo.
    echo Please download and install Ollama from:
    echo https://ollama.ai
    echo.
    pause
    exit /b 1
)

echo [✓] Ollama is installed
echo.

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [!] Starting Ollama service...
    start "" ollama serve
    timeout /t 5 /nobreak >nul
    echo [✓] Ollama service started
) else (
    echo [✓] Ollama is already running
)
echo.

REM Check if codellama model exists
echo Checking for CodeLlama model...
ollama list | findstr /C:"codellama" >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [!] CodeLlama model not found. Downloading...
    echo This may take several minutes (3.8GB download)
    echo.
    ollama pull codellama
    if %ERRORLEVEL% EQU 0 (
        echo [✓] CodeLlama model downloaded successfully
    ) else (
        echo [X] Failed to download model
        pause
        exit /b 1
    )
) else (
    echo [✓] CodeLlama model is already installed
)
echo.

REM Activate virtual environment and test
echo Activating Python environment...
call automation_env\Scripts\activate.bat

echo.
echo Testing installation...
echo.
python offline_llm_client.py

echo.
echo ============================================
echo   Setup Complete!
echo ============================================
echo.
echo You can now use the program generation feature:
echo   - Run: python hybrid_launcher.py
echo   - Or: start_hybrid_gui.bat
echo.
echo Try commands like:
echo   "write a python program to calculate factorial"
echo   "create a java program for bubble sort"
echo.
pause
