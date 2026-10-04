# CEML Compute Budget

Status: **No numeric performance claim authorized**

Bootstrap deliberately does not estimate how long a million-, billion-, or multi-billion-digit rung will take on the future machine.

## Budget dimensions

R1/R2/C1 must collect evidence for:

- wall time;
- CPU time and sustained utilization;
- peak resident memory;
- temporary allocation pressure;
- storage footprint;
- checkpoint write volume and bandwidth;
- SSD free-space reserve;
- thermal headroom and throttling;
- power configuration;
- swap behaviour;
- validation overhead;
- recovery/recompute exposure between checkpoints.

## Constraint classification

For each candidate rung, C1 calibration should identify the likely dominant practical constraint among CPU time, RAM, disk I/O/capacity, and thermals. Any conclusion must be tied to the measured local profile and benchmark configuration.

## Safe ceilings

The local machine profile must eventually specify conservative operational ceilings such as maximum RAM fraction, minimum free disk reserve, checkpoint budget, worker count, and thermal/power recommendations. These are engineering settings and must not modify scientific invariants.

## Rung selection

The final ladder is chosen only after R1–R4, implementation calibration, and V1 evidence. C1 should estimate practical maximum sizes for sustained runs lasting hours and several days, but those estimates do not themselves authorize E1.

## Benchmark boundary

Calibration inputs must be modest, deterministic, and explicitly tagged `engineering-only`. They are never CEML scientific rungs.
