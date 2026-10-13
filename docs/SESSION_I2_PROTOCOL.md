# CEML-SESSION-I2 — continuous execution extension

This separately versioned prospective profile replaces the I1 execution cap only
after explicit owner acceptance. The owner requested indefinite launcher operation
on 2026-10-13. It does not modify the frozen CEML-FRONTIER-2 source, contracts,
schemas, native build, rules, snapshot or historical records. Longer execution is
an **I2 extension using V2-format certificates**, not a claim that the frozen V2
256-batch admission contract changed. No cross-version certificate conversion occurs.

## Anchored continuation

Scientific I2 startup requires a complete, independently replayed contiguous
prefix from the original genesis through batch 256. Its immutable extension anchor
is certificate `a6ab30751d0762f10f783bebf858f846aaf948098db2879a38099b2881e61565`,
exclusive end `2392518188130441801866`. Every retained later certificate is also
fully replayed at every restart. A different root, anchor, identity, gap, duplicate,
fork, unfinished directory or altered byte refuses continuation. An aggregate,
receipt, control state or hash alone establishes no mathematical trust.
Retained manifests must exactly match their pinned batch contexts. Orphan or
unexpected manifests, including a future slot, refuse before new admission.

The I2 package is an explicit versioned fork of I1 orchestration and leases. Its
only admission change replaces the 256-sibling resource policy with authenticated
tip extension. Every historical certificate/run binding has already been checked
by frozen V2 verification and protected by Windows read leases. The new interval
must start at that tip's exclusive end, name the tip digest, share all chain identity
fields and use the next sequential directory number. No V2 constant/function is
modified or monkey-patched. Frozen V2 recursive verification remains capped; I2
always invokes its existing ledger-predecessor interface after a fresh full replay.

## Execution and stopping

The existing launcher `start` lazily generates one 9999-integer admission at a time,
without a quantity or fixed batch-count ceiling. It never allocates an infinite
plan or pre-authorises future records. Before creating any output it checks the
stop request, authenticated ledger, output/manifest absence and single operator
lock. Authority, manifest, native frame checking, independent every-integer replay,
three-slot checkpoints, atomic V2-format certificate, final verification,
inspection, pinned historical inputs and receipt saving retain I1's guarantees.
Any failure closes the trusted worker; no automatic retry or prefix promotion.

`stop` finishes the admitted batch and saves the receipt, closes the worker/leases,
releases the operator lock, then prints `CLEAN_STOPPED`. Ctrl+C retains the same
clean stop procedure. Process loss requires full reauthentication on restart.
Existing finite commands also work under I2. `start --plan` previews only the next
batch after full startup verification, and executes nothing.

"Indefinite" means no preselected quantity/count limit, not immunity to resource
exhaustion, hardware loss, integrity refusal or numeric-domain limits. Storage,
RAM, handles and startup/publication replay grow with retained history; directory
inventory remains linear. Exhaustion fails closed with retained evidence. This
release does not introduce archival trust shortcuts or alter the numeric budgets.

## Acceptance and independent publication

Owner-only `run_frontier.py accept-continuous`, literal `ACCEPT-SESSION-I2`, binds
the installed I2 source/tests/protocol, launcher and publisher digest to the
accepted V2 build. Read SESSION_I2_VALIDATION.md first. A missing acceptance cannot
activate I2; malformed/stale acceptance refuses, never falls back. The old I1
acceptance remains historical; the launcher change invalidates its digest, so the
owner must accept I2 before using the updated launcher. An engineering merge grants
neither profile acceptance nor agent scientific execution. Agents never type it.

Publication of the existing <=256 prefix keeps the original frozen CLI checks.
For a longer chain, a separate fresh audit subprocess establishes its own Windows
leases, independently replays **every** retained batch with frozen V2 arithmetic,
checks the I2 anchor, and replays/verifies/inspects the final certificate again.
Published anchors and the exact receipt must agree with that audit. This never
reuses runner RAM or a persisted verification cache, and executes no scientific
batch. Unchanged GitHub PR/check/merge safeguards apply. The runner remains offline
and never imports the publisher or commits automatically.
The parent publisher also holds read leases over all extended scientific record
and manifest bytes throughout audit, metadata derivation and publication. Its
post-audit reads cannot replace verified counters with altered record bytes.

The live observer accepts sequential batch numbers beyond 256, including beyond
9999; it remains optional informational observation without replay authority.
Public claim prose identifies I2 extension batches while preserving historical
V2 rows, identities and the original conditional base assumption.
