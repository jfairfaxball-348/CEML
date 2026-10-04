# CEML-R1 Literature Audit

Status: **COMPLETE — CEML-R1 PASS**

Decision date: **2026-10-04**  
External-source access date for this audit: **2026-10-04**  
Research stage completed: **R1 — literature and implementation evidence audit**  
Gate transition: **R1 PASS; R2 becomes the current research gate in the same reviewed repository snapshot as this audit**  
Scientific execution: **NOT AUTHORIZED**

## 1. Scope and decision

CEML-R1 asked a deliberately narrower question than either a proof programme or a contiguous Collatz verifier:

> What is the strongest current evidence for evaluating one isolated, extremely large positive integer exactly along its Collatz trajectory, and what algorithms and public implementations are credible enough to carry into a separate implementation audit?

The audit finds a clear current primary source for near-linear, exact isolated-start evaluation: Andreas-Stephan Elsenhans's standard-polynomial / affine macro-step algorithm, presented at ANTS XVII in July 2026 after an earlier 2025 arXiv preprint. The ANTS paper reports random starts through 10 billion decimal digits in its timing table and separately reports an author computation of a 20-billion-decimal-digit number using Magma, taking about 28 hours and 70 GB of memory.

That is the strongest primary scale demonstration found in this audit. It is **not** treated as independently reproduced. The paper does not identify the exact 20-billion-digit start or its total step count in the paper body, and CEML did not inspect the linked compressed code/data archive byte-for-byte in this session. Therefore CEML records the 20-billion-digit experiment as a high-confidence **author-reported computation**, not as a CEML-reproduced result.

The audit also found public implementations and older exact-start results that are much smaller but more independently cross-checkable. In particular, the open C++/GMP implementation Boutoukoat/Collatz-steps-on-large-numbers reports the standard-map total stopping time of the exact Mersenne start 2^82589933-1 as 1,111,148,968; an independent public rerun by Hermann-SW reports the same value, and OEIS A181777 records the same result. That exact start has 24,862,048 decimal digits. This is not a formal code audit, but it is stronger public output agreement than exists for the Elsenhans 20-billion-digit run.

R1 therefore passes because the required evidence classes, caveats, implementation landscape, source provenance, performance conditions, and unresolved questions have been established. R1 passing does **not** select a production architecture, certify any external implementation, authorize a scientific run, freeze the magnitude ladder, or select machine-specific engineering parameters.

## 2. Search methodology

The repository on main was read first and treated as the sole authority for CEML governance. No research state, design, terminology, or conclusions were imported from any earlier Collatz repository.

External research then used the following source hierarchy:

1. primary papers and author-hosted papers;
2. conference/publisher metadata;
3. author institutional pages and linked research supplements;
4. public source repositories and their current manifests/README files;
5. issue trackers and independent rerun artifacts;
6. curated secondary databases such as OEIS;
7. community discussions only when they supplied a lead or a clearly attributable claim.

Searches explicitly attempted to find:

- exact isolated-start computations at extreme magnitude;
- primary sources for Elsenhans's method and its predecessors;
- public code corresponding to the claimed methods;
- independent reproductions, disagreements, critiques, bug reports, or portability failures;
- hardware/software conditions behind performance claims;
- contemporary contiguous-verification work, solely to prevent category errors.

Negative findings are preserved below. Absence of a found critique, issue, or reproduction is not evidence of correctness.

## 3. Terminology and step-accounting conventions

A central audit finding is that published and public implementations do not use one universal Collatz step convention. CEML-R2 and especially CEML-R3 must make conversion rules explicit.

### 3.1 Standard map

This audit calls the conventional map C:

- C(n) = n / 2 when n is even;
- C(n) = 3n + 1 when n is odd.

Under this convention, the standard total stopping time is the number of individual C applications required to reach 1.

Boutoukoat/Collatz-steps-on-large-numbers uses this convention; its example gives 27 a total stopping time of 111.

### 3.2 Shortcut map

Elsenhans defines the shortcut map T:

- T(n) = n / 2 when n is even;
- T(n) = (3n + 1) / 2 when n is odd.

One Elsenhans elementary step is one T application. The collatz-eval crate uses the same shortcut map and gives 27 a shortcut total of 70.

If a shortcut trajectory contains I odd shortcut steps and O ordinary even shortcut steps, then:

- shortcut-step total = I + O;
- standard-map total = 2I + O.

Wei Ren's later I/O notation uses the same shortcut operations, with I = (3x+1)/2 and O = x/2. For 2^100000-1, the 2019 data paper gives I = 481,603 and O = 381,720. Thus the shortcut total is 863,323, while the standard-map total is 1,344,926. The earlier 2018 IEEE paper expresses the same trajectory as 481,603 applications of 3x+1 and 863,323 divisions by 2.

### 3.3 Odd-only map

An odd-only map may replace an odd n by

U(n) = (3n + 1) / 2^v2(3n+1).

If q = v2(3n+1), one U step represents q shortcut-map T steps and q+1 standard-map C steps. An implementation that reports odd-only iterations without also preserving q cannot reconstruct either conventional step total.

### 3.4 Stopping time versus total stopping time

In Elsenhans and the classical literature used here:

- stopping time = steps until the first value smaller than the start;
- total stopping time = steps until 1.

Some other sources use “stopping time” for the reach-1 count. Ren 2023 does this for the 6,000,000-bit experiment. CEML must not copy a source's label without also recording its actual endpoint and map convention.

## 4. Evidence/source table

