# CEML Programme Status

**Authoritative current phase:** L1 — PASS, AGENT-ASSESSED ON RECORDED EVIDENCE AND OWNER-ACCEPTED 2026-10-12; RUN1 NOT AUTHORISED
**Scientific execution authorization:** DENIED (including any L1 science pilot; RUN1 remains separately gated)
**Local Codex / local machine access authorization:** FOCUSED L1 CONTINUATION COMPLETE AND OWNER-ACCEPTED 2026-10-12; NO FURTHER LOCAL SESSION IS AUTHORISED UNTIL THE OWNER SEPARATELY INSTRUCTS RUN1
**New frontier scientific protocol:** CEML-FRONTIER-2 FROZEN (THREE-SLOT RECOVERY); CEML-FRONTIER-1 FROZEN, UNCHANGED, RETAINED AS HISTORY, NEVER RUNNABLE
**New batch-verifier implementation:** VERSION-2 GMP/PYTHON VERIFIER BUILT, TESTED, INDEPENDENTLY REVIEWED, ACCEPTED UNDER OS-ENFORCED NETWORK BLOCKING AND OWNER-ACCEPTED (L1 PASS); NEVER RUN ON A FRONTIER INTEGER; RUN1 NOT AUTHORISED
**Old ladder status:** SUPERSEDED AS ACTIVE TARGET; HISTORICAL EVIDENCE RETAINED
**Old scientific master-seed generation:** DENIED
**Last P0 decision:** 2026-10-11 — owner-directed soft pivot

## L1 version-2 continuation — 2026-10-11 to 2026-10-12

The owner invoked the focused continuation on `codex/l1-offline-frontier` and authorised the three-slot amendment, an independent review sub-agent and temporary elevated network blocking for acceptance. The full record is [docs/L1_V2_ACCEPTANCE.md](docs/L1_V2_ACCEPTANCE.md). Nothing scientific was executed.

**Done and committed.** [CEML-FRONTIER-2](docs/FRONTIER_PROTOCOL_V2.md) is frozen with four new schemas, the `CEML-FRONTIER-2/` digest domain and a carried-forward snapshot that records its provenance from the frozen version-1 snapshot. The driver implements three rotating checkpoint slots with an empty-prefix root generation, strict recovery, cross-version refusal and operator commands. The native worker and every frozen version-1 file are byte-identical to before. The frontier suite has 171 tests and the launcher suite 27, all passing with zero skips; 55 of 56 deliberate defects were detected by the tests and the remaining one is a duplicated check; release and checked workers rebuild from the retained pins and reproduce exactly. An independent review sub-agent reviewed the pinned candidate and reported one blocker, three major and eight minor findings; all were resolved, and its confirmation pass on the fixes found them resolved. That pass raised two further minor findings and five notes, resolved in the final source commit and verified by the author's tests only. The reviewer is a sub-agent of the same model family as the author, not a human or a different tool. The offline operator package is [docs/RUN1_OPERATOR_RUNBOOK.md](docs/RUN1_OPERATOR_RUNBOOK.md).

**L1 PASS, agent-assessed, 2026-10-12.** The last open gate, the OS-enforced network-blocked build and acceptance run, was met on the owner's third attempt: run `387ae837`, 08:05:32Z to 08:08:08Z, status `OS-BLOCKED-ENGINEERING-CHECKS-PASS` on the reviewed identities, with blocking verified before and after the checks, 171 and 27 tests passing with zero skips, three identical build digests, and the rules and watchdog verified removed and connectivity observed again. The first attempt refused at its connectivity baseline before any change. The second stopped in the watchdog-registration stage on a launcher defect (a rule-name list that was one joined string) before any firewall rule or task existed; the defect was fixed and the elevated path is also exercised by a simulation. The review sub-agent then reviewed the final sources, cross-checked the evidence independently and judged that it supports recording a pass. "Agent-assessed" means the agent that wrote the software reached this verdict; no human has reviewed the code and no hosted CI exists. **The owner accepted the record on 2026-10-12** ("I'm happy with all that. Can you accept L1, commit, merge, push etc everything so we are ready to go."). Limits of the evidence are listed in the acceptance record, sections 6 and 9.

