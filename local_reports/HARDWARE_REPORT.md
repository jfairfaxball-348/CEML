# C1 sanitized hardware report

Stage: **hardware characterization**. **CEML-C1 REMAINS OPEN.**

Audit: `c1-20261005-post-setup`. Generated: 2026-10-05T12:35:30Z.

JSON artifact digest: `d7001003eefba09adb0db63cd012b9d0a8cca4d5f515540abb4406c233ee27cb`.

Generated mechanically from HARDWARE_REPORT.json. Observations are not benchmarks.
No production build/profile or checkpoint durability acceptance is implied.

## obs.os.Caption

Class: `OBSERVED_FACT`.

Caption: `{"units":"text","value":"Microsoft Windows 11 Home"}`

Source: CIM Win32_OperatingSystem selected Caption.

Observation kind: active_configuration. Time: 2026-10-05T12:16:13.802Z.

Uncertainty: No additional uncertainty recorded.

## obs.os.Version

Class: `OBSERVED_FACT`.

Version: `{"units":"text","value":"10.0.26200"}`

Source: CIM Win32_OperatingSystem selected Version.

Observation kind: active_configuration. Time: 2026-10-05T12:16:13.806Z.

Uncertainty: No additional uncertainty recorded.

## obs.os.BuildNumber

Class: `OBSERVED_FACT`.

BuildNumber: `{"units":"text","value":"26200"}`

Source: CIM Win32_OperatingSystem selected BuildNumber.

Observation kind: active_configuration. Time: 2026-10-05T12:16:13.807Z.

Uncertainty: No additional uncertainty recorded.

## obs.os.OSArchitecture

Class: `OBSERVED_FACT`.

OSArchitecture: `{"units":"text","value":"64-bit"}`

Source: CIM Win32_OperatingSystem selected OSArchitecture.

Observation kind: active_configuration. Time: 2026-10-05T12:16:13.808Z.

Uncertainty: No additional uncertainty recorded.

## obs.memory.TotalVisibleMemorySize

Class: `OBSERVED_FACT`.

TotalVisibleMemorySize: `{"units":"KiB","value":"16471564"}`

Source: CIM Win32_OperatingSystem selected TotalVisibleMemorySize.

Observation kind: active_configuration. Time: 2026-10-05T12:16:13.813Z.

Uncertainty: Provider-reported value; virtual-memory fields are not physical RAM capacity.

## obs.memory.FreePhysicalMemory

Class: `OBSERVED_FACT`.

FreePhysicalMemory: `{"units":"KiB","value":"6772324"}`

Source: CIM Win32_OperatingSystem selected FreePhysicalMemory.

Observation kind: momentary_state. Time: 2026-10-05T12:16:13.814Z.

Uncertainty: Provider-reported value; virtual-memory fields are not physical RAM capacity.

## obs.memory.TotalVirtualMemorySize

Class: `OBSERVED_FACT`.

TotalVirtualMemorySize: `{"units":"KiB","value":"17585676"}`

Source: CIM Win32_OperatingSystem selected TotalVirtualMemorySize.

Observation kind: active_configuration. Time: 2026-10-05T12:16:13.815Z.

Uncertainty: Provider-reported value; virtual-memory fields are not physical RAM capacity.

## obs.memory.FreeVirtualMemory

Class: `OBSERVED_FACT`.

FreeVirtualMemory: `{"units":"KiB","value":"7190996"}`

Source: CIM Win32_OperatingSystem selected FreeVirtualMemory.

Observation kind: momentary_state. Time: 2026-10-05T12:16:13.816Z.

Uncertainty: Provider-reported value; virtual-memory fields are not physical RAM capacity.

## obs.memory.SizeStoredInPagingFiles

Class: `OBSERVED_FACT`.

SizeStoredInPagingFiles: `{"units":"KiB","value":"1114112"}`

Source: CIM Win32_OperatingSystem selected SizeStoredInPagingFiles.

Observation kind: active_configuration. Time: 2026-10-05T12:16:13.817Z.

Uncertainty: Provider-reported value; virtual-memory fields are not physical RAM capacity.

## obs.memory.FreeSpaceInPagingFiles

Class: `OBSERVED_FACT`.

FreeSpaceInPagingFiles: `{"units":"KiB","value":"1055856"}`

Source: CIM Win32_OperatingSystem selected FreeSpaceInPagingFiles.

Observation kind: momentary_state. Time: 2026-10-05T12:16:13.818Z.

Uncertainty: Provider-reported value; virtual-memory fields are not physical RAM capacity.

## obs.cpu.0.Manufacturer

Class: `OBSERVED_FACT`.

Manufacturer: `{"units":"text","value":"GenuineIntel"}`

Source: CIM Win32_Processor selected Manufacturer; enumerated entry 0.

Observation kind: static_capability. Time: 2026-10-05T12:16:13.833Z.

Uncertainty: Enumeration position is not a persistent processor identity.

## obs.cpu.0.Name

Class: `OBSERVED_FACT`.

Name: `{"units":"text","value":"11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz"}`

Source: CIM Win32_Processor selected Name; enumerated entry 0.

Observation kind: static_capability. Time: 2026-10-05T12:16:13.834Z.

Uncertainty: Enumeration position is not a persistent processor identity.

## obs.cpu.0.NumberOfCores

Class: `OBSERVED_FACT`.

NumberOfCores: `{"units":"count","value":"8"}`

Source: CIM Win32_Processor selected NumberOfCores; enumerated entry 0.

Observation kind: static_capability. Time: 2026-10-05T12:16:13.837Z.

Uncertainty: Provider-reported capability; does not establish active frequency, instruction use or topology.

## obs.cpu.0.NumberOfLogicalProcessors

Class: `OBSERVED_FACT`.

NumberOfLogicalProcessors: `{"units":"count","value":"16"}`

Source: CIM Win32_Processor selected NumberOfLogicalProcessors; enumerated entry 0.

Observation kind: static_capability. Time: 2026-10-05T12:16:13.838Z.

Uncertainty: Provider-reported capability; does not establish active frequency, instruction use or topology.

