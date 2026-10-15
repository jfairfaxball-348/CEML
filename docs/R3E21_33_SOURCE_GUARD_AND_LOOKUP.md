# R3E21-33 — 128-bit guard counterexample, exact lookup and coalescence, source-obligation ledger

**15 October 2026 | RESEARCH ONLY | PARTIAL MATHEMATICAL ADVANCE | NO-GO to hardware benchmark | £0, zero science.**

## Entry and provenance

Main at entry a742a14668d3cf19836e6a16dc01c9e39ba173d9, tree 8cf1f77bb9d3f88a19bd09c720e096cb0f7f62f5, normal 2-parent merge of PR #61 (parents 9d8ade853f9777c492ed098495a3ab985b3de3c4 and 4192cb5be6106d49331430596000d929b05937a6). Open PRs [] at entry; Actions runs 0; commit statuses []/aggregate pending = **ABSENT, NOT PASS**; rulesets []; branch reported unprotected; detailed branch protection 403/UNKNOWN. Re-read AGENTS, ROADMAP, PROGRAM_STATUS, CLAIM_POLICY and R27–R32 reports. No production/frozen changes.

Primary pinned sources (source snapshot != compiled binary): Angeltveit vigleik0/collatz commit f3f09248c7ae7299b8443e112f565f309d97f161, Rust main.rs blob 4a33b870d27059feea28985e185b8c8c709eb313 and CUDA collatz_cudav7.cu blob a783f0f39ee776c725036caec9c93d15a1c8ca72; Bařina xbarin02/collatz commit 141e13aae243d509a01a43bec597f53a5b97a09f, worker.c blob c33a6a86f35a0900ea1df8b7b2dcd30863a9b8bc and kernel.cl blob 569e0d1a46433365c822bdf4fb27a61f188cd4b5. The 2026 Angeltveit preprint arXiv:2602.10466 remains v1 dated 11 February 2026 on the available arXiv record. Bařina homepage generated Thu 15 Oct 2026 12:53:31 CEST gives BOTH first incomplete and first unassigned as 2175982616 × 2^40: author-reported, NOT independently reproduced by CEML. Separately published n<2^71 (2025) is NOT equated with mutable operational site position.

Inherited B=2392518188130438742016 is EXTERNAL/NOT REPRODUCED; E=3000000000000000000000 EXCLUSIVE; 552501489 complete U=2^40 units and one 350507499520-start partial; conditional conservative candidate upper 326518028938128165 UNCHANGED; true survivor count UNKNOWN. All source-performance comparisons remain estimates, not measurements.

## Result A — exact pinned Rust search3 overflow-guard counterexample

Rust main.rs lines 327–339:
- low 16 bits index the table; lookup yields odd-step count s and positive shifted tail c;
- line 331 performs the u128 multiplication (number >> 16) * 3^s + c;
- ONLY afterwards line 336 checks if number >> 64 >= 2^56 (i.e. number >= 2^120), prints base and RETURNS a tally without certification.

Take source-like shifted intermediate state x=2^120−2^16 = **1329227995784915872903807060280279040**, a positive 120-bit value. At entry, x<2^120, so the cited guard predicate is FALSE. Its low 16 bits are all zero; the lookup contains (s,c)=(16,0), i.e. 16 consecutive genuine odd T steps for T-state x−1. The next exact state is

y=(2^104−1)·3^16 = **873091227416114037923609044825978906815**.

The exact result has 130 bits and exceeds 2^128−1. Hence the post-operation threshold is **NOT a sufficient arithmetic guard over arbitrary u128 states**. This is a literal counterexample to the source-level guard property; it DOES NOT establish reachability from an initial n<2^72, nor falsify a particular executed run or the Collatz conjecture. Search3 can also legitimately take the print-and-return path: absent a guaranteed captured, arbitrated original start, this is UNRESOLVED not proved descent. Debug checked-overflow vs release wrapping behaviour and compilation flags remain unknown.

