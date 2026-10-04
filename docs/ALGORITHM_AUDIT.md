# CEML Algorithm and Implementation Audit

Status: **COMPLETE — CEML-R2 PASS**

Decision date: **2026-10-04**  
Research stage completed: **R2 — algorithm and implementation audit**  
Authoritative input baseline: **3638469ac641c78bb78767920a6bd6f322fd3acc**  
Scientific execution: **NOT AUTHORIZED**  
Production implementation: **NOT AUTHORIZED**

## 1. Scope and decision

CEML-R2 audits exact algorithm families and public implementations that could inform a later CEML engine. It does not select local tuning parameters, implement the production engine, generate a scientific seed, freeze the magnitude ladder, or execute a scientific rung.

The R2 exit condition is met. The audit establishes:

- normalized map and step-count semantics;
- an explicit mathematical invariant for affine batching and its composition order;
- source-level audits of the strongest public implementation lineages identified in R1;
- a machine-neutral viable architecture shortlist;
- a correctness threat model tied to R3/V1 detection methods;
- validation-oracle requirements and checkpoint implications;
- exact questions that C1 must benchmark locally.

Two external evidence gaps remain deliberately open: the Elsenhans collatz_2026.tar.gz archive could not be acquired as inspectable bytes in this audit environment, and the cited R. Gerbicz forum post could not be retrieved directly. The R2 instructions explicitly permit preserving an inaccessible artifact as an evidence gap. Neither gap prevents identification of the mathematical invariants, correctness risks, or viable architecture families required by the R2 gate. They do prevent CEML from claiming that either external artifact has been independently audited.

**R2 decision: PASS.** R3 may begin, but no implementation, local tuning, seed generation, ladder freeze, or scientific execution is authorized by this decision.

## 2. Methodology and evidence discipline

The audit began from the R1-PASS main-branch baseline and treated this repository as CEML's sole authoritative state. R1 evidence was inherited only with its recorded confidence and caveats.

Primary or source-level evidence used in R2 included:

| ID | Evidence | Pin / date | Role | R2 confidence |
|---|---|---|---|---|
| A01 | Andreas-Stephan Elsenhans, Numerical Verification of the Collatz Conjecture, ANTS XVII 2026, https://antsmath.org/ANTSXVII/papers/antsxvii-elsenhans-paper.pdf | ANTS XVII 2026 paper | Primary mathematics, pseudocode, conditional complexity and author-reported performance | HIGH for stated mathematics; performance remains author-reported |
| A02 | Institutional archive URL, https://www.mathematik.uni-wuerzburg.de/fileadmin/10040131/Magma-Skripte/collatz_2026.tar.gz | attempted 2026-10-04 | Intended author artifact | OPEN: bytes not acquired, no hash/inventory/license audit |
| A03 | DRMacIver/collatz-eval, https://github.com/DRMacIver/collatz-eval | 0f5ad6da40171cdcd68ce167776a0644ceb942dc | Rust Dense/Sparse, affine blocks, GMP super-batching, optional FLINT, tests/audits | HIGH for source observations; not a correctness certification |
| A04 | Boutoukoat/Collatz-steps-on-large-numbers, https://github.com/Boutoukoat/Collatz-steps-on-large-numbers | ec82c0a7e248add8f3f6d16b07cda0aae4e7ebfd | C++/GMP Gerbicz-attributed affine recursion and fixed-width tails | HIGH for source observations; primary Gerbicz provenance incomplete |
| A05 | Boutoukoat issue #1, https://github.com/Boutoukoat/Collatz-steps-on-large-numbers/issues/1 | 2024-10-22 | Historical mpz_mullo/build portability evidence | HIGH |
| A06 | Boutoukoat commit 5efda125e83540512a1d38490d226093f337c250 | 2024-10-22 | Removal of faster half-multiplication / portability attempt | HIGH |
| A07 | Wei Ren, Collatz Computation Sequence for Sufficient Large Integers is Random, https://eprint.iacr.org/2023/648 | 2023 revision | Independent shortcut-map bit/logical representation lineage and count convention | MEDIUM-HIGH; not a CEML correctness certification |
| A08 | Wei Ren et al., 2018 IEEE paper, DOI 10.1109/SmartWorld.2018.00099, and IEEE DataPort DOI 10.21227/FS3Z-VC10 | 2018, dataset updated later | Earlier C / bit-oriented implementation lineage and published source/data pointer | MEDIUM-HIGH |
| A09 | GMP official site/manual, https://gmplib.org/ | accessed 2026-10-04 | Exact arbitrary-precision backend properties and licensing | HIGH |
| A10 | FLINT official documentation, https://flintlib.org/doc/ | accessed 2026-10-04 | Backend/dependency/licensing context | HIGH |
| A11 | rug 1.30 documentation, https://docs.rs/rug/1.30.0/rug/ | 1.30.0 | Rust GMP wrapper/dependency/licensing context | HIGH |
| A12 | Gerbicz source linked by Boutoukoat, https://www.mersenneforum.org/showpost.php?p=634604&postcount=4 | attempted 2026-10-04 | Claimed primary lineage | OPEN: direct content unavailable in audit environment |

Repository and source inspection is not called independent certification. Tests are evidence about implemented intent and defect-detection surface; they are not a proof that an implementation is bug-free. Performance statements are classified separately in Section 11.

A bounded independent reference check was performed in R2 using direct Python standard-map stepping, not affine batching: 2^127-1 reached 1 in 1,660 standard steps, and 2^44497-1 reached 1 in 598,067 standard steps. These match Boutoukoat's published examples. For the same starts, the direct reference counted respectively 593 and 214,150 odd standard steps, giving 1,067 and 383,917 shortcut-map steps by the exact conversion below. This is a correctness fixture, not a performance benchmark and not a scientific CEML rung.

## 3. Normalized semantics

### 3.1 Standard map

For positive integer n, define the standard Collatz map C by

C(n) = n/2 when n is even, and C(n) = 3n+1 when n is odd.

