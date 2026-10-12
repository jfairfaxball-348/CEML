param(
    [Parameter(Mandatory=$true)][ValidateSet('Start','Stop')][string]$Action,
    [string]$Python
)
$ErrorActionPreference = 'Stop'
$taskName = 'CEML Live Publisher'
if ($Action -eq 'Stop') {
    if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
        Disable-ScheduledTask -TaskName $taskName | Out-Null
    }
    exit 0
}
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
$pythonWindowless = Join-Path (Split-Path -Parent $Python) 'pythonw.exe'
if (-not (Test-Path -LiteralPath $pythonWindowless)) { throw 'pythonw.exe is required for the hidden publisher' }
$publisher = Join-Path $PSScriptRoot 'live.py'
$identity = [Security.Principal.WindowsIdentity]::GetCurrent().Name
$taskAction = New-ScheduledTaskAction -Execute $pythonWindowless -Argument ('"' + $publisher + '" watch') -WorkingDirectory $root
$logon = New-ScheduledTaskTrigger -AtLogOn -User $identity
$recovery = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 1)
$principal = New-ScheduledTaskPrincipal -UserId $identity -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -Hidden -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew -ExecutionTimeLimit ([TimeSpan]::Zero) -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1)
Register-ScheduledTask -TaskName $taskName -Action $taskAction -Trigger @($logon,$recovery) -Principal $principal -Settings $settings -Description 'Optional CEML informational live status publisher. Never executes or controls scientific verification.' -Force | Out-Null
Start-ScheduledTask -TaskName $taskName
