# C1 continuation after initial local audit

Stage: **hardware characterization**. **CEML-C1 REMAINS OPEN.**

The initial session verified clean `main` at the authoritative I1 baseline
`e2148e47f4cc71ba33bfc5c05140d2adef32f479`. It read the controlling documents,
collected narrow Windows observations, recorded initial resource ceilings before
tool discovery, and investigated only eligible candidate tools/packages.

## Blocking evidence and scope

No usable GMP development package or offline source/package inputs were
established at the checked MSYS2, MinGW, vcpkg and configured/default Cargo
candidate-cache locations. This is a scoped availability finding, not a claim
that no copy exists anywhere on the machine. Rust and Python version queries
succeeded. Selected Visual C++ compiler/linker file-version fields were observed,
but its build environment was not activated and no candidate was compiled.

All eligible I1 production families require GMP directly or through rug.
Python is reference/orchestration only. No replacement backend, download,
installation, upgrade or environment activation was performed.

Initial resource ceilings are in `docs/C1_RESOURCE_CEILINGS.md`. The first paging
sample exceeded the conservative admission threshold. No non-trivial case was
started. A small generator/framing self-test is engineering tooling evidence;
it is neither a performance measurement nor V1 evidence.

The NTFS target was observed, but no checkpoint interruption/recovery matrix was
executed and no durability guarantee was established. In particular, observing
NTFS or successfully writing a report does not demonstrate durable checkpoint
promotion. Checkpoint storage remains unsupported for scientific use pending
the full required evidence; this is not a claim that NTFS cannot support it.

No production architecture, compiler mode, block schedule, backend, allocation
policy, terminal route, audit mode, checkpoint strategy or performance winner
was selected. No production engine, BUILD_MANIFEST, frozen machine profile or
offline production lock was manufactured to fill an incomplete artifact set.
PROGRAM_STATUS remains unchanged: C1 open; V1 and E1 not entered.

## Exact continuation task

Continue CEML-C1 only from the commit containing this file. Read AGENTS.md,
PROGRAM_STATUS.md, PROJECT_CHARTER.md, R4/I1 and the requested read-order documents.
Verify the I1 baseline remains an ancestor and inspect this session's reports,
decisions and tooling. Do not weaken frozen contracts.

1. Obtain an operator-specified existing local GMP development/source/package
   location, or separate explicit authorization for an exact dependency/toolchain
   acquisition and setup action. Do not download or activate missing components
   merely because C1 is open. Establish compatibility with an I1-eligible C17,
   C++20 or Rust/rug family and retain exact license/provenance/content digests.
   Confirm offline reconstruction inputs before selecting the stack.
2. Rerun the privacy-minimized hardware/tool audit after any environment change.
   Reobserve memory, storage, paging and power. Re-establish conservative ceilings
   and implement preflight, child memory/time limits, aggregate limits and safe
   mid-case monitoring before non-trivial calibration. The initial stricter
   subset has no permission to expand implicitly.
3. Reproduce the normative CEML-CAL-1 vector. Build only bounded candidate and
   independent reference harnesses. Run the applicable twelve-family matrix
   within I1 and local bounds in the specified order. Record exact correctness,
   positive REQUIRE route activation without fallback, complete build context,
   repeats, median/MAD and resource observations. Apply the exact I1 5% winner,
   noise, tie-break and refusal rules; select no unmeasured winner or crossover.
4. On the same intended checkpoint filesystem/mount class, establish documented
   atomic-promotion and directory/pointer durability semantics, then run bounded
   synthetic CKPT-1 writes, flushes, reopen verification, A/B retention and unique
   recovery. Force process interruption at all R4 section 14.5 phases and use
   fresh-process recovery. The I1 section 11.9 reference to R4 section 10 is a
   stale cross-reference; the substantive matrix is R4 section 14.5. Never
   weaken the matrix or perform unauthorized destructive power-cut testing.
5. Create evidence-backed engineering selections/refusals. Only then change the
   stage label to implementation and implement the selected engine with every
   I1 component boundary, invariant, CLI authorization gate and twelve future
   V1 hooks. Do not execute V1.
6. Pin the selected build with both native/ecosystem locks and a CEML dependency
   provenance manifest; retain approved offline source/package material. Build
   offline, bind source/toolchain/ABI/flags/dependencies/routes/artifact bytes,
   and rerun calibration invalidated by the final implementation/build.
7. Produce every required schema-valid C1 report, bundle index, build manifest
   and profile. Recompute the engineering-domain digests. Scan exact staged
   artifact bytes and generated Markdown, inspect/present the sanitized diff,
   and commit. Update PROGRAM_STATUS only with evidence satisfying C1 in the
   same commit. Report PASS only when every C1 exit condition is satisfied.
8. Stop before V1, E1, scientific seed/start work and final ladder freeze.

## Reusable audit tooling

Run the two PowerShell collectors explicitly from the repository:

```powershell
& tools\c1\collect_windows.ps1
& tools\c1\collect_tools.ps1
python tools/c1/engineering_codec.py self-test
python -m unittest discover -s tests/c1 -v
```

Their intermediate observations stay under ignored `local/c1/`. The report
assembler is specific to the initial refusal session; it must not be reused to
claim a successful later calibration or build. The privacy gate examines staged
Git blobs, so stage the intended artifacts first, then run:

```powershell
python tools/c1/privacy_gate.py
git diff --cached --check
git diff --cached
```

Do not commit a scan report claiming to include its own final bytes. Retain the
gate output locally and record its verification in the commit description.
Do not change the staged set between the final successful scan and commit.
Audit-tool unit checks are
not CEML-V1-SUITE-1 and cannot be promoted into V1 evidence.
