@echo off
title Windows Automation - Frontend (React)
cd /d "%~dp0frontend"
echo ========================================
echo Starting React Frontend (Port 3000)
echo ========================================
echo.
echo Browser will open automatically...
echo App will be available at: http://localhost:3000
echo.
echo Make sure the backend is running first!
echo (Start backend with: start-backend.bat)
echo.
echo Press Ctrl+C to stop
echo.
call npm start
pause
