# RUN1 conditional pilot record — 2026-10-12

The owner explicitly requested agent execution of pilot 1 and supplied the acknowledgement and commands. On its success the owner requested commit, merge and push, authorised the next 1440 integers, specified pilot 3 as the following 14400, and requested a single command to launch the subsequent 100000 integers personally. The latter run has not started. These pilot widths are an owner-directed exception to the runbook's usual batch-2/doubling schedule; the frozen maximum of 14400 per batch and all identity, budget and verification requirements remain in force.

| Pilot | Half-open interval | Width | Status | Certificate digest |
|---|---|---:|---|---|
| 1 | `[2392518188130438742016,2392518188130438742160)` | 144 | COMMITTED; verification, replay and ledger passed | `99d6907248aa02a517d638469d60ab0f659af0a045b0444531e93fde1380f8a2` |
| 2 | `[2392518188130438742160,2392518188130438743600)` | 1440 | COMMITTED; verification, replay and ledger passed | `cebd2cf5d6e0ae327c3e54a6bc6dfef5e89358bf6a9aecbb2f5220b5431eb77e` |
| 3 | `[2392518188130438743600,2392518188130438758000)` | 14400 | Owner-specified next pilot; not run yet | — |

```text
CEML-FRONTIER-2 conditional batch chain
Run identifier: RUN1-operational-0001
Base kind and tier: operational (author-reported, not replicated)
Assumed, not verified by CEML: every positive integer below B = 2392518188130438742016 converges
  Source and its date: author's project homepage https://pcbarina.fit.vut.cz/, generated 2026-10-11T11:29:26Z
  CEML observation time (UTC): 2026-10-11T12:38:06Z
Verified conditional on that assumption: every integer in [2392518188130438742016,2392518188130438743600) converges
Batches: 2 (1584 integers)
Genesis digest: a416bf0f89ebdb16911baf830b6c375d280829bd58587dd7787e36f5d3c53caf
Latest certificate digest: cebd2cf5d6e0ae327c3e54a6bc6dfef5e89358bf6a9aecbb2f5220b5431eb77e
Snapshot digest: 538d319bad77b58ec3b37d653df3213312e260167ad26861e8870e48b276b729
Native build digest: c0263b353e05b9f3d09730e67d321254952c7dbdc2a6d892f7ffe2b14b89c032
Source commit of pilot 1: 641e7b64acd01397f360a14eb1659107e7732459
Rule counts (E2, Q4, P3, M9, S2K4-03, EXPLICIT): 792, 396, 132, 44, 55, 165
Unresolved: 0
Explicit shortened-map steps computed: 2193 (1344 odd; 3537 standard-map steps)
Run dates (UTC): 2026-10-12; pilot 1 certificate filesystem timestamp 08:53:51Z
Independent full replay performed: yes, built-in second pass (same author and machine)
Independent reproduction by other code: none
Overlap with externally reported work: expected; not checked against the external project's current state
This is a finite, conditional computational result. It is not a proof of the Collatz conjecture, not a
reproduction of the base, and not a claim of a world-first or of global frontier extension.
```

Pilot 1's native scan and per-frame check took 0.091117 seconds; its whole pilot command took about 2.73 seconds. Checkpoint inspection found generation 1 recoverable, no pending start, no warnings and no temporary files. OS firewall isolation was not applied to this scientific pilot; the runner uses no network. `COMMITTED` denotes an immutable verified local certificate, distinct from a Git commit.

Pilot 2's native scan and per-frame check took 0.145763 seconds; its whole pilot command took about 3.17 seconds. It recomputed 150 explicit starts in 1793 shortened-map steps, with 1095 odd steps (2888 standard-map steps), and resolved all 1440 starts. Its source checkout was local commit `b556cab` with the original accepted build identity. All three verification commands passed; checkpoint inspection again found no pending work or warnings. The published latest digest above is the external continuation anchor for pilot 3.

The record above is an aggregate summary and digest record. Raw batch records, checkpoints and per-integer data remain ignored local files. Publishing this document provides an external digest record; it does not back up the actual chain or retained dependencies. No separate physical storage device was available when checked, so a backup to a different physical device remains outstanding. The owner delegated the backup location choice but supplied no additional device.
