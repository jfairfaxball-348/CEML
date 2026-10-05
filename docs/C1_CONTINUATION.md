# C1 continuation after authorized GMP setup

Stage: **hardware characterization**. **CEML-C1 REMAINS OPEN.**

The operator explicitly authorized acquisition, installation, builds and required
setup on 2026-10-05. This authorization persists; do not ask again for the same
necessary dependency actions. C1 scientific/V1 prohibitions remain unchanged.

## Completed evidence

- Baseline I1 remains authoritative. The initial refusal is preserved in commit
  `26773afae7ecd322f4a6d60ace790a83fcfa91fd`.
- Fresh narrow audits bracketed setup. Post-setup available memory was about
  6.78 GB; the existing AC and zero sleep-index configuration remained observed.
- Pinned GMP 6.3.0-2 UCRT64 binary and matching source material were acquired.
  The published binary checksum matched. Existing MSVC and SDK tools compiled
  an exact public-C arithmetic/import-export smoke test successfully.
- A strict offline rebuild reproduced the smoke executable byte for byte. The
  exact candidate pin is `config/c1_gmp_pin.toml`; approved source/package cache
  material remains under ignored `local/c1/cache/sha256/`.
- Source commit `dbbeadf` contains the bounded native route harness. The first
  1024-bit width-4 warm-up matched the definition reference with 64 block
  activations and zero fallback, but its resource check failed. It is retained
  as invalid `C1_RESOURCE_ABORT`. No measured repeats or timing winners exist.
- The unchanged paging-input ceiling is 100 pages per second. The post-child
  observation was about 1917. This proxy includes mapped-file reads and used a
  short interval; it is not proof of pagefile pressure. CPU/RSS zeros in this
  invalid raw record are abort placeholders, not accepted observations.

No production architecture, checkpoint strategy, final BUILD_MANIFEST or local
machine profile is selected/frozen. No checkpoint interruption matrix ran.
PROGRAM_STATUS remains unchanged: C1 open; V1 and E1 not entered.

## Exact next task

Read AGENTS.md, PROGRAM_STATUS.md, PROJECT_CHARTER.md, R4/I1 and the original
read-order documents. Verify baseline ancestry and inspect the current reports,
decisions, pin, resource ceilings and retained benchmark bundle.

1. Recheck the pinned offline candidate with `gmp_setup.py build` and
   `gmp_setup.py offline-smoke`. No acquisition is needed for this established
   candidate; authorized acquisition remains available for genuinely needed
   components. Keep any further environment changes explicit and rerun affected
   observations/calibration.
2. Investigate the resource refusal with narrow, bounded observations: compare
   PDH measurement intervals and idle/short-load pressure without collecting
   inventories. Retain the rejected warm-up unchanged. Establish whether the
   observed burst was transient mapped-file activity or sustained pressure;
   record uncertainty rather than guessing. Any changed monitor method or
   ceiling requires an explicit observation-backed engineering decision before
   affected calibration. Do not merely rerun until a favorable sample appears.
3. Review/enforce the guard, including timeout, Job memory, parent-loss cleanup,
   missing-monitor refusal and aggregate-budget behavior. Preserve the charged
   local budget. A new comparison run must have a distinct retained bundle and
   source/build identity; the current driver deliberately refuses overwriting
   its existing bundle. Reruns must obey I1's total bounds and retained-invalid
   evidence rules. Tool checks are not V1.
4. Re-establish safe operand/work limits before further non-trivial calibration.
   The current 4096-bit ceiling only admits two prescribed route-crossover
   classes and excludes the hierarchical/allocation grids. It cannot establish
   the required three-class timing winner. If local observations justify a
   broader subset within I1, record the revised ceilings before using it.
   Otherwise preserve explicit no-winner decisions.
5. Run applicable CEML-CAL-1 comparisons in exact family/size/candidate/case/repeat
   order with independent correctness, positive REQUIRE activation, zero
   fallback, complete provenance, resource records and the required repeat,
   median/MAD, 5-percent/noise/tie rules. No absent row may be called a tie.
6. Establish the intended NTFS checkpoint adapter's documented durability
   semantics and all bounded CEML-CKPT-1 flush/reopen/promotion/retention/recovery
   tests. Force interruption at all R4 section 14.5 phases and use fresh-process
   recovery. I1's reference to R4 section 10 is stale. Successful process tests
   alone do not establish power-loss behavior. Do not perform destructive
   power-cut testing.
7. Only after prerequisite selections are justified, change the stage to
   implementation and implement all required engine boundaries, invariants,
   CLI authorization gates and twelve future V1 hooks. Build offline with full
   source/toolchain/SDK/dependency closure and rerun invalidated calibration.
8. Produce every required sanitized C1 report, complete final build manifest
   and machine profile; reproduce digests, validate schemas, scan exact staged
   bytes, review the diff and commit. Update PROGRAM_STATUS only in the commit
   containing evidence satisfying every C1 exit condition. Stop before V1/E1.

## Current commands and evidence conventions

```powershell
& tools\c1\collect_windows.ps1 -AuditRun c1-next-audit
& tools\c1\collect_tools.ps1 -AuditRun c1-next-audit
python tools/c1/gmp_setup.py build
python tools/c1/gmp_setup.py offline-smoke
python tools/c1/engineering_codec.py self-test
python -m unittest discover -s tests/c1 -v
```

Audit observations use `local/c1/<audit-run>/`. Generic external-locator GMP
absence is scoped to those locators; it does not contradict the proven local
candidate. The old initial-refusal assembler cannot overwrite a later audit.
`dependency_report.py` is specific to the recorded setup/refusal event, not a
future successful session. Benchmark bundle member paths are filenames relative
to the bundle root, sorted lexicographically for the I1 bundle digest.

The exact staged gate is `python tools/c1/privacy_gate.py`, followed by staged
diff review and commit without changing the staged set. No permission request
is required to continue the already-authorized C1 work within these boundaries.
