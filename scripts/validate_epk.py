#!/usr/bin/env python3
"""Minimal EAGPKG v2.0 validator (read structure, verify file hashes)."""

import hashlib
import struct
import sys
from pathlib import Path


def read_epk(path: str) -> None:
    data = Path(path).read_bytes()
    if not data.startswith(b"EAGPKG$$\x06ver2.0\n"):
        raise SystemExit(f"bad header: {data[:20]!r}")

    off = len(b"EAGPKG$$\x06ver2.0\n")
    file_count = struct.unpack_from(">I", data, off)[0]
    off += 4
    print(f"files: {file_count}")

    entries = []
    for i in range(file_count):
        name_len = struct.unpack_from(">H", data, off)[0]
        off += 2
        name = data[off : off + name_len].decode("utf-8", "replace")
        off += name_len
        comp_size, raw_size = struct.unpack_from(">II", data, off)
        off += 8
        digest = data[off : off + 20]
        off += 20
        payload = data[off : off + comp_size]
        off += comp_size
        entries.append((name, comp_size, raw_size, digest, payload))

    print(f"payload end: {off} / {len(data)}")
    if off != len(data):
        print(f"WARNING: {len(data) - off} trailing bytes")

    bad = 0
    for name, comp_size, raw_size, digest, payload in entries:
        got = hashlib.sha1(payload).digest()
        ok = got == digest
        if not ok:
            bad += 1
            print(f"HASH FAIL: {name}")
        else:
            print(f"OK {name} ({comp_size} -> {raw_size})")
    if bad:
        raise SystemExit(f"{bad} hash failures")
    print("all hashes OK")


if __name__ == "__main__":
    read_epk(sys.argv[1] if len(sys.argv) > 1 else "assets.epk")
