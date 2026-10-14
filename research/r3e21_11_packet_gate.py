"""R3E21-11: bounded k=4/k=5 packet truth gate; NEVER a production worker.

Run from repo root:
    python research/r3e21_11_packet_gate.py

Imports inherited research-only modules. No science, complete trajectories,
full-[B,E) 72-depth global calculation, or local operator interaction.
"""
from r3e21_8_transfer import B,E,M,J,T,span,roots_and_mask
from r3e21_9_carry import CoherentTransfer
from r3e21_10_packed import packed_transfer,profiles

DEPTH=20
WINDOWS=((B+1,B+14),(B+12345,B+12845),
         (B+9999,B+9999+(1<<17)+17),
         (E-3*(1<<16)-77,E-13))
EXPECTED=(
    (0,0,0,0,0),
    (16,3,8,8,8),
    (4609,1351,1886,1847,1847),
    (6914,2040,2662,2662,2613),
)

def direct_state(base,child_bound,k,d,s,N,t,words):
    """Quadratic orientation-by-index oracle, independently of convolution."""
    if N<=0 or 3**s<2**d:
        return 0
    count=base.exact(d,N,t)
    if count==0 or N==1 or d==base.depth:
        return count
    if d+k>base.depth:
        return base.pair(d,s,N,t)
    L=1<<k
    g=pow(3,s,L)
    best=0
    for y in range(L):
        subtotal=0
        for i in range(L):
            ni=(N+L-1-i)//L
            if not ni:
                continue
            word=words[(y+g*i)%L]
            if any(3**(s+v)<2**(d+j) for j,v in enumerate(word,1)):
                continue
            subtotal+=child_bound(d+k,s+word[-1],ni,
                                  (t+i*base.step[d])%M)
        best=max(best,subtotal)
    return min(count,best)

def prefix20(n):
    s=0
    for j in range(1,21):
        s+=n&1
        n=T(n)
        if 3**s<2**j:
            return False
    return True

def carry_orbit(active):
    assert (27,9) in active
    first,_=span(B,E,J,27)
    assert first==2392518188130438742043
    assert first%M==104
    y=first
    for _ in range(J):
        y=T(y)
    got=[]
    for h in range(32):
        n=first+((1<<J)*M)*h
        z=n
        for _ in range(J):
            z=T(z)
        assert B<=n<E
        assert n%(1<<J)==27 and n%M==104
        assert z==y+3**9*M*h
        got.append(z%32)
    assert got==[(9+11*h)%32 for h in range(32)]
    assert len(set(got))==32
    return len(got)

def run():
    active,mask=roots_and_mask()
    assert len(active)==144 and sum(mask)==394
    carry_count=carry_orbit(active)
    base=CoherentTransfer(mask,DEPTH)
    qs={k:packed_transfer(base,k) for k in (3,4,5)}
    states=0
    for k in (4,5):
        words=profiles(k)
        count=0
        for d in (11,12,13,14,15,16,19,20):
            for s in range(d+1):
                for N in (0,1,2,3,4,5,7,8,9,15,16,17,18,19,31,32,33,40):
                    for t in (0,1,91,728):
                        fast=qs[k](d,s,N,t)
                        slow=direct_state(base,qs[k],k,d,s,N,t,words)
                        assert fast==slow,(k,d,s,N,t,fast,slow)
                        count+=1
        assert count==9216
        states+=count

    rows=[]
    for start,end in WINDOWS:
        points=truth=0
        values={k:0 for k in qs}
        for r,s in active:
            first,N=span(start,end,J,r)
            points+=N
            for k,q in qs.items():
                values[k]+=q(J,s,N,first%M)
            for n in range(first,end,1<<J):
                if mask[n%M] and prefix20(n):
                    truth+=1
        row=(points,truth,values[3],values[4],values[5])
        assert truth<=min(values.values()),(start,end,row)
        rows.append(row)
    assert tuple(rows)==EXPECTED,(rows,EXPECTED)
    total=[sum(row[i] for row in rows) for i in range(5)]
    assert total==[11539,3394,4556,4517,4468]
    print("PASS bounded R3E21-11; roots=144; U=394/729")
    print("carry orientations:",carry_count,
          "quadratic-vs-packed states:",states)
    print("windows (points,truth,Q3,Q4,Q5):",rows)
    print("totals:",total,"local Q3-Q5 upper improvement:",88)
    print("GLOBAL depth-72 upper NOT recomputed; no new global claim")

if __name__=="__main__":
    run()
