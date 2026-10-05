# C1 sanitized hardware report

Stage: **hardware characterization**. **CEML-C1 REMAINS OPEN.**

Audit: `c1-20261005-final`. Generated: 2026-10-05T15:09:02Z.

JSON artifact digest: `191e27941a733c4219c26a5973d16e81385fb69c0af60acb8c28e7b7df7448ea`.

Generated mechanically from HARDWARE_REPORT.json. Observations are not benchmarks,
benchmarks are not V1, and nothing here is scientific evidence.

## obs.os.Caption

Class: `OBSERVED_FACT`.

Caption: `{"units":"text","value":"Microsoft Windows 11 Home"}`

Source: CIM Win32_OperatingSystem selected Caption.

Observation kind: active_configuration. Time: 2026-10-05T14:51:42.913Z.

Uncertainty: No additional uncertainty recorded.

## obs.os.Version

Class: `OBSERVED_FACT`.

Version: `{"units":"text","value":"10.0.26200"}`

Source: CIM Win32_OperatingSystem selected Version.

Observation kind: active_configuration. Time: 2026-10-05T14:51:42.920Z.

Uncertainty: No additional uncertainty recorded.

## obs.os.BuildNumber

Class: `OBSERVED_FACT`.

BuildNumber: `{"units":"text","value":"26200"}`

Source: CIM Win32_OperatingSystem selected BuildNumber.

Observation kind: active_configuration. Time: 2026-10-05T14:51:42.920Z.

Uncertainty: No additional uncertainty recorded.

## obs.os.OSArchitecture

Class: `OBSERVED_FACT`.

OSArchitecture: `{"units":"text","value":"64-bit"}`

Source: CIM Win32_OperatingSystem selected OSArchitecture.

Observation kind: active_configuration. Time: 2026-10-05T14:51:42.923Z.

Uncertainty: No additional uncertainty recorded.

## obs.memory.TotalVisibleMemorySize

Class: `OBSERVED_FACT`.

TotalVisibleMemorySize: `{"units":"KiB","value":"16471564"}`

Source: CIM Win32_OperatingSystem selected TotalVisibleMemorySize.

Observation kind: active_configuration. Time: 2026-10-05T14:51:42.929Z.

Uncertainty: Provider-reported value; virtual-memory fields are not physical RAM capacity.

## obs.memory.FreePhysicalMemory

Class: `OBSERVED_FACT`.

FreePhysicalMemory: `{"units":"KiB","value":"8161852"}`

Source: CIM Win32_OperatingSystem selected FreePhysicalMemory.

Observation kind: momentary_state. Time: 2026-10-05T14:51:42.929Z.

Uncertainty: Provider-reported value; virtual-memory fields are not physical RAM capacity.

## obs.memory.TotalVirtualMemorySize

Class: `OBSERVED_FACT`.

TotalVirtualMemorySize: `{"units":"KiB","value":"17585676"}`

Source: CIM Win32_OperatingSystem selected TotalVirtualMemorySize.

Observation kind: active_configuration. Time: 2026-10-05T14:51:42.929Z.

Uncertainty: Provider-reported value; virtual-memory fields are not physical RAM capacity.

## obs.memory.FreeVirtualMemory

Class: `OBSERVED_FACT`.

FreeVirtualMemory: `{"units":"KiB","value":"7102604"}`

Source: CIM Win32_OperatingSystem selected FreeVirtualMemory.

Observation kind: momentary_state. Time: 2026-10-05T14:51:42.929Z.

Uncertainty: Provider-reported value; virtual-memory fields are not physical RAM capacity.

## obs.memory.SizeStoredInPagingFiles

Class: `OBSERVED_FACT`.

SizeStoredInPagingFiles: `{"units":"KiB","value":"1114112"}`

Source: CIM Win32_OperatingSystem selected SizeStoredInPagingFiles.

Observation kind: active_configuration. Time: 2026-10-05T14:51:42.929Z.

Uncertainty: Provider-reported value; virtual-memory fields are not physical RAM capacity.

## obs.memory.FreeSpaceInPagingFiles

Class: `OBSERVED_FACT`.

FreeSpaceInPagingFiles: `{"units":"KiB","value":"1049984"}`

Source: CIM Win32_OperatingSystem selected FreeSpaceInPagingFiles.

