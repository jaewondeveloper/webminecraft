# Copy launcher UI to repo root for GitHub Pages
$root = Split-Path $PSScriptRoot -Parent
$src = Join-Path $root "launcher"
$files = @("index.html", "launcher.js", "launcher.css", "mc-button.js", "creeper.jpg", "favicon.png")
foreach ($f in $files) {
    $from = Join-Path $src $f
    $to = Join-Path $root $f
    if (Test-Path $from) {
        Copy-Item -Force $from $to
        Write-Host "synced $f"
    }
}
