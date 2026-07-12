#!/usr/bin/env python3
"""Remove visible EaglyMC / Eaglercraft credits (equal-length only)."""

from __future__ import annotations

import os
import shutil
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAIRS: list[tuple[bytes, bytes]] = [
    (b"Made by the EaglyMC team", b"                        "),
    (b"the EaglyMC team", b"                "),
    (b"Based Off EaglercraftX", b"                      "),
    (b"By lax1dude (u44)", b"                 "),
    (b"           EaglyMC", b"                  "),
    (b"           EaglyMC ", b"                   "),
    (b"eaglymc/realms/textures/title.png", b"textures/gui/title/minecraft.png "),
]

WASM_ONLY: list[tuple[bytes, bytes]] = [
    (b"Chocofush's Cool Experimental Features:", b"                                       "),
    (b"Chocofush's cool/misc extra stuff", b"                                 "),
]

JS_ONLY: list[tuple[bytes, bytes]] = [
    (b"Chocofush\\'s Cool Experimental Features:", b"                                        "),
    (b"Chocofush\\'s cool/misc extra stuff", b"                                  "),
]


def _validate(pairs: list[tuple[bytes, bytes]], label: str) -> None:
    for old, new in pairs:
        if len(old) != len(new):
            raise ValueError(f"{label}: {old!r} ({len(old)}) != {new!r} ({len(new)})")


def patch_bytes(path: str, pairs: list[tuple[bytes, bytes]]) -> int:
    data = bytearray(open(path, "rb").read())
    total = 0
    changed = False
    for old, new in pairs:
        start = 0
        while True:
            i = data.find(old, start)
            if i == -1:
                break
            data[i : i + len(old)] = new
            total += 1
            changed = True
            start = i + len(new)
    if changed:
        bak = path + ".bak2"
        if not os.path.exists(bak):
            shutil.copy2(path, bak)
        tmp = path + ".tmp"
        with open(tmp, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
    return total


def main() -> int:
    _validate(PAIRS, "PAIRS")
    _validate(WASM_ONLY, "WASM_ONLY")
    _validate(JS_ONLY, "JS_ONLY")

    js = os.path.join(BASE, "eaglymc", "classes.js")
    wasm = os.path.join(BASE, "eaglymc-wasm", "classes.wasm")
    upstream = wasm + ".upstream"

    if os.path.isfile(upstream):
        shutil.copy2(upstream, wasm)
        print("restored classes.wasm from upstream")

    if os.path.isfile(wasm):
        print(f"classes.wasm: {patch_bytes(wasm, PAIRS + WASM_ONLY)} replacements")
    print("note: patch eaglymc/classes.js with scripts/patch_eaglymc_js.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())
