# C1 sanitized hardware report

Stage: **hardware characterization**. **CEML-C1 REMAINS OPEN.**

Audit: `c1-20261004-a`. Generated: 2026-10-05T07:05:45Z.

JSON artifact digest: `6a774c3589b73e08f2950dbc312809863cb871c6cb4af8ccb89a82c42106577a`.

Generated mechanically from HARDWARE_REPORT.json. Observations are not benchmarks.
No production build/profile or checkpoint durability acceptance is implied.

## obs.os.Caption

Class: `OBSERVED_FACT`.

Caption: `{"units":"text","value":"Microsoft Windows 11 Home"}`

Source: CIM Win32_OperatingSystem selected Caption.

Observation kind: active_configuration. Time: 2026-10-04T19:10:08.299Z.

Uncertainty: No additional uncertainty recorded.

## obs.os.Version

Class: `OBSERVED_FACT`.

Version: `{"units":"text","value":"10.0.26200"}`

Source: CIM Win32_OperatingSystem selected Version.

Observation kind: active_configuration. Time: 2026-10-04T19:10:08.305Z.

Uncertainty: No additional uncertainty recorded.

## obs.os.BuildNumber

Class: `OBSERVED_FACT`.

BuildNumber: `{"units":"text","value":"26200"}`

Source: CIM Win32_OperatingSystem selected BuildNumber.

Observation kind: active_configuration. Time: 2026-10-04T19:10:08.306Z.

Uncertainty: No additional uncertainty recorded.

## obs.os.OSArchitecture

Class: `OBSERVED_FACT`.

OSArchitecture: `{"units":"text","value":"64-bit"}`

Source: CIM Win32_OperatingSystem selected OSArchitecture.

Observation kind: active_configuration. Time: 2026-10-04T19:10:08.307Z.

Uncertainty: No additional uncertainty recorded.

## obs.memory.TotalVisibleMemorySize

Class: `OBSERVED_FACT`.

TotalVisibleMemorySize: `{"units":"KiB","value":"16471564"}`

Source: CIM Win32_OperatingSystem selected TotalVisibleMemorySize.

Observation kind: active_configuration. Time: 2026-10-04T19:10:08.313Z.

Uncertainty: Provider-reported value; virtual-memory fields are not physical RAM capacity.

## obs.memory.FreePhysicalMemory

Class: `OBSERVED_FACT`.

FreePhysicalMemory: `{"units":"KiB","value":"6395804"}`

Source: CIM Win32_OperatingSystem selected FreePhysicalMemory.

Observation kind: momentary_state. Time: 2026-10-04T19:10:08.314Z.

Uncertainty: Provider-reported value; virtual-memory fields are not physical RAM capacity.

## obs.memory.TotalVirtualMemorySize

Class: `OBSERVED_FACT`.

TotalVirtualMemorySize: `{"units":"KiB","value":"17585676"}`

Source: CIM Win32_OperatingSystem selected TotalVirtualMemorySize.

Observation kind: active_configuration. Time: 2026-10-04T19:10:08.315Z.

Uncertainty: Provider-reported value; virtual-memory fields are not physical RAM capacity.

## obs.memory.FreeVirtualMemory

Class: `OBSERVED_FACT`.

FreeVirtualMemory: `{"units":"KiB","value":"7455440"}`

Source: CIM Win32_OperatingSystem selected FreeVirtualMemory.

Observation kind: momentary_state. Time: 2026-10-04T19:10:08.316Z.

Uncertainty: Provider-reported value; virtual-memory fields are not physical RAM capacity.

## obs.memory.SizeStoredInPagingFiles

Class: `OBSERVED_FACT`.

SizeStoredInPagingFiles: `{"units":"KiB","value":"1114112"}`

Source: CIM Win32_OperatingSystem selected SizeStoredInPagingFiles.

Observation kind: active_configuration. Time: 2026-10-04T19:10:08.316Z.

