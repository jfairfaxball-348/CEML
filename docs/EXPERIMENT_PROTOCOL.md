# CEML Experiment Protocol

Status: **DRAFT — scientific semantics require R3 freeze**

## Experimental unit

The intended experimental unit is one exact, predetermined, positive odd integer for one frozen magnitude rung. There is exactly one such scientific start per rung.

No rerolling is allowed because a candidate looks uninteresting. No choice among multiple candidates, survivor ranking, peak chasing, or post-hoc substitution is permitted.

## Provisional ladder

The bootstrap targets are `10^6`, `10^7`, `10^8`, `10^9`, and `10^10` decimal digits. They remain provisional until literature, algorithm, resource, implementation, and local-hardware audits support a final ladder.

R3 must decide whether a rung is defined by decimal digits, exact bit length, or an explicit conversion/sampling rule.

## Provisional map

The current candidate convention is the shortened map

[
T(n)=
\begin{cases}
n/2, & n\equiv0\pmod2,\\
(3n+1)/2, & n\equiv1\pmod2.
\end{cases}
]

This convention is not frozen during bootstrap. If a different internal convention is used later, exact conversion formulas and exhaustive small-value tests are mandatory. Every macro operation must preserve the exact number of underlying shortened-map iterations represented.

## Exactness

All candidate-affecting arithmetic is exact. Floating-point approximations may be used only for ancillary engineering estimates when they cannot alter the candidate, trajectory state, step count, checkpoint state, or result.

## Scientific run lifecycle

A future run must have:

1. frozen protocol version;
2. frozen rung definition;
3. frozen deterministic generator and seed policy;
4. generated start digest before trajectory observation;
5. validated engine/build;
6. frozen local machine/build profile;
7. run manifest;
8. restartable checkpoints;
9. compact result record;
10. result/artifact hashes.

## Progression

A normal completion is preserved and authorizes consideration of the next rung. An anomaly trigger halts automatic progression and freezes exact state for audit.

## Scientific boundary

A single completion supports a statement about that exact integer under that exact protocol. It does not support a claim about every integer of the same magnitude or a convergence probability.
