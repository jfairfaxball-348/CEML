# RUN1 conditional chain record — 2026-10-12

The owner explicitly requested agent execution of pilot 1 and supplied the acknowledgement and commands. On its success the owner requested commit, merge and push, authorised the next 1440 integers, specified pilot 3 as the following 14400, and requested a single command to launch the subsequent 100000 integers personally. The owner has now executed that command and shown its `CONDITIONAL_RUN_COMPLETE` output; read-only verification of the saved records confirms all seven additional batches. These pilot widths are an owner-directed exception to the runbook's usual batch-2/doubling schedule; the frozen maximum of 14400 per batch and all identity, budget and verification requirements remain in force.

| Pilot | Half-open interval | Width | Status | Certificate digest |
|---|---|---:|---|---|
| 1 | `[2392518188130438742016,2392518188130438742160)` | 144 | COMMITTED; verification, replay and ledger passed | `99d6907248aa02a517d638469d60ab0f659af0a045b0444531e93fde1380f8a2` |
| 2 | `[2392518188130438742160,2392518188130438743600)` | 1440 | COMMITTED; verification, replay and ledger passed | `cebd2cf5d6e0ae327c3e54a6bc6dfef5e89358bf6a9aecbb2f5220b5431eb77e` |
| 3 | `[2392518188130438743600,2392518188130438758000)` | 14400 | COMMITTED; verification, replay and ledger passed | `ab213f7ba9016bc54afe67873747e605dd88813480a695e8fb54b9b0821f46e6` |

The owner's live continuation consists of these seven committed batches. The launcher reported verification, replay, chain audit and inspection before each extension; the agent subsequently re-audited the complete saved chain and separately verified, replayed and inspected the final batch.

| Batch | Half-open interval | Width | Certificate digest |
|---|---|---:|---|
| 4 | `[2392518188130438758000,2392518188130438772400)` | 14400 | `8a879d23f28934c9b93e4970ef4813a01b00e507ffeeba146bf9be8e5976b83f` |
| 5 | `[2392518188130438772400,2392518188130438786800)` | 14400 | `5e68013a6ac6291b1502442ef2912788ad150fecfe78e4413099c4cab96b0ed3` |
| 6 | `[2392518188130438786800,2392518188130438801200)` | 14400 | `e8fbc86a04897105a4227da3ed8ab560e7a745d9c2a1b44e70ca18cf4fe4ba16` |
| 7 | `[2392518188130438801200,2392518188130438815600)` | 14400 | `d1d7e3a0f27b318efd9f5b69296a143eb43d0f96c71cdb5bbdeab872b3743063` |
| 8 | `[2392518188130438815600,2392518188130438830000)` | 14400 | `e9d4ccb4837bb257a77430dc15361c3ed2205b7beb3a5d2a50701ceabc5d6e20` |
| 9 | `[2392518188130438830000,2392518188130438844400)` | 14400 | `f936d6262777af7933143e7576b8e776c4a936eadc6091f16479005c694868f7` |
| 10 | `[2392518188130438844400,2392518188130438858000)` | 13600 | `5f46665571ef5e85ed629576cd1e7f231ba1c8abe7a7d7975d408d94c14be17a` |

