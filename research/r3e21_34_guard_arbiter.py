#!/usr/bin/env python3
"""R3E21-34 research-only: exact 82/98-step bound and hostile conservation fixture.
No production worker, no frontier search, no published source equivalence.
"""
import copy
import hashlib
import json

MAX128 = (1 << 128) - 1

def t(n):
    assert n > 0
    return n//2 if not n&1 else (3*n+1)//2

def shifted(n):
    assert n >= 2
    return 3*n//2 if not n&1 else (n+1)//2

def lookup(r):
    # Sixteen formal shifted-map rounds, including r=0 sentinel.
    assert 0 <= r < (1<<16)
    s, x = 0, r
    for _ in range(16):
        if not x & 1:
            x += x//2
            s += 1
        else:
            x = (x+1)//2
    return s, x

def block(x):
    assert x >= 2
    s, tail = lookup(x & 65535)
    q = x >> 16
    safe = q <= (MAX128-tail)//(3**s)  # check BEFORE multiply
    exact = q*(3**s)+tail
    return safe, exact, s, tail

def prove_two_blocks():
    # All-odd 82-step prefix requires 2^82|(n+1), impossible 1<=n<2^72.
    # An even T-state >=6 costs ratio at most 8/21 against all-odd growth.
    # If such an even state is 2 or 4, all later T-values are {1,2}.
    assert 3**82 < 2**130
    assert 3**97 < 7*2**151
    return dict(first_block_end_step=82,second_block_end_step=98,
        first_block_below_bits=120,second_block_below_bits=128,
        bound_82_valid=True,bound_98_valid=True)

def test_exact_blocks():
    count=0
    for n in list(range(2,4000))+[(1<<72)-1,(1<<71)+31,2**66+1,2**64-1]:
        x=n+1
        for j in range(1,99):
            x=shifted(x)
            if j in (66,82,98): assert x.bit_length()<=128
            if j==66: first=x
            if j==82:
                assert x < (1<<120)
                safe,y,_,_=block(first)
                assert safe and y==x
                at82=x
            if j==98:
                safe,y,_,_=block(at82)
                assert safe and y==x
        count+=1
    bad=(1<<120)-(1<<16)
    safe,y,s,tail=block(bad)
    assert not safe and y>MAX128 and s==16 and tail==0
    return count,y.bit_length()

def digest(payload):
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def proof_ok(n,proof):
    if proof=='even':return n>1 and n%2==0 and t(n)<n
    if proof=='one_mod_four':return n>1 and n%4==1 and t(t(n))<n
    if proof=='inverse3':
        p=(2*n-1)//3
        return n%3==2 and 0<p<n and t(p)==n
    return False

def make_roster(L=103,H=167):
    starts=[]
    for n in range(L,H):
        if n%2==0:starts.append(dict(n=n,status='PROVED',proof='even'))
        elif n%4==1:starts.append(dict(n=n,status='PROVED',proof='one_mod_four'))
        elif n%3==2:starts.append(dict(n=n,status='PROVED',proof='inverse3'))
        else:
            trace=[n]
            for _ in range(200):
                trace.append(t(trace[-1]))
                if trace[-1]<n:break
            assert trace[-1]<n
            starts.append(dict(n=n,status='RESOLVED',trace=trace))
    packet=dict(L=L,H=H,starts=starts,launches=[0,1],completions=[1,0],
                reservations=[],events=[],event_capacity=8,generated_event_count=0)
    packet['sha256']=digest({k:v for k,v in packet.items() if k!='sha256'})
    return packet

