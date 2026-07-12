# Minecraft 1.12.2 JavaScript — http://localhost:8084
$port = 8084
$webDir = Join-Path $PSScriptRoot "web-js"

Write-Host "Minecraft 1.12.2 JS: http://localhost:$port"
Write-Host "Chromebook (same Wi-Fi): http://<PC-IP>:$port"
Write-Host ""

Set-Location $webDir
python -m http.server $port