Uncertainty: Provider-reported value; virtual-memory fields are not physical RAM capacity.

## obs.memory.FreeSpaceInPagingFiles

Class: `OBSERVED_FACT`.

FreeSpaceInPagingFiles: `{"units":"KiB","value":"1062080"}`

Source: CIM Win32_OperatingSystem selected FreeSpaceInPagingFiles.

Observation kind: momentary_state. Time: 2026-10-04T19:10:08.317Z.

Uncertainty: Provider-reported value; virtual-memory fields are not physical RAM capacity.

## obs.cpu.0.Manufacturer

Class: `OBSERVED_FACT`.

Manufacturer: `{"units":"text","value":"GenuineIntel"}`

Source: CIM Win32_Processor selected Manufacturer; enumerated entry 0.

Observation kind: static_capability. Time: 2026-10-04T19:10:08.333Z.

Uncertainty: Enumeration position is not a persistent processor identity.

## obs.cpu.0.Name

Class: `OBSERVED_FACT`.

Name: `{"units":"text","value":"11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz"}`

Source: CIM Win32_Processor selected Name; enumerated entry 0.

Observation kind: static_capability. Time: 2026-10-04T19:10:08.334Z.

Uncertainty: Enumeration position is not a persistent processor identity.

## obs.cpu.0.NumberOfCores

Class: `OBSERVED_FACT`.

NumberOfCores: `{"units":"count","value":"8"}`

Source: CIM Win32_Processor selected NumberOfCores; enumerated entry 0.

Observation kind: static_capability. Time: 2026-10-04T19:10:08.337Z.

Uncertainty: Provider-reported capability; does not establish active frequency, instruction use or topology.

## obs.cpu.0.NumberOfLogicalProcessors

Class: `OBSERVED_FACT`.

NumberOfLogicalProcessors: `{"units":"count","value":"16"}`

Source: CIM Win32_Processor selected NumberOfLogicalProcessors; enumerated entry 0.

Observation kind: static_capability. Time: 2026-10-04T19:10:08.338Z.

Uncertainty: Provider-reported capability; does not establish active frequency, instruction use or topology.

## obs.cpu.0.MaxClockSpeed

Class: `OBSERVED_FACT`.

MaxClockSpeed: `{"units":"MHz","value":"2304"}`

Source: CIM Win32_Processor selected MaxClockSpeed; enumerated entry 0.

Observation kind: static_capability. Time: 2026-10-04T19:10:08.339Z.

Uncertainty: Provider-reported capability; does not establish active frequency, instruction use or topology.

## obs.storage.FileSystemType

Class: `OBSERVED_FACT`.

FileSystemType: `{"units":"text","value":"NTFS"}`

Source: Get-Volume for repository checkpoint filesystem; selected FileSystemType.

Observation kind: active_configuration. Time: 2026-10-04T19:10:09.827Z.

Uncertainty: Observed volume class alone does not establish CEML-CKPT-1 durability.

## obs.storage.DriveType

Class: `OBSERVED_FACT`.

DriveType: `{"units":"text","value":"Fixed"}`

Source: Get-Volume for repository checkpoint filesystem; selected DriveType.

Observation kind: active_configuration. Time: 2026-10-04T19:10:09.828Z.

Uncertainty: Observed volume class alone does not establish CEML-CKPT-1 durability.

## obs.storage.Size

Class: `OBSERVED_FACT`.

Size: `{"units":"bytes","value":"999785754624"}`

Source: Get-Volume for repository checkpoint filesystem; selected Size.

Observation kind: active_configuration. Time: 2026-10-04T19:10:09.829Z.

Uncertainty: No additional uncertainty recorded.

## obs.storage.SizeRemaining

Class: `OBSERVED_FACT`.

SizeRemaining: `{"units":"bytes","value":"208097054720"}`

Source: Get-Volume for repository checkpoint filesystem; selected SizeRemaining.

