#!/usr/bin/env python3
"""R3E21-28: research-only exact interval-cover and parity-affine fixture.
No scientific Collatz batch, no full orbit-to-one, no external I/O, no production API.
"""
from fractions import Fraction

B = 2392518188130438742016
E = 3000000000000000000000
U = 2 ** 40

def T(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def ceildiv(a, b):
    assert b > 0
    return -((-a) // b)

def bounds(lo, hi, k, r):
    assert 0 <= r < 2 ** k and lo <= hi
    d = 2 ** k
    qlo = ceildiv(lo - r, d)
    qhi = ceildiv(hi - r, d) - 1
    return qlo, qhi

def count(lo, hi, k, r):
    a, b = bounds(lo, hi, k, r)
    return max(0, b - a + 1)

def affine(r, k):
    assert 0 <= r < 2 ** k
    n, s, carry = r, 0, 0
    for j in range(k):
        if n % 2:
            s += 1
            carry = 3 * carry + 2 ** j
        n = T(n)
    return s, carry

def iterate(n, k):
    for _ in range(k):
        n = T(n)
    return n

def cover_fixture(lo, hi):
    for k in range(9):
        assert sum(count(lo, hi, k, r) for r in range(2 ** k)) == hi - lo
        for r in range(2 ** k):
            assert count(lo, hi, k, r) == (
                count(lo, hi, k + 1, r) +
                count(lo, hi, k + 1, r + 2 ** k)
            )

def main():
    w = E - B
    q, r = divmod(w, U)
    assert B % U == 0
    assert q == 552501489 and r == 350507499520
    assert q * U + r == w and 0 < r < U
    assert B + q * U + r == E
    assert Fraction(w, U) == Fraction(289669900831967, 524288)
    for lo, hi in (
        (17, 59), (B, B + 270), (B + 3, B + 17),
        (B + U - 11, B + U + 19),
    ):
        cover_fixture(lo, hi)
    for k in range(1, 10):
        for residue in range(2 ** k):
            s, c = affine(residue, k)
            for q0 in (0, 1, 7, 13):
                n = residue + (2 ** k) * q0
                assert 2 ** k * iterate(n, k) == 3 ** s * n + c
    assert affine(1, 4) == (2, 7)
    assert iterate(1, 4) == 1
    assert iterate(17, 4) == 10
    assert affine(3, 4) == (2, 5)
    assert iterate(3, 4) == 2
    print("R3E21_28_RESEARCH_ONLY_COVER_AND_AFFINE_PASS")
    print("FULL_UNITS", q, "PARTIAL", r, "TASK_RECORDS", q + 1)
    print("No Collatz-to-one or scientific interval computation executed.")

if __name__ == "__main__":
    main()
