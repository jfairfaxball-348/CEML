# CEML-R1 Literature Audit

Status: **NOT STARTED**

No literature finding is established by this bootstrap file. It is a structured target for R1.

## Questions

R1 must determine, with citations and caveats:

- the largest credible published or otherwise independently verifiable isolated-start Collatz computations;
- what "largest" means in each source (starting value, decimal digits, peak, steps, or another measure);
- current algorithms intended for extreme isolated starts;
- the Elsenhans method and related Collatz-polynomial/batching formulations;
- publication and peer-review status;
- public source implementations;
- whether claimed performance has been independently reproduced;
- machine/configuration assumptions behind performance numbers;
- known correctness caveats, unresolved bugs, or validation limitations.

## Evidence table

| ID | Source | Type/status | Claim examined | Conditions | Reproduced? | Confidence/caveat |
|---|---|---|---|---|---|---|
| — | — | — | No sources audited yet | — | — | — |

## Required distinctions

Do not conflate:

- contiguous verification bounds with isolated huge starts;
- starting magnitude with trajectory peak magnitude;
- a benchmark with a scientifically audited result;
- author-reported speed with reproduced speed;
- code availability with code correctness;
- a method description with an implementation suitable for CEML.

## R1 exit checklist

- [ ] Search strategy recorded.
- [ ] Primary sources preferred where available.
- [ ] Elsenhans-related claims traced to primary material.
- [ ] Public implementations catalogued.
- [ ] At least one attempt made to find independent reproduction or criticism for important claims.
- [ ] Performance claims include hardware/software context.
- [ ] Uncertainties and inaccessible evidence recorded.
- [ ] Implications for R2 stated.
