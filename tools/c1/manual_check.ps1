# Stage: hardware characterization. One explicit bounded engineering run.
[CmdletBinding()]
param([switch]$PressureOnly)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
Push-Location $repo
try {
    & python -B tools/c1/gmp_setup.py calibration-build
    if ($LASTEXITCODE -ne 0) { throw 'Offline harness build refused.' }
    & local\c1\gmp-setup\calibration\cal_guard.exe --pressure-check
    if ($LASTEXITCODE -ne 0) { throw 'Resource preflight refused. Stop; do not retry repeatedly.' }
    if ($PressureOnly) { return }
    $bundle = 'manual-' + [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')
    & python -B tools/c1/route_subset.py --bundle-id $bundle
    if ($LASTEXITCODE -ne 0) { throw 'Subset stopped. Its evidence and budget reservation are retained.' }
    Write-Output ('Evidence: local/c1/benchmark_bundles/' + $bundle)
    Write-Output 'Engineering check complete; C1 remains open. No production or scientific run is authorized.'
} finally { Pop-Location }
