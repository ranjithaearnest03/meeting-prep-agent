@echo off
title Meeting Prep Agent - Mobile Phone Access
echo =========================================================
echo       Meeting Prep Agent - Phone Access & Remote Link
echo =========================================================
echo.
echo Option 1: On the SAME Wi-Fi network:
echo    Open this URL in Safari/Chrome on your phone:
echo    http://10.174.30.42:8080
echo.
echo Option 2: On Cellular Data (4G/5G) or Anywhere in the World:
echo    Creating a secure public HTTPS link for your phone...
echo    (Press Ctrl+C to stop sharing when done)
echo.
ssh -p 443 -o StrictHostKeyChecking=no -R0:localhost:8080 a.pinggy.io
pause
