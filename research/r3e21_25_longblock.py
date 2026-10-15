#!/usr/bin/env python3
"""R3E21-23: bounded self-contained nine-step affine reverse-family and
all-prior-disjoint CRT proof reproducer. Research only; no orbit to one.
Reconstructs old J12/729/179-template input mask from first principles.
"""
from collections import Counter, defaultdict
from itertools import product
from functools import lru_cache

B=2392518188130438742016
E=3000000000000000000000
J,D,K,MOD=12,72,67,729
OLD_UPPER=326876495338219247
PRIMS=((1,1,3,2,1),(3,2,9,4,5),(6,4,81,10,73),(7,5,243,182,211))

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


# R3E21-25 additive research-only bounded proof checker. The preceding
# J12/729 mask reconstruction is copied directly from the pinned R3E21-23
# reproducer so this file runs standalone. No scientific orbit-to-one run.
from math import comb
B25,E25=2392518188130438742016,3000000000000000000000
N25,P25=2392518855426464419611,2018687784266079354047
PRIOR25=((3,2,1,1,1),(9,8,5,2,2),(81,10,73,6,4),
         (243,182,211,7,5),(729,433,809,9,6))
def bits25(n,t):
    w=[]
    for _ in range(t):
        w.append(n&1);n=T(n)
    return n,tuple(w)
def carry25(w):
    H=0
    for i,b in enumerate(w):
        if b:H=3*H+(1<<i)
    return H
def r9_25():
    d={}
    for w in product((0,1),repeat=9):
        if w[-1] or sum(w)!=6:continue
        H=carry25(w);r=H*pow(512,-1,729)%729
        if r not in d or H>d[r]:d[r]=H
    assert len(d)==22 and d[433]==809
    return {r:H for r,H in d.items() if r!=433}
def groups25():
    groups=[]
    for t,a in ((10,7),(11,7),(11,8),(12,8)):
        d={}
        for w in product((0,1),repeat=t):
            if sum(w)!=a:continue
            H=carry25(w);r=H*pow(2**t,-1,3**a)%(3**a)
            if r not in d or H>d[r]:d[r]=H
        groups.append((t,a,d))
    assert [len(d) for t,a,d in groups]==[85,206,121,325]
    return groups
def eligible25(n,roots,U,r9,groups):
    # Conservative *all-prefix* rejection, not a query of unknown S_old.
    if n%4096 not in roots or n%729 not in U:return False,False,False
    x=n;s=0;hit=False;stopped=False
    for j in range(1,73):
        s+=x&1;x=T(x)
        if x<n:return False,False,False
        if j<=12:continue
        for mod,res,H,t,a in PRIOR25:
            if x%mod==res and 0<(2**t*x-H)//3**a<n:
                return False,False,False
        if x%729 in r9 and 0<(512*x-r9[x%729])//729<n:
            return False,False,False
        for t,a,d in groups:
            m=3**a
            if x%m in d and 0<(2**t*x-d[x%m])//m<n:hit=True
        if j<=67 and hit and s>=47:stopped=True
    return True,stopped,hit
def ceil25(a,b):return -((-a)//b)
def exact_no_descent25(L,R,depth):
    # State represents n=r+2**j q, T**j(n)=y+3**s q with q in [lo,hi).
    states=[(0,0,0,L,R)]
    for j in range(depth):
        nxt=[]
        for r,y,s,lo,hi in states:
            for bit in (0,1):
                k=(bit-y)&1
                rr=r+(1<<j)*k
                v=y+3**s*k
                assert (v&1)==bit
                yy=T(v) if v>0 else 0
                ss=s+bit
                a,b=ceil25(lo-k,2),ceil25(hi-k,2)
                slope=3**ss-(1<<(j+1))
                off=yy-rr
                if slope>0:a=max(a,ceil25(-off,slope))
                elif slope<0:b=min(b,(-off)//slope+1)
                elif off<0:continue
                if a<b:nxt.append((rr,yy,ss,a,b))
        states=nxt
        if not states:break
    return sum(hi-lo for _,_,_,lo,hi in states)
def direct_no_descent25(n,depth):
    x=n
    for _ in range(depth):
        x=T(x)
        if x<n:return False
    return True
def main25():
    assert E25-B25==607481811869561257984
    y,w=bits25(N25,15);z,v=bits25(P25,10)
    assert y==z==4311396664247964401663
    assert (sum(w),sum(v))==(10,7)
    assert (32768,27648)==(2**15,2**10*3**(10-7))
    qmax=(E25-1-N25)//32768
    assert qmax==18538853288987291
    for q in (0,1,2,1000,qmax):
        n=N25+32768*q;p=P25+27648*q
        yn,wn=bits25(n,15);yp,wp=bits25(p,10)
        assert B25<=n<E25 and 0<p<n and yn==yp==y+3**10*q
        assert wn==w and wp==v
    print("AFFINE_RAY_PASS",qmax+1,flush=True)
    roots,U=roots_mask();roots=set(roots)
    assert len(roots)==144 and len(U)==394 and N25%4096 in roots
    cycles,tail=divmod(qmax+1,729)
    input_gate=cycles*394+sum((N25+32768*q)%729 in U for q in range(tail))
    assert input_gate==10019627154816176
    print("EXACT_J12_U_RAY_INPUT_GATE",input_gate,flush=True)
    r9=r9_25();groups=groups25()
    counts=Counter();fresh=[]
    for q in range(1_000_000):
        state=eligible25(N25+32768*q,roots,U,r9,groups)
        counts[state]+=1
        if state==(True,False,True):fresh.append(q)
    assert counts[(False,False,False)]==997772
    assert counts[(True,True,True)]==379
    assert len(fresh)==counts[(True,False,True)]==1849
    assert fresh[:10]==[426,552,828,1952,2492,2688,3738,6080,6272,6362]
    assert fresh[-10:]==[995226,995880,996540,996864,997568,997968,998304,999336,999698,999792]
    for q in fresh:
        n=N25+32768*q;p=P25+27648*q
        yn,wn=bits25(n,15);yp,wp=bits25(p,10)
        assert 0<p<n<E25 and yn==yp and wn==w and wp==v
    print("EXACT_FRESH_FIRST_MILLION_PASS",len(fresh),
          "already_R24",counts[(True,True,True)],flush=True)
    L=B25+124000;R=L+2048
    for depth in (72,160,256):
        symbolic=exact_no_descent25(L,R,depth)
        direct=sum(direct_no_descent25(n,depth) for n in range(L,R))
        assert symbolic==direct
        assert symbolic==(4 if depth==72 else 0)
        print("EXACT_HIGH_BIT_TRANSFER_PASS",depth,symbolic,flush=True)
    assert E25-B25<2**256
    print("PASS_R3E21_25_RESEARCH_ONLY",flush=True)
if __name__=="__main__":main25()
