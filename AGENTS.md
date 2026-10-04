# Instructions for CEML Agents

This file governs automated and human-assisted work in this repository.

## Authority

Treat this repository as the sole authoritative CEML state. Do not import architecture, terminology, assumptions, reports or conclusions from another Collatz repository unless a specific fact is independently relevant, re-audited and cited.

## First action in every session

Read `PROGRAM_STATUS.md`, `PROJECT_CHARTER.md` and the current gate specification before changing files. For C1, `docs/CODEX_HANDOFF.md` and `docs/HARDWARE_AUDIT_SPEC.md` are mandatory controlling specifications.

## Stage discipline

Label work as exactly one of: research, hardware characterization, implementation, validation, scientific execution, anomaly investigation, or proof/certification. Mixed-stage work requires explicit protocol permission.

The current C1 gate authorizes hardware characterization and implementation only in the I1-prescribed order. Bounded calibration is engineering evidence within C1; it is not validation or scientific execution.

## Hard prohibitions unless a later gate explicitly authorizes them

Do not:

- run a scientific CEML trajectory;
- generate or request the scientific master seed;
- derive/evaluate a scientific rung start during C1;
- freeze the provisional magnitude ladder;
- reroll, rank or inspect candidate scientific starts;
- claim divergence from runtime, magnitude, peak behaviour or failure to finish;
- claim V1 or E1 completion during C1.

## C1 implementation discipline

C1 must:

- collect only R4-authorized machine facts and sanitize before persistence where practical;
- establish local resource-safety ceilings before non-trivial calibration;
- run only the CEML-CAL-1 bounded suite or stricter local subsets;
- record unavailable facts instead of guessing;
- use only I1-eligible candidate families;
- reject a benchmark lacking exact correctness agreement or required route activation;
- make every selected engineering choice traceable to local evidence;
- avoid silent dependency installation/upgrade/substitution;
- prove the intended checkpoint filesystem can satisfy CEML-CKPT-1;
- implement the production engine only after the evidence-backed architecture decisions it depends on;
- keep the build pinned and offline-capable;
- freeze only sanitized C1 report/build/profile artifacts;
- stop before V1.

## Scientific invariants

Never change exact C/T/U semantics, first-1 termination, exact standard/shortcut/odd accounting, rung/start-generation semantics, cryptographic/canonicalization rules, CEML-CKPT-1 semantics, result statuses, anomaly policy or V1 acceptance for hardware convenience.

## Privacy

Never commit usernames, hostnames, serial numbers, MAC/IP addresses, credentials, tokens, account identifiers, filesystem/device UUIDs, unrelated paths/inventories or hashes of prohibited stable identifiers. Run the I1 sensitive-data gate on the staged C1 artifacts before commit.

## Research/evidence discipline

For factual external claims, record source, publication/retrieval details, exact claim, status and uncertainty. For local C1 facts use the R4 evidence classes. A hardware observation is not a benchmark; a benchmark is not V1; V1 is not scientific execution.

## Change control

Update `PROGRAM_STATUS.md` only when the same commit contains evidence satisfying the stated gate. Material post-freeze scientific changes require a scientific protocol/schema version. Material R4/I1 contract changes require reviewed audit/engineering-spec revisions before affected evidence is accepted.

## Result discipline

A completed rung means one exact predetermined start was evaluated under an identified protocol and validated machine/build profile. It says nothing by itself about all integers at that magnitude or a probability of convergence.