Observation kind: momentary_state. Time: 2026-10-05T14:51:42.937Z.

Uncertainty: Provider-reported value; virtual-memory fields are not physical RAM capacity.

## obs.cpu.0.Manufacturer

Class: `OBSERVED_FACT`.

Manufacturer: `{"units":"text","value":"GenuineIntel"}`

Source: CIM Win32_Processor selected Manufacturer; enumerated entry 0.

Observation kind: static_capability. Time: 2026-10-05T14:51:42.956Z.

Uncertainty: Enumeration position is not a persistent processor identity.

## obs.cpu.0.Name

Class: `OBSERVED_FACT`.

Name: `{"units":"text","value":"11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz"}`

Source: CIM Win32_Processor selected Name; enumerated entry 0.

Observation kind: static_capability. Time: 2026-10-05T14:51:42.956Z.

Uncertainty: Enumeration position is not a persistent processor identity.

## obs.cpu.0.NumberOfCores

Class: `OBSERVED_FACT`.

NumberOfCores: `{"units":"count","value":"8"}`

Source: CIM Win32_Processor selected NumberOfCores; enumerated entry 0.

Observation kind: static_capability. Time: 2026-10-05T14:51:42.962Z.

Uncertainty: Provider-reported capability; does not establish active frequency, instruction use or topology.

## obs.cpu.0.NumberOfLogicalProcessors

Class: `OBSERVED_FACT`.

NumberOfLogicalProcessors: `{"units":"count","value":"16"}`

Source: CIM Win32_Processor selected NumberOfLogicalProcessors; enumerated entry 0.

Observation kind: static_capability. Time: 2026-10-05T14:51:42.962Z.

Uncertainty: Provider-reported capability; does not establish active frequency, instruction use or topology.

## obs.cpu.0.MaxClockSpeed

Class: `OBSERVED_FACT`.

MaxClockSpeed: `{"units":"MHz","value":"2304"}`

Source: CIM Win32_Processor selected MaxClockSpeed; enumerated entry 0.

Observation kind: static_capability. Time: 2026-10-05T14:51:42.962Z.

Uncertainty: Provider-reported capability; does not establish active frequency, instruction use or topology.

## obs.storage.FileSystemType

Class: `OBSERVED_FACT`.

FileSystemType: `{"units":"text","value":"NTFS"}`

Source: Get-Volume for repository checkpoint filesystem; selected FileSystemType.

Observation kind: active_configuration. Time: 2026-10-05T14:51:45.098Z.

Uncertainty: Observed volume class alone does not establish CEML-CKPT-1 durability.

## obs.storage.DriveType

Class: `OBSERVED_FACT`.

DriveType: `{"units":"text","value":"Fixed"}`

Source: Get-Volume for repository checkpoint filesystem; selected DriveType.

Observation kind: active_configuration. Time: 2026-10-05T14:51:45.098Z.

Uncertainty: Observed volume class alone does not establish CEML-CKPT-1 durability.

## obs.storage.Size

Class: `OBSERVED_FACT`.

Size: `{"units":"bytes","value":"999785754624"}`

Source: Get-Volume for repository checkpoint filesystem; selected Size.

Observation kind: active_configuration. Time: 2026-10-05T14:51:45.099Z.

Uncertainty: No additional uncertainty recorded.

## obs.storage.SizeRemaining

Class: `OBSERVED_FACT`.

SizeRemaining: `{"units":"bytes","value":"204517773312"}`

Source: Get-Volume for repository checkpoint filesystem; selected SizeRemaining.

Observation kind: momentary_state. Time: 2026-10-05T14:51:45.099Z.

Uncertainty: No additional uncertainty recorded.

## obs.storage.AllocationUnitSize

Class: `OBSERVED_FACT`.

AllocationUnitSize: `{"units":"bytes","value":"4096"}`

Source: Get-Volume for repository checkpoint filesystem; selected AllocationUnitSize.

Observation kind: active_configuration. Time: 2026-10-05T14:51:45.099Z.

Uncertainty: No additional uncertainty recorded.

## obs.power.source

Class: `OBSERVED_FACT`.

power_source: `{"units":"class","value":"AC"}`

Source: GetSystemPowerStatus; ACLineStatus only retained.

Observation kind: momentary_state. Time: 2026-10-05T14:51:45.288Z.

Uncertainty: No additional uncertainty recorded.

