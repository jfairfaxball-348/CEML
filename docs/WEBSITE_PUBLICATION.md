# Public website publication

The public research website (`jfairfaxball-348/john-fairfaxball-research`, Collatz page) shows this programme's progress. It reads one file from this repository's `main` branch at request time:

- `frontier_progress_for_website.json` (repository root, schema version 1)

That file is **derived**, never edited by hand. `docs/RUN1_PROGRESS.md` remains the authoritative aggregate record; the JSON re-expresses only its already published batch tables and claim block.

## Publishing a new verified aggregate

After a verified aggregate update to `docs/RUN1_PROGRESS.md` (the existing agent publication step), run from the repository root:

```text
python tools/publication/website_progress.py
python tools/publication/website_progress.py --check
python -m unittest discover -s tests/publication -v
```

Commit the regenerated JSON in the same commit as the `RUN1_PROGRESS.md` change. The website then shows the new tally on its next request; no website rebuild is needed.

The generator refuses (exit 2) if the batch tables are not consecutive and contiguous from the base, if widths or totals disagree, if the latest digest does not match the final batch, or if any start is unresolved. `--check` fails (exit 1) if the committed JSON is stale.

## Boundaries

- The generator reads only `docs/RUN1_PROGRESS.md`. It reads no batch directory, checkpoint, receipt or other local file, uses no network and executes nothing scientific.
- It is outside the frozen verifier identity. It changes no CEML-FRONTIER-1/2 contract, snapshot, worker, checker, launcher behaviour or batch record. The launcher still anchors on `docs/RUN1_PROGRESS.md`, not on this JSON.
- The website states the result with the same limits as the claim block: conditional on the author-reported operational base, not a proof of the conjecture, not a reproduction of the base and not a world-first or global frontier claim.

## Live view (not active)

The website page also has scaffolding for a live view of the local machine. It is currently **offline by design** and shows "working offline". No publisher exists in this repository, and the offline runner remains network-free (AGENTS.md item 8).

Any future live publisher would need a separate owner decision and must be a separate, optional, read-only sidecar process: it may only read local state, must never be imported by or become a dependency of the runner or verifier, must not affect whether a batch commits, and must publish no machine names, paths, addresses or other private identifiers. Live status is informational only; only verified, published aggregates count towards the public tally. The website-side status format is documented in the website repository at `docs/frontier-live-status.md`.
