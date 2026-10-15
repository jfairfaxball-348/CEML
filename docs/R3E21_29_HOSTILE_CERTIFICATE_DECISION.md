# R3E21-29 — Hostile certificate-compression audit and independent verification decision

**15 October 2026 | RESEARCH-ONLY | NOT A SCIENTIFIC FRONTIER CLAIM**

## Authority, provenance, read-first

Owner's invocation of main's R3E21-29 future prompt authorised this session, not R30. Pinned entry main 717bb508c467172b917dd97f87d4f0f19829b0ab; tree f0558b62ec8640c5dbef3cdea5efe4d756972c85. R28 PR #57, head 4f5d745654fc8ba5b849dd6a97127e737a217288, merge 717bb50, actual two parents af0916dbcc936456b8630d2924118a3832dfb910 and 4f5d745654fc8ba5b849dd6a97127e737a217288. At entry: 0 open PRs, 0 Actions runs, 0 individual check-runs/status contexts (**ABSENT, not PASS**), rulesets [], detailed branch protection 403/UNKNOWN. R27 and R28 reports, the R28 fixture, AGENTS, roadmap, claims policy, Barina's 2025 paper/code, Angeltveit 2026 paper/code links and BOINC validation documentation were considered. No code/source version was asserted immutably pinned for the *external* author's live changing default branch; a reproducible future benchmark must obtain the exact external executable git SHA before approval.

**External status checked 15 October 2026:** Bařina's first-party live page, generated 2026-10-15 11:23:54 CEST, still reported first incomplete AND first unassigned unit 2175982616 × 2^40; its 2075 × 2^60 headline and the author-reported B=2392518188130438742016 are not independently reproduced by CEML. Published 2025 2^71 is a separate peer-reviewed computational assertion. Target E=3000000000000000000000 EXCLUSIVE; conditional conservative candidate upper remains **326518028938128165**, while actual inherited survivors S_old are UNKNOWN. Neither change nor new exclusion count was established this session.

Sources: https://pcbarina.fit.vutbr.cz/ ; https://doi.org/10.1007/s11227-025-07337-0 ; https://github.com/xbarin02/collatz ; https://arxiv.org/abs/2602.10466 ; https://github.com/vigleik0/collatz ; https://github.com/BOINC/boinc/wiki/Validators ; https://www.runpod.io/pricing (page updated 2026-10-08).

## 1. Rigorous obstruction: prefix-only direct descent is not small enough

For shortened T, let s_j be the number of odd steps in an authentic j-bit parity word. Every positive n in that residue cylinder obeys

    2^j T^j(n) = 3^{s_j} n + C_j,  C_j >= 0.

If **3^{s_j} >= 2^j for every 1<=j<=k**, then no n in the cylinder can have strict direct descent T^j(n)<n at any j<=k. This holds *even if the residue is very large* because C_j is nonnegative. In every aligned block of 2^k starts, parity words of length k correspond bijectively to input residues modulo 2^k: extending r by 2^j flips the next parity since the previous affine odd coefficient is 3^{s_j}; induction proves bijection. Thus we can count an explicit, provably obstructed family inside each such block.

Exact integer dynamic programme: a_0(0)=1, a_j(s)=1_{3^s>=2^j}(a_{j-1}(s)+a_{j-1}(s-1)), with a_{j-1}(-1)=0. Summing a_k(s) yields:

| k | No direct descent in first k steps, **proved lower** | Portion of an aligned 2^k block |
|---|---:|---:|
| 8 | 19 | 7.421875% |
| 16 | 2,114 | 3.225708% |
| 24 | 286,581 | 1.708156% |
| 32 | 41,347,483 | 0.962696% |
| 40 | **6,402,835,000** | **0.582334%** |

The recurrence runs in O(k^2) integer operations and was recomputed in the attached independent Python fixture. This is a theorem about the **limited direct prefix-descent leaf language**, NOT a lower bound for all Collatz algorithms, Angeltveit's complete search, or certified general coalescence DAGs. Longer trajectories and genuine reverse/coalescence identities can discharge the obstructed starts. The residual is not an official novel exclusion or remaining-survivor count. The same prefix framework is explicit prior art in Angeltveit 2026; do not claim novelty.