## obs.cpu.0.MaxClockSpeed

Class: `OBSERVED_FACT`.

MaxClockSpeed: `{"units":"MHz","value":"2304"}`

Source: CIM Win32_Processor selected MaxClockSpeed; enumerated entry 0.

Observation kind: static_capability. Time: 2026-10-05T12:16:13.839Z.

Uncertainty: Provider-reported capability; does not establish active frequency, instruction use or topology.

## obs.storage.FileSystemType

Class: `OBSERVED_FACT`.

FileSystemType: `{"units":"text","value":"NTFS"}`

Source: Get-Volume for repository checkpoint filesystem; selected FileSystemType.

Observation kind: active_configuration. Time: 2026-10-05T12:16:16.461Z.

Uncertainty: Observed volume class alone does not establish CEML-CKPT-1 durability.

## obs.storage.DriveType

Class: `OBSERVED_FACT`.

DriveType: `{"units":"text","value":"Fixed"}`

Source: Get-Volume for repository checkpoint filesystem; selected DriveType.

Observation kind: active_configuration. Time: 2026-10-05T12:16:16.463Z.

Uncertainty: Observed volume class alone does not establish CEML-CKPT-1 durability.

## obs.storage.Size

Class: `OBSERVED_FACT`.

Size: `{"units":"bytes","value":"999785754624"}`

Source: Get-Volume for repository checkpoint filesystem; selected Size.

Observation kind: active_configuration. Time: 2026-10-05T12:16:16.464Z.

Uncertainty: No additional uncertainty recorded.

## obs.storage.SizeRemaining

Class: `OBSERVED_FACT`.

SizeRemaining: `{"units":"bytes","value":"209086918656"}`

Source: Get-Volume for repository checkpoint filesystem; selected SizeRemaining.

Observation kind: momentary_state. Time: 2026-10-05T12:16:16.465Z.

Uncertainty: No additional uncertainty recorded.

## obs.storage.AllocationUnitSize

Class: `OBSERVED_FACT`.

AllocationUnitSize: `{"units":"bytes","value":"4096"}`

Source: Get-Volume for repository checkpoint filesystem; selected AllocationUnitSize.

Observation kind: active_configuration. Time: 2026-10-05T12:16:16.466Z.

Uncertainty: No additional uncertainty recorded.

## obs.power.source

Class: `OBSERVED_FACT`.

power_source: `{"units":"class","value":"AC"}`

Source: GetSystemPowerStatus; ACLineStatus only retained.

Observation kind: momentary_state. Time: 2026-10-05T12:16:16.813Z.

Uncertainty: No additional uncertainty recorded.

## obs.memory.physically_installed

Class: `OBSERVED_FACT`.

physically_installed_memory: `{"units":"KiB","value":"16777216"}`

Source: GetPhysicallyInstalledSystemMemory.

Observation kind: static_capability. Time: 2026-10-05T12:16:16.816Z.

Uncertainty: API-reported installed capacity, distinct from OS-visible or available memory.

## obs.memory.page_size

Class: `OBSERVED_FACT`.

system_page_size: `{"units":"bytes","value":"4096"}`

Source: System.Environment.SystemPageSize.

Observation kind: static_capability. Time: 2026-10-05T12:16:16.817Z.

Uncertainty: No additional uncertainty recorded.

## obs.environment.process_bitness

Class: `OBSERVED_FACT`.

process_bitness: `{"units":"bits","value":"64"}`

Source: System.IntPtr.Size.

Observation kind: active_configuration. Time: 2026-10-05T12:16:16.818Z.

Uncertainty: No additional uncertainty recorded.

## obs.power.standby.AC

Class: `OBSERVED_FACT`.

standby_ac_timeout: `{"units":"seconds","value":"0"}`

Source: powercfg query current sleep policy STANDBYIDLE; normalized AC index only.

Observation kind: active_configuration. Time: 2026-10-05T12:16:16.856Z.

Uncertainty: Zero means no idle timeout for this setting; other sleep triggers and power-loss risk are not assessed.

## obs.power.standby.DC

Class: `OBSERVED_FACT`.

standby_dc_timeout: `{"units":"seconds","value":"0"}`

Source: powercfg query current sleep policy STANDBYIDLE; normalized DC index only.

Observation kind: active_configuration. Time: 2026-10-05T12:16:16.857Z.

Uncertainty: Zero means no idle timeout for this setting; other sleep triggers and power-loss risk are not assessed.

## obs.power.hibernate.AC

Class: `OBSERVED_FACT`.

hibernate_ac_timeout: `{"units":"seconds","value":"0"}`

Source: powercfg query current sleep policy HIBERNATEIDLE; normalized AC index only.

Observation kind: active_configuration. Time: 2026-10-05T12:16:16.877Z.

Uncertainty: Zero means no idle timeout for this setting; other sleep triggers and power-loss risk are not assessed.

## obs.power.hibernate.DC

Class: `OBSERVED_FACT`.

hibernate_dc_timeout: `{"units":"seconds","value":"0"}`

Source: powercfg query current sleep policy HIBERNATEIDLE; normalized DC index only.

Observation kind: active_configuration. Time: 2026-10-05T12:16:16.877Z.

Uncertainty: Zero means no idle timeout for this setting; other sleep triggers and power-loss risk are not assessed.

## obs.memory.performance.AvailableBytes

Class: `OBSERVED_FACT`.

AvailableBytes: `{"units":"bytes","value":"6775320576"}`

Source: CIM Win32_PerfFormattedData_PerfOS_Memory selected AvailableBytes.

Observation kind: momentary_state. Time: 2026-10-05T12:16:22.616Z.

Uncertainty: Single provider-formatted sample; paging includes file-backed activity and does not establish sustained swap pressure.

## obs.memory.performance.PagesInputPersec

Class: `OBSERVED_FACT`.

PagesInputPersec: `{"units":"pages_per_second","value":"0"}`

Source: CIM Win32_PerfFormattedData_PerfOS_Memory selected PagesInputPersec.

