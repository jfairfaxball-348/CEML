# CEML Checkpoint Specification

Status: **Semantic framework only — binary format not frozen**

## Purpose

Scientific runs must survive reboot, power interruption, process crash, manual shutdown, and routine machine maintenance without corrupting the sole resumable state.

## Required logical contents

A checkpoint must preserve enough exact information to resume without recomputing the orbit from the start, including:

- run identifier;
- digest of original start;
- current exact integer;
- exact total shortened-map iterations represented;
- macro-block count;
- current bit length;
- maximum bit length observed;
- elapsed wall/CPU accounting where meaningful;
- engine/build identity;
- scientific protocol version;
- machine/build profile version;
- checkpoint-format version;
- integrity hash.

Any additional internal batching state required for exact resume must also be serialized.

## Atomicity

Never overwrite the sole valid checkpoint in place. The preferred design to evaluate is a rolling A/B scheme:

1. write a complete candidate checkpoint to a new slot/temp file;
2. flush according to the frozen durability policy;
3. validate structure and integrity digest;
4. atomically promote/rename;
5. update a small manifest/pointer atomically;
6. retain at least one previously validated checkpoint until promotion is known good.

The exact filesystem semantics must be tested on the target system.

## Cadence

Checkpoint cadence is an engineering parameter, not a scientific invariant. C1 must derive it from measured state size, write throughput, SSD endurance considerations, expected run duration, and acceptable recomputation loss.

## Integrity boundary

A corrupt or ambiguous checkpoint is an anomaly/failure condition. Resume must refuse rather than guess.

## Repository policy

Large checkpoint bodies remain local and ignored by Git. Git stores the format specification, compact metadata/hashes when scientifically useful, and the frozen configuration needed to reproduce generation and interpretation.
