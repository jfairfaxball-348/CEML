# Owner-authorised continuous scheduling: change only the existing timeout.
# This configures scheduling and never starts or stops scientific execution.
$ErrorActionPreference = 'Stop'
$cemlContinuousTask = Get-ScheduledTask -TaskName 'CEML Frontier Verification'
if ([string]$cemlContinuousTask.State -eq 'Running') {
    throw 'Wait for a clean scientific stop before changing task settings.'
}
if ($cemlContinuousTask.Actions.Count -ne 1 -or
    $cemlContinuousTask.Actions[0].Execute -ne 'powershell.exe' -or
    $cemlContinuousTask.Actions[0].Arguments -notmatch [regex]::Escape('C:\CEML\local\frontier\run-operator-task.ps1')) {
    throw 'Unexpected scheduled launcher action; inspect before changing settings.'
}
$cemlContinuousTask.Settings.ExecutionTimeLimit = 'PT0S'
Set-ScheduledTask -TaskName 'CEML Frontier Verification' -Settings $cemlContinuousTask.Settings | Out-Null
$cemlContinuousSettings = (Get-ScheduledTask -TaskName 'CEML Frontier Verification').Settings
if ($cemlContinuousSettings.ExecutionTimeLimit -ne 'PT0S') { throw 'Task timeout change did not persist.' }
Write-Output 'Scheduled launcher has no execution time limit. No scientific run started.'