The standard total stopping time is the least s at which C applied s times to the start equals 1. CEML must always say whether a reported count is this standard-map count.

### 3.2 Shortcut map

Define the shortcut map T by

T(n) = n/2 when n is even, and T(n) = (3n+1)/2 when n is odd.

One odd T step merges one odd C step and the compulsory following even C step.

If a shortcut trajectory to first 1 contains I odd shortcut steps and E even shortcut steps, then

- shortcut steps = I + E;
- standard steps = 2I + E;
- therefore standard steps = shortcut steps + I.

This identity is the safest implementation conversion because I can be accumulated exactly with the parity word. Inferring conventions from a published bare integer is prohibited.

### 3.3 Odd-only valuation map

For odd n, define the odd-only map U by

U(n) = (3n+1) / 2^q, where q = v2(3n+1).

One U step represents q shortcut-map T steps: one odd T step followed by q-1 even T steps. It represents q+1 standard-map C steps.

An odd-only implementation therefore must accumulate q, not merely the number of U applications, if it is to reproduce shortcut or standard total stopping counts.

### 3.4 Stopping terminology

Sources use "stopping time" inconsistently. CEML will not infer a convention from that phrase alone. Every reported metric must identify:

- map: C, T, or U;
- endpoint condition, especially first occurrence of 1;
- whether the count is total-to-1 or first-below-start;
- any conversion fields used.

R3 must freeze the published CEML metric names.

### 3.5 First occurrence of 1 and macro-block overshoot

The endpoint is the **first occurrence of 1**. This matters because T does not remain at 1: 1 maps to 2 and 2 maps back to 1. A macro block can therefore cross the first 1 and later end at 1 or 2 while reporting too many steps.

Elsenhans explicitly notes this terminal hazard. His paper states that 2^k reaches 1 within k elementary T steps and any other (k+1)-bit number takes longer; consequently a macro schedule must not take a final block longer than the guaranteed pre-first-1 distance. His demonstrated schedule uses about half the current log2 value and is terminal-safe under that argument.

CEML invariant: a total-stopping implementation may use a macro block only when it proves that the block cannot pass the first 1, or it must shorten/decompose the terminal block and determine the first hit exactly. Merely checking n == 1 after a macro block is insufficient.

### 3.6 Minimal logical state

Without yet freezing the R3 manifest, any exact engine or checkpoint must make it possible to reconstruct at least:

- current positive integer n;
- start identity/provenance;
- shortcut step count;
- odd shortcut-step count, or an exactly equivalent field;
- derived standard count or enough state to derive it;
- map/convention version;
- algorithm/build identity;
- enough validation/checkpoint metadata to detect restart drift.

Caches, tables, multiplication plans and tuning state should be reproducible from canonical state or separately versioned; they must not silently change the mathematical trajectory.

## 4. Elsenhans mathematical audit

### 4.1 Affine standard-polynomial invariant

For a fixed k and residue r modulo 2^k, the first k shortcut parities are determined by r. There is an affine rational map

T^k(n) = (A n + B) / 2^k

for every n congruent to r modulo 2^k. A is a power of 3.

A convenient implementation state is (k, i, A, B), where i is the number of odd T steps and A = 3^i. The invariant is

2^k T^k(n) = 3^i n + B.

Starting from k=0, i=0, A=1, B=0, appending parity w in {0,1} gives

- if w=0: A is unchanged and B is unchanged;
- if w=1 at step t: A is multiplied by 3 and B becomes 3B + 2^t.

Equivalently B follows B_(t+1) = 3^w B_t + w 2^t.

**Failure surface:** wrong parity word, overflow in A/B, wrong step index in 2^t, or applying the denominator before the numerator is known divisible.

### 4.2 Why the low k bits suffice

Parity at step 0 depends on n modulo 2. After t exact shortcut steps, determining the next parity requires the numerator modulo 2^(t+1). Inductively, n modulo 2^k determines all k parities and therefore the entire affine block.

This is stronger than a heuristic locality claim: for a correct block, no high bit above position k-1 is needed to select the k-step transform.

**Implementation invariant:** low-bit extraction must return exactly n modulo 2^k in the logical value representation, even when the physical representation has shifted origins, chunk gaps, or unnormalised limbs.

### 4.3 Composition identity and order

Let P1 represent k1 steps and P2 represent the following k2 steps:

P1(x) = (A1 x + B1)/2^k1  
P2(x) = (A2 x + B2)/2^k2.

The combined block is P2 composed after P1:

A = A2 A1  
B = A2 B1 + B2 2^k1  
k = k1 + k2.

Composition order is not commutative. A common transcription error is to multiply the wrong B by the later power of three or shift the wrong additive term.

**R3/V1 fixture:** compare P2(P1(x)) with the composed block and with k1+k2 direct T steps, especially where both halves contain odd steps.

### 4.4 Direct base blocks

Elsenhans constructs a block directly by iterating on the residue and composing the elementary transforms. The paper precomputes widths 1 through 8 for its Magma pseudocode.

CEML does not inherit width 8 as a production choice. The correctness requirement is only that any base table be generated from a transparent exact definition and exhaustively cross-checked against direct stepping over every table entry.

### 4.5 Recursive binary splitting

For k = k1+k2, Elsenhans takes k1 = floor(k/2) and k2 = k-k1. It computes the first block from the low k1 bits, computes the intermediate residue T^k1(r) modulo 2^k2, recursively computes the second block, then returns P2 composed after P1.

Odd k is therefore normal: the two halves differ by one. No implementation may assume equal halves.

**Critical invariants:**

1. first residue is r modulo 2^k1;
2. the splice value is exact before reduction modulo 2^k2;
3. right-recursion input is the post-left value, not the original high bits;
4. composition order is P2 after P1;
5. k1+k2 equals the requested block length exactly.

### 4.6 Coefficient and shift bounds

