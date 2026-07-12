#!/usr/bin/env python3
"""Safe display-only branding patches (never touch metadata keys / certs)."""

from __future__ import annotations

import os
import shutil
import struct
import sys
import zlib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# UI / splash text only — do NOT patch client cert blobs or JSON property keys.
COMMON: list[tuple[bytes, bytes]] = [
    (b"the EaglyMC team", b"Jaewon          "),
    (b"           EaglyMC", b"Minecraft         "),
    (b"           EaglyMC ", b"Minecraft          "),
    (b"           EaglyMC 1.20 u5", b"Minecraft 1.8.8           "),
    (b"           EaglyMC 1.20 u5 (site origin)", b"Minecraft 1.8.8 (local)                 "),
    (b"Made by the EaglyMC team", b"Made by Jaewon          "),
    (b"Minecraft 1.20.1 (kinda)", b"Minecraft 1.8.8         "),
    (b"eaglymc/realms/textures/title.png", b"textures/gui/title/minecraft.png "),
    (b"https://discord.gg/S96sKenDhV", b"                             "),
    (b"https://gitlab.com/lax1dude/eaglercraftx-1.8", b"                                            "),
    (b"You have been given a cool Chocofush!", b"You received an item!                "),
    (b"Based Off EaglercraftX", b"                      "),
    (b"By lax1dude (u44)", b"                 "),
    (b"Discord", b"       "),
    (b"Connecting to services...", b"                         "),
]

JS_ONLY: list[tuple[bytes, bytes]] = [
    (b"Chocofush\\'s Cool Experimental Features:", b"Experimental features (off):            "),
    (b"Chocofush\\'s cool/misc extra stuff", b"Extra features (off)              "),
]

WASM_ONLY: list[tuple[bytes, bytes]] = [
    (b"Chocofush's Cool Experimental Features:", b"Experimental features (off):           "),
    (b"Chocofush's cool/misc extra stuff", b"Extra features (off)             "),
]

RUNTIME_ONLY: list[tuple[bytes, bytes]] = [
    (b"Launch EaglercraftX", b"Launch Game Now    "),
    (b"EaglercraftX WASM-GC requires", b"This browser game needs      "),
    (b"incompatible with Eaglercraft", b"incompatible with this game  "),
    (b"using Eaglercraft on a different", b"using this game on a different  "),
    (b"EaglercraftX may malfunction", b"This game may malfunction   "),
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
        bak = path + ".bak"
        if not os.path.exists(bak):
            shutil.copy2(path, bak)
        with open(path, "wb") as f:
            f.write(data)
    return total


def main() -> int:
    _validate(COMMON, "COMMON")
    _validate(JS_ONLY, "JS_ONLY")
    _validate(WASM_ONLY, "WASM_ONLY")
    _validate(RUNTIME_ONLY, "RUNTIME_ONLY")

    js = os.path.join(BASE, "eaglymc", "classes.js")
    wasm = os.path.join(BASE, "eaglymc-wasm", "classes.wasm")
    runtime = os.path.join(BASE, "eaglymc-wasm", "eagruntime.js")

    if os.path.isfile(js):
        print(f"classes.js: {patch_bytes(js, COMMON + JS_ONLY)} replacements")
    if os.path.isfile(wasm):
        print(f"classes.wasm: {patch_bytes(wasm, COMMON + WASM_ONLY)} replacements")
    if os.path.isfile(runtime):
        print(f"eagruntime.js: {patch_bytes(runtime, RUNTIME_ONLY)} replacements")

    return 0


if __name__ == "__main__":
    sys.exit(main())