Observation kind: momentary_state. Time: 2026-10-04T19:10:09.831Z.

Uncertainty: No additional uncertainty recorded.

## obs.storage.AllocationUnitSize

Class: `OBSERVED_FACT`.

AllocationUnitSize: `{"units":"bytes","value":"4096"}`

Source: Get-Volume for repository checkpoint filesystem; selected AllocationUnitSize.

Observation kind: active_configuration. Time: 2026-10-04T19:10:09.832Z.

Uncertainty: No additional uncertainty recorded.

## obs.power.source

Class: `OBSERVED_FACT`.

power_source: `{"units":"class","value":"AC"}`

Source: GetSystemPowerStatus; ACLineStatus only retained.

Observation kind: momentary_state. Time: 2026-10-04T19:10:10.208Z.

Uncertainty: No additional uncertainty recorded.

## obs.memory.physically_installed

Class: `OBSERVED_FACT`.

physically_installed_memory: `{"units":"KiB","value":"16777216"}`

Source: GetPhysicallyInstalledSystemMemory.

Observation kind: static_capability. Time: 2026-10-04T19:10:10.213Z.

Uncertainty: API-reported installed capacity, distinct from OS-visible or available memory.

## obs.memory.page_size

Class: `OBSERVED_FACT`.

system_page_size: `{"units":"bytes","value":"4096"}`

Source: System.Environment.SystemPageSize.

Observation kind: static_capability. Time: 2026-10-04T19:10:10.214Z.

Uncertainty: No additional uncertainty recorded.

## obs.environment.process_bitness

Class: `OBSERVED_FACT`.

process_bitness: `{"units":"bits","value":"64"}`

Source: System.IntPtr.Size.

Observation kind: active_configuration. Time: 2026-10-04T19:10:10.215Z.

Uncertainty: No additional uncertainty recorded.

## obs.power.standby.AC

Class: `OBSERVED_FACT`.

standby_ac_timeout: `{"units":"seconds","value":"0"}`

Source: powercfg query current sleep policy STANDBYIDLE; normalized AC index only.

Observation kind: active_configuration. Time: 2026-10-04T19:10:10.256Z.

Uncertainty: Zero means no idle timeout for this setting; other sleep triggers and power-loss risk are not assessed.

## obs.power.standby.DC

Class: `OBSERVED_FACT`.

standby_dc_timeout: `{"units":"seconds","value":"0"}`

Source: powercfg query current sleep policy STANDBYIDLE; normalized DC index only.

Observation kind: active_configuration. Time: 2026-10-04T19:10:10.257Z.

Uncertainty: Zero means no idle timeout for this setting; other sleep triggers and power-loss risk are not assessed.

## obs.power.hibernate.AC

Class: `OBSERVED_FACT`.

hibernate_ac_timeout: `{"units":"seconds","value":"0"}`

Source: powercfg query current sleep policy HIBERNATEIDLE; normalized AC index only.

Observation kind: active_configuration. Time: 2026-10-04T19:10:10.276Z.

Uncertainty: Zero means no idle timeout for this setting; other sleep triggers and power-loss risk are not assessed.

## obs.power.hibernate.DC

Class: `OBSERVED_FACT`.

hibernate_dc_timeout: `{"units":"seconds","value":"0"}`

Source: powercfg query current sleep policy HIBERNATEIDLE; normalized DC index only.

Observation kind: active_configuration. Time: 2026-10-04T19:10:10.277Z.

Uncertainty: Zero means no idle timeout for this setting; other sleep triggers and power-loss risk are not assessed.

## obs.memory.performance.AvailableBytes

Class: `OBSERVED_FACT`.

AvailableBytes: `{"units":"bytes","value":"6430892032"}`

Source: CIM Win32_PerfFormattedData_PerfOS_Memory selected AvailableBytes.

Observation kind: momentary_state. Time: 2026-10-04T19:10:10.871Z.

