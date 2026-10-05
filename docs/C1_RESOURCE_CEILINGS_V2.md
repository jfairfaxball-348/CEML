# C1 revised local resource ceilings (version 2)

Stage: **hardware characterization**. C1 remains open. This document records
an observation-backed engineering decision made **before** the calibration it
governs. It supplements `docs/C1_RESOURCE_CEILINGS.md`, which is retained
unchanged as the record of the initial ceilings. Nothing here changes an I1
suite maximum, a scientific rule or global machine policy.

## Why the initial ceilings are replaced

Two guarded attempts of the first prescribed route case were refused and are
retained unchanged as invalid `C1_RESOURCE_ABORT` evidence:

| Bundle | Paging-input observation | Interval |
|---|---|---|
| `c1-20261005-route-subset` | about 1917 pages per second | about 38 ms after the child |
| `manual-20261005-134907` | 138 pages per second | one full second after the child |

In both, the candidate agreed with its reference, activated its route with zero
fallback, and page **output** was zero. Neither is performance evidence. The
second attempt was the single authorized comparison; it was not repeated.

A separate arithmetic-free monitor study (`tools/c1/pressure_study.py`, study
`pressure-20261005-a`, retained under ignored `local/c1/pressure-study/`) then
sampled the same counters over 35 one-second intervals with no calibration
case running:

- 20 idle intervals: median about 1 page per second input, maximum about 104;
  one interval exceeded the 100-page ceiling with no CEML child at all;
- 10 intervals each containing one arithmetic-free launch of the old candidate
  image (argument refusal before any arithmetic): median about 2, maximum
  about 330; one interval exceeded the ceiling;
- 5 further idle intervals: maximum about 44;
- page output was zero in all 35 intervals;
- every excursion was a single isolated interval;
- available physical memory stayed above 7.9 GB;
- the processor-performance counter was available and read 153 to 179 percent
  of nominal throughout.

Evidence class: OBSERVED_FACT, momentary state. Interpretation and limits:
the page-input counter includes mapped-file reads and, on this machine,
crosses 100 pages per second in isolated one-second intervals without any
CEML arithmetic. A single such interval therefore cannot distinguish memory
pressure caused by a bounded case from unrelated background activity. Thirty
five samples do not characterize rare events, and no claim is made that the
machine is free of memory pressure in general.

## Decision `decision.resource-ceilings-v2`

Unchanged from the initial ceilings:

- at least 4 GiB available physical memory and 16 GiB free target storage at
  every polling boundary;
- one benchmark child, one arithmetic thread, one allowed logical processor;
- a kill-on-close Job with 256 MiB process and job memory limits. This is an
  enforced limit, not an estimate; a case that needs more fails closed;
- AC power and zero standby and hibernate idle indices;
- 5 seconds of wall time per child, checked at intervals of at most 100 ms;
- paging rates measured only over intervals of at least one second, two
  admission intervals before launch and one complete interval after exit;
- any nonzero page **output** in any interval refuses or aborts.

Revised:

1. **Paging input.** Refuse admission or abort when page input exceeds 100
   pages per second in **two consecutive** intervals. One isolated excursion
   with zero page output and intact headroom is recorded in the calibration
   record (interval count, excursion count, maximum) and does not abort. This
   keeps the unchanged threshold but requires persistence, which is the
   property the isolated idle excursions lack. It makes no claim to isolate
   pagefile traffic.
2. **Throttling proxy.** Temperature remains unavailable. Where the
   processor-performance counter is available, a reading below 100 percent of
   nominal at any sampled interval invalidates the case as
   `C1_ENVIRONMENT_INVALID`. This is a frequency-collapse stop condition, not a
   thermal measurement and not a thermal-safety claim. If the counter is
   unavailable the record says so.
3. **Sustained load.** Each child is preceded by at least two seconds and
   followed by at least one second of monitoring with no CEML arithmetic, and
   may itself run at most five seconds. Aggregate child wall time is capped at
   900 seconds, including the 80,015,800 ns already charged, which is far
   below the I1 aggregate of 5400 seconds.
4. **Work bounds.** The initial restriction to 4096-bit operands, 256 steps,
   width 4 and 1024-byte checkpoint magnitudes is lifted to the unchanged I1
   maxima: 131072 generated bits per operand, 4096 steps per fixed-step case,
   16384 steps per affine macro construction, table width 16, 32 KiB
   checkpoint magnitude. The largest operand is 16 KiB; the memory limit
   remains the enforced 256 MiB Job limit.
