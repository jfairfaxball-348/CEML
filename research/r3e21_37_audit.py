#!/usr/bin/env python3
"""R37 research-only exact bounds, low-state base and miniature parity cylinders.

No frontier starts, production binaries, hardware tests or native emitters.
Python standard library only; deterministic bounded assertions.
"""
from itertools import combinations
from math import comb

D = 518059092085797269936906884792713216

def possible_max_evens(j):
    # Outside the {1,2} T-cycle, each even T-state >= 6.
    # X_j <= 2^72 (3/2)^j (8/21)^m.
    m = 0
    while 2**72 * 3**j * 8**m >= D * 2**j * 21**m:
        m += 1
    return m - 1

def cylinder_test(j, w, bits, cap):
    mod = 1 << w
    inv3 = pow(3, -1, mod)
    ratio = (2 * inv3) % mod
    terms = [[3**k * pow(ratio, e, mod) % mod for e in range(j)]
             for k in range(cap)]
    predicted = set()
    for m in range(cap + 1):
        for es in combinations(range(j), m):
            x = -sum(terms[k][p] for k, p in enumerate(es)) % mod
            if 2 <= x <= 1 << bits:
                predicted.add(x - 1)
    actual = set()
    for n in range(1, 1 << bits):
        x = n + 1
        es = []
        for i in range(w):
            if x % 2 == 0:
                x = 3 * x // 2
            else:
                if i < j:
                    es.append(i)
                else:
                    break
                x = (x + 1) // 2
        else:
            if len(es) <= cap:
                actual.add(n)
    assert actual == predicted, (j, w, len(actual), len(predicted))
    return len(actual)

def base_99781():
    longest = (0, 0)
    biggest = 0
    for start in range(1, 99782):
        z, steps = start, 0
        biggest = max(biggest, z)
        while z != 1 and steps < 10000:
            z = z // 2 if z % 2 == 0 else (3 * z + 1) // 2
            steps += 1
            biggest = max(biggest, z)
        assert z == 1, start
        if steps > longest[0]:
            longest = (steps, start)
    assert longest == (221, 77031) and biggest == 785412368
    return longest, biggest

def producer_omission_test():
    roster = tuple(range(11, 16))
    def producer_closed(reservations, events):
        return reservations == events
    assert producer_closed(roster, roster)
    assert not producer_closed(roster, roster[:-1])  # missing event
    assert not producer_closed(roster[:-1], roster)  # missing reservation
    assert producer_closed(roster[:-1], roster[:-1]) # JOINT omission invisible!
    assert roster != roster[:-1]                     # independent roster catches

def main():
    assert [possible_max_evens(j) for j in (98, 114, 130)] == [7, 14, 21]
    expected = ((98,14958711636),(114,362205922639534084),
                (130,1080231996567188757316932))
    for j, total in expected:
        bound = possible_max_evens(j)
        assert sum(comb(j,m) for m in range(bound+1)) == total
        print('j',j,'W',j+16,'max_evens',bound,'parity_words',total)
    for params in ((10,14,7,3),(12,16,8,4),(14,20,8,4)):
        print('mini',params,'matches',cylinder_test(*params))
    print('base_99781_pass',base_99781())
    producer_omission_test()
    print('R37_BOUNDED_AUDIT_PASS')

if __name__ == '__main__':
    main()
