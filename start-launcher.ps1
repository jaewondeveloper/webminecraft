# Minecraft Web Launcher — local + GitHub Pages
$port = 8090
$siteDir = $PSScriptRoot

Write-Host "Minecraft Launcher: http://localhost:$port"
Write-Host "GitHub Pages: https://jaewondeveloper.github.io/webminecraft/"
Write-Host "게임 서버도 필요하면 start-all.ps1 을 실행하세요."
Write-Host ""

Set-Location $siteDir
python -m http.server $port
