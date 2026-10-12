# RUN1 operator runbook — CEML-FRONTIER-2

**Current quantity-only operator procedure — owner update, 2026-10-12:** use `python C:\CEML\tools\operator\run_frontier.py X`, changing only the final positive quantity X. The launcher verifies and discovers the latest committed end E, then covers exactly `[E,E+X)` in sequential batches within the unchanged 14400/256 limits. It reuses the already accepted acknowledgement only for the same verified chain, checks the tracked published anchor and any local receipt, and writes a receipt after each fully verified batch. An incomplete checkpoint never advances E. No fixed pilot digest or repeated acknowledgement entry is required for this continuation procedure. The owner removed the separate-device backup requirement; it is optional and is not a gate or an outstanding task. See `RUN1_ONE_COMMAND.md`. The owner runs the CLI unless explicitly asking the agent to execute a finite quantity. This operator amendment supersedes incompatible manual-procedure wording below; the frozen verifier contract and all historical records remain unchanged.

**Later owner-directed execution and width exception — 2026-10-12:** the owner explicitly requested agent execution of pilot 1 and then the next 1440/following 14400 pilot sequence. All three committed and passed section 7; see `RUN1_PROGRESS.md`. That instruction supersedes the owner-only and gradual-width wording below solely for those pilots. The owner requested a single CLI command for the later 100000 integers; `RUN1_ONE_COMMAND.md` and `tools/operator/run_frontier.py` implement that aggregate invocation with seven sequential batches, full checks between them, the owner's explicit acknowledgement argument, and no change to the frozen verifier or hard limits. The 100000-integer continuation is started by the owner, and is not yet run. During that invocation the verified latest digest is kept in memory; the owner retains the final external aggregate record. The remainder is the original manual procedure and remains applicable to its checks, refusal diagnostics and claim tiers.

**Subsequent completion, same day:** the owner ran that 100000-integer continuation and showed `CONDITIONAL_RUN_COMPLETE`. Read-only confirmation of the saved ten-batch ledger, accepted build, final certificate and reference replay passed. The chain now covers 115984 integers, exclusive end `2392518188130438858000`, latest certificate `5f46665571ef5e85ed629576cd1e7f231ba1c8abe7a7d7975d408d94c14be17a`. The prior "not yet run" wording above is the preparation record. The original launcher command's pilot-3 anchor is now stale; no further continuation is authorised by this completion record. The owner has since removed the separate-device backup requirement.

**RUN1 was authorised by the owner on 2026-10-12 on the operational base**; `PROGRAM_STATUS.md` records the instruction. This runbook is the procedure. The owner runs every command in sections 6 to 10 and types every acknowledgement. The agent that prepared this package acknowledged nothing and ran no batch. Every scientific command still refuses unless the status lines of section 4.3 are present and the batch has its own authority record. The session preflight of section 5 works in any phase, and the read-only commands of section 7 also work on the engineering fixtures.

Use this runbook only while `PROGRAM_STATUS.md` records RUN1 as authorised by the owner. If it does not, stop here.

All commands are PowerShell, run from the repository root, with Python 3.12.10 as `python`. Runtime needs no network and uses none.

## 1. What a batch is and what it proves

A batch is a half-open interval `[S,E)` of consecutive integers. The native worker scans every integer in ascending order and the Python reference then recomputes every integer again. A batch is COMMITTED only when `certificate.json` exists and verifies. A checkpoint, a log line, a partial scan and an INCOMPLETE result prove nothing.

A committed chain from base `B` to `E` supports exactly this statement: *if* every positive integer below `B` converges, *then* every integer in `[B,E)` converges. The base is an assumption you accept. This software does not check it.

## 2. Pinned identities

Check these before every session (section 5). A mismatch means the tree or build changed: stop and investigate.