Uncertainty: Single provider-formatted sample; paging includes file-backed activity and does not establish sustained swap pressure.

## obs.memory.performance.PagesInputPersec

Class: `OBSERVED_FACT`.

PagesInputPersec: `{"units":"pages_per_second","value":"81"}`

Source: CIM Win32_PerfFormattedData_PerfOS_Memory selected PagesInputPersec.

Observation kind: momentary_state. Time: 2026-10-04T19:10:10.872Z.

Uncertainty: Single provider-formatted sample; paging includes file-backed activity and does not establish sustained swap pressure.

## obs.memory.performance.PagesOutputPersec

Class: `OBSERVED_FACT`.

PagesOutputPersec: `{"units":"pages_per_second","value":"0"}`

Source: CIM Win32_PerfFormattedData_PerfOS_Memory selected PagesOutputPersec.

Observation kind: momentary_state. Time: 2026-10-04T19:10:10.881Z.

Uncertainty: Single provider-formatted sample; paging includes file-backed activity and does not establish sustained swap pressure.

## obs.memory.performance.PageReadsPersec

Class: `OBSERVED_FACT`.

PageReadsPersec: `{"units":"read_operations_per_second","value":"11"}`

Source: CIM Win32_PerfFormattedData_PerfOS_Memory selected PageReadsPersec.

Observation kind: momentary_state. Time: 2026-10-04T19:10:10.882Z.

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

Observation kind: active_configuration. Time: 2026-10-05T07:05:44.5990774Z.

Uncertainty: Absence from command search does not prove absence from the machine

## tools.rustc

Class: `OBSERVED_FACT`.

rustc_version: `"rustc 1.97.1 (8bab26f4f 2026-07-14)"`

Source: Resolved Application version query; automatic toolchain acquisition disabled.

Observation kind: active_configuration. Time: 2026-10-05T07:05:44.6756464Z.

Uncertainty: Version availability is not an offline rebuild proof

## tools.cargo

Class: `OBSERVED_FACT`.

cargo_version: `"cargo 1.97.1 (c980f4866 2026-06-30)"`

Source: Resolved Application version query; automatic toolchain acquisition disabled.

Observation kind: active_configuration. Time: 2026-10-05T07:05:44.7259971Z.

Uncertainty: Version availability is not an offline rebuild proof

## tools.python

Class: `OBSERVED_FACT`.

python_version: `"Python 3.12.10"`

Source: Resolved Application version query; automatic toolchain acquisition disabled.

Observation kind: active_configuration. Time: 2026-10-05T07:05:44.7465369Z.

Uncertainty: Version availability is not an offline rebuild proof

## tools.rust-target

Class: `OBSERVED_FACT`.

rust_target: `"x86_64-pc-windows-msvc"`

Source: Resolved rustc verbose version; host field only.

Observation kind: active_configuration. Time: 2026-10-05T07:05:44.7995469Z.

Uncertainty: No production candidate compiled

## tools.rug-cache

Class: `OBSERVED_FACT`.

candidate_cache_entry_counts: `{"gmp-mpfr-sys-*":"0","rug-*":"0"}`

Source: Named rug and gmp-mpfr-sys entries in configured/default Cargo registry source/package caches.

Observation kind: active_configuration. Time: 2026-10-05T07:05:44.8226750Z.

Uncertainty: No unrelated package names or cache paths collected; alternate caches not excluded; null means unavailable, not zero

## tools.msvc.cl.exe

Class: `OBSERVED_FACT`.

cl.exe_file_version: `{"build":"35228","major":"19","minor":"44","revision":"0"}`

Source: Selected executable file-version fields located using the Visual C++ component query.

Observation kind: active_configuration. Time: 2026-10-05T07:05:44.9161035Z.

Uncertainty: Toolchain environment not activated; executable metadata does not establish successful compilation, linking or offline rebuild

## tools.msvc.link.exe

Class: `OBSERVED_FACT`.

