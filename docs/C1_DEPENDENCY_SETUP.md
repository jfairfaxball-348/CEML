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
