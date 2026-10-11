#Requires -Version 5.1
<# Standalone elevated L1 engineering launcher. Preflight never mutates Windows.
Run blocks all external IPv4/IPv6 traffic on this machine for a bounded window.
Only our two uniquely named firewall rules and our cleanup task are removed.
This is acceptance infrastructure, never a scientific runner or L1 PASS gate.
#>
[CmdletBinding()]
param(
    [ValidateSet('Preflight', 'Run')][string]$Mode = 'Preflight',
    [string]$PythonPath = '',
    [ValidatePattern('^[a-fA-F0-9]{64}$')][string]$ExpectedSourceSha256 = '',
    [ValidatePattern('^[a-fA-F0-9]{64}$')][string]$ExpectedLauncherSha256 = ''
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
$helper = Join-Path $PSScriptRoot 'offline_acceptance.py'
$launcherHash = (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
if (!$PythonPath) { $PythonPath = (Get-Command python.exe -ErrorAction Stop).Source }
$PythonPath = (Resolve-Path -LiteralPath $PythonPath).Path
if ($root.Contains('"') -or $PythonPath.Contains('"')) { throw 'Unsupported quoted path' }
$planText = & $PythonPath $helper --plan
if ($LASTEXITCODE -ne 0) { throw 'Acceptance plan refused' }
$plan = $planText | ConvertFrom-Json
if ($plan.python_version -ne '3.12.10') { throw 'Pinned Python 3.12.10 required' }
$admin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator)

function Assert-FirewallPrerequisites {
    $profiles = @(Get-NetFirewallProfile -PolicyStore ActiveStore)
    if ($profiles.Count -ne 3 -or @($profiles | Where-Object { [int]$_.Enabled -ne 1 -or
            [int]$_.AllowLocalFirewallRules -eq 0 }).Count -ne 0) {
        throw 'All three effective firewall profiles must be enabled and permit local rules'
    }
    if ((Get-Service MpsSvc).Status -ne 'Running' -or (Get-Service Schedule).Status -ne 'Running') {
        throw 'Firewall and Task Scheduler services must be running'
    }
    $bypass = @(Get-NetFirewallRule -PolicyStore ActiveStore -Enabled True -Action Allow |
        Get-NetFirewallSecurityFilter | Where-Object { [int]$_.OverrideBlockRules -eq 1 })
    if ($bypass.Count -ne 0) { throw 'Authenticated firewall bypass rules require review' }
}

Assert-FirewallPrerequisites
if ($Mode -eq 'Preflight') {
    @{status='PREPARED-NOT-EXECUTED'; scope='L1-NONSCIENTIFIC'; elevation_required=(!$admin);
      source_sha256=$plan.source_sha256; launcher_sha256=$launcherHash;
      firewall_prerequisites='PASS'; os_isolated_acceptance='NOT_RUN'} | ConvertTo-Json -Compress
    exit 0
}
if (!$admin) { throw 'Start this reviewed script in an administrator PowerShell process' }
if (!$ExpectedSourceSha256 -or !$ExpectedLauncherSha256 -or
    $ExpectedSourceSha256.ToLowerInvariant() -ne $plan.source_sha256 -or
    $ExpectedLauncherSha256.ToLowerInvariant() -ne $launcherHash) { throw 'Reviewed source/launcher hashes required' }

# The OS releases this exclusive checkout-local lock on process exit.
$lockPath = Join-Path $root 'local/frontier/os-offline.lock'
$runLock = [IO.File]::Open($lockPath, [IO.FileMode]::OpenOrCreate, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None)

# Establish a working, zero-payload TCP baseline before modifying the firewall.
$baseline = & $PythonPath $helper --probe
if ($LASTEXITCODE -ne 0 -or !($baseline | ConvertFrom-Json).connected) {
    throw 'Connected baseline probe unavailable; do not claim firewall enforcement from a failed baseline'
}
$runId = [Guid]::NewGuid().ToString('N')
$group = 'CEML-L1Offline-' + $runId
$ruleNames = @($group + '-Inbound', $group + '-Outbound')
$taskName = $group + '-Restore'
$outputDir = Join-Path $root ('local/frontier/os-offline/' + $runId)
New-Item -ItemType Directory -Path $outputDir -ErrorAction Stop | Out-Null
$shell = Join-Path $env:SystemRoot 'System32/WindowsPowerShell/v1.0/powershell.exe'
$child = $null
$childExitCode = ''
$isolated = $false
$checksPassed = $false
$restored = $false
$watchdogRemoved = $false
$reconnected = $false
$passed = $false
$failureKind = ''
$stage = 'watchdog-registration'
$startedUtc = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')

function Assert-Isolation {
    Assert-FirewallPrerequisites
    foreach ($name in $ruleNames) {
        $rules = @(Get-NetFirewallRule -PolicyStore ActiveStore -Name $name -ErrorAction Stop)
        if ($rules.Count -ne 1) { throw 'Isolation rule missing or duplicated' }
        $rule = $rules[0]
        $direction = if ($name.EndsWith('-Inbound')) { 'Inbound' } else { 'Outbound' }
        if ([int]$rule.Enabled -ne 1 -or [string]$rule.Action -ne 'Block' -or
            [string]$rule.Direction -ne $direction -or [string]$rule.Profile -ne 'Any' -or
            $rule.Group -ne $group -or [string]$rule.PrimaryStatus -ne 'OK') {
            throw 'Effective isolation rule changed or is not enforced'
        }
        $app = $rule | Get-NetFirewallApplicationFilter
        $addr = $rule | Get-NetFirewallAddressFilter
        $port = $rule | Get-NetFirewallPortFilter
        if ([string]$app.Program -ne 'Any' -or [string]$addr.LocalAddress -ne 'Any' -or
            [string]$addr.RemoteAddress -ne 'Any' -or [string]$port.Protocol -ne 'Any') {
            throw 'Isolation rule scope narrowed'
        }
    }
}

try {
    # The watchdog is registered BEFORE any network change. It also runs at boot
    # after a reboot. Inline fixed UUID-only cleanup does not trust mutable files.
    # It enumerates the whole store with -ErrorAction Stop, so an empty result means
    # the rules are absent and never that the query failed. On any doubt it exits 1
    # and stays registered; the timed trigger repeats and the boot trigger remains.
    $cleanup = @"
`$ErrorActionPreference = 'Stop'
try {
    `$names = @('$($ruleNames[0])', '$($ruleNames[1])')
    `$found = @(Get-NetFirewallRule -PolicyStore PersistentStore -ErrorAction Stop | Where-Object { `$names -contains `$_.Name })
    if (`$found.Count -gt 0) { `$found | Remove-NetFirewallRule -ErrorAction Stop }
    `$left = @(Get-NetFirewallRule -PolicyStore PersistentStore -ErrorAction Stop | Where-Object { `$names -contains `$_.Name })
    if (`$left.Count -ne 0) { exit 1 }
    Unregister-ScheduledTask -TaskName '$taskName' -Confirm:`$false -ErrorAction Stop
    exit 0
} catch { exit 1 }
"@
    $encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($cleanup))
    $action = New-ScheduledTaskAction -Execute $shell -Argument ('-NoProfile -NonInteractive -EncodedCommand ' + $encoded)
    $timed = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(25) `
        -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Hours 12)
    $triggers = @($timed, (New-ScheduledTaskTrigger -AtStartup))
    $principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest
    $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
        -ExecutionTimeLimit (New-TimeSpan -Minutes 2) -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $triggers -Principal $principal -Settings $settings | Out-Null
    if (@(Get-ScheduledTask -TaskName $taskName).Count -ne 1) { throw 'Cleanup watchdog not registered' }
    $stage = 'rule-creation'
    New-NetFirewallRule -PolicyStore PersistentStore -Name $ruleNames[0] -DisplayName $ruleNames[0] `
        -Group $group -Enabled True -Profile Any -Direction Inbound -Action Block `
        -Program Any -Protocol Any -LocalAddress Any -RemoteAddress Any | Out-Null
    New-NetFirewallRule -PolicyStore PersistentStore -Name $ruleNames[1] -DisplayName $ruleNames[1] `
        -Group $group -Enabled True -Profile Any -Direction Outbound -Action Block `
        -Program Any -Protocol Any -LocalAddress Any -RemoteAddress Any | Out-Null
    $stage = 'isolation-verification'
    Assert-Isolation
    $stage = 'blocked-probe'
    $blockedProbe = & $PythonPath $helper --probe
    if ($LASTEXITCODE -ne 2 -or ($blockedProbe | ConvertFrom-Json).connected) { throw 'Network probe was not blocked' }
    $isolated = $true
    $stage = 'child-start'
    $arguments = '"' + $helper + '" --run --output-dir "' + $outputDir + '" --expected-source ' + $plan.source_sha256
    $child = Start-Process -FilePath $PythonPath -ArgumentList $arguments -WorkingDirectory $root -WindowStyle Hidden `
        -PassThru -RedirectStandardOutput (Join-Path $outputDir 'driver.stdout.log') `
        -RedirectStandardError (Join-Path $outputDir 'driver.stderr.log')
    # Hold the process handle now; otherwise the exit code can be unavailable later.
    $null = $child.Handle
    $stage = 'child-monitor'
    $deadline = [DateTime]::UtcNow.AddMinutes(20)
    while (!$child.HasExited) {
        if ([DateTime]::UtcNow -ge $deadline) { throw 'Acceptance exceeded 20-minute isolation budget' }
        Assert-Isolation
        Start-Sleep -Seconds 2
        $child.Refresh()
    }
    $child.WaitForExit()
    $childExitCode = [string]$child.ExitCode
    $stage = 'final-isolation-verification'
    Assert-Isolation
    $stage = 'final-blocked-probe'
    $blockedProbe = & $PythonPath $helper --probe
    if ($LASTEXITCODE -ne 2 -or ($blockedProbe | ConvertFrom-Json).connected) { throw 'Final network probe was not blocked' }
    $stage = 'child-exit-code'
    if ($childExitCode -ne '0') { throw 'Engineering child failed' }
    $stage = 'evidence-check'
    $checks = Get-Content -LiteralPath (Join-Path $outputDir 'checks.json') -Raw | ConvertFrom-Json
    if ($checks.status -ne 'ENGINEERING-CHECKS-PASS' -or $checks.source_sha256 -ne $plan.source_sha256) {
        throw 'Engineering evidence incomplete'
    }
    $stage = 'final-source-identity'
    $endPlan = & $PythonPath $helper --plan
    if ($LASTEXITCODE -ne 0 -or ($endPlan | ConvertFrom-Json).source_sha256 -ne $plan.source_sha256) {
        throw 'Final source identity changed'
    }
    $checksPassed = $true
    $stage = 'completed'
} catch {
    $failureKind = $_.Exception.GetType().Name
} finally {
    # Nothing in this block may prevent the rule removal that follows it.
    try {
        if ($null -ne $child -and !$child.HasExited) {
            Start-Process -FilePath (Join-Path $env:SystemRoot 'System32/taskkill.exe') `
                -ArgumentList @('/PID', [string]$child.Id, '/T', '/F') -WindowStyle Hidden -Wait
        }
    } catch { }
    try {
        # Whole-store enumeration with -ErrorAction Stop: a failed query throws and keeps
        # the watchdog. It can never be mistaken for "the rules are absent".
        $present = @(Get-NetFirewallRule -PolicyStore PersistentStore -ErrorAction Stop |
            Where-Object { $ruleNames -contains $_.Name })
        if ($present.Count -gt 0) { $present | Remove-NetFirewallRule -ErrorAction Stop }
        $remaining = @(Get-NetFirewallRule -PolicyStore PersistentStore -ErrorAction Stop |
            Where-Object { $ruleNames -contains $_.Name -or $_.Group -eq $group })
        $remaining += @(Get-NetFirewallRule -PolicyStore ActiveStore -ErrorAction Stop |
            Where-Object { $ruleNames -contains $_.Name -or $_.Group -eq $group })
        if ($remaining.Count -ne 0) { throw 'Isolation rules still present; watchdog retained' }
        $restored = $true
    } catch {
        $restored = $false
        $failureKind = 'CleanupFailed-WatchdogRetained'
    }
    # Restoration is observed, not assumed: the same zero-payload probe must connect again.
    if ($restored) {
        for ($attempt = 0; $attempt -lt 10 -and !$reconnected; $attempt++) {
            try {
                $null = & $PythonPath $helper --probe
                $reconnected = ($LASTEXITCODE -eq 0)
            } catch { }
            if (!$reconnected) { Start-Sleep -Seconds 3 }
        }
    }
    # The watchdog goes only after verified absence AND an observed reconnection.
    # Otherwise it stays, repeats, and removes itself once its own check succeeds.
    if ($restored -and $reconnected) {
        try {
            Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction Stop
            $watchdogRemoved = (@(Get-ScheduledTask -ErrorAction Stop |
                Where-Object { $_.TaskName -eq $taskName }).Count -eq 0)
        } catch { $watchdogRemoved = $false }
    }
    $passed = ($checksPassed -and $isolated -and $restored -and $watchdogRemoved -and $reconnected)
    $status = if ($passed) { 'OS-BLOCKED-ENGINEERING-CHECKS-PASS' } else { 'FAIL' }
    $record = @{schema='CEML-L1-OS-ISOLATION-2'; scope='L1-NONSCIENTIFIC'; status=$status;
        started_utc=$startedUtc; finished_utc=[DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ');
        source_sha256=$plan.source_sha256; launcher_sha256=$launcherHash;
        connected_baseline=$true; os_rules_verified=$isolated; rules_removed=$restored;
        watchdog_removed=$watchdogRemoved; connected_after_restore=$reconnected;
        checks_passed=$checksPassed; child_exit_code=$childExitCode; last_stage=$stage;
        failure_kind=$failureKind; scientific_execution='NOT_RUN';
        limitations='No power-loss guarantee; OS rules are observed, not a hardware network air gap'}
    $json = $record | ConvertTo-Json -Compress
    [IO.File]::WriteAllText((Join-Path $outputDir 'isolation.json'), $json, [Text.Encoding]::ASCII)
    Write-Output $json
    $runLock.Dispose()
}
if (!$passed) { exit 2 }
exit 0