Observation kind: momentary_state. Time: 2026-10-05T12:16:22.617Z.

Uncertainty: Single provider-formatted sample; paging includes file-backed activity and does not establish sustained swap pressure.

## obs.memory.performance.PagesOutputPersec

Class: `OBSERVED_FACT`.

PagesOutputPersec: `{"units":"pages_per_second","value":"0"}`

Source: CIM Win32_PerfFormattedData_PerfOS_Memory selected PagesOutputPersec.

Observation kind: momentary_state. Time: 2026-10-05T12:16:22.627Z.

Uncertainty: Single provider-formatted sample; paging includes file-backed activity and does not establish sustained swap pressure.

## obs.memory.performance.PageReadsPersec

Class: `OBSERVED_FACT`.

PageReadsPersec: `{"units":"read_operations_per_second","value":"0"}`

Source: CIM Win32_PerfFormattedData_PerfOS_Memory selected PageReadsPersec.

Observation kind: momentary_state. Time: 2026-10-05T12:16:22.628Z.

Uncertainty: Single provider-formatted sample; paging includes file-backed activity and does not establish sustained swap pressure.

## unavailable.thermal.temperature

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: Remaining selected ACPI temperature values.

Reason: Temperature query unavailable, denied or unusable; raw error suppressed.

Effects: Temperature-based safety conclusions require another authorized observation source..

## unavailable.instruction_features

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: Instruction-set features.

Reason: Not probed by this narrow observation adapter; no inference from model text.

Effects: Feature-dependent selection requires a C1 feature helper..

## unavailable.cache

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: Cache hierarchy and capacities.

Reason: Not probed by this narrow observation adapter; no inference from model text.

Effects: Cache tuning is unsupported..

## unavailable.topology

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: NUMA and processor topology.

Reason: Not probed by this narrow observation adapter; no inference from model text.

Effects: Topology-specific affinity or memory tuning is unsupported..

## unavailable.virtualization

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: Virtualization status.

Reason: Not probed by this narrow observation adapter; no inference from model text.

Effects: No bare-metal or virtualized-environment conclusion is permitted..

## unavailable.device_class

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: Physical storage device class.

Reason: Not probed by this narrow observation adapter; no inference from model text.

Effects: Drive technology cannot be inferred from volume class..

## unavailable.throttling

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: Throttling and active CPU frequency.

Reason: Not probed by this narrow observation adapter; no inference from model text.

Effects: No throttling or sustained-frequency conclusion is permitted..

## tools.command.gcc

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: gcc command-search availability and version.

Reason: Application was not resolved or the lookup was unavailable; alternate installation locations are not excluded.

Effects: Decisions requiring this fact remain unsupported; no production stack is selected by this adapter.

## tools.command.gpp

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: g++ command-search availability and version.

Reason: Application was not resolved or the lookup was unavailable; alternate installation locations are not excluded.

Effects: Decisions requiring this fact remain unsupported; no production stack is selected by this adapter.

## tools.command.clang

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: clang command-search availability and version.

Reason: Application was not resolved or the lookup was unavailable; alternate installation locations are not excluded.

Effects: Decisions requiring this fact remain unsupported; no production stack is selected by this adapter.

## tools.command.clangpp

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: clang++ command-search availability and version.

Reason: Application was not resolved or the lookup was unavailable; alternate installation locations are not excluded.

Effects: Decisions requiring this fact remain unsupported; no production stack is selected by this adapter.

## tools.command.cl

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: cl command-search availability and version.

Reason: Application was not resolved or the lookup was unavailable; alternate installation locations are not excluded.

Effects: Decisions requiring this fact remain unsupported; no production stack is selected by this adapter.

## tools.command.cmake

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: cmake command-search availability and version.

Reason: Application was not resolved or the lookup was unavailable; alternate installation locations are not excluded.

Effects: Decisions requiring this fact remain unsupported; no production stack is selected by this adapter.

## tools.command.ninja

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: ninja command-search availability and version.

Reason: Application was not resolved or the lookup was unavailable; alternate installation locations are not excluded.

Effects: Decisions requiring this fact remain unsupported; no production stack is selected by this adapter.

## tools.command.pkg-config

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: pkg-config command-search availability and version.

Reason: Application was not resolved or the lookup was unavailable; alternate installation locations are not excluded.

Effects: Decisions requiring this fact remain unsupported; no production stack is selected by this adapter.

## tools.path

Class: `OBSERVED_FACT`.

candidate_command_availability: `{"cargo":true,"cl":false,"clang":false,"clang++":false,"cmake":false,"g++":false,"gcc":false,"ninja":false,"pkg-config":false,"python":true,"rustc":true}`

Source: Get-Command for named I1 candidates only.

Observation kind: active_configuration. Time: 2026-10-05T12:16:23.0603303Z.

Uncertainty: Absence from command search does not prove absence from the machine

## tools.rustc

Class: `OBSERVED_FACT`.

rustc_version: `"rustc 1.97.1 (8bab26f4f 2026-07-14)"`

Source: Resolved Application version query; automatic toolchain acquisition disabled.

Observation kind: active_configuration. Time: 2026-10-05T12:16:23.1207408Z.

Uncertainty: Version availability is not an offline rebuild proof

## tools.cargo

Class: `OBSERVED_FACT`.

cargo_version: `"cargo 1.97.1 (c980f4866 2026-06-30)"`

Source: Resolved Application version query; automatic toolchain acquisition disabled.

Observation kind: active_configuration. Time: 2026-10-05T12:16:23.1706668Z.

Uncertainty: Version availability is not an offline rebuild proof

## tools.python

Class: `OBSERVED_FACT`.

python_version: `"Python 3.12.10"`

Source: Resolved Application version query; automatic toolchain acquisition disabled.

Observation kind: active_configuration. Time: 2026-10-05T12:16:23.1892369Z.

Uncertainty: Version availability is not an offline rebuild proof

## tools.rust-target

Class: `OBSERVED_FACT`.

rust_target: `"x86_64-pc-windows-msvc"`

Source: Resolved rustc verbose version; host field only.