| Identity | Value |
|---|---|
| Protocol | `CEML-FRONTIER-2` (`docs/FRONTIER_PROTOCOL_V2.md`) |
| Native build digest | `c0263b353e05b9f3d09730e67d321254952c7dbdc2a6d892f7ffe2b14b89c032` |
| Release worker `ceml_frontier.exe` SHA3-256 | `8d3a72aa077fed414ad36e8008900f95a2a0630933e5dea5e66363fd34c19b6b` |
| Checked worker `ceml_frontier_checked.exe` SHA3-256 | `b562e74ba06d7a4f936f3e0010f36142fe7025f8059e60793aea5388820bc525` |
| Checker source digest | `26e5e2e5b235fac140f0ee4afbac064a246f97fec316fb39d955d51659fc3970` |
| Parity table digest | `d368ec417e3170729f67737c414b02ced2d2f6cab349f9cd534404985058391c` |
| Frontier test-source digest | `360343f9cf63d1ed9a9c85d9f6bfe3ae99e30d622231fbf344276aea31fc4a72` |
| Version-2 snapshot digest | `538d319bad77b58ec3b37d653df3213312e260167ad26861e8870e48b276b729` |
| Frozen version-1 snapshot digest (provenance only) | `a511d6b80fc0ea6c85f3926b065e27acc696449af49cfa675d7c1315e85a2d66` |
| GMP runtime `libgmp-10.dll` SHA3-256 | `3eb5419c614771eab626c5d3f7e6cdc64279c4b5cf2eca0a28840baf9b4d75cf` |
| Toolchain | MSVC 14.44.35207, Windows SDK 10.0.26100.0, Python 3.12.10, GMP 6.3.0 release 6.3.0-2 |

The source commit is the one recorded in `docs/L1_V2_ACCEPTANCE.md`. The build digest covers the worker and oracle sources, the driver, reference and build tool, every frontier test, all eight frontier schemas, both snapshots, both protocol documents, the P1 and P2 documents, the pins and the toolchain. It is computed over LF-normalised text, so a CRLF checkout does not change it.

**The build digest is part of every chain's identity.** Editing any of those files, or changing the compiler, gives a different digest. An existing chain then refuses to verify or extend until the original tree and build are restored. Freeze the checkout for the life of a chain.

## 3. Retained offline dependencies

These ignored local files are required and are never downloaded at run time. Back them up with the checkout.

| Path | Content | Check |
|---|---|---|
| `local/c1/cache/sha256/e82a7596…d39ea/mingw-w64-ucrt-x86_64-gmp-6.3.0-2-any.pkg.tar.zst` | GMP binary archive, 592359 bytes | SHA-256 is the directory name; SHA3-256 in `config/c1_gmp_pin.toml` |
| `local/c1/cache/sha256/f288f944…35994/mingw-w64-gmp-6.3.0-2.src.tar.zst` | GMP source archive, 2097066 bytes | same |
| `local/c1/gmp-setup/offline/gmp.h` | extracted header, 84402 bytes | `header_sha3_256` in the pin |
| `local/c1/gmp-setup/offline/libgmp-10.dll` | extracted runtime, 681231 bytes | `dll_sha3_256` in the pin |
| `local/frontier/build/` | the built workers and `build_manifest.json` | `f1_build.py --verify` |

The full directory names are the `binary_sha256` and `source_sha256` values in `config/c1_gmp_pin.toml`. If any file is missing or differs, the build tool refuses with "operator provisioning required". Re-acquiring a dependency is outside RUN1 and needs its own authorisation.

## 4. Before RUN1: the owner's decisions

### 4.1 Choose one base

| | `published` | `operational` |
|---|---|---|
| `B` (exclusive) | `2361183241434822606848` = 2^71 | `2392518188130438742016` = 2175982616 × 2^40 |
| Source | Bařina, *J. Supercomputing* 81:810, published 2025-05-02 | author's project homepage, site generated 2026-10-11T11:29:26Z |
| Tier | peer-reviewed published computational claim | author-reported, not replicated |
| Observed by CEML | 2026-10-11T12:38:06Z, carried forward unchanged | same; **dynamic and may have moved since** |
| Claim tier of a chain | `BATCH_CONDITIONAL_PUBLISHED` | `BATCH_CONDITIONAL_OPERATIONAL` |

