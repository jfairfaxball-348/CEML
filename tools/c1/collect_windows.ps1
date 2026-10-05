# Stage: hardware characterization. C1 observations only; no calibration.
[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
$AuditRun = 'c1-20261004-a'
$Records = New-Object 'System.Collections.Generic.List[object]'
$StatusText = [IO.File]::ReadAllText((Join-Path $RepoRoot 'PROGRAM_STATUS.md'))
if ($StatusText -notmatch 'Authoritative current phase:\*\* C1' -or
    $StatusText -notmatch 'Scientific execution authorization:\*\* DENIED') {
    throw 'C1 observation authorization is not established.'
}
if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) {
    throw 'This observation adapter requires Windows.'
}

function Add-Fact {
    param([string]$Id, [string]$Category, [string]$Name, $Value,
          [string]$Units, [string]$Method, [string]$Kind,
          [AllowNull()][string]$Uncertainty = $null)
    $Records.Add([ordered]@{
        record_class = 'OBSERVED_FACT'
        record_id = $Id
        category = $Category
        fact_name = $Name
        value = [ordered]@{ value = $Value; units = $Units }
        source_adapter = 'windows-minimized-v1'
        source_method = $Method
        audit_run_id = $AuditRun
        source_state_kind = $Kind
        uncertainty = $Uncertainty
        sanitization = @('Explicit property selection; no raw inventory persisted.',
                         'Paths and identifying provider metadata excluded.')
        observed_at = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ss.fffZ')
    })
}

function Add-Unavailable {
    param([string]$Id, [string]$Category, [string]$Item,
          [AllowNull()][string]$Method, [string]$Reason,
          [string[]]$Effects)
    # The frozen unavailable-record schema has no timestamp/audit-run fields.
    $Records.Add([ordered]@{
        record_class = 'UNAVAILABLE_OR_UNSUPPORTED'
        record_id = $Id
        category = $Category
        requested_item = $Item
        attempted_method = $Method
        reason = $Reason
        downstream_effects = @($Effects)
    })
}

function Convert-PermittedText {
    param($Text)
    if ($null -eq $Text) { throw 'Selected text is unavailable.' }
    $Result = ([string]$Text).Trim()
    # Model/release text is allowed, but unexpected paths, controls, address or
    # identifier forms fail closed before the intermediate artifact is written.
    if ($Result.Length -eq 0 -or $Result.Length -gt 256 -or
        $Result -match '[\x00-\x1f\x7f\\/]' -or
        $Result -match '(?i)[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' -or
        $Result -match '(?i)(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}' -or
        $Result -match '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}') {
        throw 'Selected text did not pass minimization.'
    }
    return $Result
}

function Convert-Quantity {
    param($Quantity)
    if ($null -eq $Quantity) { throw 'Selected quantity is unavailable.' }
    return ([UInt64]$Quantity).ToString([Globalization.CultureInfo]::InvariantCulture)
}

