# Session I1 validation — 2026-10-13

Status: engineering candidate, author-assessed; owner acceptance NOT RECORDED.
No scientific batches were executed by this engineering session. The saved
208-batch chain and its published aggregate remain unchanged. This is neither
a new L1 acceptance nor a change to the frozen V2 acceptance evidence.

## Cause and prospective correction

The arithmetic/reference implementation is not progressively getting harder
in the measurements. V2's `predecessor()` scans sibling certificates and calls
`verify_batch()` recursively. Each recursive verification performs a complete
reference replay and build/context verification. At depth N it also loads
approximately N squared sibling records. The operator invokes this path during
manifest preparation, admission, batch execution, both commit predecessor checks,
final certificate reread and post-batch verification. It additionally audits the
whole ledger before and after every batch. Thus historical arithmetic is replayed
repeatedly inside each new batch and total session work grows quadratically.

Read-only cProfile evidence for a single recursive `verify_batch`:

| Saved batch | Full batch replays | Record loads | Profiled seconds |
| --- | ---: | ---: | ---: |
| 3 | 3 | 425 | 5.45 |
| 64 | 64 | 13,296 | 52.22 |
| 208 | 208 | 43,680 | 155.94 |

Instrumentation changes elapsed time. Use the ordinary benchmark below for
performance comparisons; the profile identifies the repeated work.

I1 establishes trust by full startup replay and Windows read leases, then uses
V2's existing trusted-ledger predecessor interface for new-batch verification.
It adds a separately identified admission/commit orchestration path instead of
modifying or monkey-patching the frozen recursive verifier. New batches still
undergo native/frame checks, independent reference computation, atomic checkpoint
and certificate operations, a final new-certificate replay and checkpoint
inspection. Cached historical certificates are protected, immutable in memory
and reauthenticated by full replay on every restart. Publication still uses the
original independent full-chain audit. See [the contract](SESSION_I1_PROTOCOL.md).

## Measured performance

The reproducible comparison uses only already committed certificates, with the
operator lock held. Legacy timings are unprofiled; I1 reports the median of three
warm independent replays of each selected batch after a single startup audit.
Each result must have the exact original certificate digest. Metadata protection
and historical inventory checks are included. Widths differ at batch 208, so
compare each row with itself rather than attributing its shorter time to depth.

Results are recorded in [the aggregate benchmark](SESSION_I1_BENCHMARK.json).

| Saved batch | Width | Legacy seconds | I1 median seconds | Stage speedup |
| --- | ---: | ---: | ---: | ---: |
| 3 | 14,400 | 2.783 | 0.263 | 10.6x |
| 64 | 14,400 | 22.223 | 0.301 | 73.7x |
| 208 | 9,999 | 77.618 | 0.159 | 488.8x |

The final protected full startup audit took 52.464 seconds; cached ledger
validation at 208 batches took 0.0138 seconds median. A first measurement gave
76.624 to 0.148 seconds at batch 208 (516x), and a 35.394-second startup audit.
Elapsed time varies with concurrent machine activity; both measurements show
the removal of historical arithmetic. The final hardening rerun in JSON is the
authoritative recorded profile `823a2d62a074b16fd81b3156804e949d74b497f11d8705c3f13529376024ceb3`.

This is a verification-stage measurement, not a claimed end-to-end scientific
throughput. No new scientific run was permitted. New-batch reference cost still
depends on its trajectories, width and checkpoint generations. Directory checks
and V2's chain-slot check still grow cheaply with history up to the unchanged
256-batch limit; historical arithmetic does not. Startup and publication remain
proportional to total retained arithmetic and can take appreciable time.

To reproduce locally without adding science:

```powershell
python C:\CEML\tools\session_i1\benchmark.py --out C:\CEML\local\frontier\verification-i1-benchmark.json
```

## Integrity and compatibility evidence

The new tests use only V2's designated small fixtures `[2,146)` and `[146,290)`.
They exercise original native computation and V2 reference/checkpoint operations.
Candidate certificates match the legacy path byte for byte, and the original V2
ledger verifies them independently. Assertions show all between-batch arithmetic
is confined to the new fixture or its checkpoint prefixes; reading old anchors
and the cached ledger triggers no historical arithmetic.

Adversarial coverage includes modified/self-hash-forged certificates, altered
totals with a recomputed digest, duplicate/missing genesis, wrong links/identity,
unexpected files/directories, native/reference disagreement, budget exhaustion,
inspection failure after atomic commit, damaged recovery warnings, unknown pipe
operations/paths, no acceptance and stale acceptance. File tests exercise denied
writes/deletes/renames, ancestor rename protection, preexisting write handles,
writable memory mappings, hardlink aliases and reparse points. Failed attempts
close trust, preserve evidence and cannot authorise a successor. A committed
certificate left by process loss must undergo a new full startup audit.

Validation commands:

```powershell
python -m unittest discover -s tests/session_i1 -v
python -m unittest discover -s tests/operator -v
python -m unittest discover -s tests/publication -v
python tools/frontier/f1_build.py --verify
```

The accepted V2 clean reproducible build still reports
`c0263b353e05b9f3d09730e67d321254952c7dbdc2a6d892f7ffe2b14b89c032`.
All frozen inputs and artifacts are unchanged. The benchmark verifies the byte
hash inventory of 1,456 historical batch/manifest files before and after replay.
No original scientific record was edited. Existing operator controls and
publication tests pass: **23 I1 tests, 28 operator tests and 18 publication tests,
all passing, zero skips**. The frozen L1 phase-gated suite was not rerun in RUN1;
its original identity-bound acceptance remains intact. There is no hosted CI
workflow in this repository; local checks must not be represented as GitHub CI.

Limitations: author-assessed engineering tests, no independent reviewer, no new
OS-blocked L1 acceptance and no end-to-end scientific performance observation.
I1 supports this Windows/accepted-Python environment and deliberately refuses
without kernel read leases. Administrators manipulating process memory/kernel or
raw hostile storage remain outside the integrity boundary; independent publication
replay is still mandatory. No permanent on-disk cache becomes mathematical authority.

## Owner handoff

Further owner acceptance is required to activate I1 because this introduces a
new execution profile, even though the V2 mathematics, native worker and record
format are unchanged. An engineering merge is not that acceptance. Review this
record and its contract, then, if accepting:

```powershell
python C:\CEML\tools\operator\run_frontier.py accept-incremental
```

Type `ACCEPT-SESSION-I1`. This binds the actual installed profile digest and V2
build to an ignored local acceptance record and executes no batch. Future source,
test, launcher or contract changes invalidate it. The agent has not invoked this
action or filled in that acknowledgement.

Then use the existing commands: `run_frontier.py start`, `run_frontier.py stop`,
`live.py start`, `live.py stop`, and `publish.py`. Only the owner starts science.
Until acceptance, start uses the original V2 path. I1 does not enlarge the chain
cap: after the published 208-batch prefix, 48 slots remain, or 479,952 integers
in continuous 9,999-wide batches. Existing conditional claims do not change.
