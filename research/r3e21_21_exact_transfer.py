#!/usr/bin/env python3
"""CEML R3E21-21 research-only exact interval/carry transfer; NO orbit-to-one jobs."""
from collections import Counter, defaultdict
from itertools import product
from functools import lru_cache
B=2392518188130438742016
E=3000000000000000000000  # exclusive
M=729
OFFICIAL=326865589733606241
T=lambda x: (3*x+1)//2 if x&1 else x//2
GATES=((3,2,1,2),(9,4,5,8),(81,64,73,10),(243,128,211,182),(729,512,809,433))

def roots_and_U():
    live=[True]
    for j in range(1,13):
        nxt=[]; seen=set()
        for r in range(1<<j):
            x,s=r,0
            for _ in range(j): s+=x&1; x=T(x)
            key=s,x
            dead=key in seen or (3**s<2**j and 3**s-2**j<r-x)
            seen.add(key); nxt.append(live[r%len(live)] and not dead)
        live=nxt
    roots=[r for r in range(4096) if live[r]]
    byphase=defaultdict(list); templates=0
    for h in range(1,10):
        for bits in product((0,1),repeat=h):
            a=sum(bits)
            if not(1<=a<=6 and 2**h<3**a): continue
            c=0
            for i,b in enumerate(bits):
                if b:c=3*c+2**i
            t0=c*pow(2**h,-1,3**a)%(3**a)
            for t in range(t0,M,3**a):byphase[t].append((h,a,c))
            templates+=1
    assert (len(roots),templates)==(182,179)
    masks={}
    for r in roots:
        x,s,c=r,0,0; prefixes=[]
        for j in range(1,13):
            if x&1:s+=1;c=3*c+2**(j-1)
            x=T(x);prefixes.append((j,s,c))
        allowed=set()
        for t in range(M):
            if t in byphase:continue
            forbidden=False
            for j,s,c in prefixes:
                y=(3**s*t+c)*pow(2**j,-1,M)%M
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

