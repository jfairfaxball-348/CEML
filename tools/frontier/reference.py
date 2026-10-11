"""Independent exact mathematical reference for CEML-FRONTIER-2.

This module imports no driver/native classifications or precomputed native rows.
An event proves only the protocol's conditional inference; replay does not accept
an external base, authorise a run, or commit a scientific certificate.
"""
import hashlib


RULES = ("E2", "Q4", "P3", "M9", "S2K4-03", "EXPLICIT")
COUNT_KEYS = ("base_count", "e2_count", "q4_count", "p3_count", "m9_count",
              "s2_count", "explicit_count", "unresolved_count")
RULE_COUNT_KEYS = dict(zip(RULES, COUNT_KEYS[1:7]))
MAX_T = 100000
MAX_TOTAL_T = 2000000
MAX_BATCH = 14400
MAX_DIGITS = 8192
MAX_VALUE = 10 ** MAX_DIGITS - 1
MAX_FRAME = 32768
# Version-2 digest domain, stated here independently of the driver.
DOMAIN = b"CEML-FRONTIER-2/"

# The complete frozen period-144 ledger, represented independently of the
# predicate code below. Residue 1 is represented by n=145, not boundary n=1.
PINNED_RESIDUES = {
    "E2": tuple(range(0, 144, 2)),
    "Q4": tuple(range(1, 144, 4)),
    "P3": (11, 23, 35, 47, 59, 71, 83, 95, 107, 119, 131, 143),
    "M9": (31, 67, 103, 139),
    "S2K4-03": (3, 19, 51, 99, 115),
    "EXPLICIT": (7, 15, 27, 39, 43, 55, 63, 75, 79, 87, 91, 111, 123, 127, 135),
}


class Refusal(ValueError):
    """Invalid input or inconsistent purported mathematical evidence."""


class Unresolved(Refusal):
    """A bounded attempt failed; no successful event exists for this n."""

    def __init__(self, n, reason, attempted_steps, last_value):
        self.n = n
        self.reason = reason
        self.attempted_steps = attempted_steps
        self.last_value = last_value
        super().__init__(reason)

    def pending(self):
        return {"n": decimal(self.n), "reason": self.reason,
                "attempted_steps": decimal(self.attempted_steps),
                "last_value": decimal(self.last_value)}


def _integer(n, minimum=1, maximum=None, label="integer"):
    if type(n) is not int or n < minimum or (maximum is not None and n > maximum):
        raise Refusal("invalid " + label)
    return n


def decimal(n):
    """Exact decimal formatting without changing Python's global digit policy."""
    _integer(n, 0)
    if n == 0:
        return "0"
    chunks = []
    while n:
        n, chunk = divmod(n, 1000000000)
        chunks.append(chunk)
    return str(chunks[-1]) + "".join(f"{x:09d}" for x in reversed(chunks[:-1]))


def C(n):
    """Standard Collatz definition, with C(1)=4."""
    _integer(n)
    if n % 2:
        return 3 * n + 1
    return n // 2


def T(n):
    """Shortcut definition, independently written, with T(1)=2."""
    _integer(n)
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2


def U(n):
    """Odd-only definition: return (next odd value, exact halving count)."""
    _integer(n)
    if n % 2 == 0:
        raise Refusal("odd-only input must be odd")
    value = 3 * n + 1
    halvings = 0
    while value % 2 == 0:
        value //= 2
        halvings += 1
    return value, halvings


def identity(n, steps):
    """Bounded fixed T-step identity; never a high-value convergence search."""
    _integer(n)
    _integer(steps, 1, 128, "identity steps")
    current = n
    odd = 0
    for _ in range(steps):
        odd += current % 2
        current = T(current)
    return {"value": current, "steps": steps, "odd": odd, "standard": steps + odd}


def classify(n):
    _integer(n, 2, label="rule domain")
    if n % 2 == 0:
        return "E2"
    if n >= 5 and n % 4 == 1:
        return "Q4"
    if n % 3 == 2:
        return "P3"
    if n >= 4 and n % 9 == 4:
        return "M9"
    if n >= 3 and n % 16 == 3:
        return "S2K4-03"
    return "EXPLICIT"