try {
    $OsProperties = @('Caption','Version','BuildNumber','OSArchitecture',
        'TotalVisibleMemorySize','FreePhysicalMemory','TotalVirtualMemorySize',
        'FreeVirtualMemory','SizeStoredInPagingFiles','FreeSpaceInPagingFiles')
    $Os = Get-CimInstance -ClassName Win32_OperatingSystem -Property $OsProperties |
        Select-Object -Property $OsProperties
    foreach ($Property in @('Caption','Version','BuildNumber','OSArchitecture')) {
        Add-Fact "obs.os.$Property" 'operating_system' $Property `
            (Convert-PermittedText $Os.$Property) 'text' `
            "CIM Win32_OperatingSystem selected $Property" 'active_configuration'
    }
    foreach ($Property in @('TotalVisibleMemorySize','FreePhysicalMemory',
        'TotalVirtualMemorySize','FreeVirtualMemory','SizeStoredInPagingFiles',
        'FreeSpaceInPagingFiles')) {
        $Kind = 'active_configuration'
        if ($Property -like 'Free*') { $Kind = 'momentary_state' }
        Add-Fact "obs.memory.$Property" 'memory' $Property `
            (Convert-Quantity $Os.$Property) 'KiB' `
            "CIM Win32_OperatingSystem selected $Property" $Kind `
            'Provider-reported value; virtual-memory fields are not physical RAM capacity.'
    }
} catch {
    Add-Unavailable 'unavailable.os.selected_fields' 'operating_system' `
        'Remaining selected operating-system or memory fields' `
        'CIM Win32_OperatingSystem selected properties' `
        'Selected-property query failed or returned an unusable value; raw error suppressed.' `
        @('Missing operating-system or memory facts must not be inferred.')
}

try {
    $CpuProperties = @('Manufacturer','Name','NumberOfCores',
                      'NumberOfLogicalProcessors','MaxClockSpeed')
    $Cpus = @(Get-CimInstance -ClassName Win32_Processor -Property $CpuProperties |
        Select-Object -Property $CpuProperties)
    if ($Cpus.Count -eq 0) { throw 'No selected processor fields returned.' }
    for ($Index = 0; $Index -lt $Cpus.Count; $Index++) {
        foreach ($Property in @('Manufacturer','Name')) {
            Add-Fact "obs.cpu.$Index.$Property" 'cpu' $Property `
                (Convert-PermittedText $Cpus[$Index].$Property) 'text' `
                "CIM Win32_Processor selected $Property; enumerated entry $Index" `
                'static_capability' 'Enumeration position is not a persistent processor identity.'
        }
        foreach ($Property in @('NumberOfCores','NumberOfLogicalProcessors','MaxClockSpeed')) {
            $Unit = 'count'
            if ($Property -eq 'MaxClockSpeed') { $Unit = 'MHz' }
            Add-Fact "obs.cpu.$Index.$Property" 'cpu' $Property `
                (Convert-Quantity $Cpus[$Index].$Property) $Unit `
                "CIM Win32_Processor selected $Property; enumerated entry $Index" `
                'static_capability' 'Provider-reported capability; does not establish active frequency, instruction use or topology.'
        }
    }
} catch {
    Add-Unavailable 'unavailable.cpu.selected_fields' 'cpu' 'Remaining selected CPU fields' `
        'CIM Win32_Processor selected properties' `
        'Selected-property query failed or returned an unusable value; raw error suppressed.' `
        @('CPU-dependent decisions requiring missing facts remain unsupported.')
}

try {
    $VolumeProperties = @('FileSystemType','DriveType','Size','SizeRemaining','AllocationUnitSize')
    $Volumes = @(Get-Volume -FilePath $RepoRoot | Select-Object -Property $VolumeProperties)
    if ($Volumes.Count -ne 1) { throw 'Target volume is not uniquely available.' }
    foreach ($Property in @('FileSystemType','DriveType')) {
        Add-Fact "obs.storage.$Property" 'checkpoint_storage' $Property `
            (Convert-PermittedText $Volumes[0].$Property) 'text' `
            "Get-Volume for repository checkpoint filesystem; selected $Property" `
            'active_configuration' 'Observed volume class alone does not establish CEML-CKPT-1 durability.'
    }
    foreach ($Property in @('Size','SizeRemaining','AllocationUnitSize')) {
        $Kind = 'active_configuration'
        if ($Property -eq 'SizeRemaining') { $Kind = 'momentary_state' }
        Add-Fact "obs.storage.$Property" 'checkpoint_storage' $Property `
            (Convert-Quantity $Volumes[0].$Property) 'bytes' `
            "Get-Volume for repository checkpoint filesystem; selected $Property" $Kind
    }
} catch {
    Add-Unavailable 'unavailable.storage.selected_fields' 'checkpoint_storage' `
        'Remaining target-volume fields' 'Get-Volume for repository checkpoint filesystem; selected properties' `
        'Selected target-volume query failed or was ambiguous; raw error suppressed.' `
        @('Storage safety or durability decisions requiring missing facts remain unsupported.')
}

try {
    if (-not ('CemlC1NarrowNative' -as [type])) {
        Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class CemlC1NarrowNative {
    [StructLayout(LayoutKind.Sequential)]
    public struct PowerState {
        public byte AcLineStatus;
        public byte BatteryFlag;
        public byte BatteryLifePercent;
        public byte SystemStatusFlag;
        public uint BatteryLifeTime;
        public uint BatteryFullLifeTime;
    }
    [DllImport("kernel32.dll", SetLastError=true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool GetSystemPowerStatus(out PowerState state);
    [DllImport("kernel32.dll", SetLastError=true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool GetPhysicallyInstalledSystemMemory(out ulong kib);
}
'@
    }
    $PowerState = New-Object 'CemlC1NarrowNative+PowerState'
    if ([CemlC1NarrowNative]::GetSystemPowerStatus([ref]$PowerState) -and
        $PowerState.AcLineStatus -in @(0,1)) {
        $PowerSource = 'battery'
        if ($PowerState.AcLineStatus -eq 1) { $PowerSource = 'AC' }
        Add-Fact 'obs.power.source' 'power' 'power_source' $PowerSource 'class' `
            'GetSystemPowerStatus; ACLineStatus only retained' 'momentary_state'
    } else {
        Add-Unavailable 'unavailable.power.source' 'power' 'Power-source state' `
            'GetSystemPowerStatus' 'The API did not return a known AC-line state.' `
            @('Uninterrupted power cannot be inferred.')
    }
    [UInt64]$InstalledKiB = 0
    if ([CemlC1NarrowNative]::GetPhysicallyInstalledSystemMemory([ref]$InstalledKiB) -and
        $InstalledKiB -gt 0) {
        Add-Fact 'obs.memory.physically_installed' 'memory' 'physically_installed_memory' `
            (Convert-Quantity $InstalledKiB) 'KiB' 'GetPhysicallyInstalledSystemMemory' `
            'static_capability' 'API-reported installed capacity, distinct from OS-visible or available memory.'
    } else {
        Add-Unavailable 'unavailable.memory.physically_installed' 'memory' `
            'Physically installed memory' 'GetPhysicallyInstalledSystemMemory' `
            'The API did not return a positive installed-memory quantity.' `
            @('Installed capacity must not be inferred from available memory.')
    }
} catch {
    Add-Unavailable 'unavailable.native.selected_apis' 'environment' `
        'Remaining selected power and installed-memory API observations' `
        'Narrow kernel32 API declarations' 'Selected API invocation unavailable; raw error suppressed.' `
        @('Unavailable power or memory facts must not be inferred.')
}

Add-Fact 'obs.memory.page_size' 'memory' 'system_page_size' `
    (Convert-Quantity ([Environment]::SystemPageSize)) 'bytes' `
    'System.Environment.SystemPageSize' 'static_capability'
Add-Fact 'obs.environment.process_bitness' 'environment' 'process_bitness' `
    (Convert-Quantity ([IntPtr]::Size * 8)) 'bits' 'System.IntPtr.Size' 'active_configuration'

foreach ($Setting in @(
    @{ Alias='STANDBYIDLE'; Name='standby' },
    @{ Alias='HIBERNATEIDLE'; Name='hibernate' }
)) {
    try {
        # The native output, including policy identifiers, exists only in memory.
        $PowerOutput = @(& powercfg.exe -query SCHEME_CURRENT SUB_SLEEP $Setting.Alias 2>$null)
        if ($LASTEXITCODE -ne 0) { throw 'Power-policy query failed.' }
        foreach ($Supply in @('AC','DC')) {
            $MatchesFound = @($PowerOutput | Select-String -Pattern `
                ("(?i)^\s*Current " + $Supply + " Power Setting Index:\s*0x([0-9a-f]+)\s*$"))
            if ($MatchesFound.Count -ne 1) { throw 'Localized or ambiguous power-policy output.' }
            $Seconds = [Convert]::ToUInt64($MatchesFound[0].Matches[0].Groups[1].Value, 16)
            Add-Fact "obs.power.$($Setting.Name).$Supply" 'power' `
                "$($Setting.Name)_$($Supply.ToLowerInvariant())_timeout" `
                (Convert-Quantity $Seconds) 'seconds' `
                "powercfg query current sleep policy $($Setting.Alias); normalized $Supply index only" `
                'active_configuration' 'Zero means no idle timeout for this setting; other sleep triggers and power-loss risk are not assessed.'
        }
        $PowerOutput = $null
    } catch {
        $PowerOutput = $null
        Add-Unavailable "unavailable.power.$($Setting.Name)" 'power' `
            "$($Setting.Name) AC/DC idle timeouts" `
            "powercfg query current sleep policy $($Setting.Alias); normalized indices only" `
            'Query failed or expected unambiguous English index labels were unavailable; raw output and errors suppressed.' `
            @('Safe power/sleep preconditions requiring these settings remain unestablished.')
    }
}

try {
    $PerfProperties = @('AvailableBytes','PagesInputPersec','PagesOutputPersec','PageReadsPersec')
    $MemorySample = Get-CimInstance -ClassName Win32_PerfFormattedData_PerfOS_Memory `
        -Property $PerfProperties | Select-Object -Property $PerfProperties
    foreach ($Property in $PerfProperties) {
        $Units = 'pages_per_second'
        if ($Property -eq 'AvailableBytes') { $Units = 'bytes' }
        if ($Property -eq 'PageReadsPersec') { $Units = 'read_operations_per_second' }
        Add-Fact "obs.memory.performance.$Property" 'memory' $Property `
            (Convert-Quantity $MemorySample.$Property) $Units `
            "CIM Win32_PerfFormattedData_PerfOS_Memory selected $Property" `
            'momentary_state' 'Single provider-formatted sample; paging includes file-backed activity and does not establish sustained swap pressure.'
    }
} catch {
    Add-Unavailable 'unavailable.memory.performance' 'memory' 'Selected current memory performance counters' `
        'CIM Win32_PerfFormattedData_PerfOS_Memory selected properties' `
        'Selected counters unavailable or unusable; raw error suppressed.' `
        @('Sustained memory-pressure conclusions are unsupported.')
}

try {
    $Temperatures = @(Get-CimInstance -Namespace root/wmi -ClassName MSAcpi_ThermalZoneTemperature `
        -Property CurrentTemperature | Select-Object -ExpandProperty CurrentTemperature)
    if ($Temperatures.Count -eq 0) { throw 'No selected temperature values.' }
    for ($Index = 0; $Index -lt $Temperatures.Count; $Index++) {
        if ($null -eq $Temperatures[$Index] -or [UInt64]$Temperatures[$Index] -eq 0) {
            throw 'No usable selected temperature.'
        }
        Add-Fact "obs.thermal.$Index" 'thermal' 'acpi_zone_temperature' `
            (Convert-Quantity $Temperatures[$Index]) 'tenths_kelvin' `
            "CIM MSAcpi_ThermalZoneTemperature selected CurrentTemperature; enumerated entry $Index" `
            'momentary_state' 'ACPI zone value; sensor identity omitted and CPU package attribution not inferred.'
    }
} catch {
    Add-Unavailable 'unavailable.thermal.temperature' 'thermal' 'Remaining selected ACPI temperature values' `
        'CIM MSAcpi_ThermalZoneTemperature selected CurrentTemperature' `
        'Temperature query unavailable, denied or unusable; raw error suppressed.' `
        @('Temperature-based safety conclusions require another authorized observation source.')
}

foreach ($Entry in @(
    @('instruction_features','cpu','Instruction-set features','Feature-dependent selection requires a C1 feature helper.'),
    @('cache','cpu','Cache hierarchy and capacities','Cache tuning is unsupported.'),
    @('topology','cpu','NUMA and processor topology','Topology-specific affinity or memory tuning is unsupported.'),
    @('virtualization','environment','Virtualization status','No bare-metal or virtualized-environment conclusion is permitted.'),
    @('device_class','checkpoint_storage','Physical storage device class','Drive technology cannot be inferred from volume class.'),
    @('throttling','thermal','Throttling and active CPU frequency','No throttling or sustained-frequency conclusion is permitted.')
)) {
    Add-Unavailable "unavailable.$($Entry[0])" $Entry[1] $Entry[2] $null `
        'Not probed by this narrow observation adapter; no inference from model text.' @($Entry[3])
}

$OutputDirectory = Join-Path $RepoRoot 'local\c1'
[IO.Directory]::CreateDirectory($OutputDirectory) | Out-Null
$OutputFile = Join-Path $OutputDirectory 'audit_observations.json'
$Json = ConvertTo-Json -InputObject @($Records.ToArray()) -Depth 12
[IO.File]::WriteAllText($OutputFile, $Json + [Environment]::NewLine,
    (New-Object Text.UTF8Encoding($false)))
[ordered]@{
    stage = 'hardware characterization'
    audit_run_id = $AuditRun
    logical_output = 'local/c1/audit_observations.json'
    observed_records = @($Records | Where-Object record_class -eq 'OBSERVED_FACT').Count
    unavailable_records = @($Records | Where-Object record_class -eq 'UNAVAILABLE_OR_UNSUPPORTED').Count
    frozen_report = $false
} | ConvertTo-Json -Compress
