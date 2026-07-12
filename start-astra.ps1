# Minecraft Astra Edition — http://localhost:8085
$port = 8085
$webDir = Join-Path $PSScriptRoot "minecraft-astra"

if (-not (Test-Path $webDir)) {
    powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "scripts\setup_astra.ps1")
}

Write-Host "Minecraft Astra Edition: http://localhost:$port"
Set-Location $webDir
python -m http.server $port