```text
CEML-FRONTIER-2 conditional batch chain
Run identifier: RUN1-operational-0001
Base kind and tier: operational (author-reported, not replicated)
Assumed, not verified by CEML: every positive integer below B = 2392518188130438742016 converges
  Source and its date: author's project homepage https://pcbarina.fit.vut.cz/, generated 2026-10-11T11:29:26Z
  CEML observation time (UTC): 2026-10-11T12:38:06Z
Verified conditional on that assumption: every integer in [2392518188130438742016,2392518188130438858000) converges
Batches: 10 (115984 integers)
Genesis digest: a416bf0f89ebdb16911baf830b6c375d280829bd58587dd7787e36f5d3c53caf
Latest certificate digest: 5f46665571ef5e85ed629576cd1e7f231ba1c8abe7a7d7975d408d94c14be17a
Snapshot digest: 538d319bad77b58ec3b37d653df3213312e260167ad26861e8870e48b276b729
Native build digest: c0263b353e05b9f3d09730e67d321254952c7dbdc2a6d892f7ffe2b14b89c032
Source commit of pilot 1: 641e7b64acd01397f360a14eb1659107e7732459
Source commit of owner's 100000-integer continuation: 789dca672cdd3bbe9ed7d30d93f465f2e2e47c7b
Rule counts (E2, Q4, P3, M9, S2K4-03, EXPLICIT): 57992, 28996, 9666, 3221, 4026, 12083
Unresolved: 0
Explicit shortened-map steps computed: 143886 (87966 odd; 231852 standard-map steps)
Run dates (UTC): 2026-10-12; certificate filesystem timestamps from 08:53:51Z (pilot 1) to 09:48:32Z (batch 10)
Independent full replay performed: yes, built-in second pass (same author and machine)
Independent reproduction by other code: none
Overlap with externally reported work: expected; not checked against the external project's current state
This is a finite, conditional computational result. It is not a proof of the Collatz conjecture, not a
reproduction of the base, and not a claim of a world-first or of global frontier extension.
```

Pilot 1's native scan and per-frame check took 0.091117 seconds; its whole pilot command took about 2.73 seconds. Checkpoint inspection found generation 1 recoverable, no pending start, no warnings and no temporary files. OS firewall isolation was not applied to this scientific pilot; the runner uses no network. `COMMITTED` denotes an immutable verified local certificate, distinct from a Git commit.

Pilot 2's native scan and per-frame check took 0.145763 seconds; its whole pilot command took about 3.17 seconds. It recomputed 150 explicit starts in 1793 shortened-map steps, with 1095 odd steps (2888 standard-map steps), and resolved all 1440 starts. Its source checkout was local commit `b556cab` with the original accepted build identity. All three verification commands passed; checkpoint inspection again found no pending work or warnings. Its digest was published before pilot 3 and used as that pilot's continuation anchor.

Pilot 3's native scan and per-frame check took 0.716840 seconds; its whole pilot command took about 4.49 seconds. It recomputed 1500 explicit starts in 17759 shortened-map steps, with 10854 odd steps (28613 standard-map steps), and resolved all 14400 starts. Its source checkout was local commit `2ea90ba1d99baf467f9aba65e73a9e2cb98b1842`, with the original accepted build identity. All three verification commands passed; checkpoint inspection found no pending work or warnings. Its digest was the externally published anchor for the owner's live run.

The owner executed the [one-command continuation](RUN1_ONE_COMMAND.md), adding exactly 100000 integers in seven sequential batches within the unchanged 14400 maximum. Those batches computed 123934 explicit shortened-map steps, including 75768 odd steps (199702 standard-map steps). Their certificate filesystem timestamps run from 09:46:42Z to 09:48:32Z; these timestamps are not an exact end-to-end timing measurement. The owner's screenshot showed the final `CONDITIONAL_RUN_COMPLETE` status, and its latest digest and endpoint match the saved ledger. The accepted build still verifies with the original identity. The agent executed no scientific batch in this confirmation session; only read-only verification and aggregate documentation were performed. No further continuation is authorised or started by this record.

The record above is an aggregate summary and digest record. Raw batch records, checkpoints and per-integer data remain ignored local files. Publishing this document provides an external digest record. The owner subsequently removed the separate-device backup requirement; no backup action is outstanding. The reusable PowerShell command is now `python C:\CEML\tools\operator\run_frontier.py X`, changing only X. The launcher audits and discovers the latest committed end, checks published/local anchors, reuses this chain's accepted assumption, and saves a local continuation receipt after verification. See `RUN1_ONE_COMMAND.md`. This procedure update executes no new batch and preserves the frozen verifier's identity and existing records.
