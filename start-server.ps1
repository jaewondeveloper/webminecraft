# Eaglercraft 1.12.2 local web server
# Open http://localhost:8080 in Chrome/Edge (WASM-GC needs Chromium)

$port = 8080
$webDir = Join-Path $PSScriptRoot "web"

Write-Host "Serving Eaglercraft 1.12.2 WASM from: $webDir"
Write-Host "Open: http://localhost:$port"
Write-Host "Press Ctrl+C to stop"
Write-Host ""

Set-Location $webDir
python -m http.server $port