**Required corrected obligation**, on EVERY block: with q=number>>16, s=lookup&31, c=lookup>>5, check q <= floor((2^128−1−c)/3^s) BEFORE native multiplication; failing this is an ordered UNRESOLVED(original_start,event) before mutation. Separately prove this bound holds on ALL actually reached states if insisting on unchanged source. Overflow safety cannot be inferred from a later cutoff.

## Result B — exact limited soundness theorems, distinct from full source equivalence

**Sixteen-step lookup semantics.** Let X=T^j(n)+1 and X=q·2^16+r with 0<=r<2^16. The first 16 parity steps of X are controlled by its low 16 bits. Writing s=s(r) genuine odd steps and c(r) the 16-step shifted result at r, the exact big-integer identity is X_after16=q·3^s+c. Proof by induction on low-bit parity using shifted transformations X→3X/2 when even and X→(X+1)/2 when odd. This proves source table arithmetic in a mathematical model (including the r=0 formal sentinel), not native u128 overflow freedom. Source-independent capped fixture checked all 65535 positive nonzero 16-bit residues and 48 lifted q,r pairs against literal exact shifted Collatz; r=0 source table has (16,0).

**search1→search2 index/bounds.** For any search1 state reaching sigfig=66, its non-pruned branch at line 217 necessarily satisfies 306·66<485·threepower, hence threepower>=42=THREEPOWEROFFSET. Parity count is <=66, hence valid magicnumbers index 0..7 whenever the <50 conditional chooses that array; THREEPOWERS[threepower] at search2 is also in range [0,71]. The exact initialbitarray allocation is 2^18+1 = **262145** 64-bit words. With index in [0,2^24), index/64<=2^18−1, +1 is in range; wrapping uses one padded word. At source defaults LASTBITS=6 only one 64-bit high-word a group is read. This settles this specific lower-bound/padding **subject to the entry search1 invariant and source's unmodified constants**. It does NOT establish native multiplication/bounds of every initial state or a-clipped interval semantics; the current Rust implementation does not implement a [B,E)-specific a-mask.

**Genuine odd-run/two-even meeting.** Suppose m is odd >=3 and has r>=1 consecutive odd shortened-T steps, followed by two even steps (so x=T^r(m) is divisible by 4). Let p=(m−1)/2. Then p is positive and strictly smaller than m, its first r−1 steps are odd, followed by even and odd, and T^(r+1)(p)=T^(r+2)(m)=x/4. Proof: x+1=3^r(m+1)/2^r, so if z=T^(r−1)(p), then x=3z+2, and x divisible by 4 forces z ≡2 mod4. Thus z→z/2→(3z+2)/4=x/4. A 2480-case capped literal-T check was PASS. For use on an arbitrary original start n, one must STILL show this local predecessor p is <n rather than merely <m, using the theorem's quantitative dip bound or direct witness; Theorems 4.1/4.4 require all visited path values >=99,781 OR an independently authenticated earlier-small-hit escape. The small fixture proves neither condition universally.

**No completion claim for search1.** Proof of the entire recurrence state (base,sigfig,threepower,number,doubleeven,numevens) for all path branches, including exact flag transitions and last-bit high mask, remains incomplete. In particular main.rs 149–179 computes maxval from descent/two-even/preimage components and sets initialbitarray for maxval<=cutoff; soundness of EVERY cleared bit requires precise source-to-paper semantics and 99,781 exceptions, not just the 16-step identity. main.rs lines 309–313 doubleeven masks also require full witness inequalities with original n. A true larger-state path meeting at local m is not automatically a certificate at the original base.

## Result C — exceptions and Bařina remain NO-GO

**Independent conservation fixture.** Standard-library research/r3e21_33_semantic_probe.py verifies a canonical 64-start [103,167) independent literal-T roster. It rejects 14 deliberately hostile modifications: missing/duplicated/reordered starts, missing/duplicate kernel completion, unknown or out-of-order exception ordinals, event-buffer truncation, false proof, fake arithmetic trace, no descent, forged-valid-looking hash, and unresolved original. PASS of this fixture means *only* that a complete roster CAN be checked. It does NOT prove the actual kernels disclose all exceptional starts *at generation*: source branch coverage, device append capacity/overflow flags, completion seals, and read-back transport proofs are still absent. A normal return after reset-to-2 or print/return cannot become a completion event. All original starts with one or more ordered exceptions stay UNRESOLVED until independently arbitrated.

