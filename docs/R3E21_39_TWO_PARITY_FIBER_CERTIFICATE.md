# R3E21-39 — independent exact-T two-parity bitmap and finite original-start fiber

**15 October 2026 | £0 research only | bounded mathematical/source checks | NO-GO for scientific frontier, benchmark, native source changes, crowdsourcing or publication.**

## Decision and what changed

1. **Parity repair is concretely reproducible:** a new source-distinct C++ construction enumerated **all 2 × 2^24 cells**, choosing actual positive high lifts with the appropriate mod-3 starting state, running **literal shortened T**, and checking at every even transition that the mod-3 predecessor is integral if and only if the *actual* carried even-run parity permits it. It reproduced the R38 eight-by-two live counts, **399,426** differing scores, **63,015 source-cleared/corrected-live** and **11,401 source-live/corrected-cleared** low-residue/threshold pairs. Full index inverses, eight 3^(42+a) permutations, 1=LIVE, extra 64-bit wrap cell and all 64 high lifts for five boundary probes also passed. This is complete **finite scoring arithmetic**, not proof that every bitmap shortcut certifies every original integer.
2. **Exact bounded original-start family:** for the fixed actual R38 source-search1 66-bit root r=6358120439071089947, among **all 64 possible high lifts** a=0..63, **exactly eight** original n=r+a·2^66 lie in [B,E). All eight pass the genuine source-search1 66-bit root gate (including rational and predecessor cuts); **exactly four** pass source mod9 and incoming doubleeven gates; **exactly one**, a=37 and n=2736476243348084729115, has source q=0 clear but corrected q=1 live at a=f−42=1, cutoff 659. The new independent original-start trace confirms no strict descent at steps 1..115, no integral predecessor smaller than original at true steps 67..90, source score 791, parity-correct score 612, invalid imagined predecessor at step 68, and first actual descent at step 116. It **does not** cover the other 63,015 bitmap residue/threshold pairs, other roots, or every conceivable path-coalescence proof. An actual false local reason for a clear is **not** a Collatz counterexample and does not invalidate an independently valid later certificate.
3. **Later Rust j blocks gain strict, small completed strata:** all **247,020** parity cylinders with at most three even steps for the j=114 prefix and next 16 odd steps, and all **366,276** such cylinders for j=130, were exhaustively enumerated modulo 2^(j+16); **zero** representatives X0 in [2,2^72]. Correctness of the cylinder congruence was checked against miniature literal-T tests. The **exact untouched remainders** are 362205922639287064 words at j=114, and 1080231996567188756950656 at j=130 (necessary growth-limited classes). m=4 already has 6,672,876 / 11,358,880 probes, beyond the prescribed 5m cap. These are **not** proofs that all later j are overflow-free. R36 j98 complete certificate is preserved unchanged.

## Symbolic q-inheritance theorem and exact four predicate boundaries

Take T(z)=z/2 for even z and (3z+1)/2 for odd z; X=z+1. For **any** odd predecessor u, T(u)≡2 mod3; repeated even steps multiply the state by 2⁻¹≡2 mod3. Thus after q consecutive even steps since that odd step, z≡2(−1)^q mod3; z≡2 mod3 exactly when q is even. A proposed odd predecessor p=(2z−1)/3 is an integer exactly when z≡2 mod3. **The q parity is indispensable until the first new odd step; an odd step resets q=0.** The Rust source search1 carries q, but precompute sets q=0 at the start of each 24-step suffix. Hence at a current in-window even step, the tested next-state backward shortcut is permitted precisely when (incoming q + the new in-window even count) mod2=0, provided no odd step has intervened. This proves why the observed **both-direction** scoring disagreements arise.

The four distinct potential witness mechanisms, with their quantifier boundaries, are:

- **Strict forward descent:** find a genuine k≥1 and exact original n such that T^k(n)<n. In an entire low-bit search1 cylinder, the source's rational criterion requires the 306/485 log bound and exact source root/lift transport; a score threshold alone is not an exact numerical descent.
- **Odd-predecessor merge:** a genuine state z must satisfy z≡2 mod3, p=(2z−1)/3 a positive *integer*, and p<n (or a separately proved smaller certified root), with a shared following orbit. Incoming q fixes eligibility at the boundary. At source's score update for an even step the relevant state is **after** that even step, not before it. Equality p=n is not smaller and cannot be silently accepted. The witness at i=68 is nonintegral; at i=67 p is integral but p>n.
- **Doubleeven coalescence:** an odd-window bit starting at position i is followed by the first subsequent even position j and another even position j+1, with **j+2<24** (source strict truncation). The independent left-to-right scanner agrees with Rust's trailing-ones/ctz formula throughout all 2^24 words; the two-even pattern alone is only an algebraic trigger. It must still be linked to a positive smaller original-start coalescence via the upstream theorem/inequality and source flags, not treated as a blanket safe exclusion.
- **Low-state route:** when a genuine trajectory falls into the separately verified ≤99,781 basin, lower-start/finite-base induction can close it. The R38 explicit bounded n≤99,781 literal-T check is **inherited**; the Angeltveit Theorems 4.1/4.4 high-intermediate-state hypotheses must be retained unless the low-state route is actually discharged. This report does not independently prove the *whole* source implementation of these theorems.