**Conditional certificate-volume stress:** if every one of these 6,402,835,000 residuals needed a distinct 32-byte singleton leaf, that hypothetical fallback would already produce 204,890,720,000 bytes (~205 GB decimal) per aligned 2^40 unit, before tree/paths. It is NOT a proved size lower bound on sophisticated compressed DAGs. Conversely, a single simple r=3 mod16 descent leaf certifies a huge known subfamily but offers no distributional bound for the hard residuals. Theoretical complexity remains O(V poly(k,D)) arithmetic operations, where neither V nor D is known to be small at a true 2^40 task.

## 2. Independent research-only semantic verifier and adversarial outcomes

New separate stdlib file research/r3e21_29_hostile_dag.py is a capped toy certificate grammar and checker, not a replacement for the frozen production verifier. Its nodes are EMPTY, exact binary SPLIT, uniform DESCENT, singleton EXPLICIT, and singleton MEET (the last deliberately does NOT certify an arbitrary affine family). It derives exact half-open residue coverage and nmin from [L,H), reconstructs the entire first k parity word and affine coefficients, rejects false slopes/thresholds and false explicit T steps, checks genuinely smaller positive coalescence witnesses, enforces declared schema, 24-depth/512-bit/8MB/50k-node/512-path toy budgets, recomputes the commitment, and rejects reused DAG node IDs across contexts. This is a **strictly limited correctness check**, not a production proof format or independently reviewed implementation. Recomputing the hash cannot make a false mathematical statement true.

Local stdlib execution (non-scientific toy) printed **R29_RESEARCH_ONLY_PASS 16 adversarial rejection cases** after generating and verifying a clean [1027,1155) record and a clipped 20-start interval crossing 2^40. Explicit rejection cases: missing child MISSING_CHILD; duplicated split child SPLIT_OVERLAP; incorrect minimum FALSE_AFFINE_OR_MIN_OR_WORD; tampered full parity word same; wrapped signed/unsigned u128 affine carry same; >512-bit injected coefficient NONINTEGER_OR_OVERFLOW; forged explicit true step and zero terminal INVALID_TRUE_STEP; context-aliased DAG node CONTEXT_ALIAS; stale/forged checksum HASH_FAIL; r=1 mod16 at actual n=1 NO_UNIFORM_DESCENT; clipped [18,19) incorrectly labelled r=1 mod16 EMPTY_DESCENT; p=0,-5,8 for n=7 BAD_PREDECESSOR; genuine steps ending at unrelated endpoints UNRELATED_ENDPOINT.

Toy [1027,1155) generated 41 nodes (20 SPLIT, 8 DESCENT, 13 EXPLICIT), compact JSON certificate **3966 bytes** versus **4070 bytes** for JSON mapping all 128 toy starts to actual first-smaller paths. The semantic Python verifier averaged approximately **0.277 ms** per toy certificate; enumerating every corresponding first-smaller path averaged **0.113 ms** per toy block (500 repetitions each, same container, uncalibrated). These tiny unoptimised tests are only a falsification of assumed effortless compression/speed, never a performance result for 2^40 or GPU/CPU-GMP comparison. Exact committed GitHub-blob execution / hosted CI are **NOT_RUN/ABSENT**, not PASS; locally tested matching source was authored independently but no reproducible hosted execution is claimed.

**Scope of hostility:** intentionally does not prove arbitrary non-singleton affine MEET, bitvector lookahead interoperability, GPU kernel correctness, cross-vendor 128-bit behaviour, adversarial decompression bombs beyond its static caps, or a globally complete accepted-ledger implementation. The overlarge injected C demonstrates semantic fail-closed handling of a forged overflow-shaped claim, not a test on physical u128 GPU machinery.

## 3. Three different evidence architectures

**A. Independently verified proof DAG:** generator produces a complete covering DAG; verifier accepts only after exact symbolic derivations and all exceptions, plus a separately accepted A(B) induction premise and complete task ledger. This can be mathematical conditional certification without recomputing each trajectory, IF a real compact DAG exists. Presently none is proved generally compressible or generated efficiently at 2^40 scale.

