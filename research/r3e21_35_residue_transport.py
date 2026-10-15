#!/usr/bin/env python3
"""R3E21-35 bounded research fixture, independent of production source.
This tests arithmetic only. No source/build/map/frontier certificate.
"""
from collections import Counter
from math import comb

M = (1 << 128) - 1
CUTOFF = 1 << 120

def T(n):
    assert n > 0
    return n//2 if n % 2 == 0 else (3*n+1)//2

def table(r):
    """Direct 16 shifted-map steps with zero as formal lookup sentinel."""
    assert 0 <= r < (1 << 16)
    s, c = 0, r
    for _ in range(16):
        if c % 2 == 0:
            s, c = s+1, 3*c//2
        else:
            c = (c+1)//2
    return s, c

def lookup_test():
    counts = Counter()
    qmax = (CUTOFF-1) >> 16
    for r in range(65536):
        s, c = table(r)
        counts[s] += 1
        assert c <= 3**s
        assert (s == 16) == (r == 0)
        if s <= 15:
            assert qmax*3**s+c <= (1 << 104)*3**15 < (1 << 128)
        else:
            assert c == 0
    assert [counts[i] for i in range(17)] == [comb(16,i) for i in range(17)]
    qmin = M // (3**16) + 1
    threshold = qmin << 16
    assert threshold < CUTOFF
    assert qmin*3**16 > M and (qmin-1)*3**16 <= M
    return threshold

def tj(n,j):
    for _ in range(j): n=T(n)
    return n

def search1_transport_test():
    # Source recursion's parity-directed arithmetic, WITHOUT using source
    # pruning. Covers all 2^11-1 partial binary nodes through depth 12.
    stack=[(3,2,2,9)]
    nodes=0
    while stack:
        base,j,k,x=stack.pop()
        assert base%4 == 3 and x == tj(base,j)+1
        for a in (0,1,2,3):
            assert tj(base+(a<<j),j)+1 == x+a*3**k
        nodes+=1
        if j == 12: continue
        for bit in (0,1):
            b=base+(bit<<j)
            z=x+bit*3**k
            if z&1: stack.append((b,j+1,k,(z+1)//2))
            else: stack.append((b,j+1,k+1,3*z//2))
    assert nodes == (1<<11)-1
    assert 3**66 < 2**105
    return nodes

def loss_test():
    # A producer-provided count rejects one-sided loss only.
    event=['UNRESOLVED:original=103:ordinal=0']
    def ok(reserved,emitted,count):
        return count==len(reserved) and reserved==emitted
    assert ok(event,event,1)
    assert not ok(event,[],1)  # lost output, reservation intact
    assert not ok([],event,1)  # lost reservation, event intact
    assert ok([],[],0)         # undetectable joint producer omission!
    return 2

def main():
    threshold=lookup_test()
    nodes=search1_transport_test()
    losses=loss_test()
    print('R35_TOY_PASS residues=65536 unsafe_residue=0 '
          'unsafe_x_min=%d transport_nodes=%d single_drops_rejected=%d '
          'joint_omission_requires_static_coverage=TRUE' %
          (threshold,nodes,losses))

if __name__=='__main__': main()
