# CEML-L1 version-2 acceptance record

Dates: work 2026-10-11 to 2026-10-12; recorded 2026-10-12. **Decision: CEML-L1 REMAINS OPEN. One gate is left: the OS-blocked acceptance run, which the owner starts (section 6).**

This record covers the owner-authorised focused continuation of the single L1 attempt. It replaces nothing in `docs/L1_ACCEPTANCE.md`, which remains the record of the first candidate. No scientific interval, frontier integer, accepted base or RUN1 step was executed.

## 1. Entry state

Live `main` and local entry were `abd5d5bd0c6bb3a5cfbd1b83d52122b04d324016`. The work branch `codex/l1-offline-frontier` was clean at `ba9ba9e137222ad9c08d3d1a6601be48633b6ad7`, the head of draft PR #5 (open, unmerged, mergeable, no status checks). The repository has no workflow files and zero Actions runs. No hosted CI result exists or is claimed.

Before any edit, on that entry tree: `f1_build.py --verify` PASS with version-1 build identity `c8e91ba7…c50b87`; `tests/frontier` 92 tests OK and `tests/l1` 8 tests OK, no skips.

## 2. What the continuation delivered

| Deliverable | Where |
|---|---|
| Frozen version-2 contract | `docs/FRONTIER_PROTOCOL_V2.md` |
| Four version-2 schemas | `schemas/frontier_{snapshot,run,checkpoint,certificate}_v2.schema.json` |
| Carried-forward research snapshot with provenance | `config/frontier_snapshot_v2.json` |
| Three-slot store, root generation, recovery, version-2 domains | `tools/frontier/ceml_frontier.py`, `reference.py`, `f1_build.py` |
| Recovery, gate, fault, cross-version and operator tests | `tests/frontier/test_recovery.py`, `test_gates.py`, `test_operator.py`, and the updated suites |
| Hardened OS-isolation launcher and helper | `tools/l1/` and `tests/l1/` |
| Offline operator package | `docs/RUN1_OPERATOR_RUNBOOK.md` |
| Bounded review prompt | `docs/L1_REVIEW_PROMPT.md` |

**Unchanged, verified by `git diff`:** the native worker (`git diff c7b0249 -- src/` is empty, and the release worker hash is still `8d3a72aa…c19b6b`, as recorded for the first candidate); the version-1 protocol, audit, four schemas and snapshot; the P1 proofs; both dependency pins; all C1 tools, tests, sources and reports.

**Decisions made beyond "three slots".** Each is stated in the protocol's amendment record or in section 5 below.

1. *Generation 0 is an empty-prefix root written at batch creation.* The first candidate wrote its first checkpoint only after the scan, so a process death during the scan left a directory that neither `pilot` nor `resume` would accept. The root also makes the one sole-record case safe by construction, because it asserts no progress.
2. *Identities use LF-normalised text.* Git on this machine converts line endings on checkout. The first candidate also hashed raw bytes, so re-checking out the branch would have changed the build identity and stranded any chain.
3. *The located compiler environment is cached per process.* Every build check previously re-ran the compiler locator, about 1.8 s each time. The five compiler binaries are still re-hashed on every call; a test changes one and observes the refusal. No scientific code path changed.
4. *The authority record is copied into each batch directory*, because one record covers one batch and is replaced for the next.
5. *Operator commands* `prepare-authority`, `prepare-manifest`, `inspect` and `replay` were added so that RUN1 needs no code work. The first two refuse outside RUN1 status and never fill in the acknowledgement.
6. *One wider fixture* `[2,9602)` was predesignated. The 144-start fixtures fit in a single pipe read; this one crosses many, which is the path every frontier-magnitude batch will take.
7. *Starting a batch checks the build and the predecessor before creating the directory*, so the common refusals leave nothing behind.
8. *Read-only commands and the driver's magnitude gate need full RUN1 status*, not the phase alone, and the driver uses the worker's own boundary (any scan ending above 10000).

One decision was made and then withdrawn: a test that scanned the single integer 10000 under a synthetic RUN1 status. It is disclosed at the end of section 5.

## 3. Commands and observations

Every row was executed in this session on the final committed sources unless it says otherwise.