**One next gate.** RUN1, which is not authorised. It needs the owner's separate explicit instruction, base choice and personally typed acknowledgement, and follows [docs/RUN1_OPERATOR_RUNBOOK.md](docs/RUN1_OPERATOR_RUNBOOK.md); the [fresh-session prompt](NEXT_SESSION_PROMPT.md) describes that stage and authorises nothing. The owner's acceptance of L1 is not RUN1 authority. No scientific interval, accepted external base, frontier claim or V1/E1 execution exists. Any change to an identity-bound file ends the validity of the L1 evidence for the changed software. The sections below are retained history; where they name a next gate, this section supersedes them.

## Owner-authorised completion preparation — 2026-10-11

The owner has authorised the agent to choose the recovery amendment and prepare the next session to complete engineering, including Windows elevation/UAC or an administrator command for true OS-blocked acceptance. The chosen prospective design is three-slot **CEML-FRONTIER-2**. The owner-decision gate is resolved; v2 contracts/implementation and acceptance are still outstanding. This remains the focused continuation of the single L1 attempt, not RUN1. See [completion preparation](docs/L1_CONTINUATION_READY.md) and the updated [fresh-session prompt](NEXT_SESSION_PROMPT.md).

Standalone bounded OS-blocking/restoration launcher, standard-library acceptance helper and harness tests are prepared. Read-only Windows preflight PASS; 8 harness tests PASS, no skips. Elevated firewall/watchdog execution and OS-isolated build/acceptance remain NOT_RUN. No network policy changed. The next session must complete v2, required review/acceptance and the operator package; no extra routine engineering permission is required. Existing L1 evidence below is historical measurement, not a PASS or scientific result.

## L1 measured exit — 2026-10-11

The owner invoked main's `NEXT_SESSION_PROMPT.md` and subsequently directed continuation. Entry/live main and P2 PR #4 merge SHA were both `abd5d5bd0c6bb3a5cfbd1b83d52122b04d324016`; P2 merged 2026-10-11T12:52:38Z. Entry had no open PRs or Actions runs. The single local L1 attempt does not amend old C1 authority or authorise RUN1.

Separate C17/GMP release and checked workers compiled from exact offline pins. The Python standard-library driver/reference, full small-batch replay, canonical schemas/digests, atomic records, authority refusals and fault tests exist. A full 91-test run passed without skips; the final affected 9-test batch suite passed after adding the one-active-batch guard (92 distinct tests covered). Clean reproduction and Python network-denied build/selftest passed. Only small acceptance intervals and bounded high-bit identities executed. Details/hashes: [L1_ACCEPTANCE.md](docs/L1_ACCEPTANCE.md).

**L1 OPEN:** later-generation torn-checkpoint recovery cannot authenticate a missing parent using only the two rotating records; the implementation conservatively refuses that ambiguity. [L1_RECOVERY_V2_PROPOSAL.md](docs/L1_RECOVERY_V2_PROPOSAL.md) proposes a prospective three-slot version 2 for review; it is not active or implemented. OS-level network-isolated build/acceptance remain NOT_RUN: firewall administration was unavailable and no adapter was disabled. Python network-import/socket denial passed but does not substitute for that missing observation.

**One next gate (updated):** invoke the prepared owner-authorised focused L1 completion prompt; recovery direction and elevation permission are recorded above. Actual v2 implementation, review and OS-level acceptance remain required. No scientific interval, accepted external base, frontier claim or V1/E1 execution exists. Old future/unimplemented L1 wording is historical, never acceptance.

