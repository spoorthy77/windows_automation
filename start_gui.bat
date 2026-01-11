@echo off
title Windows Automation Assistant - GUI Launcher
cd /d "%~dp0"
call automation_env\Scripts\activate.bat
python gui_chatbot.py
pause