For k shortcut steps, 0 <= i <= k, so A = 3^i <= 3^k. The all-odd recurrence gives B = 3^k-2^k, and in general B is also bounded by O(3^k). Thus A and B have O(k) bits while the denominator is exactly 2^k.

These bounds justify arbitrary-precision arithmetic for large blocks and support Elsenhans's multiplication-cost recurrence. They do **not** justify storing A or B in a fixed-width type merely because the current input residue fits such a type.

### 4.7 Macro-step selection and terminal safety

Elsenhans's demonstrated loop chooses approximately floor(log2(n)/2) elementary T steps per macro block. The paper's empirical macro-size sweep is performance evidence only; CEML imports no value of D or fraction.

Correctness constraints precede performance:

- selected k must be positive;
- low k bits must be available exactly;
- the affine numerator must be divisible by 2^k;
- the block must not pass the first 1 unless it is explicitly decomposed to locate that hit;
- step counters must increment by exactly k shortcut steps and by the exact number of odd parities when standard counts are required.

### 4.8 Divisibility canary

For a block selected from the correct residue, 3^i n+B is divisible by 2^k. Testing this before the shift is an excellent deterministic canary for many residue, composition, and carry errors.

It is not a full proof of correctness: some wrong transforms can still satisfy the same low-bit divisibility condition. R3 must pair it with genuinely diverse direct-state and modular/reference checks.

### 4.9 Conditional complexity theorem

Elsenhans defines B(n) as bit length and

G_c = { n : T^j(n)=1 for some j <= c B(n) }.

For n in G_c and fixed c, the paper proves:

- direct stepping is O_c(B(n)^2) bit operations;
- a k-step standard polynomial can be built in O(k log^2(k) log log(k)) bit operations under the stated multiplication bound;
- one macro step at the paper's scale costs O(B(n) log^2(B(n)) log log(B(n)));
- the full verification is O_c(B(n) log^2(B(n)) log log(B(n))).

This is a **conditional theorem for starts in G_c**, not an unconditional near-linear worst-case theorem for arbitrary Collatz trajectories. The empirical claim that observed random starts lie in small G_c sets must remain separate from the theorem.

## 5. Elsenhans artifact audit

The institutional collatz_2026.tar.gz URL was attempted directly on 2026-10-04. The web retrieval path identified the object as gzip content but did not expose downloadable bytes to the audit environment; a separate container retrieval attempt also failed. No mirror was substituted.

Therefore:

- cryptographic hash: **NOT OBTAINED**;
- archive inventory: **NOT OBTAINED**;
- Magma/C source mapping beyond the paper: **NOT AUDITED**;
- archive license: **UNKNOWN**;
- build/compiler/GMP requirements: **NOT AUDITED FROM ARTIFACT**;
- artifact assertions/tests: **NOT AUDITED**;
- exact giant-run starts/results/digests in archive: **UNKNOWN**;
- paper/artifact discrepancies: **NOT TESTABLE**.

The paper itself contains enough pseudocode to audit the mathematical recurrence, but CEML must not say that the author's implementation or giant-run artifacts have been source-audited.

Disposition: **OPEN EVIDENCE GAP, NON-BLOCKING FOR R2 ARCHITECTURE CLASSIFICATION.** Re-attempt acquisition in any later evidence refresh where direct byte access is available.

## 6. DRMacIver/collatz-eval source audit

Pinned revision: **0f5ad6da40171cdcd68ce167776a0644ceb942dc**.

License: repository MIT. The optional rug/GMP route introduces LGPL obligations from rug/GMP; optional FLINT adds FLINT's LGPL obligations. Exact distribution obligations must be reviewed when a CEML build is chosen.

The repository itself explicitly warns that it has had very little human auditing. R2 preserves that warning.

### 6.1 Small affine blocks and BlockTable

SmallBlock stores k, the odd-step count a, additive constant C and an LSB-first parity word. Its stated invariant is the same Elsenhans affine identity:

2^k T^k(n) = 3^a n + C.

The source has two useful construction surfaces:

- direct residue simulation;
- reconstruction from an emitted parity word.

Composition uses C = 3^a2 C1 + 2^k1 C2 in the correct order. A composed/table path can derive wider blocks from smaller ones.

Correctness strength: direct construction and parity-word reconstruction provide partially distinct implementations of the same mathematics. They are valuable differential checks, but not independent mathematical oracles.

### 6.2 Dense representation

Dense stores a limb vector plus a live-window base, logical length and fractional shift. Low bits are reconstructed across adjacent limbs when the logical value is shifted.

Application fuses multiplication by 3^a, addition of C at the current fractional origin, and exact right shift. The source asserts the required low-bit divisibility before advancing the live window. Larger small-block multipliers are split into smaller blocks rather than forcing a wider fixed multiplier.

Risk concentration:

- cross-limb low-bit extraction;
- carry propagation during multiply-add;
- base/frac bookkeeping;
- rebase/shrink operations;
- transient allocation during growth or shrink;
- correctness of split-block order.

The code contains tests comparing its specialized driver with the generic batch driver and uses divisibility canaries. These reduce risk but do not remove the need for R3 differential tests.

### 6.3 Sparse representation

Sparse represents separated non-zero limb chunks plus a logical fractional shift. It can exploit long zero gaps without densifying the whole span.

Block application multiplies each chunk, injects C at the logical low end, strips shifted low limbs and merges chunks when needed. The code documents and tests a proof that the C addition begins at the bottom chunk for a valid block, and checks that the lowest set bit after multiply/add lies at or above the required shift.

This representation has a larger invariant surface than Dense: chunk ordering, non-overlap, offsets, gap handling, merge correctness, low-bit reconstruction and carry bridges all matter. It is therefore a candidate optimization, not a default correctness oracle.

### 6.4 Super-batching

The superbatch module explicitly states that its polynomial recursion is the Elsenhans recurrence and claims no novelty for that recursion.

Poly stores k, a, 3^a and C. Recursive splitting:

