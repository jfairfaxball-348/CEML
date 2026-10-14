# CEML-R3E21-4 — Find the strongest mathematically certified Collatz sieve

**FUTURE, UNEXECUTED. Run exactly ONE new mathematical research session only upon the owner's next explicit invocation.** This prompt replaces the narrower R3E21-4 mask-comparison proposal; rewriting it is NOT execution of R3E21-4. No scientific frontier batch, production change, hardware job, spending or external contact is authorised.

Repository: https://github.com/jfairfaxball-348/CEML

## Overriding research mission

**Find, understand, rigorously justify, compare and—if possible—improve the mathematical sieve/algorithm that leaves the FEWEST positive starting integers requiring individual Collatz trajectory verification.**

Prioritise **maximal deterministic elimination of whole families of integers**, not practicality, GPU throughput, cost, a chosen bit depth, a predetermined 1% threshold, or the arbitrary ambition of defending CEML's existing sieve. It is fine to conclude that somebody else's method is superior. It is especially valuable to derive a new independently sound rule or mathematically better composition than any established method. If the best surviving approach is already known, identify it accurately and make that the programme's mathematical baseline rather than claiming novelty.

The motivating use case is a complete certified contiguous interval just above an accepted Collatz verification basin (previous illustrative upper target: exclusive 3 × 10^21). **Do not optimise only for all numbers below 2^N without proving that the method remains sound for an arbitrary far-above-baseline interval.** Abstract from the hardware and the frontier target as necessary to pursue the strongest mathematics.

A skipped integer must have a checkable mathematical justification: exact finite forward descent to an already certified smaller integer; exact reverse coalescence from a smaller certified integer; another sound well-founded or independently proved convergence argument; or a theorem covering its entire symbolic/arithmetic family. A density-one statement, low experimental incidence, modular necessary condition, or a hypothetical-cycle obstruction is not a safe exclusion.

## Entry, authority and preserved evidence

1. Pin LIVE CEML main SHA; inspect its governing status, roadmap, charter, AGENTS, claim policy, open/recent PRs, hosted checks, protection, competing R3E21-4 work and the R3E21-3 merged report/fixture. Reconcile actual session numbers and previous work before editing. Do not overwrite concurrent work.
2. Read PROGRAM_STATUS.md, START_HERE.md, PROJECT_CHARTER.md, ROADMAP.md, AGENTS.md, docs/CLAIM_POLICY.md, docs/P1_EXCLUSION_PROOFS.md, docs/P0_REDUCTION_AUDIT.md, docs/R3E21_1_FRONTIER_SCALE_AUDIT.md, docs/R3E21_3_MATHEMATICAL_SIEVE.md, research/r3e21_3_symbolic_sieve.py and the relevant frozen frontier protocol. The separately planned R3E21-2 architecture session has not been executed merely because R3E21-3 completed: leave its status intact.
3. Preserve the proved CEML baseline: existing P1 E2/Q4/P3/M9/S2K4-03, the research-only R3E21-1 depth-5/3-adic families, and R3E21-3's high-n depth-35 + 3^6 reverse-coalescence **0.4150130471% periodic residual**, conditional on the prior convergence basin and not deployed. Independently test all relevant hypotheses and exceptional ranges before using these numbers.
4. Keep peer-reviewed Barina's historical contiguous below-2^71 report, his moving author-reported operational bounds, and CEML's conditional published batch records separate. Do not change any claim or certified endpoint.

## Part A — Find the real mathematical state of the art (source-critical)

Conduct a substantial, current, primary-source research investigation rather than relying on our last session's comparisons.

**Mandatory source leads (verify exact versions, proofs, code and claims):**

