#!/usr/bin/env python3
"""Patch web/index.html so loading overlay shows immediately after main()."""

from __future__ import annotations

import os
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "web" / "index.html"

OLD = """\t\tmain();
\t\tif (typeof window.__eaglerStartLoadingOverlayWatch === "function") {
\t\t\twindow.__eaglerStartLoadingOverlayWatch();
\t\t}"""

NEW = """\t\tmain();
\t\tif (typeof window.__eaglerShowLoadingSplashAfterMain === "function") {
\t\t\twindow.__eaglerShowLoadingSplashAfterMain();
\t\t} else if (typeof window.__eaglerShowLoadingSplash === "function") {
\t\t\tvar frame = document.getElementById("game_frame");
\t\t\tif (frame) window.__eaglerShowLoadingSplash(frame);
\t\t}
\t\tif (typeof window.__eaglerStartLoadingOverlayWatch === "function") {
\t\t\twindow.__eaglerStartLoadingOverlayWatch();
\t\t}"""


def main() -> int:
    text = WEB.read_text(encoding="utf-8")
    if OLD not in text:
        if NEW.split("\n")[1].strip() in text:
            print("already patched")
            return 0
        print("launch overlay block missing")
        return 1
    text = text.replace(OLD, NEW, 1)
    text = text.replace("jaewon-boot.js?v=15", "jaewon-boot.js?v=17")
    text = text.replace("splash.png?v=15", "splash.png?v=17")
    text = text.replace("favicon.png?v=15", "favicon.png?v=17")
    tmp = WEB.with_suffix(".html.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, WEB)
    print("patched", WEB)
    return 0


if __name__ == "__main__":
    sys.exit(main())
