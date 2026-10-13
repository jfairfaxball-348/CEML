# Website and GitHub publication

The public research website (`jfairfaxball-348/john-fairfaxball-research`, `/collatz`) reads `frontier_progress_for_website.json` from CEML `main` on every request. That JSON is derived from the authoritative aggregate `docs/RUN1_PROGRESS.md`. Publishing it updates the website tally without a website rebuild.

## End-of-run command

After the continuous launcher reports `CLEAN_STOPPED` (or `CHAIN_LIMIT_REACHED`) and returns to the terminal prompt, paste this into PowerShell from any directory:

```powershell
python C:/CEML/tools/publication/publish.py
```

It checks the clean, synchronized `main` checkout and accepted source ancestry, holds the same operator lock as the launcher, and independently verifies the accepted build, rules, snapshot, full ledger, final certificate, reference replay and checkpoint inspection. The retained receipt must match exactly. Unexpected or incomplete batch directories/manifests stop publication. Only this verification authorises updating the aggregate; a checkpoint cursor or receipt alone does not.

It appends aggregate rows for newly verified batches, preserves historical records, updates the current claim and programme/start pages, and derives and validates the website JSON. It publishes exactly those four allowed aggregate files through a GitHub branch, PR and merge, checking actual GitHub statuses and checks before merging. No force push or review bypass is used. It then fast-forwards local main. Raw records, per-integer events and identifying machine fields are never uploaded. Repeating it with an already published chain reports `ALREADY_PUBLISHED` without another commit. `--preview` performs verification and derives the proposal without network or tracked-file changes.

If GitHub checks or required reviews prevent merging, the PR remains available, with its URL retained privately in `local/frontier/publication-pr.json`. Finish that PR through the normal review flow before running another publication command. A remote/local divergence or interrupted synchronization stops safely rather than overwriting history. Verification can take several minutes on a long chain. Publication is refused while the launcher is active; it never stops or resumes science.

## GitHub sign-in

GitHub CLI is installed on this PC. Sign in once as `jfairfaxball-348`:

```powershell
gh auth login --hostname github.com --git-protocol https --web
```

Complete browser authorization and let the terminal finish. Credentials remain in the CLI credential store. Never paste a token into a command or repository file. Both publishing tools use `gh api`; neither needs a token in source or environment files.

## Optional live progress

The owner authorised the separate observer on 2026-10-12. Start or re-enable it with:

```powershell
python C:/CEML/tools/publication/live.py start
```

It registers the dedicated Windows task `CEML Live Publisher` for the signed-in user, with limited privileges and no stored password. It runs hidden through `pythonw`, starts at logon, restarts on failure and has a one-minute recovery trigger with duplicate instances ignored. This avoids tying the observer to a terminal or Codex tool lifetime. It reads operator control state and local immutable certificates/checkpoints, and uploads an allowlist matching the website's strict status schema about once a minute. No process command line, PID, host/device name, address, path, credential or per-integer data is published. Private logs and control files are under ignored `local/frontier/live-publisher/`.

**Privilege-independent detection — 2026-10-13:** Windows hides an elevated
launcher's command line from the limited publisher. The observer reads bounded
control state, probes the operator byte lock without waiting or writing, and uses
Windows Restart Manager **list-only** queries for the resource user's PID and
exact creation time. It re-lists that identity, checks the lock again, and rereads
the control token. It never opens a privileged process handle or invokes shutdown,
restart or signalling APIs. A unique resource user born within 30 seconds before
the recorded session start confirms activity. Older/ambiguous users and query
failures report uncertainty (`error`) with retained progress, not idle/stopped.
Stale active flags with a free lock, exited/reused PIDs and publisher processes
born after the recorded session cannot establish a running verifier. Atomic
control transitions are retried once. Missing control with a held lock is unknown;
command-line lookup is a legacy fallback only with no control and no held lock.
Session counts use the recorded initial exclusive endpoint when available,
instead of certificate mtimes. Control state remains bookkeeping, never
mathematical authority. See
[RmGetList](https://learn.microsoft.com/en-us/windows/win32/api/restartmanager/nf-restartmanager-rmgetlist).

```powershell
python C:/CEML/tools/publication/live.py stop
```

Stopping it disables the recovery/logon task and asks the current observer to publish paused status and end uploads. Network errors retry on the next minute; the scientific runner is unaffected. `start` re-enables the task. `preview` prints allowlisted status locally without uploading; `once` performs one upload. No Windows service is installed; the task runs only while this user is signed in.

The public source is `https://raw.githubusercontent.com/jfairfaxball-348/CEML/live-status/frontier_live_status.json`, on a dedicated branch containing only informational status. Heartbeats create small ordinary commits on that branch and never merge into main or trigger website deployments. The website reads it by default, adds freshness queries to upstream and browser requests, and polls every 15 seconds. It refreshes immediately on mount, visibility/focus and network recovery, permits only one request at a time, and aborts browser fetches after ten seconds. Hidden tabs still expire retained freshness; cached/late responses cannot move Last checked backwards or revive a stale heartbeat. The dynamic API/page, upstream no-store fetches and browser/CDN no-store headers bypass feed caching. Latest batch checked and This session remain visible through delays; a five-minute-old heartbeat is labelled Updates delayed, without inferring PC connectivity. Fetch failures cannot extend freshness. Future heartbeats beyond 30 seconds of clock tolerance are refused. `FRONTIER_LIVE_STATUS_URL` can override the source; an explicitly empty setting disables live status. No Vercel secret, tunnel or inbound PC port is required.

Reload only the optional publisher after observer code changes. If its recovery
task is enabled, writing its existing ignored stop marker ends the old observer
and the next recovery trigger starts a fresh one; this can briefly publish paused
status. Never stop or signal science to reload monitoring. Respect a deliberately
disabled publisher; `start` is the owner's command to re-enable it. The scheduled
task stays at limited privilege.

Live checkpoint cursors are provisional. Recent `committed` entries are local file observations with canonical digest/identity checks; the observer performs no full ledger/replay verification and makes no independent verification claim. The authoritative tally changes only after separate verified publication. All claims remain conditional on the accepted author-reported base, with no conjecture proof, base reproduction or world-frontier claim.

## Engineering boundary and checks

All publication tools are outside the frozen verifier identity. The runner imports none of them, remains network-free and never commits automatically. They do not write any batch directory, change frozen contracts/worker/checker/snapshot bytes, alter continuation acknowledgement rules or execute a scientific quantity.

For manual aggregate edits, regenerate the website JSON with `python tools/publication/website_progress.py`. Check with `python tools/publication/website_progress.py --check` and `python -m unittest discover -s tests/publication -v`. The generator refuses discontinuity, width/total/digest disagreement and unresolved starts. Tests exercise privacy, provisional cursors, torn/corrupt records, rollback, preserved history and failed GitHub checks without executing science or using the network.
