# Website and GitHub publication

The public research website (`jfairfaxball-348/john-fairfaxball-research`, `/collatz`) reads `frontier_progress_for_website.json` from CEML `main` on every request. That JSON is derived from the authoritative aggregate `docs/RUN1_PROGRESS.md`. Publishing it updates the website tally without a website rebuild.

## End-of-run command

After the quantity command returns, paste this into PowerShell from any directory:

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

The owner authorised the separate observer on 2026-10-12. Start it once per Windows session:

```powershell
python C:/CEML/tools/publication/live.py start
```

It runs hidden in the background, reads the launcher process and local immutable certificates/checkpoints, and uploads an allowlist matching the website's strict status schema about once a minute. No process command line, PID, host/device name, address, path, credential or per-integer data is published. Private logs and control files are under ignored `local/frontier/live-publisher/`. Read-only process observation is used only to infer the requested quantity and session start.

```powershell
python C:/CEML/tools/publication/live.py stop
```

Stopping it publishes paused status and ends only uploads. Network errors retry on the next minute; the scientific runner is unaffected. `preview` prints allowlisted status locally without uploading; `once` performs one upload. No Windows service or logon task is installed; after reboot run `start` again.

The public source is `https://raw.githubusercontent.com/jfairfaxball-348/CEML/live-status/frontier_live_status.json`, on a dedicated branch containing only informational status. Heartbeats create small ordinary commits on that branch and never merge into main or trigger website deployments. The website reads it by default, adds a freshness query and polls every 15 seconds. Its existing five-minute stale limit shows Working offline when the observer is unavailable. `FRONTIER_LIVE_STATUS_URL` can override the source; an explicitly empty setting disables live status. No Vercel secret, tunnel or inbound PC port is required.

Live checkpoint cursors are provisional. Recent `committed` entries are local file observations with canonical digest/identity checks; the observer performs no full ledger/replay verification and makes no independent verification claim. The authoritative tally changes only after separate verified publication. All claims remain conditional on the accepted author-reported base, with no conjecture proof, base reproduction or world-frontier claim.

## Engineering boundary and checks

All publication tools are outside the frozen verifier identity. The runner imports none of them, remains network-free and never commits automatically. They do not write any batch directory, change frozen contracts/worker/checker/snapshot bytes, alter continuation acknowledgement rules or execute a scientific quantity.

For manual aggregate edits, regenerate the website JSON with `python tools/publication/website_progress.py`. Check with `python tools/publication/website_progress.py --check` and `python -m unittest discover -s tests/publication -v`. The generator refuses discontinuity, width/total/digest disagreement and unresolved starts. Tests exercise privacy, provisional cursors, torn/corrupt records, rollback, preserved history and failed GitHub checks without executing science or using the network.
