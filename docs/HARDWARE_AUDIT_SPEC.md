# CEML-R4 Hardware Audit Specification Framework

Status: **Bootstrap framework — to be completed/frozen in R4**

C1 must inspect the actual dedicated local machine before selecting hardware-sensitive implementation details.

## Information to inspect and sanitize

Where accessible and scientifically relevant, collect:

### Operating environment
- operating system and version;
- kernel;
- CPU architecture such as x86-64 or ARM64;
- filesystem relevant to the run/checkpoint location;
- sleep/hibernation behaviour;
- power-management policy;
- battery/mains-power state where relevant.

### CPU
- vendor, model, and microarchitecture where reliably identifiable;
- physical core count;
- logical thread count;
- available frequency information;
- cache hierarchy;
- supported instruction-set extensions;
- hardware performance counters available to unprivileged tooling where practical.

### Memory
- installed RAM;
- available RAM at audit time;
- swap configuration;
- memory-bandwidth information if reasonably measurable by a bounded benchmark.

### Storage
- SSD/HDD/NVMe class;
- capacity and available space for the intended local artifact area;
- filesystem;
- bounded sequential write/flush behaviour relevant to checkpoints.

### Toolchains/libraries
- C/C++ compiler availability and versions;
- Rust toolchain availability and version;
- Python version;
- GMP availability/version;
- FLINT availability/version;
- other relevant exact big-integer libraries.

### Thermal and sustained operation
- thermal sensors accessible to userspace;
- whether throttling can be observed;
- sustained-power considerations;
- safe unattended-use recommendations supported by vendor/system evidence where possible.

## Privacy exclusions

Never record or commit:

- serial numbers;
- usernames;
- hostnames;
- MAC addresses;
- IP addresses;
- account identifiers;
- credentials/tokens;
- unrelated filesystem paths;
- unrelated installed software inventories.

If a command exposes sensitive material alongside useful data, sanitize before persistence.

## Required artifacts

C1 should produce sanitized equivalents of:

- `local_reports/HARDWARE_REPORT.json`;
- `local_reports/HARDWARE_REPORT.md`;
- bounded benchmark raw/summary records;
- decision log mapping measurements to engineering choices;
- frozen `config/local_machine_profile.toml` or an equivalent versioned profile suitable for commit after sanitization.

## Bounded calibration

Calibration is engineering-only and must remain far below scientific scale. It may compare, when available:

- GMP versus GMP + FLINT;
- candidate macro/super-block sizes;
- multiplication/backend thresholds;
- compiler optimization settings;
- in-place versus copying strategies;
- single-thread versus limited auxiliary parallelism;
- checkpoint write strategies.

Record exact deterministic inputs/digests, build configuration, wall/CPU time, peak RAM, temp disk, thermal observations when available, and result checksums.

## Engineering choices C1 may make

After measurement, C1 may choose the compiled language/core architecture, arithmetic/multiplication backend, compiler flags, macro-block parameters, memory strategy, thread count, checkpoint cadence/buffers, compression, logging cadence, and safe resource ceilings.

It may not change the frozen scientific invariants.

## Special decisions to document

C1 must explicitly justify:

- whether `-march=native` or equivalent is appropriate and its reproducibility implications;
- whether trajectory evaluation stays single-threaded;
- whether auxiliary work uses other cores;
- whether FLINT materially helps beyond GMP;
- whether checkpointing is limited by serialization, storage bandwidth, flush latency, or state size;
- whether thermals invalidate calibration assumptions;
- practical maximum rung classes for hours-long and several-days-long runs.

## No scientific execution

Neither the audit nor calibration may generate or evaluate the scientific CEML start for any rung.
