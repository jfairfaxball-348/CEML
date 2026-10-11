# CEML-L1 acceptance and refusal evidence

Date: 2026-10-11. **Decision: L1 OPEN. No RUN1 handoff.**

The owner invoked the main NEXT_SESSION_PROMPT and subsequently requested continuation. Live main/local entry and P2 PR #4 merge SHA: `abd5d5bd0c6bb3a5cfbd1b83d52122b04d324016`; merged `2026-10-11T12:52:38Z`. Work branch: `codex/l1-offline-frontier`. Entry and exit inspection found no open PRs before this draft and zero Actions runs. No hosted CI PASS or L1 merge is asserted. The draft PR records an engineering candidate, not acceptance or science.

## Implemented scope and reused primitives

New GMP-only C17 worker, independent definition-level Python reference, one standard-library CLI/checker, offline build adapter and six test files. The worker emits exact ordered pipe frames; the driver compares each frame and performs a separate full every-n replay before immutable commit. Schema/canonical/domain checks, explicit budgets, pending accounting, predecessor checks, two-slot generations, write-through/no-replace promotion, re-read, prefix re-execution, strict rooted ledger, and RUN1 authority refusals are implemented. Runtime has no fetch, telemetry or Git mutation path. Scientific pilot/resume remain denied by current status and absent RUN1 evidence.

The worker links the unchanged elementary `ceml_oracle.c` only for independent bounded identity checks. Python hashlib supplies SHA3; no need to link the legacy digest module. The small ctypes filesystem adapter reproduces file fsync/Win32 FlushFileBuffers, same-directory MoveFileExW write-through and directory flush, avoiding legacy codec/store dependencies; this is the explained smaller distinct adapter. The build adapts public export/toolchain primitives without importing the network-capable legacy acquisition module. All C1 source, reports, pins, guards and historical schemas remain unchanged.

The table serialization chosen at implementation is ASCII `r|parity_lsb_first|affine_a|affine_b|T4_r\n`, rows r=0..15; digest `H("TABLE",bytes)`. Build, native and Python derive it separately. TABLE, BUILD, CHECKER and TEST-SOURCES are implementation identity tags under the existing prefix; all frozen SNAPSHOT/RUN/GENESIS/EVENTS/CHECKPOINT/CERTIFICATE domains and canonical bytes are preserved. No new exclusion is activated.

Acceptance records deliberately use small synthetic induction bases and `L1-NONSCIENTIFIC` authority, the exact interval/run-ID whitelist and a bound `acceptance.json` sidecar. The copied research snapshot remains factual and unaccepted; its external B is not claimed as the small fixture base. Production manifest validation rejects these fixtures; deleting/changing the sidecar cannot convert them into science. Repeated fixture IDs used for cold/resume reproducibility are synthetic test identities, not distinct scientific reruns.

## Commands and observations

| Check actually executed | Verdict | Observation |
|---|---|---|
| `python tools/c1/gmp_setup.py build` | REFUSED | `C1 authorization is not established`; guard preserved |
| `python tools/c1/gmp_setup.py offline-smoke` | REFUSED | Same phase refusal; no old engine or pin changed |
| `python tools/frontier/f1_build.py --show-command` | PASS | Prints exact release/checked command without compiling |
| `python tools/frontier/f1_build.py` | PASS | Separate release and checked executables compiled locally from pins |
| `python tools/frontier/f1_build.py --verify` | PASS | Separate clean build; all nine artifact hashes equal; source drift refuses |
| `python -m unittest discover -s tests/frontier -v` | PASS | 91 tests, no skips, 156.910 seconds before final one-active-batch addition |
| Final `python -m unittest discover -s tests/frontier -p test_batches.py -v` | PASS | All 9 affected tests on final source/build, no skips, 161.479 seconds; 92 distinct tests covered overall |
| CLI `rules` | PASS | All 16 parity rows, 144 assignments, fixed witnesses and bounded identities |
| CLI `snapshot --file config/frontier_snapshot_v1.json` | PASS | Exact 632 bytes and frozen research digest; no assumption accepted |
| Final clean build + selftest with Python network imports/socket audit events denied | PASS | Actual final build verification and three native/full-replay fixtures; recorded below |
| OS-level network-disconnected/blocked Windows build and acceptance | NOT_RUN | Firewall administration unavailable; no adapter was disabled; Python denial is a weaker observation |
| Directory flush in actual final fixture directory | PASS | Supported in the observed test; no power-loss guarantee |
| General later-generation torn-latest fallback under strict two-slot parent checks | FAIL / OPEN | Sole later survivor refuses; no missing historical link is inferred |
| Scientific interval / RUN1 / old V1/E1 | NOT_RUN | Not authorised |
| GitHub Actions | NOT_RUN | Repository lists zero runs, not green CI |

