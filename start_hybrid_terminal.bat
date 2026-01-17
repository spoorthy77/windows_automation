@echo off
REM Start Hybrid Chatbot Terminal

echo ========================================
echo  Starting Hybrid Chatbot Terminal...
echo ========================================
echo.

REM Activate virtual environment
call automation_env\Scripts\activate.bat

REM Launch Terminal
python hybrid_terminal.py

pause