- extracts n modulo 2^k;
- computes the left polynomial;
- computes the exact intermediate low residue by a splice;
- computes the right polynomial;
- composes in the correct order;
- applies one large exact multiply/add/shift to the current value.

Canaries test divisibility at splices and final application.

A value-threaded variant carries node values rather than C. This changes the arithmetic and fault surface, and can be checked modulo a prime, but it uses the same parity decomposition and affine identities. It is **not a mathematically independent oracle** for Elsenhans recurrence correctness.

### 6.5 GMP/rug path

With the gmp feature, rug::Integer supplies arbitrary-precision integer arithmetic via GMP. This avoids fixed-width overflow for the large coefficients and state, subject to memory/resource failure.

Rug 1.30 is LGPL v3-or-later and itself uses gmp-mpfr-sys. CEML must pin actual dependency versions and licenses at build freeze, not merely the top-level Rust crate.

### 6.6 Optional FLINT path

The flint feature can route multiplication to FLINT. The inspected source crosses an unsafe FFI boundary and calls the low-level _flint_mpn_mul symbol against GMP limb storage.

Correctness risks include:

- ABI/version drift;
- limb-layout assumptions;
- aliasing/output-capacity mistakes;
- a route not actually being exercised by tests;
- different multiplication cutovers changing only performance but accidentally changing code paths.

A historical repository commit explicitly fixed a vacuous FLINT test that had not reached the intended route. R3/V1 must therefore verify not only equality of results but also positive evidence that each feature-specific route was activated.

No FLINT threshold observed in this repository is transferable to CEML; C1 must measure locally if FLINT remains a candidate.

### 6.7 Terminal behavior and step-count API

The generic advance API advances an exact requested number of T steps and shortens its final block to that request. It is not itself a total-stopping-time routine.

Run::run_to_one uses super-batches while the value is above a configured bit threshold, then switches to direct one-step T iteration until n==1, counting each tail step. Under the default macro fraction the large phase is terminal-safe by the same type of bound used in the Elsenhans paper.

However, the public Run configuration exposes macro scheduling knobs, and the lower-level step API accepts an explicit super-batch length. CEML must not assume every arbitrary configuration is first-1 safe. R3 should require a scheduler invariant or explicit terminal decomposition independent of defaults.

The run returns shortcut-map T steps. Standard-map counts require the exact odd-step count conversion; that convention must not be inferred from the API name.

### 6.8 Audit paths and oracle independence

The strongest genuinely diverse in-tree reference is feature-gated direct GMP stepping: it applies one T step at a time. It does not use the affine binary-splitting recurrence and is therefore algorithmically independent of that recurrence, although it still shares the GMP arithmetic library.

Other checks are valuable but less independent:

- parity-word re-derivation shares the affine recurrence;
- modular residue audits share the emitted parity word and affine update law;
- valued recursion changes representation but shares the same split logic;
- Dense/Sparse agreement shares block generation.

A CEML validation plan should deliberately combine direct stepping in a separate implementation/language with affine checks, rather than counting several recurrence-derived paths as several independent oracles.

### 6.9 Tests and correctness-relevant history

The pinned tree includes agreement, oracle, property, adversarial/fuzz, superbatch, valued, anchor, parallel multiplication, FLINT and golden-vector tests.

Two history observations are especially useful for threat modeling:

- a correctness-bound constant was later corrected by one ULP and regression-tested;
- a FLINT test was found to be vacuous because its threshold had not activated the FLINT route, and was strengthened.

These are positive signs of active testing, but also concrete evidence that apparently covered low-level paths can contain subtle gaps. There were no open GitHub issues or pull requests in the queried current state; absence of issues is not evidence of correctness.

### 6.10 Checkpoint caveat

RunConfig.checkpoint_every refers to modular audit checkpoints, not durable restartable state serialization. CEML must not equate this with its own checkpoint/restart requirement.

## 7. Boutoukoat / Gerbicz lineage source audit

Pinned revision: **ec82c0a7e248add8f3f6d16b07cda0aae4e7ebfd**. License: MIT.

### 7.1 Exact recurrence

The helper routines implement k shortcut steps as

n -> (cc n + d) / 2^k

with cc = 3^i for the number i of odd shortcut steps.

They recursively split k into k1=floor(k/2), k2=k-k1, derive the post-left residue, recurse on the right and compose

cc = cc1 cc2  
d = d1 cc2 + d2 2^k1.

This is algebraically the same affine composition family as Elsenhans, though the implementation lineage and engineering choices differ.

It is therefore an **independent implementation lineage but not an independent mathematical family**.

### 7.2 Standard-map step preservation

The helper return value is not merely k. Its one-step base case returns one count for an even shortcut step and two counts for an odd shortcut step. Recursive returns sum these counts. Thus each k-step shortcut block returns

standard count = k + number of odd shortcut steps.

The final small table for n<8 contains standard total stopping times. The public examples therefore report standard-map total stopping time.

R2 independently checked the published examples 2^127-1 -> 1,660 and 2^44497-1 -> 598,067 with direct Python standard-map stepping. Agreement supports the count interpretation and those fixtures; it is not a general audit certificate.

### 7.3 Tail handling

The main GMP loop chooses roughly half the current bit length as k. It later drops to 128-bit and then 64-bit implementations when internal thresholds deem that safe, finally using a tiny table.

The half-bit-length macro schedule is compatible with first-1 safety as a family, but the fixed-width transitions add overflow and architecture assumptions that must be independently tested.

### 7.4 mpz_mullo history

Historical revision 9c8e71b4b9bcce12c9ffa30eb60aa8f10fe1ea40 called mpz_mullo in the recursive GMP helper. GitHub issue #1 recorded compilation failures because that symbol was unavailable in the reporter's GMP 6.2.1 environment, together with ARM-specific build failures.

Commit 5efda125e83540512a1d38490d226093f337c250 is explicitly titled "Remove faster half-multiplication, portability attempt". The current pinned source uses public mpz_mul instead of mpz_mullo at that point.

