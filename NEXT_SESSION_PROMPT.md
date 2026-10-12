# RUN1 handoff

For owner-run continuation, provide this reusable PowerShell command and change only the final positive quantity:

```powershell
python C:\CEML\tools\operator\run_frontier.py X
```

Use the current PROGRAM_STATUS.md, AGENTS.md and docs/RUN1_OPERATOR_RUNBOOK.md. The launcher audits the existing chain, verifies retained anchors and discovers the latest committed exclusive endpoint; no fixed end or digest belongs in this handoff. A partial checkpoint never authorises skipping an unresolved start. The existing accepted operational assumption is reused only for the same verified chain and software identity. Preserve all frozen contracts and batch records.

The owner runs the command unless explicitly asking the agent to execute a finite quantity. Editing this handoff with no numeric request runs nothing. Report a result only after complete certificate verification, replay and chain audit; keep raw records out of Git. See docs/RUN1_ONE_COMMAND.md for the operator procedure and docs/RUN1_PROGRESS.md for the current aggregate record. The owner removed the separate-device backup requirement; no backup request or outstanding backup task is appropriate.