Neither base was reproduced by CEML. The two bases are 31334946695616135168 integers apart. One chain directory holds at most 256 batches of at most 14400 integers, that is 3686400 integers, so a published-base chain cannot reach the operational bound. A chain never changes base, and chains with different bases are never joined.

Expect overlap, not novelty. The external project reports completed work far above 2^71, and its first incomplete unit of 2026-10-11 may since have been assigned or completed. A CEML batch in either region is a conditional local verification or reproduction. It is not a world-first and must not be described as one.

### 4.2 The acknowledgement

The acknowledgement is the exact string `snapshot_digest:base_kind:base_B`. For this snapshot it must equal one of:

```text
538d319bad77b58ec3b37d653df3213312e260167ad26861e8870e48b276b729:published:2361183241434822606848
538d319bad77b58ec3b37d653df3213312e260167ad26861e8870e48b276b729:operational:2392518188130438742016
```

By typing it you state: "I accept, as an unverified external assumption, that every positive integer below this `B` converges, on the evidence tier named in this snapshot." It records your acceptance. It is not evidence that the assumption is true. No tool fills it in for you.

### 4.3 RUN1 authority

All three are required. The first two are the owner's acts.

1. A fresh explicit owner instruction to start RUN1, naming the base kind.
2. A committed status transition in `PROGRAM_STATUS.md` so that it contains exactly one line of each form:

   ```text
   **Authoritative current phase:** RUN1
   **Scientific execution authorization:** AUTHORISED
   ```

   The phase line may continue with ` — ` and text. The authorisation line must end at `AUTHORISED`.
3. For **each batch**, a local authority record written by `prepare-authority` (section 6). One record covers exactly one interval.

Run the complete acceptance suite one last time **before** the status transition. The suite and `selftest` are L1-phase checks and refuse or fail by design once the phase is RUN1. After the transition use the session preflight in section 5.

Authority template to fill in and keep with the run records:

```text
RUN1 authority
Date (UTC):
Owner instruction (verbatim):
Base kind chosen: published | operational
Acknowledgement string typed by the owner:
Authority identifier (letters, digits, _ . : -):
Run identifier (new, never reused):
Assumption accepted in the owner's words:
```

## 5. Session preflight (every session, before any batch)

```powershell
python tools/frontier/f1_build.py --verify
```

```powershell
python tools/frontier/ceml_frontier.py rules
```

```powershell
python tools/frontier/ceml_frontier.py snapshot --file config/frontier_snapshot_v2.json
```

```powershell
git status --short
```

Require `"status": "PASS"` with the build digest and worker hash of section 2, `rules_pass` with the table digest of section 2, `research_only_unaccepted` with the snapshot digest of section 2, and an empty `git status`. If a chain already exists, also run the ledger audit of section 7 and compare it with your external record (section 8).

## 6. The initial 144-start pilot

Set the names once per session. Use a new run identifier for every new chain.

```powershell
$runId = 'RUN1-published-0001'
$authorityId = 'RUN1-owner-2026-xx-xx'
$kind = 'published'
$ack = '<the acknowledgement string you are accepting, from section 4.2>'
$chain = "local/frontier/run1/$runId"
$manifests = "local/frontier/run1/$runId-manifests"
New-Item -ItemType Directory -Force $manifests | Out-Null
```

The first batch is `[B, B+144)`. For the published base that is `[2361183241434822606848, 2361183241434822606992)`. For the operational base it is `[2392518188130438742016, 2392518188130438742160)`.

Record authority for exactly this batch:

```powershell
python tools/frontier/ceml_frontier.py prepare-authority --authority-id $authorityId --base-kind $kind --batch-start 2361183241434822606848 --batch-end 2361183241434822606992 --acknowledge $ack --owner-instruction "<the owner's instruction, ASCII>"
```

Write the manifest. The budgets shown are the protocol maxima and are finite:

```powershell
python tools/frontier/ceml_frontier.py prepare-manifest --out "$manifests/batch-0001.json" --authority-id $authorityId --acknowledge $ack --max-t-per-explicit 100000 --max-total-t 2000000 --run-id $runId --base-kind $kind
```