Confidence labels are CEML assessments of what the cited source establishes, not ratings of the authors.

| ID | Source and stable locator | Author / publisher / date | Source type and status | Exact proposition used by CEML | Conditions / independent reproduction / caveat | CEML confidence |
|---|---|---|---|---|---|---|
| E01 | https://antsmath.org/ANTSXVII/papers/antsxvii-elsenhans-paper.pdf | Andreas-Stephan Elsenhans; ANTS XVII, Groningen; July 2026 | Primary conference paper presented at ANTS XVII | Defines shortcut T; standard-polynomial affine batching; binary splitting; macro-step algorithm; timing table through 10^10 decimal digits; separate 2×10^10-digit author run; conditional complexity result | 10^4–10^10 table: one core Intel i7-12700 at 4.7 GHz. 2×10^10 run: Magma, ~28 h, ~70 GB. Not independently reproduced by CEML. Exact 2×10^10 input not stated in paper body. | High for what the paper reports; medium for reproducibility of the largest experiment |
| E02 | https://arxiv.org/abs/2502.16743 | Andreas-Stephan Elsenhans; submitted 2025-02-23 | Primary preprint, arXiv:2502.16743 | Establishes the earlier public preprint and version history | Preprint is not itself evidence of peer review. Current audit uses the later ANTS paper for the mature method/results. | High |
| E03 | https://antsmath.org/ANTSXVII/papers.html and https://www.claymath.org/events/algorithmic-number-theory-symposium-ants-xvii/ | ANTS XVII / Clay Mathematics Institute; 2026 | Conference metadata | ANTS XVII lists Elsenhans's paper, code and talk; Clay states contributed talks are selected through a competitive submission and review process | This supports “conference-reviewed/presented”; it is not a code audit. The exact journal/proceedings bibliographic record for Elsenhans was not independently resolved here. | High |
| E04 | https://www.mathematik.uni-wuerzburg.de/en/computeralgebra/team/elsenhans-stephan-prof-dr/research-supplements/ and linked archive https://www.mathematik.uni-wuerzburg.de/fileadmin/10040131/Magma-Skripte/collatz_2026.tar.gz | Elsenhans / Universität Würzburg; linked from 2026 paper | Primary research-supplement locator | Public code/data archive exists for the paper | The archive is compressed; CEML's web environment located it but did not byte-inspect it in this session. License, exact giant-start files and build details remain to be audited in R2. | High for availability; open for artifact contents |
| E05 | https://doi.org/10.1016/0898-1221(92)90034-F and author-hosted report https://www.cs.ucf.edu/~leavens/tech-reports/ISU/TR92-01/TR.pdf | Gary T. Leavens and Mike Vermeulen; Computers & Mathematics with Applications 24(11), 1992 | Primary peer-reviewed journal article plus technical report | Historical “composite/standard polynomial” compression: fixed low bits determine multiple exact Collatz steps represented by one affine rational polynomial | Historical fixed-size search context, not an extreme arbitrary-precision implementation. | High |
| E06 | https://doi.org/10.1109/SmartWorld.2018.00099 | Wei Ren et al.; IEEE SmartWorld 2018 | Primary conference paper | 2^100000-1 reaches 1; 481,603 odd 3x+1 operations and 863,323 divisions by 2; file/bit representation proposed for very large starts | Historical “largest” wording is obsolete. Algorithm is not the current fast asymptotic approach. | High for author report |
| E07 | https://doi.org/10.3390/data4020089 | Wei Ren; Data 4(2):89; 2019-06-21 | Primary data/code paper | Public C code/data; for 2^100000-1, 481,603 I operations ((3x+1)/2) and 381,720 O operations (x/2), clarifying shortcut step accounting | Dataset license reported CC-BY. “No upper bound” is an algorithmic representation claim, not evidence that arbitrary finite resources suffice. | High |
| E08 | https://eprint.iacr.org/2023/648 | Wei Ren; Cryptology ePrint 2023/648, revised 2023-05-17 | Primary preprint; ePrint explicitly labels it “Preprint” | Random 6,000,000-bit odd start, reported shortcut-style reach-1 count 28,911,397; laptop/compiler configuration and timing 8d1h40m44s | Exact start is not reproduced in this audit. Related work later appeared as a 2026 Mathematics Open article, DOI 10.1142/S2811007225500233. | Medium-high as author report |
| E09 | https://github.com/DRMacIver/collatz-eval | David R. MacIver; v0.1.0; latest inspected main commit 0f5ad6da40171cdcd68ce167776a0644ceb942dc, 2026-08-08 | Public Rust implementation, MIT | Shortcut-map engine; Dense/Sparse representations; optional GMP super-batch; optional FLINT multiplication routing; optional independent rug oracle | README explicitly says very little human auditing and likely flaws; precise large-scale benchmark suite is not yet established. No formal independent audit found. | High for repository facts; low-to-medium for unvalidated extreme-run performance |
| E10 | https://github.com/Boutoukoat/Collatz-steps-on-large-numbers | Boutoukoat; latest inspected main commit ec82c0a7e248add8f3f6d16b07cda0aae4e7ebfd, 2025-04-29 | Public C++/GMP implementation, MIT | Standard-map total stopping time for large expressions/Mersenne numbers; published example outputs through 2^345678877-1 | README attributes underlying asymptotic speed idea to R. Gerbicz forum work. Primary Gerbicz post was not fully audited here. README benchmark hardware/compiler/library versions are incomplete. | Medium-high for public outputs; open for algorithm proof and performance |
| E11 | https://github.com/Boutoukoat/Collatz-steps-on-large-numbers/issues/1 | Hermann-SW and repository maintainer; 2024-10-22 | Public issue / portability evidence | GMP 6.2.1 builds initially failed on Ubuntu 22.04 and Raspberry PiOS due mpz_mullo/link/architecture issues; reporter later got builds working after library-path changes | Evidence of portability/build fragility, not evidence of incorrect arithmetic. | High |
| E12 | https://gist.github.com/Hermann-SW/f44c3500b8db158eb87ae8c2fd010e21 | Hermann-SW; 2024-10-22 | Independent public rerun artifact | Rerun of Boutoukoat code reports 2^82589933-1 -> 1 in 1,111,148,968 standard steps and 2^136279841-1 -> 1 in 1,833,585,702 standard steps | Shell hostname contains “7950x”, but CEML does not infer an exact CPU specification from that label. Build configuration is incomplete. | Medium-high for output agreement; low for benchmark comparability |
| E13 | https://oeis.org/A181777 | OEIS contributors; current entry inspected 2026-10-04 | Curated secondary sequence record | Records standard-map total stopping times for Mersenne primes; M82589933 = 1,111,148,968; M136279841 = 1,833,585,702; notes independent confirmations/contributors | Useful cross-check, not a formal software audit or primary computational certificate. | Medium-high |
| E14 | https://link.springer.com/article/10.1007/s11227-025-07337-0 and https://pcbarina.fit.vut.cz/ | David Bařina; Journal of Supercomputing 81:810; published 2025-05-02 | Primary peer-reviewed journal article and live project page | Contiguous verification reached 2^71 in the paper; live project reports all starts below 2075×2^60 ≈ 2^71.02 verified | Fundamentally different workload: interval verification with bounded-width optimized CPU/GPU workers, not one extreme arbitrary-precision start. Included to prevent conflation. | High |
| E15 | https://www.reddit.com/r/Collatz/comments/13g7cb0/largest_number_ever_tested/ | Multiple community users; thread begun 2023, later updates | Community discussion, secondary/weak | Includes a claim of a C+GMP Elsenhans translation evaluating 2^33219280950-1 (10,000,000,001 decimal digits by CEML digit conversion) in under 23 h, plus other multi-million-digit reports | No durable code/build/result artifact or independent reproduction established for this claim. The thread is reference [11] in Elsenhans's comparison figure, so its evidentiary weakness matters. | Low |

