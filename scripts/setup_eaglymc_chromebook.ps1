# Creates eaglymc-chromebook/ with hardlinks to large game files from eaglymc/
$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$src = Join-Path $root "eaglymc"
$dst = Join-Path $root "eaglymc-chromebook"

if (-not (Test-Path $src)) {
    Write-Error "Missing source folder: $src"
}

New-Item -ItemType Directory -Force -Path $dst | Out-Null

function Link-Or-CopyFile($name) {
    $from = Join-Path $src $name
    $to = Join-Path $dst $name
    if (-not (Test-Path $from)) {
        Write-Warning "Skip missing: $from"
        return
    }
    if (Test-Path $to) { Remove-Item $to -Force }
    try {
        New-Item -ItemType HardLink -Path $to -Target $from | Out-Null
        Write-Host "hardlink $name"
    } catch {
        Copy-Item $from $to -Force
        Write-Host "copy $name"
    }
}

Link-Or-CopyFile "classes.js"
Link-Or-CopyFile "assets.epk"

$langSrc = Join-Path $src "lang"
$langDst = Join-Path $dst "lang"
if (Test-Path $langDst) { Remove-Item $langDst -Recurse -Force }
try {
    cmd /c mklink /J "`"$langDst`"" "`"$langSrc`"" | Out-Null
    Write-Host "junction lang"
} catch {
    Copy-Item $langSrc $langDst -Recurse -Force
    Write-Host "copy lang"
}

$assets = @("favicon.png", "splash.png", "splash2.png", "crashLogo.png", "pressAnyKey.png", "jaewon-boot.js")
foreach ($a in $assets) {
    $from = Join-Path $src $a
    if (-not (Test-Path $from)) { $from = Join-Path (Join-Path $root "web") $a }
    if (Test-Path $from) {
        Copy-Item $from (Join-Path $dst $a) -Force
        Write-Host "asset $a"
    }
}

Write-Host ""
Write-Host "Ready: $dst"
Write-Host "Run: .\start-eaglymc-chromebook.ps1"