| Check | Verdict | Observation |
|---|---|---|
| `python tools/frontier/f1_build.py --show-command` | PASS | prints the release and checked command lines without compiling |
| `python tools/frontier/f1_build.py` | PASS | release and checked workers compiled locally from the retained pins |
| `python tools/frontier/f1_build.py --verify` | PASS | separate clean rebuild; all nine artifact hashes equal |
| `python tools/frontier/ceml_frontier.py rules` | PASS | 16 parity rows, 144 assignments, fixed witnesses, bounded identities |
| `… snapshot --file config/frontier_snapshot_v2.json` | PASS | 956 canonical bytes; `research_only_unaccepted`; provenance verified against the frozen version-1 file |
| `… snapshot --file config/frontier_snapshot_v1.json` | PASS | `frozen_version_1_research_only_not_runnable`; 632 bytes; digest `a511d6b8…5a2d66` unchanged |
| `python -m unittest discover -s tests/frontier` | PASS | 171 tests, no failures, errors or skips, about 60 s |
| `python -m unittest discover -s tests/l1` | PASS | 18 tests, no skips; includes a real launcher preflight and four real refused `-Mode Run` invocations |
| `python tools/frontier/ceml_frontier.py selftest` | PASS | five fixtures committed; two-batch ledger audited |
| Complete acceptance plan, unisolated rehearsal (`tools/l1/offline_acceptance.py --run`) | PASS, **not acceptance evidence** | all ten checks; three equal build digests; both suites with zero skips |
| `run_offline_acceptance.ps1 -Mode Preflight` | PASS | read-only; firewall prerequisites PASS; elevation required |
| `run_offline_acceptance.ps1 -Mode Run`, unelevated | REFUSED, as designed | stops at the administrator check; nothing changed |
| Mutation check, 56 deliberate defects, final tree | 55 detected, 1 equivalent | section 4 |
| OS-enforced network-blocked build and acceptance | **NOT_RUN** | awaits the owner; section 6 |
| `tools/c1/gmp_setup.py build` and `offline-smoke` | not re-run | the legacy tool is unchanged; its refusal outside C1 is recorded in `docs/L1_ACCEPTANCE.md` |
| GitHub Actions | none exist | zero runs is not green CI |
| Scientific interval, RUN1, old V1/E1 | NOT_RUN | not authorised |

Failures met on the way are part of the record. The first version of the batch tests took five minutes because each build check re-located the compiler; that led to decision 3. A class attribute named `run` shadowed the test runner's method and was renamed. Three shell patch attempts were rejected by the shell's quoting and redone as files. The first mutation round left one survivor and the second left one weak test; both are described in section 4. The independent review found one blocker and three major defects in the first candidate commit, and its confirmation pass, interrupted once by a usage limit and resumed, found two further minor ones; section 5.

## 4. Recovery acceptance

The three-slot decision is tested against a model written independently in the test file (`model` in `tests/frontier/test_recovery.py`), not against the driver's own logic. The independent reviewer separately compared the code with its own decision table over 703 states.

| Obligation (protocol section 5) | Evidence |
|---|---|
| 8. every slot state through generation 4 | 165 states: newest generation 0 to 6, each slot intact, damaged or absent; outcome, warning, read-only recovery, next write and retention of the last two generations all checked |
| 9. damaged and missing newest, predecessor, oldest; duplicates, forks, gaps, slot mismatch, rollback, root violations, overflow | 16 self-hashed contradictions at every retained position for newest 1 to 5; lower-cursor child; cursor moved past pending work; fork with a valid sibling; wrong, swapped and rotated slots; duplicate generations; root with progress or pending work; generation bound on read and write; six damage kinds; self-hashed but shape-invalid or non-canonical records |
| 10. every fault point | eight named points, in process for generations 1 to 6 and the root, by real process death for generations 1 to 5, the root and the certificate |
| 11. pending excluded from coverage | five generations of the same pending start, fallback past a damaged newest slot, forged advances refused; native repeated resume through generation 4 stays INCOMPLETE |
| 12. prefix replay and cold versus resume equality | resume observed to scan `[2,31)` then `[2,146)`; a lying native prefix refused in seven ways; certificates byte-equal to the cold one from four fallback recoveries and from a native death after the root |
| 13. cross-version refusal | version-1 checkpoint, run, snapshot and certificate shapes; version-1 digest domain and genesis; version-1 certificate as predecessor; fifteen foreign records in every slot at five generations |
| 14. OS-enforced blocked run | **open**; section 6 |