Run the batch:

```powershell
python tools/frontier/ceml_frontier.py pilot --manifest "$manifests/batch-0001.json" --out "$chain/batch-0001"
```

`"status": "COMMITTED"` with a `digest` means the certificate exists. `"status": "INCOMPLETE"` means a start is pending and nothing was committed: go to section 10. `"status": "REFUSED"` means nothing was promoted: go to section 10.

Do not propose the next batch until section 7 passes for this one.

**First-execution note.** L1 was not allowed to run a scientific batch, so this pilot is the first end-to-end execution of the authorised path. In L1 that path was exercised through the worker only for the single integer 10000 under a synthetic status file, and through the driver only with the scan mocked. If the first pilot refuses for a reason that section 10 does not explain, stop. A refusal promotes nothing. A code fix at that point needs review and changes the build identity, which is harmless only because no chain exists yet.

## 7. Verify, replay and audit

```powershell
python tools/frontier/ceml_frontier.py verify-batch --certificate "$chain/batch-0001/certificate.json"
```

```powershell
python tools/frontier/ceml_frontier.py replay --batch-dir "$chain/batch-0001"
```

```powershell
python tools/frontier/ceml_frontier.py ledger --dir $chain
```

```powershell
python tools/frontier/ceml_frontier.py inspect --batch-dir "$chain/batch-0001"
```

- `verify-batch` re-reads the certificate, re-checks the build, snapshot, manifest and the whole predecessor chain, and recomputes every integer of every batch back to genesis. Expect `conditional_complete`.
- `replay` recomputes one batch with the pure-Python reference only. It checks arithmetic, not the chain, build or authority. Expect `REFERENCE_REPLAY_MATCH`.
- `ledger` audits the whole chain once from genesis: no gap, overlap, duplicate or fork. Expect `conditional_chain`, with `start` equal to `B`, and the `genesis_digest`, `latest_certificate_digest`, `batches` and `end` you record in section 8.
- `inspect` is a read-only diagnosis of one batch directory: slot states, the recoverable generation, warnings and whether a certificate is present.

## 8. Continuation receipts and external aggregate record

After every fully verified batch, the quantity-only launcher records `genesis_digest`, `latest_certificate_digest`, `batches` and `end` atomically in `local/frontier/operator_tip.json`, outside the batch directories. It checks that retained receipt and the locally frozen tracked aggregate record against the audited chain before continuation. The current verified end is discovered from `ledger`, not from a partial checkpoint, a receipt alone or a fixed prompt. The owner does not need to paste a changing digest. An explicit `--expected-latest` pin remains available when desired.

Keep the final printed values with the aggregate progress record; publishing that record provides an external comparison point without adding a network dependency to scientific execution. A local receipt is not independent reproduction, authentication or protection against replacement/rollback of all local files together. If the actual chain is shorter than a retained anchor or contains a different certificate at that anchor, stop. Full replay and chain audit remain required even when every receipt matches.

The owner explicitly removed the separate-device backup requirement on 2026-10-12. Backups are optional, and their absence is not an outstanding task or a reason to block continuation. After any restore or power failure, verify the accepted build and audit the whole chain before proceeding; never overwrite a more advanced chain with an older copy. No durability or rollback-detection capability is claimed beyond the retained evidence.

## 9. Contiguous extension

Each later batch starts exactly where the previous certificate ended. Authority is recorded again for the new interval.

```powershell
python tools/frontier/ceml_frontier.py prepare-authority --authority-id $authorityId --base-kind $kind --batch-start <previous batch_end> --batch-end <previous batch_end + width> --acknowledge $ack --owner-instruction "<the owner's instruction, ASCII>"
```

```powershell
python tools/frontier/ceml_frontier.py prepare-manifest --out "$manifests/batch-0002.json" --authority-id $authorityId --acknowledge $ack --max-t-per-explicit 100000 --max-total-t 2000000 --after-certificate "$chain/batch-0001/certificate.json" --width 144
```

