#!/usr/bin/env python3
"""R45: seven exact disjoint 58+8-bit classes; no global interval certification."""
from collections import Counter, defaultdict
from hashlib import sha256
import r3e21_44_suffix_certificate as r44

B,E,L,P=r44.B,r44.E,r44.L,r44.P
OLD,ALLOW=r44.OLD,r44.ALLOWED
CLASSES=(
 ((38,0,0),47500853814159,697,2,116480,((2,71),(3,752),(4,1483),(5,3506),(6,4117),(7,3971),(8,3169),(9,861),(10,502))),
 ((38,0,1),28882653731593,436,2,116480,((2,71),(3,752),(4,1483),(5,3506),(6,4117),(7,3971),(8,3169),(9,861),(10,502))),
 ((38,0,2),15078186832956,235,2,116480,((2,71),(3,752),(4,1483),(5,3506),(6,4117),(7,3971),(8,3169),(9,861),(10,502))),
 ((39,0,1),25876421228438,403,5,206080,((5,49),(6,90),(7,485),(8,1844),(9,2509),(10,1677),(11,2914),(12,3744),(13,2627),(14,1269),(15,747),(16,416),(17,61))),
 ((40,0,0),42926694229296,651,7,197120,((7,500),(8,1743),(9,2568),(10,4281),(11,3344),(12,2716),(13,1883),(14,1117),(15,219),(16,61))),
 ((40,0,1),17040117571551,249,7,197120,((7,500),(8,1743),(9,2568),(10,4281),(11,3344),(12,2716),(13,1883),(14,1117),(15,219),(16,61))),
 ((41,0,0),26414490561909,352,3,107520,((3,899),(4,1860),(5,4590),(6,4538),(7,5161),(8,1378),(9,6))),
)
SAMPLE_SHA='b60a5e41435c2b5169d1071d821c73c6c8c76dce77698f41350dfeec9ab6d090'

def prefixes():
    states={(2,0,0):1}
    for i in range(2,58):
        nxt=defaultdict(int)
        for (f,flag,q),c in states.items():
            if not r44.eligible(i,f,q):continue
            nxt[(f+1,(flag|int(306*(i+1)>=485*f))&~2,0)]+=c
            if flag<2:nxt[(f,flag<<1,q+1)]+=c
        states=nxt
    assert len(states)==303 and states[(39,0,0)]==55114089659444
    for st,count,*_ in CLASSES:assert states[st]==count
    return states

def excluded():
    counts=Counter()
    by_cylinder=[]
    for low in OLD:
        local=Counter()
        for j in range(1024):
            state=r44.genuine_prefix(low+(j<<48))
            if state is not None:
                local[state[:3]]+=1
                counts[state[:3]]+=1
        by_cylinder.append(local)
    assert tuple(c[(39,0,0)] for c in by_cylinder)==r44.EXPECTED_OLD
    assert counts[(39,0,0)]==843
    for st,_,x,*_ in CLASSES:assert counts[st]==x
    return counts

def suffixes(state,num0):
    terms=[]
    for bits in range(256):
        f,flag,q,num=(*state,num0)
        shift=0
        for i in range(58,66):
            bit=(bits>>(i-58))&1
            shift=(shift+bit*r44.POW2MOD9[i])%9
            next_state=r44.src_transition(i,f,flag,q,num,bit)
            if next_state is None:break
            f,flag,q,num=next_state
            num&=(1<<(66-i-1+3))-1
            if not r44.eligible(i+1,f,q):break
        else:
            if (f,flag)==(43,0) and q%2:
                amod=(3*(1-num))%8
                if amod:
                    a=32+amod
                    assert (num-1+a*P)%8==0
                    terms.append((bits,shift,a))
    return terms

def phases(st,minimum,expected_total,expected_hist):
    hist=Counter()
    total=0
    for num in range(2048):
        terms=suffixes(st,num)
        for r9 in range(9):
            k=sum((r9+shift+a)%9 in ALLOW for _,shift,a in terms)
            hist[k]+=1
            total+=k
    assert sum(hist.values())==18432
    assert min(hist)==minimum and total==expected_total
    assert tuple(sorted(hist.items()))==expected_hist
    return max(hist)

