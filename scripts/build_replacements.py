#!/usr/bin/env python3
"""Build equal-length branding replacements from actual file content."""

import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS = os.path.join(BASE, "eaglymc", "classes.js")

# Human-readable new text -> will be padded/truncated to match each old string
INTENT = {
    "the EaglyMC team": "Minecraft",
    "           EaglyMC": "Minecraft",
    "           EaglyMC ": "Minecraft",
    "EaglyMC 1.20-u5 eventual [": "Minecraft 1.8.8 eventual [",
    "           EaglyMC 1.20 u5": "Minecraft 1.8.8",
    "           EaglyMC 1.20 u5 (site origin)": "Minecraft 1.8.8 (local)",
    "EaglyMC 1.20-u5 - ": "Minecraft 1.8.8 - ",
    "Made by the EaglyMC team": "Happy mining!",
    "Minecraft 1.20.1 (kinda)": "Minecraft 1.8.8",
    "eaglymc/realms/textures/title.png": "textures/gui/title/minecraft.png",
    "https://discord.gg/S96sKenDhV": "",
    "https://gitlab.com/lax1dude/eaglercraftx-1.8": "",
    "Chocofush's Cool Experimental Features:": "Experimental features (off):",
    "Chocofush's cool/misc extra stuff": "Extra features (off)",
    "You have been given a cool Chocofush!": "You received an item!",
    "Based Off EaglercraftX": "",
    "By lax1dude (u44)": "",
    "client_origin_name": "client_display_nm",
    "Discord": "",
    "Connecting to services...": "",
}

EXTRA = [
    ("Chocofush\\'s Cool Experimental Features:", "Experimental features (disabled):      "),
    ("Chocofush\\'s cool/misc extra stuff", "Extra features (disabled)          "),
    ('"client_origin_name","EaglyMC"', '"client_origin_name","Minecraft"'),
    ('"game_version","1.20"', '"game_version","1.8 "'),
]


def fit(old: str, new: str) -> str:
    if len(new) > len(old):
        new = new[: len(old)]
    return new + " " * (len(old) - len(new))


def main() -> None:
    data = open(JS, "r", encoding="utf-8", errors="replace").read()
    found = set(re.findall(r"EaglyMC[^\"]{0,50}|eaglymc/[a-z_/]+|Chocofush[^\"]{0,50}|discord\.gg[^\"]+|Made by the EaglyMC team|Minecraft 1\.20\.1 \(kinda\)|Based Off EaglercraftX|By lax1dude \(u44\)|Connecting to services\.\.\.|https://gitlab\.com/lax1dude/eaglercraftx-1\.8", data))
    # Also explicit keys
    keys = list(INTENT.keys())
    pairs = []
    for old in keys:
        if old not in data:
            print(f"# skip (not found): {old!r}")
            continue
        new = fit(old, INTENT.get(old, ""))
        assert len(old) == len(new), (old, len(old), new, len(new))
        pairs.append((old, new))
        print(f"    ({old!r}, {new!r}),")

    for old, new in EXTRA:
        assert len(old) == len(new), (old, len(old), new, len(new))
        pairs.append((old, new))
        print(f"    ({old!r}, {new!r}),")

    print("\n# count in js:")
    for old, new in pairs:
        print(old, data.count(old))


if __name__ == "__main__":
    main()
