# CEML-R3E21-12 — Deep mathematical reconnaissance: find NEW exclusion objects, not a sharper version of the current sieve

**FUTURE / UNEXECUTED — requires a NEW, separately owner-authorised session. This document is a queued instruction, not authority to execute it while editing this prompt.**
Repository: `jfairfaxball-348/CEML`. **Research-only mathematics and deep prior-art reconnaissance.** Do not launch scientific Collatz batches, local Codex or an owner's machine, R3E21-2, production worker/verifier or operational V2/I1/I2, identity-bound source/certificates, website/feed/publication, Lean, spending, external correspondence or experimental frontier claims. Do not turn research into an operational claim.

## Why this session exists: a strategic change, not the next packet optimisation

The programme has genuinely reduced the *conditional conservative upper bound on explicit starts not yet excluded* in
`[B,E)`, where `B=2175982616*2^40=2392518188130438742016` and exclusive `E=3*10^21`,
to **330156319374735841 (~3.30×10^17)**. The mathematical progress is substantial. But another small percentage improvement in the same machinery will not make the outstanding obligation meaningfully computable.

**Owner's new objective:** step outside the current optimisation trajectory and conduct an unusually deep, broad, inventive mathematical investigation of the *machinery and assumptions we already have*, looking for **different mathematical objects, structural theorems or exclusion mechanisms** that might collapse the number of integers needing explicit checking by **orders of magnitude**, rather than shaving the existing bound. We are now asking **what else can be proved about whole classes of Collatz starting integers**, not how to compute the present transfer faster.

The current 330156319374735841 is an **upper bound, NOT an exact survivor count**; it assumes only externally reported/assumed `A(B)` (convergence of all positive integers below B). Do not present it as already verified by CEML, a verified global frontier, or a speedup measurement. No 10×, 100× or 1000× saving is a promised result or mandatory theorem; those are *scales of impact to investigate*, not grounds to fabricate a bound.

## Entry and authority audit

1. Independently pin actual **LIVE main**, reconcile R3E21-11 / PR #38's one-authored-commit and normal expected-head two-parent merge, all open/recent PRs and branch history; inspect GitHub Actions, check runs, statuses, jobs, rulesets and branch protection (**403=UNKNOWN, absent CI is NOT PASS**). Halt/reconcile if another R3E21-12 has already executed.
2. Read `PROGRAM_STATUS.md`, `START_HERE.md`, `PROJECT_CHARTER.md`, `ROADMAP.md`, `AGENTS.md`, `docs/CLAIM_POLICY.md`, `NEXT_SESSION_PROMPT.md`, and R3E21-1..11 proofs, reports and their essential executable research fixtures, especially the exact R3E21-4..11 exclusion predicates and their dependency on A(B). Distinguish **proved masks, conditional conservative majorants, exact finite counts, heuristic observations and unexecuted proposals**. Confirm the numerical baseline from committed material; rerun only bounded necessary research fixtures if useful.
3. Construct a concise but mathematically exact **current sieve anatomy**: each exclusion object, what mathematical property makes it valid, where it applies, which families it excludes, what overlaps, where it stops making progress, and which information its abstractions irretrievably discard (parity-prefix / coefficient slope, lower-predecessor/merging, modulo `3^6` inverse classes, CRT phase, packet carry/orientation, early descent, etc.). Pin down which bottlenecks are mathematical (lack of a new exclusion predicate) and which are only computational (cost of evaluating an already valid predicate).

## Main work: search for fundamentally different mathematical objects

Spend **the bulk of the session on discovery, critique and mathematical development**, not another k=4/k=5 packet recursion, faster memo table, narrower CRT phase bound, extra root orientation, or implementation tuning. Prior machinery can be reused as a comparison baseline or as a component of a *genuinely new* object, but routine sharpening is **not the session target**.

Run several serious, independent lines of attack; do not stop at the first mildly interesting observation. Possibilities to explore and challenge include, **without treating this list as exhaustive or requiring a proposal from every category**:

