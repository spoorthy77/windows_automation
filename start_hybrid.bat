@echo off
REM Start Hybrid Chatbot Launcher

echo ========================================
echo  Hybrid Chatbot Launcher
echo ========================================
echo.

REM Activate virtual environment
call automation_env\Scripts\activate.bat

REM Launch Launcher
python hybrid_launcher.py

pause