def ceildiv(a,b):return -(-a//b)

def linear_keep(lo,hi,a,d):
    """Intersect q in [lo,hi) with a+d*q>=0, using exact signed arithmetic."""
    if d>0:lo=max(lo,ceildiv(-a,d))
    elif d<0:hi=min(hi,a//(-d)+1)
    elif a<0:return 0,0
    return lo,max(lo,hi)

@lru_cache(None)
def phase_table(j,Ut):
    U=set(Ut); d=(1<<j)%M
    bits=[int(k*d%M in U) for k in range(2*M)]
    pref=[0]
    for v in bits:pref.append(pref[-1]+v)
    return pow(d,-1,M),pref

def count_phase(a,j,lo,hi,U):
    """Exact CRT cyclic count, never replacing inputs by a density."""
    N=hi-lo
    if N<=0:return 0
    q,r=divmod(N,M)
    inv,pref=phase_table(j,tuple(sorted(U)))
    f=(a+(lo<<j))%M; k0=f*inv%M
    return q*len(U)+pref[k0+r]-pref[k0]

def cell(r):
    a=B+(r-B)%4096
    hi=ceildiv(E-a,4096)
    x=a;s=0
    for _ in range(12):s+=x&1;x=T(x)
    return (12,a,x,s,0,hi)

def advance(z,b,with_q6=True):
    """True cell (j,a,y,s,lo,hi): n=a+2^j*q, T^j(n)=y+3^s*q.
    Splitting q by true parity yields one child without approximation."""
    j,a,y,s,lo,hi=z
    k=(b-(y&1))&1
    L=ceildiv(lo-k,2); R=ceildiv(hi-k,2)
    if L>=R:return None
    aa=a+(k<<j); yy=T(y+3**s*k);ss=s+b; jj=j+1
    # Exact initial-to-current no-descent test, including signed high-bit carry.
    L,R=linear_keep(L,R,yy-aa,3**ss-2**jj)
    if L>=R:return None
    for den,mul,offset,residue in GATES if with_q6 else GATES[:4]:
        if yy%den!=residue:continue
        numer0=mul*yy-offset
        assert numer0%den==0 and mul*3**ss%den==0
        p0=numer0//den; d=mul*3**ss//den
        assert p0+d*L>0  # in this large-positive test range
        # Keep precisely when no strictly smaller positive predecessor exists.
        L,R=linear_keep(L,R,p0-aa,d-2**jj)
        if L>=R:return None
    return (jj,aa,yy,ss,L,R)

def exact_depth(roots,U,depth=20):
    cs=[cell(r) for r in roots]
    hist=[]
    for j in range(12,depth+1):
        actual=sum(count_phase(a,j,lo,hi,U) for _,a,y,s,lo,hi in cs)
        hist.append((j,len(cs),actual))
        if j<depth:
            cs=[v for z in cs for b in (0,1) if (v:=advance(z,b)) is not None]
    return hist,cs

def prefix_oracle(n,root_set,U,depth=20):
    if n%4096 not in root_set or n%M not in U:return False
    x=n
    for j in range(1,depth+1):
        x=T(x)
        if j<=12:continue
        if x<n:return False
        for den,mul,offset,res in GATES:
            if x%den==res:
                p=(mul*x-offset)//den
                if 0<p<n:return False
    return True

def collision(roots,U,depth=20):
    seen={}
    for r0 in roots:
        for tail in range(1<<(depth-12)):
            r=r0+(tail<<12)
            x=r;s=0;c=0
            for j in range(depth):
                bit=x&1;s+=bit
                if bit:c=3*c+2**j
                x=T(x)
            a=B+(r-B)%(1<<depth)
            N=ceildiv(E-a,1<<depth)
            if N<=0:continue
            count=count_phase(a,depth,0,N,U)
            key=(s,c%M)
            if key in seen and seen[key][2]!=count:
                return key,seen[key],(r,a,count)
            seen[key]=(r,a,count)
    raise AssertionError('no collision found')

def endpoint_collision(U):
    # Same (j,s,C mod 729); right EXCLUSIVE endpoint gives different lengths.
    j=22; out=[]
    for r in (1253403,2097179):
        x=r;s=0;c=0
        for t in range(j):
            b=x&1;s+=b
            if b:c=3*c+(1<<t)
            x=T(x)
        a=B+(r-B)%(1<<j);N=ceildiv(E-a,1<<j)
        out.append((r,(s,c%M),N,count_phase(a,j,0,N,U)))
    assert out[0][1]==out[1][1]==(16,559)
    assert (out[0][2]-out[1][2],out[0][3]-out[1][3])==(1,1)
    return out

def adversarial_windows():
    out=[]
    for j in (20,32):
        rows=[]
        for off in (0,256,512,768,1024,2048,3072):
            no_descent=0
            for n in range(B+off,B+off+256):
                x=n;stable=True
                for _ in range(j):
                    x=T(x)
                    if x<n:stable=False
                no_descent+=stable
            rows.append((off,no_descent))
        out.append((j,rows))
    return out

def main():
    roots,U=roots_and_U();rs=set(roots)
    hist,cs=exact_depth(roots,U)
    assert hist[0][1]==144 and hist[-1][1]<=144*256
    # Independent exact large-number oracle: small bounded prefix, no orbit to one.
    cells_by_residue={a%(1<<20):z for z in cs for j,a,y,s,lo,hi in (z,)}
    assert len(cells_by_residue)==len(cs)
    for n in range(B,B+40000):
        z=cells_by_residue.get(n%(1<<20))
        symbolic=False
        if z:
            j,a,y,s,lo,hi=z
            q=(n-a)//(1<<j)
            symbolic=lo<=q<hi and n%M in U
        assert symbolic==prefix_oracle(n,rs,U),('oracle mismatch',n)
    pair=collision(roots,U)
    assert pair[1][2]!=pair[2][2]
    print('PASS R3E21-21 roots/U',len(roots),len(U),'templates 179')
    for row in hist:print('EXACT_CELL j count exact_surviving',*row)
    print('PASS 40000 independent genuine signed-prefix checks, no orbit to one')
    print('SAME_COMPRESSED_STATE_DIFFERENT_PHASE_COUNTS',pair)
    print('DIFFERENT_ENDPOINT_LENGTHS_AT_J22',endpoint_collision(U))
    print('CORRELATED_BLOCK_WINDOW_COUNTS',adversarial_windows())
    print('UNCHANGED OFFICIAL CONDITIONAL UPPER',OFFICIAL)

if __name__=='__main__':main()
