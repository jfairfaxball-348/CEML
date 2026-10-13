# CEML-SESSION-I1 execution profile

Version I1 is a prospective, separately accepted execution profile. It does not
amend CEML-FRONTIER-2, its native worker, arithmetic, schemas, checker identity,
immutable records or the accepted external-base assumption. Certificates retain
the V2 format and remain independently checkable with the frozen V2 CLI.
I1 binds its own implementation, tests, this contract and operator launcher by
an LF-normalised SHA3-256 profile digest. A profile change invalidates acceptance.

## Trust construction and lifetime

At startup, acquire Windows read leases before trusting bytes. Refuse reparse
points and unavailable leases. Protect every accepted build input and artifact,
profile input, phase gate and historical batch file against writes and deletion;
protect ancestor directories against rename/deletion. Replay the entire ledger
once using V2's existing `_ledger_predecessors` interface. Check unique digests,
genesis, adjacency, identity, native build and replay. Store verified certificates
in private immutable in-memory mappings only. There is no disk verification cache.
Every restart constructs trust again. File handles are the authentication lifetime,
not mtime, hashes stored alongside mutable files, receipts or aggregate counts.

Between batches, check the exact historical directory/file inventory and the
latest authenticated predecessor. Unexpected, missing or unfinished directories
refuse continuation. Cheap inventory checks may grow linearly up to the unchanged
256-batch limit; historical arithmetic must not be repeated. This is approximately
constant arithmetic overhead, not a claim of constant filesystem complexity.

## Admission and atomic promotion

The owner must explicitly accept I1 before scientific writes. Admission retains
all RUN1 authority, manifest, snapshot, resource, checkpoint, native-frame and
rule gates. Pin a new batch's immutable context before computation. Use unchanged
V2 native computation and frame validation, then an independent full Python
replay. Refuse incomplete or mismatched work. Revalidate context and authenticated
predecessor, write the original V2 certificate atomically, pin all completed files,
independently verify that new certificate through V2 with the trusted predecessor
map, inspect checkpoint recovery and refuse warnings/temporaries. Only then
promote the in-memory ledger and save the operator receipt. No partially completed
batch or provisional checkpoint authorises a successor. Any failed attempt closes
the session. Failed records are preserved for diagnosis; there is no automatic retry.

The worker is a persistent local subprocess using standard pipes, isolated from
the operator's Ctrl+C process group. No network, telemetry or publication is
introduced. Stop admission at a requested boundary, finish the admitted batch and
save its receipt, close the worker and leases, release the operator lock, then
print publication readiness. Process loss releases leases and requires a new full
audit; it cannot recreate trust from a receipt.

## Acceptance and publication

The existing `start`, `stop`, finite-quantity and watcher commands keep their
interfaces. Without an I1 acceptance record they use the original V2 execution
path. `accept-incremental` is an owner-only interactive action, records no science,
and requires the literal `ACCEPT-SESSION-I1`; it binds the profile digest to the
accepted V2 build. An invalid/stale acceptance record refuses rather than silently
falling back. Engineering agents must not execute that acceptance action.

Publication remains an independent full frozen-V2 ledger audit, latest recursive
verification, reference replay, checkpoint inspection and accepted-build check.
The scientific runner never commits or publishes. A merged engineering PR is not
owner acceptance of I1 or authorisation for an agent to execute scientific batches.

Windows kernel file-sharing semantics are documented in
[CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew).
The threat boundary is ordinary local filesystem writers, crashes and corruption,
as for V2; an administrator capable of modifying process memory or the kernel is
outside it. Privileged raw disk writes and hostile storage are not authenticated
by read leases. Publication's independent full replay remains mandatory.
