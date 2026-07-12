# EaglyMC Chromebook 저사양 — http://localhost:8083
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$src = Join-Path $root "eaglymc"
$dst = Join-Path $root "eaglymc-chromebook"
$setup = Join-Path $root "scripts\setup_eaglymc_chromebook.ps1"

if (-not (Test-Path $dst)) {
    & $setup
}

$port = 8083
Write-Host "EaglyMC Chromebook (저사양 JS) — http://localhost:$port"
Write-Host "같은 Wi-Fi 크롬북: http://<PC-IP>:$port"
Write-Host ""

Set-Location $dst
python -m http.server $port