## obs.memory.physically_installed

Class: `OBSERVED_FACT`.

physically_installed_memory: `{"units":"KiB","value":"16777216"}`

Source: GetPhysicallyInstalledSystemMemory.

Observation kind: static_capability. Time: 2026-10-05T14:51:45.295Z.

Uncertainty: API-reported installed capacity, distinct from OS-visible or available memory.

## obs.memory.page_size

Class: `OBSERVED_FACT`.

system_page_size: `{"units":"bytes","value":"4096"}`

Source: System.Environment.SystemPageSize.

Observation kind: static_capability. Time: 2026-10-05T14:51:45.297Z.

Uncertainty: No additional uncertainty recorded.

## obs.environment.process_bitness

Class: `OBSERVED_FACT`.

process_bitness: `{"units":"bits","value":"64"}`

Source: System.IntPtr.Size.

Observation kind: active_configuration. Time: 2026-10-05T14:51:45.297Z.

Uncertainty: No additional uncertainty recorded.

## obs.power.standby.AC

Class: `OBSERVED_FACT`.

standby_ac_timeout: `{"units":"seconds","value":"0"}`

Source: powercfg query current sleep policy STANDBYIDLE; normalized AC index only.

Observation kind: active_configuration. Time: 2026-10-05T14:51:45.336Z.

Uncertainty: Zero means no idle timeout for this setting; other sleep triggers and power-loss risk are not assessed.

## obs.power.standby.DC

Class: `OBSERVED_FACT`.

standby_dc_timeout: `{"units":"seconds","value":"0"}`

Source: powercfg query current sleep policy STANDBYIDLE; normalized DC index only.

Observation kind: active_configuration. Time: 2026-10-05T14:51:45.336Z.

Uncertainty: Zero means no idle timeout for this setting; other sleep triggers and power-loss risk are not assessed.

## obs.power.hibernate.AC

Class: `OBSERVED_FACT`.

hibernate_ac_timeout: `{"units":"seconds","value":"0"}`

Source: powercfg query current sleep policy HIBERNATEIDLE; normalized AC index only.

Observation kind: active_configuration. Time: 2026-10-05T14:51:45.353Z.

Uncertainty: Zero means no idle timeout for this setting; other sleep triggers and power-loss risk are not assessed.

## obs.power.hibernate.DC

Class: `OBSERVED_FACT`.

hibernate_dc_timeout: `{"units":"seconds","value":"0"}`

Source: powercfg query current sleep policy HIBERNATEIDLE; normalized DC index only.

Observation kind: active_configuration. Time: 2026-10-05T14:51:45.353Z.

Uncertainty: Zero means no idle timeout for this setting; other sleep triggers and power-loss risk are not assessed.

## obs.memory.performance.AvailableBytes

Class: `OBSERVED_FACT`.

AvailableBytes: `{"units":"bytes","value":"8186925056"}`

Source: CIM Win32_PerfFormattedData_PerfOS_Memory selected AvailableBytes.

Observation kind: momentary_state. Time: 2026-10-05T14:51:51.328Z.

Uncertainty: Single provider-formatted sample; paging includes file-backed activity and does not establish sustained swap pressure.

## obs.memory.performance.PagesInputPersec

Class: `OBSERVED_FACT`.

PagesInputPersec: `{"units":"pages_per_second","value":"0"}`

Source: CIM Win32_PerfFormattedData_PerfOS_Memory selected PagesInputPersec.

Observation kind: momentary_state. Time: 2026-10-05T14:51:51.328Z.

Uncertainty: Single provider-formatted sample; paging includes file-backed activity and does not establish sustained swap pressure.

## obs.memory.performance.PagesOutputPersec

Class: `OBSERVED_FACT`.

PagesOutputPersec: `{"units":"pages_per_second","value":"0"}`

Source: CIM Win32_PerfFormattedData_PerfOS_Memory selected PagesOutputPersec.

Observation kind: momentary_state. Time: 2026-10-05T14:51:51.331Z.

Uncertainty: Single provider-formatted sample; paging includes file-backed activity and does not establish sustained swap pressure.

## obs.memory.performance.PageReadsPersec

Class: `OBSERVED_FACT`.

PageReadsPersec: `{"units":"read_operations_per_second","value":"0"}`

Source: CIM Win32_PerfFormattedData_PerfOS_Memory selected PageReadsPersec.