## 5. State-of-the-art summary

### 5.1 There is no useful unconditional “largest integer ever tested”

A literal ranking by numerical starting value is scientifically unhelpful. Arbitrarily large easy starts can be manufactured, for example powers of two, and sparse/formula-defined starts may have representations far smaller than their decimal expansions. CEML therefore compares:

- explicit starting magnitude;
- whether the start is arbitrary/random or specially structured;
- whether the exact start is recoverable;
- whether the trajectory was computed to 1 or only to a smaller value;
- the map/step convention;
- algorithm and arithmetic representation;
- hardware/software conditions;
- surviving code/data;
- independent output agreement.

### 5.2 Strongest primary extreme-scale evidence found

The 2026 Elsenhans ANTS paper is the clearest current primary evidence for exact isolated-start computation at the scale relevant to CEML.

Its tabulated experiment includes one random 10,000,000,000-decimal-digit start reaching 1 after 160,079,821,246 shortcut-map elementary steps in 13.2 hours on one core of an Intel i7-12700 at 4.7 GHz using the Magma implementation.

Separately, the paper states that the largest number checked by the author had 2×10^10 decimal digits, approximately 8 GB in binary representation; the Magma computation took about 28 hours and used 70 GB of memory.

CEML did not find an independent reproduction of the 20-billion-digit experiment. The exact start, result count and result digest are not in the paper body. The linked research-supplement archive may contain stronger provenance, but its contents were not inspected in this R1 environment. Thus the experiment is credible and highly relevant, but not fully reproducible from the paper alone.

### 5.3 Stronger output cross-checks at smaller scale

Boutoukoat's C++/GMP repository reports:

- 2^82589933-1: 1,111,148,968 standard-map steps;
- 2^117385963-1: 1,579,841,291 standard-map steps;
- 2^345678877-1: 4,651,594,256 standard-map steps.

The final exponent corresponds to 104,059,711 decimal digits, by the exact digit-count formula floor(p log10 2)+1 for 2^p-1. The repository README supplies timings but not enough hardware/software context to treat them as portable benchmarks.

For 2^82589933-1, an independent public rerun by Hermann-SW reports the same 1,111,148,968 standard steps, and OEIS A181777 also records the same value. That start has 24,862,048 decimal digits. Hermann-SW also reports the OEIS value 1,833,585,702 for 2^136279841-1, a 41,024,320-decimal-digit start.

These agreements are valuable validation signals. They are not equivalent to a documented source audit, proof of the algorithm, or independent reproduction of the Elsenhans scale.

### 5.4 Historical exact large-start evidence

Ren's 2018/2019 work gives a particularly useful exact, public convention bridge for 2^100000-1 (30,103 decimal digits):

- 481,603 odd 3x+1 operations;
- 863,323 total divisions by two;
- equivalently 481,603 shortcut I operations and 381,720 shortcut O operations;
- 863,323 shortcut steps;
- 1,344,926 standard-map steps.

