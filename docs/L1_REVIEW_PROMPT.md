# Bounded independent review prompt — CEML-L1 / CEML-FRONTIER-2

Give this whole file to a reviewer that did not write the code: a separate Claude Code session, another tool or a person. It was first used on 2026-10-11 by a review sub-agent against commit `638e332`; that run, its findings, their resolutions and its limits are recorded in `docs/L1_V2_ACCEPTANCE.md` section 5. Re-running it against the final pinned commit named there is the way to obtain a further independent opinion. A reviewer that only restates the author's notes has not reviewed anything.

## Your role and limits

You are reviewing engineering software for an offline Collatz interval verifier. You are not the author. Assume the author is wrong until the code shows otherwise.

- Work only in this repository checkout at the commit named by whoever invoked you. Record `git rev-parse HEAD` first and stop if the working tree is not clean.
- Read-only for every tracked file. Do not edit, stage, commit, push, merge, reset or check out anything.
- You may run the two test suites and small throwaway Python experiments. Put any file you create under your own scratch directory or under the ignored `local/frontier/` tree, and say what you created.
- Do not run `tools/l1/run_offline_acceptance.ps1 -Mode Run`, any elevated command, or anything that changes firewall, scheduler, adapter, power or system settings. `-Mode Preflight` is read-only and allowed.
- No network access, downloads or dependency changes.
- No science. Never scan, replay or certify any integer at or above 10000, never create `local/frontier/run1_authorization.json`, never change `PROGRAM_STATUS.md`, and never run the `pilot`, `resume`, `prepare-authority` or `prepare-manifest` commands except to observe that they refuse.

## Read first

1. `PROGRAM_STATUS.md`, `AGENTS.md`, `docs/L1_CONTINUATION_READY.md`, `docs/L1_RECOVERY_V2_PROPOSAL.md`.
2. The frozen version-1 contract: `docs/FRONTIER_PROTOCOL_V1.md`, `docs/P2_PROTOCOL_AUDIT.md`, `docs/P1_EXCLUSION_PROOFS.md`, `schemas/frontier_*_v1.schema.json`, `config/frontier_snapshot_v1.json`.
3. The version-2 contract under review: `docs/FRONTIER_PROTOCOL_V2.md`, `schemas/frontier_*_v2.schema.json`, `config/frontier_snapshot_v2.json`.
4. The implementation: `tools/frontier/ceml_frontier.py`, `tools/frontier/reference.py`, `tools/frontier/f1_build.py`, `src/frontier_main.c`, `src/frontier_worker.c`, `src/frontier_worker.h`.
5. The tests: every file in `tests/frontier/` and `tests/l1/`.
6. The acceptance harness: `tools/l1/offline_acceptance.py`, `tools/l1/run_offline_acceptance.ps1`.
7. The operator package: `docs/RUN1_OPERATOR_RUNBOOK.md`.

## Questions to answer, each with evidence

**A. Contract.** Is version 2 complete and unambiguous on its own for records, canonical bytes, digest domains, genesis, the three-slot store, recovery, the final certificate and claims? Does it change any mathematics, rule, bound or trust tier relative to version 1? Are the version-1 files byte-identical to `origin/main` (`git diff origin/main -- docs/FRONTIER_PROTOCOL_V1.md docs/P2_PROTOCOL_AUDIT.md schemas/*_v1.schema.json config/frontier_snapshot_v1.json` must be empty)? Is any genesis or digest definition circular?

**B. Recovery soundness.** Work through protocol section 4.5 yourself before reading `CheckpointStore.recover`. For every combination of intact, damaged and absent slots at newest generations 0 to 6, decide what must happen, then compare with the code and with the model in `tests/frontier/test_recovery.py`. Look specifically for: a state that is accepted but should refuse; a state where a write could destroy one of the last two authenticated generations; a way to make a self-hashed contradictory record count as merely damaged; a way a checkpoint could advance over pending work; a way a damaged or foreign file could be promoted; any path where an orphan, a relaxed hash check or a missing parent is tolerated. State whether refusing in the remaining cases is the conservative choice.

**C. Chain and certificate integrity.** Can a certificate be committed without a complete second Python replay of every integer? Can an uncommitted, damaged, forked, duplicated, overlapping or cross-version predecessor be extended? Can a version-1 record, digest or genesis be spliced into a version-2 chain? Can `certificate.json` ever be replaced? Does every read re-verify canonical bytes and digests?

**D. Gates.** Can any command scan a frontier integer while `PROGRAM_STATUS.md` says L1? Check the Python gate (`run1_status`, `run1_gate`, `l1_gate`, `consume_native`) and the native gate (`scan_authority`). Can `L1-NONSCIENTIFIC` fixtures become science, or science be disguised as a fixture? Does any tool fill in the operator's acknowledgement or authority for them? Do `prepare-authority` and `prepare-manifest` refuse outside RUN1 status?

**E. Native worker.** Re-check exact arithmetic: no machine-width value for an endpoint or iterate, range-proved budget conversions under LLP64, the bounded allocator, exact divisibility before each `mpz_divexact_ui`, and that an exhausted start emits no success frame. The worker source should be unchanged from the previous L1 commit; confirm with `git diff c7b0249 -- src/`.

**F. Build and identity.** Does `f1_build.py` have any download or extraction path? Are all version-2 contract files, both snapshots and all eight schemas build inputs? Is hashing LF-normalised text safe for every input, including the canonical record files? Is caching the located compiler environment per process safe given that the tool binaries are re-hashed on each call?

**G. Tests.** Run `python -m unittest discover -s tests/frontier` and `python -m unittest discover -s tests/l1` (a current build is required: `python tools/frontier/f1_build.py`). Report totals, skips and failures. Then judge adequacy: do the tests have teeth, are any assertions vacuous, is anything named in protocol section 5 items 8 to 14 untested, and does any test compute a first descent for an integer at or above 2^64 (it must not)?

**H. Elevated launcher.** Without running it elevated: can any failure path leave the two block rules in place without the SYSTEM watchdog? Does it touch any rule, profile, adapter or task other than its own two rules and one task? Can it report `OS-BLOCKED-ENGINEERING-CHECKS-PASS` without the checks having run under verified blocking and verified restoration? Are the 20-minute child limit and the 25-minute watchdog consistent?

**I. Operator runbook.** Follow every command in `docs/RUN1_OPERATOR_RUNBOOK.md` against the argument parser in `ceml_frontier.py`. Report any command that would not parse, any step that needs code work, any claim the evidence does not support, and any place where the runbook acknowledges or authorises something on the owner's behalf.

## Report format

Start with the commit you reviewed, what you ran and the suite totals. Then list findings, most severe first:

`[BLOCKER | MAJOR | MINOR | NOTE] file:line — one-sentence defect. Scenario: concrete inputs or state leading to the wrong outcome. Suggested fix.`

BLOCKER means an unsound acceptance, a possible promotion of unverified work, a gate bypass or a way to leave the machine blocked. MAJOR means a contract and code disagreement or a required behaviour with no effective test. Finish with one line per section A to I: `SOUND`, `SOUND WITH FINDINGS` or `NOT SOUND`, and a final sentence saying whether, in your judgement, the engineering is acceptable once the listed findings are resolved. Say plainly what you did not check.
