#!/usr/bin/env python3
"""R3E21-19 finite-saturation no-go; exact research arithmetic, no scientific Collatz-to-one run."""
from collections import Counter, defaultdict
from itertools import product
from functools import lru_cache
B=2392518188130438742016
E=3000000000000000000000
W=E-B
J,D,K,MOD=12,72,67,729
CURRENT_UPPER=326865589733606241

def T(n):
    return (3*n+1)//2 if n&1 else n//2

def roots_mask():
    """Independently reconstruct inherited J12, 179 templates and 394/729 U."""
    live=[True]
    for j in range(1,J+1):
        nxt=[];seen=set()
        for r in range(1<<j):
            x,s=r,0
            for _ in range(j):
                s+=x&1;x=T(x)
            key=(s,x)
            dead=key in seen or (3**s<2**j and 3**s-2**j<r-x)
            seen.add(key)
            nxt.append(live[r%len(live)] and not dead)
        live=nxt
    roots=[r for r in range(1<<J) if live[r]]
    assert len(roots)==182
    byphase=defaultdict(list);ntemplates=0
    for h in range(1,10):
        for bits in product((0,1),repeat=h):
            a=sum(bits)
            if not (1<=a<=6 and 2**h<3**a):continue
            c=0
            for i,b in enumerate(bits):
                if b:c=3*c+2**i
            t0=c*pow(2**h,-1,3**a)%(3**a)
            for t in range(t0,MOD,3**a):byphase[t].append((h,a,c))
            ntemplates+=1
    assert (ntemplates,len(byphase))==(179,335)
    masks={}
    for r in roots:
        x,s,c,prefixes=r,0,0,[]
        for j in range(1,J+1):
            if x&1:s+=1;c=3*c+2**(j-1)
            x=T(x);prefixes.append((j,s,c))
        allowed=set()
        for t in range(MOD):
            if t in byphase:continue
            forbidden=False
            for j,s,c in prefixes:
                y=(3**s*t+c)*pow(2**j,-1,MOD)%MOD
                for h,a,v in byphase.get(y,()):
                    coeff=2**h*3**s-3**a*2**j
                    off=2**h*c-2**j*v
                    if coeff<=0 and coeff*B+off<0 and 2**h*3**s*B+off>0:
                        forbidden=True;break
                if forbidden:break
            if not forbidden:allowed.add(t)
        masks[r]=frozenset(allowed)
    assert Counter(map(len,masks.values()))=={394:144,0:38}
    nonempty={m for m in masks.values() if m}
    assert len(nonempty)==1
    return [r for r in roots if masks[r]],next(iter(nonempty))

def root_state(r):
    x,s,c=r,0,0
    for j in range(J):
        if x&1:s+=1;c=3*c+(1<<j)
        x=T(x)
    assert s>=8
    return s,c%MOD


# New ceiling counts every prior-admissible parity cylinder which FIRST reaches
# s>=47 by depth67, regardless of whether ANY fresh inverse witness exists.
# This is deliberately a MAXIMUM-POWER / ORACLE model, not a new sieve.
def admissible_child(j,s,c,b):
    jj=j+1; ss=s+b
    if 3**ss<2**jj:return None
    cc=(3*c+2**j)%MOD if b else c
    y=cc*pow(2**jj,-1,MOD)%MOD
    if y%3==2 and 2*3**ss<3*2**jj:return None
    if y%9==8 and 4*3**ss<9*2**jj:return None
    if y%81==10 and 64*3**ss<81*2**jj:return None
    if y%243==182 and 128*3**ss<243*2**jj:return None
    return ss,cc

def universal_cylinder_upper(k,U):
    # Every k-cylinder in the nonaligned [B,E) has N or N+1 points;
    # consecutive elements traverse one cyclic residue orbit modulo 729.
    N=W//(1<<k); q,r=divmod(N,MOD)
    stride=pow(2,k,MOD)
    ring=[int(i*stride%MOD in U) for i in range(MOD)]*2
    v=sum(ring[:r]); mx=v
    for a in range(1,MOD):
        v+=ring[a+r-1]-ring[a-1]
        mx=max(mx,v)
    return q*len(U)+mx+1

