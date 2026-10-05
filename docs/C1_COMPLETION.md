# CEML-C1 completion record

Stage: **implementation and build/profile freeze**, closing C1.
Date: 2026-10-05. Assessment: **CEML-C1 PASS**, offered for operator review.
V1 and E1 are not entered. No scientific seed, start or trajectory exists.

This document is a guide to the committed evidence. Where it differs from
`local_reports/*.json` or `config/local_machine_profile.json`, those artifacts
govern; where those differ from the frozen R3, R4 or I1 documents, the frozen
documents govern.

## Order of work, as recorded in Git history

1. Narrow audits (`c1-20261004-a`, pre- and post-setup, `c1-20261005-final`).
2. Initial ceilings; two refused attempts retained; arithmetic-free monitor
   study; revised ceilings version 2 and amendment 2.1, each committed before
   the calibration it governs (`docs/C1_RESOURCE_CEILINGS_V2.md`).
3. Bounded CEML-CAL-1 on a calibration harness: ten arithmetic families and
   the checkpoint family, plus the NTFS interruption matrix.
4. Engineering decisions committed (`3602ba2`), before any engine source.
5. Production engine implemented (`5c354aa`), built offline from pinned inputs.
6. Every calibration family and the complete interruption matrix rerun on the
   production executable itself; decisions recomputed from that evidence and
   found identical.
7. Build manifest, machine profile and reports frozen; digests reproduced;
   sensitive-data gate passed on the staged set.

## Evidence totals

- 604 guarded children on the production executable (run `final-20261005-a`)
  and the same matrix earlier on the harness; one warm-up and five measured
  repetitions each (three for filesystem cases), all with exact agreement
  against an independent Python definition reference and positive route
  activation with zero fallback.
- Aggregate guarded child wall time 39.1 seconds of a 900-second ceiling.
- Eight refusals in total, all retained and indexed, none used as timing:
  the two initial attempts, three under run `a`, one under run `b`, two under
  the final run. Five explicit resumes were used; no case was refused twice.
- 27 local bundles bound by digest in `local_reports/BENCHMARK_BUNDLES.json`.

## Selections (see `local_reports/ENGINEERING_DECISIONS.json`)

| Question | Selection | Basis |
|---|---|---|
| Language and toolchain | C17, public GMP mpz, pinned Microsoft C | only complete offline family |
| Backend | `arith.gmp.public` | exact products at six sizes and three shapes; FLINT unavailable |
| Representation | `state.dense` | exact export, low bits and stepping; sparse not implemented |
| Macro route | `engine.hier_affine.explicit` | beats direct T and every table width by more than 5 percent on the three largest classes |
| Table width | none in the schedule | every width loses to hierarchical batching from 4096 bits up |
| Scheduler | divisor 2, cap 16384 | fifteen candidates performance-tied; stated tie choice, not a winner |
| Allocation | `alloc.copy` | tied with reuse on the macro route; smaller correctness surface |
| Build mode | portable-release | more than 5 percent faster than checked; no native mode exists |
| Parallelism | `parallel.single`, one thread | no auxiliary route implemented |
| Terminal handoff | `terminal.direct_t` | tied with odd-only; definition-level simplicity |
| Audit level | `audit.divisibility` | canary costs nothing measurable; modular audit left forcible |
| Checkpoint filesystem | supported | 78 of 78 scenarios, 13 of 13 adversarial cases, twice |
| Checkpoint strategy | `checkpoint.buffered`, 600-second cadence | no timing winner possible with three repetitions; simpler path |

## Implemented architecture

`src/` holds one C17 program, `ceml.exe`:

- `ceml_oracle.c` — separate direct C, T and odd-only definitions; shares no
  code with the engine;
- `ceml_engine.c` — exact T-boundary state, centralized unbounded counters,
  leaf blocks built from elementary T, explicit-coefficient binary splitting
  with P2-after-P1 composition, macro clamp `k <= bit_length(n)-1` with exact
  terminal handoff, divisibility and modular canaries, fail-closed route
  registry with REQUIRE and FORBID, validation-only fault points;
- `ceml_codec.c`, `ceml_sha3.c`, `ceml_start.c` — UENC, SHA3-256, SHAKE256,
  the frozen digest domains, CEML-CKPT-1 body and metadata, strict manifest
  decoding, result emission and the `ceml-start-v1` adapter (exercised only on
  the frozen public vectors);
- `ceml_fs_win32.c`, `ceml_store.c` — filesystem adapter and the
  two-valid-generation store;
- `ceml_validate.c` — one callable target for each of the twelve V1 classes;
- `ceml_calibrate.c` — the bounded calibration child entry;
- `ceml_main.c` — commands and authorization gates.

`validate` refuses unless the programme status names V1. `prepare` and `run`
refuse unless it names E1 with scientific execution authorized. Under the
committed status all three refuse. `self-test` is a bounded developer mode of
the hooks; it is not V1 and proves nothing about V1.

## Limitations a reviewer should weigh

1. **Interpretations recorded before measurement.** A hierarchical case totals
   16384 steps as a sequence of macro constructions each within the I1 macro
   bound; a stricter reading caps the total at 4096. The decision-critical
   classes for the "more than 5 percent worse" test are the three largest.
   Multiplication shapes and sparse inputs use extended case indices.
2. **Scheduler choice is a tie choice.** A reviewer who lets a few KiB of
   allocator live bytes decide would select cap 1024 instead.
3. **Resource proxy.** Page input is non-specific; the ceilings were revised
   twice from observation. No temperature is available.
4. **Unprobed facts.** Instruction features, caches, topology and
   virtualization were not probed and are not inferred.
5. **Dependency closure.** GMP is a checksum-verified distribution binary, not
   rebuilt from source here; SDK components are pinned by version only.
6. **Durability.** Forced process termination only; no power-loss evidence.
7. **Scale.** Nothing here measures scientific-scale time or memory. The
   pinned LLP64 GMP counts bits in 32 bits, so states of 2^32 bits or more
   (about 1.29e9 decimal digits) are outside this build; the two largest
   provisional rungs would need a new build and profile event.
8. **Gated code.** `prepare` and `run` cannot be exercised end to end in C1;
   their pieces are covered only by the bounded self-test.
9. **Review.** C1 was executed by an automated agent. The PASS is its
   assessment and does not replace operator review.

## Reproduction

```powershell
python tools/c1/gmp_setup.py build
python tools/c1/gmp_setup.py offline-smoke
python tools/c1/engine_build.py
python tools/c1/c1_profile.py verify
python -m unittest discover -s tests/c1 -v
local\c1\engine\bin\ceml.exe status
```

`engine_build.py` reproduced `ceml.exe` byte for byte on every rebuild in this
session. Raw bundles remain under ignored `local/c1/benchmark_bundles/`.
