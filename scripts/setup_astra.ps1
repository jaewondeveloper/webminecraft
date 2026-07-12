# Setup Minecraft Astra Edition (port 8085) with locked resource pack
$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$src = Join-Path $root "eaglymc"
$dst = Join-Path $root "minecraft-astra"
$zip = Join-Path $env:USERPROFILE "Downloads\Astra 1.19.2.zip"

if (-not (Test-Path $src)) { throw "Missing eaglymc source" }
if (-not (Test-Path $zip)) { throw "Missing Astra zip: $zip" }

New-Item -ItemType Directory -Force -Path $dst | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $dst "resourcepacks") | Out-Null

function Link-Or-Copy($name) {
    $from = Join-Path $src $name
    $to = Join-Path $dst $name
    if (-not (Test-Path $from)) { return }
    if (Test-Path $to) { Remove-Item $to -Force }
    try { New-Item -ItemType HardLink -Path $to -Target $from | Out-Null }
    catch { Copy-Item $from $to -Force }
}

foreach ($f in @("classes.js", "assets.epk")) { Link-Or-Copy $f }

$langSrc = Join-Path $src "lang"
$langDst = Join-Path $dst "lang"
if (Test-Path $langDst) { Remove-Item $langDst -Recurse -Force }
try { cmd /c mklink /J "`"$langDst`"" "`"$langSrc`"" | Out-Null }
catch { Copy-Item $langSrc $langDst -Recurse -Force }

foreach ($a in @("favicon.png", "splash.png", "splash2.png", "crashLogo.png", "pressAnyKey.png")) {
    $from = Join-Path $src $a
    if (Test-Path $from) { Copy-Item $from (Join-Path $dst $a) -Force }
}

Copy-Item -Force (Join-Path $root "web\jaewon-boot.js") (Join-Path $dst "jaewon-boot.js")
Copy-Item -Force $zip (Join-Path $dst "resourcepacks\Astra.zip")

# ZIP only — browser installs on first launch via astra-boot.js + JSZip

Write-Host "Astra edition ready at $dst"