def exact_prefix_spotcheck(roots,U):
    # True signed 22-digit T-prefixes independently confront symbolic gates.
    # Construct 4608 explicit low-bit cylinders and an input phase in U.
    for r in roots:
        for suffix in range(32):
            low=r+(suffix<<J)
            n=B+(low-B)%(1<<17)
            for _ in range(MOD):
                if n%MOD in U:break
                n+=(1<<17)
            assert B<=n<E and n%(1<<17)==low and n%MOD in U
            x=n;s=0;c=0
            for j in range(1,18):
                bit=x&1;s+=bit
                if bit:c=3*c+2**(j-1)
                x=T(x)
                if j>=J:
                    assert x%MOD==(c*pow(2**j,-1,MOD))%MOD
                if j>J:
                    ps=s-bit
                    pc=(c-2**(j-1))//3 if bit else c
                    prediction=admissible_child(j-1,ps,pc%MOD,bit)
                    forbidden=(x<n)
                    # Independent actual exact predecessors, not phase-only lookups.
                    for t,a,m,res,H in ((1,1,3,2,1),(2,2,9,8,5),
                                        (6,4,81,10,73),(7,5,243,182,211)):
                        if x%m==res and 0<(2**t*x-H)//(3**a)<n:
                            forbidden=True
                    assert (prediction is None)==forbidden
                    if prediction is not None:assert prediction==(s,c%MOD)
    return len(roots)*32

