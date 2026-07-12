# Start all game servers + launcher
$root = $PSScriptRoot
$scripts = @(
    @{ Name = "8080 WASM 1.12.2"; File = "start-server.ps1" },
    @{ Name = "8081 EaglyMC JS"; File = "start-eaglymc.ps1" },
    @{ Name = "8082 EaglyMC WASM"; File = "start-eaglymc-wasm.ps1" },
    @{ Name = "8083 Chromebook"; File = "start-eaglymc-chromebook.ps1" },
    @{ Name = "8084 JS 1.12.2"; File = "start-server-js.ps1" },
    @{ Name = "8085 Astra Edition"; File = "start-astra.ps1" },
    @{ Name = "8090 Launcher"; File = "start-launcher.ps1" }
)

Write-Host "Starting all servers in new windows..."
foreach ($s in $scripts) {
    $path = Join-Path $root $s.File
    if (Test-Path $path) {
        Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", $path
        Start-Sleep -Milliseconds 400
        Write-Host "  started $($s.Name)"
    } else {
        Write-Host "  missing $($s.File)" -ForegroundColor Yellow
    }
}
Write-Host ""
Write-Host "Launcher: http://localhost:8090"
