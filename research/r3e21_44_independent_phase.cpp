// R44 independent exhaustive phase verifier, source-search1 58+8 suffix.
// Bounded CPU mathematics, not Collatz science, source bitmap or production.
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
using std::uint32_t;
using std::uint64_t;
static uint32_t p3[67];
static int p2[67];
struct State { int f,flag,q; uint32_t number; int residue; };
static inline bool eligible(int i,int f,int q){
    return 306*i<485*f && !(q>=2 && (q%2)==0 && 306*(i-1)>=485*(f-1));
}
static inline bool gate(int n){return n==0||n==1||n==3||n==6||n==7;}
static bool transition(int i,State &s,int bit){
    const uint32_t modulus=(uint32_t(1)<<(66-i+3))-1u;
    uint32_t x=(s.number+(bit?p3[s.f]:0u))&modulus;
    bool odd=(((s.number&1u)==0u)!=bool(bit));
    State t=s;
    t.residue=(s.residue+bit*p2[i])%9;
    if(odd){
        t.f++;
        t.flag=(s.flag|(306*(i+1)>=485*s.f))&~2;
        t.q=0;
        t.number=(x+x/2u)&(modulus>>1);
    } else {
        if(s.flag>=2)return false;
        t.flag=s.flag<<1;
        t.q=s.q+1;
        t.number=(x/2u+1u)&(modulus>>1);
    }
    if(!eligible(i+1,t.f,t.q))return false;
    s=t;
    return true;
}
int main(){
    p3[0]=1;p2[0]=1;
    for(int i=1;i<67;i++){p3[i]=p3[i-1]*3u;p2[i]=(p2[i-1]*2)%9;}
    int minimum=256,maximum=0;
    uint64_t sum=0,phase_count=0,probes=0;
    std::array<uint32_t,257> histogram{};
    for(int residue=0;residue<9;residue++)for(int number=0;number<2048;number++){
        int hits=0;
        for(int suffix=0;suffix<256;suffix++){
            State s{39,0,0,static_cast<uint32_t>(number),residue};
            bool ok=true;
            for(int i=58;i<66;i++){
                if(!transition(i,s,(suffix>>(i-58))&1)){ok=false;break;}
            }
            ++probes;
            if(!ok||s.f!=43||!(s.q&1)||s.flag!=0)continue;
            int a_residue=(3*(1-static_cast<int>(s.number)))&7;
            if(a_residue==0)continue; // only common a=33,...,39
            if(gate((s.residue+32+a_residue)%9))++hits;
        }
        if(hits<minimum)minimum=hits;
        if(hits>maximum)maximum=hits;
        ++histogram[hits];++phase_count;sum+=hits;
    }
    if(probes!=4718592ull||phase_count!=18432||minimum!=5||maximum!=17||sum!=206080ull){
        std::fprintf(stderr,"R44_FAIL probes=%llu phases=%llu min=%d max=%d sum=%llu\n",
            (unsigned long long)probes,(unsigned long long)phase_count,minimum,maximum,(unsigned long long)sum);
        return EXIT_FAILURE;
    }
    const uint32_t expected[]={0,0,0,0,0,49,90,485,1844,2509,1677,2914,3744,2627,1269,747,416,61};
    for(int i=0;i<18;i++)if(histogram[i]!=expected[i])return EXIT_FAILURE;
    for(int i=18;i<257;i++)if(histogram[i])return EXIT_FAILURE;
    std::printf("R44_INDEPENDENT_PHASE_PASS probes=4718592 phases=18432 min=5 max=17 sum=206080 histogram=5:49,6:90,7:485,8:1844,9:2509,10:1677,11:2914,12:3744,13:2627,14:1269,15:747,16:416,17:61\n");
}
