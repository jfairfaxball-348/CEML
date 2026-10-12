# RUN1 is a separate, owner-authorised stage — this prompt does not authorise it

Work in `C:\CEML`. L1 is recorded as PASS, agent-assessed, in `PROGRAM_STATUS.md` and `docs/L1_V2_ACCEPTANCE.md`. The owner's acceptance of that record is outstanding. RUN1, the first offline scientific pilot, is **not authorised**. Invoking this prompt authorises nothing. It tells a session what RUN1 needs and what the session may and may not do.

Read `PROGRAM_STATUS.md`, `AGENTS.md`, `START_HERE.md`, `docs/L1_V2_ACCEPTANCE.md`, `docs/FRONTIER_PROTOCOL_V2.md` and `docs/RUN1_OPERATOR_RUNBOOK.md` before anything else. Current status controls every older phase string.

## Before any RUN1 step

1. Pin live `main` and inspect local status, the PR that carries L1, its head, mergeability, actual checks and Actions. Verify CI rather than invent it. A merge proves no acceptance obligation.
2. Confirm the tree is clean and at, or a descendant of, the source commit named in `docs/L1_V2_ACCEPTANCE.md` section 7 with no identity-bound file changed. Run the runbook's session preflight (section 5) and require the pinned build digest, worker hash, table digest and snapshot digest. If any differs, stop: the accepted software is not what is in front of you.
3. Do not edit any identity-bound file. A change to the worker, driver, reference, build tool, frontier tests, schemas, snapshots or protocol documents gives a new build identity. That needs the L1 acceptance evidence again, including a fresh OS-blocked run, before any chain is started.

## What only the owner can do

- Accept or reject the L1 record. Until the owner has accepted it, L1 is an agent-assessed pass and nothing follows from it.
- Give a fresh, explicit instruction to start RUN1, naming the base kind (`published` or `operational`).
- Type the acknowledgement string of runbook section 4.2. No agent and no tool fills it in.
- Decide the run identifier, the authority identifier and where backups and the external digest record are kept.

Until the owner has accepted L1 and given the RUN1 instruction in the current conversation, do nothing beyond reading and the read-only preflight. Do not prepare a status transition "in advance".

## What a session may do once the owner has instructed RUN1

- Make the status transition of runbook section 4.3 as a reviewed commit that quotes the owner's instruction, changing only the two status lines and the supporting text. Run the complete L1 suites one last time before that commit; they are L1-phase checks and are expected to refuse afterwards.
- Follow `docs/RUN1_OPERATOR_RUNBOOK.md` exactly, one batch at a time, starting with the 144-start pilot at the chosen base, with the maximum finite budgets. Verify, replay and audit each batch (section 7) and have the owner update the external record (section 8) before the next.
- Report every result with the claim template of runbook section 13. A batch is a finite conditional result. It is never a proof, a reproduction of the base, or a world-first.

## What a session must never do

- Start, resume or extend any batch without the owner's instruction covering it, or type an acknowledgement or owner instruction on the owner's behalf.
- Edit, delete, move or copy any record in a batch directory. Quarantine of an uncommitted attempt is the operator's act, described in runbook section 10.
- Change base inside a chain, reuse a run identifier, run two batches at once, or describe an INCOMPLETE or checkpoint-only batch as verified.
- Treat a pending start as divergence, or retry, skip or reorder it. Preserve it and report it.
- Fetch, upload, refresh the snapshot, add a dependency, add an exclusion, use a GPU or parallel workers, or start an optimisation programme.
- Run the elevated launcher. It is acceptance infrastructure, not part of RUN1.

## Known first-execution risk

L1 was not allowed to run a scientific batch. The first RUN1 pilot is the first end-to-end execution of the authorised path, and the first time the worker's gate accepts a status. If it refuses for a reason the runbook's section 10 does not explain, stop. A refusal promotes nothing. A fix needs review and a new L1 acceptance, which is harmless only while no chain exists.

## Exit discipline

Keep raw logs, run records and per-integer data out of Git. The runner never fetches, uploads, changes source or commits. Finish every session with the exact interval covered, the base and its tier, the chain digests, what was and was not independently reproduced, and any owner action needed.
