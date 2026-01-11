@echo off
echo ========================================
echo Windows Automation Web App Launcher
echo ========================================
echo.
echo Starting Backend and Frontend...
echo.

REM Activate Python environment if it exists
if exist "..\automation_env\Scripts\activate.bat" (
    call ..\automation_env\Scripts\activate.bat
)

REM Start Flask backend
start "Backend Server - Flask" cmd /k "python app.py"
timeout /t 3 /nobreak > nul

REM Start React frontend
start "React Frontend" cmd /k "cd /d "%~dp0frontend" && npm start"

timeout /t 5 /nobreak

REM Open browser
start http://localhost:3000

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo.
echo Backend:  http://localhost:5000 (Flask API)
echo Frontend: http://localhost:3000 (React App)
echo.
echo.
echo Browser will open automatically...
echo.
pause
