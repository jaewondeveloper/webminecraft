#!/usr/bin/env python3
"""Fix web/index.html favicon duplicate and set safe overlay mode."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "web" / "index.html"


def main() -> int:
    text = WEB.read_text(encoding="utf-8")
    # Remove embedded base64 favicon that overrides favicon.png
    text2, n = re.subn(
        r'<link type="image/png" rel="shortcut icon" href="data:image/png;base64,[^"]+" />\s*',
        "",
        text,
        count=1,
    )
    if n:
        print("removed base64 favicon link")
    else:
        print("base64 favicon link not found (may already be removed)")
        text2 = text

    text2 = text2.replace("favicon.png?v=14", "favicon.png?v=15")
    text2 = text2.replace("jaewon-boot.js?v=14", "jaewon-boot.js?v=15")
    text2 = text2.replace("splash.png?v=14", "splash.png?v=15")

    marker = '<script type="text/javascript" src="jaewon-boot.js?v=15"></script>'
    inject = (
        '<script type="text/javascript">window.__eaglerOverlayMode="timer";'
        "window.__eaglerOverlayMinMs=14000;</script>\n"
    )
    if inject.strip() not in text2 and marker in text2:
        text2 = text2.replace(marker, inject + marker, 1)
        print("injected overlay timer mode")

    if "<body" not in text2 or "</html>" not in text2:
        print("refusing to write: broken html")
        return 1

    tmp = WEB.with_suffix(".html.tmp")
    tmp.write_text(text2, encoding="utf-8")
    os.replace(tmp, WEB)
    print("patched", WEB)
    return 0


if __name__ == "__main__":
    sys.exit(main())