Ren's 2023 ePrint reports a random 6,000,000-bit odd input, about 1,806,180 decimal digits, reaching 1 in 28,911,397 shortcut-style operations after 8 days 1 hour 40 minutes 44 seconds on a Lenovo ThinkPad X1 Carbon with Intel i7-10510U, 8 GB RAM, 64-bit Windows 10 and MinGW Developer Studio 2.05/GNU GCC. This is author-reported and not independently reproduced here.

### 5.5 Contiguous verification is a separate state of the art

Bařina's peer-reviewed 2025 work verifies all starts below 2^71, and the current project page reports progress beyond that to 2075×2^60. This is a major computational Collatz result, but its algorithms optimize a different problem: vast numbers of bounded-width starts, often stopping once a trajectory reaches a previously covered lower value.

CEML must not use that bound as an isolated-start magnitude record or infer that its GPU/128-bit architecture transfers to billion-digit arbitrary-precision trajectories.

## 6. Elsenhans-style method

### 6.1 Publication and review status

The method first appeared publicly as arXiv:2502.16743 on 2025-02-23. The current source inspected is a nine-page paper presented at the Seventeenth Algorithmic Number Theory Symposium (ANTS XVII), Groningen, 6–10 July 2026.

The official ANTS paper page lists the Elsenhans paper with code and talk. ANTS/Clay describe contributed talks as chosen through a competitive submission and review process. CEML therefore classifies the 2026 item as a reviewed conference paper/presentation. This classification does not imply that the source code or the largest run received an independent code audit.

### 6.2 Mathematical core

For k steps, the low k bits of n determine the parity decisions made by the shortcut map T. For each residue r modulo 2^k there is therefore an exact affine rational map

S_(k,r)(X) = (aX+b) / 2^c

such that S_(k,r)(n) = T^k(n) whenever n ≡ r mod 2^k.

Elsenhans calls these standard polynomials and cites Leavens and Vermeulen's 1992 Section 2.3.2. The representation is a triple <a,b,c>. Exact composition preserves affine form.

The key composition identity is simply the functional identity T^(k+l) = T^k composed with T^l, restricted to the residue class that fixes the relevant parity pattern. This allows a large standard polynomial to be built recursively from smaller ones.

### 6.3 Binary splitting and macro steps

Elsenhans supplies Magma pseudocode/functions for:

- direct construction of a short standard polynomial;
- exact evaluation of a triple at an integer;
- exact affine composition;
- a table of all short polynomials for lengths 1 through 8;
- PolyFast, which recursively splits a requested k-step block roughly in half.

The main trajectory loop chooses

StepSize = max(1, floor(log2(n)/2)),

constructs the relevant standard polynomial from the current low bits, applies it once, and increments the elementary-step counter by exactly StepSize.

This is exact batching, not approximation or probabilistic skipping.

### 6.4 Step accounting and the terminal boundary

The paper's count is in shortcut-map elementary steps. Each macro step has a declared exact length k, so the count advances by k.

The paper also notes an important terminal-boundary issue: a macro step longer than roughly the current bit length can jump beyond the first occurrence of 1. Its macro-step denominator parameter D is therefore not allowed below 1. CEML-R2 must turn this observation into an explicit correctness obligation: the implementation must detect/restrict the final block so that “first reaches 1” accounting is exact rather than merely landing on a later point in the 4-2-1 cycle.

### 6.5 Complexity claim

For numbers n in the set G_c that reach 1 within c·B(n) shortcut steps, where B(n) is bit length, the paper proves:

- direct stepping costs O_c(B(n)^2) bit operations;
- computing a k-step standard polynomial by the recursive method costs O(k log^2 k log log k);
- one macro step at k ≈ B(n)/2 costs O(B(n) log^2 B(n) log log B(n));
- the full algorithm is O_c(B(n) log^2 B(n) log log B(n)).

This is a **conditional domain statement**, not an unconditional proof that every trajectory has near-linear cost. The paper explicitly notes that a fully general complexity proof of the observed form would imply the Collatz conjecture.

CEML must not quote the asymptotic result without the G_c condition.

### 6.6 Author-reported performance

All values in the main timing table were computed on one core of an Intel i7-12700 running at 4.7 GHz:

| Decimal digits | Examples | Average shortcut steps to 1 | Std. dev. | Magma time per number |
|---:|---:|---:|---:|---:|
| 10,000 | 10,000 | 160,085 | 1,531 | 0.02 s |
| 100,000 | 10,000 | 1,600,728 | 4,838 | 0.25 s |
| 1,000,000 | 10,000 | 16,007,868 | 15,177 | 2.72 s |
| 10,000,000 | 10,000 | 160,077,568 | 48,567 | 31 s |
| 100,000,000 | 4,000 | 1,600,785,302 | 152,901 | 353 s |
| 1,000,000,000 | 400 | 16,007,824,543 | 515,453 | 1.13 h |
| 10,000,000,000 | 1 | 160,079,821,246 | — | 13.2 h |

The paper says an optimized C/GMP implementation is about 7.5 times faster than Magma at one million decimal digits and about 3.5 times faster at one billion digits. It does not give enough compiler, OS, GMP version, build flags, or memory detail for these ratios to be treated as generally reproducible benchmarks.

A separate macro-step experiment uses n0 = 13^(10^6)-1 and tests StepSize = max(1,floor(log2(n)/D)). The reported Magma times for D = 10,6,5,4,3,2,4/3,1 are 3.11, 3.08, 3.03, 3.01, 3.01, 3.04, 3.05, 3.06 seconds; corresponding C times are 0.48, 0.41, 0.41, 0.40, 0.41, 0.42, 0.45, 0.47 seconds. The paper concludes that D between about 2 and 5 worked best for those tests.

