@echo off
title Meeting Prep Agent
echo ==============================================
echo       Starting Meeting Prep Agent...
echo ==============================================
echo.
cd /d "%~dp0"

echo Launching browser at http://localhost:8080...
start http://localhost:8080

echo Starting Python Flask Server...
python app.py
pause
