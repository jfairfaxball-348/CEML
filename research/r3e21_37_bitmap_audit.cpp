// R3E21-37 independent 24-bit symbolic bitmap reproduction (research only).
// Run: g++ -O3 -std=c++17 -Wall -Wextra -o /tmp/r37_bitmap research/r3e21_37_bitmap_audit.cpp
//      /tmp/r37_bitmap
// Finite input domain: exactly 2^24 residues; no production Collatz frontier checks.
#include <cstdint>
#include <cstdio>
#include <algorithm>
#include <cassert>
using U=unsigned __int128;
static bool de(uint32_t w,int i) {
    uint32_t q=w>>i;
    int a=__builtin_ctz(q+1u);
    if(i+a+2>=24) return false;
    return ((w>>(i+a))&3u)==0u;
}
int main() {
    const uint32_t LIM=1u<<24;
    long long live[8]={},gap[8]={},equal=0;
    bool emitted=false;
    for(uint32_t r=0;r<LIM;r++) {
        // First generate the genuine 24 parity steps independently,
        // using a positive high lift to avoid the zero-state corner.
        U x=(U)r+LIM;
        uint32_t word=0;
        for(int i=0;i<24;i++) {
            if((x&1)==0) {word|=1u<<i; x=(x*3)/2;}
            else x=(x+1)/2;
        }
        // Independently reproduce main.rs's shifted-X parity encoder.
        uint64_t nx=r;
        uint32_t source_word=0;
        for(int i=0;i<24;i++) {
            if((nx&1)==0) {nx+=nx/2; source_word|=1u<<i;}
            else nx=nx/2+1;
        }
        assert(word==source_word);
        // Source-compatible maxval; alternative guarded score omits
        // a mod-3 preimage inference before the first odd step in-window.
        int cur=0,src=0,guarded=0,evens=0;
        bool prior_odd=false;
        for(int i=0;i<24;i++) {
            if((word>>i)&1) {
                if(cur+306>src && de(word,i)) src=cur+306;
                if(cur+306>guarded && de(word,i)) guarded=cur+306;
                cur-=179; evens=0; prior_odd=true;
            } else {
                cur+=306; evens++;
                if(evens%2==0) {
                    src=std::max(src,cur+179);
                    if(prior_odd) guarded=std::max(guarded,cur+179);
                }
            }
            src=std::max(src,cur);
            guarded=std::max(guarded,cur);
        }
        for(int a=0;a<8;a++) {
            int cutoff=174+485*a;
            if(src<=cutoff) live[a]++;
            if(src>cutoff && guarded<=cutoff) {
                gap[a]++;
                if(!emitted) {
                    emitted=true;
                    printf("diagnostic residue=%u parity_word=%06x source_score=%d guarded_score=%d a=%d cutoff=%d\n",
                        r,word,src,guarded,a,cutoff);
                }
            }
        }
        if(src==guarded) equal++;
    }
    const long long expected_live[8]={333343,1590275,3837929,6750160,
        9809263,12495505,14479396,15712298};
    const long long expected_gap[8]={0,60002,0,0,0,2529,484,0};
    for(int a=0;a<8;a++) {
        assert(live[a]==expected_live[a]);
        assert(gap[a]==expected_gap[a]);
        printf("a=%d cutoff=%d live=%lld gap=%lld\n",
            a,174+485*a,live[a],gap[a]);
    }
    assert(equal==16633847);
    printf("R37_BITMAP_PASS all_residues=%u equal_scores=%lld\n",LIM,equal);
}
// A 'gap' is missing justification in this conservative 24-step-only
// witness model, NOT a demonstrated faulty clearing of a full original
// 72-bit start after its 66-step prefix or other pruning layers.