Observation kind: active_configuration. Time: 2026-10-05T12:16:23.2480535Z.

Uncertainty: No production candidate compiled

## tools.rug-cache

Class: `OBSERVED_FACT`.

candidate_cache_entry_counts: `{"gmp-mpfr-sys-*":"0","rug-*":"0"}`

Source: Named rug and gmp-mpfr-sys entries in configured/default Cargo registry source/package caches.

Observation kind: active_configuration. Time: 2026-10-05T12:16:23.2670717Z.

Uncertainty: No unrelated package names or cache paths collected; alternate caches not excluded; null means unavailable, not zero

## tools.msvc.cl.exe

Class: `OBSERVED_FACT`.

cl.exe_file_version: `{"build":"35228","major":"19","minor":"44","revision":"0"}`

Source: Selected executable file-version fields located using the Visual C++ component query.

Observation kind: active_configuration. Time: 2026-10-05T12:16:23.3555867Z.

Uncertainty: Toolchain environment not activated; executable metadata does not establish successful compilation, linking or offline rebuild

## tools.msvc.link.exe

Class: `OBSERVED_FACT`.

link.exe_file_version: `{"build":"35228","major":"14","minor":"44","revision":"0"}`

Source: Selected executable file-version fields located using the Visual C++ component query.

Observation kind: active_configuration. Time: 2026-10-05T12:16:23.3565607Z.

Uncertainty: Toolchain environment not activated; executable metadata does not establish successful compilation, linking or offline rebuild

## tools.gmp-locators

Class: `OBSERVED_FACT`.

gmp_header_at_narrow_candidate_locations: `{"mingw":false,"msys2-mingw64":false,"msys2-ucrt64":false,"vcpkg-standard":false}`

Source: Existence probes for named development-package header locators only.

Observation kind: active_configuration. Time: 2026-10-05T12:16:23.3587849Z.

Uncertainty: Not a whole-machine search; headers alone would not establish library compatibility or provenance

## tools.gmp-unavailable

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: I1-eligible GMP development package at the standard external locators.

Reason: No usable package established within these locators; repository-local acquired candidates require their own package and build evidence

Effects: Decisions requiring this fact remain unsupported; no production stack is selected by this adapter.

## tools.flint-unavailable

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: Optional public FLINT backend.

Reason: A usable GMP-backed production prerequisite is not established by locator probes; optional FLINT candidate not activated or measured

Effects: Decisions requiring this fact remain unsupported; no production stack is selected by this adapter.

## dependency.pre-setup

Class: `OBSERVED_FACT`.

before_setup_resource_snapshot: `{"obs.memory.performance.AvailableBytes":{"units":"bytes","value":"6691520512"},"obs.memory.performance.PageReadsPersec":{"units":"read_operations_per_second","value":"0"},"obs.memory.performance.PagesInputPersec":{"units":"pages_per_second","value":"0"},"obs.memory.performance.PagesOutputPersec":{"units":"pages_per_second","value":"0"},"obs.power.hibernate.AC":{"units":"seconds","value":"0"},"obs.power.hibernate.DC":{"units":"seconds","value":"0"},"obs.power.source":{"units":"class","value":"AC"},"obs.power.standby.AC":{"units":"seconds","value":"0"},"obs.power.standby.DC":{"units":"seconds","value":"0"}}`

Source: Narrow Windows collector before acquisition and compilation.

Observation kind: momentary_state. Time: initial audit session; exact timestamp not retained.

Uncertainty: Transient conditions; initial calibration ceilings remain in force

## dependency.authorization

Class: `OBSERVED_FACT`.

dependency_setup_authorized: `true`

Source: Explicit operator message on 2026-10-05 authorizing installation, builds and required setup.

Observation kind: active_configuration. Time: initial audit session; exact timestamp not retained.

Uncertainty: Authorization persists; it does not authorize scientific work or production selection

## dependency.acquisition

Class: `OBSERVED_FACT`.

acquisition: `{"binary":{"bytes":"592359","name":"mingw-w64-ucrt-x86_64-gmp-6.3.0-2-any.pkg.tar.zst","sha256":"e82a75968a556484a50084578238a84eb60fb93e34986fd6695c537975bd39ea","sha3_256":"f9657bbd612ff84b5c23df35ac5b1eec5977bc0e7ac45ea6accfb378316c16f5","url":"https://mirror.msys2.org/mingw/ucrt64/mingw-w64-ucrt-x86_64-gmp-6.3.0-2-any.pkg.tar.zst"},"observed_at":"2026-10-05T12:10:10Z","source":{"bytes":"2097066","name":"mingw-w64-gmp-6.3.0-2.src.tar.zst","sha256":"f288f944fd9609db220bcf6a8dd0703a5674eeb906ef35eb8485bb8192135994","sha3_256":"88453154634288954d97c875b6358d2c76f50d787346055fbffdff03d49471e2","url":"https://mirror.msys2.org/mingw/sources/mingw-w64-gmp-6.3.0-2.src.tar.zst"},"source_authentication":"Official HTTPS channel; no independent signature verification claimed","stage":"hardware characterization"}`

Source: Explicit acquisition, safe archive inspection, public C compile/link and fixed arithmetic capability probe.

Observation kind: active_configuration. Time: 2026-10-05T12:10:10Z.

Uncertainty: Engineering candidate evidence only; offline production toolchain closure and stack selection remain open

## dependency.source-provenance

Class: `OBSERVED_FACT`.