def bitmap_score(word,initial_even_run):
    # Faithful independent spelling of Rust's source precompute maxval.
    cur=peak=0
    run=initial_even_run
    for i in range(24):
        if word>>i&1:
            j=i
            while j<24 and word>>j&1:j+=1
            if j+2<24 and (word>>j)&3==0:peak=max(peak,cur+306)
            cur-=179
            run=0
        else:
            cur+=306
            run+=1
            if run%2==0:peak=max(peak,cur+179)
        peak=max(peak,cur)
    return peak

def direct_samples():
    limits={(39,0,0):5}
    for st,_,_,m,*_ in CLASSES:limits[st]=m
    quota={st:4 for st in limits}
    starts=[]
    bitmap=Counter()
    for j in range(200000):
        r0=3+4*j
        if r0%(1<<48) in OLD:continue
        state=r44.genuine_prefix(r0)
        if state is None or state[:3] not in quota or not quota[state[:3]]:continue
        st=state[:3]
        terms=[v for v in suffixes(st,state[3]%2048)
               if (r0%9+v[1]+v[2])%9 in ALLOW]
        assert len(terms)>=limits[st]
        for suffix,_,a in terms[:limits[st]]:
            root=r0+(suffix<<58)
            n=root+a*L
            f,flag,q,num=state
            for i in range(58,66):
                step=r44.src_transition(i,f,flag,q,num,(suffix>>(i-58))&1)
                assert step
                f,flag,q,num=step
                assert r44.eligible(i+1,f,q)
            assert f==43 and flag==0 and q%2
            assert B<=n<E and n%9 in ALLOW
            orbit=[n]
            for _ in range(90):orbit.append(r44.original_T(orbit[-1]))
            assert orbit[66]==num+a*P-1
            assert orbit[66]%8==0 and orbit[69]<n
            assert sum(t%2 for t in orbit[:66])==43
            true_run=0
            for t in orbit[:66]:true_run=0 if t%2 else true_run+1
            assert true_run==q
            word=sum((orbit[66+i]&1)<<i for i in range(24))
            source=bitmap_score(word,0)
            corrected=bitmap_score(word,q%2)
            bitmap['starts']+=1
            bitmap['source_CLEAR']+=int(source>659)
            bitmap['source_LIVE']+=int(source<=659)
            bitmap['corrected_CLEAR']+=int(corrected>659)
            # Three successor evens force source maxval>=918 (strictly > cutoff659).
            assert source>=918 and corrected>659
            starts.append(n)
        quota[st]-=1
    assert not any(quota.values()) and len(starts)==len(set(starts))
    digest=sha256(('\n'.join(map(str,sorted(starts)))+'\n').encode()).hexdigest()
    assert digest==SAMPLE_SHA and bitmap=={'starts':132,'source_CLEAR':132,'corrected_CLEAR':132}
    return bitmap,digest

def main():
    dp=prefixes()
    old=excluded()
    total_new=0
    for st,expected,prior,minhit,phase_total,hist in CLASSES:
        maxhit=phases(st,minhit,phase_total,hist)
        new=(dp[st]-old[st])*minhit
        total_new+=new
        print('R45_CLASS_PASS state=%s prefixes=%d old_prefixes=%d min=%d max=%d phase_sum=%d new_originals=%d'
              %(','.join(map(str,st)),expected,prior,minhit,maxhit,phase_total,new))
    assert total_new==811316649179155
    union=total_new+275570448293005+96375
    assert union==1086887097568535
    remaining=6438209236755220-93792-total_new-275570448293005
    assert remaining==5351322139189268
    print('R45_GLOBAL_UNION_PASS new_originals=%d inherited_R44=275570448293005 old_originals=96375 combined_originals=%d untouched_eligible_roots=%d global_candidate_upper_unchanged=326518028938128165'
          %(total_new,union,remaining))
    bitmap,digest=direct_samples()
    print('R45_ORIGINAL_T_BITMAP_PASS samples=%d source_CLEAR=%d source_LIVE=%d corrected_CLEAR=%d sha256=%s'
          %(bitmap['starts'],bitmap['source_CLEAR'],bitmap['source_LIVE'],bitmap['corrected_CLEAR'],digest))
    # Large integers are not safely distinguished by IEEE double: never float-merge phases.
    assert float(2733576887422834181503)==float(2733576887422834181504)
    print('R45_EXACT_PHASE_PASS prefix_mod2048 root_mod9 eight_suffix_steps=8 future_equivalence=integer_only source_bitmap_CLEAR=mathematical_not_native')
if __name__=='__main__':main()
