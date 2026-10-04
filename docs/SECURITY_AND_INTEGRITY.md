# Security and Integrity Policy

Status: **Bootstrap policy**

CEML does not need secrets for offline scientific execution.

## Sensitive-data exclusions

Do not commit credentials, tokens, private keys, usernames, hostnames, machine serial numbers, MAC addresses, IP addresses, unrelated paths, or raw system inventories beyond what is scientifically necessary.

Hardware reports must be sanitized before commit.

## Artifact integrity

Future manifests, machine profiles, builds, checkpoints, and results must use specified cryptographic digests. Algorithm choice and canonicalization are frozen in R3/I1 before E1.

Hashes identify bytes; they do not independently prove mathematical correctness. Validation supplies correctness evidence.

## Start precommitment

The seed/generator protocol must make candidate substitution detectable. The exact start digest is recorded before trajectory interpretation.

## Checkpoint integrity

Resume refuses corrupted, version-incompatible, or ambiguous checkpoint state. The operator must not manually edit a checkpoint to force continuation.

## Build provenance

Scientific results identify the engine commit, build digest, compiler/toolchain, relevant flags, arithmetic-library versions, and frozen local machine/profile version.

## Repository integrity

Protocol or result corrections use normal Git history; do not rewrite published scientific history merely to hide an error. Superseded results should remain traceable and be explicitly marked.

## Dependency hygiene

C1/I1 must identify exact build/runtime dependencies and an offline build/run strategy as appropriate. Network-fetched code during an active scientific run is prohibited.
