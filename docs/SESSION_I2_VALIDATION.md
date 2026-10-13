# Continuous I2 validation — 2026-10-13

Status: engineering PASS, author-assessed; I2 owner acceptance NOT RECORDED.
No scientific batch was executed by the agent. The owner previously accepted I1
and completed/published the original 256-batch prefix. This is a prospective I2
extension, not retrospective alteration of that evidence or V2's frozen contract.

## Change and integrity boundary

The frozen V2 protocol deliberately caps admission/recursive verification at 256.
The owner now requests quantity-free continuous operation beyond that limit.
I2 is a separately identified orchestration fork of I1; it uses frozen V2's
existing authenticated-predecessor interface and replaces only the admission
slot policy. Neither a V2 constant nor function is monkey-patched in production.
All versioned I1 package/contract bytes and all frozen V2 identities remain
unchanged. The shared launcher changed, invalidating the earlier I1 profile
acceptance as designed; it must never be silently upgraded to I2.

I2 fully replays every retained batch on startup, pins records and manifests with
Windows read leases, and requires the exact published batch-256 certificate
`a6ab30751d0762f10f783bebf858f846aaf948098db2879a38099b2881e61565` at exclusive
end `2392518188130441801866`. Thereafter only that authenticated tip can be
extended, lazily, in 9999-integer batches. Stop still completes the admitted
batch and all checks before saving the receipt and releasing the operator lock.
Malformed/stale acceptance, gaps, altered context/manifest bytes, forks, pending
records, anomalous replay and resource errors refuse further admission.

Long-chain publication independently replays all history in a fresh subprocess;
it never trusts runner RAM. Parent publication leases keep records immutable
through metadata derivation and GitHub publication. The original <=256 audit
path remains. Informational live reporting accepts larger batch numbers; public
claim prose explicitly identifies I2 extension batches.

## Validation evidence

Commands run locally:

```powershell
python -m unittest discover -s tests/session_i2 -v
python -m unittest discover -s tests/operator -v
python -m unittest discover -s tests/publication -v
python tools/frontier/f1_build.py --verify
python tools/publication/website_progress.py --check
```

**35 I2, 28 operator and 32 publication tests passed: 95 total, zero skips.**
The I2 tests use only designated small fixtures `[2,146)` and `[146,290)` and
simulated operator/publication responses. A reduced isolated test-only slot cap
makes those two fixtures cross the legacy boundary: the original admission
refuses while I2 produces byte-identical certificates, independently accepted by
the frozen full-ledger audit. Production code never patches that constant.

Adversarial coverage includes self-hash-forged arithmetic, damaged checkpoints,
native/reference disagreement, incomplete work, inspection loss after atomic
commit, wrong identity/tip, missing or altered extension anchor, stale acceptance,
unknown RPC operations and external paths. Windows tests cover existing writers,
writable mappings, hardlink aliases, ancestor rename/deletion and reparse points.
Additional cases cover a clean stop at batch 257, lazy planning beyond 9999,
orphan/future manifests, a one-batch read-only preview, long publication refusing
changed receipts/final digests, and protection of post-audit publication reads.

A read-only I2 audit of **all 256 saved scientific batches**, including the final
extra replay/inspection and anchors 1/227/256, passed in **43.100616 seconds**.
SHA3 inventories before/after were identical for **1792 batch and manifest files**.
See [aggregate evidence](SESSION_I2_REPLAY.json). The installed profile digest
recorded there is `bb0575893b228dbb0d7c26606229f0e3bca87e58ea5c525453e70fddda17e1de`.
The accepted reproducible V2 build remains
`c0263b353e05b9f3d09730e67d321254952c7dbdc2a6d892f7ffe2b14b89c032`.
The current published aggregate/website JSON remains consistent and unchanged.
PowerShell parsing of the task configurator reports zero errors.

There is no hosted CEML CI workflow; these are local engineering checks. No
independent reviewer or actual scientific batch beyond 256 is claimed. Full
startup/publication replay, storage, RAM, Windows handles and directory inventory
grow with history; there is no promise of infinite physical capacity or constant
filesystem cost. Ordinary local writers/crashes/corruption are covered; privileged
kernel/process-memory manipulation and hostile raw storage remain outside the
accepted integrity boundary. See [the contract](SESSION_I2_PROTOCOL.md).

## Owner activation and scheduled launcher

After reading this record, accept this changed execution policy explicitly:

```powershell
python C:\CEML\tools\operator\run_frontier.py accept-continuous
```

Type `ACCEPT-SESSION-I2`. It binds the actual installed profile/build digest to an
ignored local record and executes no batch. The agent has not executed this
command or written its acknowledgement. Future profile changes invalidate it.

The existing task calls the current launcher and will automatically select the
accepted I2 path:

```powershell
Start-ScheduledTask -TaskName 'CEML Frontier Verification'
```

Its separate `P2D` execution timeout would forcibly terminate a long run. The
prepared configurator changes only that setting to `PT0S` and starts no task:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File C:\CEML\tools\operator\configure_task.ps1
```

**Windows returned Access is denied from this unelevated session.** The owner must
run that one-time command in Administrator PowerShell. The timeout has not yet
been removed. The helper verifies the expected existing launcher action, refuses
while it is running, preserves all other task settings and confirms the change.
Existing battery/power settings still apply.

Clean stop remains `python C:\CEML\tools\operator\run_frontier.py stop`; wait for
`CLEAN_STOPPED` in the task log and Ready state before `publish.py`. Watcher
commands remain unchanged. Only the owner launches science.