source_provenance: `{"observed_at":"2026-10-05T12:14:38Z","source_material":{"COPYING":{"bytes":"35147","sha256":"8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903","sha3_256":"040444d59237d8142345043e4aec153ef10c8291c8932e5f9e1eba6e791e71e7"},"COPYING.LESSERv3":{"bytes":"7639","sha256":"a853c2ffec17057872340eee242ae4d96cbf2b520ae27d903e1b2fef1a5f9d1c","sha3_256":"8dac4a2dd3799d07bec9dd706b109a40286d4ba7c6cd21d51b35d6bffb3ec83e"},"COPYINGv2":{"bytes":"18092","sha256":"8177f97513213526df2cf6184d8ff986c675afb514d4e68a404010521b880643","sha3_256":"32fac3e90cdea91b37289b9ca09d781a364bf22864e52d5c5d6a6fa40080be17"},"COPYINGv3":{"bytes":"35150","sha256":"e6037104443f9a7829b2aa7c5370d0789a7bda3ca65a0b904cdc0c2e285d9195","sha3_256":"dafc0b870e82d76b16cbcc06bf994a031619b8bba9f7498dbfd6888f287f10c1"},"PKGBUILD":{"bytes":"2288","sha256":"b9d3bb2b5b12cb0fc47c4dc17a9a2aa82513236eaefa34c8dfc57dd0d92bc42a","sha3_256":"c994b704be0e79587f0c513ed385609349966f0461b445d30287364a575e0ef2"},"do-not-use-dllimport.diff":{"bytes":"491","sha256":"385ab704f82c47f3aecc9141f43c96e7b8de2bf0e654dc457ce0f1a039db2c68","sha3_256":"a202ea7c81081dd75ac22ce22bbf5d072232a3ae32520e6b9b0d02e2e4f957db"},"gmp-6.3.0.tar.xz":{"bytes":"2094196","sha256":"a3c2b80201b89e68616f4ad30bc66aee4927c3ce50e33929ca819d5c43538898","sha3_256":"025f4fc3c5f68a0faae40cb8579dc7979eded558edfbc58ac030a072a6b5a6e7"},"gmp-6.3.0.tar.xz.sig":{"bytes":"374","sha256":"94def8c1a731854de684689126046ec93589147abd4cd0025f12d741d323aa82","sha3_256":"6dc5910b7b96baef21728c41be93df2d9131e28027cf6f5b7ddcc69bacaf1ebe"},"gmp-staticlib.diff":{"bytes":"900","sha256":"7c3cde2634baa2cb1c31404bbfed2d8d7ba33556971ac842a08f2e87667849ab","sha3_256":"502e12f8b86aff5e2a4e1968463c77c9c7356427351c160d63f85ab145fdf787"}},"stage":"hardware characterization","upstream_archive_matches_distribution_recipe":true}`

Source: Explicit acquisition, safe archive inspection, public C compile/link and fixed arithmetic capability probe.

Observation kind: active_configuration. Time: 2026-10-05T12:14:38Z.

Uncertainty: Engineering candidate evidence only; offline production toolchain closure and stack selection remain open

## dependency.probe-build

Class: `OBSERVED_FACT`.

probe_build: `{"compiler_flags":["-nologo","-std:c17","-W4","-WX","-O2","-MD","-D_CRT_SECURE_NO_WARNINGS","-Brepro","-external:I.","-external:W0"],"definition":{"bytes":"2731","sha256":"a4c424976559f5a12312f3c2c5fc35249f997a74dd649c35e938147d26882b8d","sha3_256":"802a861d30f6ecd6141d829e004422b386088449b67ccf39c4e01b6a3d323a58"},"dll":{"bytes":"681231","sha256":"c2567ccf3f410c3411ba7cd4b7ba14f393a0e70a1d0c0593297df6706b5fba96","sha3_256":"3eb5419c614771eab626c5d3f7e6cdc64279c4b5cf2eca0a28840baf9b4d75cf"},"dll_imports":["KERNEL32.dll","api-ms-win-crt-convert-l1-1-0.dll","api-ms-win-crt-environment-l1-1-0.dll","api-ms-win-crt-filesystem-l1-1-0.dll","api-ms-win-crt-heap-l1-1-0.dll","api-ms-win-crt-locale-l1-1-0.dll","api-ms-win-crt-private-l1-1-0.dll","api-ms-win-crt-runtime-l1-1-0.dll","api-ms-win-crt-stdio-l1-1-0.dll","api-ms-win-crt-string-l1-1-0.dll","api-ms-win-crt-time-l1-1-0.dll","api-ms-win-crt-utility-l1-1-0.dll"],"executable":{"bytes":"12800","sha256":"e13bc9d24cd8ad3bdf80214642f795e03ba6955bacf9bc4ddff69bf1e420dee8","sha3_256":"83642cac3a3c6b92b5b64e6fe5b7a2bb9227de600ea5c6b244b258dc33a5ec83"},"executable_imports":["KERNEL32.dll","VCRUNTIME140.dll","api-ms-win-crt-heap-l1-1-0.dll","api-ms-win-crt-locale-l1-1-0.dll","api-ms-win-crt-math-l1-1-0.dll","api-ms-win-crt-runtime-l1-1-0.dll","api-ms-win-crt-stdio-l1-1-0.dll","api-ms-win-crt-string-l1-1-0.dll","libgmp-10.dll"],"header":{"bytes":"84402","sha256":"178db66910305eed62d2d3fdd1f203a45febaa2aaa64690b608c7d95f2a1a3cc","sha3_256":"69f6f7fa09466586c737a404a41b07f9b432fdbe61e64a479e03b6b2f19413bc"},"import_library":{"bytes":"35754","sha256":"9760887ab67cfb63990c64c776745c6c1b35a355adef8d3f8c16dfeada99f75b","sha3_256":"466b597c4222446daf0446274738294521690a9d4d24d7331fcc127f27d29b58"},"linker_flags":["-Brepro"],"observed_at":"2026-10-05T12:14:00Z","offline":false,"package_sha256":"e82a75968a556484a50084578238a84eb60fb93e34986fd6695c537975bd39ea","public_export_count":"170","source":{"bytes":"2722","sha256":"71db457cd7d39d80736b1b2d26fa470560f295e5a2a98e1470523fa3738f8f52","sha3_256":"d09b5456e9952967c0f347f0ae7ecf92a2400c086d39d53c396ddded1a84072e"},"stage":"hardware characterization","toolchain":{"abi":"LLP64","linkage":"dynamic-GMP-and-UCRT","msvc_tools_version":"14.44.35207","target":"x86_64-pc-windows-msvc","tool_bytes":{"c1.dll":{"bytes":"3430200","sha256":"48bb561939cfd8fbf194bb73b111b2083912da4fb81af2c181cbe8f4b89e5ad1","sha3_256":"4e6736cb20af2cadd2734075bf528cdd1132393133a366dd06932b59428b152f"},"c2.dll":{"bytes":"10462008","sha256":"98050f97d60f7e95fcaf3525a7103e4818fba498a43563922476819ce88ed162","sha3_256":"a5cdf00c3fae9e7c7d00de3b7f80ab9fb69fa5e65ebc1d648c95f805e3e021f5"},"cl.exe":{"bytes":"677736","sha256":"88c8344236a27a6e727e0a8edc49aaa2690bdc7a9464b9d18cc7abe70a9f1c0d","sha3_256":"66a0ad5274cfed76c1c33323612280e4066a09afc59b3af8bb4497b090a795a9"},"lib.exe":{"bytes":"23376","sha256":"3d694c782f93e998fec5db0c2df78153565da23a028ee4618561fa0c33408489","sha3_256":"d907b67a6f37ff537e1297fefd6a23ebe605b74a3c00a3b855e4838e045b9fdc"},"link.exe":{"bytes":"3252576","sha256":"ca11e6c45debd34bf652dfe984c5360a531a005ed78bf72852330c9c2590cf0d","sha3_256":"22c20f3744d0e11af1b1a92e481bb1dea13083c7af6164ca4fb6ddc0a053338e"}},"windows_sdk_version":"10.0.26100.0"}}`