**Mutation check.** Deliberate defects were applied one at a time to a scratch copy of the driver, and the tests that need no native build were run against each. The repository was not modified.

- Round 1 (19 recovery defects): 18 detected. The survivor was the slot rule; a test for swapped and rotated slots was added and it is now detected.
- Round 2 (52 defects: the 19 above and 33 covering every check the independent review found untested, plus its blocker and major findings): 50 detected at first. One survivor showed that the `replay` gate test refused for the wrong reason, because its forged certificate was shape-invalid; the forgery was made shape-valid and correctly bound, and that defect is now detected. The other survivor is equivalent: the write-side generation bound is duplicated by the same check inside record validation, so deleting either one alone changes no behaviour.
- Final run on the final tree (56 defects: the 52 above and four for the confirmation-pass fixes): 55 detected, and the same single equivalent survivor.

The reviewer ran its own deletion experiments as well, 23 on the first candidate and 43 on the fix commit; section 5.

## 5. Independent review

**Provenance.** The review was done by a separate review sub-agent started from the authoring session at the owner's instruction ("Use an independent review sub-agent, resolve its findings"). It ran in its own context and was given only the bounded prompt `docs/L1_REVIEW_PROMPT.md` and a short brief, not the author's notes or reasoning. It was read-only on tracked files, used no network and ran nothing elevated. It reviewed local commit `638e3329b37e9de66b76173280f111771d7cb65e`, with a clean tree at its start and end.

**What "independent" means here.** The reviewer is a different instance with a different context. It is the same model family from the same vendor as the author, so it can share blind spots, and it is not a human or a different tool. `docs/L1_REVIEW_PROMPT.md` is kept so the owner can obtain a further opinion from a separate session or person against the final commit.

**What it ran.** Both suites (138 and 18 tests at that commit, no failures, errors or skips); `f1_build.py --verify`; every runbook command line under the real L1 status; and eight experiments of its own. Those included its own section-4.5 decision table compared with `recover` and `write` over 703 slot states (intact, damaged, absent, foreign and stale, newest generation 0 to 7), a recomputation of every runbook identity, and 23 single-check deletions each followed by the full frontier suite. It scanned nothing at or above 10000.

**Its findings and their resolution.** It reported one blocker, three major and eight minor findings and six notes. (Its closing sentence says "four MAJOR"; the report lists three.) Every finding was accepted. None was disputed.

