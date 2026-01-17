@echo off
REM Start Hybrid Chatbot GUI

echo ========================================
echo  Starting Hybrid Chatbot GUI...
echo ========================================
echo.

REM Activate virtual environment
call automation_env\Scripts\activate.bat

REM Launch GUI
python hybrid_gui.py

pause