**Angeltveit CUDA/OpenCL.** Source default MAXBITS=45 cannot represent B. CUDA source has explicit print/reset-to-2 at lines ~295–300 and ~334–340; a successful hash after reset does not authenticate original convergence. Four-u32 carry/borrow, unsigned widening (including p3 and addition of carry), funnel shifts 0/31/32/63/64/127/128, ctz/ffs zero handling, lookup limits, host launch coverage, device/host event capacity, retuned N=72 correctness are NOT proved. Do not reuse Rust arithmetic proof as a GPU proof.

**Bařina.** Worker CPU non-precalc +3/stride4 is an exact class3 abstract cover for aligned complete units, but half-open arbitrary [L,H) and final partial need explicit clipping. worker.c 96–103 defines IS_LIVE differently for USE_LUT50 vs bitmap; actual source-generated map bytes, generator semantics, digest and compiled macro/config identities are the FIRST missing map artifacts. worker.c 341–366 USE_PRECALC N0=(task_id<<task_size)+(h<<R0)+L0 and N=(H>>R0)*3^Salpha+L require a source-authenticated T^R0(N0)=N with exact flags and no unsigned overflow. CPU _USE_GMP vs print/abort is build-dependent. kernel.cl lines ~181–232 class3 workload segments, IS_LIVE, ctz, overflow and checksum zero-return require complete per-original-start events, per-workgroup dispatch receipts and host fallback proof. Source commit != compiled flags/driver/ISA/map. No source-compiled build or 2^40 work-unit proof was executed.

## Reproduction and acceptance matrix

Run **python3 research/r3e21_33_semantic_probe.py** using only the standard library. Local capped output during authorship: R33_TOY_PASS, lookup_states=65583; 130-bit guard violation; search2 minimum threepower=42 and padded words=262145; 2480 meeting samples; 2222 inverse-preimage samples; 64 roster starts; 14 adversarial rejections. This is NOT a full 2^24 bitarray precomputation, source compilation, emitted-exception proof, GPU benchmark or scientific verification. Hosted CI remains ABSENT/NOT_RUN until actually observed.

| Acceptance axis | Tier | Status |
| --- | --- | --- |
| Exact mathematical interval class3 / a-cylinder cover | mathematical | PROVED in R31–R32 |
| Sixteen-step table semantics, lower-bound and padding, local two-even coalescence | specified mathematics | PROVED / capped tests |
| 24-step all-state bitmap, search1 flags, 99,781 alternatives | actual source equivalence | UNKNOWN |
| Rust 128-bit exception-proof search3 | runtime source | COUNTEREXAMPLE to unrestricted guard; reachable-case risk UNKNOWN |
| CUDA/OpenCL four-limb, Bařina LUT map/precalc/compiled flags | source/build | UNKNOWN |
| Exception generation, durable transport, kernel completion | conservation | UNKNOWN |
| Independent literal-T arbiter over full actual source roster | independent certification | NOT IMPLEMENTED |
| Cold/warm 20+20 benchmark on [2^70,2^70+2^40) per build | owner-only timing | NOT_RUN |
| Global [B,E) convergence verification / new frontier | science | NOT_RUN |

**Decision: NO-GO EVEN TO REQUEST HARDWARE BENCHMARK AUTHORISATION.** The first concrete safe next step is a fail-closed 16-step Rust source-equivalent exception contract plus reachable-state range proof; in parallel, finish 24-step cleared-bit semantics and source-specific Bařina map/precaclc obligations. Do not infer any extra excluded integers. The deliberately held benchmark, 20 cold/20 warm per source with immutable p50/p95 and build/device/map/GMP evidence, stays NOT_RUN. No science, native worker/verifier, production, website/feed, frozen protocol, owner's computer, spend, contact, BOINC recruitment, publication or arXiv submission in R33.
