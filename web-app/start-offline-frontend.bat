@echo off

echo ========================================
echo  OFFLINE WINDOWS AUTOMATION CHATBOT
echo  Starting React Frontend...
echo ========================================
echo.

cd /d "%~dp0frontend"

echo Starting React development server...
echo This will open http://localhost:3000 in your browser
echo.

npm start

pause
