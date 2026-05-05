@echo off
title Shotloom - Web Interface
color 0A

echo.
echo ===============================================
echo    SHOTLOOM - WEB INTERFACE
echo ===============================================
echo.
echo Starting the web server...
echo.
echo =====================================================
echo    ACCESS FROM OTHER DEVICES (iPad/Phone):
echo    Look for "Network URL" below after startup
echo    Example: http://192.168.x.x:8501
echo =====================================================
echo.

python -m streamlit run web_app.py --server.headless true

pause
