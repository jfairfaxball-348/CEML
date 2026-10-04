# CEML Result Record Policy

Status: **Bootstrap draft; canonical JSON schema is `schemas/result.schema.json`**

A result record is compact evidence about one run. It is not a dump of the trajectory and must not become a grab-bag of easy-to-collect metrics.

## Core identity

A completed scientific result should identify:

- experiment;
- result-schema version;
- scientific protocol version/commit;
- machine profile version/digest;
- rung;
- generator version and exact start digest;
- engine commit and build digest;
- compiler/toolchain and relevant arithmetic-library versions;
- hardware-profile digest.

## Core outcome

It should record only scientifically interpretable and reproducibility-relevant outcome/accounting fields, such as:

- status;
- exact shortened-map step count;
- macro-block count;
- maximum bit length;
- minimum bit length after the start if this metric survives R3 review;
- wall/CPU duration with definitions;
- final value;
- final checkpoint/artifact digest where applicable;
- result digest.

Counts may be encoded as decimal strings in machine-readable schemas to avoid language-specific integer-size ambiguity.

## Status semantics

At minimum distinguish a normal completion from anomaly freeze, operator abort, validation failure, resource stop, and integrity failure. A non-completed status must never be rendered as evidence of divergence.

## Digest rule

The result digest must be computed over a canonical representation defined before E1. Hash algorithm and canonicalization are R3/I1 decisions.

## No silent enrichment

Adding or changing a field with scientific meaning requires a schema/protocol version change. Local diagnostic logs may contain more engineering detail without redefining the scientific result.