Observation kind: momentary_state. Time: 2026-10-05T14:51:51.331Z.

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

Observation kind: active_configuration. Time: 2026-10-05T14:51:52.2482116Z.

Uncertainty: Absence from command search does not prove absence from the machine

## tools.rustc

Class: `OBSERVED_FACT`.

rustc_version: `"rustc 1.97.1 (8bab26f4f 2026-07-14)"`

Source: Resolved Application version query; automatic toolchain acquisition disabled.

Observation kind: active_configuration. Time: 2026-10-05T14:51:52.3537156Z.

Uncertainty: Version availability is not an offline rebuild proof

## tools.cargo

Class: `OBSERVED_FACT`.

cargo_version: `"cargo 1.97.1 (c980f4866 2026-06-30)"`

Source: Resolved Application version query; automatic toolchain acquisition disabled.

Observation kind: active_configuration. Time: 2026-10-05T14:51:52.4580240Z.

Uncertainty: Version availability is not an offline rebuild proof

## tools.python

Class: `OBSERVED_FACT`.

python_version: `"Python 3.12.10"`

Source: Resolved Application version query; automatic toolchain acquisition disabled.

Observation kind: active_configuration. Time: 2026-10-05T14:51:52.4687211Z.

Uncertainty: Version availability is not an offline rebuild proof

## tools.rust-target

Class: `OBSERVED_FACT`.

rust_target: `"x86_64-pc-windows-msvc"`

Source: Resolved rustc verbose version; host field only.

Observation kind: active_configuration. Time: 2026-10-05T14:51:52.5177048Z.

Uncertainty: No production candidate compiled

## tools.rug-cache

Class: `OBSERVED_FACT`.

candidate_cache_entry_counts: `{"gmp-mpfr-sys-*":"0","rug-*":"0"}`

Source: Named rug and gmp-mpfr-sys entries in configured/default Cargo registry source/package caches.

Observation kind: active_configuration. Time: 2026-10-05T14:51:52.5316709Z.

Uncertainty: No unrelated package names or cache paths collected; alternate caches not excluded; null means unavailable, not zero

## tools.msvc.cl.exe

Class: `OBSERVED_FACT`.

cl.exe_file_version: `{"build":"35228","major":"19","minor":"44","revision":"0"}`

Source: Selected executable file-version fields located using the Visual C++ component query.

Observation kind: active_configuration. Time: 2026-10-05T14:51:52.6234507Z.

Uncertainty: Toolchain environment not activated; executable metadata does not establish successful compilation, linking or offline rebuild

## tools.msvc.link.exe

Class: `OBSERVED_FACT`.

link.exe_file_version: `{"build":"35228","major":"14","minor":"44","revision":"0"}`

Source: Selected executable file-version fields located using the Visual C++ component query.

Observation kind: active_configuration. Time: 2026-10-05T14:51:52.6252792Z.

Uncertainty: Toolchain environment not activated; executable metadata does not establish successful compilation, linking or offline rebuild

## tools.gmp-locators

Class: `OBSERVED_FACT`.

gmp_header_at_narrow_candidate_locations: `{"mingw":false,"msys2-mingw64":false,"msys2-ucrt64":false,"vcpkg-standard":false}`

Source: Existence probes for named development-package header locators only.

Observation kind: active_configuration. Time: 2026-10-05T14:51:52.6284676Z.

Uncertainty: Not a whole-machine search; headers alone would not establish library compatibility or provenance

## dependency.authorization

Class: `OBSERVED_FACT`.

dependency_setup_authorized: `true`

Source: Explicit operator authorization on 2026-10-05 for acquisition, installation and builds needed to finish C1.

Observation kind: active_configuration. Time: not retained.

Uncertainty: Does not authorize scientific work, V1 or E1

## dependency.gmp-candidate

Class: `OBSERVED_FACT`.

pinned_gmp_public_c_candidate: `{"abi":"LLP64","distribution_release":"6.3.0-2","dll_sha3_256":"3eb5419c614771eab626c5d3f7e6cdc64279c4b5cf2eca0a28840baf9b4d75cf","header_sha3_256":"69f6f7fa09466586c737a404a41b07f9b432fdbe61e64a479e03b6b2f19413bc","limb_bits":"64","msvc_tools_version":"14.44.35207","nail_bits":"0","offline_rebuild_byte_identical":true,"package_sha256":"e82a75968a556484a50084578238a84eb60fb93e34986fd6695c537975bd39ea","smoke_passed":true,"version":"6.3.0","windows_sdk_version":"10.0.26100.0"}`

