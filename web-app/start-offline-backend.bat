@echo off
echo ========================================
echo  OFFLINE WINDOWS AUTOMATION CHATBOT
echo  Starting Backend Server...
echo ========================================
echo.

cd /d "%~dp0"

REM Activate virtual environment
echo Activating virtual environment...
call ..\automation_env\Scripts\activate.bat

echo.
echo Starting Flask backend on http://localhost:5000
echo.
echo ========================================
echo Backend is ready!
echo Open http://localhost:3000 in browser
echo ========================================
echo.

REM Start the offline backend
python offline_app.py

pause
