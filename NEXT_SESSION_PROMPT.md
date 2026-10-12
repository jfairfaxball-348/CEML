# Close CEML-L1 on the OS-blocked acceptance evidence — not RUN1

Work in `C:\CEML` on branch `codex/l1-offline-frontier` (draft PR #5). The CEML-FRONTIER-2 contract, implementation, tests, independent review and offline operator package are complete and committed. Read `docs/L1_V2_ACCEPTANCE.md` first; it is the record this prompt continues. Exactly one gate is open: the OS-enforced network-blocked acceptance run. Only the owner can start it, because it changes Windows Firewall rules and registers a SYSTEM task.

Only engineering fixtures are authorised. RUN1, any scientific or frontier scan, external-base acceptance, old V1/E1, legacy ungating, new exclusions or dependencies, GPU or parallel work and optimisation programmes remain denied. Preserve all historical evidence, the frozen version-1 and version-2 contract bytes, the dependency pins and every guard.

The reviewed source identity binds `src/frontier_*`, `src/ceml_oracle.*`, `tools/frontier/`, `tests/frontier/`, `tools/l1/`, `tests/l1/`, `schemas/frontier_*`, `config/frontier_snapshot_*`, both dependency pins, `docs/FRONTIER_PROTOCOL_V*.md`, `docs/P1_EXCLUSION_PROOFS.md`, `docs/P2_PROTOCOL_AUDIT.md` and `tools/c1/gmp_smoke.c`. Do not edit any of them unless a recorded failure requires it. Any such edit needs fresh hashes and a fresh run, and anything beyond a trivial fix needs the bounded review of `docs/L1_REVIEW_PROMPT.md` again.

## Steps

1. Pin live `main`. Inspect local status, PR #5 head, commits, mergeability, actual checks and Actions before any edit. Confirm `HEAD` is the source commit named in `docs/L1_V2_ACCEPTANCE.md` section 7 or a descendant that changes no identity-bound file, and that the tree is clean. Verify CI rather than invent it; the repository had no workflows and zero runs.
2. If the owner has not run the acceptance yet: run `-Mode Preflight`, require its `source_sha256` to equal the reviewed value in section 7, and give the owner the exact command of section 6 with those hashes. Do not start the elevated process yourself. Say plainly that the whole machine, this chat included, loses network for up to about 25 minutes, and give the emergency restore line.
3. After the owner has run it: take the newest `local/frontier/os-offline/<id>/` that contains both `isolation.json` and `checks.json`. Require all of:
   - `isolation.json`: `status` is `OS-BLOCKED-ENGINEERING-CHECKS-PASS`; `connected_baseline`, `os_rules_verified`, `rules_removed`, `watchdog_removed`, `connected_after_restore` and `checks_passed` are true; `child_exit_code` is `"0"`; `last_stage` is `completed`; the source and launcher hashes equal the reviewed ones.
   - `checks.json`: `status` is `ENGINEERING-CHECKS-PASS` with the same source hash; both suites `PASS` with zero skips and zero expected failures and the test totals of section 3; three equal build digests equal to section 7; calibration `fixtures_pass`.
   - A read-only check that no `CEML-L1Offline-*` firewall rule or scheduled task remains.
   A miss on any item is a FAIL. Keep the evidence, record the failure honestly, fix only what is justified, obtain fresh hashes and ask for another run. A Python hook or the unisolated rehearsal never substitutes.
4. Record the outcome. Fill sections 6 and 10 of `docs/L1_V2_ACCEPTANCE.md` with the observed path-free values. Replace the calibration table in `docs/RUN1_OPERATOR_RUNBOOK.md` section 12 with the OS-blocked figures. Update `PROGRAM_STATUS.md`, `START_HERE.md`, `ROADMAP.md` and this prompt only to the supported outcome. L1 PASS requires every obligation listed in section 10. Keep raw and path-bearing logs ignored. Commit the evidence, push, update PR #5 and inspect the actual checks. A merge proves none of this. Do not auto-merge a draft.
5. Only after an accepted L1 PASS may the next prompt describe RUN1 as a separately owner-authorised stage that follows `docs/RUN1_OPERATOR_RUNBOOK.md`. It must not authorise RUN1, acknowledge any base or start any scan.

## Exit discipline

Finish with the verdict, the exact evidence identifiers, and any owner action still needed. If the run cannot be supplied, leave that one gate accurately OPEN. No science is preauthorised or executed here.
