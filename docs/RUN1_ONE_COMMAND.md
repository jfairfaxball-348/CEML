# Check the next quantity of integers

Paste this into PowerShell, replacing only the final number with the quantity you want:

```powershell
python C:\CEML\tools\operator\run_frontier.py 100000
```

The absolute path works from any current directory. The command audits the chain and finds its latest verified, committed endpoint E, then checks exactly [E,E+X) for your requested quantity X. No end, batch number, digest or acknowledgement needs to be pasted. It reuses the accepted operational assumption only for this same verified base, snapshot, build and chain.

The latest checkpoint means a completed immutable certificate. A checkpoint inside an incomplete batch does not advance the frontier. An uncommitted directory, pending start, abandoned manifest, identity mismatch or failed verification stops continuation without automatic retry, resume, skip or overwrite. Each batch is at most 14400 integers, and the existing chain may have at most 256 batches. A request must fit its remaining capacity; there is no separate 100000-per-invocation cap.

The launcher checks the locally frozen published aggregate anchor and, when present, local/frontier/operator_tip.json against the verified chain. It saves that local receipt atomically after each fully verified batch. The receipt is bookkeeping outside batch directories, not a mathematical certificate. Certificate verification, reference replay, chain audit and inspection still precede every extension. The verified digest is also retained and compared in memory between batches.

The owner has removed the separate-device backup requirement. It is optional and is not a prerequisite or outstanding task. The final printed digest and published aggregate progress record remain useful external references. Local receipts alone cannot detect replacement or rollback of all local files together. The offline command performs no network or Git operation.

For a read-only rehearsal, append --plan. Legacy --count X, an explicit --acknowledge, an optional exact --expected-latest digest pin, and the spelling check-next X still work. Without an explicit pin, the latest committed endpoint is discovered dynamically on every invocation. Do not infer completion from a partial checkpoint or receipt after an interruption.

This update changes the operator procedure and convenience launcher outside the frozen verifier identity. It changes no frozen v1/v2 contract, snapshot, worker, checker or batch record. The original 100000-integer run remains recorded in RUN1_PROGRESS.md. The example command above is for owner use; no new scientific quantity was executed while preparing this update.
