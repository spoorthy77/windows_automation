@echo off
echo ========================================
echo Windows Automation Web App - Setup
echo ========================================
echo.

echo [1/3] Installing Backend Dependencies...
cd backend
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Backend installation failed!
    pause
    exit /b 1
)

echo.
echo [2/3] Installing Frontend Dependencies...
cd ..\frontend
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Frontend installation failed!
    pause
    exit /b 1
)

echo.
echo [3/3] Setup Complete!
echo.
echo ========================================
echo Ready to Launch!
echo ========================================
echo.
echo To start the web app:
echo   1. Run "start-backend.bat" in one terminal
echo   2. Run "start-frontend.bat" in another terminal
echo   3. Open http://localhost:3000 in your browser
echo.
pause