```powershell
python tools/frontier/ceml_frontier.py pilot --manifest "$manifests/batch-0002.json" --out "$chain/batch-0002"
```

`prepare-manifest --after-certificate` verifies the whole predecessor chain first and inherits the run identifier, base and build identity from it. Then repeat sections 7 and 8.

**Width policy.** Batch 1 is 144 by rule. Keep batch 2 at 144. After that, raise the width only on your own measured batches: at most double it after a batch that committed and passed section 7, never above 14400, and go back to the previous width after any INCOMPLETE or REFUSED result. L1 measured only small-integer fixtures (section 12). Speed at 2^71 is unknown until your first batches measure it.

**Hard limits.** Width 1 to 14400. At most 256 batches in one chain directory; a 257th is refused before it is created. Per-start budget at most 100000 shortened-map steps and per-batch budget at most 2000000. The worker has a 30-second wall budget per scan. One worker, one batch at a time. Every new batch re-verifies the whole chain, so time per batch grows with chain length. Every chain starts at its base and cannot be continued by a second chain, so with this build one base supports at most 256 × 14400 = 3686400 verified integers. This is a pilot-scale tool. L1 exercised chains of two batches only; the 256 limit was tested by lowering it, not by building 256 batches.

## 10. Stop, resume and refusal diagnostics

**Stopping.** Let the current command finish, or press Ctrl+C. Interrupting is always safe: a batch is committed only if `certificate.json` exists and verifies. Never delete or edit anything in a batch directory.

**Resuming an uncommitted batch.** The authority record must still be the one for that batch (re-run `prepare-authority` for its interval if you have since recorded another).

```powershell
python tools/frontier/ceml_frontier.py inspect --batch-dir "$chain/batch-0002"
```

```powershell
python tools/frontier/ceml_frontier.py resume --batch-dir "$chain/batch-0002"
```

Resume recovers the newest authenticated checkpoint generation, re-scans its prefix, then re-scans the whole batch from its start and commits only a complete result. A `warnings` entry means a checkpoint slot was damaged or missing and an older generation was used; the result is still fully recomputed, but note the warning and check your storage.

