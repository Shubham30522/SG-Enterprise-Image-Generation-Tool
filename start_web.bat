@echo off
title Gemini Auto Tool - Web UI
echo ==========================================
echo   Gemini Auto Tool - Web UI Launcher
echo ==========================================
echo.

:: Start the FastAPI backend
echo Starting Backend Server on port 8000...
start "Backend" cmd /c "cd /d %~dp0 && python -m uvicorn server:app --reload --port 8000"

:: Wait a moment for backend to initialize
timeout /t 3 /nobreak > nul

:: Start the frontend dev server
:: Open Chrome after a short delay to allow servers to start
start "" cmd /c "timeout /t 4 /nobreak > nul & start chrome http://localhost:5173"

echo Starting Frontend on port 5173...
cd /d %~dp0web
call npm run dev

pause
