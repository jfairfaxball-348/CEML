# CEML Roadmap

This roadmap is gate-based. Dates are intentionally absent; evidence, not schedule pressure, controls progression.

## BOOTSTRAP — governance and planning

Deliver repository scaffold, charter, research protocol, claim boundaries, hardware-audit framework, schemas, integrity rules, and a gate model. No production implementation or scientific computation.

## CEML-R1 — state-of-the-art and literature audit

Research and cite:

- largest credible isolated-start Collatz computations;
- published high-magnitude evaluation algorithms;
- Elsenhans-style Collatz-polynomial/batching methods;
- peer-review and publication status;
- public implementations and independent reproductions;
- claimed performance and the conditions under which it was measured;
- known correctness caveats.

**Exit evidence:** completed `docs/LITERATURE_AUDIT.md` with source-level citations, claim confidence, reproducibility notes, unresolved questions, and no inherited authority.

## CEML-R2 — algorithm and implementation audit

Compare naive stepping, odd-only stepping, affine batching, Collatz-polynomial batching, binary splitting, super-batching, GMP, FLINT, Rust, C/C++, and Python orchestration.

**Exit evidence:** `docs/ALGORITHM_AUDIT.md` identifies viable architecture families, mathematical invariants, correctness risks, and what must be benchmarked locally. It must not choose machine-specific parameters.

## CEML-R3 — reproducibility and validation audit

Freeze scientific semantics for:

- magnitude/rung definition;
- deterministic random-start generation and seed handling;
- exact Collatz map and step accounting;
- manifests and hashes;
- independent reference oracle;
- fixtures and differential tests;
- checkpoint semantics;
- anomaly/freeze rules;
- result certification requirements.

**Exit evidence:** approved protocol versions and machine-readable schemas. Scientific master seed still need not be generated at this gate.

## CEML-R4 — Codex hardware-audit specification

Freeze what C1 may inspect, record, benchmark, and optimize, with privacy exclusions and bounded-work limits.

**Exit evidence:** `docs/HARDWARE_AUDIT_SPEC.md` is complete enough to constrain a local automated audit without inventing a machine profile.

## CEML-I1 — hardware-adaptive implementation specification

Produce the one self-contained Codex brief. It must distinguish frozen scientific invariants from hardware-dependent engineering choices and define acceptance tests, interfaces, dependencies, checkpoint semantics, and prohibited scientific execution.

**Exit evidence:** `docs/CODEX_HANDOFF.md` changes from NOT READY to APPROVED with references to all frozen prerequisites.

## CEML-C1 — local hardware audit and implementation

On the dedicated local machine, Codex must:

1. inspect and sanitize the environment;
2. write human- and machine-readable hardware reports;
3. run bounded deterministic engineering benchmarks;
4. choose architecture from measured evidence;
5. implement/build the system;
6. freeze the local machine/build profile;
7. document every hardware-dependent choice.

**Prohibition:** no giant scientific rung.

## CEML-V1 — local implementation validation

Run layered offline validation: identities, independent oracle comparisons, randomized differential tests, known fixtures, implementation diversity where practical, and scale-ladder validation below scientific magnitude.

**Exit evidence:** all required checks pass with recorded hashes and environment/build identity.

## CEML-E1 — first scientific ladder

Only now may the final ladder and seed protocol be frozen and executed. One predetermined start per rung; no rerolling for interest. Every completed rung produces a compact result record and reproducible provenance.

An anomaly freezes progression and enters a separate audit state. A possible nonconvergent object would require a distinct certification programme rather than silently expanding CEML.