Source: Checksum-verified package, public C compile and link with installed MSVC, exact product and import-export smoke, strict offline rebuild.

Observation kind: active_configuration. Time: 2026-10-05T14:47:55Z.

Uncertainty: The GMP binary is a distribution build; GMP itself was not rebuilt from source locally

## engineering.generator-vector

Class: `OBSERVED_FACT`.

normative_generator_vector: `{"checks":{"descriptor_jcs":true,"initial_state_digest":true,"input_digest":true,"shake_output_hex":true,"state_hex":true},"initial_state_digest":"95eef319edc55bd8a1aa5f9f210fea3f3b9bae480913f7ae1af9bc59332e6271","input_digest":"84b55262e1b0543c0201479122d92f19cf8ab38550db60a3075c5564b3b7fc0a","input_id":"cal1/01/route-crossover/256/0","purpose":"engineering-only","represented_shortcut_steps":"0","scope":"Fixed generator vector only; no benchmark, trajectory or V1 execution.","stage":"hardware characterization","status":"PASS","suite_version":"CEML-CAL-1"}`

Source: Fixed normative CEML-CAL-1 vector reproduced before calibration.

Observation kind: active_configuration. Time: not retained.

Uncertainty: No trajectory is performed

## resource.pressure-study

Class: `OBSERVED_FACT`.

arithmetic_free_paging_proxy_study: `{"interval_ms":"1000","minimum_available_bytes":"7933947904","processor_performance_counter_available":true,"processor_performance_percent_range":["153","179"],"summary":{"arithmetic-free-launch":{"count":"10","intervals_above_100_pages":"1","maximum_pages_input_milli":"329929","maximum_pages_output_milli":"0","median_pages_input_milli":"1924","minimum_pages_input_milli":"0"},"idle":{"count":"20","intervals_above_100_pages":"1","maximum_pages_input_milli":"104287","maximum_pages_output_milli":"0","median_pages_input_milli":"992","minimum_pages_input_milli":"0"},"idle-after":{"count":"5","intervals_above_100_pages":"0","maximum_pages_input_milli":"44482","maximum_pages_output_milli":"0","median_pages_input_milli":"3953","minimum_pages_input_milli":"0"}}}`

Source: PDH memory page input and output rates and processor performance over 35 one-second intervals with no calibration case.

Observation kind: momentary_state. Time: 2026-10-05T13:51:11Z.

Uncertainty: Thirty-five samples; page input includes mapped-file reads; not a pagefile-specific measurement

## resource.refusal-log

Class: `OBSERVED_FACT`.

retained_guard_refusals_and_aggregate_budget: `{"aggregate_ceiling_ns":"900000000000","aggregate_child_wall_ns":"19526603300","explicit_resumes":{"cal1-20261005-a":"2","cal1-20261005-b":"1"},"refusals":[{"abort_code":"C1_RESOURCE_ABORT","bundle_id":"c1-20261005-route-subset","maximum_pages_input_rounded":"1917","member":"1024-affine-small-public-0-0-detail.json","pages_output_rounded":"0","reason":"paging-pressure"},{"abort_code":"C1_RESOURCE_ABORT","bundle_id":"cal1-20261005-a-01-route-crossover","maximum_pages_input_rounded":"2978","member":"065536-affine-small-w04-1-a1-detail.json","pages_output_rounded":"0","reason":"paging-input-sustained"},{"abort_code":"C1_PREFLIGHT_REFUSAL","bundle_id":"cal1-20261005-a-01-route-crossover","maximum_pages_input_rounded":"112","member":"065536-affine-small-w16-2-a1-detail.json","pages_output_rounded":"0","reason":"paging-input-sustained"},{"abort_code":"C1_PREFLIGHT_REFUSAL","bundle_id":"cal1-20261005-a-02-small-block-sweep","maximum_pages_input_rounded":"414","member":"004096-affine-small-w16-1-a1-detail.json","pages_output_rounded":"0","reason":"paging-input-sustained"},{"abort_code":"C1_PREFLIGHT_REFUSAL","bundle_id":"cal1-20261005-b-03-hierarchical-sweep","maximum_pages_input_rounded":"0","member":"131072-hier-explicit-d6-k16384-1-a1-detail.json","pages_output_rounded":"33","reason":"paging-output"},{"abort_code":"C1_RESOURCE_ABORT","bundle_id":"manual-20261005-134907","maximum_pages_input_rounded":"138","member":"1024-affine-small-public-0-0-detail.json","pages_output_rounded":"0","reason":"paging-pressure"}]}`