**B. Two full independent exhaustive passes:** run all source-selected candidates/exception cases twice with independently built implementations (prefer distinct authors/toolchains/platforms); require exactly identical canonical task boundaries, algorithm/spec semantics, exception coverage, and independently recomputed exception witnesses. Disagreements go to separately trusted arbitrary-precision CPU/GMP arbitration, not accepted by majority vote. No sparse checksums can replace those passes. This remains the defensible baseline.

**C. BOINC two-/three-host checksum quorum or spot checks:** BOINC validators can accept equivalence across replicas, but replicas are not a semantic proof, and volunteers can be Sybil identities or share software/compiler bugs. Credit and host count do not imply independent correctness. Any future volunteer network needs an identity/independence anti-Sybil model, diverse immutable builds, exception escalation and complete accepted-ledger invariant; not authorisation to recruit now.

**Ledger invariant:** for accepted unit IDs i, authenticated disjoint half-open intervals exactly partition [B,E) with Q=552501489 complete 2^40 units and final 350507499520-value partial unit; each ID has an accepted proof or two independently fully verified agreeing computations; each exception has a trusted fully checked resolution; no accepted/overlapping/gapped/duplicated units; every artifact ties to exact source/spec, B tier, task endpoints and content digest. Until all are accepted, never claim global [B,E) verification. A(B) is still an author-reported premise.

## 4. Quantitative cost gate, not hardware authorisation

Bařina's first-party live page quotes ~5 seconds **average on modern GPUs** for *his* 2^40 work unit, not any particular rentable GPU or the Angeltveit adapted method. At that optimistic reference rate, 552501490 task IDs represent ~767363 GPU-hours for ONE pass, ~1,534,726 GPU-hours for TWO. A third full pass adds another ~767363 GPU-hours. Example vendor list prices on 2026-10-08: Runpod L40S $1.09/h and H100 PCIe $2.89/h, but these are **NOT** device-matched performance/cost forecasts; billing, failures, initialization, storage, staffing, traffic, electricity and data integrity are ignored. No price in GBP is assumed, and no allocation was purchased.

For a particular source-equivalent task, denote two full GPU times G1,G2, generation time Gc, trusted independent validation V and proof transfer/storage cost X. Proof method wins latency/cost *only if* Gc+V+X < G1+G2 (adjust by independently measured device price and energy rates). When Gc≈G1≈G2≈5s, V+X must be <~5s; if DAG generation is already a full verifier with costly output, there is no automatic improvement. In terms of proof bytes P and trusted parsing/validation throughput R, require P/R+other validation overhead to fit that time. This is a decision inequality, not empirical validation or a proved upper bound.

**Falsifiable future benchmark design, gated by NEW owner approval:** exact same [L,H) source-equivalent 2^40-aligned unit plus specified final partial fixture; independently pin author SHAs, build flags, launch parameters, environment, signed outputs and check methods; cold and warm starts separately; measured p50/p95 full GPU time, second source-distinct GPU, full CPU/GMP trusted exception audit, proof generation/check and bytes, failure and cross-vendor 128-bit overflow tests, W/task exact ledger. Require at least 3 timed replications per configuration and specify all aborted jobs. Compare 1/2/3-pass throughput, energy kWh, total traffic, storage and currency-normalised marginal cost. **Budget default £0 and NOT_RUN:** stop and ask the owner before any paid cloud job, local Windows/Codex run, production modification, scientific task, volunteer recruitment, publication or external outreach.

## 5. Explicit decision

**NO:** we have a mathematically sound small *language* for some local certificates, not a **proved fast-to-check, realistically compressible, independently generated 2^40 proof**. No measured speed or cost advantage over Bařina's mature GPU implementation or Angeltveit's long-bit recursive method was established. Both the prefix method and lookahead/merging are pre-existing in those sources; the exact capped toy grammar is not shown scientifically novel. **RETAIN TWO COMPLETE SOURCE-INDEPENDENT EXHAUSTIVE PASSES plus high-trust independent GMP arbitration** as the default roadmap; allow future unfunded read-only algorithm comparisons and owner-approved source-equivalent benchmarks, but do not move the system into proof-only/BOINC-quorum mode. The only new rigorous result in R29 is a restricted-family counting obstruction, not a general Collatz theorem.

No local owner-machine runs; no scientific intervals, changes to source worker/frozen certificates/protocols/site/feed, spending, contacts or new global frontier. No R3E21-30 execution.
