@echo off
echo ========================================
echo  OFFLINE CHATBOT - COMPLETE SETUP
echo ========================================
echo.

cd /d "%~dp0"

echo Step 1: Activating virtual environment...
call ..\..\automation_env\Scripts\activate.bat

echo.
echo Step 2: Installing Python dependencies...
pip install -r offline_requirements.txt

echo.
echo Step 3: Testing offline NLP engine...
python offline_nlp.py

echo.
echo ========================================
echo  SETUP COMPLETE!
echo ========================================
echo.
echo To start the application:
echo 1. Run: start-offline-backend.bat
echo 2. Run: start-offline-frontend.bat (in another terminal)
echo 3. Open http://localhost:3000 in browser
echo.

pause
