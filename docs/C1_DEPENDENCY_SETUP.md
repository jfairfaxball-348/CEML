# C1 authorized dependency setup

Stage: **hardware characterization**. C1 remains open.

On 2026-10-05 the operator explicitly authorized installation, building and
setup of GMP and other required dependencies. This supersedes the initial
session's acquisition stop. It does not select a production architecture or
authorize scientific work. The acquisition candidate is the public C interface
of GMP 6.3.0, distribution release 6.3.0-2, with the existing Microsoft x64 C
compiler. No system configuration change is needed for this candidate.

## Scope and bounds established before setup

The fresh `c1-20261005-pre-setup` audit observed 6,691,520,512 available bytes,
zero pages input/output per second, AC power and zero standby/hibernate idle
indices. These are transient observations. The initial calibration ceilings in
`docs/C1_RESOURCE_CEILINGS.md` remain in force for non-trivial calibration.

Dependency preparation is bounded separately: one sequential tool invocation,
no parallel compilation, 32 MiB per download, 128 MiB per extracted archive,
256 MiB total setup storage, 60 seconds per build command and five seconds for
the small arithmetic capability probe. Retain at least 4 GiB free physical
memory and 16 GiB free target storage before setup. Archives are checked before
extraction; links, traversal, special files and unexpected names are refused.
The probe uses only small fixed arithmetic/import-export fixtures, with no
Collatz transition, benchmark, scientific input or production route selection.

Artifacts stay under ignored repository-local storage. Acquisition is an
explicit command; offline build and smoke commands cannot fetch dependencies.
Compiler activation is confined to subprocess environments, with paths and
environment contents kept in memory. Raw compiler and package metadata are not
report evidence. Exact selected versions, package and code-content hashes,
public interface facts and sanitized outcomes are eligible report evidence.

## Primary-source basis

All sources below were retrieved 2026-10-05. These are external documentary
claims; local package compatibility must still be observed.

- [GMP platform notes](https://gmplib.org/manual/Notes-for-Particular-Systems)
  document use of a MinGW GMP DLL from Microsoft C and creation of a Microsoft
  import library. Publication date unavailable. Status: documented support for
  the general C interface route, not evidence for this local binary pair.
- [MSYS2 environments](https://www.msys2.org/docs/environments/) identify UCRT64
  as x86-64 with UCRT and explain MSVC runtime compatibility. Publication date
  unavailable; the page includes a dated changelog. Status: documented runtime
  context; no assumption of C++ ABI compatibility or local instruction use.
- [MSYS2 package index](https://packages.msys2.org/packages/mingw-w64-ucrt-x86_64-gmp)
  identifies release 6.3.0-2, build date 2023-09-15, binary/source archive
  locations and binary SHA-256
  `e82a75968a556484a50084578238a84eb60fb93e34986fd6695c537975bd39ea`.
  Status: published distribution metadata, to be checked against downloaded
  bytes. Source-archive authenticity is limited to the official HTTPS channel
  unless an independently authenticated digest is established.
- [Microsoft import-library documentation](https://learn.microsoft.com/en-us/cpp/build/reference/building-an-import-library-and-export-file?view=msvc-170)
  describes DEF-based import-library generation. Publication date unavailable.
  Status: documented tooling mechanism; data exports require DATA treatment.

GMP source, license texts and distribution patches must be retained locally.
Offline rebuilding a CEML candidate against a pinned GMP binary is distinct
from rebuilding GMP itself; a complete GMP source-build tool closure has not
yet been acquired. Neither is a production build/profile freeze.

## Observed setup result

The package was acquired, its published binary checksum matched, and its
matching source archive, upstream source tarball, distribution patches and
license material are retained in the ignored content-addressed local cache.
The upstream tarball also matches the source-package recipe's SHA-256. The
source package includes separate static/shared build recipes and the x86-64
fat-build option; this is provenance, not locally measured instruction-route
activation. No full GMP source compilation was performed.

The unchanged installed header and GMP DLL compiled/linked with the existing
MSVC tools 14.44.35207 and Windows SDK 10.0.26100.0. The public API smoke observed
GMP 6.3.0 in both header and runtime, LLP64 widths, 64-bit limbs and zero nail
bits. Exact multiplication agreed with an independent Python integer result;
minimal big-endian byte export/import agreed. The loaded GMP DLL was observed
beside the executable. The application owns buffers crossing the API boundary.

The pinned offline command rebuilt a byte-identical smoke executable and its
smoke test passed. Only explicit `acquire` can fetch. `build` verifies local
package/header/DLL/source/tool pins and fails on missing or changed inputs.
The package's GNU C++ wrapper is unused. Compiler flags suppress warnings from
the unmodified external GMP header while treating warnings in our C source as
errors. No host-specific compiler tuning was selected. This capability pin is
not the complete final production build manifest or SDK closure.

Rebuild the capability probe offline:

```powershell
python tools/c1/gmp_setup.py build
python tools/c1/gmp_setup.py offline-smoke
```

The candidate header, import library and DLL are available under
`local/c1/gmp-setup/offline/`. Native route harness binaries are separately under
`local/c1/gmp-setup/calibration/`. No global environment or package manager was
changed. The committed `config/c1_gmp_pin.toml` is the exact package/tool pin;
the dependency records in `local_reports/HARDWARE_REPORT.json` provide the
sanitized CEML provenance layer for this candidate event.

## Bounded calibration outcome

The first 1024-bit, width-4 affine warm-up represented exactly 256 T steps,
120 odd steps and 376 standard steps. It agreed with the separate definition
C path, activated 64 requested blocks and had zero fallback. The post-child
paging-input proxy was about 1917 pages per second, exceeding the unchanged
100-page threshold, so the record is `C1_RESOURCE_ABORT` and invalid.
Two preceding one-second admission samples passed. Paging includes mapped-file
reads; the short post-child interval can amplify bursts. Actual pagefile
pressure has not been established. No valid performance datum, winner or
production architecture follows from this attempt.

The ordered subset stopped immediately; later cases and checkpoint testing did
not run. The original invalid record, details and exact harness build context
are retained in the indexed local bundle. Its CPU/RSS zeros are guard
placeholders on an abort, not observations. The driver now emits null for those
unavailable values in any future aborted record; existing raw evidence is
unchanged. Summary timing and RSS statistics are null. Its invalid-repeat count
includes this rejected warm-up; no measured repeat occurred.
