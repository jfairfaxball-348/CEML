# Start the next 100000 integers with one command

**Completed by the owner on 2026-10-12.** The command below successfully added the specified 100000 integers. The saved ten-batch chain, final certificate and reference replay passed read-only confirmation; see [RUN1 progress](RUN1_PROGRESS.md) for the current endpoint and digest. The original command's default pilot-3 anchor is now stale and deliberately refuses a repeat. This page retains the executed instruction as history; it does not authorise another run.

At preparation, pilot 3 had committed and passed certificate verification, full reference replay and chain audit. The selected interval was `[2392518188130438758000,2392518188130438858000)`: exactly 100000 additional integers. The owner subsequently started and completed this run; the agent did not execute it.

Open PowerShell and paste this one command. The absolute script path works from any current directory, with the accepted Python 3.12.10 available as `python`:

```powershell
python C:\CEML\tools\operator\run_frontier.py --count 100000 --acknowledge 538d319bad77b58ec3b37d653df3213312e260167ad26861e8870e48b276b729:operational:2392518188130438742016
```

The acknowledgement repeats the operational assumption you already accepted: every positive integer below `2392518188130438742016` converges, based on the author's unreplicated report in the frozen 11 October snapshot. Pasting and submitting the command is your instruction to execute this complete finite continuation. The operator launcher records that CLI invocation as authority for each exact constituent interval.

The launcher checks the clean checkout, source ancestry, accepted build, rules, snapshot and whole chain. By default it compares the latest certificate with the pilot-3 digest recorded externally in [RUN1_PROGRESS.md](RUN1_PROGRESS.md): `ab213f7ba9016bc54afe67873747e605dd88813480a695e8fb54b9b0821f46e6`. It then runs batches 4–10: six of 14400 integers and one of 13600. Each uses one worker and the unchanged finite per-start/per-batch budgets. Each certificate must pass verification, replay, ledger audit and checkpoint inspection before the next batch is prepared.

Within this single invocation, the verified latest digest is retained in memory and compared before every successor. This owner-requested aggregate operation replaces the manual one-command-at-a-time procedure for these seven batches; it does not establish an external durable record automatically. The terminal prints each batch's count, exclusive end, genesis and latest certificate digest. Save the final values outside this machine after the command, and back up the chain and retained build/dependencies to another physical device under the original runbook's section 8. At preparation time only C: was available, so that physical backup remains outstanding.

The scientific runner and this launcher perform no network access, Git operation, upload or automatic commit. They never edit an existing batch record. Refusal, INCOMPLETE, mismatch, warning or interruption stops the launcher. Completed predecessors stay committed; it never retries, resumes, skips or quarantines a failed attempt automatically. Ctrl+C stops the command. An interrupted run must be inspected and compared with its external record before further instruction; do not simply re-paste the original command. Its pilot-3 anchor deliberately refuses after the chain has advanced. An abandoned manifest without a batch directory is also preserved and stops automatic continuation.

For a read-only rehearsal, append `--plan` to the command. It performs the preflight and prints the exact seven-batch plan without authority, manifest, checkpoint or certificate writes. `--expected-latest` may be supplied for a separately authorised later invocation after comparison with an external digest record; the script permits at most 100000 requested integers, at most 14400 per constituent batch, and at most 256 total batches in this chain. There is no chain reset or base-change option.

The launcher is an operator convenience layer in `tools/operator`, with its orchestration tests in `tests/operator`. It calls the existing CLI unchanged and is outside the frozen verifier's identity inputs. The accepted build digest remains `c0263b353e05b9f3d09730e67d321254952c7dbdc2a6d892f7ffe2b14b89c032`. It is not a new verifier, a new L1 acceptance, or independent reproduction. The result remains finite and conditional on the author-reported base.
