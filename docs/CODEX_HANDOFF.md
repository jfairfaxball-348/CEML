# CEML-I1 Codex Implementation Handoff

Status: **NOT READY — PLACEHOLDER ONLY**

This file will become the self-contained brief for the single substantial local Codex run after R1–R4 are complete.

It must not be treated as implementation authorization in its current state.

## Mandatory content before approval

The approved I1 brief must state:

- frozen scientific invariants;
- exact map convention and step-accounting rules;
- random-generation/manifests semantics without exposing or generating a seed prematurely;
- hardware properties C1 must inspect;
- privacy exclusions;
- bounded calibration tests and maximum permitted scale;
- viable implementation choices from R2;
- criteria for choosing language, GMP/FLINT/other backend, multiplication strategy, memory strategy, threading, and compiler flags;
- dependencies and offline-execution requirements;
- required file layout/interfaces;
- `hardware-report`, calibration, self-test, validation, prepare/run/status/resume/verify capabilities at a semantic level;
- checkpoint and result formats;
- test requirements and independent oracle;
- local machine/build profile generation;
- prohibited scientific execution;
- acceptance criteria.

## Required local sequence

`hardware audit -> bounded measured calibration -> architecture choice -> implementation -> build -> frozen local profile`

Codex must not reverse that order by implementing a generic assumed architecture first.

## Approval condition

Change this status to APPROVED only in a commit that also advances `PROGRAM_STATUS.md` to C1 authorization and references completed R1–R4 evidence.