Source: Explicit acquisition, safe archive inspection, public C compile/link and fixed arithmetic capability probe.

Observation kind: active_configuration. Time: 2026-10-05T12:14:00Z.

Uncertainty: Engineering candidate evidence only; offline production toolchain closure and stack selection remain open

## dependency.probe-smoke

Class: `OBSERVED_FACT`.

probe_smoke: `{"executable_sha3_256":"83642cac3a3c6b92b5b64e6fe5b7a2bb9227de600ea5c6b244b258dc33a5ec83","observed_at":"2026-10-05T12:14:00Z","offline":false,"reference":"Independent Python integer product of two fixed decimal operands; no transition","result":{"dll_beside_executable":true,"export_bytes":"25","header_version":"6.3.0","limb_bits":"64","limb_bytes":"8","long_bytes":"4","nail_bits":"0","ok":true,"pointer_bytes":"8","product_decimal":"12193263113702179522618503273362292333223746380111126352690","roundtrip_equal":true,"runtime_version":"6.3.0"},"stage":"hardware characterization"}`

Source: Explicit acquisition, safe archive inspection, public C compile/link and fixed arithmetic capability probe.

Observation kind: active_configuration. Time: 2026-10-05T12:14:00Z.

Uncertainty: Engineering candidate evidence only; offline production toolchain closure and stack selection remain open

## dependency.offline-build

Class: `OBSERVED_FACT`.

offline_build: `{"compiler_flags":["-nologo","-std:c17","-W4","-WX","-O2","-MD","-D_CRT_SECURE_NO_WARNINGS","-Brepro","-external:I.","-external:W0"],"definition":{"bytes":"2731","sha256":"a4c424976559f5a12312f3c2c5fc35249f997a74dd649c35e938147d26882b8d","sha3_256":"802a861d30f6ecd6141d829e004422b386088449b67ccf39c4e01b6a3d323a58"},"dll":{"bytes":"681231","sha256":"c2567ccf3f410c3411ba7cd4b7ba14f393a0e70a1d0c0593297df6706b5fba96","sha3_256":"3eb5419c614771eab626c5d3f7e6cdc64279c4b5cf2eca0a28840baf9b4d75cf"},"dll_imports":["KERNEL32.dll","api-ms-win-crt-convert-l1-1-0.dll","api-ms-win-crt-environment-l1-1-0.dll","api-ms-win-crt-filesystem-l1-1-0.dll","api-ms-win-crt-heap-l1-1-0.dll","api-ms-win-crt-locale-l1-1-0.dll","api-ms-win-crt-private-l1-1-0.dll","api-ms-win-crt-runtime-l1-1-0.dll","api-ms-win-crt-stdio-l1-1-0.dll","api-ms-win-crt-string-l1-1-0.dll","api-ms-win-crt-time-l1-1-0.dll","api-ms-win-crt-utility-l1-1-0.dll"],"executable":{"bytes":"12800","sha256":"e13bc9d24cd8ad3bdf80214642f795e03ba6955bacf9bc4ddff69bf1e420dee8","sha3_256":"83642cac3a3c6b92b5b64e6fe5b7a2bb9227de600ea5c6b244b258dc33a5ec83"},"executable_imports":["KERNEL32.dll","VCRUNTIME140.dll","api-ms-win-crt-heap-l1-1-0.dll","api-ms-win-crt-locale-l1-1-0.dll","api-ms-win-crt-math-l1-1-0.dll","api-ms-win-crt-runtime-l1-1-0.dll","api-ms-win-crt-stdio-l1-1-0.dll","api-ms-win-crt-string-l1-1-0.dll","libgmp-10.dll"],"header":{"bytes":"84402","sha256":"178db66910305eed62d2d3fdd1f203a45febaa2aaa64690b608c7d95f2a1a3cc","sha3_256":"69f6f7fa09466586c737a404a41b07f9b432fdbe61e64a479e03b6b2f19413bc"},"import_library":{"bytes":"35754","sha256":"dcf72ee7800d25f31cbfd1716776453ab479cba12a0e377a547923d42b6e13d6","sha3_256":"8f57620305b8d88415729151159007b7f2561b6d2d1bcb1b10c5501c67418286"},"linker_flags":["-Brepro"],"observed_at":"2026-10-05T12:27:12Z","offline":true,"package_sha256":"e82a75968a556484a50084578238a84eb60fb93e34986fd6695c537975bd39ea","public_export_count":"170","source":{"bytes":"2722","sha256":"71db457cd7d39d80736b1b2d26fa470560f295e5a2a98e1470523fa3738f8f52","sha3_256":"d09b5456e9952967c0f347f0ae7ecf92a2400c086d39d53c396ddded1a84072e"},"stage":"hardware characterization","toolchain":{"abi":"LLP64","linkage":"dynamic-GMP-and-UCRT","msvc_tools_version":"14.44.35207","target":"x86_64-pc-windows-msvc","tool_bytes":{"c1.dll":{"bytes":"3430200","sha256":"48bb561939cfd8fbf194bb73b111b2083912da4fb81af2c181cbe8f4b89e5ad1","sha3_256":"4e6736cb20af2cadd2734075bf528cdd1132393133a366dd06932b59428b152f"},"c2.dll":{"bytes":"10462008","sha256":"98050f97d60f7e95fcaf3525a7103e4818fba498a43563922476819ce88ed162","sha3_256":"a5cdf00c3fae9e7c7d00de3b7f80ab9fb69fa5e65ebc1d648c95f805e3e021f5"},"cl.exe":{"bytes":"677736","sha256":"88c8344236a27a6e727e0a8edc49aaa2690bdc7a9464b9d18cc7abe70a9f1c0d","sha3_256":"66a0ad5274cfed76c1c33323612280e4066a09afc59b3af8bb4497b090a795a9"},"lib.exe":{"bytes":"23376","sha256":"3d694c782f93e998fec5db0c2df78153565da23a028ee4618561fa0c33408489","sha3_256":"d907b67a6f37ff537e1297fefd6a23ebe605b74a3c00a3b855e4838e045b9fdc"},"link.exe":{"bytes":"3252576","sha256":"ca11e6c45debd34bf652dfe984c5360a531a005ed78bf72852330c9c2590cf0d","sha3_256":"22c20f3744d0e11af1b1a92e481bb1dea13083c7af6164ca4fb6ddc0a053338e"}},"windows_sdk_version":"10.0.26100.0"}}`

