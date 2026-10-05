# C1 initial local resource ceilings

Stage: **hardware characterization**. Audit run: `c1-20261004-a`.

These are conservative engineering admission limits, established before any
non-trivial calibration. They are not production tuning or scientific resource
forecasts. Reobserve momentary conditions before every admitted case.

The initial permitted Windows probes reported 16 GiB installed RAM,
16,866,881,536 bytes OS-visible RAM, 5,730,615,296 bytes free physical RAM,
and 208,232,972,288 bytes free on the repository checkpoint target's NTFS volume.
A later pressure sample reported 5,612,523,520 available bytes, 1,566 pages
input/second and zero pages output/second. Page input can include mapped-file
reads; it is not asserted to be pagefile traffic. AC was connected, and the
standby/hibernate idle indices were zero for AC and battery. Thermal observation
was unavailable. These observations are transient, not permanent guarantees.

## Admission and stopping policy

- Reserve at least 4 GiB available physical memory and 16 GiB free target storage.
- Limit a benchmark child to 256 MiB process memory, including simultaneous
  buffers; limit scratch and all per-case checkpoint generations to 64 MiB.
- Admit one benchmark child and one arithmetic thread; no auxiliary parallelism
  is admitted by this initial subset. A supervisor is measurement infrastructure.
- Require AC connected and observed zero standby/hibernate idle timers.
- Require two consecutive pressure samples with zero pages output/second and
  no more than 100 pages input/second; otherwise refuse admission. This deliberately
  conservative proxy can refuse cases because of mapped-file I/O. It makes no
  claim to isolate pagefile traffic.
- At deterministic safe polling boundaries stop on headroom breach, pressure
  breach, loss of AC, timer change, missing required monitor, or case timeout.
- Thermal/throttling telemetry is unavailable: no sustained load is admitted;
  restrict each case to 5 seconds and aggregate measured work to 60 seconds
  under this initial subset. No thermal-safety conclusion is claimed.
- Retain all CEML-CAL-1 input/work/repeat maxima, further restricting fixed
  arithmetic work to 256 shortcut steps, operands to 4,096 bits, tables to
  width 4, and checkpoint magnitude to 1,024 bytes in this initial subset.
- No non-trivial case starts until these preflight and mid-case monitors exist.

The first pressure observation does not meet admission. No calibration was
started. A later session may replace these initial ceilings only with a new,
explicitly recorded observation-backed decision within I1 maxima. No global
power, swap, firmware or thermal policy is changed.

## Source methods

Field-selective `Win32_OperatingSystem`, target-volume query,
`Win32_PerfFormattedData_PerfOS_Memory`, `GetSystemPowerStatus`,
`GetPhysicallyInstalledSystemMemory`, selected power configuration indices,
and the unsuccessful field-selective ACPI thermal query. The report and adapter
preserve only permitted fields; unavailable facts remain unavailable.
