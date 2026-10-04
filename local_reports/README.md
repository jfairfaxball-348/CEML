# C1 Sanitized Reports

This directory is reserved for the small sanitized C1 artifacts that the approved I1 handoff requires in repository history:

- HARDWARE_REPORT.json and its reconciled HARDWARE_REPORT.md rendering;
- BENCHMARK_SUMMARY.json;
- ENGINEERING_DECISIONS.json;
- BENCHMARK_BUNDLES.json;
- BUILD_MANIFEST.json.

I1 contains no machine values, so these files do not exist yet.

Raw or large per-repeat benchmark evidence belongs under ignored `local/c1/` paths by default. A raw bundle used by a frozen decision must be retained locally and represented here by its engineering digest/index. No prohibited stable identifier may be committed, even in hashed form.

The C1 sensitive-data scan defined by docs/CODEX_HANDOFF.md must pass before any generated artifact in this directory is committed.
