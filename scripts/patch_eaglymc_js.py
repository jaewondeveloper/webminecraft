#!/usr/bin/env python3
"""Safely patch eaglymc/classes.js without truncating or corrupting the file."""

from __future__ import annotations

import os
import shutil
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS = os.path.join(BASE, "eaglymc", "classes.js")
BAK = JS + ".bak2"

A_F_OLD = (
    b"function A_f(a,b){var c,d;HjL=null;c=HjK;if(c!==null){d=Hi4;if(d!==null)d.removeChild(c);}"
    b"HjK=null;En(a.dh_,BC(b));}"
)
A_F_NEW = (
    b"function A_f(a,b){var c,d;HjL=null;c=HjK;if(c!==null){d=Hi4;if(d!==null)d.removeChild(c);}"
    b"HjK=null;if(typeof $rt_globals.__eaglerShowLoadingSplash===\"function\"&&Hi4!==null)"
    b"$rt_globals.__eaglerShowLoadingSplash(Hi4);En(a.dh_,BC(b));}"
)

# Equal-length replacements only — never change byte length.
BRANDING: list[tuple[bytes, bytes]] = [
    (b"Made by the EaglyMC team", b"                        "),
    (b"the EaglyMC team", b"                "),
    (b"Based Off EaglercraftX", b"                      "),
    (b"By lax1dude (u44)", b"                 "),
    (b"           EaglyMC", b"                  "),
    (b"           EaglyMC ", b"                   "),
    (b"eaglymc/realms/textures/title.png", b"textures/gui/title/minecraft.png "),
]


def main() -> int:
    if not os.path.isfile(BAK):
        print("missing backup", BAK)
        return 1

    shutil.copy2(BAK, JS)
    data = bytearray(open(JS, "rb").read())

    if A_F_OLD not in data:
        print("A_f pattern missing")
        return 1

    data = data.replace(A_F_OLD, A_F_NEW, 1)

    for old, new in BRANDING:
        if len(old) != len(new):
            raise ValueError(f"length mismatch for {old!r}")
        count = data.count(old)
        if count:
            data = data.replace(old, new)
            print(f"branding {old!r}: {count}")

    tmp = JS + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, JS)

    bak_size = os.path.getsize(BAK)
    cur_size = os.path.getsize(JS)
    expected = bak_size + len(A_F_NEW) - len(A_F_OLD)
    if cur_size != expected:
        print(f"ERROR: size {bak_size} -> {cur_size}, expected {expected}")
        return 1

    text = open(JS, encoding="utf-8", errors="ignore").read()
    if "//# sourceMappingURL=../classes.js.map" not in text:
        print("ERROR: truncated or corrupt tail")
        return 1
    if "__eaglerShowLoadingSplash" not in text:
        print("ERROR: A_f hook missing")
        return 1

    print("ok size", cur_size)
    tail = open(JS, encoding="utf-8", errors="ignore").read().strip()[-60:]
    print("tail", tail)
    return 0


if __name__ == "__main__":
    sys.exit(main())