CEML conclusion: the old truncated-multiplication path is historical evidence only and must not be treated as a currently portable API. If low-product multiplication is reconsidered later, it requires a documented public interface or a separately audited implementation.

### 7.5 GMP internals and architecture assumptions

The current source still reads GMP's mpz structure fields _mp_d and _mp_size in its 128-bit extraction helper. This is an internal-layout dependency rather than a portable public serialization/API boundary.

The code also contains architecture-specific x86-64 and AArch64 inline assembly or compiler builtins for multiplication, carry, shifts and bit scans, and the Makefile uses aggressive native compilation flags and static GMP linking.

These choices may be fast on suitable systems but increase:

- ABI sensitivity;
- compiler and architecture dependence;
- undefined-behavior review burden;
- reproducibility burden;
- portability failure modes.

They are not suitable as an unmodified correctness baseline for CEML.

### 7.6 Size and resource limits

The README acknowledges limits from local memory and GMP internal limits. Such statements are not CEML resource ceilings. C1 must measure local memory and failure behavior rather than importing them.

### 7.7 Gerbicz provenance

The repository attributes its speed-up to an R. Gerbicz MersenneForum post. The exact linked forum content could not be retrieved directly in this audit environment. Later public code by another author cites a Gerbicz forum post and displays a closely related split recurrence, but that is secondary evidence and was not substituted for the unavailable primary post.

Accordingly:

- the code recurrence itself is source-audited;
- the attribution is preserved;
- the original Gerbicz derivation and any complexity argument remain **not independently audited**;
- Boutoukoat's README phrase "approximately O(log(n)^1.1)" is **not promoted to a theorem**.

## 8. Other exact algorithm and representation families

| Family | Mathematical state and exact transform | Count preservation | Arithmetic / memory profile | Correctness basis | R2 disposition |
|---|---|---|---|---|---|
| Direct arbitrary-precision stepping | Current n; apply C or T one step at a time | Trivial if convention explicit | Repeated whole-number operations; no macro coefficients | Definition itself | **VIABLE reference/oracle and tail; not assumed production-fast** |
| Odd-only valuation stepping | Odd n and q=v2(3n+1); n <- (3n+1)/2^q | Accumulate q for T and q+1 for C | Efficient when valuation scan/shift cheap; still repeated big multiplies | Exact valuation identity | **VIABLE independent family for validation/reference; production role deferred** |
| Fixed/table-driven affine batching | Current n plus precomputed transform selected by low w bits | Track block k and odd count | Table grows exponentially with w; small w cheap | Exhaustive table generation and affine identity | **VIABLE leaves/tails; table width deferred to C1** |
| On-demand binary-split affine batching | Low-k residue plus (k,i,3^i,B) | Exact k and i | O(k)-bit coefficients; divide-and-conquer multiplication | Elsenhans recurrence | **VIABLE core family** |
| Hierarchical/super-batching | Large affine block built recursively, then one large apply | Exact k and i | Reduces repeated full-width state operations; substantial temporary allocation and multiplication | Same affine recurrence plus splice invariants | **VIABLE core family; schedule/size deferred** |
| Value-threaded affine recursion | Carry T^k(r) or node value instead of B while retaining 3^i | Exact k and i | Different multiplication/copy profile; can avoid explicit large B in parts | Algebraically equivalent affine recurrence | **VIABLE optimization hypothesis, not an independent oracle** |
| Sparse chunk representation | Same exact integer split into non-zero limb chunks/gaps | Representation-neutral | Can save work on sparse states, but adds merge/offset invariants | Exact chunk arithmetic + differential tests | **DEFERRED optimization; benchmark and validate** |
| Ren-style bit/logical/file representation | Explicit bit string/array/file, implements shortcut I/O operations by bit manipulation/logical operations | Naturally emits I/O sequence if implementation is exact | Avoids general big-int multiplication but tends toward per-step bit/IO work; file representation can trade RAM for I/O | Direct bit-level transform, distinct lineage | **Useful validation lineage; deferred as production architecture** |

### Ren-specific note

Ren's 2023 paper defines the same shortcut map T and explicitly counts I=(3x+1)/2 and O=x/2 operations to first 1. Earlier published material points to ANSI C implementations for very large bit strings and data artifacts.

This is useful because its transform surface differs substantially from affine binary splitting. However, published scale or randomness claims are not correctness proofs, and the bit/file approach does not inherit the near-linear conditional complexity result of Elsenhans. CEML should use it, where practical, as a convention and independent-lineage check rather than as a presumed production winner.

### Bařina contiguous verification

Bařina's contiguous verifier remains excluded from the architecture shortlist for CEML's isolated-start workload. Techniques may be informative at a low level, but the problem structure and amortisation target are different. A contiguous bound is not a replacement for one exact arbitrary-precision trajectory.

## 9. Arithmetic and implementation backend comparison

No backend is selected in R2.