def algebraic_witness(n):
    """Recompute a finite rule witness and its defining T identity."""
    rule = classify(n)
    if rule == "E2":
        witness = n // 2
        valid = T(n) == witness
    elif rule == "Q4":
        witness = 3 * ((n - 1) // 4) + 1
        valid = T(T(n)) == witness
    elif rule == "P3":
        quotient, remainder = divmod(2 * n - 1, 3)
        witness = quotient
        valid = remainder == 0 and witness % 2 == 1 and T(witness) == n
    elif rule == "M9":
        quotient, remainder = divmod(8 * n - 5, 9)
        witness = quotient
        valid = remainder == 0 and T(T(T(witness))) == n
    elif rule == "S2K4-03":
        quotient, remainder = divmod(9 * n + 5, 16)
        witness = quotient
        valid = remainder == 0 and T(T(T(T(n)))) == witness
    else:
        raise Refusal("EXPLICIT requires a bounded first-descent computation")
    if not valid or not 0 < witness < n:
        raise Refusal("invalid algebraic witness")
    return witness


def _event(n, max_t, total_remaining):
    _integer(n, 2, MAX_VALUE, "event start")
    rule = classify(n)
    steps = odd = 0
    if rule != "EXPLICIT":
        witness = algebraic_witness(n)
    else:
        current = n
        while True:
            if steps >= total_remaining:
                raise Unresolved(n, "total_budget", steps, current)
            if steps >= max_t:
                raise Unresolved(n, "step_budget", steps, current)
            following = T(current)
            if following > MAX_VALUE:
                raise Unresolved(n, "resource_refusal", steps, current)
            odd += current % 2
            steps += 1
            current = following
            if current < n:
                witness = current
                break
    frame = "|".join((decimal(n), rule, decimal(steps), decimal(odd), decimal(witness))) + "\n"
    raw = frame.encode("ascii")
    if len(raw) > MAX_FRAME:
        raise Refusal("event frame resource limit")
    return raw


def event(n, max_t=MAX_T):
    _integer(max_t, 1, MAX_T, "per-explicit budget")
    return _event(n, max_t, MAX_TOTAL_T)


def truth_table():
    """Generate every residue by predicates and check the frozen full ledger."""
    generated = tuple(classify(144 + r) for r in range(144))
    pinned = [None] * 144
    for rule, residues in PINNED_RESIDUES.items():
        for residue in residues:
            if pinned[residue] is not None:
                raise Refusal("duplicate pinned residue")
            pinned[residue] = rule
    if generated != tuple(pinned):
        raise Refusal("period-144 truth table mismatch")
    return generated


def expected_counts(start, end):
    _integer(start, 2, label="interval start")
    _integer(end, start, label="interval end")
    counts = dict.fromkeys(COUNT_KEYS, 0)
    for residue, rule in enumerate(truth_table()):
        counts[RULE_COUNT_KEYS[rule]] += ((end - 1 - residue) // 144
                                       - (start - 1 - residue) // 144)
    if sum(counts.values()) != end - start:
        raise Refusal("floor-count conservation failure")
    return counts


def table_rows(k=4):
    """Derive low-residue parity via C and affine data via two recurrences.

    T(0)=0 is extended only inside this finite derivation. No table-based skip
    is activated here; classify has exactly the proved residue-3 predicate.
    """
    _integer(k, 1, 7, "table steps")
    modulus = 1 << k
    rows = []
    for residue in range(modulus):
        current = residue
        parity = []
        for _ in range(k):
            bit = current % 2
            parity.append(bit)
            # Definition-level standard-C steps, separate from T recurrence.
            if bit:
                current = 3 * current + 1
            current //= 2
        a_direct = 3 ** sum(parity)
        b_direct = modulus * current - a_direct * residue
        a = 1
        b = 0
        for j, bit in enumerate(parity):
            if bit:
                a = 3 * a
                b = 3 * b + (1 << j)
        if (a, b) != (a_direct, b_direct) or b < 0:
            raise Refusal("independent affine recurrence mismatch")
        numerator = a * residue + b
        if numerator % modulus or numerator // modulus != current:
            raise Refusal("affine exact divisibility mismatch")
        # Whole-class strict inequality has nonnegative q slope exactly when
        # modulus-a>=0; equality slope is treated as a constant inequality.
        universal_q0 = modulus - a >= 0 and current < residue
        rows.append({"residue": residue, "parity_lsb_first": "".join(map(str, parity)),
                     "odd_count": sum(parity), "affine_a": a, "affine_b": b,
                     "T4_r": current, "universal_q0": universal_q0})
    if k == 4:
        selected = rows[3]
        if (selected["parity_lsb_first"], selected["affine_a"], selected["affine_b"],
                selected["T4_r"], selected["universal_q0"]) != ("1100", 9, 5, 2, True):
            raise Refusal("S2K4-03 whole-class witness mismatch")
        survivors = [r["residue"] for r in rows
                     if r["residue"] % 4 == 3 and r["universal_q0"]]
        if survivors != [3]:
            raise Refusal("unexpected new table exclusion")
    return tuple(rows)


def table_bytes():
    """Build-pinned serialization; one newline-terminated ASCII row per residue."""
    return "".join("|".join(str(row[key]) for key in
                           ("residue", "parity_lsb_first", "affine_a", "affine_b", "T4_r")) + "\n"
                   for row in table_rows()).encode("ascii")


def domain_digest(tag, payload):
    if type(tag) is not str or not tag or not tag.isascii() or "\0" in tag:
        raise Refusal("invalid digest domain")
    if type(payload) is not bytes:
        raise Refusal("digest payload must be bytes")
    return hashlib.sha3_256(DOMAIN + tag.encode("ascii") + b"\0" + payload).hexdigest()


def table_digest():
    return domain_digest("TABLE", table_bytes())


def verify_table(raw):
    if type(raw) is not bytes or raw != table_bytes():
        raise Refusal("parity-table bytes mismatch")
    return table_digest()


def check_rules():
    """Execute bounded mathematical fixtures without authorising a scan."""
    rows = table_rows()
    assignment = truth_table()
    for n in range(2, 10001):
        if classify(n) != assignment[n % 144]:
            raise Refusal("rule periodicity mismatch")
        if classify(n) != "EXPLICIT":
            algebraic_witness(n)
    # Strict all-q S2 inequality is the P1 proof; these exact identities are
    # independent fixtures and are not a substitute for that universal proof.
    for k in range(1, 8):
        for row in table_rows(k):
            for q in (0, 1, 3):
                current = (1 << k) * q + row["residue"]
                for _ in range(k):
                    current = current // 2 if current % 2 == 0 else (3 * current + 1) // 2
                if current != row["affine_a"] * q + row["T4_r"]:
                    raise Refusal("bounded parity-affine identity mismatch")
    return {"scope": "NONSCIENTIFIC", "parity_rows": len(rows),
            "priority_residues": len(assignment), "table_digest": table_digest()}


def replay(start, end, max_t=MAX_T, max_total=MAX_TOTAL_T):
    """Fresh complete/prefix replay; counters contain successful events only."""
    _integer(start, 2, MAX_VALUE, "batch start")
    # An empty replay is necessary to validate a checkpoint's empty prefix.
    # The driver separately requires a nonempty scientific batch manifest.
    _integer(end, start, MAX_VALUE, "batch end")
    _integer(end - start, 0, MAX_BATCH, "batch width")
    _integer(max_t, 1, MAX_T, "per-explicit budget")
    _integer(max_total, 1, MAX_TOTAL_T, "total budget")
    counts = dict.fromkeys(COUNT_KEYS, 0)
    digest = hashlib.sha3_256(DOMAIN + b"EVENTS\0")
    t_steps = odd_steps = attempts = 0
    next_n = start
    pending = None
    while next_n < end:
        rule = classify(next_n)
        attempts += int(rule == "EXPLICIT")
        try:
            frame = _event(next_n, max_t, max_total - t_steps)
        except Unresolved as failure:
            pending = failure.pending()
            break
        fields = frame.decode("ascii").rstrip("\n").split("|")
        # These are our own freshly derived event bytes, not a native stream.
        t_steps += int(fields[2])
        odd_steps += int(fields[3])
        counts[RULE_COUNT_KEYS[rule]] += 1
        digest.update(frame)
        next_n += 1
    if counts != expected_counts(start, next_n):
        raise Refusal("replayed prefix counters mismatch")
    return {"next_n": next_n, "complete": next_n == end, "pending": pending,
            "counts": counts, "transcript_digest": digest.hexdigest(),
            "explicit_t_steps": t_steps, "explicit_odd_steps": odd_steps,
            "explicit_standard_steps": t_steps + odd_steps, "explicit_attempts": attempts}


def iter_events(start, end, max_t=MAX_T):
    """Bounded event iterator for independent byte comparisons in tiny fixtures."""
    _integer(start, 2, MAX_VALUE, "interval start")
    _integer(end, start, MAX_VALUE, "interval end")
    _integer(end - start, 0, MAX_BATCH, "batch width")
    _integer(max_t, 1, MAX_T, "per-explicit budget")
    for n in range(start, end):
        yield event(n, max_t)
