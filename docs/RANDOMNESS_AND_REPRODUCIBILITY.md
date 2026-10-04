# Randomness and Reproducibility

Status: **R3 DECISION REQUIRED — no scientific seed exists**

## Objective

Each rung must have exactly one start that is deterministically fixed before its trajectory is examined.

## Requirements to freeze in R3

The generator must be:

- deterministic from a master seed;
- standardized or fully specified;
- versioned;
- bias-resistant for the chosen sampling space;
- independently reproducible;
- able to generate the exact requested magnitude;
- constrained to positive odd integers;
- independent of trajectory behaviour.

Candidates for audit include SHAKE256 and ChaCha20-based deterministic streams. Mention here does not select either.

## Rung-distribution question

If decimal-digit rungs are retained, R3 must define the sampling distribution exactly. For a D-digit positive integer, the permitted domain and method for obtaining a uniform (or otherwise explicitly defined) odd sample must be mathematical, not implementation-dependent.

If exact bit-length rungs are chosen, the bit constraints and conversion/reporting rules must likewise be explicit.

## Reroll rule

There is no behavioural reroll. Any retry/expansion mechanism used to eliminate generator bias or handle an invalid raw encoding must be predetermined by the generator specification and depend only on the random stream and target domain.

## Seed policy

R3 must decide whether the repository stores the master seed, a pre-run commitment with delayed disclosure, or another reproducible scheme. The choice must balance precommitment, independent reproduction, and avoidance of discretionary candidate selection.

The scientific master seed must not be generated during bootstrap.

## Minimum manifest provenance

A future manifest must preserve:

- experiment/protocol version;
- rung definition;
- generator name/version;
- seed or seed commitment according to policy;
- derivation/domain-separation string;
- exact start digest;
- bit length;
- decimal-digit count when computed.

The giant decimal expansion need not be committed if it is exactly regenerable.
