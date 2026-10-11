# CEML — Start Here (post-P0)

CEML's active purpose is **gap-free exhaustive Collatz frontier verification**, not the former isolated extreme-magnitude random ladder. The previous programme is preserved at [the 2026-10-11 entry commit](https://github.com/jfairfaxball-348/CEML/tree/63fc41610603782eefc709139e6dcbdcca97b78f).

**Current gate:** L1 OPEN after the owner-invoked implementation/test session. The separate verifier builds and its executed tests pass; later-generation recovery and OS-level network-isolated acceptance remain open. See [L1 acceptance](docs/L1_ACCEPTANCE.md) and the [prospective recovery amendment](docs/L1_RECOVERY_V2_PROPOSAL.md). **Only a fresh focused L1 continuation is next; RUN1 remains denied.** C1 and its gates remain unchanged.

Read, in order:
1. `PROGRAM_STATUS.md`, `PROJECT_CHARTER.md`, `ROADMAP.md`, `AGENTS.md`;
2. `docs/FRONTIER_PROTOCOL_V1.md`, `docs/P2_PROTOCOL_AUDIT.md`, new `schemas/frontier_*_v1.schema.json` and the research-only `config/frontier_snapshot_v1.json`;
3. `docs/P0_FRONTIER_AUDIT.md`, `docs/P0_REDUCTION_AUDIT.md`, `docs/P0_BATCH_MODEL.md`, `docs/CLAIM_POLICY.md`;
4. `docs/C1_COMPLETION.md`, `docs/CODEX_HANDOFF.md`, `docs/ALGORITHM_AUDIT.md` and historic CEML-SCI-1/CEML-CKPT-1 material for REUSE assessment only;
5. `NEXT_SESSION_PROMPT.md` for the single next authorised session.

Priorities: source-pinned published vs operational frontiers; strict mathematical predecessor induction; proven mod 2/mod 3 exclusions and finite parity sieves; exact per-range accounting; smallest offline CPU-oriented verifier with fixed frontier snapshot, atomic records and independent reference oracle. Do not confuse a lower starting value, lower batch, old external basin or completed CEML predecessor; they support different stopping invariants.

Workstreams: A cloud research/governance; B one later focused local Codex implementation; C actual local CLI science, offline. See `ROADMAP.md`.

P2 documents are specification evidence. L1 evidence describes a separate tested candidate, not accepted software or science. `NEXT_SESSION_PROMPT.md` contains the focused OPEN-gate continuation, not RUN1 authority.
