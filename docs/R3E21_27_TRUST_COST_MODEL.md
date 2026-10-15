# R3E21-27 — auditable numerical/time/cost/trust sensitivity model

Status: research calculation, **not a throughput benchmark** and not a new exclusion or interval certificate. Report: [R3E21-27 feasibility](R3E21_27_COMPUTE_CROWDSOURCING.md).

## Frozen integers (exact)

| Variable | Literal | Semantics |
|---|---|---|
| B | 2392518188130438742016 | author-reported external first incomplete unit start, not CEML reproduced |
| E | 3000000000000000000000 | exclusive target |
| W | 607481811869561257984 | E−B |
| U | 1099511627776 | 2^40 |
| Q | 552501489 | W // U, full units |
| R | 350507499520 | W % U, PARTIAL LAST unit |
| A | 552501490 | total distinct work-unit records Q+1 |
| F | 552501489 + 350507499520/1099511627776 | full-width fractional equivalents |
| M | 326518028938128165 | conditional mathematical possibly-unresolved explicit starts upper; NOT full-work-unit workload |

Exact invariant Q×U+R=W, 0<R<U, final unit [B+Q×U,E), E exclusive, and first Q units pairwise disjoint. Counting 552501490 full units would over-cover beyond E; linear pro-rating final task gives 552501489.3187847 equivalents and the alternative full-unit cost is only ~3.4 seconds larger than the prorated case at 5 s/unit.

## Parameter dictionary

| Parameter | Default | What it really measures |
|---|---:|---|
| t | 5 seconds per full 2^40 unit | author-homepage advertised modern-GPU value, UNREPRODUCED and not pinned to a model |
| r | 1 | reference-equivalent sustained throughput relative to t; later source-matched benchmark required |
| m | 2 | full independent computation attempts per accepted unit, excludes extra arbitration |
| d | 0.5 | average availability/volunteer duty (hypothesis, not observed) |
| e | 0.9 | scheduler/checkpoint/retry/serialization efficiency for completed attempts (hypothesis) |
| N | 1,10,100,1000,10000 | total **installed reference GPU-equivalents**, not registrations |
| p | $0.74/h | Runpod 4090 Secure Cloud observed 10 Aug 2026 per 25 Sep article; not an availability promise |
| Pw | 0.45 kW | hypothetical incremental local GPU+host active draw, not measured |
| c | £0.2632/kWh | Ofgem England/Scotland/Wales default-tariff October 2026 average (special VAT note) |

The independent unit-pipeline rate is accepted units/second = N×r×d×e / (m×t). Tcalendar [365.25-day years] = (F×t)/(365.25×86400) × m/(N×r×d×e). Pseudocode arithmetic: gap = E−B; [Q,R]=divmod(gap,2^40); F=Q+R/2^40; raw_gpu_seconds=F*t; total_gpu_hours=m*raw_gpu_seconds/3600; cloud_dollars=total_gpu_hours*p (PLUS any paid idle); local_kWh=Pw*total_gpu_hours; local_gbp=local_kWh*c (do not double-count cloud power). If the physical validator is slower than the worker, elapsed time is maximum of worker and validator completion paths, NOT just this expression.

## Base scenario: m=2, d=.5, e=.9, r=1, t=5 s

| Installed reference GPUs N | Raw reports/s at assumed duty | Accepted unique units/s after 2× and 90% | Calendar years | Calendar days |
|---:|---:|---:|---:|---:|
| 1 | 0.1 | 0.045 | 389.06 | 142104 |
| 10 | 1 | 0.45 | 38.906 | 14210 |
| 100 | 10 | 4.5 | 3.8906 | 1421 |
| 1000 | 100 | 45 | 0.38906 | 142.10 |
| 10000 | 1000 | 450 | 0.038906 | 14.21 |

Raw reports/s with uninterrupted full duty is 0.2*N; hence at 1000 *continuously busy* devices 200 reports/s and 1000 volunteer devices at 50% duty 100 reports/s. Distinguish reports from quorum-accepted distinct intervals. Completion calendar is optimistic conditional, excluding acquisition, ramp, arbitration backlog and external-base shifts.

### Relative performance / reliability sensitivity

| r relative speed | m complete passes | d | e | N=1000 calendar days | Interpretation |
|---:|---:|---:|---:|---:|---|
| 0.2 | 2 | 0.5 | 0.9 | 710.52 | five times slower than quoted GPU |
| 1 | 2 | 0.5 | 0.9 | 142.10 | base |
| 2 | 2 | 0.5 | 0.9 | 71.05 | source-equivalent 2x efficiency, not observed |
| 1 | 3 | 0.5 | 0.9 | 213.16 | escalation to third full pass |
| 1 | 2 | 0.25 | 0.9 | 284.21 | dropouts / part-time use |
| 1 | 2 | 0.75 | 0.9 | 94.74 | higher continuous availability |
| 1 | 2 | 0.5 | 0.6 | 213.16 | coordinator/validator saturation |
| 1 | 2 | 1 | 1 | 63.95 | unrealistic ideal continuous 2× baseline |

For specified Y years: required N=ceiling(87.5385785546*m/(Y*r*d*e)); default 3-year goal 130, 1-year 390, 90-day goal ~1580 (365.25/90 conversion); these are capability thresholds, not recruitable user estimates.

