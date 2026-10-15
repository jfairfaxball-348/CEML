#!/usr/bin/env python3
"""R3E21-33: capped, research-only semantic probes. NEVER frontier science."""
from collections import defaultdict
from dataclasses import dataclass
import hashlib
import json

NUM, DEN, M, B, A = 306, 485, 66, 24, 6
LIMIT128 = (1 << 128)-1

def t(n):
    assert n >= 1
    return n//2 if n%2==0 else (3*n+1)//2

def shifted_step(n):
    assert n >= 1
    return 3*n//2 if n%2==0 else (n+1)//2

def source_table_entry(r):
    # Exact arithmetic restatement of pinned Rust main.rs lines 110-123.
    n,s = r,0
    for _ in range(16):
        if n%2==0:
            n=n+n//2
            s+=1
        else:
            n=n//2+1
    return s,n

def independently_trace_shifted(n,count):
    for _ in range(count): n=shifted_step(n)
    return n

def rust_search3_block(n):
    s,tail=source_table_entry(n%65536)
    return (n>>16)*3**s+tail

def test_lookup():
    count=0
    for r in range(1,65536):
        s,tail=source_table_entry(r)
        if r>=2: assert independently_trace_shifted(r,16)==tail
        assert rust_search3_block(r)==tail
        count+=1
    for q in (0,1,2,17,1<<20,1<<86,1<<103,1<<104):
        for r in (2,3,7,0x100,0x8000,0xffff):
            n=(q<<16)+r
            assert independently_trace_shifted(n,16)==rust_search3_block(n)
            count+=1
    return count

def test_guard():
    # Counterexample to sufficiency for arbitrary state, NOT proven reachable.
    n=(1<<120)-(1<<16)
    assert (n>>64)<(1<<56)
    assert n.bit_length()==120 and n%65536==0
    assert source_table_entry(0)==(16,0)
    nxt=rust_search3_block(n)
    assert nxt==((1<<104)-1)*3**16
    assert nxt.bit_length()==130 and nxt>LIMIT128
    return n,nxt

def test_search2_bounds():
    off=M*NUM//DEN+1
    assert off==42
    for s in range(M+1):
        if M*NUM<s*DEN:
            assert off<=s<=M and s<72
            if s<off+8: assert 0<=s-off<8
    length=(1<<(B-6))+((1<<A)+63)//64
    for idx in (0,1,63,64,(1<<B)-2,(1<<B)-1):
        w=idx//64
        assert w<length
        if idx%64: assert w+1<length
    assert length==262145
    return off,length

def test_two_even():
    hits=0
    for n in range(3,10000,2):
        for r in range(1,8):
            x=n;ok=True
            for _ in range(r):
                if x%2==0:ok=False;break
                x=t(x)
            if not ok or x%4:continue
            y=(n-1)//2
            lhs,rhs=n,y
            for _ in range(r+2):lhs=t(lhs)
            for _ in range(r+1):rhs=t(rhs)
            assert 0<y<n and lhs==rhs==x//4
            assert x+1==3**r*(n+1)//(1<<r)
            hits+=1
    assert hits>100
    return hits

def test_inverse():
    count=0
    for n in range(3,5001):
        if n%3==2:
            p=(2*n-1)//3
            assert 0<p<n and t(p)==n
            count+=1
        if n%9==4:
            p=(8*n-5)//9
            assert 0<p<n and t(t(t(p)))==n
            count+=1
    return count

@dataclass(frozen=True)
class Event:
    original_n:int
    ordinal:int
    kind:str
    state:int

