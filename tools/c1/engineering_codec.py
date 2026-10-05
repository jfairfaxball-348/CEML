"""Stage: hardware characterization; bounded C1 engineering helpers only.

The JSON encoder supports the ASCII, number-free subset of RFC 8785 used by
these engineering artifacts. It is not a full JCS implementation or a schema
validator. Quantities must be canonical decimal strings checked by the caller
against their schema. No scientific generator, trajectory or production codec
is implemented here. See CODEX_HANDOFF sections 10 and 12.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re


class CodecRefusal(ValueError):
    """Unsupported or noncanonical engineering input, with no captured values."""


def canonical_decimal(value: str) -> str:
    """Check a nonnegative canonical decimal quantity without converting it."""
    if type(value) is not str or re.fullmatch(r"0|[1-9][0-9]*", value) is None:
        raise CodecRefusal("expected a canonical nonnegative decimal string")
    return value


def canonical_bytes(obj: object) -> bytes:
    """Encode only ASCII strings/keys, dicts, lists, booleans and null.

    ASCII key ordering agrees with JCS UTF-16 ordering; its string escaping
    agrees with json.dumps here. JSON numbers and all non-ASCII strings are
    refused instead of approximating unsupported JCS behavior.
    """
    active: set[int] = set()

    def check(value: object) -> None:
        if value is None or type(value) is bool:
            return
        if type(value) is str:
            if not value.isascii():
                raise CodecRefusal("non-ASCII strings are unsupported")
            return
        if type(value) not in (dict, list):
            raise CodecRefusal("JSON numbers and unsupported types are refused")
        if id(value) in active:
            raise CodecRefusal("cyclic objects are unsupported")
        active.add(id(value))
        try:
            if type(value) is dict:
                for key, child in value.items():
                    if type(key) is not str or not key.isascii():
                        raise CodecRefusal("object keys must be ASCII strings")
                    check(child)
            else:
                for child in value:
                    check(child)
        finally:
            active.remove(id(value))

    check(obj)
    return json.dumps(
        obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"),
        allow_nan=False,
    ).encode("ascii")


def u64be(value: int) -> bytes:
    if type(value) is not int or not 0 <= value < 2**64:
        raise CodecRefusal("frame length must fit an unsigned 64-bit integer")
    return value.to_bytes(8, "big")


def blob(value: bytes) -> bytes:
    if type(value) is not bytes:
        raise CodecRefusal("BLOB requires bytes")
    return u64be(len(value)) + value


def uenc(value: int) -> bytes:
    if type(value) is not int or value < 0:
        raise CodecRefusal("UENC requires a nonnegative integer")
    magnitude = value.to_bytes(max(1, (value.bit_length() + 7) // 8), "big")
    return blob(magnitude)


def decode_uenc(value: bytes) -> int:
    """Decode exactly one UENC frame, rejecting trailing/nonminimal bytes."""
    if type(value) is not bytes or len(value) < 9:
        raise CodecRefusal("incomplete UENC frame")
    length = int.from_bytes(value[:8], "big")
    if length != len(value) - 8:
        raise CodecRefusal("UENC frame length mismatch")
    magnitude = value[8:]
    if len(magnitude) > 1 and magnitude[0] == 0:
        raise CodecRefusal("nonminimal UENC magnitude")
    return int.from_bytes(magnitude, "big")


def artifact_digest(obj: dict) -> str:
    """I1 generic artifact digest; omit only top-level artifact_digest.

    Schema validation and the sensitive-data gate are separate requirements.
    Dedicated build/profile digest domains are deliberately unsupported.
    """
    if type(obj) is not dict:
        raise CodecRefusal("engineering artifact must be an object")
    version = obj.get("schema_version")
    if type(version) is not str or not version or not version.isascii():
        raise CodecRefusal("artifact requires a nonempty ASCII schema version")
    if "build_digest" in obj or "machine_profile_digest" in obj:
        raise CodecRefusal("build/profile artifacts require dedicated domains")
    body = {key: value for key, value in obj.items() if key != "artifact_digest"}
    preimage = (
        b"CEML-I1-ENGINEERING-ARTIFACT-V1\0"
        + blob(version.encode("ascii")) + blob(canonical_bytes(body))
    )
    return hashlib.sha3_256(preimage).hexdigest()


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise CodecRefusal("duplicate JSON key")
        result[key] = value
    return result


def self_test_vector(suite_path: Path | None = None) -> dict:
    """Reproduce only the normative 256-bit CEML-CAL-1 input and zero counters.

    There is no configurable workload or stepping path. This tiny engineering
    vector is a prerequisite, not a benchmark or evidence of V1 completion.
    """
    if suite_path is None:
        suite_path = Path(__file__).resolve().parents[2] / "config/calibration_suite_v1.json"
    suite = json.loads(suite_path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    canonical_bytes(suite)
    expected_header = {
        "suite_version": "CEML-CAL-1",
        "purpose": "engineering-only",
        "random_domain_label": "CEML-CALIBRATION-RANDOM-V1",
        "public_seed_hex": "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f",
        "scientific_master_seed_permitted": False,
        "scientific_start_permitted": False,
    }
    if type(suite) is not dict or any(suite.get(k) != v for k, v in expected_header.items()):
        raise CodecRefusal("suite identity does not match the fixed engineering vector")
    vector = suite.get("generator_test_vector")
    identity = {
        "family": "route-crossover", "size_bits": "256", "case_index": "0",
        "stream_index": "0", "input_id": "cal1/01/route-crossover/256/0",
    }
    outputs = {"shake_output_hex", "state_hex", "descriptor_jcs", "input_digest", "initial_state_digest"}
    if type(vector) is not dict or set(vector) != set(identity) | outputs:
        raise CodecRefusal("unexpected engineering vector structure")
    if any(vector[k] != v for k, v in identity.items()):
        raise CodecRefusal("only the fixed 256-bit engineering vector is supported")
    for field in ("size_bits", "case_index", "stream_index"):
        canonical_decimal(vector[field])
    descriptor = {
        "case_index": "0", "family": "route-crossover",
        "generator": "shake256-ceml-calibration-random-v1",
        "input_id": identity["input_id"],
        "operand_roles": [{"forced_odd": True, "role": "state", "size_bits": "256", "stream_index": "0"}],
        "size_bits": "256", "suite_version": "CEML-CAL-1",
    }
    message = (
        b"CEML-CALIBRATION-RANDOM-V1\0"
        + bytes.fromhex(expected_header["public_seed_hex"])
        + blob(b"route-crossover") + uenc(256) + uenc(0) + uenc(0)
    )
    raw = hashlib.shake_256(message).digest(32)
    state = (int.from_bytes(raw, "big") & ((1 << 256) - 1)) | (1 << 255) | 1
    descriptor_bytes = canonical_bytes(descriptor)
    actual = {
        "shake_output_hex": raw.hex(),
        "state_hex": state.to_bytes(32, "big").hex(),
        "descriptor_jcs": descriptor_bytes.decode("ascii"),
        "input_digest": hashlib.sha3_256(
            b"CEML-I1-CALIBRATION-INPUT-V1\0" + blob(descriptor_bytes) + blob(uenc(state))
        ).hexdigest(),
        "initial_state_digest": hashlib.sha3_256(
            b"CEML-I1-CALIBRATION-STATE-V1\0" + uenc(state) + uenc(0) * 3
        ).hexdigest(),
    }
    if any(actual[key] != vector[key] for key in sorted(outputs)):
        raise CodecRefusal("frozen engineering vector mismatch")
    return {
        "stage": "hardware characterization", "purpose": "engineering-only",
        "suite_version": "CEML-CAL-1", "status": "PASS",
        "input_id": identity["input_id"],
        "checks": {key: True for key in sorted(outputs)},
        "input_digest": actual["input_digest"],
        "initial_state_digest": actual["initial_state_digest"],
        "represented_shortcut_steps": "0",
        "scope": "Fixed generator vector only; no benchmark, trajectory or V1 execution.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="C1 engineering codec, fixed vector only")
    parser.add_argument("command", choices=("self-test",))
    parser.parse_args()
    try:
        result = self_test_vector()
    except (OSError, ValueError, TypeError, RecursionError):
        print('{"purpose":"engineering-only","status":"REFUSED","reason":"Fixed vector unavailable or mismatched"}')
        return 1
    print(canonical_bytes(result).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
