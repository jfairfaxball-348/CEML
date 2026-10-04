# Local-only Artifact Area

Everything in `local/` except this README is ignored by Git.

Suggested future layout:

```
local/
  hardware_raw/
  benchmarks/
  checkpoints/
  logs/
  tmp/
  artifacts/
```

Raw machine reports may contain sensitive identifiers and must remain local until sanitized. Large checkpoints, giant integer states, temporary arithmetic files, and verbose logs stay here or in another explicitly configured local path.

Compact sanitized reports/hashes may later be copied into tracked locations under the frozen protocol.
