# L1 recovery refusal and proposed CEML-FRONTIER-2 amendment

Date: 2026-10-11. **DRAFT FOR OWNER REVIEW; NOT AN ACTIVE CONTRACT.**

**Owner decision recorded later on 2026-10-11:** the owner authorised the agent's choice; the minimal three-slot CEML-FRONTIER-2 amendment is selected for the focused continuation. No further owner decision is missing. This document remains a design proposal until new v2 protocol/schemas are frozen, implemented, reviewed and accepted; v1 is unchanged. See L1_CONTINUATION_READY.md. Original proposal text below is retained as history and does not negate this later permission. RUN1 remains denied.
The frozen CEML-FRONTIER-1 protocol, four v1 schemas, snapshot and P2 audit remain unchanged. L1 is OPEN. This document authorises neither a new implementation session nor RUN1.

## Reproducible ambiguity in the two-slot obligation

FRONTIER_PROTOCOL_V1 section 4 requires both strict previous-generation hashes/orphan refusal and recovery from a broken latest slot to its independently verified prior generation. With two rotating slots, after generation 2 the slots hold generations 2 and 1; generation 0 has been replaced. If generation 2 is torn, the surviving generation 1 names generation 0's digest, whose record is unavailable. The same observable surviving generation 1 plus a torn other slot can result from corrupting generation 0 immediately after generation 1. Two slot bytes alone cannot distinguish these histories or authenticate the missing parent link.

Fresh prefix replay validates the arithmetic, but cannot recreate the missing historical checkpoint generation/digest relation. An untrusted latest pointer does not supply independent historical evidence. No new mathematical exclusion or divergence issue is involved.

The implementation therefore accepts generation 0 alone, or a valid adjacent parent/child pair. It refuses a sole later generation, even when the other slot is torn. A torn generation 1 with intact generation 0 recovers with an integrity warning. Both cases are tested. This deliberately preserves orphan refusal; **general later-generation fallback is not accepted as complete v1 compliance**. No partial checkpoint is a committed interval.

## Explicit prospective version change proposed for review

Proposed protocol identifier: **CEML-FRONTIER-2**. Proposed change: three rotating self-contained slots `ckpt.0.json`, `ckpt.1.json`, `ckpt.2.json`, each retaining the existing record bound. On an ordinary write, retain the last two verified generations and replace only the older third slot. Generation 0 still has a null previous digest; later generations still bind the immediate previous digest. Slot index is generation modulo 3.

Recovery would independently validate each present record and its prefix, then require the highest accepted generation to have its immediately preceding valid generation and matching hash. A damaged newest record can consequently leave a valid adjacent pair. Generation 0 remains the only sole-record root case. Contradictory self-hashed identities, forks, invalid links and missing required evidence remain refusals. Native and Python re-execution of the completed prefix still precede advancement. Physical power-loss protection and malicious rollback detection remain conditional on independently retained roots; three files do not create authentication or a power-loss guarantee.

A future authorised amendment must create all four **new** v2 schemas with new schema constants, freeze the complete v2 byte/storage contract and use `CEML-FRONTIER-2/` digest domains. It must preserve v1 files and historical artifacts, create fresh v2 run IDs/roots, and refuse cross-version chain splicing. The five P1 rules, their proofs, independent every-n replay, snapshot trust tiers, single worker, budgets, immutable final certificate and separately owner-authorised RUN1 obligations carry forward unchanged unless an explicit reviewed amendment says otherwise.

Before accepting that amendment, test torn newest and missing/corrupt predecessor cases at generations 0 through at least 4, hash-linked adjacent pairs, duplicate/fork generations, write/flush/rename termination, native plus independent Python replay, and exact cold/resume equality. A subsequent focused L1 continuation must implement and test the newly frozen version. The current worker/driver still emits only v1 records and does not implement this draft.

## Required owner decision

Review the stricter current v1 refusal and this prospective amendment before authorising a focused continuation. Do not label L1 PASS or prepare a RUN1 handoff while the required recovery contract and network-isolated acceptance evidence remain unresolved.