link.exe_file_version: `{"build":"35228","major":"14","minor":"44","revision":"0"}`

Source: Selected executable file-version fields located using the Visual C++ component query.

Observation kind: active_configuration. Time: 2026-10-05T07:05:44.9177295Z.

Uncertainty: Toolchain environment not activated; executable metadata does not establish successful compilation, linking or offline rebuild

## tools.gmp-locators

Class: `OBSERVED_FACT`.

gmp_header_at_narrow_candidate_locations: `{"mingw":false,"msys2-mingw64":false,"msys2-ucrt64":false,"vcpkg-standard":false}`

Source: Existence probes for named development-package header locators only.

Observation kind: active_configuration. Time: 2026-10-05T07:05:44.9206674Z.

Uncertainty: Not a whole-machine search; headers alone would not establish library compatibility or provenance

## tools.gmp-unavailable

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: I1-eligible GMP development package and offline source/package inputs.

Reason: No usable package established within the checked scope; no download, installation, replacement or activation authorized

Effects: Decisions requiring this fact remain unsupported; no production stack is selected by this adapter.

## tools.flint-unavailable

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: Optional public FLINT backend.

Reason: A usable GMP-backed production prerequisite is not established by locator probes; optional FLINT candidate not activated or measured

Effects: Decisions requiring this fact remain unsupported; no production stack is selected by this adapter.

## initial.resource-observation

Class: `OBSERVED_FACT`.

initial_selected_resource_fields: `{"ac_connected":true,"free_physical_memory_bytes":"5730615296","free_target_storage_bytes":"208232972288","hibernate_ac_seconds":"0","hibernate_dc_seconds":"0","installed_memory_bytes":"17179869184","later_available_bytes":"5612523520","os_visible_memory_bytes":"16866881536","page_reads_per_second":"948","pages_input_per_second":"1566","pages_output_per_second":"0","standby_ac_seconds":"0","standby_dc_seconds":"0"}`

Source: Initial field-selective CIM, target-volume, kernel32 power/installed-memory APIs and filtered powercfg indices before dependency discovery.

Observation kind: momentary_state. Time: initial audit session; exact timestamp not retained.

Uncertainty: Two successive initial snapshots, distinct from later collector samples; exact timestamps not retained; paging includes mapped-file activity

## initial.authorization

Class: `OBSERVED_FACT`.

verified_local_main_baseline: `"e2148e47f4cc71ba33bfc5c05140d2adef32f479"`

Source: git status, git log main and merge-base ancestry; controlling-document read.

Observation kind: active_configuration. Time: initial audit session; exact timestamp not retained.

Uncertainty: Local main and local remote-tracking state inspected; no network fetch performed

## tools.jsonschema

Class: `OBSERVED_FACT`.

jsonschema_version: `"4.26.0"`

Source: Existing Python importlib.metadata version query.

Observation kind: active_configuration. Time: 2026-10-05T07:05:45Z.

Uncertainty: Audit schema checker only; no dependency installation

## engineering.generator-vector

Class: `OBSERVED_FACT`.

normative_generator_vector: `{"checks":{"descriptor_jcs":true,"initial_state_digest":true,"input_digest":true,"shake_output_hex":true,"state_hex":true},"initial_state_digest":"95eef319edc55bd8a1aa5f9f210fea3f3b9bae480913f7ae1af9bc59332e6271","input_digest":"84b55262e1b0543c0201479122d92f19cf8ab38550db60a3075c5564b3b7fc0a","input_id":"cal1/01/route-crossover/256/0","purpose":"engineering-only","represented_shortcut_steps":"0","scope":"Fixed generator vector only; no benchmark, trajectory or V1 execution.","stage":"hardware characterization","status":"PASS","suite_version":"CEML-CAL-1"}`

Source: Fixed-vector engineering_codec.self_test_vector against frozen CEML-CAL-1.