- David **Bařina**, *Improved verification limit for the convergence of the Collatz conjecture*, J. Supercomputing (2025), DOI https://doi.org/10.1007/s11227-025-07337-0 ; https://github.com/xbarin02/collatz and https://github.com/xbarin02/collatz-sieve . Reconstruct actual **full** 2^k mask generation: descent, earlier-prefix descent, joining trajectories of lower residues, reverse predecessor rules, and any enhanced recursive/CTZ exclusions. Explain exactly why published esieve-16 reports 1,720 / 65,536 survivors versus CEML's narrower 2,114 / 65,536 at the same k. Distinguish mask generation from the GPU/CPU runtime that applies it; identify effective larger CPU/GPU masks and 3^k options with their provenance.
- **Vigleik Angeltveit**, *An improved algorithm for checking the Collatz conjecture for all n < 2^N*, February 2026 arXiv preprint https://arxiv.org/abs/2602.10466 and https://github.com/vigleik0/collatz . Investigate the *actual proofs and implementation*, especially the adaptive bit-block/branch-and-bound mechanism, descent sieve, modulo-9 preimage sieve, path-merging sieve, odd-even-even sieve, and any stronger theoretical exclusion criterion. Independently evaluate the author's projection of **less than 0.02% explicitly checked below 2^72**—do not silently promote a projected/experimental figure to proved finite deterministic coverage, or assume it transfers to [B,E).
- Other directly relevant published or preprint mathematical improvements to forward stopping-time sieves, exact parity-vector affine formulas, inverse-preimage trees, controlled interval covering, symbolic residue automata, or proof-carrying pruning. Look for genuinely stronger methods, even if they have never been implemented at scale. Prioritise primary papers, independently accessible proofs and source-pinned generators; be sceptical of unreviewed claims.

Do not merely reproduce names, percentages or algorithms. **Reconstruct their exact mathematical acceptance rules and induction dependencies.** Look for hidden early-descent assumptions, positivity thresholds, predecessor order, wraparound/overflow artefacts and duplicate counts. Check applicability to arbitrary starting intervals as opposed to checking everything from 1 upward.

## Part B — Define an apples-to-apples strongest-sieve benchmark

Use T(n)=n/2 for even n and (3n+1)/2 for odd n.

Define a *valid elimination certificate* and a fixed lower-base assumption A(B): all 1 <= m < B converge. Where ascending within a new interval is necessary, explain its induction/atomic-commit dependencies; where an exclusion is independent of previous unchecked n, prove that instead.

For each candidate, at matched coverage domain, report:

- **Exact residual set** (or certified finite bounds) in a specified [B,E), not just the count of raw low-bit mask entries;
- residual fraction and number needing individual trajectories, with proper overlap handling across forward/reverse/mixed sieves;
- exact finite exceptions, thresholds, modulus or automaton state depth, and dependence on B and E;
- symbolic certificate length, construction/checking work, and mathematical scaling as parameters/depth grow;
- optional engineering implications only where they materially affect whether a purported mathematical exclusion is usable. Keep coverage and elapsed time separate.

Compare the *strongest full combinations* actually proved by Bařina, Angeltveit and other contenders, and CEML's depth-35 + 3^6 result. Do not compare CEML depth-35+3^6 with somebody else's depth-16-only subcomponent and call it a victory. Do not multiply densities unless modular independence is mathematically justified, and do not treat one paper's overall number as a residue density without verifying its denominator/domain.

Distinguish **(i) proved general rules, (ii) independently checked finite residue enumeration, (iii) measured implementation performance, (iv) author's extrapolation, and (v) conjectures**.

## Part C — Select and attack ONE mathematical champion

After the comparative audit, choose the **best rigorously justified survivor-minimising method**, whether external or home-grown. Give a defensible reason for the choice. Then undertake an actual proof-first attack instead of producing another literature catalogue.

Suitable primary targets include:

- Derive a stronger *adaptive prefix/affine stopping-time certificate* that prunes additional 2-adic branches, including low-bit prefixes with no descent yet, using exact future bounds or path-merging and a finite exception theorem.
- Find a new exact *mixed forward/reverse* elimination rule with nontrivial added coverage **after** all existing masks (not merely the CRT intersection or a restatement of modulo 9/729 coalescence).
- Derive a mathematically sound *branch-and-bound/finite-state ranking/lifting theorem* that can certify very large symbolic families without enumerating individual residues.
- Translate an overlooked or recently published strong sieve into a more powerful **far-above-baseline contiguous-interval** certificate; prove every dependency needed for induction.
- Prove a general theorem on survivor counts/decay in an adaptive sieve, or a sharp finite-range recurrence/transfer bound, that improves established mathematical coverage rather than relying on heuristic distributions.

