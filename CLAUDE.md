# CLAUDE.md — Claude Code adapter for CEML

This file is an **adapter and index** for Claude Code sessions. It is not a
scientific specification and freezes nothing. If anything here differs from an
original repository document, **the original document is authoritative** and
this file is wrong.

Authoritative documents, never rewritten, weakened, reinterpreted or superseded
by this adapter:

- `AGENTS.md` (agent governance; read it completely every session)
- `PROGRAM_STATUS.md` (the only statement of the current gate)
- `PROJECT_CHARTER.md`
- `docs/HARDWARE_AUDIT_SPEC.md` (frozen R4 contract)
- `docs/CODEX_HANDOFF.md` (frozen I1 specification, CEML-CAL-1 rules)
- CEML-SCI-1 and CEML-CKPT-1 documents: `docs/EXPERIMENT_PROTOCOL.md`,
  `docs/RANDOMNESS_AND_REPRODUCIBILITY.md`, `docs/CHECKPOINT_SPEC.md`,
  `docs/RESULT_SCHEMA.md`, `docs/VALIDATION_PLAN.md`,
  `docs/SECURITY_AND_INTEGRITY.md`, `docs/CLAIM_POLICY.md`
- everything under `schemas/` and `config/calibration_suite_v1.json`

## First actions in every session

1. `git fetch`, confirm the expected baseline commit is an ancestor of `HEAD`,
   confirm the working tree is clean.
2. Read `PROGRAM_STATUS.md`, `PROJECT_CHARTER.md`, `AGENTS.md` and the current
   gate specification before changing any file. For C1 the controlling
   specifications are `docs/CODEX_HANDOFF.md` and `docs/HARDWARE_AUDIT_SPEC.md`.
3. Follow the full read order in `START_HERE.md`, then the C1 handover
   documents: `NEXT_SESSION_PROMPT.md`, `docs/C1_CONTINUATION.md`,
   `docs/C1_RESOURCE_CEILINGS.md`, `docs/C1_DEPENDENCY_SETUP.md`,
   `docs/C1_MANUAL_CHECK.md` and any later `docs/C1_*.md` file.
4. State which single stage the work belongs to: research, hardware
   characterization, implementation, validation, scientific execution, anomaly
   investigation, or proof/certification.

## Current gate (summary only; `PROGRAM_STATUS.md` governs)

C1 — local hardware audit and implementation — produced its package and
stopped for operator review (see `docs/C1_COMPLETION.md`). R1, R2, R3, R4 and
I1 passed. V1 and E1 are not entered; `docs/V1_HANDOVER_PROMPT.md` is inactive
until a reviewed status transition names V1. Scientific execution and scientific
master-seed generation are denied.

Mandatory C1 order (I1 section 1):
audit -> resource ceilings -> bounded CEML-CAL-1 -> evidence-backed decisions ->
implementation -> offline pinned build -> checkpoint-filesystem proof ->
sanitized build manifest and machine profile -> commit -> stop before V1.

## Hard prohibitions

Never, unless a later gate recorded in `PROGRAM_STATUS.md` authorizes it:

- generate, request, reveal or use the scientific master seed;
- derive, inspect, rank, reroll or run a scientific start;
- run a scientific or giant trajectory;
- freeze the final magnitude ladder;
- claim divergence from runtime, magnitude, peaks or failure to finish;
- enter or claim V1 or E1;
- change exact C/T/U semantics, first-1 termination, counter accounting,
  canonicalization, digest domains, CEML-CKPT-1 semantics, result statuses,
  anomaly policy or V1 acceptance;
- use private GMP or FLINT interfaces, raw limb dumps or any I1-rejected
  candidate;
- invent a measurement, substitute a product specification or another
  machine's benchmark, or interpolate an unmeasured crossover;
- treat a refused, aborted or incorrect benchmark as performance evidence;
- rerun a resource refusal repeatedly until a favorable sample appears;
- silently install, upgrade or substitute a dependency (the operator's
  2026-10-05 authorization covers explicit, pinned, provenance-recorded
  acquisition needed to finish C1 — see `docs/C1_DEPENDENCY_SETUP.md`);
- change global power, swap, firmware or thermal policy;
- commit private identifiers, credentials, machine or account names, network
  addresses, serials, stable device or filesystem identifiers, or unrelated
  paths. Hashing such a value is not sanitization.

## Evidence discipline

- C1 records are exactly one of OBSERVED_FACT, CALIBRATION_MEASUREMENT,
  ENGINEERING_DECISION, UNAVAILABLE_OR_UNSUPPORTED.
- A hardware observation is not a benchmark; a benchmark is not V1; V1 is not
  scientific execution.
- A performance datum counts only with exact reference-digest agreement,
  positive activation of the requested route, zero fallback, valid resource
  observations and complete build provenance.
- Timing winners need at least three size classes, five valid measured repeats
  per class, and the I1 section 11.13 thresholds (5 percent, MAD at most 10
  percent of the median). Otherwise record a tie, a tie-break under the I1
  order, or an explicit no-winner refusal.
- Invalid and aborted records are retained, never overwritten or discarded.
- Process-interruption tests do not prove power-loss behaviour; say so.

## Remote or cloud sessions

Machine-local evidence (hardware observations, calibration timing, NTFS
checkpoint durability, the frozen machine profile) can only be produced on the
dedicated local machine. A session running anywhere else may prepare and test
portable code and documentation, but must not claim local calibration,
checkpoint durability or C1 completion. It must leave exact commands for the
operator and incorporate only returned sanitized evidence.

## Repository map

| Path | Role |
|---|---|
| `docs/` | Frozen audits, protocol, specifications and C1 working notes |
| `schemas/` | Frozen R3 and I1 JSON schemas |
| `config/` | CEML-CAL-1 suite, dependency pins, later the machine profile |
| `tools/c1/` | C1 audit adapters, calibration harness, privacy gate, reports |
| `tests/c1/` | Bounded developer tests for the C1 tooling (not V1) |
| `src/` | Production engine, only after its prerequisite C1 decisions |
| `local_reports/` | Committed sanitized C1 reports (see `.gitignore` allowlist) |
| `local/` | Ignored raw local evidence, caches and build outputs |

## Routine commands (Windows, repository root)

```powershell
python tools/c1/gmp_setup.py build
python tools/c1/gmp_setup.py offline-smoke
python tools/c1/engineering_codec.py self-test
python -m unittest discover -s tests/c1 -v
powershell -NoProfile -ExecutionPolicy Bypass -File tools\c1\manual_check.ps1 -PressureOnly
```

Only the explicit `acquire` subcommand of a setup tool may use the network.
Bounded calibration drivers accept no arbitrary seed, start, size or work
input, charge a shared local budget and stop at the first refusal.

## Commit procedure

1. Stage exactly the intended files; never `git add -A` blindly.
2. `python tools/c1/privacy_gate.py` must print PASS for the staged set.
3. `git diff --cached --check` and a full read of `git diff --cached`.
4. Commit without changing the staged set, then push.
5. Update `PROGRAM_STATUS.md` only in the commit that contains evidence
   satisfying every exit condition of the gate being closed.
6. Corrections are additive history; never rewrite published history.

## Stopping rule

C1 ends with a report stating either "CEML-C1 PASS" or "CEML-C1 REMAINS OPEN".
If it remains open, commit all safe progress and write a continuation document
naming the missing local action and evidence. Do not execute V1.
