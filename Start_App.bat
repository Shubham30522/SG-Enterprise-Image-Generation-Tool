@echo off
cd /d "%~dp0"
echo Starting Gemini Auto Tool (GUI)...
python main.py
if errorlevel 1 pause
