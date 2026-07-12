# Restore + patch web/index.html (8080 WASM) from upstream
$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$web = Join-Path $root "web"
$upstream = Join-Path $web "index.html.upstream"
$url = "https://github.com/ojw12/eaglercraft/releases/download/1.12.2/Eaglercraft_1.12.2_WASM_Offline_Download.html"
$index = Join-Path $web "index.html"

if (-not (Test-Path $upstream)) {
    Write-Host "Downloading WASM upstream..."
    Invoke-WebRequest -Uri $url -OutFile $upstream -UseBasicParsing -TimeoutSec 600
}

$needRestore = $false
if (-not (Test-Path $index)) { $needRestore = $true }
else {
    $sz = (Get-Item $index).Length
    if ($sz -lt 15000000) {
        Write-Host "index.html truncated ($sz bytes) — restoring from upstream"
        $needRestore = $true
    }
}

if ($needRestore) {
    Copy-Item -Force $upstream $index
    Write-Host "Restored index.html from upstream"
}

$srcJs = Join-Path $root "web-js"
foreach ($name in @("favicon.png", "splash.png", "splash2.png")) {
    $from = Join-Path $srcJs $name
    if (Test-Path $from) { Copy-Item -Force $from (Join-Path $web $name) }
}
if (Test-Path (Join-Path $srcJs "jaewon-boot.js")) {
    Copy-Item -Force (Join-Path $srcJs "jaewon-boot.js") (Join-Path $web "jaewon-boot.js")
}

python (Join-Path $root "scripts\patch_web_boot.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python (Join-Path $root "scripts\fix_web_launch_overlay.py")
Write-Host "8080 web client ready."
