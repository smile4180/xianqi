$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$pythonPath = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw 'Virtual environment missing. Follow README setup instructions first.'
}
Push-Location $projectRoot
try {
    & $pythonPath app_server.py
    $processExitCode = $LASTEXITCODE
} finally {
    Pop-Location
}
exit $processExitCode
