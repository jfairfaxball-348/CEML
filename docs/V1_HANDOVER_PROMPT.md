# V1-only handover prompt

Not active. This prompt may be used only after the operator has reviewed the
C1 package and committed a `PROGRAM_STATUS.md` transition whose authoritative
current phase is V1. Until then the engine's `validate` command refuses.

---

CEML-V1 — LOCAL IMPLEMENTATION VALIDATION ONLY

Repository: the CEML repository, `main`, at the reviewed commit whose
`PROGRAM_STATUS.md` names V1 as the authoritative current phase. Resolve and
report that commit SHA first and stop if the status does not authorize V1.

Read, in order: `PROGRAM_STATUS.md`, `PROJECT_CHARTER.md`, `AGENTS.md`,
`CLAUDE.md`, `docs/VALIDATION_PLAN.md`, `docs/REPRODUCIBILITY_VALIDATION_AUDIT.md`,
`docs/CHECKPOINT_SPEC.md`, `docs/RANDOMNESS_AND_REPRODUCIBILITY.md`,
`docs/SECURITY_AND_INTEGRITY.md`, `docs/CODEX_HANDOFF.md` sections 2, 3, 6 and
17, `schemas/validation_evidence.schema.json`, `docs/C1_COMPLETION.md`,
`local_reports/BUILD_MANIFEST.json`, `config/local_machine_profile.json`.

Scope: execute CEML-V1-SUITE-1 for exactly the engine, build and profile frozen
by C1, on the same machine. Nothing else.

Hard boundaries:

- Do not generate, request, reveal or use the scientific master seed. Only the
  public validation seed and the frozen public test vectors may be used.
- Do not derive, inspect or run a scientific start or any ladder rung. Do not
  freeze the ladder. Do not enter E1. Do not claim divergence from anything.
- Do not change the engine, flags, dependencies or profile. A defect found by
  V1 is a V1 failure to be reported; any fix is a new build and profile event
  that needs its own calibration and review before V1 is run again.
- Do not weaken any V1 class, the zero-unexplained-disagreement rule or any
  frozen semantic. Calibration records are not V1 evidence.

Steps:

1. Rebuild offline (`gmp_setup.py build`, `engine_build.py`) and confirm every
   artifact digest equals `BUILD_MANIFEST.json`; run `c1_profile.py verify`.
   Any mismatch is a provenance failure: stop.
2. Run `ceml.exe validate` (full suite) and `ceml_checked.exe validate`. Record
   per-class case and failure counts.
3. Supply what the in-process hooks do not: a definition oracle in a separately
   authored code path and language (Python direct C stepping) for the
   differential and fixture classes, including `2^44497-1`; fresh-process
   checkpoint stop and resume at several boundaries through `checkpoint` and
   `resume` with `v1-validation-` identities; independent recomputation of
   UENC, JCS and every domain vector; forced activation of every enabled route
   compared against the independent oracle; an applicable sanitizer or checker
   run of the checked build, or explicit recorded non-applicability.
4. Confirm every required injected fault is detected by its intended check.
5. Emit a schema-valid `CEML-VALIDATION-EVIDENCE-1` record bound to the
   protocol commit, engine commit, build digest and machine-profile digest,
   with its evidence digest, plus digests of retained raw logs.
6. Run the sensitive-data gate, review the staged diff, commit.
7. State exactly "CEML-V1 PASS" or "CEML-V1 FAIL" with the evidence digest.
   Update `PROGRAM_STATUS.md` only in the commit containing that evidence.
   Stop before E1 in either case.
