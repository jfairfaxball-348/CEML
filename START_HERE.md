# CEML — Start Here (post-P0)

CEML's active purpose is **gap-free exhaustive Collatz frontier verification**, not the former isolated extreme-magnitude random ladder. The previous programme is preserved at [the 2026-10-11 entry commit](https://github.com/jfairfaxball-348/CEML/tree/63fc41610603782eefc709139e6dcbdcca97b78f).

**Current gate:** L1 PASS, agent-assessed on 2026-10-12; the owner's acceptance is outstanding. The owner-authorised continuation froze the three-slot [CEML-FRONTIER-2 protocol](docs/FRONTIER_PROTOCOL_V2.md), implemented and tested it, had it independently reviewed in three passes, passed the OS-enforced network-blocked acceptance run on the owner's third attempt, and prepared the [RUN1 operator runbook](docs/RUN1_OPERATOR_RUNBOOK.md). The [version-2 acceptance record](docs/L1_V2_ACCEPTANCE.md) holds the evidence, its limits and the verdict. RUN1 is not authorised: it needs the owner's acceptance of L1 and then a separate explicit instruction. The [fresh-session prompt](NEXT_SESSION_PROMPT.md) describes that stage and authorises nothing. The first candidate's [L1 acceptance](docs/L1_ACCEPTANCE.md) measurements and all C1 gates remain preserved.

Read, in order:
1. `PROGRAM_STATUS.md`, `PROJECT_CHARTER.md`, `ROADMAP.md`, `AGENTS.md`;
2. `docs/L1_V2_ACCEPTANCE.md`, then the active contract `docs/FRONTIER_PROTOCOL_V2.md` with `schemas/frontier_*_v2.schema.json` and the research-only `config/frontier_snapshot_v2.json`;
3. the frozen history it amends: `docs/FRONTIER_PROTOCOL_V1.md`, `docs/P2_PROTOCOL_AUDIT.md`, `schemas/frontier_*_v1.schema.json`, `config/frontier_snapshot_v1.json`, `docs/L1_RECOVERY_V2_PROPOSAL.md`, `docs/L1_CONTINUATION_READY.md` and `docs/L1_ACCEPTANCE.md`;
4. `docs/P1_EXCLUSION_PROOFS.md`, `docs/P0_FRONTIER_AUDIT.md`, `docs/P0_REDUCTION_AUDIT.md`, `docs/P0_BATCH_MODEL.md`, `docs/CLAIM_POLICY.md`;
5. `docs/C1_COMPLETION.md`, `docs/CODEX_HANDOFF.md`, `docs/ALGORITHM_AUDIT.md` and historic CEML-SCI-1/CEML-CKPT-1 material for REUSE assessment only;
6. `NEXT_SESSION_PROMPT.md` for the next stage, which it describes and does not authorise, and `docs/RUN1_OPERATOR_RUNBOOK.md` only as a prepared, unauthorised package.

Priorities: source-pinned published vs operational frontiers; strict mathematical predecessor induction; proven mod 2/mod 3 exclusions and finite parity sieves; exact per-range accounting; smallest offline CPU-oriented verifier with fixed frontier snapshot, atomic records and independent reference oracle. Do not confuse a lower starting value, lower batch, old external basin or completed CEML predecessor; they support different stopping invariants.

Workstreams: A cloud research/governance; B one later focused local Codex implementation; C actual local CLI science, offline. See `ROADMAP.md`.

P2 and version-2 protocol documents are specification evidence. L1 evidence describes software tested, reviewed and accepted on small engineering fixtures. It is never science. `NEXT_SESSION_PROMPT.md` describes RUN1 as a separately owner-authorised stage and is not RUN1 authority.