| Option | Exactness / strengths | Correctness and ABI risks | License / dependency notes | Serialization implication | C1 question |
|---|---|---|---|---|---|
| GMP public mpz API | Mature exact arbitrary-precision integer arithmetic; fast large multiplication | OOM/resource handling is external to mathematical exactness; version/CPU code paths differ | GMP 6.x dual GNU LGPL v3 / GPL v2, later-version options per official manual | Use mpz_export/import or a CEML canonical byte format; never raw limb dumps as protocol | Baseline throughput, memory, allocation/copy behavior |
| GMP + FLINT | Exact integer multiplication can expose alternative algorithms/routing | Extra ABI/library version surface; internal symbols are especially risky | Current FLINT 3.x LGPL v3-or-later and requires GMP/MPFR versions per release | Canonical CEML format must remain backend-neutral | Does a supported FLINT route beat GMP for CEML operand shapes, and at what local cost? |
| C with GMP | Minimal wrapper overhead, direct public API access | Manual lifetime/error handling, buffer arithmetic and UB risks | Application license must be compatible with linked libraries | Straightforward if protocol code avoids internal limbs | Compare safety cost, build reproducibility and speed |
| C++ with GMP | RAII/wrappers possible; can share C performance characteristics | Native intrinsics/templates/UB and exception behavior need audit | Same backend obligations plus wrapper choice | Same canonical requirement | Compare implementation complexity and performance only after I1 |
| Rust + rug/GMP | Strong safe-language boundaries for ordinary state; ergonomic exact Integer | rug/gmp-mpfr-sys FFI remains unsafe underneath; direct limb/FLINT calls reintroduce alias/lifetime risk | rug 1.30 LGPL v3-or-later; GMP obligations remain | Serde-like convenience is not enough; CEML must define canonical integer bytes/version | Compare wrapper overhead, allocation patterns, FFI risk and reproducibility |
| Rust with custom limb engine | Potential for explicit invariants and safe interfaces | Very high implementation/audit burden; would recreate mature big-int work | License depends on chosen crates/code | Can define canonical format natively | **Deferred unless strong evidence justifies complexity** |
| Python bigint | Very simple direct oracle/orchestration; separate implementation lineage from GMP on normal CPython | Not suitable to assume extreme-scale memory/performance; interpreter/version behavior | Python/stdlib licensing; dependency-light | Excellent for fixture/result parsers and canonical-format reference | Use as reference/orchestration; benchmark only if relevant, not as presumed core |

### Public API rule

A correctness baseline should prefer documented public arithmetic interfaces. Private GMP structure fields, private FLINT mpn symbols, architecture-specific assembly and native-only assumptions can be investigated later, but every such optimization increases the validation matrix and must have a public-API comparison route.

## 10. Correctness threat model

| Threat | How it can fail | R3/V1 detection requirement |
|---|---|---|
| Fixed-width overflow | A, B, n*multiplier, carry or shift intermediate wraps silently | Checked/sanitized builds; boundary-value fixtures; differential arbitrary-precision reference; explicit proofs for every fixed-width fast path |
| Big-integer allocation failure | Process abort, partial checkpoint, lost state, or misleading "did not finish" | Fault/resource tests; crash-consistent checkpoint protocol; classify resource failure separately from trajectory result |
| Carry/borrow mistake | Limb multiply-add or chunk merge loses/duplicates carry | Limb-boundary adversarial values; compare public big-int route; modular residues plus exact direct state |
| Low-bit extraction | Shifted/chunked representation returns wrong n mod 2^k | Patterns crossing word boundaries and gaps; compare with canonical integer modulo 2^k |
| Parity/valuation boundary | Wrong odd/even bit or v2 around zero words | Powers of two, 2^m±1, long zero runs, alternating/all-one low words; direct map oracle |
| Affine composition order | P1 and P2 reversed or wrong B gets power/shift | Non-commuting split fixtures; direct k-step comparison; associative three-block tests |
| Denominator/shift error | Wrong k, off-by-one shift, premature truncation | Divisibility canary; exact numerator comparison; widths around limb boundaries |
| Incorrect base table | Precomputed entry has wrong parity word/A/B/count | Exhaustively regenerate every table entry from elementary T definition |
| Odd split length | k1/k2 lose or duplicate one step when k is odd | Dedicated 2m+1 widths; assert k1+k2=k; direct comparison |
| Final-block overshoot of 1 | Macro passes first 1 and later lands at 1/2 | Terminal-safe scheduler proof plus powers-of-two/near-terminal fixtures; force decomposition around first hit |
| Convention/count mismatch | T count reported as C count, U applications counted as steps | Track odd count/valuations; cross-check identities C=T+I and U conversions |
| Serialization mismatch | Endianness/sign/length/version changes n or counters | Canonical byte vectors; round-trip across implementations and architectures |
| Restart drift | Resume changes n, count, scheduler semantics or hidden cache state | Stop/resume equivalence at arbitrary safe boundaries; hash state and manifests; caches rebuild deterministically |
| FFI alias/lifetime error | Output overlaps input or borrowed limb pointer becomes invalid | Safe wrappers; ASan/UBSan/Miri where applicable; compare FFI and public routes; route activation assertions |
| Architecture-specific UB | Inline asm/builtins assume word size, shift behavior or instruction support | Multi-compiler/multi-target CI; sanitizers; portable baseline; no architecture path accepted solely by benchmark |
| Compiler-sensitive UB | Optimization changes result due signed overflow, aliasing, invalid shift, uninitialised data | O0/O2/O3 and multiple compiler differential runs; UBSan; warnings-as-errors for relevant classes |
| Wrong multiplication route | Optimized backend silently diverges or test never enters it | Instrument route selection; exact product vectors; feature-specific end-to-end differential tests |
| Modular-audit common-mode bug | Audit uses same parity/recurrence error as engine | Pair with direct independent oracle and separate implementation language/transform |
| Checkpoint corruption/partial write | Latest file exists but contains mixed/partial state | Transactional write, length/hash/version validation, previous-checkpoint retention policy to be frozen in R3 |
| Dependency/version drift | Rebuild changes arithmetic ABI or optimized route | Locked dependency/build manifest; reproducible build records; revalidation on material changes |

## 11. Validation implications for R3

R3 must design validation around **diversity of bug surface**, not the number of tests.

### 11.1 Oracle classes

At least these roles should exist:

1. **Definition oracle:** one-step direct C/T implementation in a separate, simple code path, preferably also a separate language/runtime for bounded fixtures.
2. **Affine differential:** for arbitrary bounded n and k, compare a k-step affine block with k direct T steps.
3. **Count oracle:** record shortcut count, odd count and standard count and verify standard = shortcut + odd.
4. **Odd-only differential:** compare U stepping with the direct T/C trajectory while expanding valuations into exact counts.
5. **Implementation-lineage cross-check:** compare at least one implementation that does not share CEML's batching code.
6. **Backend differential:** identical algorithm/state through public GMP and each optional multiplication/backend route.

Several residue audits derived from the same parity word do not satisfy item 1 or item 5 by themselves.