Initial integration failures are preserved as observations: offline wrapper needed its local module path, and exact status/UNC tests exposed permissive substring/resolved-path checks. Both were fixed and rerun. Build/source drift during parallel edits correctly refused stale manifests; every final affected test used the recaptured build. Librarian timestamps initially broke clean equality; adding `-Brepro` to the new import-library build fixed reproducibility. No historical library or gate was modified.

## Acceptance matrix detail

PASS: 144 priorities and 16 independently derived rows; flipped table refusal; P3/M9 reverse witnesses; E2/Q4/S2 finite witnesses and n=1 exception; independent C/T/U and standard=t+odd; exact floor counts across boundaries; three full micro-batches; fixed-step identities around 2^32/64/71/128 and above; huge decimal/resource and LLP64 conversion refusal; skipped/duplicated/reordered/truncated/forged frames, counts, states and hashes; aborted or ambiguous native status refusal; pending starts excluded from coverage; partial/self-hashed false certificates rejected; snapshot/build/table/predecessor corruption; immutable final files; one-active-batch/rerun refusal; chain continuity and no checkpoint-only predecessor; ledger replays each member once; crash/resume equals cold certificate; real child process exit99 before/during write/flush and before/after rename; orphan temporary, duplicate/fork/orphan/overflow generations; corrupt latest generation1 fallback to replayed generation0 with warning; ambiguous later sole generation refusal; runtime scientific authority and lookalike flags denied; local source/import/PE/offline dependency review and network-denied Python paths.

OPEN: broader later-generation recovery demanded by the frozen wording; actual OS-level network-isolated build/native acceptance. Power-loss/controller-loss and authenticated rollback resistance remain unproved and are not acceptance claims. No mathematical proof correction was identified. See [the explicit recovery refusal/version-2 proposal](L1_RECOVERY_V2_PROPOSAL.md); its amendment is draft only. V1 contracts and schemas remain unchanged.

## Final build identities

- Build identity: `c8e91ba7510e69b821d77d138fbf291dc1b49ae9fd24d43cd9d67ac9f4c50b87`
- Release executable SHA3-256: `8d3a72aa077fed414ad36e8008900f95a2a0630933e5dea5e66363fd34c19b6b`
- Checked executable SHA3-256: `b562e74ba06d7a4f936f3e0010f36142fe7025f8059e60793aea5388820bc525`
- Build manifest raw SHA3-256: `bd7d774eb99e19bb7b143e5dc3215b76203b34a1f1badf2ab5f595869dfa43bf`
- Test source identity: `5e9a31d2eed01dfa558da0762237fc73d13649e4c289d595508fb90662582913`
- Table identity: `c669b20ad5e928a8a2618a3f4da5afd84ca9e46d14178cef5f0f05ab1eb4d894`
- Research snapshot identity: `a511d6b80fc0ea6c85f3926b065e27acc696449af49cfa675d7c1315e85a2d66`

Observed pins: GMP 6.3.0 / MSYS2 UCRT64 6.3.0-2; exact retained binary/source archive checksums and extracted header/DLL; MSVC 14.44.35207 compiler/linker/librarian content hashes; SDK 10.0.26100.0; Python 3.12.10. The new build uses no zstandard/extraction module; retained extracted bytes and archives are checked separately. The original pinned capability probe was rebuilt byte-for-byte and independently checked for its fixed integer product/runtime version. SDK closure is version-identified, not content-hashed. Missing/changed cache, tools or artifact refuses; no download or fallback exists.

