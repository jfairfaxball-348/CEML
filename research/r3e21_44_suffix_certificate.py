#!/usr/bin/env python3
"""R44 exact huge disjoint source-gated T^69<n family via 58+8-bit suffixes.
Research-only. Neither full bitmap nor global Collatz frontier certification.
"""
from collections import Counter, defaultdict
from hashlib import sha256

B,E,L,P = 2392518188130438742016,3000000000000000000000,1<<66,3**43
ALLOWED=frozenset((0,1,3,6,7))
OLD=(163665130792219,148957342012655,146557399178687,
     130677744459943,21359721993575,236955905271263,
     53319191503839,202396992200703,35120119522751)
EXPECTED_OLD=(121,26,125,125,74,52,125,121,74)
MIN_CERT=5
POW3=[3**i for i in range(67)]
POW2MOD9=[pow(2,i,9) for i in range(67)]

def eligible(i,f,q):
    return 306*i<485*f and not(q>=2 and q%2==0 and 306*(i-1)>=485*(f-1))

def src_transition(i,f,flag,q,num,bit):
    # Same integer search1 algebra, independently parameterized by ring input.
    x=num+bit*POW3[f]
    if ((num&1)==0)!=bool(bit):
        return f+1,(flag | int(306*(i+1)>=485*f))&~2,0,x+x//2
    if flag>=2:return None
    return f,flag<<1,q+1,x//2+1

def prefix_dp():
    states={(2,0,0):1}
    for i in range(2,58):
        nxt=defaultdict(int)
        for (f,flag,q),cnt in states.items():
            if not eligible(i,f,q):continue
            nxt[(f+1,(flag | int(306*(i+1)>=485*f))&~2,0)]+=cnt
            if flag<2:nxt[(f,flag<<1,q+1)]+=cnt
        states=nxt
    answer=states[(39,0,0)]
    assert eligible(58,39,0)
    assert answer==55114089659444
    return answer

def suffix(num0,suffix):
    """Suffix finite ring: at i keep lower (66-i+3) number bits.
    Terminal number mod 8 remains exact after all eight halvings.
    """
    f,flag,q,num=39,0,0,num0
    shift=0
    for i in range(58,66):
        bit=(suffix>>(i-58))&1
        shift=(shift+bit*POW2MOD9[i])%9
        state=src_transition(i,f,flag,q,num,bit)
        if state is None:return None
        f,flag,q,num=state
        num &= (1 << (66-i-1+3))-1
        if not eligible(i+1,f,q):return None
    if f!=43 or not (q&1) or flag!=0:return None
    a_residue=(3*(1-num))%8
    if a_residue==0:return None
    a=32+a_residue  # common valid lift 33,...,39, regardless of clipping
    assert (num-1+a*P)%8==0
    return (shift+a)%9,suffix,a

def phase_oracle():
    # 2048*256 exact 8-step suffix computations; all 9 root residues analytically.
    lowest=100;highest=0;total=0;probes=0;hist=Counter()
    for num in range(2048):
        terms=[]
        for s in range(256):
            probes+=1
            v=suffix(num,s)
            if v is not None:terms.append(v)
        for r9 in range(9):
            choices=[(s,a) for (shift,s,a) in terms if (r9+shift)%9 in ALLOWED]
            choices.sort()
            count=len(choices)
            hist[count]+=1;lowest=min(lowest,count);highest=max(highest,count);total+=count
            assert count>=5,(r9,num,count)
    assert probes==524288 and lowest==5 and highest==17 and total==206080
    assert hist=={5:49,6:90,7:485,8:1844,9:2509,10:1677,11:2914,
                  12:3744,13:2627,14:1269,15:747,16:416,17:61}
    return probes,lowest,highest,total,hist

def genuine_prefix(r):
    assert 0<=r<(1<<58) and r%4==3
    num,f,flag,q=9,2,0,0
    for i in range(2,58):
        if not eligible(i,f,q):return None
        nxt=src_transition(i,f,flag,q,num,(r>>i)&1)
        if nxt is None:return None
        f,flag,q,num=nxt
    if not eligible(58,f,q):return None
    return f,flag,q,num

def exclusion():
    vals=[]
    for low in OLD:
        c=0
        for j in range(1024):
            r=low+(j<<48)
            s=genuine_prefix(r)
            c+=int(s is not None and s[:3]==(39,0,0))
        vals.append(c)
    assert tuple(vals)==EXPECTED_OLD
    return sum(vals)

def original_T(z):return z//2 if z%2==0 else (3*z+1)//2

def make_witnesses():
    # Exact original integers; 69-step direct replays for first 25 viable prefixes.
    results=[];tried=0
    for r in range(3,(1<<58),4):
        tried+=1
        if r%(1<<48) in OLD:continue
        s=genuine_prefix(r)
        if s is None or s[:3]!=(39,0,0):continue
        phase=(r%9,s[3]%2048)
        choices=[]
        for suffixbits in range(256):
            v=suffix(phase[1],suffixbits)
            if v is not None and (phase[0]+v[0])%9 in ALLOWED:choices.append((suffixbits,v[2]))
        assert len(choices)>=5
        for suff,a in choices[:5]:
            root=r+(suff<<58);n=root+a*L
            assert B<=n<E and n%9 in ALLOWED
            z=n;odd=0;trail=0
            for i in range(1,70):
                if i<=66:
                    odd+=z&1;trail=0 if z&1 else trail+1
                z=original_T(z)
                if i==66:
                    assert odd==43 and trail%2==1 and z%8==0
                if i==69: assert z<n
            results.append(n)
        if len(results)>=125:break
    assert len(results)==125
    digest=sha256(('\n'.join(map(str,sorted(results)))+'\n').encode()).hexdigest()
    assert digest=='9466aa8a805c11ea60f7f0448ccd152941a25c54b21c8f8825529031c9a38518'
    return tried,digest,results[0]

def main():
    n=prefix_dp()
    probes,low,high,total,hist=phase_oracle()
    removed=exclusion();bound=MIN_CERT*(n-removed)
    assert removed==843 and bound==275570448293005
    tested,h,example=make_witnesses()
    assert tested==35328 and example==2733576887422834181503
    print('R44_PREFIX_DP_PASS i=58 f=39 flag=0 q=0 exact_prefixes=%d'%n)
    print('R44_SUFFIX_PHASE_PASS probes=%d phases=%d min=%d max=%d sum=%d histogram=%s'%(probes,9*2048,low,high,total,','.join('%d:%d'%k for k in sorted(hist.items()))))
    print('R44_DISJOINT_COUNT_PASS excluded_old_prefixes=%d remaining_prefixes=%d certified_per_prefix=%d new_original_starts=%d union_with_R43_R41=%d'%(removed,n-removed,MIN_CERT,bound,bound+96375))
    print('R44_LITERAL_T_PASS starts=125 prefix_search_probes=%d sha256=%s example=%d'%(tested,h,example))
if __name__=='__main__':main()