### 11.2 Required fixture classes

R3 should freeze a suite containing:

- exhaustive residues for small block widths;
- random bounded integers and random k;
- widths on both sides of machine-limb boundaries;
- all-even and all-odd parity prefixes where constructible;
- powers of two;
- 2^m-1 and 2^m+1 families;
- long low-zero runs and sparse high/low limbs;
- alternating low-bit patterns;
- deliberately odd split lengths;
- values whose block ends exactly at 1 and values where an overlong block would pass 1;
- selected exact large formula-defined starts.

The R2 bounded reference fixtures include:

| Start | Standard total steps | Odd standard steps | Shortcut T steps | Evidence |
|---|---:|---:|---:|---|
| 27 | 111 | derivable by direct reference | 70 | classical bounded fixture; collatz-eval also documents 70 T steps |
| 2^127-1 | 1,660 | 593 | 1,067 | direct Python R2 reference; standard total matches Boutoukoat |
| 2^44497-1 | 598,067 | 214,150 | 383,917 | direct Python R2 reference; standard total matches Boutoukoat |

R3 may add fixtures, but should preserve exact provenance and avoid treating an external published result as self-authenticating.

### 11.3 Fault injection

Validation should deliberately corrupt:

- one parity bit;
- A or B;
- one carry limb;
- one low-bit extraction;
- one serialized counter/value byte;
- one multiplication result;
- one checkpoint manifest field.

The point is to show that intended canaries and independent oracles actually fire, not merely that they exist in code.

## 12. Checkpoint and restart implications

No cadence is selected in R2.

A CEML checkpoint must be a **durable protocol artifact**, not merely an in-memory residue check.

R3 should freeze:

- canonical unsigned integer encoding independent of GMP/Rust/host limb layout;
- exact step-count fields and map convention;
- rung/start identity and provenance;
- protocol/algorithm/build versions;
- checkpoint sequence number and parent/previous identity as needed;
- content hash and manifest hash;
- atomic/crash-consistent write procedure;
- rules for validating a checkpoint before accepting it;
- rules for resuming and for proving resumed execution equals uninterrupted execution.

Engineering caches should be disposable. If restart correctness depends on an unrecorded table, anchor cache, allocator shape or thread schedule, the checkpoint protocol is underspecified.

A checkpoint must never conceal a macro block that has already passed first 1. Checkpoint boundaries should occur only at mathematically exact states with exact counts.

## 13. Performance evidence classification

| Claim | Classification | R2 treatment |
|---|---|---|
| Elsenhans standard-polynomial and conditional full-run complexity on n in G_c | **THEORETICAL, PRIMARY PAPER** | Accepted with its hypotheses; not generalized beyond G_c |
| Elsenhans 10-billion-decimal-digit run: about 13.2 h on one i7-12700 core at 4.7 GHz | **AUTHOR-REPORTED** | Evidence of demonstrated scale, not a CEML forecast |
| Elsenhans 20-billion-decimal-digit Magma run: about 28 h and 70 GB | **AUTHOR-REPORTED** | Evidence only; archive not independently inspected |
| Elsenhans C-vs-Magma and macro-size sweep | **AUTHOR-REPORTED BENCHMARK** | No parameter imported |
| collatz-eval measured thresholds/ratios in source comments/tests | **AUTHOR/REPOSITORY-REPORTED** | Useful hypotheses for C1 only |
| Boutoukoat README timings | **AUTHOR/REPOSITORY-REPORTED, HARDWARE INCOMPLETE** | Not usable as local performance evidence |
| R2 Python checks of 2^127-1 and 2^44497-1 counts | **CEML BOUNDED INDEPENDENT CORRECTNESS REPRODUCTION** | Correctness fixtures only; timings intentionally not recorded |
| Any prediction of which backend/threshold wins on the CEML machine | **NOT ESTABLISHED** | Deferred to C1 |

Performance never substitutes for invariant or oracle coverage.

## 14. Viable architecture shortlist

The shortlist is deliberately a set of families, not a winner.

### 14.1 Core exact-transform candidate

**On-demand binary-split affine batching / hierarchical super-batching** over an arbitrary-precision integer backend using documented public interfaces.

Why viable:

- exact mathematical invariant is explicit;
- low-k-bit dependence is proved;
- composition and coefficient bounds are understood;
- conditional complexity is supported by a primary theorem;
- multiple public implementations exhibit the same recurrence;
- it admits strong direct-step and modular canaries.

Required before production: R3 semantic freeze and oracle suite, R4 hardware specification, I1 implementation brief, C1 local benchmarks, V1 validation.

### 14.2 Reference and terminal candidate

**Direct arbitrary-precision T/C stepping**, with optional odd-only valuation stepping as a second direct family.

Why viable:

- simplest correspondence to definitions;
- essential for independent differential testing;
- robust tail/terminal handling;
- minimal transformation common-mode with affine batching.

It is not selected as the high-magnitude core.

### 14.3 Leaf/tail candidate

**Small fixed/table-driven affine blocks**, generated and exhaustively checked from the definition.

Why viable:

- compact, testable leaf for recursive batching;
- can reduce recursion overhead;
- exact count fields are simple.

Table width is a C1 benchmark variable, not an R2 decision.

### 14.4 Optimization candidates held for C1

- Dense versus sparse state representations;
- value-threaded versus explicit-C superbatch recursion;
- GMP versus supported GMP+FLINT multiplication;
- allocation/reuse strategies;
- auxiliary parallel multiplication/audit work.

All are **PROVISIONAL PERFORMANCE HYPOTHESES**, not frozen engineering choices.

## 15. Rejected or deferred approaches