For z0=original T^66(n), original n=r+a·2^66, search1 number+ a·3^f = z0+1; the search2 bitmap index is [(number·3^(−f) mod2^24)+a] mod2^24. For f=42+array_a, the independent bitmap writes at [r_low·3^(−(42+array_a))] mod2^24. Inverse permutation is a unit in Z/2^24; 64-bit word crossing wraps correctly. **Source 1=LIVE; a bit clear is the pruning operation.** Threshold comparison is maxval ≤174+485·array_a (live), not the reverse. These algebraic/index facts are complete; whether every actual cleared cell has *some* sound witness is still open.

## Reproduction and explicit scopes

Run in a standard local research checkout (no native source build or scientific interval):
```sh
python3 -B research/r3e21_39_exact_lift_fiber.py
python3 -B research/r3e21_39_later_block_caps.py
g++ -O3 -std=c++17 -Wall -Wextra -o /tmp/r39-bmp research/r3e21_39_independent_bitmap.cpp
/tmp/r39-bmp
```

Exact expected assertions:
```text
R39_EXACT_FIBER_PASS interval_lifts=8 admitted_lifts=4 false_clear_lifts=1 no_direct_or_predecessor_through90=1
R39_WITNESS_PASS original_n=2736476243348084729115 lift=37 original_24word=0x9faddc source=791 corrected=612 cutoff=659 first_descent=116
R39_LATER_STRATUM_PASS j=114 checked=247020 zero_hits=1 unexamined=362205922639287064 max_m=14 next_class_count=6672876 cap_probes=5000000
R39_LATER_STRATUM_PASS j=130 checked=366276 zero_hits=1 unexamined=1080231996567188756950656 max_m=21 next_class_count=11358880 cap_probes=5000000
R39_INDEPENDENT_BITMAP_PASS residues=16777216 parity_states=2 mismatched=399426 source_clear_corrected_live=63015 source_live_corrected_clear=11401 padded_lifts=64
```

These tests **actually passed in the bounded research environment** before push, including a separate full C++ 2×2^24 scan (~13.4 s on this non-frontier environment; NOT benchmark). The workflow changes ensure both PR and push triggers for all three new fixtures, plus exact failures and both g++ / clang++; R36, R37 and R38 jobs are retained. **Record PR-head CI run SHA, job URLs and outcomes only after observed**; do not substitute historical green R38 run for R39. No 2^72 sweep, n≥B scientific batch, GPU or native production code was executed.

## External source and map provenance

Pinned source observations: Angeltveit vigleik0/collatz `f3f09248c7ae7299b8443e112f565f309d97f161` remains HEAD as queried; Bařina xbarin02/collatz **current HEAD** `e98d0294a7ff77e783907e307a80e83b92f4a164` differs from evidence-pinned `141e13aae243d509a01a43bec597f53a5b97a09f`; xbarin02/collatz-sieve evidence pin `e5f0c264ba1f5f9c0a7d32a10c3aa61b225c70d1` remains HEAD. This does not silently rebase any audited worker binary to the new HEAD. Angeltveit arXiv 2602.10466 v1 remains the identified version; no proof of an updated version from this check.

The actual pinned first-party LUT50 `fdc.c` and `fdd.c` share **the same 50 pairwise-distinct 64-bit words** (blob hashes `1ed04b...` and `0074ab...`). Hence if a raw stream consists of these dictionary words in the expected host byte order, fdc maps every full 8-byte input word injectively to an index 0..49, and fdd reverses each valid index (ordinary 50-value partial codec). The decoder does **not** check whether incoming byte index is <50; there is no independent data-byte-range proof, full-byte read test, or resilient malformed-input handling. Both helpers recursively call their next-item function, so resource behavior on giant streams is not certified; the endian assumption must be pinned. In particular the **exact original raw generator** for `esieve-34.lut50` and `h2esieve-24`, actual compressed/downloaded map SHA-256, native executable SHA-256, deployed compile options and period of deployment remain **NOT REVERIFIED**. `bootstrap.sh` performs live git pull and `unpack.sh` chooses raw/lz4/lzo/gzip by availability: source snapshot ≠ actual build attestation. We performed no download and make **no** map digest claim.

