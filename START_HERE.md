# CEML — Start Here (post-P0)

**Current PowerShell procedure:** `python C:\CEML\tools\operator\run_frontier.py X`. Change only the final number X. The command discovers and verifies the current committed endpoint and checks the next X integers, with the existing accepted chain assumption. The owner removed the separate-device backup requirement. See [current command](docs/RUN1_ONE_COMMAND.md); this procedure-edit request executes no batch.

**Latest published result:** 122 committed and verified batches, covering 1719984 integers through exclusive endpoint `2392518188130440462000`, conditional on the accepted author-reported operational base. See [RUN1 progress](docs/RUN1_PROGRESS.md). The offline runner logs locally; the separate publication command verifies and updates GitHub and the website feed.

**Latest RUN1 handoff (2026-10-12):** the three pilots (144, 1440, 14400 integers) and the owner's subsequent 100000-integer continuation committed and passed verification, replay and chain audit. The finite conditional chain now covers 115984 integers in 10 batches on the accepted author-reported operational base. See [RUN1 progress](docs/RUN1_PROGRESS.md). The owner ran the [single CLI command](docs/RUN1_ONE_COMMAND.md) successfully; its original default pilot-3 anchor is now stale, and no additional run is authorised by this record. The later owner exception recorded in `AGENTS.md` supersedes the pilot owner-only wording below solely for those completed pilots.

CEML's active purpose is **gap-free exhaustive Collatz frontier verification**, not the former isolated extreme-magnitude random ladder. The previous programme is preserved at [the 2026-10-11 entry commit](https://github.com/jfairfaxball-348/CEML/tree/63fc41610603782eefc709139e6dcbdcca97b78f).

**Current gate:** RUN1, authorised by the owner on 2026-10-12 on the operational base. The owner runs it offline, one batch at a time, under the [RUN1 operator runbook](docs/RUN1_OPERATOR_RUNBOOK.md); agents check, explain and record, and never run a batch or type an acknowledgement. `PROGRAM_STATUS.md` holds the instruction and what the base means. L1 is PASS, agent-assessed and owner-accepted on 2026-10-12: the [version-2 acceptance record](docs/L1_V2_ACCEPTANCE.md) holds that evidence and its limits for the frozen three-slot [CEML-FRONTIER-2 protocol](docs/FRONTIER_PROTOCOL_V2.md). The [fresh-session prompt](NEXT_SESSION_PROMPT.md) says what a session may do during RUN1. The first candidate's [L1 acceptance](docs/L1_ACCEPTANCE.md) measurements and all C1 gates remain preserved.

Read, in order:
1. `PROGRAM_STATUS.md`, `PROJECT_CHARTER.md`, `ROADMAP.md`, `AGENTS.md`;
2. `docs/L1_V2_ACCEPTANCE.md`, then the active contract `docs/FRONTIER_PROTOCOL_V2.md` with `schemas/frontier_*_v2.schema.json` and the research-only `config/frontier_snapshot_v2.json`;
3. the frozen history it amends: `docs/FRONTIER_PROTOCOL_V1.md`, `docs/P2_PROTOCOL_AUDIT.md`, `schemas/frontier_*_v1.schema.json`, `config/frontier_snapshot_v1.json`, `docs/L1_RECOVERY_V2_PROPOSAL.md`, `docs/L1_CONTINUATION_READY.md` and `docs/L1_ACCEPTANCE.md`;
4. `docs/P1_EXCLUSION_PROOFS.md`, `docs/P0_FRONTIER_AUDIT.md`, `docs/P0_REDUCTION_AUDIT.md`, `docs/P0_BATCH_MODEL.md`, `docs/CLAIM_POLICY.md`;
5. `docs/C1_COMPLETION.md`, `docs/CODEX_HANDOFF.md`, `docs/ALGORITHM_AUDIT.md` and historic CEML-SCI-1/CEML-CKPT-1 material for REUSE assessment only;
6. `NEXT_SESSION_PROMPT.md` for what a session may do during RUN1, and `docs/RUN1_OPERATOR_RUNBOOK.md`, the procedure the owner follows.

Priorities: source-pinned published vs operational frontiers; strict mathematical predecessor induction; proven mod 2/mod 3 exclusions and finite parity sieves; exact per-range accounting; smallest offline CPU-oriented verifier with fixed frontier snapshot, atomic records and independent reference oracle. Do not confuse a lower starting value, lower batch, old external basin or completed CEML predecessor; they support different stopping invariants.

Workstreams: A cloud research/governance; B one later focused local Codex implementation; C actual local CLI science, offline. See `ROADMAP.md`.

P2 and version-2 protocol documents are specification evidence. L1 evidence describes software tested, reviewed and accepted on small engineering fixtures. It is never science. `NEXT_SESSION_PROMPT.md` describes what a session may do during RUN1 and adds no authority of its own.
