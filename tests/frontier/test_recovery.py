"""Three-slot CEML-FRONTIER-2 recovery acceptance on tiny prefix fixtures; no science.

Every slot state through generation 6 is compared with a decision model written
here independently of the driver. Process-death tests show OS process exit only;
they do not prove storage power-loss behaviour.
"""

import copy
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "frontier"))
import ceml_frontier as driver


START, END = 2, 146
# Generation g of these self-contained fixtures has next_n CURSORS[g].
CURSORS = (2, 7, 15, 31, 55, 79, 111, 146)
DAMAGE = ("garbage", "empty", "zeros", "truncated", "bitflip", "stale_digest")
RENAMED = ("after_rename", "after_directory_flush")


def prefix(cursor):
    return driver.summary_reference(START, cursor, 100000, 2000000)


def files(directory):
    return {path.name: path.read_bytes() for path in sorted(directory.iterdir())}


def damage(path, kind):
    """Overwrite one written slot the way a torn or bit-rotted write could leave it."""
    raw = path.read_bytes()
    if kind == "garbage":
        data = b"torn"
    elif kind == "empty":
        data = b""
    elif kind == "zeros":
        data = bytes(len(raw))
    elif kind == "truncated":
        data = raw[:len(raw) // 2]
    else:
        record = json.loads(raw)
        if kind == "bitflip":
            old = record["transcript_digest"]
            record["transcript_digest"] = ("1" if old[0] == "0" else "0") + old[1:]
        else:
            record["explicit_attempts"] = str(int(record["explicit_attempts"]) + 1)
        data = driver.canonical(record)
    path.write_bytes(data)


def model(newest, states):
    """Independent restatement of protocol section 4.5.

    Returns None for refusal, else (recovered generation, integrity warning).
    """
    held = {generation % 3: generation for generation in range(max(0, newest - 2), newest + 1)}
    intact = sorted(generation for slot, generation in held.items() if states[slot] == "intact")
    if not intact:
        return None
    top = intact[-1]
    if intact != list(range(intact[0], top + 1)):
        return None
    if len(intact) < 2 and top != 0:
        return None
    return top, "damaged" in states or ("absent" in states and top >= 2)


class StoreCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scratch = tempfile.TemporaryDirectory(prefix="ceml-frontier-recovery-")
        cls.manifest = driver.fixture_run("L1-fixture-a", build_digest="0" * 64)
        cls.templates, cls.records = {}, {}
        for newest in range(len(CURSORS)):
            directory = Path(cls.scratch.name) / f"template-{newest}"
            store = driver.CheckpointStore(directory, cls.manifest)
            records = [store.initialize()]
            for generation in range(1, newest + 1):
                records.append(store.write(prefix(CURSORS[generation])))
            cls.templates[newest], cls.records[newest] = directory, records

    @classmethod
    def tearDownClass(cls):
        cls.scratch.cleanup()

    def clone(self, newest):
        directory = Path(tempfile.mkdtemp(dir=self.scratch.name)) / "batch"
        shutil.copytree(self.templates[newest], directory)
        return directory, driver.CheckpointStore(directory, self.manifest)

    def fresh(self):
        directory = Path(tempfile.mkdtemp(dir=self.scratch.name)) / "batch"
        return directory, driver.CheckpointStore(directory, self.manifest)

    def put(self, directory, slot, record):
        (directory / f"ckpt.{slot}.json").write_bytes(driver.canonical(driver.seal(record, "CHECKPOINT")))

    def assert_refused_unchanged(self, directory, store):
        before = files(directory)
        with self.assertRaises(driver.Refusal):
            store.recover()
        with self.assertRaises(driver.Refusal):
            store.write(prefix(END))
        self.assertEqual(before, files(directory))
        self.assertNotIn("certificate.json", before)


class RotationTests(StoreCase):
    def test_root_is_the_empty_prefix_and_generations_rotate_through_three_slots(self):
        directory, store = self.fresh()
        root = store.initialize()
        self.assertEqual(("0", None, str(START), None),
                         (root["generation"], root["previous_checkpoint_digest"], root["next_n"], root["pending"]))
        self.assertEqual(0, sum(map(int, root["counts"].values())))
        self.assertEqual(hashlib.sha3_256(b"CEML-FRONTIER-2/EVENTS\0").hexdigest(), root["transcript_digest"])
        self.assertEqual(["ckpt.0.json"], sorted(files(directory)))
        with self.assertRaises(driver.Refusal):
            store.initialize()
        previous, cursor = root, START
        for generation in range(1, 14):
            cursor = min(END, cursor + 11)
            record = store.write(prefix(cursor))
            self.assertEqual((str(generation), previous["digest"]),
                             (record["generation"], record["previous_checkpoint_digest"]))
            on_disk = {name: json.loads(raw)["generation"] for name, raw in files(directory).items()}
            expected = {f"ckpt.{g % 3}.json": str(g) for g in range(max(0, generation - 2), generation + 1)}
            self.assertEqual(expected, on_disk)
            self.assertEqual((record, []), store.recover())
            previous = record

    def test_write_requires_an_existing_authenticated_root(self):
        directory, store = self.fresh()
        with self.assertRaises(driver.Refusal):
            store.write(prefix(7))
        self.assertEqual({}, files(directory))
        # Deleting every slot never restarts a batch silently at generation 0.
        directory, store = self.clone(4)
        for slot in range(3):
            (directory / f"ckpt.{slot}.json").unlink()
        self.assert_refused_unchanged(directory, store)

    def test_cursor_rollback_refuses_before_any_slot_changes(self):
        directory, store = self.clone(4)
        before = files(directory)
        with self.assertRaises(driver.Refusal):
            store.write(prefix(CURSORS[3]))
        self.assertEqual(before, files(directory))

    def test_root_cannot_be_created_beside_a_certificate_or_slot(self):
        for name in ("certificate.json", "ckpt.1.json", "ckpt.2.json"):
            directory, store = self.fresh()
            (directory / name).write_bytes(b"torn")
            with self.subTest(name=name), self.assertRaises(driver.Refusal):
                store.initialize()


class SlotStateMatrixTests(StoreCase):
    def test_every_intact_damaged_absent_state_through_generation_6(self):
        checked = 0
        for newest in range(0, 7):
            held = {generation % 3: generation for generation in range(max(0, newest - 2), newest + 1)}
            options = [("intact", "damaged", "absent") if slot in held else ("absent", "damaged")
                       for slot in range(3)]
            for case, states in enumerate(itertools.product(*options)):
                with self.subTest(newest=newest, states=states):
                    directory, store = self.clone(newest)
                    for slot, state in enumerate(states):
                        path = directory / f"ckpt.{slot}.json"
                        if state == "absent" and path.exists():
                            path.unlink()
                        elif state == "damaged" and slot in held:
                            damage(path, DAMAGE[(case + slot) % len(DAMAGE)])
                        elif state == "damaged":
                            path.write_bytes((b"torn", b"", bytes(64))[(case + slot) % 3])
                    expected = model(newest, states)
                    if expected is None:
                        self.assert_refused_unchanged(directory, store)
                    else:
                        generation, warned = expected
                        before = files(directory)
                        recovered, warnings = store.recover()
                        self.assertEqual(self.records[newest][generation], recovered)
                        self.assertEqual(warned, bool(warnings))
                        self.assertEqual(before, files(directory))
                        written = store.write(prefix(CURSORS[generation + 1]))
                        self.assertEqual((str(generation + 1), recovered["digest"]),
                                         (written["generation"], written["previous_checkpoint_digest"]))
                        after = files(directory)
                        self.assertEqual(driver.canonical(written), after[f"ckpt.{(generation + 1) % 3}.json"])
                        # The last two authenticated generations survive the write untouched.
                        for retained in range(max(0, generation - 1), generation + 1):
                            name = f"ckpt.{retained % 3}.json"
                            self.assertEqual(before[name], after[name])
                        self.assertEqual(written, store.recover()[0])
                        self.assertNotIn("certificate.json", after)
                    checked += 1
        self.assertEqual(12 + 18 + 5 * 27, checked)

    def test_each_damage_kind_is_a_torn_slot_and_never_a_record(self):
        for kind in DAMAGE:
            directory, store = self.clone(4)
            damage(directory / "ckpt.1.json", kind)
            with self.subTest(kind=kind):
                self.assertIs(driver.DAMAGED, store.read_slot(1))
                recovered, warnings = store.recover()
                self.assertEqual(self.records[4][3], recovered)
                self.assertTrue(warnings)

    def test_orphan_temporary_files_are_never_checkpoint_evidence(self):
        directory, store = self.fresh()
        (directory / "ckpt.0.json.orphan.tmp").write_bytes(driver.canonical(self.records[0][0]))
        with self.assertRaises(driver.Refusal):
            store.recover()
        directory, store = self.clone(3)
        (directory / "ckpt.1.json.0123456789abcdef0123456789abcdef.tmp").write_bytes(
            driver.canonical(self.records[4][4]))
        self.assertEqual((self.records[3][3], []), store.recover())


class ContradictionTests(StoreCase):
    """Canonical self-hashed records that lie are refused; recovery never falls back past them."""

    def test_self_hashed_contradictions_at_every_retained_position(self):
        changes = (
            ("next_n", lambda r: str(int(r["next_n"]) + 1)),
            ("explicit_t_steps", lambda r: str(int(r["explicit_t_steps"]) + 1)),
            ("explicit_attempts", lambda r: str(int(r["explicit_attempts"]) + 1)),
            ("transcript_digest", "1" * 64), ("native_build_digest", "1" * 64),
            ("snapshot_digest", "1" * 64), ("table_digest", "1" * 64), ("run_digest", "1" * 64),
            ("run_id", "changed"), ("base_B", "3"), ("batch_end", "147"),
            ("predecessor_digest", "1" * 64), ("generation", str(2 ** 64)),
            ("generation", lambda r: str(int(r["generation"]) + 3)),
            ("previous_checkpoint_digest", "1" * 64),
            ("previous_checkpoint_digest", lambda r: None if r["previous_checkpoint_digest"] else "1" * 64),
        )
        checked = 0
        for newest in range(1, 6):
            for generation in range(max(0, newest - 2), newest + 1):
                for index, (field, value) in enumerate(changes):
                    directory, store = self.clone(newest)
                    record = copy.deepcopy(self.records[newest][generation])
                    record[field] = value(record) if callable(value) else value
                    self.put(directory, generation % 3, record)
                    with self.subTest(newest=newest, generation=generation, change=index):
                        self.assert_refused_unchanged(directory, store)
                    checked += 1
        self.assertEqual((2 + 3 + 3 + 3 + 3) * len(changes), checked)

    def test_valid_prefix_with_lower_cursor_than_its_parent_refuses(self):
        for newest in range(2, 6):
            directory, store = self.clone(newest)
            record = dict(copy.deepcopy(self.records[newest][newest]), **prefix(CURSORS[newest - 2]))
            self.put(directory, newest % 3, record)
            with self.subTest(newest=newest):
                self.assert_refused_unchanged(directory, store)

    def test_root_violations_refuse(self):
        root = self.records[0][0]
        progressed = dict(copy.deepcopy(root), **prefix(7))
        pending = copy.deepcopy(root)
        pending["pending"] = dict(n="2", reason="native_failure", attempted_steps="0", last_value="2")
        for index, record in enumerate((progressed, pending)):
            directory, store = self.fresh()
            self.put(directory, 0, record)
            with self.subTest(case=index):
                self.assert_refused_unchanged(directory, store)

    def test_wrong_slot_and_duplicate_generations_refuse(self):
        for newest in (2, 3, 5):
            for source in range(newest - 2, newest + 1):
                for target in range(3):
                    if target == source % 3:
                        continue
                    directory, store = self.clone(newest)
                    shutil.copyfile(directory / f"ckpt.{source % 3}.json", directory / f"ckpt.{target}.json")
                    with self.subTest(newest=newest, source=source, target=target):
                        self.assert_refused_unchanged(directory, store)

    def test_valid_linked_generations_in_swapped_or_rotated_slots_refuse(self):
        # Every record stays intact and hash-linked; only the slot rule can refuse.
        # Without it the next write could replace one of the last two generations.
        for newest in (1, 2, 4, 6):
            present = [generation % 3 for generation in range(max(0, newest - 2), newest + 1)]
            orders = [order for order in itertools.permutations(present) if list(order) != present]
            for order in orders:
                directory, store = self.clone(newest)
                contents = [(directory / f"ckpt.{slot}.json").read_bytes() for slot in present]
                for slot, data in zip(order, contents):
                    (directory / f"ckpt.{slot}.json").write_bytes(data)
                with self.subTest(newest=newest, order=order):
                    self.assert_refused_unchanged(directory, store)

    def test_fork_with_valid_looking_sibling_history_refuses(self):
        # A different, internally valid generation-3 child of generation 2 replaces
        # the real generation 3 while generation 4 still names the original.
        directory, store = self.clone(4)
        fork = dict(copy.deepcopy(self.records[4][3]), **prefix(CURSORS[3] + 2))
        self.put(directory, 0, fork)
        self.assert_refused_unchanged(directory, store)

    def test_advancing_over_pending_work_refuses(self):
        run = driver.fixture_run("L1-fixture-a", max_t=1, build_digest="0" * 64)
        directory = Path(tempfile.mkdtemp(dir=self.scratch.name)) / "batch"
        store = driver.CheckpointStore(directory, run)
        store.initialize()
        blocked = driver.summary_reference(START, END, 1, 2000000)
        record = store.write(blocked)
        forged = dict(copy.deepcopy(record), **prefix(8))
        (directory / "ckpt.1.json").write_bytes(driver.canonical(driver.seal(forged, "CHECKPOINT")))
        with self.assertRaises(driver.Refusal):
            store.recover()

    def test_cursor_moved_past_the_pending_start_with_unchanged_counters_refuses(self):
        # Independent-review finding: the honest counters of [2,7) were kept while
        # next_n was moved beyond the unresolved start and pending was cleared.
        for label, max_t, max_total in (("step_budget", 1, 2000000), ("total_budget", 100000, 5)):
            run = driver.fixture_run("L1-fixture-a", max_t=max_t, max_total=max_total, build_digest="0" * 64)
            directory = Path(tempfile.mkdtemp(dir=self.scratch.name)) / "batch"
            store = driver.CheckpointStore(directory, run)
            store.initialize()
            honest = store.write(driver.summary_reference(START, END, max_t, max_total))
            self.assertEqual(("7", label, 5), (honest["next_n"], honest["pending"]["reason"],
                                              sum(map(int, honest["counts"].values()))))
            for cursor in (8, 100, 146):
                forged = driver.seal(dict(copy.deepcopy(honest), next_n=str(cursor), pending=None), "CHECKPOINT")
                (directory / "ckpt.1.json").write_bytes(driver.canonical(forged))
                with self.subTest(budget=label, cursor=cursor):
                    with self.assertRaisesRegex(driver.Refusal, "not completely resolved"):
                        driver.checkpoint_valid(forged, run)
                    before = files(directory)
                    with self.assertRaises(driver.Refusal):
                        store.recover()
                    with self.assertRaises(driver.Refusal):
                        store.write(driver.summary_reference(START, END, max_t, max_total))
                    self.assertEqual(before, files(directory))
            # A cursor that keeps the pending object but claims more coverage also refuses.
            inflated = copy.deepcopy(honest)
            inflated["counts"]["e2_count"] = str(int(inflated["counts"]["e2_count"]) + 1)
            with self.assertRaises(driver.Refusal):
                driver.checkpoint_valid(driver.seal(inflated, "CHECKPOINT"), run)
            (directory / "ckpt.1.json").write_bytes(driver.canonical(honest))
            self.assertEqual(honest, store.recover()[0])

    def linked(self, generation, parent, cursor):
        """A correctly bound, sealed record at an arbitrary generation number."""
        return driver.seal(dict(schema=driver.SCHEMA_IDS["checkpoint"],
                                run_digest=driver.H("RUN", driver.canonical(self.manifest)),
                                generation=str(generation), previous_checkpoint_digest=parent,
                                **{key: self.manifest[key] for key in driver.BINDING}, **prefix(cursor)),
                           "CHECKPOINT")

    def test_generation_bound_refuses_on_write_and_on_read(self):
        top = 2 ** 64 - 1
        directory, store = self.fresh()
        older = self.linked(top - 1, "1" * 64, 7)
        newest = self.linked(top, older["digest"], 15)
        self.put(directory, (top - 1) % 3, older)
        self.put(directory, top % 3, newest)
        recovered, warnings = store.recover()
        self.assertEqual((newest, True), (recovered, bool(warnings)))
        before = files(directory)
        with self.assertRaisesRegex(driver.Refusal, "generation overflow"):
            store.write(prefix(31))
        self.assertEqual(before, files(directory))
        # The same linked pair one step higher is unreadable, whatever its slots and hashes say.
        directory, store = self.fresh()
        over = self.linked(top + 1, newest["digest"], 31)
        self.put(directory, top % 3, newest)
        self.put(directory, (top + 1) % 3, over)
        with self.assertRaisesRegex(driver.Refusal, "generation overflow"):
            store.recover()


class CrossVersionTests(StoreCase):
    def version_1_checkpoint(self, record):
        old = copy.deepcopy(record)
        old["schema"] = "CEML-FRONTIER-CKPT-1"
        old.pop("digest")
        old["digest"] = hashlib.sha3_256(b"CEML-FRONTIER-1/CHECKPOINT\0" + driver.canonical(old)).hexdigest()
        return driver.canonical(old)

    def test_foreign_and_version_1_records_refuse_instead_of_falling_back(self):
        old = self.version_1_checkpoint(self.records[4][4])
        foreign = (old, b"{}", b"[]", b"null", b'"torn"',
                   driver.canonical(self.manifest), driver.canonical({"schema": "CEML-FRONTIER-CKPT-3"}),
                   driver.canonical(driver.seal({"schema": "CEML-FRONTIER-2-CERTIFICATE"}, "CERTIFICATE")),
                   # Parseable but not canonical: a re-saved version-1 record is still foreign, not torn.
                   old + b"\n", json.dumps(json.loads(old), indent=2).encode("ascii"),
                   b"1", b"true", b"[1]", b'{"generation":1,"schema":"CEML-FRONTIER-CKPT-1"}',
                   b' {"schema": "CEML-FRONTIER-1-RUN"} ')
        checked = 0
        for newest in (0, 1, 2, 4, 6):
            for slot in range(3):
                for index, data in enumerate(foreign):
                    directory, store = self.clone(newest)
                    (directory / f"ckpt.{slot}.json").write_bytes(data)
                    with self.subTest(newest=newest, slot=slot, record=index):
                        self.assert_refused_unchanged(directory, store)
                    checked += 1
        self.assertEqual(5 * 3 * len(foreign), checked)

    def test_self_hashed_record_that_is_shape_invalid_or_noncanonical_refuses(self):
        # A matching self-digest rules out a torn write, so these are contradictions.
        record = self.records[4][4]
        extra = driver.seal(dict(record, unexpected="yes"), "CHECKPOINT")
        padded = driver.seal(dict(record, generation="04"), "CHECKPOINT")
        missing = {key: value for key, value in record.items() if key != "pending"}
        missing = driver.seal(missing, "CHECKPOINT")
        stored = driver.canonical(record)
        cases = (driver.canonical(extra), driver.canonical(padded), driver.canonical(missing),
                 stored + b"\n", b" " + stored, json.dumps(record, indent=1).encode("ascii"),
                 json.dumps(dict(reversed(list(record.items()))), separators=(",", ":")).encode("ascii"))
        self.assertNotEqual(stored, cases[-1])
        for index, data in enumerate(cases):
            directory, store = self.clone(4)
            (directory / "ckpt.1.json").write_bytes(data)
            with self.subTest(case=index):
                with self.assertRaises(driver.Refusal):
                    store.read_slot(1)
                self.assert_refused_unchanged(directory, store)

    def test_version_2_objects_that_cannot_be_self_hashed_are_only_damaged(self):
        record = self.records[4][4]
        unsigned = {key: value for key, value in record.items() if key != "digest"}
        cases = (b'{"generation":1,"schema":"CEML-FRONTIER-CKPT-2"}', driver.canonical(unsigned),
                 driver.canonical(dict(unsigned, digest="0" * 64)),
                 json.dumps(dict(record, generation=4)).encode("ascii"),
                 b'{"schema":"CEML-FRONTIER-CKPT-2","value":NaN}')
        for index, data in enumerate(cases):
            directory, store = self.clone(4)
            (directory / "ckpt.1.json").write_bytes(data)
            with self.subTest(case=index):
                self.assertIs(driver.DAMAGED, store.read_slot(1))
                recovered, warnings = store.recover()
                self.assertEqual((self.records[4][3], True), (recovered, bool(warnings)))

    def test_version_1_digest_domains_never_validate_version_2_records(self):
        record = self.records[3][3]
        unsigned = {key: value for key, value in record.items() if key != "digest"}
        old_domain = hashlib.sha3_256(b"CEML-FRONTIER-1/CHECKPOINT\0" + driver.canonical(unsigned)).hexdigest()
        self.assertNotEqual(old_domain, record["digest"])
        directory, store = self.clone(3)
        (directory / "ckpt.0.json").write_bytes(driver.canonical(dict(unsigned, digest=old_domain)))
        # A version-2 shaped record sealed in the version-1 domain is merely a torn slot.
        self.assertIs(driver.DAMAGED, store.read_slot(0))
        self.assertEqual(self.records[3][2], store.recover()[0])
        old_genesis = hashlib.sha3_256(
            b"CEML-FRONTIER-1/GENESIS\0" + "|".join(self.manifest[k] for k in driver.IDENTITY).encode("ascii")).hexdigest()
        self.assertNotEqual(old_genesis, driver.genesis(self.manifest))
        spliced = dict(self.manifest, predecessor_digest=old_genesis)
        with self.assertRaises(driver.Refusal):
            driver.validate_manifest(spliced, driver.snapshot(), True)

    def test_version_1_run_snapshot_and_certificate_shapes_refuse(self):
        scratch = Path(tempfile.mkdtemp(dir=self.scratch.name))
        old_run = dict(self.manifest, schema="CEML-FRONTIER-1-RUN")
        old_snapshot = (ROOT / "config/frontier_snapshot_v1.json").read_bytes()
        old_certificate = dict(schema="CEML-FRONTIER-1-CERTIFICATE", digest="0" * 64)
        for kind, data in (("run", driver.canonical(old_run)), ("snapshot", old_snapshot),
                           ("certificate", driver.canonical(old_certificate)),
                           ("checkpoint", self.version_1_checkpoint(self.records[2][2]))):
            path = scratch / (kind + ".json")
            path.write_bytes(data)
            with self.subTest(kind=kind), self.assertRaises(driver.Refusal):
                driver.load_record(path, kind)
        with self.assertRaises(driver.Refusal):
            driver.validate_manifest(old_run, driver.snapshot(), True)
        with self.assertRaises(driver.Refusal):
            driver.validate_snapshot(json.loads(old_snapshot))


class FaultPointTests(StoreCase):
    def test_fault_point_list_is_the_frozen_set(self):
        self.assertEqual(("before_create", "before_write", "during_write", "before_flush", "after_flush",
                          "before_rename", "after_rename", "after_directory_flush"), driver.FAULT_POINTS)
        directory, store = self.clone(1)
        with self.assertRaises(driver.Refusal):
            store.write(prefix(15), "unknown_point")
        self.assertEqual(self.records[1][1], store.recover()[0])

    def test_every_fault_point_for_generations_1_through_6(self):
        for newest in range(0, 6):
            for fault in driver.FAULT_POINTS:
                with self.subTest(writing=newest + 1, fault=fault):
                    directory, store = self.clone(newest)
                    before = files(directory)
                    with self.assertRaises(driver.Refusal):
                        store.write(prefix(CURSORS[newest + 1]), fault)
                    recovered, warnings = store.recover()
                    after = files(directory)
                    temporaries = [name for name in after if name.endswith(".tmp")]
                    if fault in RENAMED:
                        self.assertEqual(self.records[newest + 1][newest + 1], recovered)
                        self.assertEqual([], temporaries)
                    else:
                        self.assertEqual(self.records[newest][newest], recovered)
                        self.assertEqual(before, {k: v for k, v in after.items() if not k.endswith(".tmp")})
                        self.assertEqual(0 if fault == "before_create" else 1, len(temporaries))
                    self.assertEqual([], warnings)
                    self.assertNotIn("certificate.json", after)
                    # The interrupted store stays usable and never skips or repeats a generation.
                    following = store.write(prefix(END))
                    self.assertEqual(str(int(recovered["generation"]) + 1), following["generation"])

    def test_every_fault_point_while_creating_the_root(self):
        for fault in driver.FAULT_POINTS:
            with self.subTest(fault=fault):
                directory, store = self.fresh()
                with self.assertRaises(driver.Refusal):
                    store.initialize(fault)
                if fault in RENAMED:
                    self.assertEqual((self.records[0][0], []), store.recover())
                    with self.assertRaises(driver.Refusal):
                        store.initialize()
                else:
                    self.assertFalse((directory / "ckpt.0.json").exists())
                    with self.assertRaises(driver.Refusal):
                        store.recover()
                    with self.assertRaises(driver.Refusal):
                        store.write(prefix(7))


class ProcessDeathTests(StoreCase):
    # os._exit ends the child while the named write, flush or rename point is on
    # the stack. This is OS process death, not storage power loss.
    WRAPPER = r'''
import os
from pathlib import Path
import sys
root, directory, fault, cursor, mode = sys.argv[1:]
sys.path.insert(0, str(Path(root) / "tools/frontier"))
import ceml_frontier as driver
import f1_build
original = driver.Refusal
class ProcessDeath(original):
    def __init__(self, reason):
        if reason == "injected " + fault:
            os._exit(99)
        super().__init__(reason)
driver.Refusal = ProcessDeath
f1_build.verify_build = lambda *args, **kwargs: {"digest": "0" * 64}
run = driver.fixture_run("L1-fixture-a", build_digest="0" * 64)
if mode == "root":
    driver.CheckpointStore(directory, run).initialize(fault)
elif mode == "certificate":
    driver.commit_batch(directory, run, driver.summary_reference(2, 146, 100000, 2000000), True, fault)
else:
    driver.CheckpointStore(directory, run).write(driver.summary_reference(2, int(cursor), 100000, 2000000), fault)
os._exit(98)
'''

    def die(self, directory, fault, cursor, mode):
        result = subprocess.run([sys.executable, "-c", self.WRAPPER, str(ROOT), str(directory), fault,
                                 str(cursor), mode], capture_output=True, timeout=30)
        self.assertEqual(99, result.returncode, result.stderr.decode("ascii", "replace"))

    def test_process_death_at_every_fault_point_for_generations_1_through_5(self):
        for newest in range(0, 5):
            for fault in driver.FAULT_POINTS:
                with self.subTest(writing=newest + 1, fault=fault):
                    directory, store = self.clone(newest)
                    self.die(directory, fault, CURSORS[newest + 1], "write")
                    recovered, warnings = store.recover()
                    expected = newest + 1 if fault in RENAMED else newest
                    self.assertEqual(self.records[expected][expected], recovered)
                    self.assertEqual([], warnings)
                    self.assertFalse((directory / "certificate.json").exists())

    def test_process_death_while_creating_the_root(self):
        for fault in driver.FAULT_POINTS:
            with self.subTest(fault=fault):
                directory, store = self.fresh()
                self.die(directory, fault, START, "root")
                if fault in RENAMED:
                    self.assertEqual((self.records[0][0], []), store.recover())
                else:
                    with self.assertRaises(driver.Refusal):
                        store.recover()

    def test_process_death_while_committing_the_certificate(self):
        from unittest import mock
        import f1_build
        for fault in driver.FAULT_POINTS:
            with self.subTest(fault=fault):
                directory = Path(tempfile.mkdtemp(dir=self.scratch.name)) / "batch"
                driver.prepare_fixture(directory, self.manifest)
                self.die(directory, fault, END, "certificate")
                path = directory / "certificate.json"
                if fault in RENAMED:
                    with mock.patch.object(f1_build, "verify_build", return_value={"digest": "0" * 64}):
                        certificate = driver.verify_batch(path, True)
                    self.assertEqual(prefix(END)["transcript_digest"], certificate["independent_replay_digest"])
                else:
                    self.assertFalse(path.exists())


class PendingTests(StoreCase):
    def test_pending_start_stays_outside_coverage_across_generations_and_fallback(self):
        run = driver.fixture_run("L1-fixture-a", max_t=1, build_digest="0" * 64)
        directory = Path(tempfile.mkdtemp(dir=self.scratch.name)) / "batch"
        store = driver.CheckpointStore(directory, run)
        store.initialize()
        blocked = driver.summary_reference(START, END, 1, 2000000)
        records = []
        for generation in range(1, 6):
            record = store.write(blocked)
            records.append(record)
            self.assertEqual((str(generation), "7", "7"),
                             (record["generation"], record["next_n"], record["pending"]["n"]))
            self.assertEqual(5, sum(map(int, record["counts"].values())))
            self.assertEqual(("0", "0", "1"), (record["counts"]["explicit_count"],
                                               record["counts"]["unresolved_count"], record["explicit_attempts"]))
        self.assertEqual((records[-1], []), store.recover())
        damage(directory / "ckpt.2.json", "truncated")
        recovered, warnings = store.recover()
        self.assertEqual(records[-2], recovered)
        self.assertEqual("7", recovered["pending"]["n"])
        self.assertTrue(warnings)
        self.assertFalse((directory / "certificate.json").exists())


if __name__ == "__main__":
    unittest.main()
