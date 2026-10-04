# CEML Claim Policy

Status: **Bootstrap policy**

This policy applies immediately and survives into later protocol versions unless explicitly replaced.

## Claims CEML may make

When supported by complete provenance, CEML may state facts about an exact sampled object, for example:

> This exact predetermined N-digit integer was evaluated under scientific protocol X and machine/build profile Y and reached 1 after Z shortened-map iterations.

CEML may also compare descriptive empirical behaviour across its predetermined rungs, provided the comparison is clear that each rung contains one sampled start.

## Claims CEML may not infer from the ladder

One sampled start per rung does not establish:

- convergence of all integers of that magnitude;
- a population probability of convergence;
- a verified interval;
- representativeness of all starts near that magnitude;
- divergence from failure to finish;
- divergence from long runtime;
- divergence from a large trajectory peak;
- proof of the Collatz conjecture.

A resource ceiling is an engineering outcome, not a mathematical counterexample.

## Falsification boundary

An explicit start whose exact trajectory is independently certified to violate the conjecture would be extraordinary evidence requiring a separate certification programme. CEML must freeze and preserve the object, not silently relabel a difficult or unfinished run as falsification.

## Language rules

Use `completed`, `frozen`, `resource stop`, `validation failure`, or other exact statuses defined by schema. Avoid words such as `divergent`, `counterexample`, or `proof` unless the corresponding mathematical standard has actually been met.

## Performance claims

Report performance only with machine/build/configuration context. A calibration result is not a universal algorithm-performance claim.

## External claims

When discussing another implementation or published result, attribute it and state whether CEML reproduced it. Do not write "verified" when only author-reported evidence has been seen.