Source: Explicit acquisition, safe archive inspection, public C compile/link and fixed arithmetic capability probe.

Observation kind: active_configuration. Time: 2026-10-05T12:27:12Z.

Uncertainty: Engineering candidate evidence only; offline production toolchain closure and stack selection remain open

## dependency.offline-smoke

Class: `OBSERVED_FACT`.

offline_smoke: `{"executable_sha3_256":"83642cac3a3c6b92b5b64e6fe5b7a2bb9227de600ea5c6b244b258dc33a5ec83","observed_at":"2026-10-05T12:14:41Z","offline":true,"reference":"Independent Python integer product of two fixed decimal operands; no transition","result":{"dll_beside_executable":true,"export_bytes":"25","header_version":"6.3.0","limb_bits":"64","limb_bytes":"8","long_bytes":"4","nail_bits":"0","ok":true,"pointer_bytes":"8","product_decimal":"12193263113702179522618503273362292333223746380111126352690","roundtrip_equal":true,"runtime_version":"6.3.0"},"stage":"hardware characterization"}`

Source: Explicit acquisition, safe archive inspection, public C compile/link and fixed arithmetic capability probe.

Observation kind: active_configuration. Time: 2026-10-05T12:14:41Z.

Uncertainty: Engineering candidate evidence only; offline production toolchain closure and stack selection remain open

## dependency.calibration-build

Class: `OBSERVED_FACT`.

calibration_build: `{"artifacts":{"cal_candidate":{"executable":{"bytes":"13824","sha256":"7d3fbd434eb6ae60f5fa7ad59d1d8bde9df622e5e6126ca7d7282e3ba33105b9","sha3_256":"a62d3107052bed595cdf00acf9f3c5faccd26a6a6a9d74f1654ca6881d5bf306"},"source":{"bytes":"4432","sha256":"801b5e5abbc5f7b1a6e8a4e307274c8f9379addf02e9fac80e91822b5241505c","sha3_256":"a725a635b8f705d4844aa687475a7d3724a0826d2c2a355c4a2af2f4402936df"}},"cal_guard":{"executable":{"bytes":"16896","sha256":"8e6883ed04de93e71891bd04d3c9997258eb702233b271fbc544a3b8c284f79e","sha3_256":"b501a11b0363ef97858b6e108da063f34030078f49a871c8c521139cd7e171fd"},"source":{"bytes":"8731","sha256":"8341c36ad772ba9f17ccd247c1d862059c4f110426473a011f417e05cc4f842b","sha3_256":"766c4aed98d1ef53e206241478aa2f9a016bd2528d5dde7bd943d25da09ed114"}}},"compiler_flags":["-nologo","-std:c17","-W4","-WX","-O2","-MD","-D_CRT_SECURE_NO_WARNINGS","-Brepro","-external:I.","-external:W0"],"dependency":{"bytes":"681231","sha256":"c2567ccf3f410c3411ba7cd4b7ba14f393a0e70a1d0c0593297df6706b5fba96","sha3_256":"3eb5419c614771eab626c5d3f7e6cdc64279c4b5cf2eca0a28840baf9b4d75cf"},"observed_at":"2026-10-05T12:27:15Z","offline":true,"pin":{"bytes":"2011","sha256":"8b3896071f587fd4a3063b579b11eab5adec8dd0950389e5a271eb5851f9cc0b","sha3_256":"325273e55ae870a017d12636d0eabe4e3a64041872959b4afc682b4cd3e9fb89"},"stage":"hardware characterization","toolchain":{"abi":"LLP64","linkage":"dynamic-GMP-and-UCRT","msvc_tools_version":"14.44.35207","target":"x86_64-pc-windows-msvc","tool_bytes":{"c1.dll":{"bytes":"3430200","sha256":"48bb561939cfd8fbf194bb73b111b2083912da4fb81af2c181cbe8f4b89e5ad1","sha3_256":"4e6736cb20af2cadd2734075bf528cdd1132393133a366dd06932b59428b152f"},"c2.dll":{"bytes":"10462008","sha256":"98050f97d60f7e95fcaf3525a7103e4818fba498a43563922476819ce88ed162","sha3_256":"a5cdf00c3fae9e7c7d00de3b7f80ab9fb69fa5e65ebc1d648c95f805e3e021f5"},"cl.exe":{"bytes":"677736","sha256":"88c8344236a27a6e727e0a8edc49aaa2690bdc7a9464b9d18cc7abe70a9f1c0d","sha3_256":"66a0ad5274cfed76c1c33323612280e4066a09afc59b3af8bb4497b090a795a9"},"lib.exe":{"bytes":"23376","sha256":"3d694c782f93e998fec5db0c2df78153565da23a028ee4618561fa0c33408489","sha3_256":"d907b67a6f37ff537e1297fefd6a23ebe605b74a3c00a3b855e4838e045b9fdc"},"link.exe":{"bytes":"3252576","sha256":"ca11e6c45debd34bf652dfe984c5360a531a005ed78bf72852330c9c2590cf0d","sha3_256":"22c20f3744d0e11af1b1a92e481bb1dea13083c7af6164ca4fb6ddc0a053338e"}},"windows_sdk_version":"10.0.26100.0"}}`

