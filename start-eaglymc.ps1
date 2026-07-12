# EaglyMC 1.8 modded client — http://localhost:8081
$port = 8081
$webDir = Join-Path $PSScriptRoot "eaglymc"

Write-Host "EaglyMC local server"
Write-Host "Open: http://localhost:$port"
Write-Host "Chromebook (same Wi-Fi): http://<PC-IP>:$port"
Write-Host ""

Set-Location $webDir
python -m http.server $port