| Message contains | Meaning | Action |
|---|---|---|
| `RUN1 not owner-authorised` | the phase is not RUN1, or scientific execution is not `AUTHORISED` | owner decision; do nothing else |
| `missing/duplicate authoritative status field` | one of the two status lines of 4.3 is absent or appears more than once, or `PROGRAM_STATUS.md` has Windows (CRLF) line endings, which the driver's parser refuses | the status file is malformed; restore it from Git (`.gitattributes` keeps it LF) or have the owner correct it |
| `L1 inspects and replays only predesignated fixtures`, `L1 verifies only predesignated fixtures`, `L1 ledger accepts only fixtures` | a read-only command was used on a scientific directory outside RUN1 status | owner decision; do nothing else |
| `selected external B mismatch`, `snapshot identity mismatch`, `snapshot provenance does not match` | the manifest or the stored snapshot is not the pinned one | regenerate the manifest with `prepare-manifest`; never edit one by hand |
| `RUN1 authority evidence shape`, `does not cover this batch`, `fresh RUN1 owner authority missing` | authority record absent, altered, or for another interval | re-run `prepare-authority` for this exact batch |
| `acknowledgement is not snapshot_digest:base_kind:base_B` | acknowledgement string wrong | re-read 4.2; type it exactly |
| `first RUN1 pilot is exactly 144 starts` | first batch width is not 144 | use 144 |
| `Native build … mismatch`, `rebuild required`, `native build identity mismatch` | tree or build differs from the chain's | restore the pinned tree and build; never edit to match |
| `operator provisioning required`, `checksum mismatch` | a retained dependency of section 3 is missing or changed | restore from backup |
| `batch directory already exists` | `--out` exists | use `resume` for that batch, or a new name for a new batch |
| `another batch of this chain is uncommitted` | one batch is still active | finish, resume or quarantine it first |
| `duplicate/overlapping batch; rerun needs a new run ID` | the interval is already present in this chain | never re-run a committed interval under the same run ID |
| `missing/duplicate immutable predecessor`, `predecessor chain gap/identity mismatch`, `genesis mismatch` | the chain is broken before this batch | stop; restore the chain from backup and re-audit |
| `no independently valid checkpoint`, `missing/damaged checkpoint predecessor generation`, `checkpoint fork/orphan/gap generation`, `checkpoint cursor rollback`, `slot/generation mismatch`, `root checkpoint is not the empty prefix` | checkpoint history cannot be authenticated | quarantine the attempt (below) |
| `foreign or cross-version checkpoint record` | a file that is not a version-2 checkpoint sits in a slot | quarantine the attempt; find out how it got there |
| `batch already has a final certificate; use verify-batch` | the batch is committed | run section 7 |
| `record digest mismatch`, `noncanonical JSON bytes`, `certificate full replay mismatch`, `checker source identity mismatch` | a committed record or the checker changed | stop; this chain member is not trustworthy as stored; restore and re-audit |
| `checkpoint run mismatch`, `checkpoint identity mismatch`, `prefix replay mismatch`, `claimed prefix is not completely resolved`, `self-hashed checkpoint is not stored canonically` | a checkpoint contradicts its batch or the recomputed prefix; it is a lying record, not a torn one | quarantine the attempt; keep it for review |
| `resume native prefix mismatch` | the worker's re-scan of the recovered prefix disagrees with the checkpoint | stop; keep the directory; report it as an anomaly |
| `certificate cycle/depth limit`, `local chain directory resource limit` | the chain directory already holds 256 batches | the chain is full; every chain starts at its base, so this build cannot verify further from this base (see the hard limits in section 9) |
| `"status": "INCOMPLETE"` with `step_budget` or `total_budget` | a start did not descend within the budget | see pending starts below |
| `ambiguous native success`, `missing/ambiguous native failure status`, `native wall budget` | the worker died, hung or misreported; for the first two an anomaly record is written under `local/frontier/refusals/` | keep the record; `inspect`, then `resume` once; if it repeats, stop and report |
| `FileNotFoundError`, `PermissionError` | a required file is missing or locked, most often the authority record or a record file | check the path; re-run `prepare-authority` if the authority record is the missing file |

**Pending starts.** With the maximum budgets, a pending start is an anomaly: preserve the directory, record the `pending` object, do not retry, skip or reorder, and report it for separate review. It is not evidence of divergence. If the budgets or the width were chosen too small, quarantine the attempt and restart the same start with the maximum budgets or a smaller width.

**Quarantining an abandoned uncommitted attempt.** Only for a batch directory with **no** `certificate.json` that cannot proceed. Move the whole directory out of the chain directory, keep it, and write down why:

```powershell
New-Item -ItemType Directory -Force "local/frontier/run1/$runId-quarantine" | Out-Null
Move-Item "$chain/batch-0002" "local/frontier/run1/$runId-quarantine/batch-0002-attempt-1"
```

Then prepare authority and a manifest again for the same start and predecessor (a new manifest file name), and run `pilot` into a new directory name. The new manifest may differ from the abandoned one only in its end and its two budgets. Never move, delete or re-run a directory that contains `certificate.json`.

**Never:** edit or delete a record; copy a checkpoint or certificate between directories; reuse a run identifier for a new chain; change base inside a chain; run two batches at once; change tracked files during a chain; describe an INCOMPLETE or checkpoint-only batch as verified; let any tool or agent type the acknowledgement or authority for the owner.

## 11. Independent reproduction handoff

The built-in second pass is a separate Python implementation, but it shares author, machine, operating system and input with the first pass. It is a strong internal check. It is **not** an independent reproduction.

**Same-code reproduction on another machine.** Give the other party the source commit that carries the RUN1 status lines (the read-only commands refuse on any other status), the files of section 3, and a copy of the chain directory. With the same pinned toolchain they build with `python tools/frontier/f1_build.py`, must obtain the build digest and worker hash of section 2, and run `ledger --dir <chain>`. With only Python 3.12.10 and no compiler they can still run `replay --batch-dir` on each batch, which needs no build. This shows the records are reproducible from the same code. Report it as a same-code re-execution.

