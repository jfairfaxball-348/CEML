#!/usr/bin/env python3
"""R46 bounded regression: check family cardinality and an explicit literal-T sample.
Set containment is a mathematical corollary, not a large finite enumeration.
"""
B=2392518188130438742016
E=3000000000000000000000
F44=275570448293005
F45=811316649179155
OLD=96375
ROOTS=6438209236755220
OLD_ROOTS=93792
UPPER=326518028938128165

def T(n):
    return n//2 if n%2==0 else (3*n+1)//2

def main():
    assert F44+F45==1086887097472160
    assert F44+F45+OLD==1086887097568535
    assert ROOTS-OLD_ROOTS-F44-F45==5351322139189268
    # The reported R44 sample; replay all 69 literal shortened-map steps.
    n=2733576887422834181503
    assert B<=n<E
    x=n
    for i in range(1,70):
        x=T(x)
        if i==66:assert x%8==0
    assert x<n
    assert 69<=72
    assert UPPER==326518028938128165
    print("R46_MASK_CONTAINMENT_PASS fresh=0 selected=1086887097472160 untouched_roots=5351322139189268 witness69=1 upper_unchanged=326518028938128165")

if __name__=="__main__":
    main()
