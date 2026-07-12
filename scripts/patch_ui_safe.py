#!/usr/bin/env python3
"""Minimal safe UI patches — never patch cert/internal strings."""

from __future__ import annotations

import os
import shutil
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WASM = os.path.join(BASE, "eaglymc-wasm", "classes.wasm")
UPSTREAM = WASM + ".upstream"

INTENT: list[tuple[str, str]] = [
    ("Minecraft 1.20.1 (kinda)", "1.20.1 Jaewon 웹버전 "),
    ("eaglymc/realms/textures/title.png", "textures/gui/title/minecraft.png"),
    ("           EaglyMC", "Minecraft"),
    ("           EaglyMC ", "Minecraft"),
    ("Made by the EaglyMC team", "Made by Jaewon"),
    ("the EaglyMC team", "Jaewon"),
    ("https://discord.gg/S96sKenDhV", ""),
    ("Discord", ""),
    ("Connecting to services...", ""),
    ("Chocofush's Cool Experimental Features:", "Experimental features (off):"),
    ("Chocofush's cool/misc extra stuff", "Extra features (off)"),
]


def fit_bytes(old: bytes, text: str) -> bytes:
    nb = text.encode("utf-8")
    while len(nb) > len(old):
        nb = nb[:-1]
    return nb + b" " * (len(old) - len(nb))


def build_pairs(data: bytes) -> list[tuple[bytes, bytes]]:
    pairs = []
    for old_s, new_s in INTENT:
        ob = old_s.encode("utf-8")
        if ob not in data:
            continue
        nb = fit_bytes(ob, new_s)
        if len(ob) != len(nb):
            raise ValueError(f"length mismatch for {old_s!r}")
        pairs.append((ob, nb))
    return pairs


def main() -> int:
    if not os.path.isfile(UPSTREAM):
        print("missing", UPSTREAM)
        return 1

    shutil.copy2(UPSTREAM, WASM)
    data = open(UPSTREAM, "rb").read()
    pairs = build_pairs(data)
    buf = bytearray(data)
    total = 0
    for old, new in pairs:
        c = buf.count(old)
        if c:
            for i in range(len(buf) - len(old) + 1):
                if buf[i : i + len(old)] == old:
                    buf[i : i + len(old)] = new
            total += c
            print(f"{c}x {old.decode('utf-8', 'replace')}")
    open(WASM, "wb").write(buf)
    print("rules", len(pairs), "replacements", total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
