#!/usr/bin/env python3
"""R40 exact source-text 66-bit cylinder certificate. Research ONLY; not frontier science."""
from collections import Counter
from hashlib import sha256

B, E = 2392518188130438742016, 3000000000000000000000
N = 2736476243348084729115
K, L = 48, 1 << 66
LOW = N % (1 << K)
POW = [3**i for i in range(67)]
EXPECTED_DIGEST = "ea27859daa20511ce786caba1c212110663e1d42fbb36f7b7a299028ed96406e"

def T(z):
    return z // 2 if z % 2 == 0 else (3*z+1)//2

def gate(n, number, f, flag, a):
    if n % 9 not in (0, 1, 3, 6, 7):
        return False
    if flag == 2 and (number+a) % 2 == 1:
        return False
    if flag == 1 and (number+(a if f%2 == 0 else 3*a)) % 4 == 1:
        return False
    return True

def source_child(i, base, f, number, flag, run, bit):
    x = number + bit*POW[f]
    odd = ((number & 1) == 0) != bool(bit)
    if odd:
        return (i+1, base+(bit<<i), f+1, x+x//2,
                (flag | int(306*(i+1)>=485*f)) & ~2, 0)
    if flag >= 2:
        return None
    return (i+1, base+(bit<<i), f, x//2+1, flag<<1, run+1)

def eligible(i, base, f, number, flag, run):
    return (number > base and 306*i < 485*f
            and not (run>=2 and run%2 == 0 and 306*(i-1)>=485*(f-1)))

def original_word_score(x, incoming):
    states = [x]
    word = 0
    for i in range(24):
        word |= (states[-1]&1)<<i
        states.append(T(states[-1]))
    cur = peak = 0
    run = incoming
    for i in range(24):
        if (word>>i)&1:
            j=i
            while j<24 and (word>>j)&1:
                j+=1
            if j+2<24 and ((word>>j)&3)==0:
                peak=max(peak,cur+306)
            cur-=179
            run=0
        else:
            cur+=306
            run+=1
            if run%2 == 0:
                peak=max(peak,cur+179)
        peak=max(peak,cur)
    return word, peak

def trace_certificate(n, number, a, f, run):
    path = [n]
    for _ in range(90):
        path.append(T(path[-1]))
    assert path[66] == number+a*POW[f]-1
    assert sum(z&1 for z in path[:66])==f
    assert run%2 == (1 if path[65]%2==0 else 0) if run in (0,1) else True
    # All direct descents and smaller integral predecessors through the exact 24-window.
    assert all(z>=n for z in path[1:91])
    for z in path[67:91]:
        assert z%3 != 2 or (2*z-1)//3 >= n
    z=path[-1]
    for step in range(91,2001):
        z=T(z)
        if z<n:
            return step
    raise AssertionError("no subsequent descent by step 2000")

def finish_root(state, counts, flagged, descents):
    _,root,f,number,flag,run=state
    counts["root"]+=1
    lower=max(0,(B-root+L-1)//L)
    upper=min(63,(E-1-root)//L)
    for a in range(lower,upper+1):
        n=root+a*L
        assert B<=n<E
        counts["interval"]+=1
        if not gate(n,number,f,flag,a):
            continue
        counts["admitted"]+=1
        if not 42<=f<50:
            continue
        counts["bitmap"]+=1
        z=number+a*POW[f]-1
        w,s0=original_word_score(z,0)
        w1,s1=original_word_score(z,run%2)
        assert w==w1
        threshold=174+485*(f-42)
        if s0>threshold:
            counts["source_clear"]+=1
            if s1<=threshold:
                assert f==43 and run%2==1 and w&3==0
                assert (s0,threshold)==(791,659)
                step=trace_certificate(n,number,a,f,run)
                flagged.append(n)
                descents[step]+=1
        elif s1>threshold:
            counts["inverse"]+=1

def dfs(state, counts, flagged, descents):
    i,base,f,number,flag,run=state
    if not eligible(*state):
        return
    if i==66:
        finish_root(state,counts,flagged,descents)
        return
    for bit in (0,1):
        nxt=source_child(*state,bit)
        if nxt is not None:
            dfs(nxt,counts,flagged,descents)

def prefix_state():
    state=(2,3,2,9,0,0)
    for i in range(2,K):
        assert state[0]==i and eligible(*state)
        state=source_child(*state, (LOW>>i)&1)
        assert state is not None
    assert state==(48,163665130792219,33,3232345501328340,0,2)
    return state

def brute_root(root):
    # Direct enumeration of every one of 2^18 roots, without the DFS/prefix shortcut.
    state=(2,3,2,9,0,0)
    while eligible(*state):
        i=state[0]
        if i==66:
            return state
        state=source_child(*state,(root>>i)&1)
        if state is None:
            return None
    return None

def main():
    counts=Counter()
    bad=[]
    descents=Counter()
    dfs(prefix_state(),counts,bad,descents)
    expected=dict(root=105742,interval=870591,admitted=456289,
                  bitmap=456203,source_clear=338468,inverse=15)
    assert dict(counts)==expected,(counts,expected)
    assert len(bad)==167 and N in bad
    assert sum(descents.values())==167 and max(descents)==181 and min(descents)==91
    digest=sha256(("\n".join(map(str,sorted(bad)))+"\n").encode()).hexdigest()
    assert digest==EXPECTED_DIGEST,digest
    print(f"R40_CYLINDER_PASS roots={counts['root']} interval={counts['interval']} admitted={counts['admitted']} bitmap={counts['bitmap']} false_clear={len(bad)} inverse={counts['inverse']} max_descent={max(descents)} digest={digest}")
    independent_roots=0
    for j in range(1<<(66-K)):
        root=LOW+(j<<K)
        s=brute_root(root)
        if s is not None:
            assert s[0]==66 and s[1]==root
            independent_roots+=1
    assert independent_roots==counts["root"]==105742
    print(f"R40_DIRECT_ROOT_ORACLE_PASS tested_roots={1<<(66-K)} surviving_roots={independent_roots}")

if __name__=="__main__":
    main()
