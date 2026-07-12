# Download upstream + patch web-js if needed
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$webJs = Join-Path $root "web-js"
$upstream = Join-Path $webJs "index.html.upstream"
$url = "https://github.com/ojw12/eaglercraft/releases/download/1.12.2/Eaglercraft_1.12_Offline_en_US.html"

if (-not (Test-Path $upstream)) {
    Write-Host "Downloading 1.12 JS client..."
    New-Item -ItemType Directory -Force -Path $webJs | Out-Null
    Invoke-WebRequest -Uri $url -OutFile $upstream -UseBasicParsing
}

python (Join-Path $root "scripts\patch_web_js_boot.py")