**Independent reproduction.** A different person writes their own program from the protocol, not from this code, and recomputes each certificate. `docs/FRONTIER_PROTOCOL_V2.md` sections 1 and 3 are the complete specification. For a certificate with `batch_start=S`, `batch_end=E` and the manifest's `max_t_per_explicit`:

1. For each `n` from `S` to `E-1`, choose the first applicable rule in the order E2, Q4, P3, M9, S2K4-03, EXPLICIT.
2. Compute the witness: E2 `n/2`; Q4 `3(n-1)/4+1`; P3 `(2n-1)/3`; M9 `(8n-5)/9`; S2K4-03 `(9n+5)/16`; EXPLICIT the first iterate of `T` below `n`, counting `steps` and the number of `odd` steps, with `steps=odd=0` for the five algebraic rules.
3. Form the frame `n|rule|steps|odd|witness` followed by one newline byte, all numbers in plain decimal.
4. Compute SHA3-256 over the ASCII bytes `CEML-FRONTIER-2/EVENTS`, one zero byte, then every frame in order.
5. Compare with the certificate: the digest with `transcript_digest` and `independent_replay_digest`; the per-rule counts with `counts`; the sums of `steps` and `odd` with `explicit_t_steps` and `explicit_odd_steps`.

Only a result obtained this way, by different code and a different build, may be reported as `INDEPENDENT_REPRODUCTION`. `GLOBAL_FRONTIER_EXTENSION` additionally needs contemporaneous independent evidence about every earlier work unit and about priority; nothing in this package provides that.

## 12. Measured L1 calibration

Measured on this machine by the L1 self-test on small-integer engineering fixtures. Times include the build check, the native scan, the per-frame check, both Python replays, the checkpoint writes and the certificate commit. They are overhead measurements on integers below 10000. They are not throughput at 2^71, and no speed at that magnitude has been measured.

Source: the OS-blocked acceptance run of 2026-10-12 (evidence run 387ae837, network blocked by Windows Firewall for the whole measurement).

| Fixture | Interval width | Explicit starts | Explicit steps | Scan and per-frame check (s) | Whole batch (s) |
|---|---:|---:|---:|---:|---:|
| `L1-fixture-a` | 144 | 15 | 269 | 0.084 | 0.418 |
| `L1-fixture-successor` | 144 | 15 | 150 | 0.085 | 0.734 |
| `L1-fixture-b` | 144 | 15 | 150 | 0.084 | 0.406 |
| `L1-fixture-c` | 96 | 10 | 225 | 0.084 | 0.406 |
| `L1-fixture-wide` | 9600 | 1001 | 11840 | 0.269 | 0.928 |

`L1-fixture-successor` is the second batch of a two-batch chain, so its whole-batch time includes re-verifying its predecessor. The two-batch ledger audit took 0.370 s. Directory flush was reported `yes` on this volume.

## 13. Truthful claim template

Fill in every field from the records; delete nothing.

```text
CEML-FRONTIER-2 conditional batch chain
Run identifier:
Base kind and tier: published (peer-reviewed) | operational (author-reported, not replicated)
Assumed, not verified by CEML: every positive integer below B = <B> converges
  Source and its date:                      CEML observation time (UTC): 2026-10-11T12:38:06Z
Verified conditional on that assumption: every integer in [<B>, <E>) converges
Batches:        Genesis digest:        Latest certificate digest:
Snapshot digest:        Native build digest:        Source commit:
Rule counts (E2, Q4, P3, M9, S2K4-03, EXPLICIT):        Unresolved: 0
Explicit shortened-map steps computed:        Run dates (UTC):
Independent full replay performed: yes, built-in second pass (same author and machine)
Independent reproduction by other code: none | <who, when, what>
Overlap with externally reported work: expected; not checked against the external project's current state
This is a finite, conditional computational result. It is not a proof of the Collatz conjecture, not a
reproduction of the base, and not a claim of a world-first or of global frontier extension.
```
