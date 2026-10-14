"""CEML-R3E21-9: two-bit coherent-orientation arithmetic transfer.
Research-only exact integers. Run: python research/r3e21_9_carry.py
Reuses (and reruns the independent checks of) the frozen R3E21-8
root reconstruction; NEW packet recurrence and its oracles are here.
Never import this as a production verifier.
"""
from functools import lru_cache
from r3e21_8_transfer import (B,E,M,J,D,T,Transfer,span,
    roots_and_mask,independent_fixtures)

PREVIOUS_PHASE=334199143141076940
PREVIOUS_ORIENTED=334199143141062522
COHERENT_PHASE=333316047379009407
COHERENT_ORIENTED=333316047378995972

class CoherentTransfer(Transfer):
    def __init__(self, mask, end_depth=D):
        super().__init__(mask, end_depth)
        @lru_cache(maxsize=None)
        def pair(d,s,N,t):
            # State describes all N integers first+i*2**d, with
            # common d-step parity prefix (odd count s) and t=first%729.
            if N<=0 or 3**s<2**d:
                return 0
            immediate=self.exact(d,N,t)
            if immediate==0 or N==1 or d==end_depth:
                return immediate
            if d+2>end_depth:
                a,b=(N+1)//2,N//2
                t1=(t+self.step[d])%M
                return min(immediate,max(
                    pair(d+1,s,a,t)+pair(d+1,s+1,b,t1),
                    pair(d+1,s+1,a,t)+pair(d+1,s,b,t1)))
            # T**d(first+i*2**d) = T**d(first)+3**s*i.
            # All four 2-step parity words are determined jointly by
            # y=T**d(first) mod4. Do NOT optimise each child separately.
            children=[((N+3-i)//4,(t+i*self.step[d])%M)
                      for i in range(4)]
            coeff=3 if s&1 else 1
            maximum=0
            for y in range(4):
                subtotal=0
                for i,(ni,ti) in enumerate(children):
                    if ni==0:
                        continue
                    v=(y+coeff*i)&3
                    e0=v&1
                    # A descending intermediate prefix is already dead.
                    if 3**(s+e0)<2**(d+1):
                        continue
                    e1=T(v)&1
                    subtotal+=pair(d+2,s+e0+e1,ni,ti)
                maximum=max(maximum,subtotal)
            return min(immediate,maximum)
        self.pair=pair

    def oriented_pair(self,d,s,first,N,known):
        if N<=0 or 3**s<2**d:
            return 0
        direct=self.exact(d,N,first%M)
        if not direct or N==1 or d==self.depth or known==0:
            return min(direct,self.pair(d,s,N,first%M))
        y=first
        for _ in range(d):
            y=T(y)
        orientation=y&1
        a,b=(N+1)//2,N//2
        children=(self.oriented_pair(d+1,s+orientation,first,a,known-1)
                  +self.oriented_pair(d+1,s+1-orientation,
                                      first+(1<<d),b,known-1))
        return min(direct,children)


def packet_oracles():
    # Independent direct Collatz parity at the input of all four
    # descendants. Includes numerical r away from the root, and
    # shifted/high-base representatives.
    cases=0
    for d in (1,3,12,13,20):
        L=1<<d
        for offset in (91,639,B+77,E-100007):
            for q in range(12):
                first=offset+q*L
                y=first
                s=0
                for _ in range(d):
                    s+=y&1
                    y=T(y)
                c=pow(3,s,4)
                for i in range(4):
                    z=first+i*L
                    for _ in range(d):
                        z=T(z)
                    assert z==y+3**s*i
                    v=(y+c*i)%4
                    assert (z&1)==(v&1)
                    assert (T(z)&1)==(T(v)&1)
                    cases+=1
    # The first parity alone is not a sufficient carry state.
    witnesses=[]
    for n in (639,6471):
        x=n;s=0
        for j in range(1,14):
            s+=x&1
            x=T(x)
            assert 3**s>=2**j
        witnesses.append((s,n%729,x&1,T(x)&1))
    assert witnesses==[(11,639,1,0),(11,639,1,1)]
    return cases


def direct_prefix_oracles(active, mask):
    # A completely separate per-integer test for K<=20. No orbits
    # to 1; these small windows are research fixtures only.
    p=CoherentTransfer(mask,20)
    windows=((B+1,B+14),(B+12345,B+12845),
             (B+9999,B+9999+(1<<17)+17),
             (E-3*(1<<16)-77,E-13))
    points=0
    for start,end in windows:
        certified=0;actual=0
        for r,s in active:
            first,N=span(start,end,J,r)
            certified+=p.pair(J,s,N,first%M)
            for i in range(N):
                n=first+(i<<J)
                assert start<=n<end and n%(1<<J)==r
                if not mask[n%M]:
                    continue
                x=n;odd=0;ok=True
                for j in range(1,21):
                    odd+=x&1
                    x=T(x)
                    if 3**odd<2**j:
                        ok=False;break
                actual+=int(ok)
            points+=N
        assert actual<=certified,(start,end,actual,certified)
    assert points==11539,points
    return points


def run():
    active,mask=roots_and_mask()
    # Previously published methods: independent 980 cyclic, 2000
    # signed interval/CRT, 11539 high-n direct-prefix witnesses.
    earlier=independent_fixtures(active,mask)
    assert earlier==(980,2000,11539),earlier
    parity_cases=packet_oracles()
    direct_cases=direct_prefix_oracles(active,mask)
    p=CoherentTransfer(mask)
    phase=old_oriented=coherent=coherent_oriented=0
    for r,s in active:
        first,N=span(B,E,J,r)
        phase+=p.transfer(J,s,N,first%M)
        old_oriented+=p.oriented(J,s,first,N,8)
        coherent+=p.pair(J,s,N,first%M)
        coherent_oriented+=p.oriented_pair(J,s,first,N,8)
    assert (phase,old_oriented)==(PREVIOUS_PHASE,PREVIOUS_ORIENTED)
    assert (coherent,coherent_oriented)==(COHERENT_PHASE,COHERENT_ORIENTED)
    assert coherent_oriented<=min(coherent,old_oriented)
    print('PASS CEML-R3E21-9; 144 roots; 394/729 mask')
    print('prior independent fixtures:',earlier,
          'two-bit parity oracles:',parity_cases,
          'independent K<=20 direct points:',direct_cases)
    print('R3E21-8 phase:',phase,'oriented8:',old_oriented)
    print('two-bit phase:',coherent,'two-bit+oriented8:',coherent_oriented)
    print('upper-bound saving:',old_oriented-coherent_oriented)
    print('cache:',p.pair.cache_info())

if __name__=='__main__':
    run()
