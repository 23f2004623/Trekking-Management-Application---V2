# Ensures Node.js is on PATH for this session, then starts the Vite dev server.
$nodeDir = "C:\Program Files\nodejs"
if (-not (Test-Path "$nodeDir\node.exe")) {
    Write-Error "Node.js not found at $nodeDir. Install from https://nodejs.org"
    exit 1
}
if ($env:PATH -notlike "*$nodeDir*") {
    $env:PATH = "$nodeDir;$env:PATH"
}
Set-Location $PSScriptRoot
node -v
npm -v
npm run dev
