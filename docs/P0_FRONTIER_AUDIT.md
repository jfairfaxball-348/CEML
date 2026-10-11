# CEML-P0 — Frontiers, source hierarchy and starting snapshot
Research date: **2026-10-11** (UK); primary live project page generated `Sun, 11 Oct 2026 13:29:26 +0200` as surfaced at retrieval. Retrieval is NOT a perpetual live guarantee.

## Exact exclusive endpoints and evidence
| Class | Evidence / source | Every positive n below B reported verified; B exact |
|---|---|---|
| A, peer-reviewed | David Bařina, *Improved verification limit for the convergence of the Collatz conjecture*, Journal of Supercomputing 81, 810 (2025), https://doi.org/10.1007/s11227-025-07337-0 (2 May 2025) | B = 2^71 = **2361183241434822606848** |
| Historic peer-reviewed | Bařina, *Convergence verification of the Collatz problem*, J. Supercomputing 77, 2681–2688 (2021), https://doi.org/10.1007/s11227-020-03368-x | earlier 2^68 = **295147905179352825856**; overtaken |
| B, live headline | Bařina's current primary operational https://pcbarina.fit.vut.cz/ (2026-10-11 retrieval) | B = 2075*2^60 = **2392312122059207475200** (rounded-to-2^60 public statement) |
| C, live exact work-unit pointer | Same live page, showing "Lowest incomplete: work unit 2175982616 * 2^40; all work units below are verified" | B = 2175982616*2^40 = **2392518188130438742016** (author-reported contiguous completed prefix, NOT independent reproduction) |
| D, pending/unassigned | Same live page: "Lowest unassigned" equals work unit 2175982616 at snapshot; work unit size 2^40 = **1099511627776** | first not-claimed-complete unit **[2392518188130438742016, 239251928764206651?]** — use exact formula `[2175982616*2^40, 2175982617*2^40)`; never infer this unit is permanently unassigned |

**Authoritative exact end of first incomplete unit:** 2175982617*2^40 = **239251928764206651?** [P1 must independently recompute this decimal; the exact formula, not this human display, governs]. This row deliberately does NOT certify this interval.

The 2025 paper describes 2^40-sized distributed tasks, a work-unit checksum, overflowing-state counts and maxima, assignment/server metadata, and CPU/GPU C/OpenCL implementations with 128-bit arithmetic plus CPU GMP fallback. Published project claim is that 2^71 was reached on 2025-01-15. Repository reference: https://github.com/xbarin02/collatz; author implementation description (CTZ and n/n+1 switching): https://github.com/xbarin02/collatz/blob/master/doc/ALGORITHM.md. The site does not expose to this P0 audit a complete independently verifiable manifest of *every* completed live unit and independent re-run. No project data was downloaded or certified.

## Cross-checks, alternative computations and independence
- Oliveira e Silva's historical verification through 5*2^60 and Roosendaal's earlier work are discussed in Bařina 2025 section 2 and Roosendaal https://ericr.nl/wondrous/ (site updated June 2026). Roosendaal reports yoyo@home reached 87*2^60 in 2017, twice checked; and distinguishes older multi-checked intervals (5*2^60 at least three times; 2^60 in four projects). These are smaller than today's reported frontier.
- The independent path-record/class-record projects may explore isolated starts beyond contiguous basins. Such samples do NOT establish exhaustive intervals; a highest path record is not a verified bound.
- An independently circulated July 2026 preprint by Rafik Zeraoulia (Zenodo 10.5281/zenodo.21695296) reports independently testing [2^71, 2^71+2^40), but this single unit sits **inside** Bařina's substantially larger live reported basin. Its full supporting logs were not independently inspected at P0; do not promote it as a higher global boundary.
- No primary evidence of an alternate newer **higher contiguous** frontier was established in this bounded audit. This is NOT a proof none exists.

## Snapshot and novelty policy
**P0 snapshot candidate:** `source_date=2026-10-11`; `published_exclusive_B=2361183241434822606848`; `operational_reported_exclusive_B=2392518188130438742016`; `work_unit_size=1099511627776`; `first_reported_incomplete_unit=2175982616`; `source_url=https://pcbarina.fit.vut.cz/`; `status=AUTHOR_REPORTED_NOT_REPLICATED`; `snapshot_identifier=CEML-P0-FRONTIER-20261011`. This is **research evidence**, not a valid RUN1 configuration file. P2 must freeze an exact-format, content-digested locally supplied file.

**Published-base mode:** CEML can accept published B=2^71 as an externally peer-reviewed input; a claimed gap-free extension above any later B must account for each intervening number. **Operational-report mode:** start at current reported lowest-incomplete B only with explicit `external_baseline_assumed` labeling. Such batches are conditional on the author's reported lower coverage; they are *not* standalone independent proof of all earlier numbers. Never borrow published-only credibility for live-only intervals. A local run may independently repeat an individual interval without independently replicating all smaller ranges.

"Beyond published", "beyond contemporaneously reported completed work units", "locally checked", "independently reproduced", and "new world-first verified coverage" are DISTINCT claims. Before a claimed novel run, cloud research may refresh the primary-source snapshot and scan other public work-unit/single-start records; offline computation MUST NOT perform live queries. Snapshot dates are historical; later public advances do not retrospectively change what a run actually verified. To claim globally new contiguous coverage, independently establish completed lower segments and contemporaneous global state.

## Feasibility
Bařina's live homepage advertises approx. five seconds per 2^40-start work unit on a modern GPU, a hardware-/implementation-specific figure. The paper distinguishes integers certified/sec from trajectories or Collatz operations/sec, claims up to 52x GPU-vs-CPU throughput and 1335x improvement from the original baseline. Neither figure predicts CEML i7 throughput. A local single-CPU/GMP front can be orders slower than the distributed service. First milestone: correct short pilot of an interval believed unverified when selected, with honest status; a world record is conditional. Do not invent an offline benchmark.

### Outstanding independent source work for P1/P2
Obtain or explicitly record absence of accessible unit-level completion manifests/replication checksums; inspect source-pinned work-unit indexing, input coverage and checksum meanings; recheck site's live lowest-incomplete and other newer projects immediately before freezing RUN1 snapshot. Source publication vs operational reporting vs checksum matching must remain separate even when their decimal bounds coincide.