### CPU / GPU composition illustration

Total N_equiv = Σ(number_of_hosts_of_type_i × observed_sustained_work_unit_rate_i/reference_rate), NOT user accounts. Example only: 1000 CPU cores each assigned a **hypothetical** ratio 1/52 yields N_equiv≈19.23, not 1000, before d and e. The 52.1× GPU/CPU relation was measured on specific historical hardware in Barina 2025; CPU present-day ratio is UNKNOWN until matched workload on actual hardware. One 4090 and one A100 do NOT automatically yield the same N_equiv; rental dollars/TFLOPS don't certify integer/branch throughput.

## Cost matrix (hypothetical matched 5 sec on priced rental GPU)

| Pass policy | GPU-equivalent hours | Cloud at $0.34/h | Cloud at $0.74/h | Cloud at $0.99/h |
|---|---:|---:|---:|---:|
| 1 exact full-width equivalent pass | 767363.18 | $260903 | $567849 | $759690 |
| 2 full independent passes | 1534726.36 | $521807 | $1135698 | $1519379 |
| 3 full passes | 2302089.54 | $782710 | $1703546 | $2279069 |

Prices are source examples from Runpod pages; exact card model, secure/community tier, region, stock, billing, taxes, dispatch and uptime can radically differ. Do not infer 4090 actually does 5 seconds/unit; unqualified conversion is the point of the sensitivity model. At 450 W assumed per active device: one pass = 345313.43 kWh and ≈£90886.49 at 26.32p/kWh; dual passes = 690626.86 kWh and ≈£181772.99, excluding other household load, PUE and capex. Carbon depends on actual marginal electricity mix/location: not estimated here.

## Work reporting and data durability

Unique unit identities A=552501490. Two full result submissions imply 1105002980 minimum attempt receipts before retries (plus coordinator canonical entries). A 1KiB record × 1105002980 ≈1.13 decimal TB, *not* 1.13 TiB; a 200-byte record ≈221 GB. Actual upload/storage and signed transcript size require protocol specification. Bundling K IDs per signed volunteer task reduces task requests to ceil(A/K), not the number of logically distinct accepted subunits: with K=1000, 552502 bundles and each subunit remains separately accounted. GPU time/bundle ~5000 s if t=5 s, with checkpoints; last partial unit retains its clipped end. At 1000 busy worker devices one 5-second unit produces ~200 result reports/s, 1000-ID bundle averages ~0.2 bundle completions/s; for 10000 devices ~2000 or ~2. No protocol/worker exists.

## Fault/verification matrix

| Fault | Accept condition / recovery | Consequence if ignored |
|---|---|---|
| missing or repeated arithmetic unit ID | sorted interval-cover check; uniqueness of accepted unit, overlapping attempt provenance separate | gap invalidates entire claimed contiguous prefix |
| end-of-range partial task | exact [start,end), last endpoint=E, run range-specific reference | silently unverified tail or overrun |
| GPU overflow / CPU GMP absent | explicit overflow to CPU/GMP verified complete job, else HALT | false completion |
| stale baseline B, new external assignments | externally dated assumption tier; independent current-priority audit | false novelty / gap |
| checksum agreement without full computation | independently implemented full replay, golden vectors, spot adversarial replays | fabricated/bug-correlated results |
| fake peers / Sybil hosts | do not count devices as independent solely by account; trusted arbitration and external audit | sham quorum |
| coordinator database loss, split-brain | append-only digested record snapshots and recovery from independent copy | phantom global progress |
| poisoned source or unsafe release | signed reproducible builds, SBOM and version revocation | volunteer security / invalid result |
| late retry/disagreement | keep attempts but one canonical accepted unit transaction; escalate mismatch to HALT | duplicate or contradictory ledger |

Not-yet-proven: a succinct proof-carrying transcript that a third party can check cheaper than redo without trusting the worker. Random spot-checking has statistical risk and is NEVER an exhaustive certificate.

## Independent bounded validation of the arithmetic

JavaScript exact BigInt used for B/E/U/Q/R, with floating point only for displayed rounded rate/time/cost. Cross-check: 552501489×1099511627776+350507499520=607481811869561257984. No Collatz orbit evaluated; no GPU or local scientific worker benchmark executed. No GitHub Actions were configured (zero checks is ABSENT NOT PASS).

## Primary sources

- Barina official report and five-second homepage https://pcbarina.fit.vut.cz/ (observed 15 Oct 2026; first incomplete and first unassigned index 2175982616)
- Barina peer-reviewed paper https://doi.org/10.1007/s11227-025-07337-0 (2 May 2025) and source https://github.com/xbarin02/collatz
- Angeltveit arXiv:2602.10466v1 https://arxiv.org/html/2602.10466 (11 Feb 2026)
- BOINC March 2026 replication/validator docs https://github.com/BOINC/boinc/wiki/Job-replication and https://github.com/BOINC/boinc/wiki/Validators
- Runpod 25 Sep 2026 quote https://www.runpod.io/articles/guides/ai-server-cost and https://www.runpod.io/pricing (8 Oct 2026)
- Ofgem Oct–Dec 2026 https://www.ofgem.gov.uk/news/changes-energy-price-cap-between-1-october-and-31-december-2026