- **New equivalence / coalescence / dominance relations** between starting integers or shortened-map orbit prefixes, perhaps allowing one certified representative to discharge a provably large set of distinct integers. Can paths be linked by new affine or semigroup identities, with strict smaller-start certificates and well-founded dependencies?
- **Reverse Collatz and predecessor-tree objects:** classes of guaranteed smaller ancestors, backward coverings, inverse branching constraints, modular certificates, or a better way to detect that a forward path has met a previously discharged path. Carefully handle the difference between a *smaller integer* and an actually proven or inductively covered one.
- **Residue and local-global phenomena beyond the existing mask:** interactions of 2-adic parity words with 3-adic/inverse-map restrictions, nontrivial compatible congruence covers, lifting or obstructions that exclude entire infinite families rather than just introducing another small modulus.
- **Finite automata, symbolic dynamics and transfer objects of a different type:** invariant languages, forbidden words, stronger long-range compatibility, constrained graph cycles, automata quotients, or certificates which avoid counting vast numbers of individually permissible but jointly impossible prefixes. Determine whether they represent genuinely new information instead of repackaging current parity carry.
- **Stopping-time, energy/potential or invariant inequalities:** prove that broad classes must dip below their starts (or reach already settled material), using exact deterministic witnesses, forbidden growth regimes or arithmetic inequalities, rather than statistical negative-drift intuition.
- **Algebraic/combinatorial coverings and induction schemes:** partition the interval into families with a shared short proof object; graph-theoretic well-founded dependencies; certified interval/cylinder covers; exact disjointness or overlap control; potentially a way to replace per-integer checks with a small collection of universal certificates.
- **Structural lessons from existing mathematics** (Bařina enhanced v2/v3 `fsieve.c` and `smallest_predecessor`, Angeltveit Rust/CUDA/OpenCL and arXiv:2602.10466v1 `search1/precompute/search2/lookahead24/search3`, and other relevant published Collatz/3x+1 work including Tao where appropriate). Independently read the real sources; distinguish what is already known from genuinely different candidate objects. Tao's logarithmic-density result is **not** a deterministic pointwise sieve rule.

**Think freely:** formulate new definitions, equivalence classes, inverse templates, invariants, admissibility obstructions, covering lemmas, intermediate propositions or conjectures. Where an obstruction destroys an avenue, prove and record it rather than quietly discarding it. An attractive finite experiment is only evidence to investigate, never a skip rule.

## A demanding proof/impact gate, not a forced numerical result

For every serious candidate, specify:

1. **Mathematical object and statement**: an exact definition, theorem/conjecture, quantified domain, relation to the shortened map `T(n)=n/2` for even n and `(3n+1)/2` for odd n, and a concise illustrative witness.
2. **Exclusion certificate**: exactly WHY a positive n is safe to skip. Give a complete well-founded proof or mark **CONJECTURAL / PARTIAL / COUNTEREXAMPLE**. Preserve the A(B) assumption, signed/strict inequalities, finite interval boundaries, equality/terminal-path corner cases and induction order. Mere stopping-time density or empirical orbit behaviour does not certify an integer.
3. **Genuinely new information**: explain what the current R3E21-4..11 predicate misses that the new object captures, and why it is more than changing a parameter or accelerating the current transducer. Demonstrate a specific *additional* exclusion (if possible) with an independent oracle.
4. **Scale and overlap**: estimate or bound the *marginal* number of additional [B,E) starts eliminated **after** the existing sieve, not the candidate's stand-alone density. Use exact interval arithmetic or defensible rigorous bounds for numerical claims; otherwise label any scale estimate explicitly **HEURISTIC / UNPROVEN**. Consider correlations, intersection effects, overlap with enhanced external sieves and possible much larger certificates than explicit checks.
5. **Mathematical versus computational feasibility**: what theorem/lemma remains? Could a bounded symbolic calculation or closed family proof establish it? Can the object be represented without walking `2^72` residues or 29.7 quadrillion stopped leaves? Would the new proof itself require an infeasible enumeration?
6. **Prior art / novelty**: a source-matched comparison to actual existing work, with pinned sources and precise overlaps; no unsupported originality or global-champion language.