5. **Refusal handling.** A family run stops at its first invalid case and
   retains it. A stopped family may be resumed only by an explicit operator
   action, with at most one further attempt per case and at most five resumed
   attempts per run. A case refused twice leaves its family without a valid
   measurement. Invalid attempts are never deleted or summarized as valid.

## Interpretation notes recorded before measurement

- One child performs one warm-up and five measured repetitions of one case in
  process. Records remain one per repetition. Peak working set is cumulative
  for the child; allocator peak live bytes are per repetition, from the
  documented GMP custom-allocation interface.
- The reference state is computed by the driver with Python integers using
  direct standard-map stepping compared at shortcut boundaries, independent of
  the native candidate code and of GMP.
- Fixed-step families use 2016 shortcut steps, the largest multiple of every
  swept table width not exceeding the I1 crossover budget of 2048, so a table
  route never needs an elementary remainder.
- A hierarchical case is a sequence of affine macro constructions, each at
  most 16384 steps, totalling 16384 represented steps; it is treated as macro
  construction work, not as a fixed-step case. A stricter reading of I1 would
  cap the total at 4096 and make two of the three prescribed caps identical.
  This reading is recorded so a reviewer can reject it explicitly.
- The backend-multiplication family uses case indices 0 to 8: indices 0 to 2,
  3 to 5 and 6 to 8 use multiplier bit-length ratios 1, 2 and 4. One
  repetition is 256 identical exact products so that small sizes are
  measurable with a 100 ns clock.
- The representation family uses indices 0 to 2 for generated dense states
  and 3 to 5 for formula-defined sparse states.
- Families that do not sweep the hierarchical scheduler use the labelled
  harness default divisor 4 and cap 4096. That default is not a selection.

## Amendment 2.1 — bounded admission wait (2026-10-05)

Recorded before the calibration it governs. Run `cal1-20261005-a` completed
the route-crossover family (150 children) under the rules above, with three
retained refusals and two explicit resumes:

| Case | Outcome | Observation |
|---|---|---|
| route-crossover 65536 `affine-small-w04` index 1 | `C1_RESOURCE_ABORT` | two consecutive intervals of about 2053 and 2978 pages per second input; output zero |
| route-crossover 65536 `affine-small-w16` index 2 | `C1_PREFLIGHT_REFUSAL` | two consecutive admission intervals above 100; the case never started |
| small-block-sweep 4096 `affine-small-w16` index 1 | `C1_PREFLIGHT_REFUSAL` | same, with the session otherwise idle; the case never started |

Among the 92 route-crossover children before the first refusal, 7 recorded an
isolated input excursion and none recorded page output; processor performance
never fell below 170 percent of nominal; available memory stayed near 8.4 GB.
Sustained input bursts therefore recur every few minutes from activity that is
not CEML arithmetic. Two of the three refusals occurred before any case work.

Decision `decision.resource-ceilings-v2.1`, changing admission only:

- Admission still requires two consecutive one-second intervals, and now each
  of them must be at or below the 100-page input ceiling with zero output (an
  isolated excursion no longer counts toward admission, which is stricter).
- When page input alone is above the ceiling, the guard defers and keeps
  sampling, for at most 30 one-second intervals in total, then refuses with
  `C1_PREFLIGHT_REFUSAL`. No case work and no measurement occurs while
  waiting, so no sample is being selected; the number of admission intervals
  and deferrals is written into every record.
- Page output, headroom, power, sleep-index, monitor and processor-performance
  conditions still refuse immediately, without waiting.
- The in-case and post-case rules, the abort codes, the resume limits and all
  work bounds are unchanged. A sustained burst during a case still aborts it.

Because the guard program changes, the remaining families run under a new run
identifier, `cal1-20261005-b`, starting again at the small-block sweep. The
partial `cal1-20261005-a` small-block bundle (11 valid children and one
refusal) is retained and indexed but is not used for any decision. Comparisons
are made only within one family and one build identity; the guard is outside
every timed region.

## Not established

No temperature, no power-loss behaviour, no pagefile-specific pressure
measurement and no production resource forecast. Calibration under these
ceilings is engineering evidence only; it is not V1 and not scientific work.
