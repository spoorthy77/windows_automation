@echo off
REM Complete setup script for Web Application

setlocal enabledelayedexpansion

echo.
echo ======================================================================
echo   Windows Automation Assistant - Web App Complete Setup
echo ======================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js and try again
    pause
    exit /b 1
)

REM Get Python version
echo Checking Python...
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo %PYTHON_VERSION% found ✓

REM Get Node version
echo Checking Node.js...
for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
echo Node.js v!NODE_VERSION! found ✓

echo.
echo Step 1: Installing Python dependencies...
echo ======================================================================
if exist "..\automation_env\Scripts\activate.bat" (
    call ..\automation_env\Scripts\activate.bat
) else (
    echo WARNING: Virtual environment not found
    echo Using system Python
)

pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
echo Python dependencies installed ✓

echo.
echo Step 2: Installing frontend Node modules...
echo ======================================================================
cd frontend
if exist node_modules (
    echo Node modules already installed
) else (
    echo Installing npm packages...
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install npm packages
        pause
        exit /b 1
    )
)
echo Frontend dependencies installed ✓
cd ..

echo.
echo ======================================================================
echo ✅ Setup Complete!
echo ======================================================================
echo.
echo You can now launch the application using:
echo   • start-all.bat          (Start everything at once)
echo   • start-backend.bat      (Start Flask backend only)
echo   • start-frontend.bat     (Start React frontend only)
echo.
echo Browser will open at: http://localhost:3000
echo Backend API runs at: http://localhost:5000
echo.
pause