Source: Explicit acquisition, safe archive inspection, public C compile/link and fixed arithmetic capability probe.

Observation kind: active_configuration. Time: 2026-10-05T12:27:15Z.

Uncertainty: Engineering candidate evidence only; offline production toolchain closure and stack selection remain open

## engineering.generator-vector

Class: `OBSERVED_FACT`.

normative_generator_vector: `{"checks":{"descriptor_jcs":true,"initial_state_digest":true,"input_digest":true,"shake_output_hex":true,"state_hex":true},"initial_state_digest":"95eef319edc55bd8a1aa5f9f210fea3f3b9bae480913f7ae1af9bc59332e6271","input_digest":"84b55262e1b0543c0201479122d92f19cf8ab38550db60a3075c5564b3b7fc0a","input_id":"cal1/01/route-crossover/256/0","purpose":"engineering-only","represented_shortcut_steps":"0","scope":"Fixed generator vector only; no benchmark, trajectory or V1 execution.","stage":"hardware characterization","status":"PASS","suite_version":"CEML-CAL-1"}`

Source: Fixed normative CEML-CAL-1 vector self-test before the subset.

Observation kind: active_configuration. Time: initial audit session; exact timestamp not retained.

Uncertainty: The vector self-test performs no trajectory

## calibration.first-attempt

Class: `OBSERVED_FACT`.

guarded_initial_warmup_outcome: `{"abort_code":"C1_RESOURCE_ABORT","accepted_for_performance":false,"available_bytes":"6721101824","candidate_reference_agreement":true,"child_wall_time_ns":"38032000","fallback_count":"0","final_pages_input_rounded":"1917","final_pages_output_rounded":"0","free_storage_bytes":"209080311808","odd_steps":"120","preflight_pages_input_rounded":"0","preflight_samples":"2","rate_units":"pages_per_second","record_id":"calibration.route.1024.affine-small-public.0.0","requested_affine_blocks":"64","shortcut_steps":"256","standard_steps":"376"}`

Source: Native Job-guarded 1024-bit public engineering warmup; PDH preflight and post-child observation.

Observation kind: momentary_state. Time: initial audit session; exact timestamp not retained.

Uncertainty: Paging includes mapped-file reads. Short rate interval can amplify bursts. No claim of actual pagefile pressure. Invalid raw CPU/RSS zeros are suppressed placeholders, not measurements. No accepted timing or V1 evidence

## c1.checkpoint-unestablished

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CKPT-1 filesystem durability and recovery acceptance.

Reason: Ordered calibration stopped at its first resource refusal; no synthetic filesystem interruption matrix executed

Effects: No checkpoint strategy, production engine, final build or machine profile selected.

## c1.production-unselected

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: Production architecture and complete final offline build/profile.

Reason: Dependency capability is established but valid decision-relevant calibration and checkpoint acceptance are absent

Effects: Remain at C1 hardware characterization; V1 and scientific execution remain denied.

## c1.matrix.01.route-crossover

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 route-crossover.

Reason: First 1024-bit affine warmup invalidated by resource check; no measured repetitions. Two admitted size classes are insufficient for the I1 three-class timing rule.

Effects: No justified production selection or winner.

## c1.matrix.02.small-block-sweep

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 small-block-sweep.

Reason: Not reached after the first resource refusal; required evidence remains unavailable

Effects: No justified production selection or winner.

## c1.matrix.03.hierarchical-sweep

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 hierarchical-sweep.

Reason: Not reached after the first resource refusal; required evidence remains unavailable

Effects: No justified production selection or winner.

## c1.matrix.04.backend-multiplication

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 backend-multiplication.

Reason: Not reached after the first resource refusal; required evidence remains unavailable

Effects: No justified production selection or winner.

## c1.matrix.05.representation

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 representation.

Reason: Not reached after the first resource refusal; required evidence remains unavailable

Effects: No justified production selection or winner.

## c1.matrix.06.allocation

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 allocation.

Reason: Not reached after the first resource refusal; required evidence remains unavailable

Effects: No justified production selection or winner.

## c1.matrix.07.compiler-build

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 compiler-build.

Reason: Not reached after the first resource refusal; required evidence remains unavailable

Effects: No justified production selection or winner.

## c1.matrix.08.parallelism

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 parallelism.

Reason: Not reached after the first resource refusal; required evidence remains unavailable

Effects: No justified production selection or winner.

## c1.matrix.09.checkpoint

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 checkpoint.

Reason: Not reached after the first resource refusal; required evidence remains unavailable

Effects: No justified production selection or winner.

## c1.matrix.10.terminal-handoff

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 terminal-handoff.

Reason: Not reached after the first resource refusal; required evidence remains unavailable

Effects: No justified production selection or winner.

## c1.matrix.11.audit-cost

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 audit-cost.

Reason: Not reached after the first resource refusal; required evidence remains unavailable

Effects: No justified production selection or winner.

## c1.matrix.12.memory-scaling

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 memory-scaling.

Reason: Not reached after the first resource refusal; required evidence remains unavailable

Effects: No justified production selection or winner.