Choose at most one secondary ingredient. Define a precise ambitious candidate lemma, derive all identities, seek counterexamples or a no-go theorem, refine to the strongest provable statement, and supply an independently checkable certificate. **No novelty or improvement claims without a line-by-line comparison against prior art.** A rigorously demonstrated already-known winner, with an exact applicability and coverage gap analysis, is preferable to an unsupported original-looking result.

Do not target a predetermined 1%, 0.1%, 0.02% or fixed bit depth as the finish line. Minimise the **number requiring explicit checking as far as rigorous mathematical tools allow**; if one architecture can eventually drive the residual fraction arbitrarily low, distinguish its proved quantitative scaling from an asymptotic conjecture and from potentially unbounded construction cost.

## Part D — Small independent experiments (research only)

Allowed: bounded exact-arithmetic parity/residue enumeration, independent source-algorithm reproduction, test of generator-versus-checker, proof witness construction, small counterexample searches, independent CRT count verification, and symbolic analytic/finite-state reasoning. Where possible build two distinct independent oracles.

Required: prove why a skipped class is safe *for all integers in its domain*, test boundary/exceptional cases, count **incremental uniquely eliminated** classes after the strongest established composite sieve, and clearly label finite experiments as supporting evidence only.

No new CEML frontier verification run, local PC inspection, worker replacement, production LUT change, website update, scientific publication, GPU/HPC acquisition, external researcher contact or spending. Do not silently alter frozen V2/I1/SESSION-I2 identities, certificates or tallies. Any experimental code stays segregated and ineligible for scientific production.

## Part E — Decisive result and next research direction

Produce one substantial source-pinned mathematical report with:

1. **Best existing mathematical sieve/algorithm** and exactly what its proof certifies, with code/paper source references and credible weaknesses.
2. **Fair coverage leaderboard** for the strongest variants and combinations, matched to a common domain and with exact/bounded residual counts. Include CEML's 0.4150130471% baseline and the Angeltveit projection correctly labelled.
3. **Primary new mathematical attack**: candidate theorem, full proof or exact obstruction/counterexample, edge cases and independent checker.
4. **Quantified best achievable proven coverage**, remaining count for the illustrative research interval [B,3×10^21) when meaningful, and what additional theorem would genuinely shrink it further.
5. **Gaps between theory and production** (briefly) without pivoting back to hardware/logistics. A higher exclusion fraction is not automatically a faster worker.
6. **Unambiguous champion decision**: adopt a stronger external method if it wins; retain CEML's method if it wins; or preserve an honest incomparable/undetermined verdict with the smallest decisive missing test. Give the mathematical frontier of what remains unknown.
7. **Repository evidence and next handoff**: research document/fixtures, tests actually executed, and a pointed future **R3E21-5** prompt focused on the highest-value open proof—not another broad preliminary survey.

## Governance and finish

This is ONE independently owner-authorised, research-only session. Respect live CEML AGENTS/claim rules. Keep changes narrowly scoped to research and handoff. A dedicated branch, ONE atomic authored commit, reviewable PR, and expected-head non-force two-parent merge may be used only after the actual checks/permissions are reconciled. Hosted CI missing means **ABSENT**, not PASS; inaccessible branch protection means **UNKNOWN**. Do not bypass protections or claim external independent validation.

**Primary success criterion:** finish with the most powerful *mathematically justified* method currently identifiable for eliminating starting integers from explicit Collatz checks—and, if possible, prove an improvement over that genuine benchmark. Do not execute R3E21-5, do not retroactively complete R3E21-2 and do not claim a new world verification frontier.