All compiler/include/source/link flags are printed by f1_build --show-command. Release uses the frozen -W4 -WX -O2 -MD C17 flags; checked uses -Od -RTC1 with the same warnings. The injected unused-variable build failed under -WX without replacing the worker.

New source/test files, normalized-LF SHA3-256 (raw and LF hashes also retained in the build manifest):

| File | SHA3-256 |
|---|---|
| `src/frontier_main.c` | `356b81dab45ff9d8cc1dcef493dfbd73bdcceb00ad292beea733b9256a3af8cb` |
| `src/frontier_worker.c` | `3e13f572d680a3ed7af6dd20b72d0eb2a17e03beee6cb1868f488bcfceb6f120` |
| `src/frontier_worker.h` | `26a42e68c6f56c00d2af7220dc13acf0784d5e0557bd3d19bf0d49903d3b724d` |
| `tests/frontier/test_batches.py` | `871fc0068caa2dfcf763e152608b1591b1059532719c95ce8a7d95089d6815fe` |
| `tests/frontier/test_build.py` | `0a107bffdef9e11627ae8451eed820ff28953bee25fddf4a44eae185bcdc782e` |
| `tests/frontier/test_exactness.py` | `286207e295ca0881af6673a3453be1298d3f8a0e8cd6fbae3523f85f20406244` |
| `tests/frontier/test_faults.py` | `5d9d62f0f9016fdf915c91681751183bfd31d3a8ad097637b2e6c55fdbfcde47` |
| `tests/frontier/test_offline.py` | `4c249df074996ad51d9c40a123bb1a4a8ec51ba7c5f55670c946030c541066ab` |
| `tests/frontier/test_rules.py` | `758ecccb1bd968078060e9af05192b054a82a59066d4b9928c1370da4334111f` |
| `tools/frontier/ceml_frontier.py` | `476d799e7773a9eacc6871b0d4eb60f6effcdfc308e9bf50244f6109810d647b` |
| `tools/frontier/f1_build.py` | `8df0fbef634f134c172e738f78583201a1af08337a8f13b99360166cc69493ad` |
| `tools/frontier/reference.py` | `feed8cb719ea7b77d0676d3665e1af86a81c63cc06461a5c80bb58dd437eb140` |

## Measured final small fixtures

Elapsed time includes native pass, Python replay, source/tool pin revalidation and atomic certificate checks; these are overhead-inclusive micro-fixture timings, not scientific-scale native throughput. T steps below are successful explicit steps in one prescribed pass; replay independently computes the same event totals. Multiple validation passes are not combined into claimed trajectory counts.

| Interval | Completed starts | Explicit starts | Explicit T steps | Elapsed seconds |
|---|---:|---:|---:|---:|
| `[2,146)` | 144 | 15 | 269 | 8.621063 |
| `[143,287)` | 144 | 15 | 150 | 8.639834 |
| `[17,113)` | 96 | 10 | 225 | 8.758993 |

Local evidence is ignored: `local/frontier/build/build_manifest.json`, `local/frontier/l1_authorization.json`, `local/frontier/evidence/offline-application-acceptance.json`, and `local/frontier/acceptance/session-*/` aggregate reports, exact run/snapshot/checkpoint/certificate/acceptance records. Events stream through a pipe and memory; no per-integer persistent audit file is created or tracked. The build manifest/report preserves all exact source/tool/test/artifact hashes. Earlier fixtures remain engineering artifacts bound to their earlier build identity and correctly refuse against changed current source.

## Exit and sole next gate

**L1 OPEN, not ENGINE_ACCEPTED and not RUN1-authorised.** A separate future owner invocation must review/freeze any prospective version amendment and arrange the missing OS-level isolated acceptance, then run only a focused L1 continuation. No baseline assumption was accepted, no frontier integer trajectory or scientific batch was executed, no certificate is advertised as science, and old C1 material/guards remain intact. A draft PR makes the candidate reviewable; no L1 merge/approval, hosted CI, recognised frontier or independent external reproduction is asserted.
