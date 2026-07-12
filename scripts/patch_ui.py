#!/usr/bin/env python3
"""UI/boot branding patches for EaglyMC WASM."""

from __future__ import annotations

import os
import shutil
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WASM_DIR = os.path.join(BASE, "eaglymc-wasm")
WASM = os.path.join(WASM_DIR, "classes.wasm")
UPSTREAM = WASM + ".upstream"

INTENT = {
    "Minecraft 1.20.1 (kinda)": "1.20.1 Jaewon 웹버전 ",
    "           EaglyMC": "Minecraft",
    "           EaglyMC ": "Minecraft",
    "EaglyMC 1.20-u5 - ": "Jaewon Web 1.8.8- ",
    "Made by the EaglyMC team": "Made by Jaewon",
    "the EaglyMC team": "Jaewon",
    "eaglymc/realms/textures/title.png": "textures/gui/title/minecraft.png",
    "Based Off EaglercraftX": "",
    "By lax1dude (u44)": "",
    "https://discord.gg/S96sKenDhV": "",
    "https://gitlab.com/lax1dude/eaglercraftx-1.8": "",
    "Chocofush's Cool Experimental Features:": "Experimental features (off):",
    "Chocofush's cool/misc extra stuff": "Extra features (off)",
    "Discord": "",
    "Connecting to services...": "",
    "eaglercraftx wasm gc is starting": "game client wasm gc is starting",
}


def fit_bytes(old: bytes, text: str) -> bytes:
    nb = text.encode("utf-8")
    while len(nb) > len(old):
        nb = nb[:-1]
    return nb + b" " * (len(old) - len(nb))


def build_pairs(data: bytes) -> list[tuple[bytes, bytes]]:
    pairs = []
    for old, intent in INTENT.items():
        ob = old.encode("utf-8")
        if ob not in data:
            continue
        nb = fit_bytes(ob, intent)
        if len(ob) != len(nb):
            raise ValueError(f"{old!r}: {len(ob)} vs {len(nb)}")
        pairs.append((ob, nb))
    return pairs


def patch_file(path: str, pairs: list[tuple[bytes, bytes]]) -> int:
    data = bytearray(open(path, "rb").read())
    total = 0
    for old, new in pairs:
        c = data.count(old)
        if c:
            data = data.replace(old, new)
            total += c
            print(f"  {c}x {old.decode('utf-8', 'replace')}")
    with open(path, "wb") as f:
        f.write(data)
    return total


def main() -> int:
    if not os.path.isfile(UPSTREAM):
        print("missing upstream wasm:", UPSTREAM)
        return 1

    shutil.copy2(UPSTREAM, WASM)
    data = open(UPSTREAM, "rb").read()
    pairs = build_pairs(data)
    print(f"patching {len(pairs)} string rules into classes.wasm")
    n = patch_file(WASM, pairs)
    print("replacements:", n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
