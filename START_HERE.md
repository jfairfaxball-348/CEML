# CEML — Start Here (post-P0)

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
