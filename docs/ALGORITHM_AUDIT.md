# CEML-R2 Algorithm and Implementation Audit

Status: **NOT STARTED**

R2 compares architecture families. It must not select machine-specific parameters before C1 measures the dedicated machine.

## Families to compare

- direct/naive shortened-map stepping;
- odd-only transformations;
- affine batching;
- Collatz-polynomial batching;
- binary splitting;
- super-batching or hierarchical composition;
- other exact macro-transform methods supported by R1 evidence.

For each, document mathematical state representation, exact step accounting, asymptotic considerations, memory behaviour, checkpoint implications, correctness argument, and implementation complexity.

## Backends/toolchains to compare

- GMP;
- GMP + FLINT;
- Rust big-integer/FFI options;
- C;
- C++;
- Python as orchestration/reference code;
- any other credible option discovered in R1.

Python must not be assumed suitable for the per-step extreme-integer hot loop. Equally, no compiled language or library wins merely by reputation; R2 narrows viable families and C1 measures them on the actual machine.

## Required output matrix

For every viable architecture record:

- source/reference basis;
- exactness model;
- batched transformation form;
- step-count preservation method;
- expected allocation/copy pressure;
- likely library dependencies;
- threading constraints;
- checkpoint boundary options;
- independent-test strategy;
- hardware characteristics likely to affect the choice;
- local benchmarks needed in C1;
- reasons to retain or reject.

## R2 exit rule

R2 may produce a shortlist and hypotheses. It may not freeze compiler flags, backend thresholds, macro-block sizes, worker counts, RAM ceilings, or checkpoint cadence.
