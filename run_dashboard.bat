@echo off
cd /d "%~dp0"
set PYTHONPATH=%~dp0;%PYTHONPATH%

echo ===============================================================================
echo Starting WHO-Style Explainable HRV ^& Cognitive Mental Load Digital Twin
echo Developer: Ms. Taniya Mondal, B.Tech ^| Version 1.0
echo ===============================================================================
echo.
echo Launching Web Dashboard at http://127.0.0.1:5000 ...
echo (Press Ctrl+C in this terminal window to stop the server)
echo.

start http://127.0.0.1:5000
python web_app\app.py
pause
