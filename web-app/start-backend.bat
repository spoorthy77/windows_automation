@echo off
title Windows Automation - Backend Server (Flask)
echo ========================================
echo Starting Backend Server (Flask - Port 5000)
echo ========================================
echo.

REM Activate Python environment
if exist "..\automation_env\Scripts\activate.bat" (
    call ..\automation_env\Scripts\activate.bat
) else (
    echo WARNING: Virtual environment not found
)

echo Starting Flask API server...
echo API available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop
echo.

python app.py

pause
