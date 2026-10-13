# Continuous checking with a clean stop

Start from the latest verified, committed exclusive endpoint without choosing a quantity:

```powershell
python C:\CEML\tools\operator\run_frontier.py start
```

The launcher audits the accepted chain and retained published/local anchors, then checks sequential batches of exactly 9999 integers. It reuses the same accepted operational assumption only after the base, build, snapshot and chain verify. It runs in the foreground so the terminal shows every verified batch. No scientific run was started by this procedure edit.

The prospective [CEML-SESSION-I1 profile](SESSION_I1_PROTOCOL.md) avoids repeatedly
replaying historical batches during a session. Review its
[validation record](SESSION_I1_VALIDATION.md), then, if accepting it, run:

```powershell
python C:\CEML\tools\operator\run_frontier.py accept-incremental
```

Type `ACCEPT-SESSION-I1` when prompted. This records acceptance only, with no
scientific execution. The same `start`/`stop` commands then use I1. Each startup
still fully verifies the ledger; subsequent batches use protected, authenticated
predecessors and independent verification of the new batch. Publication still
fully audits the chain with frozen V2. Until acceptance, the original V2 path
continues to run. A stale acceptance refuses; it never silently falls back.

## Stop after the current batch

In a second PowerShell window, paste:

```powershell
python C:\CEML\tools\operator\run_frontier.py stop
```

`STOP_REQUESTED` acknowledges a request, not completed shutdown. The active batch finishes its preparation, native check, certificate commit, verification, reference replay, ledger validation and checkpoint inspection. V2 audits the complete ledger here; accepted I1 validates the protected ledger and independently verifies the new batch. Its continuation receipt is saved before exit. If the request arrives before the next batch is admitted, no new authority, manifest or batch directory is created. The request is tied to the current session and cannot stop a future session. Repeated requests are harmless; no active run returns `NO_ACTIVE_RUN`.

Wait for `CLEAN_STOPPED` and the PowerShell prompt in the run window. The operator lock is released before that final status is printed. You can then publish immediately:

```powershell
python C:\CEML\tools\publication\publish.py
```

Publication still performs the required independent checks, so upload/merge can take several minutes. A normal clean stop leaves no unfinished successor to quarantine. A verification failure remains a failure and preserves its evidence; requesting a stop never promotes incomplete or mismatched work.

The launcher also treats Ctrl+C as a clean-stop request in this controlled mode. Verifier subprocesses use a separate process group so the signal does not abort the current verification command. The explicit `stop` command is preferable when using a remote terminal. Closing or forcibly killing processes is outside this clean-stop procedure.

## Accepted limits

The owner chose to keep the accepted frozen verifier. This is continuous operation within its existing 256-batch limit, not unlimited verification. At batch 256 it finishes all checks, saves the receipt, releases the lock and reports `CHAIN_LIMIT_REACHED`; publication is ready in the same way. Starting an already full chain reports that state without executing a batch. The build cannot start a second chain at the last endpoint or silently enlarge this limit.

At the published 208-batch prefix, 48 slots remain: 479952 additional integers in 9999-wide batches. This capacity is illustrative and declines as batches commit. I1 preserves this cap. A separately versioned contract and acceptance would be needed beyond the existing limit. Frozen v1/v2 records, contracts, identities and historical batch widths remain unchanged.

## Rehearsal and older finite commands

`python C:\CEML\tools\operator\run_frontier.py start --plan` is a read-only rehearsal; it runs no science and shows the remaining bounded plan. Legacy quantity-only, `--count X` and `check-next X` commands remain supported, now defaulting to 9999-wide batches; their last batch may be smaller to meet the exact quantity. An explicit finite `--batch-width` remains capped at 14400. Continuous `start` always requires 9999.

The latest checkpoint means a verified immutable certificate, never a provisional cursor. Pending starts, incomplete directories, abandoned active manifests, mismatched records and failed checks stop continuation without automatic resume, retry, skip or overwrite. The previously interrupted empty attempt of batch 123 was preserved in local quarantine by explicit owner instruction; it is not part of the committed chain.

Control requests and diagnostic state live atomically under ignored `local/frontier/`, outside batch directories. They are bookkeeping, not mathematical certificates. The runner remains offline and performs no Git/network operation. The separate live publisher observes continuous sessions without inventing a requested total. The owner removed the separate-device backup requirement; no backup task is outstanding. See `WEBSITE_PUBLICATION.md` for optional live status and end-of-run publishing.
