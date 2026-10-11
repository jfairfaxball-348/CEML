# Owner-authorised L1 completion preparation — 2026-10-11

**L1 remains OPEN. This is preparation, not acceptance or RUN1.**

## Owner decision and scope

In the current CEML chat the owner stated: "i authorise whatever decision you decide is best" and authorised local preparation, Windows elevation if needed, and a fresh-session prompt to finish engineering before final local offline scientific runs. This supersedes the missing-owner-decision gate. The chosen amendment is the minimal three-slot design in `L1_RECOVERY_V2_PROPOSAL.md`, prospectively named **CEML-FRONTIER-2**. Approval permits specifying/implementing/reviewing the amendment; the new contract does not yet exist or have a freeze/acceptance PASS.

The focused continuation may create new v2 protocol/snapshot/schemas/digest domains, implement recovery, perform bounded engineering tests/calibration, fix findings, update the existing PR and prepare the complete RUN1 operator package. All v1 bytes, P0/P1/P2 and legacy evidence/pins/gates remain preserved. No additional exclusions, scientific frontier scan, new dependency, optimisation programme, old V1/E1, accepted external base or RUN1 is authorised. No routine engineering permission or repeat amendment decision is needed. Invoking `NEXT_SESSION_PROMPT.md` starts the continuation of the single L1 attempt.

## Standalone OS isolation prepared

`tools/l1/run_offline_acceptance.ps1` separates read-only `Preflight` and elevated `Run`. Run requires reviewed current source/launcher SHA256 identities, pinned Python, effective firewall profiles enabled/local rules allowed, running firewall/scheduler services, no authenticated bypass rules, and a successful connected zero-application-payload TCP baseline.

Before blocking traffic it registers a uniquely named SYSTEM cleanup task for 25 minutes later and next boot. Two temporary machine-wide Windows Firewall rules then block inbound/outbound traffic, all programs/protocols/interfaces/profiles and IPv4/IPv6. The launcher checks effective rules and a failing probe, runs acceptance in a separate child, monitors policy, and rechecks rules/probe/source before success. The child has a 20-minute limit and shorter command budgets. `finally` stops an unfinished child tree, removes only these two rules, verifies removal and unregisters its task. Failed cleanup retains the watchdog. An exclusive checkout-local lock prevents overlapping launchers.

**The machine, including the cloud chat, temporarily loses network access.** Launch detached so local checks continue, prepare all files first and read evidence after connectivity returns. No credentials, telemetry or hardware identity are needed. Existing firewall profiles/rules/adapter settings are not overwritten. References: [Microsoft firewall cmdlets](https://learn.microsoft.com/en-us/powershell/module/netsecurity/new-netfirewallrule?view=windowsserver2025-ps), [scheduled-task principals](https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtaskprincipal?view=windowsserver2025-ps).

The Python helper rebuilds release/checked workers, independently reproduces artifacts, runs rules/snapshot checks, launcher tests, the complete frontier suite with **zero skips/expected failures**, independent full-replay selftests/calibration, then final reproduction. It selects a v2 snapshot once present. The continuation must review/adapt its plan for the final v2 interface and include all recovery tests. This harness is not a frozen scientific contract.

Raw diagnostics and path-free summaries stay in ignored `local/frontier/os-offline/<random-id>/`. `checks.json` alone does not establish OS isolation: require matching `isolation.json` with `OS-BLOCKED-ENGINEERING-CHECKS-PASS`, current identities, verified restoration, logs/test totals, exact build identity and command observations. Neither file alone grants L1 PASS. Do not track raw logs, user paths, adapter identifiers or per-integer records.

## Launch in the next session

Finish implementation/review and prepare final sources first. Then:

```powershell
$ready = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\CEML\tools\l1\run_offline_acceptance.ps1 -Mode Preflight | ConvertFrom-Json
$argsForL1 = '-NoProfile -ExecutionPolicy Bypass -File "C:\CEML\tools\l1\run_offline_acceptance.ps1" -Mode Run -ExpectedSourceSha256 ' + $ready.source_sha256 + ' -ExpectedLauncherSha256 ' + $ready.launcher_sha256
$l1Process = Start-Process powershell.exe -Verb RunAs -WindowStyle Hidden -ArgumentList $argsForL1 -PassThru
```

The owner may need to accept Windows UAC on the secure desktop. If elevation fails, provide this exact reviewed command for an administrator terminal. Do not claim UI automation bypasses UAC. No coding permission needs repeating. A source edit requires fresh hashes/run. Wait/poll in bounded calls and inspect the unique local result after return; chat disconnection does not mean the local run failed. Early pre-run refusals may exit without an evidence directory and must be investigated rather than treated as success.

Emergency restoration from administrator PowerShell if timer/boot cleanup fails:

```powershell
Get-NetFirewallRule -PolicyStore PersistentStore | Where-Object { $_.Group -like 'CEML-L1Offline-*' -and $_.Name -like 'CEML-L1Offline-*' } | Remove-NetFirewallRule
```

Verify launcher rules are absent. Retain any `CEML-L1Offline-*-Restore` task until removal succeeds. OS rules are not a physical air gap or power-loss guarantee. Ineffective policy, failed baseline, timeout, skipped check or missing evidence leaves L1 OPEN.

## Preparation observations

Live main `abd5d5bd0c6bb3a5cfbd1b83d52122b04d324016`; draft PR #5 open/unmerged, entry head `c7b0249e4ae25de02568143d97aaacb07c6bc763`; zero Actions runs. Existing science/engineering claims unchanged.

Read-only Windows preflight PASS: all three effective profiles enabled/local rules allowed, required services running, no bypass found, pinned Python available, current process not administrator. Harness tests: **8 PASS, zero skips**. Initial test fixture module-cache collisions were corrected and rerun. Elevated rule creation, watchdog behavior and OS-blocked build/acceptance remain **NOT_RUN**. No network policy changed during preparation. Validate the elevated path in the continuation.

## Acceptance and handoff

Require final v2 contract/code review; complete test results; generation-0-through-at-least-4 faults; abrupt exit stages; full every-integer replay; cold/resume equality; immutable certificates; rooted/cross-version refusal; gates; actual OS-isolated evidence and bounded calibration. Capture failures honestly. Required independent acceptance is separate from the author rereading the code; record reviewer provenance, or explicitly leave that remaining gate OPEN.

Prepare an offline operator package/runbook with dependencies, source/build/snapshot digests, baseline/trust-tier choices, fresh RUN1 authority/acknowledgement template, 144-start initial pilot, finite budgets, verify/backup/resume/stop/replay/contiguous-extension commands, refusal diagnostics and truthful claims. Include independent-reproduction instructions distinct from the built-in second pass. Test with synthetic fixtures only. No scientific batch to test the handoff.

Commit evidence before advancing L1. Final output must state whether engineering is actually complete, any remaining operator action, and only separately owner-authorised RUN1 after accepted L1 PASS. No auto science, seed generation or runner Git mutation.
