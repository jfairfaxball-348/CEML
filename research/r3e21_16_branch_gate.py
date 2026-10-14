#!/usr/bin/env python3
"""CEML R3E21-16: research-only finite tail-graph and source-semantic probes.
No Collatz-to-one interval science; no complete enhanced competitor reproduction.
"""
from functools import lru_cache

B = 2392518188130438742016
E = 3000000000000000000000
UPPER = 326928588657578096

def T(x):
    assert x > 0
    return (3*x + 1)//2 if x & 1 else x//2

def path(n, j):
    bits = []
    for _ in range(j):
        bits.append(n & 1)
        n = T(n)
    return n, tuple(bits)

def meet(x, a, y, b):
    z, px = path(x, a)
    w, py = path(y, b)
    assert z == w
    return (x, a, y, b, z, px, py)

def compose(e, f):
    x, a, y, b, _, _, _ = e
    v, c, z, d, _, _, _ = f
    assert y == v
    k = max(b, c)
    return meet(x, a+k-b, z, d+k-c)

# Pinned Bařina fsieve.c smallest_predecessor four primitive transports.
# Tuple: gate modulus, gate residue, numerator multiplier, loss, T steps.
BRANCHES = ((3, 2, 2, 1, 1), (9, 4, 8, 5, 3),
            (81, 10, 64, 73, 6), (243, 182, 128, 211, 7))

@lru_cache(None)
def pred(L, budget):
    best = L
    for (mod, res, mul, loss, _), debit in zip(BRANCHES, (1, 2, 4, 5)):
        if budget >= debit and L % mod == res:
            p, rem = divmod(mul*L-loss, mod)
            assert rem == 0 and p > 0
            best = min(best, pred(p, budget-debit))
    return best

def all_predecessors(L, budget):
    reachable = {L}
    agenda = [(L, budget)]
    states = set(agenda)
    while agenda:
        target, remaining = agenda.pop()
        for (mod, res, mul, loss, _), debit in zip(BRANCHES, (1, 2, 4, 5)):
            if remaining >= debit and target % mod == res:
                p, rem = divmod(mul*target-loss, mod)
                assert rem == 0 and p > 0
                reachable.add(p)
                state = (p, remaining-debit)
                if state not in states:
                    states.add(state)
                    agenda.append(state)
    return reachable

def ctz(n):
    assert n > 0
    return (n & -n).bit_length()-1

def barina_v2_v3(k, n, v3):
    # Faithful bounded source control-flow port, not native uint64 execution.
    R, L, previous, salpha = k, n, n, 0
    while R:
        L += 1
        alpha = min(ctz(L), R)
        salpha += alpha
        R -= alpha
        L = (L >> alpha) * 3**alpha - 1
        assert L > 0
        beta = min(ctz(L), R)
        R -= beta
        L >>= beta
        if v3:
            best = pred(L, salpha)
            if beta >= 2:
                best = min(best, pred((previous-1)//2, salpha-alpha))
            if best < n:
                return False
        elif L < n or (beta >= 2 and (previous-1)//2 < n):
            return False
        previous = L
    return True

def run():
    assert E > B and UPPER == 326928588657578096
    assert path(7, 3)[1] == path(15, 3)[1] == (1, 1, 1)
    assert path(7, 4)[1] != path(15, 4)[1]
    n, j = B + 243871, 20
    # Actual 72-step oracle vs exact affine-offset recurrence, NOT to 1.
    x, odd_count, C = n, 0, 0
    for depth in range(72):
        if x & 1:
            C = 3*C + (1 << depth)
            odd_count += 1
        x = T(x)
        assert 3**odd_count*n + C == (1 << (depth+1))*x
    assert path(n, 72)[0] == x and B <= n < E
    assert not B <= E < E
    y, word = path(n, j)
    assert y == 3637739920859037280367 and y % 9 == 8
    p1, p2 = (2*y-1)//3, (4*y-5)//9
    assert 0 < p2 < n < p1
    e1, e2 = meet(n, j, p1, 1), meet(p1, 1, p2, 2)
    assert compose(e1, e2)[0:5] == (n, 20, p2, 2, y)
    assert T(p2) == p1 and T(p1) == y and T(2*y) == y
    assert pred(y, 2) <= p2
    assert path((8*13-5)//9, 3)[0] == 13
    assert meet(1, 2, 1, 0)[0] == meet(1, 2, 1, 0)[2]
    assert meet(5, 1, 8, 0)[2] == 8 > 5
    assert meet(5, 1, 3, 2)[2] == 3 < 5
    for (mod, res, mul, loss, steps) in BRANCHES:
        for L in (res, res+mod, res+2*mod):
            p, rem = divmod(mul*L-loss, mod)
            assert rem == 0 and p > 0 and path(p, steps)[0] == L
    for L in range(1, 300):
        for budget in range(7):
            assert pred(L, budget) == min(all_predecessors(L, budget))
    compared = live_v2 = live_v3 = v3only = v2only = 0
    for k in range(2, 11):
        for r in range(1, 1 << k):
            a, b = barina_v2_v3(k, r, False), barina_v2_v3(k, r, True)
            compared += 1
            live_v2 += a
            live_v3 += b
            v3only += b and not a
            v2only += a and not b
    odd = sum(word)
    backward_gate = 306*(j-1) >= 485*(odd-1)
    assert odd == 13 and not backward_gate
    print("PASS 72-prefix affine oracle, branching composition, equality/phase/endpoint cases")
    print("PASS four source transports; 2093 independent primitive-min comparisons")
    print("PASS bounded v2/v3 control-flow", compared, live_v2, live_v3, v3only, v2only)
    print("PASS search1 rational h1 gate (20,13):", backward_gate)
    print("PRESERVED CONDITIONAL UPPER", UPPER)

if __name__ == "__main__":
    run()
