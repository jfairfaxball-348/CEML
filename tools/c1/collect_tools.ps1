# Stage: hardware characterization. No installs, environment activation or builds.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
try {
    $statusText = [IO.File]::ReadAllText((Join-Path $root 'PROGRAM_STATUS.md'))
    if ($statusText -notmatch 'Authoritative current phase:\*\* C1' -or
        $statusText -notmatch 'Scientific execution authorization:\*\* DENIED' -or
        -not (Test-Path -LiteralPath (Join-Path $root 'docs/C1_RESOURCE_CEILINGS.md'))) {
        throw 'Authorization precondition failed.'
    }
} catch {
    throw 'C1 authorization and prior resource ceilings must be established; raw diagnostic suppressed.'
}
$records = [System.Collections.Generic.List[object]]::new()
function Observed($id, $name, $value, $method, $note) {
    $records.Add([ordered]@{
        record_class='OBSERVED_FACT'; record_id=$id; category='toolchain'; fact_name=$name
        value=$value; source_adapter='windows-narrow-tool-discovery'; source_method=$method
        audit_run_id='c1-20261004-a'; source_state_kind='active_configuration'
        uncertainty=$note; sanitization=@('Only selected versions, counts and availability are emitted; locator paths omitted')
        observed_at=[DateTime]::UtcNow.ToString('o')
    })
}
function Unavailable($id, $item, $method, $reason) {
    $records.Add([ordered]@{
        record_class='UNAVAILABLE_OR_UNSUPPORTED'; record_id=$id; category='toolchain'
        requested_item=$item; attempted_method=$method; reason=$reason
        downstream_effects=@('Decisions requiring this fact remain unsupported; no production stack is selected by this adapter')
    })
}
$availability = [ordered]@{}
$applications = @{}
foreach ($name in @('python','gcc','g++','clang','clang++','cl','rustc','cargo','cmake','ninja','pkg-config')) {
    $recordName = $name.Replace('++','pp')
    try {
        $application = Get-Command -Name $name -CommandType Application -ErrorAction Stop |
            Select-Object -First 1
        if ($null -eq $application -or [string]::IsNullOrWhiteSpace($application.Path)) {
            throw 'No application path returned.'
        }
        # Application locators stay in memory; aliases/functions cannot be invoked.
        $applications[$name] = $application.Path
        $availability[$name] = $true
    } catch {
        $availability[$name] = $false
        Unavailable ('tools.command.'+$recordName) ($name+' command-search availability and version') `
            'Get-Command Application for the named candidate; locators withheld' `
            'Application was not resolved or the lookup was unavailable; alternate installation locations are not excluded.'
    }
}
Observed 'tools.path' 'candidate_command_availability' $availability 'Get-Command for named I1 candidates only' 'Absence from command search does not prove absence from the machine'
# Rustup is prohibited from acquiring a toolchain during a version query.
$priorAutoInstall = $env:RUSTUP_AUTO_INSTALL
$priorOffline = $env:RUSTUP_OFFLINE
try {
    $env:RUSTUP_AUTO_INSTALL='0'
    $env:RUSTUP_OFFLINE='1'
    foreach ($name in @('rustc','cargo','python')) {
        if (-not $availability[$name]) { continue }
        try {
            $applicationPath = $applications[$name]
            if ($applicationPath -notmatch '^[A-Za-z]:[\\/]' -or
                $applicationPath -match '(?i)[\\/]Microsoft[\\/]WindowsApps[\\/]') {
                throw 'Remote or application-store alias execution is not admitted.'
            }
            $lines = @(& $applicationPath --version 2>$null)
            if ($LASTEXITCODE -ne 0 -or $lines.Count -ne 1 -or
                $lines[0] -notmatch '^[A-Za-z0-9 .()_-]+$') {
                throw 'Version output did not meet the minimized grammar.'
            }
            Observed ('tools.'+$name) ($name+'_version') $lines[0] `
                'Resolved Application version query; automatic toolchain acquisition disabled' `
                'Version availability is not an offline rebuild proof'
        } catch {
            Unavailable ('tools.'+$name) ($name+' version') 'Resolved Application version query; raw output withheld' `
                'Version query failed, the locator was not admitted, or output was outside minimized grammar; raw diagnostic suppressed.'
        }
    }
    if ($availability['rustc']) {
        try {
            $applicationPath = $applications['rustc']
            if ($applicationPath -notmatch '^[A-Za-z]:[\\/]') { throw 'Nonlocal application locator.' }
            $lines = @(& $applicationPath --version --verbose 2>$null)
            $nativeExit = $LASTEXITCODE
            $hostLine = @($lines | Where-Object { $_ -match '^host: [A-Za-z0-9_-]+$' })
            if ($nativeExit -ne 0 -or $hostLine.Count -ne 1) { throw 'No unique host field.' }
            Observed 'tools.rust-target' 'rust_target' ($hostLine[0].Substring(6)) `
                'Resolved rustc verbose version; host field only' 'No production candidate compiled'
        } catch {
            Unavailable 'tools.rust-target' 'Rust host target' 'Resolved rustc verbose version; host field only' `
                'Query failed or a unique permitted host field was unavailable; raw diagnostic suppressed.'
        }
    }
} finally {
    # These are process-local query safeguards, not environment activation.
    $env:RUSTUP_AUTO_INSTALL = $priorAutoInstall
    $env:RUSTUP_OFFLINE = $priorOffline
}
$cacheCounts = [ordered]@{}
foreach ($family in @('rug-*','gmp-mpfr-sys-*')) {
    try {
        $cacheRoot = if ($env:CARGO_HOME) { $env:CARGO_HOME } else { Join-Path $env:USERPROFILE '.cargo' }
        if ($cacheRoot -notmatch '^[A-Za-z]:[\\/]') { throw 'Nonlocal cache locator.' }
        $count = 0
        foreach ($area in @('registry/cache','registry/src')) {
            $base = Join-Path $cacheRoot $area
            if (Test-Path -LiteralPath $base) {
                foreach ($registry in (Get-ChildItem -LiteralPath $base -Directory)) {
                    $count += @(Get-ChildItem -LiteralPath $registry.FullName -Filter $family).Count
                }
            }
        }
        $cacheCounts[$family] = [string]$count
    } catch {
        $cacheCounts[$family] = $null
        Unavailable ('tools.cache.'+$family.Replace('-*','')) ($family+' cache entry count') `
            'Named candidate entries in configured/default Cargo source/package cache only' `
            'Cache observation failed or its locator was not admitted; raw diagnostic suppressed and count is unknown.'
    }
}
Observed 'tools.rug-cache' 'candidate_cache_entry_counts' $cacheCounts 'Named rug and gmp-mpfr-sys entries in configured/default Cargo registry source/package caches' 'No unrelated package names or cache paths collected; alternate caches not excluded; null means unavailable, not zero'
try {
    $vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio/Installer/vswhere.exe'
    if (-not (Test-Path -LiteralPath $vswhere)) { throw 'Component locator unavailable.' }
    $installs = @(& $vswhere -latest -products '*' -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath 2>$null)
    if ($LASTEXITCODE -ne 0 -or $installs.Count -ne 1 -or $installs[0] -notmatch '^[A-Za-z]:[\\/]') {
        throw 'No unique local installation locator.'
    }
    $install = $installs[0]
    $versionFile = Join-Path $install 'VC/Auxiliary/Build/Microsoft.VCToolsVersion.default.txt'
    $version = (Get-Content -LiteralPath $versionFile -Raw).Trim()
    if ($version -notmatch '^\d+\.\d+\.\d+$') { throw 'Unrecognized compiler directory version.' }
    foreach ($name in @('cl.exe','link.exe')) {
        try {
            $compilerRoot = Join-Path $install ('VC/Tools/MSVC/'+$version)
            $exe = Join-Path $compilerRoot ('bin/Hostx64/x64/'+$name)
            if (-not (Test-Path -LiteralPath $exe)) { throw 'Selected executable absent.' }
            $v = (Get-Item -LiteralPath $exe).VersionInfo
            if ($null -eq $v) { throw 'Selected executable version absent.' }
            $parts = [ordered]@{major=[string]$v.FileMajorPart; minor=[string]$v.FileMinorPart; build=[string]$v.FileBuildPart; revision=[string]$v.FilePrivatePart}
            foreach ($part in $parts.Values) {
                if ($part -notmatch '^(0|[1-9][0-9]*)$') { throw 'Noncanonical version component.' }
            }
            Observed ('tools.msvc.'+$name) ($name+'_file_version') $parts `
                'Selected executable file-version fields located using the Visual C++ component query' `
                'Toolchain environment not activated; executable metadata does not establish successful compilation, linking or offline rebuild'
        } catch {
            Unavailable ('tools.msvc.'+$name) ($name+' file version') `
                'Visual C++ component query and selected executable file-version fields' `
                'Selected executable metadata was absent or unavailable; raw diagnostic suppressed.'
        }
    }
} catch {
    Unavailable 'tools.msvc.discovery' 'Visual C++ compiler and linker file versions' `
        'Component-specific locator query and selected version-file fields' `
        'Component discovery was absent, failed or ambiguous; raw locator output and diagnostic suppressed.'
}
foreach ($name in @('gcc','g++','clang','clang++','cl','cmake','ninja','pkg-config')) {
    if ($availability[$name]) {
        Unavailable ('tools.version-unprobed.'+$name.Replace('++','pp')) ($name+' invoked version') `
            'Command-search availability only; invocation not attempted by this minimal adapter' `
            'Presence alone is insufficient for candidate selection; exact version and offline provenance require a later explicit candidate probe.'
    }
}
$headers = [ordered]@{}
try {
    $systemRoot = $env:SystemDrive + [IO.Path]::DirectorySeparatorChar
    $locations = @(
        @('msys2-ucrt64',(Join-Path $systemRoot 'msys64/ucrt64/include/gmp.h')),
        @('msys2-mingw64',(Join-Path $systemRoot 'msys64/mingw64/include/gmp.h')),
        @('mingw',(Join-Path $systemRoot 'MinGW/include/gmp.h')),
        @('vcpkg-standard',(Join-Path $systemRoot 'vcpkg/installed/x64-windows/include/gmp.h'))
    )
    # Locators are constructed in memory, never included in observation records.
    if ($env:VCPKG_ROOT) { $locations += ,@('vcpkg-configured',(Join-Path $env:VCPKG_ROOT 'installed/x64-windows/include/gmp.h')) }
    foreach ($location in $locations) {
        try {
            if ($location[1] -notmatch '^[A-Za-z]:[\\/]') { throw 'Nonlocal locator.' }
            $headers[$location[0]] = [bool](Test-Path -LiteralPath $location[1])
        } catch {
            $headers[$location[0]] = $null
            Unavailable ('tools.gmp-locator.'+$location[0]) ($location[0]+' GMP header availability') `
                'Named development-package header locator only' `
                'Locator unavailable or not admitted; raw diagnostic suppressed and availability is unknown.'
        }
    }
} catch {
    Unavailable 'tools.gmp-locator-construction' 'Named GMP header locator availability' `
        'Construction of narrow standard/configured development-package locators' `
        'Required locator configuration unavailable; raw diagnostic suppressed.'
}
Observed 'tools.gmp-locators' 'gmp_header_at_narrow_candidate_locations' $headers 'Existence probes for named development-package header locators only' 'Not a whole-machine search; headers alone would not establish library compatibility or provenance'
if (-not ($headers.Values -contains $true) -and $cacheCounts['rug-*'] -eq '0' -and $cacheCounts['gmp-mpfr-sys-*'] -eq '0') {
    Unavailable 'tools.gmp-unavailable' 'I1-eligible GMP development package and offline source/package inputs' 'Named development-package header locators and Cargo candidate cache probes' 'No usable package established within the checked scope; no download, installation, replacement or activation authorized'
}
Unavailable 'tools.flint-unavailable' 'Optional public FLINT backend' 'Not probed beyond prerequisite assessment' 'A usable GMP-backed production prerequisite is not established by locator probes; optional FLINT candidate not activated or measured'
try {
    $out = Join-Path $root 'local/c1'
    [IO.Directory]::CreateDirectory($out) | Out-Null
    [IO.File]::WriteAllText((Join-Path $out 'tool_observations.json'),(ConvertTo-Json -InputObject @($records.ToArray()) -Depth 12),[Text.UTF8Encoding]::new($false))
} catch {
    throw 'Sanitized observation output could not be written; raw diagnostic suppressed.'
}
[ordered]@{
    stage='hardware characterization'
    audit_run_id='c1-20261004-a'
    logical_output='local/c1/tool_observations.json'
    observed_records=@($records | Where-Object record_class -eq 'OBSERVED_FACT').Count
    unavailable_records=@($records | Where-Object record_class -eq 'UNAVAILABLE_OR_UNSUPPORTED').Count
    frozen_report=$false
} | ConvertTo-Json -Compress