def verify_roster(L,H,leaves,events,launches,completions,event_capacity,claimed_hash=None):
    # Independently supplied roster, not a proof source emitted every branch.
    assert 1<=L<=H<=512 and H-L<=128
    if sorted(launches)!=sorted(completions) or len(set(launches))!=len(launches):
        return "REJECT_KERNEL_SEAL"
    if len(events)>event_capacity:return "REJECT_EVENT_TRUNCATION"
    if [x["n"] for x in leaves]!=list(range(L,H)):return "REJECT_ROSTER"
    groups=defaultdict(list);previous=None
    for e in events:
        tag=(e.original_n,e.ordinal)
        if previous is not None and tag<=previous:return "REJECT_EVENT_ORDER"
        if e.original_n<L or e.original_n>=H:return "REJECT_EVENT_DOMAIN"
        if e.ordinal!=len(groups[e.original_n]):return "REJECT_EVENT_ORDINAL"
        if e.state<1:return "REJECT_BAD_STATE"
        groups[e.original_n].append(e)
        previous=tag
    for x in leaves:
        n=x["n"];status=x["status"];proof=x.get("proof")
        if status=="UNRESOLVED":return "REJECT_UNRESOLVED"
        if groups[n]:return "REJECT_UNARBITRATED_EVENT"
        if status=="PROVED":
            if proof=="even" and n%2==0 and n>=2:continue
            if proof=="one_mod_four" and n%4==1 and n>1 and t(t(n))<n:continue
            if proof=="inverse3" and n%3==2 and n>2 and t((2*n-1)//3)==n:continue
            return "REJECT_FALSE_PROOF"
        if status=="RESOLVED":
            path=x.get("path")
            if not isinstance(path,list) or not path or path[0]!=n:return "REJECT_BAD_TRACE"
            if any(t(a)!=b for a,b in zip(path,path[1:])):return "REJECT_BAD_TRACE"
            if path[-1]>=n:return "REJECT_NO_DESCENT"
        else:return "REJECT_STATUS"
    if claimed_hash is not None and not isinstance(claimed_hash,str):return "REJECT_HASH_FORMAT"
    return "TOY_ACCEPT"

def test_roster():
    L,H=103,167
    leaves=[]
    for n in range(L,H):
        if n%2==0:leaves.append(dict(n=n,status="PROVED",proof="even"))
        elif n%4==1:leaves.append(dict(n=n,status="PROVED",proof="one_mod_four"))
        elif n%3==2:leaves.append(dict(n=n,status="PROVED",proof="inverse3"))
        else:
            path=[n]
            for _ in range(200):
                path.append(t(path[-1]))
                if path[-1]<n:break
            assert path[-1]<n
            leaves.append(dict(n=n,status="RESOLVED",path=path))
    args=dict(L=L,H=H,leaves=leaves,events=[],launches=[0,1],completions=[1,0],event_capacity=128)
    assert verify_roster(**args)=="TOY_ACCEPT"
    mutations=[
      dict(leaves=leaves[:-1]),
      dict(leaves=leaves[:-1]+[leaves[-2]]),
      dict(leaves=[leaves[1],leaves[0]]+leaves[2:]),
      dict(launches=[0,1,2]),
      dict(completions=[1]),
      dict(events=[Event(103,0,"OVERFLOW",2048)]),
      dict(events=[Event(103,1,"OVERFLOW",2048)]),
      dict(events=[Event(104,0,"OVERFLOW",2048),Event(103,0,"OVERFLOW",4096)]),
      dict(events=[Event(103,0,"OVERFLOW",2048)],event_capacity=0),
      dict(leaves=[dict(n=103,status="PROVED",proof="even")]+leaves[1:]),
      dict(leaves=[dict(n=103,status="RESOLVED",path=[103,2])]+leaves[1:]),
      dict(leaves=[dict(n=103,status="RESOLVED",path=[103])]+leaves[1:]),
      dict(leaves=[dict(n=103,status="RESOLVED",path=[103,2])]+leaves[1:],claimed_hash=hashlib.sha256(b"forged").hexdigest()),
      dict(leaves=[dict(n=103,status="UNRESOLVED")]+leaves[1:]),
    ]
    for mutation in mutations:
        assert verify_roster(**{**args,**mutation})!="TOY_ACCEPT",mutation
    return len(leaves),len(mutations)

def main():
    lookups=test_lookup()
    n,nxt=test_guard()
    off,padding=test_search2_bounds()
    hits=test_two_even()
    inverse=test_inverse()
    roster,rejected=test_roster()
    print("R33_TOY_PASS "+json.dumps(dict(lookup_states=lookups,
        overflow_input=n,overflow_output=nxt,overflow_bits=nxt.bit_length(),
        search2_min_threepower=off,padded_words=padding,
        coalescence_cases=hits,inverse_cases=inverse,roster_starts=roster,
        hostile_rejections=rejected),sort_keys=True))
if __name__=="__main__":main()
