#!/usr/bin/env python3
"""Patch splashes.txt inside EaglyMC assets.epk (recalculate per-object CRC32)."""

import struct
import zlib
from pathlib import Path

EPK = Path(__file__).resolve().parents[1] / "eaglymc-wasm" / "assets.epk"

SPLASH_INTENT = {
    "EaglyMC!\n": "Jaewon! \n",
    "You Eagler!\n": "By Jaewon!\n",
    "Made in Sweden!\n": "Made by Jaewon!\n",
}


def fit(old: bytes, text: str) -> bytes:
    nb = text.encode("utf-8")
    while len(nb) > len(old):
        nb = nb[:-1]
    return nb + b" " * (len(old) - len(nb))


def patch_object(data: bytearray, name: bytes, subs: list[tuple[bytes, bytes]]) -> bool:
    needle = name + b"\x00\x00"
    i = data.find(needle)
    if i < 0:
        print("object not found", name)
        return False
    crc_off = i + len(needle)
    old_crc = struct.unpack_from(">I", data, crc_off)[0]
    body_start = crc_off + 4
    end = data.find(b"\x00\x00END$", body_start)
    if end < 0:
        end = len(data)
    body = bytearray(data[body_start:end])
    changed = False
    for old, new in subs:
        if old in body:
            body = body.replace(old, new)
            changed = True
            print("  sub", old, "->", new)
    if not changed:
        return False
    new_crc = zlib.crc32(body) & 0xFFFFFFFF
    struct.pack_into(">I", data, crc_off, new_crc)
    data[body_start:end] = body
    print(f"patched {name.decode()} crc {old_crc:08x} -> {new_crc:08x}")
    return True


def main() -> None:
    raw = bytearray(EPK.read_bytes())
    subs = []
    for old_s, new_s in SPLASH_INTENT.items():
        ob = old_s.encode()
        nb = fit(ob, new_s)
        if len(ob) != len(nb):
            raise SystemExit(f"bad len {old_s}")
        subs.append((ob, nb))
    bak = EPK.with_suffix(".epk.bak2")
    if not bak.exists():
        bak.write_bytes(raw)
    if patch_object(raw, b"texts/splashes.txt", subs):
        EPK.write_bytes(raw)
        print("saved", EPK)


if __name__ == "__main__":
    main()