Source: Guard outcomes retained in the indexed local bundles; shared durable budget file.

Observation kind: momentary_state. Time: not retained.

Uncertainty: Every refusal is retained as invalid evidence; none contributes a timing datum

## resource.ceilings

Class: `OBSERVED_FACT`.

local_resource_ceilings_v2_1: `{"admission_wait_intervals_maximum":"30","aggregate_child_wall_seconds":"900","maximum_case_seconds":"5","maximum_process_memory_bytes":"268435456","maximum_processes":"1","maximum_threads":"1","minimum_available_memory_bytes":"4294967296","minimum_free_storage_bytes":"17179869184","pages_input_ceiling_per_second":"100","pages_output_required":"0","power":"AC with zero standby and hibernate idle indices","processor_performance_floor_percent":"100"}`

Source: docs/C1_RESOURCE_CEILINGS_V2.md including amendment 2.1; enforced by the native guard and Job limits.

Observation kind: active_configuration. Time: not retained.

Uncertainty: Ceilings are engineering admission limits for bounded calibration, not scientific resource forecasts

## checkpoint.durability-matrix

Class: `OBSERVED_FACT`.

synthetic_ckpt1_interruption_and_recovery_matrix: `{"adversarial_cases":"13","adversarial_names":["pointer-missing","pointer-garbage","pointer-stale","newest-body-bit-flip","newest-body-truncated","newest-body-trailing-byte","newest-metadata-counter-edit","newest-metadata-noncanonical-space","newest-metadata-missing","older-body-bit-flip","chain-break","foreign-identity","terminal-state"],"adversarial_passed":"13","all_passed":true,"boundary_not_reached":"8","directory_flush_supported":true,"filesystem":"NTFS, fixed local volume, same volume as the intended checkpoint directory","forced_terminations":"70","phases_forced":{"after-flush-before-verify":"6","after-pointer-promote":"6","after-promote-before-dirsync":"6","after-verify-before-promote":"6","body-complete":"6","body-partial":"6","complete-before-exit":"6","metadata-complete-before-flush":"6","metadata-partial":"6","pointer-temp-written":"6","published-before-retire":"6","retire-partial":"2","retire-renamed":"2"},"scenarios":"78","scenarios_passed":"78"}`

Source: Forced self-termination at each named boundary, fresh-process recovery and continuation, independent Python byte validation.

Observation kind: active_configuration. Time: not retained.

Uncertainty: Process interruption only. No power-loss, device write-cache or operating-system crash behaviour was tested or is claimed

## checkpoint.documented-semantics

Class: `OBSERVED_FACT`.

platform_documentation_used: `{"flushfilebuffers":"https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-flushfilebuffers","flushfilebuffers_claim":"Flushes the buffers of a specified file; the handle must have GENERIC_WRITE access","movefileex":"https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw","movefileex_claim":"MOVEFILE_WRITE_THROUGH: the function does not return until the file is actually moved on the disk","publisher":"Microsoft Learn, Win32 API reference","retrieved":"2026-10-05","status":"external documentary claims; publication dates unavailable; not independently reproduced beyond the bounded tests"}`

Source: Primary vendor documentation retrieved during C1.

Observation kind: active_configuration. Time: not retained.

Uncertainty: The pages do not state rename atomicity under power loss; the store does not rely on it for safety

## unsupported.flint

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: Public FLINT backend route.

Reason: No FLINT installation or pinned package is present; the optional route was not acquired

Effects: arith.flint.public is not a candidate.

## unsupported.rust-rug

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: Rust with rug and GMP candidate.

Reason: A Rust toolchain exists but no pinned offline rug or gmp-mpfr-sys source is cached and its GMP build prerequisites are absent

Effects: Rust family not benchmarked; C17 with public GMP is the only complete local family.

## unsupported.native-tuning

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: native-release build mode.