| # | Severity | Finding at `638e332` | Resolution | Evidence |
|---|---|---|---|---|
| 1 | BLOCKER | `inspect` and `replay` treated the mere existence of `acceptance.json` as proof of a fixture, so the Python reference could be run on any manifest at any magnitude while the status said L1. No certificate or chain effect; the native gate was unaffected. | Both commands now pass `read_only_gate` first: the exact marker and the exact predesignated interval, or RUN1 status with a valid scientific manifest, before any slot is read or any start recomputed. | `ReadOnlyCommandGateTests` (arithmetic and slot access replaced by failing sentinels, including a 2^71 manifest) and a command-line test with bogus markers |
| 2 | MAJOR | A self-hashed checkpoint whose `next_n` had been moved past the first unresolved start, keeping the honest counters, was accepted as an authenticated record. It could not produce a certificate. | The independent prefix replay must itself reach `next_n` with nothing unresolved, and the categories must sum to `next_n - S`. Resume also requires the native prefix to be complete to the recovered cursor. | the reviewer's exact forgery for both budget kinds and three cursors; `test_resume_requires_complete_and_equal_native_prefix` |
| 3 | MAJOR | Fifteen required checks had no effective test: deleting each left the suite green. The shipped code was correct in every case exercised. | One negative test per check, asserting the refusal reason: resume prefix equality, predecessor gap and identity, duplicate predecessor, ledger duplicate and adjacency, generation bound on read and write, the Python magnitude gate, resume beside a certificate, run-ID reuse, cycle and depth, the directory limit, wall, pipe, event and extra-frame limits, and `l1_gate` and `selftest`. Two of its survivors are redundant with neighbouring checks and were left. | `tests/frontier/test_gates.py`; mutation round 2 below |
| 4 | MAJOR | By reading only: the launcher and the watchdog both inferred "rules absent" from lookups that suppressed errors, and the launcher removed the watchdog before observing reconnection. A failed query could then leave the block rules with no watchdog. | Both now enumerate the whole store with errors terminating, so an empty result means absent. The watchdog exits 1 on any doubt, stays registered, repeats every 5 minutes for 12 hours and still fires at boot. The launcher removes it only after verified absence and an observed reconnection. | static launcher tests; in-memory construction of the task objects; **not executed elevated** |
| 5 | MINOR | The directory limit admitted a 257th batch that verification then refused for ever. | The new batch counts toward the limit; both bounds use one constant. | `test_directory_limit_equals_the_verifiable_chain_length` |
| 6 | MINOR | The RUN1 gate accepted a blank or non-string owner instruction. | Every member must be a string and the instruction non-blank. | authority tests |
| 7 | MINOR | Protocol prose said two damaged slots above the root refuse; the rules, the code and the test model accept the root. | Prose corrected. Falling back to the root is safe because the root asserts nothing. | protocol 4.5 |
| 8 | MINOR | A record with a valid self-digest but an invalid shape, and parseable other-schema files that were not canonical, were treated as merely damaged. | The contract was tightened and the code follows it: only non-JSON bytes or a version-2 object whose digest fails are damaged; a self-hashed record must be canonical and shape-valid or recovery refuses; any other parseable JSON is foreign and refuses. | two new classification tests; seven more foreign cases |
| 9 | MINOR | "First batch is exactly 144" was enforced only at execution. | It is part of scientific manifest validity, so verification and the ledger enforce it. The protocol says "scientific chain"; fixtures are exempt. | `test_scientific_first_batch_width_is_part_of_manifest_validity` |
| 10 | MINOR | The runbook and the review prompt referred to this record before it existed. | This file. | |
| 11 | MINOR | The runbook said every command in sections 5 to 9 refuses before RUN1; the preflight commands do not. | Sentence corrected. | runbook, opening paragraph |
| 12 | MINOR | The diagnostics table mislabelled one refusal and omitted others. | Rows added. | runbook section 10 |

**Notes it raised.**

- *The two magnitude gates keyed differently.* The driver now refuses any scan ending above 10000, as the worker does, and requires full RUN1 status rather than the phase alone.
- *The worker's accepting branch was never executed by a test.* It still is not, in the committed suite; see the disclosure at the end of this section. The driver's side of the hand-off is tested on a mock.
- *No non-fixture batch can be run end to end in L1.* That stays true. The runbook now carries a first-execution note for the initial pilot.
- *`tests/frontier/test_rules.py` evaluates closed-form rule witnesses for 20 integers at or above 2^64.* These are the bounded fixed-step identity fixtures that version 1 section 5 items 1 to 3 require. They predate this continuation and are unchanged. No test computes a first descent by iteration at that magnitude.
- *The worker's first comment line still says CEML-FRONTIER-1.* That follows from keeping the worker byte-identical; the worker has no protocol-version-dependent behaviour.
- *Loose ends.* Two unbounded reads are now bounded; the fixture list and marker are in protocol section 5; the authority record's lack of a run-ID binding is stated in protocol section 2 and left as specified.

**Its section verdicts at `638e332`:** contract, recovery, chain integrity, tests, launcher and runbook SOUND WITH FINDINGS; native worker and build identity SOUND; gates NOT SOUND because of finding 1. Its closing judgement was that the engineering is acceptable once the blocker and the major findings are resolved and re-tested.

**What it did not check:** any elevated execution; anything at or above 10000 and so the whole non-fixture path; power-loss or storage faults; build reproducibility on a second machine; dependency provenance beyond the pinned hashes; whether the firewall cmdlet really fails non-terminatingly when its service is down (the premise of finding 4); the status documents; `selftest` end to end.