CEML records this only as an author benchmark. It is specifically **not** a CEML choice of macro-step size.

### 6.7 Code, data, reproduction and criticism status

The ANTS paper links a Würzburg research-supplement page; the ANTS paper index labels the artifact “code”. A linked archive named collatz_2026.tar.gz was located.

This R1 environment did not unpack and source-audit that archive. Consequently R2 must establish:

- archive hash and contents;
- exact license;
- whether both Magma and optimized C/GMP code are included;
- compiler/build requirements;
- exact data files for the 10-billion- and 20-billion-digit runs;
- whether exact starting integers, step totals and result digests survive;
- test coverage and any independent implementation agreement.

No formal independent reproduction of the 20-billion-digit run, formal third-party code audit, or published correctness critique was found in this R1 search. That negative finding is an **open evidence gap**, not a correctness endorsement.

## 7. Other algorithm families relevant to isolated extreme starts

### 7.1 Direct arbitrary-precision stepping

Idea: apply C or T one step at a time using an arbitrary-precision integer.

Correctness basis: direct definition; easiest reference oracle.

Resource implication: for a typical convergent trajectory whose step count scales with bit length, each step touches a large integer, leading empirically/conditionally to quadratic-scale bit work.

Maturity: trivial to implement with GMP/rug/Python big integers; useful as a validation oracle on bounded inputs, not attractive as the sole extreme-scale engine.

R2 relevance: retain as an independent reference path, not as the presumptive production hot loop.

### 7.2 Odd-only valuation stepping

Idea: for odd n, compute v2(3n+1) and replace n by (3n+1)/2^v2(3n+1).

Correctness basis: exact grouping of one odd operation plus its following run of divisions by two.

Resource implication: reduces control-loop iterations but does not by itself remove repeated full-size arithmetic. It also complicates exact conventional step accounting if valuations are not accumulated.

Maturity: standard and simple; a useful intermediate oracle/implementation family.

### 7.3 Table-driven affine / composite-polynomial batching

Idea: low m bits determine the next m parity decisions; precompute a small affine transform per low-bit residue and apply one transform per block.

Primary basis: Leavens and Vermeulen 1992; Elsenhans explicitly reuses the standard-polynomial formulation.

Resource implication: large tables grow exponentially with m, so practical fixed tables use modest m. They can reduce branches and repeated shifts but do not alone solve the cost of very long extreme trajectories.

Maturity: old, well-understood technique; suitable as a component and as a correctness bridge.

### 7.4 On-demand affine batching by binary splitting

Idea: compute the exact k-step affine map for only the current residue class, recursively composing sub-blocks rather than tabulating all 2^k residues.

Primary basis: Elsenhans 2026.

Resource implication: trades many full-size elementary updates for subquadratic multiplication of large affine coefficients and the current state. This is the key asymptotic improvement identified in R1.

Maturity: peer/conference-reviewed mathematical description plus author code; independent production-grade audit remains open.

### 7.5 Hierarchical / super-batching

Idea: form a much longer affine pair, often denoted (a_J,C_J), by recursively composing exact low-bit blocks, then apply one large multiplication/add/shift to the current state.

Public example: DRMacIver/collatz-eval calls this its GMP “super-batch” engine and states that it is based on Elsenhans.

Resource implication: performance becomes tightly coupled to the big-integer multiplication backend, allocation strategy, and block construction. Memory and multiplication thresholds become important, but those are later machine-specific engineering questions.

Maturity: active public implementation with explicit test/oracle scaffolding; README self-disclaims substantial human auditing.

### 7.6 Bit-array / file-backed explicit dynamics

Idea: represent the integer or trajectory logic as bits/files rather than relying on a conventional in-memory big integer.

Primary examples: Ren 2018/2019 and the later 2023 work.

Resource implication: can remove a single fixed machine-word bound and can operate at million-bit scale, but the demonstrated runtimes are far behind affine binary-splitting methods at modern extreme sizes.

Maturity: published C/data artifacts exist; scientifically useful as an independent algorithmic lineage and step-convention check rather than a leading CEML candidate.

### 7.7 Gerbicz/Boutoukoat recursive GMP method

The Boutoukoat repository attributes its main speed idea to an R. Gerbicz MersenneForum post and describes a change from textbook roughly quadratic behavior to approximately O(log(n)^1.1), with further gains from reducing GMP overhead and temporary allocations.

CEML did not independently reconstruct or verify the cited asymptotic argument from a primary formal source in R1. The repository nevertheless demonstrates fast public exact-start computations and independent output agreement for some Mersenne inputs.

R2 must treat the complexity description as a repository/author claim until the underlying recurrence and correctness argument are reconstructed source-first.

## 8. Existing implementations