Reason: The pinned Microsoft C compiler has no host-native target mechanism and the GMP binary is a prebuilt distribution library

Effects: Only checked and portable-release modes were compared; the build is portable.

## unsupported.parallel-aux

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: Auxiliary-parallel route.

Reason: The optional auxiliary-parallel candidate was not implemented; no eligible parallel route exists to compare

Effects: parallel.single is the only eligible route; thread count one.

## unsupported.sparse-state

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: Sparse or chunked state representation.

Reason: The optional sparse candidate was not implemented; its larger invariant surface was not justified for C1

Effects: state.dense is the only eligible representation.

## unsupported.value-threaded

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: Value-threaded hierarchical form.

Reason: The optional value-threaded candidate was not implemented

Effects: engine.hier_affine.explicit is the only hierarchical form.

## unavailable.power-loss

Class: `UNAVAILABLE_OR_UNSUPPORTED`.

Requested: Power-loss durability evidence.

Reason: Destructive power-cut testing is not authorized and was not performed

Effects: Durability rests on documented flush semantics plus process-interruption tests; recorded as a limitation.

## bundle.c1-20261005-route-subset

Class: `OBSERVED_FACT`.

retained_local_bundle: `{"bundle_digest":"460b1dc104a9a49e8ebcaa7621d45d5e617e9ce3d8499b09b09f8e239eebec05","member_count":"3","role":"retained refusal or superseded evidence; not used for selection"}`

Source: I1 benchmark bundle digest over lexicographically ordered member names and raw bytes.

Observation kind: active_configuration. Time: not retained.

Uncertainty: Raw records stay local; this digest binds them

## bundle.cal1-20261005-a-01-route-crossover

Class: `OBSERVED_FACT`.

retained_local_bundle: `{"bundle_digest":"1d3e78d7f46147cac780263d065a553cb06cc01bd846ab603a34ac55875732f6","member_count":"1065","role":"decision evidence"}`

Source: I1 benchmark bundle digest over lexicographically ordered member names and raw bytes.

Observation kind: active_configuration. Time: not retained.

Uncertainty: Raw records stay local; this digest binds them

## bundle.cal1-20261005-a-02-small-block-sweep

Class: `OBSERVED_FACT`.

retained_local_bundle: `{"bundle_digest":"a3a60b24a00a5753dee85969afe5a03e699c47d1b4bb68726f7548c165f35480","member_count":"78","role":"retained refusal or superseded evidence; not used for selection"}`

Source: I1 benchmark bundle digest over lexicographically ordered member names and raw bytes.

Observation kind: active_configuration. Time: not retained.

Uncertainty: Raw records stay local; this digest binds them

## bundle.cal1-20261005-b-02-small-block-sweep

Class: `OBSERVED_FACT`.

retained_local_bundle: `{"bundle_digest":"d550bebaa37712961496040307f30fa273ffab5eae672fdada889037e364b591","member_count":"253","role":"decision evidence"}`

Source: I1 benchmark bundle digest over lexicographically ordered member names and raw bytes.

Observation kind: active_configuration. Time: not retained.

Uncertainty: Raw records stay local; this digest binds them

## bundle.cal1-20261005-b-03-hierarchical-sweep

Class: `OBSERVED_FACT`.

retained_local_bundle: `{"bundle_digest":"bdd75664754947e673bb9f71e1fb7fb96aa72504f9efac62d88bfd2ed3bbb467","member_count":"953","role":"decision evidence"}`

Source: I1 benchmark bundle digest over lexicographically ordered member names and raw bytes.

Observation kind: active_configuration. Time: not retained.

Uncertainty: Raw records stay local; this digest binds them

## bundle.cal1-20261005-b-04-backend-multiplication

Class: `OBSERVED_FACT`.

retained_local_bundle: `{"bundle_digest":"ce46503b5f7b291a11b4f5a4ee5732a8709fef995cb2fcfdf1779606b22dc589","member_count":"379","role":"decision evidence"}`

Source: I1 benchmark bundle digest over lexicographically ordered member names and raw bytes.

Observation kind: active_configuration. Time: not retained.

Uncertainty: Raw records stay local; this digest binds them

## bundle.cal1-20261005-b-05-representation

Class: `OBSERVED_FACT`.