def main():
    roots,U=roots_mask()
    assert (len(roots),len(U))==(144,394)
    assert 3**47>2**72
    assert all(2**t*3**47>3**a*2**72 for t,a in
               ((1,1),(2,2),(3,2),(6,4),(7,5)))
    upperweight={j:universal_cylinder_upper(j,U) for j in range(J,K+1)}
    forward=Counter(root_state(r) for r in roots)
    histogram=Counter()
    for j in range(J,K+1):
        nxt=Counter()
        for (s,c),count in forward.items():
            if s>=47:
                histogram[j]+=count
                continue
            if j==K:continue
            for bit in (0,1):
                child=admissible_child(j,s,c,bit)
                if child is not None:nxt[child]+=count
        forward=nxt
    count=sum(histogram.values())
    cap=sum(v*upperweight[j] for j,v in histogram.items())
    gross=sum(v*((W+(1<<j)-1)//(1<<j)) for j,v in histogram.items())
    expected={
        47:1,48:45,49:1025,50:15785,51:185098,
        52:1763990,53:14235784,54:100071478,55:625428763,
        56:3529402099,57:18200971694,58:86593465771,
        59:382986329187,60:1584390774299,61:6161456074871,
        62:22614289247623,63:78580837327321,64:259083180924310,
        65:811526764882527,66:2415589448043344,67:6824092752144912}
    assert dict(histogram)==expected
    assert (count,cap,gross)==(10419725171289927,62289308018259707,
                                89547365280396712)
    # Independent memoised BACKWARD solution, no first-hit histogram reuse.
    @lru_cache(None)
    def back(j,s,c):
        if s>=47:return (1,upperweight[j])
        if j==K:return (0,0)
        ans=(0,0)
        for b in (0,1):
            z=admissible_child(j,s,c,b)
            if z is None:continue
            result=back(j+1,*z)
            ans=(ans[0]+result[0],ans[1]+result[1])
        return ans
    vals=[back(J,*root_state(r)) for r in roots]
    assert (sum(v[0] for v in vals),sum(v[1] for v in vals))==(count,cap)
    probes=exact_prefix_spotcheck(roots,U)
    required=CURRENT_UPPER-CURRENT_UPPER//10
    assert gross<required and cap<required
    print("PASS source-reconstructed roots 144; templates 179; mask |U|=394")
    print("PASS forward/backward high-saturation ceiling",count,cap,
          "memo_states",back.cache_info().currsize)
    print("PASS gross ceiling ignoring U",gross)
    print("PASS authenticated true-prefix samples",probes)
    print("PASS no-go: tenfold requires",required,"; available cap",cap)
    print("UNCHANGED conditional conservative upper",CURRENT_UPPER)

# Historical baseline entrypoint relocated to main20()


# ---- R3E21-20: NEW, independent fixed-depth envelope and exact renewal. ----
from math import comb

def step20(j,s,c,b,mode):
    z=admissible_child(j,s,c,b)
    if z is None: return None
    jj=j+1
    ss,cc=z
    y=cc*pow(2**jj,-1,MOD)%MOD
    if mode!='four' and y==433 and 512*3**ss<729*2**jj:
        return None
    if mode=='q6+p2' and y%9==4 and 8*3**ss<9*2**jj:
        return None
    return z

def envelope20(roots,U,mode):
    states=Counter(root_state(r) for r in roots)
    hist=[];p2_candidates=0
    for j in range(J,D+1):
        cylinders=sum(states.values())
        h=universal_cylinder_upper(j,U)
        hist.append((j,cylinders,h,cylinders*h,len(states)))
        if j==D:break
        next_states=Counter()
        for (s,c),multiplicity in states.items():
            for b in (0,1):
                z=step20(j,s,c,b,mode if mode!='q6+p2' else 'q6')
                if z is None:continue
                ss,cc=z; jj=j+1
                y=cc*pow(2**jj,-1,MOD)%MOD
                if y%9==4 and 8*3**ss<9*2**jj:
                    p2_candidates+=multiplicity
                    if mode=='q6+p2':continue
                next_states[z]+=multiplicity
        states=next_states
    return hist,p2_candidates

def exact_min_odd(j):
    return next(s for s in range(j+1) if (3*B+1)**s>=(2**j)*(B**s))

def shift_collapse_spotcheck():
    # P2's last true step must be even; its predecessor is identical to h2's.
    for y in range(4,20000,9):
        p=(8*y-5)//9
        z=2*y
        assert y%9==4 and z%9==8
        assert p==(4*z-5)//9
        assert T(p)>0 and T(T(p))==z and T(z)==y
        assert (2*y-1)%3 != 0

def main20():
    # Run inherited full independent forward/backward high-s ceiling and true-T checks.
    main()
    roots,U=roots_mask()
    rows4,p4=envelope20(roots,U,'four')
    rows6,p6=envelope20(roots,U,'q6')
    rowsP,pP=envelope20(roots,U,'q6+p2')
    best4=min(rows4,key=lambda x:x[3])
    best6=min(rows6,key=lambda x:x[3])
    assert best4==(63,9540579385237983,38,362542016639043354,8668)
    assert best6==(63,9524984305884588,38,361949403623614344,8667)
    assert rows6==rowsP and (p4,p6,pP)==(0,0,0)
    assert best6[3]>CURRENT_UPPER
    shift_collapse_spotcheck()
    print('R3E21-20 PASS: P2 exact h2 shift; all 729-phase endpoint upper bounds')
    print('R3E21-20 four best',best4,'Q6 best',best6,'P2 extra candidates',pP)
    for j,expected in ((72,46),(128,81),(160,101),(192,122),(256,162)):
        cutoff=exact_min_odd(j)
        assert cutoff==expected
        tail=sum(comb(j,s) for s in range(cutoff,j+1))
        print('R3E21-20 renewal',j,'min_odds',cutoff,'full-modulus tail_words',tail,
              'tail_density',format(tail/(1<<j),'.10g'))
    print('R3E21-20 UNCHANGED',CURRENT_UPPER)

if __name__=='__main__':
    main20()
