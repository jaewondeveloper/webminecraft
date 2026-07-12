#!/usr/bin/env python3
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WASM = os.path.join(BASE, "eaglymc-wasm", "classes.wasm.upstream")
d = open(WASM, "rb").read()

INTENT = {
    "Minecraft 1.20.1 (kinda)": "1.20.1 Jaewon 웹버전 ",
    "           EaglyMC": "Minecraft",
    "           EaglyMC ": "Minecraft",
    "           EaglyMC 1.20 u5": "Minecraft 1.8.8",
    "           EaglyMC 1.20 u5 (site origin)": "Jaewon Web Edition",
    "EaglyMC 1.20-u5 - ": "Jaewon Web 1.8.8 - ",
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
    "assets/eagler/eagtek.png": "textures/gui/title/minecraft.png",
}


def fit_bytes(old: bytes, text: str) -> bytes:
    nb = text.encode("utf-8")
    if len(nb) > len(old):
        # trim by bytes without breaking utf-8
        while len(nb) > len(old):
            nb = nb[:-1]
    return nb + b" " * (len(old) - len(nb))


for old, intent in INTENT.items():
    ob = old.encode("utf-8")
    if ob not in d:
        print("# skip", old)
        continue
    nb = fit_bytes(ob, intent)
    assert len(ob) == len(nb), (old, len(ob), len(nb), nb)
    print(f"OK {len(ob)} {old!r} -> {nb!r}")