## Live baseline and completed historical gates
P0 entry main: `63fc41610603782eefc709139e6dcbdcca97b78f`. Repo tree, recent commits, open/recent PRs and Actions were inspected. One historical merged PR (#1) was found, with no open PRs and no recorded workflow runs at entry. No CI success is asserted.

Original BOOTSTRAP, R1–R4, I1 are PASS. C1 was recorded as agent-assessed PASS on 2026-10-05; its Windows/MSVC C17/GMP engine, calibration, build/profile, checkpoint store, reference oracle and Python scripts remain preserved but await operator review. Old V1/E1: NEVER ENTERED. C1 calibration did not validate an interval-verification engine. New P0: PASS for reorientation/documentation only. **P1 PASS — 2026-10-11** for elementary exclusion mathematics and research fixture checks only; see docs/P1_EXCLUSION_PROOFS.md. **P2: PASS FOR SPECIFICATION ONLY — 2026-10-11; L1 NOT EXECUTED.** No production verifier or scientific batch has been run.

## Frontier evidence hierarchy as of 2026-10-11
- **Peer-reviewed published**: every positive integer n < `2361183241434822606848` (2^71), Barina (2025), published claim, not CEML reproduction.
- **Live homepage rounded completed claim**: n < `2392312122059207475200` (2075 * 2^60).
- **Live work-unit progress, exact lowest incomplete**: unit ID `2175982616` of size `1099511627776` (2^40). Homepage says all lower units complete, yielding **reported** n < `2392518188130438742016`. This is a dynamic, NOT independently replicated, work-unit-ledger statement.
- The first reported incomplete interval at snapshot was `[2392518188130438742016,2392518189229950369792)`; dynamic overlap/assignment may change at any time. No world-first claim is permitted from this snapshot.
- P1 must distinguish published-supported starting modes from operational-report-dependent modes. See `docs/P0_FRONTIER_AUDIT.md`.

## New phase limits
P2 has frozen the separate CEML-FRONTIER-1 specification and dated research-only snapshot; see docs/FRONTIER_PROTOCOL_V1.md, docs/P2_PROTOCOL_AUDIT.md and the four new schemas. L1 is the ONE future local Codex implementation and test session requiring NEW owner instruction. P2 has neither run local Codex nor executed scientific trajectories. RUN1, old V1/E1 and any frontier-validity claim remain prohibited. The old `ceml.exe` was hard-gated to legacy phase strings; this P2 status intentionally authorises none of those modes. Do not manually bypass its guards.

P1 proof gate closed with five precisely proved rules in deterministic precedence; exact modulo-144 counts (72/36/12/4/5/15). P2 has frozen NEW schemas, independent full replay and coverage integrity, atomic checkpoint and acceptance semantics. These are UNIMPLEMENTED obligations for L1, not validated facts. Historical files/schemas remain authoritative solely for legacy data.

## P1 completion evidence and explicit proof limitations

Committed cloud-only P1 elementary math: conditional ascending-prefix theorem, E2/Q4/P3/M9/S2K4-03 integer-only predicates, universal k=4 residue proof, 144-class conservation, bounded identity tests (NOT science), primary-source audit and fixed Tao non-skip decision. The mathematical proof is given in [docs/P1_EXCLUSION_PROOFS.md](docs/P1_EXCLUSION_PROOFS.md) and has not been formally verified or independently peer reviewed. P1 PASS is **not** P2 protocol approval, L1 acceptance, RUN1 authorization, local V1, independent reproduction of Bařina's frontier or a novel verified interval. The old C1 native executable is deliberately phase-blocked; do not change its gate to run it.

## P2 freeze decision (2026-10-11)
P2 completed cloud specification only: new strict snapshot/run/checkpoint/certificate contracts, dual-pass exact coverage, separate peer-reviewed vs author-reported trust roots, strict chains, bounded failure/atomicity semantics, local pin reuse and a single future L1 prompt. See `docs/FRONTIER_PROTOCOL_V1.md`, `docs/P2_PROTOCOL_AUDIT.md`, `config/frontier_snapshot_v1.json`. The snapshot is **research-only and unaccepted** until a separately authorised RUN1 acceptance event. No Actions CI was configured at entry; neither P2 source review nor future L1 self-tests imply a scientific result.
