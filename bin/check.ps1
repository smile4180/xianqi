$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $projectRoot
try {
    & '.\.venv\Scripts\python.exe' -m pytest
    if ($LASTEXITCODE -ne 0) { throw 'Backend tests failed.' }
    node --test tests/client.test.cjs
    if ($LASTEXITCODE -ne 0) { throw 'Client tests failed.' }
    node bin/check-miniprogram.cjs
    if ($LASTEXITCODE -ne 0) { throw 'Mini program static checks failed.' }
} finally {
    Pop-Location
}