| Project | Language / arithmetic | Method | Public source / license / inspected version | Visible validation strategy | Audit/reproduction status | Important limitations |
|---|---|---|---|---|---|---|
| Elsenhans ANTS implementation | Magma; optimized C with GMP also reported | Standard-polynomial affine macro steps; recursive binary splitting | Public research-supplement archive linked from paper; license not established in R1 | Paper gives mathematical identities and experiments | Conference-reviewed method; no independent 20B reproduction found; archive not source-audited by CEML | Exact giant input provenance and build/library versions incomplete in paper |
| DRMacIver/collatz-eval | Rust 2024 edition; default custom limb code; optional rug/GMP and optional FLINT | Dense/Sparse batched stepping; GMP super-batch; binary-split affine maps | GitHub; MIT; v0.1.0; inspected main commit 0f5ad6d (2026-08-08) | Optional rug oracle; property-based dev dependency; audit profile with overflow checks; tests include exact arithmetic/cross-check paths according to manifest/README | No formal external audit found; README explicitly says very little human auditing | “1GB in minutes” is expressly not backed by precise benchmarks; FLINT/system integration needs audit |
| Boutoukoat/Collatz-steps-on-large-numbers | C++ with GMP, flex/bison expression parser | Gerbicz-derived recursive acceleration plus low-level GMP optimizations | GitHub; MIT; inspected main commit ec82c0a (2025-04-29) | Known-value examples including Mersenne starts; external rerun agreement for several values | Independent public output rerun and OEIS agreement; no formal code audit found | Benchmark hardware/build context incomplete; architecture-specific code; GMP internal/size limits noted; prior compile portability issue |
| Wei Ren txpo15/data code | ANSI C; bit/file representation | Explicit shortcut I/O sequence, bit manipulation/file-backed representation | Code/data in 2019 Data supplementary material; dataset CC-BY | Published output tables and public source/data | Peer-reviewed data paper but no independent extreme-run audit found | Much slower scaling than affine batching; terminology differs; “no upper bound” is representational, not resource-unbounded |
| Bařina collatz | C/C++/OpenCL and fixed-width optimized kernels | Contiguous interval verification with residue/sieving optimizations and distributed work units | GitHub xbarin02/collatz; MIT repository; paper cites commit 53c2a06; current repo active through at least 2026-09-28 | Large distributed verification campaign, published methodology | Strong peer-reviewed evidence for contiguous bound | Workload and integer-width assumptions are not CEML's isolated extreme-start problem |

### 8.1 collatz-eval details relevant to R2

The inspected Cargo manifest reports:

- package version 0.1.0;
- Rust edition 2024 and rust-version 1.91;
- MIT license;
- optional rug 1.30;
- optional gmp-mpfr-sys 1.7;
- optional hegeltest 0.29.3 for property-based tests;
- release profile opt-level 3, thin LTO, one codegen unit;
- a separate audit profile retaining debug assertions and overflow checks.

The README states that the default path has no runtime dependencies, that the gmp feature uses a super-batch engine, and that the flint feature can route sufficiently large products through FLINT's low-level multiplication. It also explicitly warns that the repository was developed by Claude Fable with human input but very little human auditing and “likely has many flaws”.

That warning is material. CEML must not call this implementation “audited”.

### 8.2 Boutoukoat portability evidence

Issue #1 documents build failures with GMP 6.2.1 on Ubuntu 22.04 and Raspberry PiOS, involving mpz_mullo availability, static library paths and ARM-specific helper code. The reporter later closed the issue after modifying libgmp.a paths and reported that the program worked on both systems.

This is evidence that build reproducibility cannot be inferred from “uses GMP”. It is not evidence that computed trajectories were wrong.

## 9. Huge isolated-start evidence table

This table is intentionally not a leaderboard.

| Start / class | Starting magnitude | Reported result | Method / source | Reproducibility and evidence |
|---|---:|---|---|---|
| Random number, exact value not in paper body | 20,000,000,000 decimal digits | Reached 1; paper does not give step total for this run; ~28 h, ~70 GB | Elsenhans Magma standard-polynomial/binary-splitting method, E01 | Strong primary author claim; exact start and run digest not established from paper body; no independent reproduction found |
| One random number in timing table | 10,000,000,000 decimal digits | 160,079,821,246 shortcut steps; 13.2 h | Elsenhans Magma, one i7-12700 core @ 4.7 GHz, E01 | Primary paper; exact start not printed in table; public supplement may improve provenance; not independently reproduced here |
| 2^33219280950-1 | 10,000,000,001 decimal digits | Community claim: 286,935,064,604 steps, under 23 h | Claimed C/GMP translation of Elsenhans, E15 | Exact formula-defined start but weak community-only evidence; no inspected code/build/result artifact; low confidence |
| 2^345678877-1 | 104,059,711 decimal digits | 4,651,594,256 standard steps; README timing 240,021.755 ms | Boutoukoat C++/GMP, E10 | Public source and exact start; benchmark conditions incomplete; no independent matching output located in R1 for this exact exponent |
| 2^136279841-1 | 41,024,320 decimal digits | 1,833,585,702 standard steps | Hermann-SW rerun plus OEIS A181777, E12/E13 | Independent/public agreement stronger than a single author report; not a formal audit |
| 2^82589933-1 | 24,862,048 decimal digits | 1,111,148,968 standard steps | Boutoukoat README; Hermann-SW rerun; OEIS A181777, E10/E12/E13 | Exact start with multiple public matching outputs; good cross-check point for R2/V1 |
| Random odd start, exact value not captured in this audit | 6,000,000 bits ≈ 1,806,180 decimal digits | 28,911,397 shortcut-style operations; 8d1h40m44s | Ren 2023 ePrint, E08 | Detailed laptop/compiler context; author report; no independent reproduction found |
| 2^100000-1 | 100,000 bits = 30,103 decimal digits | 481,603 odd 3x+1 ops + 863,323 divisions; equivalently 863,323 shortcut steps and 1,344,926 standard steps | Ren 2018 IEEE + 2019 Data, E06/E07 | Exact start, published code/data and internally consistent convention conversion; useful validation fixture |

## 10. Performance evidence

Performance evidence must retain its provenance class.

### 10.1 Author-reported benchmarks

