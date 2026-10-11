# Finish the owner-authorised L1 engineering continuation — not RUN1

Work in `C:\CEML`. Complete implementation, review, acceptance and the operator handoff within the existing single L1 attempt. Persist through routine fixes; do not stop at a plan or request already-granted permission again. The owner authorised the agent to choose the recovery amendment and prepare/perform local engineering, including Windows elevation with an owner UAC click/admin command if needed. Read `docs/L1_CONTINUATION_READY.md` for the recorded decision. The selected amendment is the smallest three-slot **CEML-FRONTIER-2** design. No repeat amendment approval is needed; invoking this prompt starts the fresh focused continuation.

Only engineering/test fixtures are authorised. RUN1, science/frontier scans, external-base acceptance, old V1/E1, legacy ungating, new exclusions/dependencies, GPU/parallel scientific work and optimisation programmes remain denied. Preserve all historical evidence, frozen v1 bytes, dependency pins and guards.

Pin live main; inspect local status, draft PR #5/head/commits/merge and actual checks/Actions before edits. Reuse `codex/l1-offline-frontier` if suitable; do not reset owner changes or run main's historical P2-only prompt. Read PROGRAM_STATUS.md, AGENTS.md, START_HERE.md, ROADMAP.md, L1 acceptance/recovery/continuation-ready documents, P0/P1 proofs, complete frozen v1 protocol/audit/four schemas, candidate source/tests and necessary C1 pins/build primitives. Current status controls old phase strings. Verify CI rather than invent it.

## Finish all remaining engineering

1. Specify/freeze new v2 protocol and four matching schemas/constants/digest domains, plus a separately versioned canonical research snapshot with provenance. Preserve v1 bytes/digest. Specify three rotating slots retaining the last two authenticated generations while replacing the oldest; recovery via verified adjacent pairs, root handling and strict missing-parent/fork/corrupt-history refusal. Avoid circular genesis hashes; refuse cross-version splicing. Keep mathematics, full independent replay, one worker, bounds, immutable certificates and trust tiers.
2. Implement only the amendment in driver/checker/native/build inputs/CLI/tests as needed. Test every relevant state through at least generation 4, corrupt/missing predecessor/newest slots, duplicate/forks, all write/flush/rename crash points, pending exclusion, full prefix native/Python replay and cold/resume certificate equality. Never relax orphan/hash checks. No science.
3. Review final contract/code/gates/integrity with an available independent reviewer/tool. Record provenance/findings; a second self-read is not independent acceptance. If the operator uses separate Claude Code, provide a bounded review prompt against the same pinned commit; never pretend it ran. Fix/retest findings. Do not spawn agents merely because available. If independent review is unavailable, complete the other deliverables and accurately leave that one acceptance gate OPEN with the exact review prompt.
4. Run affected checks and the complete final suite with zero skips; build release/checked workers from retained pins and prove clean reproduction. Review `tools/l1/` and `tests/l1/`; adapt the prepared command plan for final v2, include all new recovery tests and validate elevated refusal/restoration behavior. No downloads or dependency changes.
5. Perform actual OS-blocked acceptance with `tools/l1/run_offline_acceptance.ps1` following `L1_CONTINUATION_READY.md`. Preflight passed; elevated rules/watchdog/build acceptance remain NOT_RUN. Compute fresh reviewed source/launcher hashes and launch detached with `Start-Process -Verb RunAs -WindowStyle Hidden`; owner may accept UAC. Notify before temporary machine-wide network blocking. The local process continues without chat and restores its rules; 25-minute SYSTEM/boot cleanup backs up normal restoration, child limit 20 minutes. If elevation fails, provide the exact administrator command. Require matching checks/isolation records, zero-skipped suite, stable source/build identities, measured calibration and verified restoration. Do not substitute Python hooks/preflight. Failure leaves OPEN; fix/rerun as justified.
6. Produce a complete pinned offline operator package/runbook so RUN1 needs no routine code work: retained dependencies; source/build/snapshot identities; published/operational baseline choices and assumptions; explicit fresh RUN1 authority/acknowledgement template; 144-start initial pilot; finite budgets; verify/resume/ledger/replay/backup/stop/contiguous-extension commands; refusal diagnostics; independent-reproduction handoff and truthful claims. Test only with synthetic fixtures. Do not acknowledge RUN1 on the owner's behalf or execute science.

Existing commands (adapt for final v2):

```powershell
python tools/frontier/f1_build.py --show-command
python tools/frontier/f1_build.py
python tools/frontier/f1_build.py --verify
python -m unittest discover -s tests/frontier -v
python tools/frontier/ceml_frontier.py rules
python tools/frontier/ceml_frontier.py snapshot --file config/frontier_snapshot_v1.json
python tools/frontier/ceml_frontier.py selftest
python -m unittest discover -s tests/l1 -v
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools/l1/run_offline_acceptance.ps1 -Mode Preflight
```

The unchanged tools/c1/gmp_setup.py build and offline-smoke commands refuse outside C1; this was observed and preserved. The distinct standard-library f1_build.py checks the retained archives, extracted header/DLL and tools, reproduces the original pinned smoke executable, and never imports the acquisition path. Do not change legacy status/guards to make the old commands succeed.

## Exit discipline

Capture exact final source/build/test/commit identities, measured calibration, reviewer provenance and OS policy/probe/restoration evidence. Keep raw/path-bearing logs ignored; no secrets/hardware IDs/per-integer tracked records. Runtime never fetches, uploads, changes source or auto-commits. Update evidence/status/start/roadmap/prompt only to supported outcomes, commit required evidence, update the branch/PR and inspect actual checks. L1 PASS requires all amended obligations, actual OS-isolated acceptance and independent acceptance; merge alone proves none of these. Do not auto-merge a draft.

Finish with whether engineering is actually complete, the exact operator package/runbook and any unavoidable owner action. If review/elevation cannot be supplied, finish every other concrete deliverable and leave the minimal remaining gate accurately OPEN. Only after accepted L1 PASS may the next prompt describe separately owner-authorised RUN1. No science is preauthorised or executed here.