def accept(packet):
    q=copy.deepcopy(packet)
    claim=q.pop('sha256',None)
    if not isinstance(claim,str) or len(claim)!=64 or claim!=digest(q):return 'REJECT_DIGEST'
    L,H=q.get('L'),q.get('H')
    if not isinstance(L,int) or not isinstance(H,int) or not (1<=L<H<=512 and H-L<=128):
        return 'REJECT_DOMAIN'
    starts=q.get('starts')
    if not isinstance(starts,list) or [x.get('n') for x in starts]!=list(range(L,H)):
        return 'REJECT_ROSTER'
    launches=q.get('launches',[]);completions=q.get('completions',[])
    if not (len(launches)==len(set(launches)) and sorted(launches)==sorted(completions)):
        return 'REJECT_KERNEL'
    reservations=q.get('reservations',[]);events=q.get('events',[])
    if not isinstance(events,list) or not isinstance(reservations,list):return 'REJECT_EVENT_TYPE'
    if not isinstance(q.get('event_capacity'),int) or q['event_capacity']<0:return 'REJECT_CAPACITY'
    if q.get('generated_event_count')!=len(reservations) or len(events)>q['event_capacity']:
        return 'REJECT_EVENT_CAPACITY_OR_COUNT'
    # Authenticated producer reservation required. The toy does NOT prove native
    # source really reserves an event for every exceptional branch.
    if events!=reservations:return 'REJECT_MISSING_EVENT'
    last=None;ordinal={}
    for event in events:
        n,o=event.get('original_n'),event.get('ordinal')
        if not isinstance(n,int) or not isinstance(o,int) or not (L<=n<H) or o!=ordinal.get(n,0):
            return 'REJECT_ORDINAL'
        if last is not None and (n,o)<=last:return 'REJECT_EVENT_ORDER'
        if event.get('kernel') not in launches:return 'REJECT_EVENT_KERNEL'
        if event.get('reason') not in ('OVERFLOW','RESET','CTZ_ZERO','LOOKUP','RETURN','CARRY'):
            return 'REJECT_EVENT_KIND'
        last=n,o;ordinal[n]=o+1
    for item in starts:
        n=item['n'];state=item.get('status')
        if any(e['original_n']==n for e in events):return 'REJECT_UNRESOLVED_EVENT'
        if state=='PROVED':
            if not proof_ok(n,item.get('proof')):return 'REJECT_FALSE_PROOF'
        elif state=='RESOLVED':
            trace=item.get('trace')
            if not isinstance(trace,list) or not trace or trace[0]!=n:return 'REJECT_START'
            if not all(isinstance(z,int) and z>0 for z in trace):return 'REJECT_TRACE_TYPE'
            if any(t(a)!=b for a,b in zip(trace,trace[1:])):return 'REJECT_BAD_TRACE'
            if trace[-1]>=n:return 'REJECT_NO_DESCENT'
        else:return 'REJECT_STATUS'
    return 'TOY_ACCEPT'

def reseal(p):
    p['sha256']=digest({k:v for k,v in p.items() if k!='sha256'})
    return p

def test_arbiter():
    good=make_roster()
    assert accept(good)=='TOY_ACCEPT'
    attacks=[]
    def attack(change):
        p=copy.deepcopy(good);change(p);reseal(p)
        result=accept(p)
        assert result!='TOY_ACCEPT',result
        attacks.append(result)
    attack(lambda p:p['starts'].pop())
    attack(lambda p:p['starts'].__setitem__(1,p['starts'][0]))
    attack(lambda p:p['starts'].reverse())
    attack(lambda p:p['completions'].pop())
    attack(lambda p:p['completions'].append(0))
    attack(lambda p:p['starts'][0].update(status='PROVED',proof='even'))
    attack(lambda p:p['starts'][0].update(status='RESOLVED',trace=[103,2]))
    attack(lambda p:p['starts'][0].update(status='RESOLVED',trace=[103]))
    attack(lambda p:p['starts'][0].update(status='RESOLVED',trace=[2,1]))
    attack(lambda p:p['starts'][0].update(status='UNRESOLVED'))
    # Hash-only forgery: do NOT corrupt any other field.
    forged=copy.deepcopy(good);forged['sha256']='0'*64
    assert accept(forged)=='REJECT_DIGEST';attacks.append('REJECT_DIGEST')
    ev=dict(original_n=103,ordinal=0,kernel=0,reason='OVERFLOW')
    attack(lambda p:p.update(reservations=[ev],generated_event_count=1))
    attack(lambda p:p.update(reservations=[ev],events=[ev],generated_event_count=1))
    attack(lambda p:p.update(reservations=[ev],events=[ev],generated_event_count=2))
    attack(lambda p:p.update(reservations=[ev],events=[ev],generated_event_count=1,event_capacity=0))
    attack(lambda p:p.update(reservations=[{**ev,'ordinal':1}],events=[{**ev,'ordinal':1}],generated_event_count=1))
    attack(lambda p:p.update(reservations=[{**ev,'kernel':9}],events=[{**ev,'kernel':9}],generated_event_count=1))
    attack(lambda p:p.update(reservations=[{**ev,'reason':'RESET'}],events=[{**ev,'reason':'RESET'}],generated_event_count=1))
    ev2={**ev,'ordinal':1,'reason':'CARRY'}
    attack(lambda p:p.update(reservations=[ev,ev2],events=[ev2,ev],generated_event_count=2))
    attack(lambda p:p.update(reservations=[ev,ev],events=[ev,ev],generated_event_count=2))
    return len(good['starts']),len(attacks)

def main():
    bounds=prove_two_blocks()
    cases,overflow_bits=test_exact_blocks()
    roster,attacks=test_arbiter()
    print('R34_TOY_PASS '+json.dumps(dict(bounds=bounds,small_and_boundary_starts=cases,
        arbitrary_unreachable_overflow_bits=overflow_bits,roster=roster,
        hostile_rejections=attacks),sort_keys=True))

if __name__=='__main__':main()
