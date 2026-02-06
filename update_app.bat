@echo off
cd /d "%~dp0"
echo Updating Gemini Auto Tool...
git pull
echo.
echo Installing/Updating dependencies...
pip install -r requirements.txt
echo.
echo Update finished! You can now run Start_App.bat
pause