**Confirmation pass.** The same reviewer was resumed on the fix commit `71ad8a90d378d854cb15d69415b9266b142c26eb` on 2026-10-12. The pass was interrupted once by a usage limit and resumed with its partial work intact. It re-ran both suites (168 and 18 tests at that commit, zero skips), `f1_build.py --verify`, its original probes, a differential fuzz of 78,456 checkpoint summaries against its own oracle, a rewritten decision table over 1,223 slot states, 39 parser attacks on the new slot classification, a set of gate attacks, and 43 single-check deletions.

Its result: the blocker and all three majors RESOLVED; seven of the eight minors RESOLVED, and the eighth (this record not yet committed) open only until the commit that adds this file; no new blocker or major. The fuzz found no summary accepted that its oracle rejects and none wrongly rejected. The decision table matched the code on all 1,223 states, and the last two generations survived every write in the accepted states. Of the 43 deletions 37 were detected; five survivors are checks duplicated by a neighbouring check and one was an untested branch (C5 below).

It raised two new minor findings and five notes. All seven were resolved in the commit after `71ad8a9`. Those last resolutions were verified by the author's tests and mutation run only; they were **not** re-reviewed.

| # | Severity | Finding at `71ad8a9` | Resolution |
|---|---|---|---|
| C1 | MINOR | A new test gave the worker a synthetic RUN1 status and scanned the integer 10000, contradicting the L1 boundary text added in the same commit and the review prompt. | The test was removed. The driver's hand-off is observed on a mock only, and the protocol now states that the worker's accepting branch is first executed at RUN1. See the disclosure below. |
| C2 | MINOR, suspicion by reading | Cleanup depended on a whole-store enumeration that the preflight never exercised; if it failed persistently the rules would stay until the manual command. | The prerequisites, which the preflight and every isolation check run, now perform the same enumerations. Cleanup and the watchdog first remove the two rules by exact name, which needs no enumeration. A run also refuses to start while block rules from an earlier run exist. Static tests added; the preflight was observed to pass. Not executed elevated. |
| C3 | NOTE | The `selftest` test depended on an ignored local file and left a session folder behind. | The invocation gate is mocked in that test and the session it creates is removed. |
| C4 | NOTE | The fixture check accepted `L1-fixture-successor` as a run ID with its own base. | Fixture intervals are an explicit map by run ID; the successor is only the second batch of `L1-fixture-a`. Tested. |
| C5 | NOTE | The "over 128 KiB is damaged" branch had no test. | Two tests: one byte over the limit is damaged; padding to exactly the limit is a non-canonical self-hashed record and refuses. |
| C6 | NOTE | Two protocol sentences claimed more than the code does (pending reason; "put there"). | Wording corrected to what is verified. Both behaviours are conservative. |
| C7 | NOTE | Read-only commands on a scientific directory checked the phase alone, so "RUN1" with science still denied would have sufficed. | They require full RUN1 status. Tested. |

Its section verdicts at `71ad8a9`: recovery, chain integrity, native worker and build identity SOUND; contract, gates, tests, launcher and runbook SOUND WITH FINDINGS, the findings being the items above. Its judgement: acceptable once this record is committed, the owner has ruled on the handshake test, and the OS-blocked run has produced evidence. It did not review this record, the status documents or anything elevated.

**Disclosure: the one-integer handshake.** Between `71ad8a9` and the final commit the suite contained a test that gave the real worker a synthetic RUN1 status file and scanned the single integer 10000 (algebraic rule, witness 5000). It ran in the author's suite runs, in one unisolated rehearsal and in the reviewer's suite run, and passed with a plain and an annotated phase line. The reviewer's view was that it is not science in substance but lies outside the L1 boundary as the documents draw it, and that the decision is the owner's. The author removed it rather than make that decision for the owner. It is recorded here so the owner knows it happened. If the owner wants the worker's accepting branch exercised before RUN1, the test can be reinstated as a named gate fixture; that changes the build identity and needs a fresh OS-blocked run.

## 6. OS-blocked acceptance: the one open gate

**Status: NOT_RUN.** The run adds two machine-wide Windows Firewall block rules and registers a SYSTEM scheduled task. Those are system security settings, so the authoring agent did not start it. The owner authorised the run and starts it personally.