- **Elsenhans Magma timing table:** one Intel i7-12700 core at 4.7 GHz; input sizes and counts listed in Section 6.6. OS, Magma version, RAM except the largest run, compiler and library versions are not specified in the paper.
- **Elsenhans optimized C/GMP ratios:** ~7.5× faster than Magma at 1M decimal digits and ~3.5× at 1B digits. Compiler, GMP version and flags are not specified.
- **Elsenhans 20B-digit run:** Magma, ~28 h, ~70 GB; processor context appears to be the same experimental environment but the sentence itself chiefly establishes time/memory, not a complete build manifest.
- **Ren 6M-bit run:** Lenovo ThinkPad X1 Carbon, Intel i7-10510U, 8 GB RAM, x86/64-bit Windows 10, MinGW Developer Studio 2.05 using GNU GCC, ANSI C; 8d1h40m44s.
- **Boutoukoat README timings:** exact input/output pairs are useful, but hardware, compiler version, flags and GMP version for the published timing list are not supplied.

### 10.2 Independently reproduced measurements

Hermann-SW reran Boutoukoat's code and published timings/output for the Mersenne-prime sequence. Those are independent from the repository README, but the artifact does not provide a complete reproducibility manifest. CEML therefore uses it primarily as output agreement, not as a transferable speed benchmark.

No independent benchmark of the Elsenhans 10B/20B experiments was found.

### 10.3 Theoretical estimates

Elsenhans's O_c(B log^2 B log log B) full-run bound applies only on G_c, the set of starts known to reach 1 within c times their bit length in shortcut steps. It is not an unconditional worst-case bound.

Leavens/Vermeulen's older composite-polynomial work establishes the exact batching idea but its fixed-width search speedups are not predictive for billion-digit arbitrary-precision multiplication.

### 10.4 CEML inferences

CEML may infer from the evidence that large-integer multiplication quality, allocation/copy behavior and affine block construction are likely performance-critical for an Elsenhans-style engine.

CEML **does not** infer:

- the eventual CEML runtime at any ladder rung;
- the best arithmetic backend on the future machine;
- the correct macro/super-block size;
- a suitable thread count;
- a RAM ceiling;
- a checkpoint cadence;
- the benefit of FLINT versus GMP on the future machine.

Those require R2 reasoning and later C1 measurement.

## 11. Correctness and audit caveats

### 11.1 Overflow and arithmetic width

Fixed-width Collatz implementations can overflow in 3n+1 or intermediate batched coefficients unless they prove sufficient headroom. Extreme CEML starts require exact arbitrary-precision state and exact coefficient arithmetic. A contiguous verifier engineered around 128-bit state is not automatically reusable.

### 11.2 Convention conversion errors

A result can differ by millions or billions of “steps” while both programs are correct if one counts standard C steps and another counts shortcut T steps. Every comparison must identify:

- the map;
- the endpoint;
- whether an odd 3n+1 and its mandatory first division count as one or two;
- whether odd-only valuation steps have been expanded.

### 11.3 Affine-composition errors

Exact batching introduces specific proof obligations:

- low-bit residue must match the block length;
- affine coefficients must compose in the correct order;
- right-shift denominator must be exact;
- intermediate coefficient arithmetic must not overflow;
- splitting at odd block lengths must preserve all steps;
- table entries and recursive base cases must agree;
- the terminal block must not silently pass the first occurrence of 1.

These are R2 audit targets even when the mathematics is correct on paper.

### 11.4 Parity / valuation boundary errors

Odd-only methods must account for v2(3n+1) exactly. Off-by-one valuation errors change both state and step totals. Fast low-level implementations that inspect machine limbs must correctly handle runs of zero limbs and cross-limb carries.

### 11.5 Serialization and restart

None of the extreme isolated-start sources inspected in R1 supplied a CEML-grade, documented crash-safe checkpoint/restart protocol with state hashes, step-count semantics and recovery validation.

This is a **missing feature/evidence class**, not a discovered bug. CEML must design and validate checkpoint semantics later rather than assume that a fast trajectory kernel is restart-safe.

### 11.6 Public code is not audited code

- Elsenhans: reviewed mathematical paper and linked code/data do not constitute an independent code audit.
- collatz-eval: README explicitly disclaims substantial human auditing.
- Boutoukoat: public outputs and independent reruns do not establish source-level correctness.
- Ren: publication and supplementary code do not establish independent extreme-run reproduction.

### 11.7 Performance claims can be unreproducible even when outputs are right

Missing compiler flags, library versions, thermal/power state, OS, allocation settings or exact input generation can make speed claims non-reproducible without undermining the underlying mathematics. R1 therefore separates output agreement from benchmark reproduction.

### 11.8 “Largest verified” claims age badly

Ren's 2018/2019 “largest” claim was historically framed against the then-visible literature and was later exceeded. Community threads contain newer claims without durable artifacts. CEML will report demonstrated scale and evidence quality, not maintain an informal record title.

## 12. Established facts versus weak or unsupported claims

### 12.1 Established strongly enough to carry into R2

**OBSERVATION:** The shortcut-map low k bits uniquely determine an exact k-step affine map; this is supported by the classical composite-polynomial literature and Elsenhans's formal presentation.

**OBSERVATION:** Recursive binary splitting can construct the current residue's affine macro-transform without tabulating all 2^k residues.

**OBSERVATION:** Elsenhans reports exact reach-1 computations at 10B decimal digits in the main table and a largest 20B-decimal-digit Magma computation, with stated hardware for the table and stated time/memory for the largest run.