Observation kind: active_configuration. Time: 2026-10-05T07:05:45Z.

Uncertainty: No trajectory step, timing case, route comparison or V1 class executed

## c1.monitor-unavailable

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: Enforced non-trivial calibration admission and mid-case monitoring.

Reason: Ceilings recorded, but benchmark supervisor not implemented and first pressure sample fails selected threshold

Effects: No non-trivial calibration or filesystem interruption test admitted.

## c1.checkpoint-unestablished

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CKPT-1 durability and recovery acceptance.

Reason: Stopped at earlier dependency and monitoring prerequisites; no synthetic durability or interruption case executed

Effects: Scientific checkpoint storage unsupported pending evidence; no conclusion that the filesystem is inherently incapable.

## c1.matrix.01.route-crossover

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 route-crossover.

Reason: Required candidate harness, eligible dependency/build provenance and enforced safety monitors are not established; zero cases executed

Effects: No route activation or performance winner; decision.matrix.01.route-crossover refuses selection.

## c1.matrix.02.small-block-sweep

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 small-block-sweep.

Reason: Required candidate harness, eligible dependency/build provenance and enforced safety monitors are not established; zero cases executed

Effects: No route activation or performance winner; decision.matrix.02.small-block-sweep refuses selection.

## c1.matrix.03.hierarchical-sweep

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 hierarchical-sweep.

Reason: Required candidate harness, eligible dependency/build provenance and enforced safety monitors are not established; zero cases executed

Effects: No route activation or performance winner; decision.matrix.03.hierarchical-sweep refuses selection.

## c1.matrix.04.backend-multiplication

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 backend-multiplication.

Reason: Required candidate harness, eligible dependency/build provenance and enforced safety monitors are not established; zero cases executed

Effects: No route activation or performance winner; decision.matrix.04.backend-multiplication refuses selection.

## c1.matrix.05.representation

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 representation.

Reason: Required candidate harness, eligible dependency/build provenance and enforced safety monitors are not established; zero cases executed

Effects: No route activation or performance winner; decision.matrix.05.representation refuses selection.

## c1.matrix.06.allocation

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 allocation.

Reason: Required candidate harness, eligible dependency/build provenance and enforced safety monitors are not established; zero cases executed

Effects: No route activation or performance winner; decision.matrix.06.allocation refuses selection.

## c1.matrix.07.compiler-build

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 compiler-build.

Reason: Required candidate harness, eligible dependency/build provenance and enforced safety monitors are not established; zero cases executed

Effects: No route activation or performance winner; decision.matrix.07.compiler-build refuses selection.

## c1.matrix.08.parallelism

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 parallelism.

Reason: Required candidate harness, eligible dependency/build provenance and enforced safety monitors are not established; zero cases executed

Effects: No route activation or performance winner; decision.matrix.08.parallelism refuses selection.

## c1.matrix.09.checkpoint

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 checkpoint.

Reason: Prior calibration prerequisites unmet; exact codec/store, documented durability semantics and interruption/recovery tests have not been established

Effects: No route activation or performance winner; decision.matrix.09.checkpoint refuses selection.

## c1.matrix.10.terminal-handoff

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 terminal-handoff.

Reason: Required candidate harness, eligible dependency/build provenance and enforced safety monitors are not established; zero cases executed

Effects: No route activation or performance winner; decision.matrix.10.terminal-handoff refuses selection.

## c1.matrix.11.audit-cost

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 audit-cost.

Reason: Required candidate harness, eligible dependency/build provenance and enforced safety monitors are not established; zero cases executed

Effects: No route activation or performance winner; decision.matrix.11.audit-cost refuses selection.

## c1.matrix.12.memory-scaling

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: CEML-CAL-1 memory-scaling.

Reason: Required candidate harness, eligible dependency/build provenance and enforced safety monitors are not established; zero cases executed

Effects: No route activation or performance winner; decision.matrix.12.memory-scaling refuses selection.