Seek **high-leverage objects**: tens/hundreds/thousands-fold potential only if logically defensible. An avenue with no proof but substantial plausible upside is welcome as a clearly identified research hypothesis, not as a certified bound. Do not impose an arbitrary numerical target or rush to claim one result per session.

## Mandatory synthesis and research decisions

Produce a **ranked discovery portfolio**, comparing several *distinct* serious routes on theorem potential, possible marginal savings, independence from the current sieve, prior-art overlap, proof obligations, and risk of dead ends. Identify at least one **champion next mathematical bridge** and one credible alternate. Include:

- A failure/overlap map of existing exclusions: what exactly remains unproved about the large residual and why the prior refinements are plateauing.
- Concrete mathematical definitions and strongest valid lemmas reached for the leading candidates, with hostile checks and explicit counterexamples where found.
- A **test that would decisively distinguish** each leading new object from the old machinery, preferably by producing previously nonexcluded high-base residue/interval witnesses or a family theorem.
- A route from the leading new theorem to a rigorous *full, nonaligned [B,E) count or upper bound* with no double-counting, plus what would be needed to approach a tractable explicit-check obligation. If the ultimate cost cannot be quantified yet, explain the missing mathematical bridge without inventing a projection.
- **Go/no-go gates**: whether the next session should aim at proving a new theorem, disprove a tempting conjecture, create an exact finite combinatorial certificate, or undertake deeper prior-art reconstruction.

Do **not** default at the end to wider carry packets merely because they are available. If every candidate fails, document what was ruled out and recommend a *genuinely different* next research angle. A sober negative reconnaissance is preferable to manufactured progress.

## Research fixtures and validation

Small independent exact-arithmetic experiments are authorised **only** to test a new hypothesis, check definitions, expose counterexamples or validate a proposed exclusion certificate. Reuse old bounded fixtures for baseline sanity; do not undertake a full production sweep, full [B,E) scan, pointwise-to-one batch or costly unbounded parameter search. Use signed/irregular endpoints, finite CRT phases, empty/full masks, exact integer arithmetic, strict reverse-witness inequalities, high-base slope constraints and small direct-prefix oracles where relevant. A fixture is **not** by itself a mathematical proof. If a candidate merits a new research-only fixture, make it reproducible with independently checkable expected values and explicit limitations.

Keep **Bařina enhanced** and **Angeltveit full high-base [B,E)** matched counts labelled **INCOMPARABLE** until a true source-equivalent matched comparison is established; retain **NOVELTY UNPROVED** until an adequate literature check supports a more specific claim.

## Deliverables and finish

1. **One substantial mathematical reconnaissance report** in `docs/` containing the machinery audit, new-object portfolio, proofs/obstructions, evidence, marginal-impact gate and ranked research recommendation. A well-organised extensive report is preferred to shallow snippets.
2. **One research-only executable fixture** in `research/` when candidate probes are computationally meaningful; it may be a bounded catalogue/countermodel oracle rather than a full global count. If no honest computational test is suitable, explicitly justify that and supply precise human-checkable mathematical witnesses in the report instead; do not create an ornamental script.
3. A minimal **`PROGRAM_STATUS.md` overlay** preserving all historical authority and baseline truth tiers, and a **FUTURE / UNEXECUTED R3E21-13 prompt** pointing directly at the most substantial open bridge, without prematurely choosing a familiar optimisation.
4. One dedicated research branch, **one atomic authored commit**, inspected diff, reviewed PR, and only an expected-head non-force normal two-parent merge if contemporaneous protection and check evidence permit. Preserve all frozen identities, certificates, records, site/feed and historical scientific totals. **Do not execute R3E21-13 inside R3E21-12.**

**Success is a serious expansion of the mathematical search space and a precisely identified route to new exclusion power—not necessarily a smaller headline bound this session.**