retained_local_bundle: `{"bundle_digest":"7210181db873d7b6813f5a4f853ebd5b4535add6142ed2453c002e432744c40e","member_count":"169","role":"decision evidence"}`

Source: I1 benchmark bundle digest over lexicographically ordered member names and raw bytes.

Observation kind: active_configuration. Time: not retained.

Uncertainty: Raw records stay local; this digest binds them

## bundle.cal1-20261005-b-06-allocation

Class: `OBSERVED_FACT`.

retained_local_bundle: `{"bundle_digest":"8cb443a07ca59befc8f16629e5f50b55eb82905e3a781d40f2f21bb4e3b7762c","member_count":"253","role":"decision evidence"}`

Source: I1 benchmark bundle digest over lexicographically ordered member names and raw bytes.

Observation kind: active_configuration. Time: not retained.

Uncertainty: Raw records stay local; this digest binds them

## bundle.cal1-20261005-b-07-compiler-build

Class: `OBSERVED_FACT`.

retained_local_bundle: `{"bundle_digest":"0b179b726814ae00f78c22d39a34d5b29783c75c5380b0c24e45fd76e7dedf99","member_count":"127","role":"decision evidence"}`

Source: I1 benchmark bundle digest over lexicographically ordered member names and raw bytes.

Observation kind: active_configuration. Time: not retained.

Uncertainty: Raw records stay local; this digest binds them

## bundle.cal1-20261005-b-10-terminal-handoff

Class: `OBSERVED_FACT`.

retained_local_bundle: `{"bundle_digest":"514f682ebe091ec448df9c86a86f47c672453c219d7bae0818605edba493bdb7","member_count":"211","role":"decision evidence"}`

Source: I1 benchmark bundle digest over lexicographically ordered member names and raw bytes.

Observation kind: active_configuration. Time: not retained.

Uncertainty: Raw records stay local; this digest binds them

## bundle.cal1-20261005-b-11-audit-cost

Class: `OBSERVED_FACT`.

retained_local_bundle: `{"bundle_digest":"87c6a6431be9665eddcde468509ef2f20503f16efb82c747c9d5bc1779e977e9","member_count":"190","role":"decision evidence"}`

Source: I1 benchmark bundle digest over lexicographically ordered member names and raw bytes.

Observation kind: active_configuration. Time: not retained.

Uncertainty: Raw records stay local; this digest binds them

## bundle.cal1-20261005-b-12-memory-scaling

Class: `OBSERVED_FACT`.

retained_local_bundle: `{"bundle_digest":"2f57323798cedc7e10b575613d8adf14ce2245e289120a789d185ea1034b9065","member_count":"505","role":"decision evidence"}`

Source: I1 benchmark bundle digest over lexicographically ordered member names and raw bytes.

Observation kind: active_configuration. Time: not retained.

Uncertainty: Raw records stay local; this digest binds them

## bundle.ckpt-20261005-a-09-checkpoint-durability

Class: `OBSERVED_FACT`.

retained_local_bundle: `{"bundle_digest":"002cb3d7368ed31f88ce360f1aef7ee60f9da1c6a6c80113b216df468359d82f","member_count":"81","role":"decision evidence"}`

Source: I1 benchmark bundle digest over lexicographically ordered member names and raw bytes.

Observation kind: active_configuration. Time: not retained.

Uncertainty: Raw records stay local; this digest binds them

## bundle.ckpt-20261005-a-09-checkpoint-performance

Class: `OBSERVED_FACT`.

retained_local_bundle: `{"bundle_digest":"72a5cfc6cb6282c5b99f05e7ca01c27a44d2d1f30bd3ba216d54e54a733d4ef7","member_count":"121","role":"decision evidence"}`

Source: I1 benchmark bundle digest over lexicographically ordered member names and raw bytes.

Observation kind: active_configuration. Time: not retained.

Uncertainty: Raw records stay local; this digest binds them

## bundle.manual-20261005-134907

Class: `OBSERVED_FACT`.

retained_local_bundle: `{"bundle_digest":"389e0a43d534d0f792b471e748f0058b1c83140975be61acf63959ddd21a0d36","member_count":"3","role":"retained refusal or superseded evidence; not used for selection"}`

Source: I1 benchmark bundle digest over lexicographically ordered member names and raw bytes.

Observation kind: active_configuration. Time: not retained.

Uncertainty: Raw records stay local; this digest binds them
