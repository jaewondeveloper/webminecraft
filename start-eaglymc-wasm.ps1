# EaglyMC WASM — http://localhost:8082 (크롬북 추천)
$port = 8082
Set-Location (Join-Path $PSScriptRoot "eaglymc-wasm")
Write-Host "EaglyMC WASM: http://localhost:$port"
python -m http.server $port