All-path Bařina `USE_PRECALC` L++, zero-ctz, alpha/beta and 64→63 clamp, shifts, R decrements, signed unsigned type transport, sieve/lookup table, GMP and GPU producer/host/partial coverage remain **UNPROVED**. A safe proposed native exception process would reserve `UNRESOLVED(original_n, step_ordinal, source, immutable_pre_state)` before every possibly overflowing multiply/add, high cutoff or abort, seal the event, and compare against an **independently generated original-start roster** plus arbitrary-precision literal-T arbiter. Event-only omissions and reservation-only omissions can be caught by matching records; a **joint** reservation-and-event omission defeats producer-only checksums and demands a separate roster. This is **pseudoprotocol**, not an implemented source patch or exception emitter.

## External interval and evidence tiers

Author homepage checked on 15 October 2026, generated **Thu 15 Oct 2026 17:39:51 +0200**: first incomplete **2175982616×2^40** and first unassigned **2175982616×2^40** are recorded as separate indicators even though equal in that snapshot. These are **author-reported** status, not CEML-reverified science; peer-reviewed historical `n<2^71` is a separate tier.

Carry unchanged B=`2392518188130438742016`; exclusive E=`3000000000000000000000`; U=2^40; **552501489 full units + one partial 350507499520**, conditional conservative candidate majorant **326518028938128165 unchanged**, actual survivors **UNKNOWN**. This research neither establishes disjointness of earlier exclusions nor promotes a new global sieve certificate. The frozen scientific V2/I1 records, website/feed, 20 cold + 20 warm per-source [2^70,2^70+2^40) untouched p50/p95 benchmark plan, hardware, production, and crowdsourcing remain untouched and **UNEXECUTED**.

## GO/NO-GO and next gate

**NO-GO for production changes, frontier science, benchmark permission request, crowdsourcing and external correctness claims.** Research-only bounded CI is authorised. Tier assessment: q-mod3 inheritance **MATHEMATICAL PROOF**; full finite 2×2^24 score/index construction **LOCAL FINITE CERTIFICATE** with CI to confirm; one exact original 66-bit fiber **FINITE SOURCE-FILTERED TRACE**; j98 **INHERITED complete R36 certificate**; j114/j130 m≤3 **NEW COMPLETE FINITE STRATA**, remainder explicit; full source/compiled binary/native exceptions/maps/independent whole-work-unit arbiter **NOT CERTIFIED**. Next R40 should focus one sharply defined source-reachable witness theorem (full q0/q1 repair and independent source-certified 66-bit prefix/bitmap gate) before dispersing effort across map and native-block engineering. Preserve separate secondary backlog and stop conditions.

## GitHub Actions independent verification (first complete PR-head check)

On R39 PR #70 commit `08e89a9b41fd98040366b5ea49b05d81b3ef1ac2`, actual [Actions run 38771219326](https://github.com/jfairfaxball-348/CEML/actions/runs/38771219326) completed **SUCCESS** with all **8/8 jobs passing** (15 October 2026):

- [R36 MITM and R37 bounded Python](https://github.com/jfairfaxball-348/CEML/actions/runs/38771219326/job/116547230442) — PASS.
- [R37 all-24-bit g++](https://github.com/jfairfaxball-348/CEML/actions/runs/38771219326/job/116547230148) and [clang++](https://github.com/jfairfaxball-348/CEML/actions/runs/38771219326/job/116547229987) — PASS.
- [R38 authentic original and two-parity g++](https://github.com/jfairfaxball-348/CEML/actions/runs/38771219326/job/116547229990) and [clang++](https://github.com/jfairfaxball-348/CEML/actions/runs/38771219326/job/116547229898) — PASS.
- [R39 full independent positive-lift bitmap g++](https://github.com/jfairfaxball-348/CEML/actions/runs/38771219326/job/116547230005) and [clang++](https://github.com/jfairfaxball-348/CEML/actions/runs/38771219326/job/116547229585) — PASS.
- [R39 original-start exact fiber + later-block caps](https://github.com/jfairfaxball-348/CEML/actions/runs/38771219326/job/116547229875) — PASS.

**Important:** this appendix creates a *new documentation commit after the above successful run*. The cited 8/8 verdict is tied to `08e89a9...`, **not automatically** to the eventual merge SHA. Confirm any newer PR-head run after the appendix change, and any merged-main push run separately; never pretend cross-SHA status transfers.

## Fixed full chronological source-admitted witness (additional R39 artifact)

The exact original-start sequence for `n=2736476243348084729115` is committed as [117-state original witness JSON](../research/r3e21_39_original_witness_trace.json), from T^0 through T^116 inclusive, with original n, fixed source-text pin, exact odd count 43 through the first 66 states, incoming-even-run 1, and first strict descent at 116. The independent R39 Python witness fixture **recomputes the entire record element by element**, checks every equality, validates the pre-boundary odd count, and emits `R39_TRACE_FILE_PASS`; both PR and push workflow path filters include the JSON artifact. The earlier 8-job run in the previous appendix predates this new file and **does not certify this newer PR head**; re-check the new exact SHA and jobs. Nothing in this file is a frontier science batch or full-source deployed binary verification.
