# RUN1 handoff

For owner-run continuous continuation:

```powershell
python C:\CEML\tools\operator\run_frontier.py start
```

No quantity is required. The launcher audits the same accepted chain, discovers its verified exclusive endpoint, and checks sequential batches of exactly 9999. The owner chose to preserve the frozen 256-batch limit; it stops cleanly there with `CHAIN_LIMIT_REACHED`.

In a second PowerShell window, request a clean stop with:

```powershell
python C:\CEML\tools\operator\run_frontier.py stop
```

Wait for `CLEAN_STOPPED` and the run terminal prompt, then invoke `python C:\CEML\tools\publication\publish.py`. The active batch must finish every check and save the receipt; stop requests do not terminate the worker or promote unresolved work. No successor is admitted after the request. The operator lock is released before the final ready status.

Use PROGRAM_STATUS.md, AGENTS.md, docs/RUN1_OPERATOR_RUNBOOK.md and docs/RUN1_ONE_COMMAND.md. Preserve every frozen contract and batch record. The owner starts scientific execution; this procedure-edit request executes no quantity. Agents check and record only unless separately authorised for a finite scientific run. Keep raw records out of Git, distinguish conditional results from independent reproduction, and never skip a partial checkpoint. Backups are optional and not an outstanding task. Legacy finite quantity commands remain supported but are no longer the default handoff.
