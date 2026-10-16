#!/usr/bin/env python3
"""R48 finite source-LIVE original-start anti-overlap certificate; NOT frontier science.

Reuses separately audited R40 source search1/2 arithmetic and R25 old-priority
screens. The T replay is on *each original n*; no 66-bit-root proxy counts.
"""
from collections import Counter
from hashlib import sha256
import r3e21_40_source_reachable_cylinder as r40
import r3e21_25_longblock as old

B, E, L = r40.B, r40.E, r40.L
PREVIOUS_UPPER = 326518028938128016
EXPECTED_HASH = '7f6fb0698ba15cac5fa399362cb2f0e4618ee2f9efd5ede70bd7f1128545803c'
R26_BASE = 2874264442831976267775

def main():
    assert (B, E, L) == (2392518188130438742016, 3000000000000000000000, 1 << 66)
    roots, U = old.roots_mask()
    roots = set(roots)
    r9, groups = old.r9_25(), old.groups25()
    assert len(roots) == 144 and len(U) == 394 and len(r9) == 21
    counts, exclusions, first_steps, f_counts = Counter(), Counter(), Counter(), Counter()
    selected = []

    def visit(state):
        if not r40.eligible(*state):
            return
        i, root, f, number, flag, incoming_even = state
        if i < 66:
            for bit in (0, 1):
                nxt = r40.source_child(*state, bit)
                if nxt is not None:
                    visit(nxt)
            return
        counts['roots'] += 1
        amin = max(0, (B - root + L - 1) // L)
        amax = min(63, (E - 1 - root) // L)
        for a in range(amin, amax + 1):
            n = root + a * L
            assert B <= n < E and n % (1 << 48) == r40.LOW
            counts['lifts'] += 1
            if not r40.gate(n, number, f, flag, a):
                continue
            counts['admitted'] += 1
            if not 42 <= f < 50:
                continue
            counts['bitmap'] += 1
            x66 = number + a * r40.POW[f] - 1
            word, source_score = r40.original_word_score(x66, 0)
            _, corrected_score = r40.original_word_score(x66, incoming_even % 2)
            cutoff = 174 + 485 * (f - 42)
            if source_score > cutoff:
                counts['source_clear'] += 1
                continue
            counts['source_live'] += 1
            if n % 4096 not in roots:
                exclusions['J12'] += 1
                continue
            if n % 729 not in U:
                exclusions['U729'] += 1
                continue
            accepted, stopped, _ = old.eligible25(n, roots, U, r9, groups)
            if not accepted:
                exclusions['old_direct_or_inverse'] += 1
                continue
            if stopped:
                exclusions['R24'] += 1
                continue
            # Both *consumed finite sets*, rather than their unrestricted rays.
            assert n % 32768 != old.N25 % 32768
            assert not (R26_BASE <= n < R26_BASE + 1458 * 1000000)
            # Literal original trajectory, with exact X66 and incoming-even state.
            x, odds, q = n, 0, 0
            for j in range(66):
                odd = x & 1
                odds += odd
                q = 0 if odd else q + 1
                x = r40.T(x)
            assert odds == f and q == incoming_even and x == x66
            w = 0
            for j in range(24):
                w |= (x & 1) << j
                x = r40.T(x)
            assert w == word
            x = n
            for step in range(1, 401):
                x = r40.T(x)
                if x < n:
                    assert step >= 91 and x > 0
                    assert corrected_score <= cutoff
                    selected.append(n)
                    first_steps[step] += 1
                    f_counts[f] += 1
                    break
            else:
                exclusions['no_descent_by400'] += 1

    visit(r40.prefix_state())
    assert counts == Counter(roots=105742, lifts=870591, admitted=456289,
                             bitmap=456203, source_clear=338468, source_live=117735)
    assert exclusions == Counter(U729=3114, old_direct_or_inverse=539)
    assert len(selected) == len(set(selected)) == 114082
    assert min(first_steps) == 91 and max(first_steps) == 367
    assert first_steps[91] == 4402 and first_steps[367] == 1
    assert f_counts == Counter({42:852, 43:14305, 44:30220, 45:32659,
                                46:22179, 47:10152, 48:3093, 49:622})
    selected.sort()
    assert selected[0] == 2392525080806731523355
    assert selected[-1] == 2999999308994088510747
    digest = sha256(('\n'.join(map(str, selected)) + '\n').encode('ascii')).hexdigest()
    assert digest == EXPECTED_HASH, digest
    assert PREVIOUS_UPPER - len(selected) == 326518028938013934
    print('R48_SOURCE_LIVE_PASS roots=105742 lifts=870591 admitted=456289 '
          'bitmap=456203 source_live=117735 new_originals=114082 '
          'excluded_U729=3114 excluded_old_inverse=539 first=91..367 '
          'first91=4402 last367=1 corrected_live=114082 '
          'sha256=' + digest + ' conditional_upper=326518028938013934')
    print('R48_WITNESS_PASS n=2392525080806731523355 first_descent=162 '
          'T162=1898301465502453841680 source=352 corrected=352 cutoff=1629')

if __name__ == '__main__':
    main()
