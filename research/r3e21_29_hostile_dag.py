#!/usr/bin/env python3
"""R3E21-29 independent research-only toy verifier. No frontier science."""
import copy
import hashlib
import json
from collections import Counter

SCHEME = "CEML-R29-TOY-1"
MAX_DEPTH = 24
MAX_BYTES = 8_000_000
MAX_PATH = 512
MAX_BITS = 512

class Reject(Exception):
    pass

def need(cond, code):
    if not cond:
        raise Reject(code)

def integer(x):
    return type(x) is int and x.bit_length() <= MAX_BITS

def T(n):
    need(integer(n) and n > 0, "NONPOSITIVE_OR_OVERFLOW")
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def bounds(L, H, k, r):
    d = 1 << k
    a = -((r - L) // d)
    b = -((r - H) // d) - 1
    return a, b

def elements(L, H, k, r):
    a, b = bounds(L, H, k, r)
    return max(0, b - a + 1), (r + (1 << k) * a if a <= b else None)

def affine(k, r):
    need(0 <= k <= MAX_DEPTH and 0 <= r < (1 << k), "BAD_CONTEXT")
    s, c, z, word = 0, 0, r, []
    for j in range(k):
        odd = z % 2
        word.append(odd)
        if odd:
            s += 1
            c = 3 * c + (1 << j)
            z = (3 * z + 1) // 2
        else:
            z //= 2
    return s, c, "".join(map(str, word))

def descent(k, r, L, H, cl):
    count, nmin = elements(L, H, k, r)
    need(count > 0, "EMPTY_DESCENT")
    s, c, w = affine(k, r)
    need(set(cl) == {"type", "k", "r", "s", "c", "word", "nmin"}, "BAD_FIELDS")
    need(all(integer(cl[x]) for x in ("k", "r", "s", "c", "nmin")),
         "NONINTEGER_OR_OVERFLOW")
    need((cl["k"], cl["r"], cl["s"], cl["c"], cl["word"], cl["nmin"]) ==
         (k, r, s, c, w, nmin), "FALSE_AFFINE_OR_MIN_OR_WORD")
    need(2 ** k > 3 ** s and (2 ** k - 3 ** s) * nmin > c,
         "NO_UNIFORM_DESCENT")

def trace(seq, start):
    need(type(seq) is list and 1 <= len(seq) <= MAX_PATH, "BAD_PATH_LENGTH")
    need(seq[0] == start, "BAD_PATH_START")
    for a, b in zip(seq, seq[1:]):
        need(integer(b) and b > 0 and T(a) == b, "INVALID_TRUE_STEP")

def digest(record):
    clone = {k: v for k, v in record.items() if k != "sha256"}
    return hashlib.sha256(json.dumps(
        clone, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def seal(record):
    record["sha256"] = digest(record)
    return record

def check(record):
    raw = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    need(len(raw) <= MAX_BYTES, "TOO_MANY_BYTES")
    need(set(record) == {"scheme", "L", "H", "root", "nodes", "sha256"},
         "BAD_ROOT_FIELDS")
    need(record["scheme"] == SCHEME, "WRONG_SCHEME")
    L, H = record["L"], record["H"]
    need(integer(L) and integer(H) and 1 <= L < H,
         "BAD_INTERVAL_OR_OVERFLOW")
    need(isinstance(record["nodes"], dict) and len(record["nodes"]) <= 50000,
         "NODE_LIMIT")
    need(digest(record) == record["sha256"], "HASH_FAIL")
    visited = {}
    def visit(idx, k, r):
        need(k <= MAX_DEPTH, "DEPTH_LIMIT")
        need(isinstance(idx, str) and idx in record["nodes"], "MISSING_CHILD")
        current = (k, r, L, H)
        need(idx not in visited or visited[idx] == current, "CONTEXT_ALIAS")
        need(idx not in visited, "CYCLE_OR_DUPLICATE")
        visited[idx] = current
        node = record["nodes"][idx]
        need(isinstance(node, dict), "NODE_MALFORMED")
        count, nmin = elements(L, H, k, r)
        ty = node.get("type")
        need(node.get("k") == k and node.get("r") == r
             and integer(node.get("k")) and integer(node.get("r")),
             "WRONG_CYLINDER")
        if ty == "EMPTY":
            need(set(node) == {"type", "k", "r"}, "BAD_FIELDS")
            need(count == 0, "FALSE_EMPTY")
        elif ty == "SPLIT":
            need(set(node) == {"type", "k", "r", "children"}, "BAD_FIELDS")
            children = node["children"]
            need(type(children) is list and len(children) == 2
                 and children[0] != children[1], "SPLIT_OVERLAP")
            visit(children[0], k + 1, r)
            visit(children[1], k + 1, r + (1 << k))
        elif ty == "DESCENT":
            descent(k, r, L, H, node)
        elif ty == "EXPLICIT":
            need(set(node) == {"type", "k", "r", "n", "path"}, "BAD_FIELDS")
            need(count == 1 and nmin == node["n"], "EXPLICIT_NOT_SINGLETON")
            trace(node["path"], nmin)
            need(0 < node["path"][-1] < nmin, "NO_STRICT_DESCENT")
        elif ty == "MEET":
            need(set(node) ==
                 {"type", "k", "r", "n", "p", "path_n", "path_p"}, "BAD_FIELDS")
            need(count == 1 and nmin == node["n"] and integer(node["p"])
                 and 0 < node["p"] < nmin, "BAD_PREDECESSOR")
            trace(node["path_n"], nmin)
            trace(node["path_p"], node["p"])
            need(node["path_n"][-1] == node["path_p"][-1],
                 "UNRELATED_ENDPOINT")
        else:
            raise Reject("UNKNOWN_NODE_TYPE")
    visit(record["root"], 0, 0)
    need(len(visited) == len(record["nodes"]), "UNREACHABLE_NODE")
    return len(visited)

def path_to_smaller(n):
    z, out = n, [n]
    for _ in range(MAX_PATH - 1):
        z = T(z)
        out.append(z)
        if z < n:
            return out
    raise Reject("FIXTURE_NO_DESCENT_WITHIN_CAP")

def generate(L, H):
    nodes = {}
    def walk(k, r):
        idx = str(len(nodes))
        nodes[idx] = None
        count, nmin = elements(L, H, k, r)
        common = {"k": k, "r": r}
        if count == 0:
            val = {**common, "type": "EMPTY"}
        else:
            s, c, w = affine(k, r)
            if k > 0 and (2 ** k - 3 ** s) * nmin > c and 2 ** k > 3 ** s:
                val = {**common, "type": "DESCENT",
                       "s": s, "c": c, "word": w, "nmin": nmin}
            elif count == 1:
                val = {**common, "type": "EXPLICIT",
                       "n": nmin, "path": path_to_smaller(nmin)}
            else:
                need(k < MAX_DEPTH, "FIXTURE_SPLIT_DEPTH")
                val = {**common, "type": "SPLIT",
                       "children": [walk(k + 1, r),
                                    walk(k + 1, r + (1 << k))]}
        nodes[idx] = val
        return idx
    root = walk(0, 0)
    return seal({"scheme": SCHEME, "L": L, "H": H,
                 "root": root, "nodes": nodes})

def count_bad_prefix(k):
    q = {0: 1}
    for j in range(1, k + 1):
        nxt = Counter()
        for s, c in q.items():
            if 3 ** s >= 2 ** j:
                nxt[s] += c
            if 3 ** (s + 1) >= 2 ** j:
                nxt[s + 1] += c
        q = dict(nxt)
    return sum(q.values())

def adversarial():
    base = generate(1027, 1155)
    c0 = check(base)
    counts = Counter(x["type"] for x in base["nodes"].values())
    assert len(base["nodes"]) == c0
    cases = []
    def mutated(label, fn, expected):
        v = copy.deepcopy(base)
        fn(v)
        seal(v)
        try:
            check(v)
        except Reject as e:
            if str(e) != expected:
                raise AssertionError((label, expected, str(e)))
            cases.append((label, str(e)))
        else:
            raise AssertionError("accepted tampering: " + label)
    split = next(k for k, v in base["nodes"].items()
                 if v["type"] == "SPLIT")
    des = next(k for k, v in base["nodes"].items()
               if v["type"] == "DESCENT")
    explicit = next(k for k, v in base["nodes"].items()
                    if v["type"] == "EXPLICIT")
    mutated("missing_child",
            lambda v: v["nodes"][split]["children"].__setitem__(0, "not-present"),
            "MISSING_CHILD")
    mutated("overlapping_child",
            lambda v: v["nodes"][split]["children"].__setitem__(
                1, v["nodes"][split]["children"][0]),
            "SPLIT_OVERLAP")
    mutated("wrong_minimum",
            lambda v: v["nodes"][des].__setitem__(
                "nmin", v["nodes"][des]["nmin"] + 1),
            "FALSE_AFFINE_OR_MIN_OR_WORD")
    mutated("mismatched_parity",
            lambda v: v["nodes"][des].__setitem__(
                "word",
                ("1" if v["nodes"][des]["word"][0] == "0" else "0") +
                v["nodes"][des]["word"][1:]),
            "FALSE_AFFINE_OR_MIN_OR_WORD")
    mutated("u128_wraparound",
            lambda v: v["nodes"][des].__setitem__(
                "c", v["nodes"][des]["c"] + (1 << 128)),
            "FALSE_AFFINE_OR_MIN_OR_WORD")
    mutated("arbitrarily_large_bits",
            lambda v: v["nodes"][des].__setitem__("c", 1 << 600),
            "NONINTEGER_OR_OVERFLOW")
    mutated("fake_explicit_step",
            lambda v: v["nodes"][explicit]["path"].__setitem__(1, 99),
            "INVALID_TRUE_STEP")
    mutated("zero_terminal",
            lambda v: v["nodes"][explicit]["path"].__setitem__(-1, 0),
            "INVALID_TRUE_STEP")
    mutated("context_free_alias",
            lambda v: v["nodes"][v["nodes"][split]["children"][1]]["children"].
            __setitem__(1, des),
            "CONTEXT_ALIAS")
    v = copy.deepcopy(base)
    v["nodes"][des]["nmin"] += 1
    try:
        check(v)
    except Reject as e:
        assert str(e) == "HASH_FAIL"
        cases.append(("forged_checksum", "HASH_FAIL"))
    else:
        raise AssertionError("forged checksum")
    k, r = 4, 1
    s, c, w = affine(k, r)
    bad = {"type": "DESCENT", "k": k, "r": r,
           "s": s, "c": c, "word": w, "nmin": 1}
    try:
        descent(k, r, 1, 2, bad)
    except Reject as e:
        assert str(e) == "NO_UNIFORM_DESCENT"
        cases.append(("r1_mod16_false_rule", str(e)))
    else:
        raise AssertionError("false r1 accepted")
    bad["nmin"] = 17
    try:
        descent(k, r, 18, 19, bad)
    except Reject as e:
        assert str(e) == "EMPTY_DESCENT"
        cases.append(("clipped_partial_unit", str(e)))
    else:
        raise AssertionError("clipped unit accepted")
    pn = path_to_smaller(7)
    meet = seal({"scheme": SCHEME, "L": 7, "H": 8,
                 "root": "0", "nodes": {"0": {
                     "type": "MEET", "k": 0, "r": 0, "n": 7,
                     "p": pn[-1], "path_n": pn, "path_p": [pn[-1]]}}})
    assert pn[-1] == 5 and check(meet) == 1
    for p in (0, -5, 8):
        v = copy.deepcopy(meet)
        v["nodes"]["0"]["p"] = p
        seal(v)
        try:
            check(v)
        except Reject as e:
            assert str(e) == "BAD_PREDECESSOR"
            cases.append(("bad_predecessor_" + str(p), str(e)))
        else:
            raise AssertionError("bad predecessor")
    v = copy.deepcopy(meet)
    v["nodes"]["0"]["path_p"] = [5, 8]
    seal(v)
    try:
        check(v)
    except Reject as e:
        assert str(e) == "UNRELATED_ENDPOINT"
        cases.append(("unrelated_endpoint", str(e)))
    else:
        raise AssertionError("unrelated endpoint accepted")
    clipped = generate((1 << 40) - 3, (1 << 40) + 17)
    assert check(clipped) == len(clipped["nodes"])
    return c0, counts, len(json.dumps(
        base, sort_keys=True, separators=(",", ":")).encode()), cases, len(clipped["nodes"])

def main():
    for k, v in ((8, 19), (16, 2114), (24, 286581),
                 (32, 41347483), (40, 6402835000)):
        assert count_bad_prefix(k) == v
        print("PREFIX_OBSTRUCTION", k, v, "out_of", 1 << k)
    n, c, b, cases, clip = adversarial()
    print("GOOD_TOY_NODES", n, "TYPES", dict(c),
          "BYTES", b, "CLIPPED_NODES", clip)
    for label, status in cases:
        print("REJECT", label, status)
    print("R29_RESEARCH_ONLY_PASS", len(cases), "adversarial rejection cases")

if __name__ == "__main__":
    main()