**OBSERVATION:** Public, actively maintained implementations now exist outside the Elsenhans artifact, including a Rust/GMP/optional-FLINT implementation explicitly based on his affine super-batching and a C++/GMP implementation in the Gerbicz lineage.

**OBSERVATION:** Public independent output agreement exists for large formula-defined Mersenne starts, including 2^82589933-1.

**OBSERVATION:** Contiguous verification above 2^71 is a different computational problem and cannot be used as evidence that an isolated billion-digit engine is correct or fast.

### 12.2 Claims that remain bounded/weak

**OPEN:** The exact start, step total, output digest and independent reproduction for Elsenhans's 20B-digit run are not established by the paper body or this audit.

**OPEN:** The exact contents, license, test corpus and build instructions of the Elsenhans collatz_2026.tar.gz archive were not source-audited in R1.

**OPEN:** The Gerbicz asymptotic description quoted by Boutoukoat was not reconstructed from a formal primary source.

**OPEN:** collatz-eval's “up to 1GB in minutes” statement is explicitly not backed by precise benchmarks and must not be treated as a measured performance result.

**OPEN:** The Reddit 10B-digit Mersenne run is a weak community claim lacking the provenance required for a CEML evidence record.

**OPEN:** No external implementation surveyed here has demonstrated CEML-grade checkpoint integrity and restart semantics.

## 13. Unresolved questions for CEML-R2

R2 must answer these before any architecture family can be called viable:

1. Can the Elsenhans Magma and C/GMP archive be obtained, hashed, unpacked and mapped line-by-line to the ANTS formulas?
2. Does the archive preserve exact starts/results for the 10B and 20B runs, and if so what identifiers/hashes can CEML record?
3. What exact invariant should represent an affine block: map convention, coefficient normalization, denominator/shift, block length and step count?
4. How should the implementation prove that a macro step uses only parity information justified by the current low bits?
5. How should the final macro block be shortened so that reaching 1 is counted at its first occurrence?
6. Can collatz-eval's Dense, Sparse and super-batch paths be shown equivalent on a broad deterministic test corpus, including adversarial carry/zero-limb cases?
7. What parts of collatz-eval are genuinely independent of Elsenhans versus a transcription of the same recurrence, and therefore what constitutes an independent oracle?
8. What exact recurrence underlies the Gerbicz/Boutoukoat method, and is its claimed approximate exponent supported mathematically or only empirically?
9. Can Boutoukoat outputs for large Mersenne starts be reproduced with a fully recorded toolchain and cross-checked against an independent standard/shortcut implementation?
10. Which architecture families permit checkpoint boundaries that preserve exact state, exact step count and integrity without changing scientific semantics?
11. What library/toolchain licenses and ABI constraints would affect a later CEML implementation?
12. Which comparisons can be benchmarked later on the local machine without prematurely fixing block sizes, backends or compiler flags?

## 14. Implications for CEML-R2

R1 does not choose an implementation. It narrows R2 to a defensible set of families and proof obligations.

R2 should give highest scrutiny to:

- Elsenhans standard-polynomial / affine binary splitting as the primary current high-magnitude method;
- direct and odd-only exact stepping as independent reference oracles;
- collatz-eval as a current Rust implementation of super-batching, with its self-declared audit limitations;
- Boutoukoat/Gerbicz as a separate fast C++/GMP lineage with useful exact-start cross-checks;
- GMP and optional FLINT only as candidate exact arithmetic backends, not predetermined winners;
- explicit conversion among standard, shortcut and odd-only step counts;
- terminal-block correctness;
- state/checkpoint boundaries and independent validation strategy.

R2 must remain implementation-audit research. It may create small deterministic fixtures or bounded reference calculations allowed by the research protocol, but it must not implement the production engine, run a scientific rung, generate the scientific seed, freeze the ladder, or select machine-specific parameters.

## 15. R1 exit checklist

- [x] **Search strategy recorded.** Primary-first hierarchy and negative-search discipline are documented above.
- [x] **Primary sources preferred where available.** Elsenhans ANTS/arXiv, Leavens/Vermeulen, Ren/IEEE/MDPI/ePrint and Bařina/Springer are cited directly.
- [x] **Elsenhans-related claims traced to primary material.** Mathematical method, code sketch, complexity qualification, benchmark table, memory statement and public supplement locator were inspected.
- [x] **Public implementations catalogued.** Elsenhans artifacts, collatz-eval, Boutoukoat, Ren code/data and Bařina comparator are recorded with language/backend/status where available.
- [x] **At least one attempt made to find independent reproduction or criticism for important claims.** Independent Mersenne reruns and OEIS agreement were found; build issue evidence was inspected; no independent 20B reproduction or formal Elsenhans code audit was found and that absence is recorded.
- [x] **Performance claims include hardware/software context.** Available CPU/RAM/compiler/library/input details are preserved and missing fields are explicitly marked.
- [x] **Uncertainties and inaccessible evidence recorded.** The uninspected compressed Elsenhans archive, weak community claims, incomplete benchmark manifests, Gerbicz primary-source gap and missing checkpoint evidence are explicit.
- [x] **Implications for R2 stated.** Section 14 defines the research shortlist and proof obligations without choosing machine-specific engineering parameters.

## 16. R1 decision

**CEML-R1 PASS.**

R1 has established enough sourced state-of-the-art evidence to begin CEML-R2.

This decision means only that the literature/evidence gate is complete. It does not certify an external implementation, authorize production code, authorize scientific execution, generate a scientific seed, freeze a magnitude ladder, or select local hardware parameters.
