#!/usr/bin/env python3
"""R3E21-36 finite 114-bit sparse-parity cylinder certificate; research only.

No frontier workload, native production code, crowdsourcing, or source binaries.
Python standard library only. Fixed bounded N=72,J=98,W=114,Z=7.
Expected memory ~130 MiB, time ~11 s on the author's research environment
(the machine used for the fixture, NOT an owner's or frontier benchmark).
"""
from bisect import bisect_left
from itertools import combinations
from math import comb

J, W, Z, N = 98, 114, 7, 72
M = 1 << W
LIMIT = 1 << N
inverse3 = pow(3, -1, M)
ratio = (2 * inverse3) % M
powers = [pow(ratio, p, M) for p in range(J)]
terms = [[(3**k * v) % M for v in powers] for k in range(Z)]


def is_start_residue(s):
    x = (-s) % M
    return 2 <= x <= LIMIT  # X0=n+1, 1<=n<2^72


def verify_small_oracle():
    """Independent literal shifted-T steps for every n<2^12 with <=7 even states."""
    for n in range(1, 1 << 12):
        x, even_positions = n + 1, []
        for j in range(12):
            if x % 2:
                even_positions.append(j)
                x = (x + 1) // 2
            else:
                x = 3 * x // 2
        if len(even_positions) <= Z:
            residue = (-sum(terms[k][p] for k, p in enumerate(even_positions))) % (1 << 12)
            assert residue == (n + 1) % (1 << 12)
    print("small_oracle_pass=True", flush=True)


def prove_empty_sparse_cylinders():
    total = 0
    for m in range(Z + 1):
        first_half = m // 2
        count = comb(J, m)
        if m == 0:
            assert not is_start_residue(0)
            print("m=0 cylinders=1 hits=0", flush=True)
            total += 1
            continue
        if first_half == 0:
            found = [p for p in range(J) if is_start_residue(terms[0][p])]
            assert not found, found
        else:
            left = sorted(
                (sum(terms[k][p] for k, p in enumerate(es)) % M, es[-1])
                for es in combinations(range(J), first_half)
            )
            values = [v for v, last in left]
            assert len(left) == comb(J, first_half)
            found = []
            # Right half streamed; retain only <= C(98,3) left tuples.
            for es in combinations(range(J), m - first_half):
                rhs = sum(terms[first_half + k][p] for k, p in enumerate(es)) % M
                low = (M - LIMIT - rhs) % M
                high = (M - 2 - rhs) % M
                ranges = ((low, high),) if low <= high else ((0, high), (low, M - 1))
                for lo, hi in ranges:
                    idx = bisect_left(values, lo)
                    while idx < len(values) and values[idx] <= hi:
                        if left[idx][1] < es[0]:
                            possible_start = (-(values[idx] + rhs)) % M - 1
                            assert 1 <= possible_start < LIMIT
                            found.append((m, possible_start, es, left[idx]))
                        idx += 1
            assert not found, found[:4]
        total += count
        print(f"m={m} cylinders={count} hits=0", flush=True)
    assert total == 14958711636
    print(
        f"R36_MITM_PASS cylinders={total} "
        "third_block_unsafe_sparse_cylinders=0", flush=True
    )


if __name__ == "__main__":
    verify_small_oracle()
    prove_empty_sparse_cylinders()
