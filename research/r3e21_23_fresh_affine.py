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

def inverse_nonclosure():
    x=303;w=[];s=c=0
    for j in range(9):
        bit=x&1;w.append(bit);s+=bit
        if bit:c=3*c+2**j
        x=T(x)
    assert (x,s,c)==(433,6,809)
    assert w==[1,1,1,1,0,1,0,1,0]
    # All y=433+729*t have a true p=303+512*t, not one source first gate.
    for t in (0,1,2,9,10000):
        p=303+512*t;y=433+729*t
        assert 0<p<y and all(y%mod!=res for _,_,mod,res,_ in PRIMS)
        z=p;bits=[]
        for j in range(9):
            bits.append(z&1);z=T(z)
        assert z==y and bits==w
    assert [433%mod for _,_,mod,_,_ in PRIMS]==[1,1,28,190]
    # Exact signed high-base inequality for p(y)=(512*y-809)/729.
    high=(0,0,0);low=(0,0,0)
    for j in range(J,D+1):
        for s in range(6,j+1):
            Cmax=2**(j-s)*(3**s-2**s)
            delta=729*2**j-512*3**s
            if delta>0:
                threshold=max(0,(512*Cmax-809*2**j)//delta+1)
                if threshold>high[0]:high=(threshold,j,s)
            elif delta<0:
                threshold=809*2**j//(-delta)+1
                if threshold>low[0]:low=(threshold,j,s)
    assert high==(486401988,71,45)
    assert low==(82,28,18)
    assert B>max(high[0],low[0])
    assert 3**47>2**72
    assert all(2**t*3**47>3**a*2**72 for t,a,*_ in PRIMS)
    assert 4*3**47>9*2**72
    return ''.join('O' if b else 'E' for b in w),high,low

def root_state(r):
    x,s,c=r,0,0
    for j in range(J):
        if x&1:s+=1;c=3*c+(1<<j)
        x=T(x)
    assert s>=8
    return s,c%MOD

def weight(k,U):
    """True all-endpoint cyclic CRT lower for any depth-k cylinder."""
    N=(E-B)//(1<<k);q,r=divmod(N,MOD)
    stride=pow(2,k,MOD)
    ring=[int(i*stride%MOD in U) for i in range(MOD)]*2
    v=sum(ring[:r]);mn=v
    for i in range(1,MOD):
        v+=ring[i+r-1]-ring[i-1];mn=min(mn,v)
    if k>=60:
        assert mn==min(sum((a+i*stride)%MOD in U for i in range(r)) for a in range(MOD))
    return q*len(U)+mn

def child(j,s,c,hit,bit):
    jj=j+1;ss=s+bit
    if 3**ss<2**jj:return None
    cc=(3*c+(1<<j))%MOD if bit else c
    y=cc*pow(2**jj,-1,MOD)%MOD
    # Reject every prior certified h1, h2, P3 or P4 inverse slope hit.
    if y%3==2 and 2*3**ss<3*2**jj:return None
    if y%9==8 and 4*3**ss<9*2**jj:return None
    if y%81==10 and 64*3**ss<81*2**jj:return None
    if y%243==182 and 128*3**ss<243*2**jj:return None
    if y==433 and 512*3**ss<729*2**jj:hit=True
    return ss,cc,hit

def count_cover(roots,U):
    weights=[weight(j,U) for j in range(K+1)]
    frontier=Counter((*root_state(r),False) for r in roots)
    hist=Counter()
    for j in range(J,K+1):
        nxt=Counter()
        for (s,c,hit),mult in frontier.items():
            if hit and s>=47:
                hist[j]+=mult
                continue
            if j==K:continue
            for b in (0,1):
                z=child(j,s,c,hit,b)
                if z is not None:nxt[z]+=mult
        frontier=nxt
    forward=sum(mult*weights[j] for j,mult in hist.items())
    # Completely separate backward stop-or-follow optimization.
    @lru_cache(None)
    def V(j,s,c,hit):
        stop=weights[j] if hit and s>=47 else 0
        if j==K:return stop
        follow=sum(V(j+1,*z) for b in (0,1)
                   if (z:=child(j,s,c,hit,b)) is not None)
        return max(stop,follow)
    backward=sum(V(J,*root_state(r),False) for r in roots)
    assert forward==backward==10905604613006
    assert sum(hist.values())==5007697793933
    assert dict(sorted(hist.items()))=={
        53:5,54:183,55:3452,56:44715,57:444970,58:3615408,
        59:24959993,60:150717839,61:813301404,62:3985167231,
        63:17948960651,64:74811820363,65:289742018391,
        66:1048307318233,67:3571909421095}
    print("PASS independent forward/memoized antichain count",forward,
          "memo_states",V.cache_info().currsize)
    print("PASS depth histogram",sorted(hist.items()))
    print("CONDITIONAL NEW UPPER",OLD_UPPER-forward)
    return forward

def bounded_truth(roots,U):
    roots=set(roots);eligible=0;new_offsets=[]
    for n in range(B,B+350000):
        if n%4096 not in roots or n%729 not in U:continue
        x=n;s=0;hit=False;bad=False
        for j in range(1,73):
            s+=x&1;x=T(x)
            if 3**s<2**j:bad=True;break
            if j<=12:continue
            if x%3==2 and 0<(2*x-1)//3<n:bad=True;break
            if x%9==8 and 0<(4*x-5)//9<n:bad=True;break
            for t,a,m,res,H in (PRIMS[2],PRIMS[3]):
                if x%m==res and 0<(2**t*x-H)//3**a<n:
                    bad=True;break
            if bad:break
            if x%729==433:
                p=(512*x-809)//729
                if 0<p<n:
                    z=p
                    for _ in range(9):z=T(z)
                    assert z==x
                    hit=True
        if not bad:
            eligible+=1
            if hit:new_offsets.append(n-B)
    assert eligible==113 and new_offsets==[143519]
    n=B+143519;x=n;s=0;hits=[]
    for j in range(1,73):
        s+=x&1;x=T(x)
        if j>12 and x%729==433 and 512*3**s<729*2**j:
            p=(512*x-809)//729
            if 0<p<n:
                z=p
                for _ in range(9):z=T(z)
                assert z==x
                hits.append((j,s,x,p))
    assert hits==[(60,38,2803258757066889700603,1968818221698556278063)]
    print("PASS true 72-prefix old+prior-disjoint",eligible,
          "new witness n",n,"at",hits)


# R3E21-23 additional independent family: nine true steps, six odd,
# final step even; choose largest affine carry for any duplicate residue.
R3_OLD=330156319374735841
R3_CONSUMED=(3007471253458601,220259463699144,52093319358849,10905604613006)
R3_PRIOR=R3_OLD-sum(R3_CONSUMED)
R3_GATES=((3,2,1,1,1),(9,8,5,2,2),(9,4,5,3,2),
          (81,10,73,6,4),(243,182,211,7,5),(729,433,809,9,6))
assert R3_PRIOR==326865589733606241
assert 3**47>2**72
assert all(2**t*3**47>3**a*2**72 for _,_,_,t,a in R3_GATES)

def r3_words():
    d={}
    for bits in product((0,1),repeat=9):
        if bits[-1] or sum(bits)!=6:continue
        c=0
        for i,b in enumerate(bits):
            if b:c=3*c+(1<<i)
        r=c*pow(512,-1,MOD)%MOD
        y=r+729*3
        p=(512*y-c)//729
        assert 0<p<y and (512*y-c)%729==0
        x=p;got=[]
        for _ in range(9):
            got.append(x&1);x=T(x)
        assert x==y and tuple(got)==bits
        if r not in d or c>d[r][1]:d[r]=(bits,c)
    assert len(d)==22 and 433 in d
    return d

R3_TWO=[1<<j for j in range(73)]
R3_THREE=[3**j for j in range(73)]
R3_INV=[pow(1<<j,-1,MOD) for j in range(73)]

def r3_child(j,s,c,hit,b,R):
    jj=j+1; ss=s+b
    if R3_THREE[ss]<R3_TWO[jj]:return None
    cc=(3*c+R3_TWO[j])%MOD if b else c
    y=cc*R3_INV[jj]%MOD
    for den,res,H,t,a in R3_GATES:
        if y%den==res and 2**t*R3_THREE[ss]<3**a*R3_TWO[jj]:
            return None
    newhit=hit or (y in R and 512*R3_THREE[ss]<729*R3_TWO[jj])
    return (ss,cc,newhit)

def r3_signed_threshold(R):
    worst=(0,None)
    for r,(bits,H) in R.items():
        for j in range(13,73):
            for s in range(8,j+1):
                d=729*R3_TWO[j]-512*R3_THREE[s]
                if d<=0:continue
                Cmax=2**(j-s)*(R3_THREE[s]-2**s)
                threshold=max(0,(512*Cmax-H*R3_TWO[j])//d+1)
                if threshold>worst[0]:worst=(threshold,(r,j,s))
    assert worst==(486401989,(524,71,45)) and B>worst[0]
    return worst

def r3_count(roots,U,R):
    wk={j:weight(j,U) for j in range(12,68)}
    front=Counter((*root_state(r),False) for r in roots)
    hist=Counter()
    for j in range(12,68):
        nxt=Counter()
        for (s,c,hit),multiplicity in front.items():
            if hit and s>=47:
                hist[j]+=multiplicity
                continue
            if j==67:continue
            for bit in (0,1):
                z=r3_child(j,s,c,hit,bit,R)
                if z is not None:nxt[z]+=multiplicity
        front=nxt
    lower=sum(v*wk[j] for j,v in hist.items())
    @lru_cache(None)
    def back(j,s,c,hit):
        if hit and s>=47:return (wk[j],1)
        if j==67:return (0,0)
        amt=leaves=0
        for bit in (0,1):
            z=r3_child(j,s,c,hit,bit,R)
            if z is not None:
                a,n=back(j+1,*z)
                amt+=a;leaves+=n
        return amt,leaves
    backward=0; backward_leaves=0
    for r in roots:
        a,n=back(12,*root_state(r),False)
        backward+=a;backward_leaves+=n
    count=sum(hist.values())
    assert (lower,count)==(backward,backward_leaves)
    gross_lower=sum(v*((E-B)//(1<<j)) for j,v in hist.items())
    gross_upper=sum(v*(((E-B)+(1<<j)-1)//(1<<j)) for j,v in hist.items())
    print("forward_backward",lower,count,back.cache_info().currsize)
    print("gross_bounds_without_U",gross_lower,gross_upper)
    print("stops",sorted(hist.items()))
    return lower,hist

def r3_bounded_oracle(roots,U,R,N=350000):
    eligible=hit_count=0
    rs=set(roots)
    for n in range(B,B+N):
        if n%4096 not in rs or n%729 not in U:continue
        x=n;bad=False;new=False
        for j in range(1,73):
            x=T(x)
            if x<n:bad=True;break
            if j<=12:continue
            for den,res,H,t,a in R3_GATES:
                if x%den==res:
                    p=((1<<t)*x-H)//3**a
                    if 0<p<n:bad=True;break
            if bad:break
            if x%729 in R:
                bits,H=R[x%729]
                p=(512*x-H)//729
                if 0<p<n:
                    z=p;observed=[]
                    for _ in range(9):
                        observed.append(z&1);z=T(z)
                    assert z==x and tuple(observed)==bits
                    new=True
        if not bad:
            eligible+=1
            if new:hit_count+=1
    assert (eligible,hit_count)==(112,0)
    print("bounded_350000_true_oracle",eligible,hit_count)

def r3_witness(roots,U,R):
    n=2392531586096650219611
    assert B<=n<E and n%4096 in roots and n%729 in U
    x=n;odd=0;hits=[];stopped=None
    for j in range(1,73):
        odd+=x&1;x=T(x)
        assert x>=n
        if j<=12:continue
        for den,res,H,t,a in R3_GATES:
            if x%den==res:
                p=((1<<t)*x-H)//3**a
                assert not 0<p<n
        if x%729 in R:
            bits,H=R[x%729]
            p=(512*x-H)//729
            if 0<p<n:
                z=p;observed=[]
                for _ in range(9):
                    observed.append(z&1);z=T(z)
                assert z==x and tuple(observed)==bits
                hits.append((j,odd,x,p,x%729))
        if stopped is None and hits and odd>=47:stopped=j
    assert stopped==53
    assert (17,11,3233564703996759769087,2271035841490179700647,604) in hits
    print("authentic_22_digit_witness",n,"stop",stopped,"hits",hits[:4])

def main_r3e21_23():
    roots,U=roots_mask()
    assert len(roots)==144 and len(U)==394
    words=r3_words()
    R={r:w for r,w in words.items() if r!=433}
    assert len(R)==21
    print("new_residues",sorted(R))
    print("signed_threshold",r3_signed_threshold(R))
    lower,hist=r3_count(roots,U,R)
    assert lower==21708672114515 and sum(hist.values())==10387180339353
    alias,_=r3_count(roots,U,{433:words[433]})
    assert alias==0
    r3_bounded_oracle(roots,U,R)
    r3_witness(roots,U,R)
    print("NEW_CONDITIONAL_UPPER",R3_PRIOR-lower)
    assert R3_PRIOR-lower==326843881061491726
    print("PASS R3E21-23 RESEARCH ONLY")

if __name__=="__main__":main_r3e21_23()
