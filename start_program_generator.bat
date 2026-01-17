@echo off
REM Quick Start Guide for Offline Program Generator

echo ╔══════════════════════════════════════════════════════════════╗
echo ║   Offline LLM Program Generator - Quick Start               ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo This feature lets you generate programs using AI completely offline!
echo.
echo ┌──────────────────────────────────────────────────────────────┐
echo │  PREREQUISITES                                               │
echo └──────────────────────────────────────────────────────────────┘
echo.
echo 1. Ollama installed (download from https://ollama.ai)
echo 2. CodeLlama model downloaded (ollama pull codellama)
echo 3. Ollama service running (ollama serve)
echo.
echo ┌──────────────────────────────────────────────────────────────┐
echo │  QUICK SETUP                                                 │
echo └──────────────────────────────────────────────────────────────┘
echo.
echo If you haven't set up yet, run:
echo    setup_offline_llm.bat
echo.

pause
cls

echo ┌──────────────────────────────────────────────────────────────┐
echo │  EXAMPLE COMMANDS                                            │
echo └──────────────────────────────────────────────────────────────┘
echo.
echo Try these commands in the chatbot:
echo.
echo 📝 Python:
echo    - "write a python program to calculate factorial"
echo    - "create a python program for bubble sort"
echo    - "generate python code for fibonacci series"
echo.
echo ☕ Java:
echo    - "write a java program to check palindrome"
echo    - "create a java program for prime numbers"
echo.
echo 🔧 C:
echo    - "write a c program to reverse a string"
echo    - "create a c program for matrix addition"
echo.
echo ⚡ C++:
echo    - "write a cpp program for linked list"
echo    - "generate c++ code for stack implementation"
echo.
pause
cls

echo ┌──────────────────────────────────────────────────────────────┐
echo │  TESTING SYSTEM                                              │
echo └──────────────────────────────────────────────────────────────┘
echo.
echo Running system tests...
echo.

call automation_env\Scripts\activate.bat
python test_offline_llm.py

echo.
pause
cls

echo ┌──────────────────────────────────────────────────────────────┐
echo │  START CHATBOT                                               │
echo └──────────────────────────────────────────────────────────────┘
echo.
echo Choose your interface:
echo.
echo 1. Terminal Interface (text-based)
echo 2. GUI Interface (graphical)
echo 3. Exit
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    cls
    echo Starting Terminal Chatbot...
    echo.
    python hybrid_launcher.py
) else if "%choice%"=="2" (
    cls
    echo Starting GUI Chatbot...
    echo.
    call start_hybrid_gui.bat
) else (
    echo.
    echo Goodbye!
    timeout /t 2 /nobreak >nul
)