| Approach | R2 disposition | Reason |
|---|---|---|
| Unmodified Boutoukoat code as CEML production baseline | **DEFERRED / NOT BASELINE** | useful lineage, but internal GMP layout access, native assembly/build assumptions and limited checkpoint/audit structure enlarge correctness surface |
| Historical mpz_mullo path | **REJECTED AS CURRENT BASELINE** | not present in current source; documented portability/build failure; no public portable contract established |
| Private/internal FLINT symbol as mandatory backend | **DEFERRED** | ABI risk and prior route-test gap; must compete with public GMP route locally |
| Ren bit/file engine as presumed production core | **DEFERRED** | useful independent transform lineage but no evidence it dominates affine batching at CEML scale; potentially high per-step/I/O cost |
| Pure fixed-width engine for giant state | **REJECTED** | cannot represent arbitrary CEML magnitude exactly without a big-int layer |
| Python as production giant engine | **DEFERRED / REFERENCE ONLY** | excellent independent oracle/orchestration, but no reason to assume acceptable extreme-scale performance/memory |
| Contiguous verifier architecture as CEML core | **REJECTED FOR WORKLOAD MISMATCH** | solves a different amortised problem |
| Any machine-specific threshold imported from external benchmarks | **REJECTED IN R2** | violates stage discipline; must be measured in C1 |

## 16. Exact benchmark questions for C1

C1 must answer these on the actual audited local machine, after I1 and without changing frozen scientific semantics:

1. What is the crossover between direct stepping, small affine blocks and large binary-split/super-batches for CEML-like operand sizes?
2. For each viable affine family, how does throughput vary over a sweep of macro/block sizes rather than one inherited value?
3. What are peak RSS, live big-int bytes and transient allocation peaks for each family?
4. How much time is spent in low-bit extraction, recursion, coefficient composition, the full-width apply, allocation/copy, audit and checkpoint serialization?
5. Does a supported FLINT route improve the relevant product shapes over GMP alone, and is the route actually active?
6. What is the cost/benefit of Dense versus Sparse or analogous representations across dense random-like and adversarial sparse states?
7. What allocation reuse, in-place operation and temporary-lifetime strategies reduce peak memory without weakening correctness?
8. If auxiliary parallelism is permitted by later stages, what wall-clock/core-hour tradeoff does it produce and is the result bit-identical?
9. What is the cost of each proposed canary/audit mode?
10. What is canonical checkpoint serialization/deserialization throughput and transient memory cost?
11. How does memory scale with current state size and macro size, including failure margin for simultaneous old/new buffers?
12. How stable are results and performance across the candidate compiler/build modes permitted by the eventual hardware profile?
13. What terminal handoff rule gives exact first-1 counting with negligible risk and acceptable cost?
14. Can each optimized route be forced and proven active in a bounded benchmark/validation case?

C1 must preserve raw conditions and reject any benchmark that silently changes the mathematical map, counting convention or audit level.

## 17. Unresolved questions handed forward

These are real open items, but none blocks the R2 architecture-family exit condition:

1. **Elsenhans artifact:** obtain, hash, inventory and source-audit collatz_2026.tar.gz if direct byte access becomes available.
2. **Gerbicz primary source:** retrieve/archive the cited forum post or another primary statement; until then, keep complexity/provenance claims limited to what current code proves.
3. **Scientific output schema:** R3 must decide which map/counts, trajectory maxima, hashes and first-1 semantics are mandatory published fields.
4. **Oracle independence:** R3 must freeze the minimum number and diversity of reference paths.
5. **Checkpoint protocol:** canonical encoding, hash algorithm, crash consistency and restart proof remain to be frozen scientifically.
6. **Dependency pinning:** exact GMP/FLINT/rug/compiler versions are later build/profile decisions.
7. **Resource-failure semantics:** R3/V1 must specify how OOM, disk exhaustion, signal/interrupt and corrupted checkpoint are classified without producing a scientific claim.
8. **Architecture optimization:** Dense/Sparse, value-threading, FLINT, parallelism and block sizes remain unselected until C1.
9. **Macro terminal rule:** R3 should state the implementation-independent first-1 safety requirement; I1 will later express it in code-level invariants.

## 18. R2 exit checklist

| Criterion | Result | Evidence |
|---|---|---|
| Semantics normalized across C/T/U and counts | **PASS** | Section 3 |
| First-1 macro overshoot handled explicitly | **PASS** | Sections 3.5, 4.7, 10 |
| Elsenhans affine mathematics reconstructed with invariants/failures | **PASS** | Section 4 |
| Elsenhans archive attempted and gap preserved without mirror substitution | **PASS WITH OPEN EVIDENCE GAP** | Section 5 |
| DRMacIver source audited beyond README | **PASS** | Section 6 |
| Independent versus shared validation surfaces distinguished | **PASS** | Sections 6.8, 11 |
| Boutoukoat/Gerbicz current source and mpz_mullo history audited | **PASS** | Section 7 |
| Standard-step accounting and tail handling audited | **PASS** | Sections 7.2-7.3 |
| Other exact algorithm families compared | **PASS** | Section 8 |
| GMP/FLINT/language/FFI/license/serialization implications recorded | **PASS** | Section 9 |
| Explicit correctness threat model produced | **PASS** | Section 10 |
| R3 validation inputs identified | **PASS** | Section 11 |
| Checkpoint/restart implications identified | **PASS** | Section 12 |
| Performance evidence classified | **PASS** | Section 13 |
| Viable machine-neutral shortlist justified without selecting a winner | **PASS** | Section 14 |
| Rejected/deferred approaches documented | **PASS** | Section 15 |
| Exact C1 benchmark questions specified without local values | **PASS** | Section 16 |
| Unresolved evidence/engineering questions preserved | **PASS** | Section 17 |
| Production code, seed, ladder freeze, giant/scientific run and local tuning avoided | **PASS** | Scope of R2 work |

## 19. R2 decision

**CEML-R2 PASS.**

R2 establishes a defensible mathematical and implementation basis for R3. It does **not** certify any public implementation, select the production language/backend, freeze macro sizes or thresholds, or authorize execution.

The next gate is **CEML-R3 — reproducibility and validation audit**. R3 must freeze the scientific semantics and reproducibility/validation contract before the programme can proceed to hardware-specific work.
