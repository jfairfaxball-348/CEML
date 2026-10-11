"""Local-only pinned build of the distinct CEML-FRONTIER-2 worker.

Reads retained cache and previously extracted pinned bytes. It has no archive
download/extraction path, legacy engine invocation, telemetry or Git write.
The PE/export and compiler-environment primitives are narrowly adapted from
tools/c1/gmp_setup.py and cal1_build.py without importing their acquire path.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "local/frontier/build"
PIN = ROOT / "config/c1_gmp_pin.toml"
FLAGS = ["-nologo", "-std:c17", "-W4", "-WX", "-O2", "-MD",
         "-D_CRT_SECURE_NO_WARNINGS", "-Brepro", "-external:I.", "-external:W0"]
CHECKED_FLAGS = ["-nologo", "-std:c17", "-W4", "-WX", "-Od", "-RTC1", "-MD",
                 "-D_CRT_SECURE_NO_WARNINGS", "-Brepro", "-external:I.", "-external:W0"]
NATIVE = ("src/frontier_main.c", "src/frontier_worker.c", "src/frontier_worker.h",
          "src/ceml_oracle.c", "src/ceml_oracle.h")
FIXED = ("config/c1_gmp_pin.toml", "config/c1_dependency_manifest.toml",
         "config/frontier_snapshot_v1.json", "config/frontier_snapshot_v2.json",
         "docs/FRONTIER_PROTOCOL_V1.md", "docs/FRONTIER_PROTOCOL_V2.md",
         "docs/P1_EXCLUSION_PROOFS.md", "docs/P2_PROTOCOL_AUDIT.md", "tools/c1/gmp_smoke.c")
MANIFEST_NAME = "build_manifest.json"
MANIFEST_SCHEMA = "CEML-FRONTIER-2-BUILD"
DOMAIN = b"CEML-FRONTIER-2/"


class Refusal(Exception):
    """A bounded, path-free refusal safe to record."""


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def domain_hash(tag, data):
    return hashlib.sha3_256(DOMAIN + tag.encode("ascii") + b"\0" + data).hexdigest()


def hashes(data):
    return {"sha256": hashlib.sha256(data).hexdigest(),
            "sha3_256": hashlib.sha3_256(data).hexdigest(), "bytes": str(len(data))}


def lf(path):
    return path.read_bytes().replace(b"\r\n", b"\n")


def table_bytes():
    """Build-time derivation independent of reference.py and native helpers."""
    output = []
    for r in range(16):
        values = [r, r + 16]
        word = []
        for _ in range(4):
            bits = [v % 2 for v in values]
            if bits[0] != bits[1]:
                raise Refusal("Parity lift table disagreement")
            word.append(bits[0])
            values = [(3*v + 1)//2 if v % 2 else v//2 for v in values]
        direct_a = values[1] - values[0]
        direct_b = 16*values[0] - direct_a*r
        a, b = 1, 0
        for j, bit in enumerate(word):
            if bit:
                a, b = 3*a, 3*b + 2**j
        if a != direct_a or b != direct_b or (a*r+b) % 16:
            raise Refusal("Affine table disagreement")
        if r == 3 and (word != [1, 1, 0, 0] or a != 9 or b != 5 or values[0] != 2
                       or 16-a <= 0 or r-values[0] <= 0):
            raise Refusal("Activated S2 universal inequality disagreement")
        output.append(f"{r}|{''.join(map(str, word))}|{a}|{b}|{values[0]}\n")
    return "".join(output).encode("ascii")


def input_paths():
    paths = set(NATIVE + FIXED)
    paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/"tools/frontier").rglob("*.py"))
    paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/"tests/frontier").rglob("*.py"))
    paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/"src").glob("frontier_*.c"))
    paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/"src").glob("frontier_*.h"))
    paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/"schemas").glob("frontier_*.schema.json"))
    expected = {f"schemas/frontier_{kind}_v{version}.schema.json" for version in (1, 2)
                for kind in ("snapshot", "run", "checkpoint", "certificate")}
    if {p for p in paths if p.startswith("schemas/")} != expected:
        raise Refusal("Frozen schema set incomplete or unexpected")
    return sorted(paths)


def inputs():
    result = {}
    for name in input_paths():
        path = ROOT/name
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 2*1024*1024:
            raise Refusal("Build input missing or oversized")
        # LF-normalised only: a CRLF checkout must not change the build identity.
        result[name] = {"lf": hashes(lf(path))}
    return result


def suite_digest(values):
    subset = {k: v for k, v in values.items() if k.startswith("tests/frontier/")}
    return domain_hash("TEST-SOURCES", canonical(subset))


def invoke(args, env=None, cwd=None, timeout=60):
    try:
        process = subprocess.run(args, env=env, cwd=cwd, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise Refusal("Local build tool unavailable or timed out") from error
    if len(process.stdout) > 1024*1024 or process.returncode != 0:
        raise Refusal("Local build tool refused; raw diagnostics retained only in memory")
    return process.stdout


def pe_info(data):
    """Bounds-checked public PE32+ export/import adapter from frozen C1."""
    def read(fmt, offset):
        length = struct.calcsize(fmt)
        if offset < 0 or offset+length > len(data):
            raise Refusal("Malformed PE extent")
        return struct.unpack_from(fmt, data, offset)
    if data[:2] != b"MZ":
        raise Refusal("PE header absent")
    pe, = read("<I", 60)
    if data[pe:pe+4] != b"PE\0\0":
        raise Refusal("PE signature absent")
    machine, count = read("<HH", pe+4)
    optional_size, = read("<H", pe+20)
    optional = pe+24
    magic, = read("<H", optional)
    if machine != 0x8664 or magic != 0x20b or count > 96 or optional_size < 128:
        raise Refusal("Unexpected PE target")
    sections = []
    for i in range(count):
        offset = optional+optional_size+40*i
        virtual_size, address, raw_size, raw = read("<IIII", offset+8)
        flags, = read("<I", offset+36)
        sections.append((address, max(virtual_size, raw_size), raw, raw_size, flags))
    def locate(rva):
        for address, extent, raw, raw_size, flags in sections:
            if address <= rva < address+extent and rva-address < raw_size:
                return raw+rva-address, flags
        raise Refusal("Unmapped PE data")
    def name(rva):
        offset, _ = locate(rva)
        end = data.find(b"\0", offset, min(len(data), offset+512))
        if end < 0:
            raise Refusal("Unterminated PE name")
        value = data[offset:end].decode("ascii")
        if not re.fullmatch(r"[A-Za-z0-9_.?-]+", value):
            raise Refusal("Unexpected PE name")
        return value
    export_rva, export_size, import_rva, _ = read("<IIII", optional+112)
    imports, exports = [], {}
    if import_rva:
        offset, _ = locate(import_rva)
        for i in range(256):
            record = read("<IIIII", offset+20*i)
            if not any(record):
                break
            imports.append(name(record[3]))
        else:
            raise Refusal("Too many PE imports")
    if export_rva:
        offset, _ = locate(export_rva)
        nfunc, nnames, functions, names, ordinals = read("<IIIII", offset+20)
        if nnames > 10000 or nfunc > 10000:
            raise Refusal("Too many PE exports")
        foff, _ = locate(functions)
        noff, _ = locate(names)
        ooff, _ = locate(ordinals)
        for i in range(nnames):
            nrva, = read("<I", noff+4*i)
            ordinal, = read("<H", ooff+2*i)
            if ordinal >= nfunc:
                raise Refusal("Bad PE export ordinal")
            frva, = read("<I", foff+4*ordinal)
            if export_rva <= frva < export_rva+export_size:
                raise Refusal("Forwarded PE export unsupported")
            matches = [s for s in sections if s[0] <= frva < s[0]+s[1]]
            if len(matches) != 1:
                raise Refusal("Unmapped PE export")
            exports[name(nrva)] = "function" if matches[0][4] & 0x20000000 else "data"
    return {"imports": sorted(imports), "exports": exports}


_LOCATED = None


def toolchain():
    """Locate the pinned compiler and hash its binaries.

    The installation path and its vcvars environment are discovered once per
    process. The five tool binaries are re-read and re-hashed on every call, so
    a changed compiler still refuses.
    """
    global _LOCATED
    if _LOCATED is None:
        _LOCATED = locate_toolchain()
    env, bindir, version, sdk = _LOCATED
    metadata = {"msvc_tools_version": version, "windows_sdk_version": sdk,
                "target": "x86_64-pc-windows-msvc", "abi": "LLP64",
                "sdk_closure_content_hashed": "no",
                "tool_sha3_256": {n: hashes((bindir/n).read_bytes())["sha3_256"]
                                  for n in ("cl.exe", "link.exe", "lib.exe", "c1.dll", "c2.dll")}}
    return dict(env), bindir, metadata


def locate_toolchain():
    if os.name != "nt":
        raise Refusal("Pinned Windows toolchain required")
    locator = Path(os.environ.get("ProgramFiles(x86)", ""))/"Microsoft Visual Studio/Installer/vswhere.exe"
    root = Path(invoke([str(locator), "-latest", "-products", "*", "-requires",
                       "Microsoft.VisualStudio.Component.VC.Tools.x86.x64", "-property",
                       "installationPath"]).decode("utf-8-sig").strip())
    script = root/"VC/Auxiliary/Build/vcvars64.bat"
    processor = os.environ.get("COMSPEC", "cmd.exe")
    unsafe = ('"', "\n", "\r", "%", "!", "&", "|", "<", ">", "^")
    if not root.is_absolute() or not script.is_file() or any(c in str(script) or c in processor for c in unsafe):
        raise Refusal("Unsupported compiler locator")
    initial = dict(os.environ)
    for key in ("CL", "_CL_", "LINK", "_LINK_", "INCLUDE", "LIB", "LIBPATH"):
        initial.pop(key, None)
    command = f'"{processor}" /d /s /c "call "{script}" >nul && set"'
    output = invoke(command, env=initial)
    env = initial.copy()
    for line in output.decode("mbcs").splitlines():
        if "=" in line and not line.startswith("="):
            key, value = line.split("=", 1)
            env[key.upper()] = value
    version = (root/"VC/Auxiliary/Build/Microsoft.VCToolsVersion.default.txt").read_text().strip()
    sdk = env.get("WINDOWSSDKVERSION", "").strip("\\/")
    if not re.fullmatch(r"\d+(?:\.\d+){2,3}", version) or not re.fullmatch(r"\d+(?:\.\d+){2,3}", sdk):
        raise Refusal("Toolchain version unavailable")
    return env, root/"VC/Tools/MSVC"/version/"bin/Hostx64/x64", version, sdk


def dependency_check():
    pin = tomllib.loads(PIN.read_text(encoding="utf-8"))
    if pin["version"] != "6.3.0" or pin["distribution_release"] != "6.3.0-2" or pin["compiler_flags"] != FLAGS:
        raise Refusal("Frozen dependency or flags mismatch")
    if pin["python_version"] != ".".join(map(str, sys.version_info[:3])):
        raise Refusal("Pinned Python version mismatch")
    for kind, name in (("binary", "mingw-w64-ucrt-x86_64-gmp-6.3.0-2-any.pkg.tar.zst"),
                       ("source", "mingw-w64-gmp-6.3.0-2.src.tar.zst")):
        path = ROOT/"local/c1/cache/sha256"/pin[kind+"_sha256"]/name
        if not path.is_file() or path.stat().st_size > 32*1024*1024:
            raise Refusal("Pinned offline archive absent or oversized; operator provisioning required")
        value = hashes(path.read_bytes())
        if value["sha256"] != pin[kind+"_sha256"] or value["sha3_256"] != pin[kind+"_sha3_256"]:
            raise Refusal("Pinned retained archive checksum mismatch")
    extracted = ROOT/"local/c1/gmp-setup/offline"
    for name, key in (("gmp.h", "header_sha3_256"), ("libgmp-10.dll", "dll_sha3_256")):
        path = extracted/name
        if not path.is_file() or path.stat().st_size > 16*1024*1024 or hashes(path.read_bytes())["sha3_256"] != pin[key]:
            raise Refusal("Provisioned header or DLL missing/mismatched; operator provisioning required")
    env, bindir, metadata = toolchain()
    if (metadata["msvc_tools_version"] != pin["msvc_tools_version"]
            or metadata["windows_sdk_version"] != pin["windows_sdk_version"]
            or metadata["tool_sha3_256"] != pin["tool_sha3_256"]):
        raise Refusal("Frozen compiler content or version mismatch")
    return pin, extracted, env, bindir, metadata


def command(executable="ceml_frontier.exe", flags=None):
    return ["cl.exe", *(FLAGS if flags is None else flags), "-I.",
            "frontier_main.c", "frontier_worker.c", "ceml_oracle.c", "gmp_public.lib",
            "-Fe:"+executable, "-link", "-Brepro"]


def definition(exports, memory):
    public_data = {"__gmp_version", "__gmp_bits_per_limb"}
    if memory:
        public_data.update(("__gmp_set_memory_functions", "__gmp_get_memory_functions"))
    allowed = {k: v for k, v in exports.items() if k.startswith("__gmpz_") or k in public_data}
    if allowed.get("__gmpz_mul") != "function" or (memory and allowed.get("__gmp_set_memory_functions") != "function"):
        raise Refusal("Public GMP exports unavailable")
    return ("LIBRARY libgmp-10.dll\nEXPORTS\n" + "".join(
        n+(" DATA" if k == "data" else "")+"\n" for n, k in sorted(allowed.items()))).encode("ascii")


def compile_at(folder, env, bindir, extracted, pin):
    folder.mkdir(parents=True, exist_ok=True)
    for name in ("gmp.h", "libgmp-10.dll"):
        (folder/name).write_bytes((extracted/name).read_bytes())
    exports = pe_info((folder/"libgmp-10.dll").read_bytes())["exports"]
    for stem, memory in (("gmp", False), ("gmp_public", True)):
        (folder/(stem+".def")).write_bytes(definition(exports, memory))
        invoke([str(bindir/"lib.exe"), "-nologo", "-Brepro", "-machine:x64", "-def:"+stem+".def", "-out:"+stem+".lib"], env, folder)
    smoke = lf(ROOT/"tools/c1/gmp_smoke.c")
    if hashes(smoke)["sha3_256"] != pin["smoke_source_sha3_256"]:
        raise Refusal("Pinned smoke source mismatch")
    (folder/"gmp_smoke.c").write_bytes(smoke)
    invoke([str(bindir/"cl.exe"), *FLAGS, "-I.", "gmp_smoke.c", "gmp.lib", "-Fe:gmp_smoke.exe",
            "-Fo:gmp_smoke.obj", "-link", "-Brepro"], env, folder)
    if hashes((folder/"gmp_smoke.exe").read_bytes())["sha3_256"] != pin["smoke_executable_sha3_256"]:
        raise Refusal("Rebuilt capability probe differs from frozen pin")
    smoke_result = json.loads(invoke([str(folder/"gmp_smoke.exe")], cwd=folder, timeout=5))
    product = 123456789012345678901234567890 * 98765432109876543210987654321
    if (not smoke_result.get("ok") or smoke_result.get("product_decimal") != str(product)
            or smoke_result.get("runtime_version") != "6.3.0" or not smoke_result.get("roundtrip_equal")
            or not smoke_result.get("dll_beside_executable")):
        raise Refusal("Independent tiny GMP arithmetic probe disagreement")
    for path in NATIVE:
        (folder/Path(path).name).write_bytes(lf(ROOT/path))
    for name, flags in (("ceml_frontier.exe", FLAGS), ("ceml_frontier_checked.exe", CHECKED_FLAGS)):
        args = command(name, flags)
        args[0] = str(bindir/"cl.exe")
        invoke(args, env, folder)
        if "libgmp-10.dll" not in pe_info((folder/name).read_bytes())["imports"]:
            raise Refusal("Worker imports incorrect GMP dependency")
        if invoke([str(folder/name), "--table"], cwd=folder, timeout=5) != table_bytes()+b"COMPLETE TABLE TEST ONLY\n":
            raise Refusal("Native independently rebuilt table disagreement")
    return smoke_result


def artifact_hashes(folder):
    names = ("ceml_frontier.exe", "ceml_frontier_checked.exe", "libgmp-10.dll", "gmp.h",
             "gmp_public.lib", "gmp_public.def", "gmp_smoke.exe", "gmp.lib", "gmp.def")
    return {n: hashes((folder/n).read_bytes()) for n in names}


def build():
    pin, extracted, env, bindir, metadata = dependency_check()
    before = inputs()
    probe = compile_at(BUILD, env, bindir, extracted, pin)
    after = inputs()
    if before != after:
        raise Refusal("Build source inputs changed during compilation")
    table = table_bytes()
    result = {"schema": MANIFEST_SCHEMA, "offline": "yes",
              "python_version": pin["python_version"], "toolchain": metadata,
              "compiler_flags": FLAGS, "checked_compiler_flags": CHECKED_FLAGS,
              "linker_flags": ["-Brepro"], "inputs": after, "artifacts": artifact_hashes(BUILD),
              "table_text": table.decode("ascii"), "table_digest": domain_hash("TABLE", table),
              "test_suite_revision": suite_digest(after), "capability_probe": probe,
              "provisioning": "retained archives plus separately hash-verified extracted header/DLL; no extraction",
              "sdk_limitation": "SDK closure identified by version, not content-hashed"}
    result["digest"] = domain_hash("BUILD", canonical(result))
    (BUILD/MANIFEST_NAME).write_bytes(canonical(result))
    return verify_build()


def verify_build(clean=False):
    """Fail closed on current inputs, tools, table, artifacts or manifest drift.

    With clean=True, rebuild in a separate ignored same-volume directory and
    require all reproducible artifact bytes equal without replacing the build.
    Returns the canonical manifest plus resolved executable convenience paths.
    """
    pin, extracted, env, bindir, metadata = dependency_check()
    path = BUILD/MANIFEST_NAME
    if not path.is_file() or path.stat().st_size > 128*1024:
        raise Refusal("Native build manifest missing or oversized")
    raw = path.read_bytes()
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise Refusal("Duplicate build manifest key")
            result[key] = value
        return result
    manifest = json.loads(raw, object_pairs_hook=unique)
    expected = {"schema", "offline", "python_version", "toolchain", "compiler_flags", "checked_compiler_flags",
                "linker_flags", "inputs", "artifacts", "table_text", "table_digest", "test_suite_revision",
                "capability_probe", "provisioning", "sdk_limitation", "digest"}
    if not isinstance(manifest, dict) or set(manifest) != expected:
        raise Refusal("Native build manifest shape mismatch")
    if canonical(manifest) != raw or manifest.get("schema") != MANIFEST_SCHEMA:
        raise Refusal("Noncanonical native build manifest")
    unsigned = dict(manifest)
    digest = unsigned.pop("digest", None)
    if digest != domain_hash("BUILD", canonical(unsigned)):
        raise Refusal("Native build manifest digest mismatch")
    current = inputs()
    if manifest["inputs"] != current or manifest["test_suite_revision"] != suite_digest(current):
        raise Refusal("Native build/source/test identity mismatch; rebuild required")
    if (manifest["toolchain"] != metadata or manifest["compiler_flags"] != FLAGS
            or manifest["checked_compiler_flags"] != CHECKED_FLAGS
            or manifest["table_text"].encode("ascii") != table_bytes()
            or manifest["table_digest"] != domain_hash("TABLE", table_bytes())
            or manifest["artifacts"] != artifact_hashes(BUILD)):
        raise Refusal("Native build/table/artifact identity mismatch")
    if clean:
        import tempfile
        with tempfile.TemporaryDirectory(prefix="clean-", dir=BUILD.parent) as directory:
            folder = Path(directory)
            compile_at(folder, env, bindir, extracted, pin)
            if artifact_hashes(folder) != manifest["artifacts"]:
                raise Refusal("Clean offline reproducibility disagreement")
    result = dict(manifest)
    result["executable"] = str(BUILD/"ceml_frontier.exe")
    result["checked_executable"] = str(BUILD/"ceml_frontier_checked.exe")
    return result


def build_digest():
    return verify_build()["digest"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--show-command", action="store_true")
    group.add_argument("--verify", action="store_true", help="independent clean rebuild and exact equality")
    args = parser.parse_args()
    if args.show_command:
        print(json.dumps({"cwd": "local/frontier/build", "release": command(),
                          "checked": command("ceml_frontier_checked.exe", CHECKED_FLAGS)}, sort_keys=True))
        return
    manifest = verify_build(clean=True) if args.verify else build()
    print(json.dumps({"status": "PASS", "offline": "yes", "digest": manifest["digest"],
                      "executable_sha3_256": manifest["artifacts"]["ceml_frontier.exe"]["sha3_256"],
                      "table_digest": manifest["table_digest"]}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(json.dumps({"status": "REFUSED", "reason": str(error) if isinstance(error, Refusal)
                          else "Offline build refused; raw diagnostic suppressed"}, sort_keys=True))
        sys.exit(2)