What the launcher does, in order: checks firewall and scheduler prerequisites; refuses unless both reviewed hashes match; takes a lock; proves a zero-payload TCP connection works; registers the SYSTEM watchdog (25 minutes, repeating, and at boot); adds one inbound and one outbound block-all rule named `CEML-L1Offline-<random id>-…`; verifies the rules and that the same probe now fails; runs the whole acceptance plan in a child process with a 20-minute limit while re-checking the rules; re-checks blocking; removes its two rules and verifies their absence; observes the probe connect again; removes the watchdog; writes `isolation.json`. The whole machine has no network while the rules exist. On this machine the unisolated plan took about 90 seconds.

Run from an **administrator** PowerShell window, with the absolute path of the Python 3.12.10 interpreter:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\l1\run_offline_acceptance.ps1 -Mode Run -PythonPath "<absolute path of python.exe 3.12.10>" -ExpectedSourceSha256 00a7477daf68576a39570d62bb6d2d2242154391672c2143e9552b25258c5985 -ExpectedLauncherSha256 97ccd27cf564fca0bc4e52da829b4bd71cce47d1aa1d41293e258315503b3669
```

The two hashes are the reviewed identities of section 7. If `-Mode Preflight` reports a different `source_sha256`, something changed: stop and find out what. The launcher hash is of the file's bytes as checked out here and changes if Git rewrites its line endings; take it from a fresh preflight in that case, after confirming the source hash is still the reviewed one.

Emergency restore, from an administrator PowerShell, if the network has not returned after 30 minutes:

```powershell
Get-NetFirewallRule -PolicyStore PersistentStore | Where-Object { $_.Group -like 'CEML-L1Offline-*' -and $_.Name -like 'CEML-L1Offline-*' } | Remove-NetFirewallRule
```

Then confirm no such rule is left and leave any `CEML-L1Offline-*-Restore` task in place until it removes itself.

**What will count as PASS.** In the newest `local/frontier/os-offline/<id>/`: an `isolation.json` with status `OS-BLOCKED-ENGINEERING-CHECKS-PASS`; `connected_baseline`, `os_rules_verified`, `rules_removed`, `watchdog_removed`, `connected_after_restore` and `checks_passed` all true; `child_exit_code` `"0"`; `last_stage` `completed`; both hashes equal to section 7. And a `checks.json` with status `ENGINEERING-CHECKS-PASS`, the same source hash, both suites PASS with zero skips at the totals of section 3, three equal build digests equal to section 7, and calibration `fixtures_pass`. Plus a read-only confirmation afterwards that no `CEML-L1Offline-*` rule or task remains. Anything less is a FAIL and leaves L1 OPEN. The unisolated rehearsal and the Python socket-denial tests are weaker observations and do not substitute.

The elevated path itself has never been executed. Its unelevated refusals, its read-only preflight, its parse and the in-memory construction of its scheduled-task objects were observed; its rule creation, watchdog and restoration were reviewed by reading only.

## 7. Final identities

| Identity | Value |
|---|---|
| Source commit (code, tests, contract, launcher) | `47240126d4da01e4be0cca89d632a01bc25a6b70` |
| First candidate commit, as independently reviewed | `638e3329b37e9de66b76173280f111771d7cb65e` |
| Reviewed acceptance source identity (`source_sha256`) | `00a7477daf68576a39570d62bb6d2d2242154391672c2143e9552b25258c5985` |
| Launcher SHA-256, as checked out on this machine | `97ccd27cf564fca0bc4e52da829b4bd71cce47d1aa1d41293e258315503b3669` |
| Native build digest | `c0263b353e05b9f3d09730e67d321254952c7dbdc2a6d892f7ffe2b14b89c032` |
| Release worker SHA3-256 | `8d3a72aa077fed414ad36e8008900f95a2a0630933e5dea5e66363fd34c19b6b` |
| Checked worker SHA3-256 | `b562e74ba06d7a4f936f3e0010f36142fe7025f8059e60793aea5388820bc525` |
| Checker source digest | `26e5e2e5b235fac140f0ee4afbac064a246f97fec316fb39d955d51659fc3970` |
| Frontier test-source digest | `360343f9cf63d1ed9a9c85d9f6bfe3ae99e30d622231fbf344276aea31fc4a72` |
| Parity table digest (version-2 domain) | `d368ec417e3170729f67737c414b02ced2d2f6cab349f9cd534404985058391c` |
| Version-2 snapshot digest | `538d319bad77b58ec3b37d653df3213312e260167ad26861e8870e48b276b729` |
| Frozen version-1 snapshot digest | `a511d6b80fc0ea6c85f3926b065e27acc696449af49cfa675d7c1315e85a2d66` |
| Tests | 171 frontier, 18 launcher, zero skips |
| Toolchain and pins | MSVC 14.44.35207, SDK 10.0.26100.0, Python 3.12.10, GMP 6.3.0 release 6.3.0-2; unchanged from `config/c1_gmp_pin.toml` |

The two worker hashes equal those recorded for the first candidate in `docs/L1_ACCEPTANCE.md`, because the worker sources and the pinned toolchain are unchanged. The build digest differs from the first candidate's because it now also covers the version-2 contract, snapshot, schemas and tests, and uses the version-2 domain.

## 8. Privacy gate

`tools/c1/privacy_gate.py` is the C1 recognizer with a closed C1 schema map. Run on each staged set it does not print PASS, and it did not for the two earlier L1 commits either. Every match was listed and inspected:

- `unknown_json_schema` for the four version-2 schemas and the version-2 snapshot, because the gate only knows C1 evidence schemas;
- `absolute_path` for division signs in formulas (`/2`, `/144`), command switches (`/E`, `/PID`, `/d`), and relative path fragments inside expressions (`/certificate.json`);
- `ipv4` for the public address the pre-existing connectivity probe connects to.

None is a private identifier. No user name, home path, host name, account, adapter or device identifier, address of this machine, credential or per-integer record is tracked. Raw logs and the acceptance evidence stay under the ignored `local/` tree. The gate itself was not changed.

## 9. Limits and what is not claimed

- Engineering fixtures only. The committed suite scans and replays only integers below 10000. It also evaluates closed-form rule identities, with no iteration, up to 10000 and for bounded fixtures near 2^32 to 2^160, as version 1 section 5 items 1 to 3 require; those tests predate this continuation. No frontier integer was scanned, replayed or certified, and no speed at 2^71 was measured. The integer 10000 itself was scanned by the withdrawn handshake test disclosed in section 5.
- No scientific batch has ever run end to end, and the committed suite never gives the worker a status its gate accepts. The first RUN1 pilot will be the first execution of the authorised path.
- Process-death tests show operating-system process exit. They do not prove behaviour under power loss or storage failure. Directory flush was observed as supported on this volume; that is an observation, not a durability guarantee.
- Three slots add neither authentication nor rollback detection. Those depend on the operator's external record (runbook section 8).
- OS firewall rules are an observed software block. They are not a hardware air gap.
- The Windows SDK closure is identified by version and is not content-hashed.
- One chain holds at most 256 batches and every chain starts at its base, so one base supports at most 3686400 verified integers with this build. Chains longer than two batches were not built; the limit was tested by lowering it.
- The snapshot's operational figures were observed on 2026-10-11 and were not refreshed.
- The mathematics is the unchanged P1 material, which is not formally verified or externally peer reviewed.
- The independent reviewer is a sub-agent of the same model family as the author (section 5).

## 10. Verdict

**CEML-L1 REMAINS OPEN.**

L1 PASS requires all of the following. The first six are met; the seventh is not.

1. Version-2 contract, schemas, snapshot and digest domains frozen, with version 1 preserved byte for byte. **Met.**
2. The amendment implemented, with every protocol section 5 obligation from 8 to 13 tested. **Met.**
3. Complete suites with zero skips; release and checked workers built from the retained pins; clean reproduction. **Met.**
4. Independent review with provenance recorded, findings resolved and re-tested. **Met**, within the limits stated in section 5.
5. Launcher and harness reviewed and adapted for version 2, with all recovery tests in the plan. **Met**; the elevated path itself is unexecuted.
6. Offline operator package and runbook, tested with synthetic fixtures only. **Met.**
7. Actual OS-enforced network-blocked build and acceptance with verified restoration, on these exact identities. **NOT MET: NOT_RUN.**

Engineering is complete except for that observation. The remaining action is the owner's: run the command in section 6. A later step then records the evidence here and, only if every item in section 6 is satisfied, changes this verdict. RUN1 is not authorised, and nothing in this record authorises it.
