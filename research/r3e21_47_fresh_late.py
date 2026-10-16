#!/usr/bin/env python3
"""R3E21-47: bounded true-late-descent original-start priority-difference certificate.

This reuses the exact earlier R40 source-reachable low-48 cylinder enumeration
and independently coded R25 inherited J12/U + R9/R24 old-priority screens.
It is NOT a native verifier, full-interval census, or a proof of convergence to 1.
"""
from collections import Counter
from hashlib import sha256
import r3e21_40_source_reachable_cylinder as r40
import r3e21_25_longblock as old

B, E = r40.B, r40.E
UPPER_OLD = 326518028938128165
UPPER_NEW = 326518028938128016
EXPECTED = "e2e797a88d5fefb00addaaab39536d1b557e56d99215658e7e21546e6c0ff082"

def trace(n):
    x = n
    states = [n]
    first = None
    for j in range(1, 182):
        x = old.T(x)
        states.append(x)
        if x < n and first is None:
            first = j
    return first, states

def main():
    assert (B, E) == (2392518188130438742016, 3000000000000000000000)
    counts, bad, old_descents = Counter(), [], Counter()
    r40.dfs(r40.prefix_state(), counts, bad, old_descents)
    assert len(bad) == len(set(bad)) == 167
    assert (counts["root"], counts["interval"], counts["admitted"],
            counts["bitmap"], counts["source_clear"]) == (
                105742, 870591, 456289, 456203, 338468)
    assert (sum(old_descents.values()), min(old_descents), max(old_descents)) == (167, 91, 181)

    roots, U = old.roots_mask()
    roots = set(roots)
    assert len(roots) == 144 and len(U) == 394
    r9, groups = old.r9_25(), old.groups25()
    classes = Counter()
    fresh = []
    first_steps = Counter()
    for n in sorted(bad):
        assert B <= n < E
        if n % 4096 not in roots:
            classes["J12"] += 1
            continue
        if n % 729 not in U:
            classes["U729"] += 1
            continue
        accepted, stopped, _hit = old.eligible25(n, roots, U, r9, groups)
        if not accepted:
            classes["old_inverse_or_D72"] += 1
            continue
        if stopped:
            classes["R24"] += 1
            continue
        # Earlier R25 and R26 finite one-million-q families, not full rays.
        assert n % 32768 != old.N25 % 32768  # all R40 cylinder starts
        ray26_base = 2874264442831976267775
        assert not (ray26_base <= n < ray26_base + 1458 * 1000000)
        step, states = trace(n)
        assert step is not None and 91 <= step <= 181
        assert all(x >= n for x in states[1:step])
        assert 0 < states[step] < n
        assert all(x >= n for x in states[1:73])  # exact D72 complement
        classes["fresh_late"] += 1
        first_steps[step] += 1
        fresh.append(n)
    assert classes == Counter({"fresh_late":149,"old_inverse_or_D72":17,"U729":1})
    assert len(fresh) == 149 and len(set(fresh)) == 149
    assert fresh[0] == 2405315022273487021339
    assert r40.N in fresh
    assert first_steps[91] == 8 and first_steps[181] == 1
    digest = sha256(("\n".join(map(str, fresh)) + "\n").encode("ascii")).hexdigest()
    assert digest == EXPECTED, (digest, EXPECTED)
    assert UPPER_OLD - len(fresh) == UPPER_NEW
    # Fully replay one specified original integer, not a low-bit root.
    step, states = trace(r40.N)
    assert (step, states[72], states[90], states[115], states[116]) == (
        116, 5135819021812816951207, 31235330163244917908105,
        4452395912276666812958, 2226197956138333406479)
    print("R47_FRESH_LATE_PASS original_starts=149 complement=18 first_range=91..181 "
          "old_inverse=17 u729=1 first91=8 last181=1 "
          "sha256=" + digest + " upper=" + str(UPPER_NEW))
    print("R47_WITNESS_PASS n=2736476243348084729115 D72_negative=1 "
          "first_descent=116 T116=2226197956138333406479")

if __name__ == "__main__":
    main()
