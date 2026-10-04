# Failure and Lesson Ledger

Status: **Active from bootstrap**

This is a durable record of technical/scientific failures, near misses, rejected assumptions, and lessons that should prevent recurrence.

## Rules

- Do not delete an entry because the problem was later fixed.
- Distinguish observed failure from suspected cause.
- Link the fixing commit/test when available.
- Record whether past results/configurations are invalidated.
- Security-sensitive details may be summarized without exposing secrets.
- A failed scientific run is never silently replaced by a fresh random candidate.

## Entry template

### F-YYYY-NNN — short title

- **Stage:** research / hardware / implementation / validation / scientific / anomaly
- **Date observed:**
- **Affected versions/artifacts:**
- **Observed behaviour:**
- **Expected behaviour:**
- **Evidence/hashes:**
- **Immediate containment:**
- **Root cause:** unknown until demonstrated
- **Corrective action:**
- **Validation of fix:**
- **Impact on prior results:**
- **Lesson / protocol change:**
- **Status:** open / contained / resolved

## Bootstrap entries

No computation failure is recorded at bootstrap because no scientific or production computation is authorized. Open design questions belong in their relevant audit documents rather than being mislabeled as failures.
