# Immediate manual engineering check

Stage: **hardware characterization**. C1 remains open.

The guard now uses pressure-rate intervals of at least one second for admission,
mid-case sampling and the final observation. Memory, storage and power checks
continue at every polling boundary. The thresholds, case/work/memory limits and
shared aggregate budget are unchanged. Short cases wait for a full final pressure
interval after child completion; candidate timing excludes this wait.

This is an explicit monitor-method correction based on the retained attempt:
two one-second admission samples had zero page input, while its approximately
38 ms child interval produced a rate near 1917 pages per second. That observation
does not establish actual swap pressure. The new method makes interval lengths
consistent; it does not assert that future conditions are safe. The original
invalid bundle and reports remain unchanged. Future runs carry new build/source
identities and distinct bundles, preserve the aggregate budget, and stop at the
first refusal. Do not loop/retry until a favorable result appears.

Open PowerShell in the repository, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools\c1\manual_check.ps1 -PressureOnly
powershell -NoProfile -ExecutionPolicy Bypass -File tools\c1\manual_check.ps1
```

The first command is optional and checks build/resource readiness. The second
performs one bounded engineering comparison: 1024/4096-bit public generated
inputs, 256 shortcut steps, direct/width-4 routes, three inputs per class and one
warm-up plus five measured repeats. Typical elapsed time is a few minutes because
each child has admission and final monitoring. The arithmetic ceiling remains
60 seconds aggregate, including previous charged work. No network fetch occurs.

If it stops, preserve the displayed refusal and the new local bundle. If it
completes, preserve the bundle; no further action automatically follows. Do not
run the older session-specific report assembler against new successful evidence.

A scientific live run is not a quick next command. The remaining work includes
the other C1 comparisons and required size classes, checkpoint durability and
recovery, the production engine, complete build/profile freeze, and then the
separate V1 suite. This command provides an immediate engineering test only.
