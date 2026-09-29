Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "       Starting Meeting Prep Agent...        " -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Launch browser
Start-Process "http://localhost:8080"

# Run Flask
python app.py
