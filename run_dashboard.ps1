# WHO-Style Explainable HRV & Cognitive Mental Load Digital Twin Launcher
# Developer: Ms. Taniya Mondal, B.Tech | Version 1.0

Set-Location $PSScriptRoot
$env:PYTHONPATH = "$PSScriptRoot;$env:PYTHONPATH"

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Starting WHO-Style Explainable HRV & Cognitive Mental Load Digital Twin" -ForegroundColor Green
Write-Host "Developer: Ms. Taniya Mondal, B.Tech | Version 1.0" -ForegroundColor Yellow
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Launching Web Dashboard at http://127.0.0.1:5000 ..." -ForegroundColor White

Start-Process "http://127.0.0.1:5000"
python web_app\app.py
