# Instructions for CEML Agents

This file governs automated and human-assisted work in this repository.

## Authority

Treat this repository as the sole authoritative CEML state. Do not import architecture, terminology, assumptions, reports, or conclusions from another Collatz repository unless a specific fact is independently relevant, re-audited, and cited.

## First action in every session

Read `PROGRAM_STATUS.md`, `PROJECT_CHARTER.md`, and the current gate's specification before changing files.

## Hard prohibitions during BOOTSTRAP/R1/R2/R3/R4/I1

Do not:

- run a scientific CEML trajectory;
- generate the scientific master seed;
- freeze the provisional magnitude ladder without the required audit;
- implement the production arithmetic engine before I1/C1 authorization;
- infer local hardware that has not been measured;
- present generic performance estimates as local facts;
- treat calibration inputs as scientific samples;
- reroll, rank, or inspect multiple candidate starts to choose a rung;
- claim divergence from runtime, magnitude, or peak behaviour.

## Stage discipline

Label work as exactly one of: research, hardware characterization, implementation, validation, scientific execution, anomaly investigation, or proof/certification. Mixed-stage work requires explicit protocol permission.

## Research discipline

For factual external claims, record the source, publication/retrieval details, exact claim supported, status (primary/secondary), and uncertainty. Distinguish published fact, reproduced observation, author claim, community report, and CEML inference.

## Scientific invariants

Once frozen, never change exact map semantics, random-generation semantics, one-start-per-rung selection, exact step accounting, integrity rules, or anomaly policy for hardware convenience.

## Engineering discipline

Machine-specific choices are deferred until C1 measures the actual machine. Bounded calibration must remain deterministic, modest, and explicitly non-scientific.

## Privacy

Never commit usernames, hostnames, serial numbers, MAC addresses, credentials, tokens, unrelated paths, or other unnecessary machine identifiers. Sanitize local hardware reports before committing them.

## Change control

Update `PROGRAM_STATUS.md` only when the same commit contains evidence satisfying the stated exit gate. Material post-freeze changes require a new protocol/build/profile version.

## Result discipline

A completed rung means an exact predetermined start was evaluated under an identified protocol and machine/build profile. It says nothing by itself about all integers at that magnitude or a probability of convergence.
