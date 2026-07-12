#!/usr/bin/env python3
"""Ensure loading overlay shows before main() in web/index.html."""

from __future__ import annotations

import re
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "web" / "index.html"

OLD = """\t\tmain();
\t\tif (typeof window.__eaglerShowLoadingSplashAfterMain === "function") {
\t\t\twindow.__eaglerShowLoadingSplashAfterMain();"""

NEW = """\t\tif (typeof window.__eaglerShowLoadingSplashAfterMain === "function") {
\t\t\twindow.__eaglerShowLoadingSplashAfterMain();
\t\t}
\t\tif (typeof window.__eaglerInstallNetworkStatusHooks === "function") {
\t\t\twindow.__eaglerInstallNetworkStatusHooks();
\t\t}
\t\tmain();
\t\tif (typeof window.__eaglerShowLoadingSplashAfterMain === "function") {
\t\t\twindow.__eaglerShowLoadingSplashAfterMain();"""

# Remove duplicate second ShowLoadingSplashAfterMain call
NEW_CLEAN = """\t\tif (typeof window.__eaglerShowLoadingSplashAfterMain === "function") {
\t\t\twindow.__eaglerShowLoadingSplashAfterMain();
\t\t}
\t\tif (typeof window.__eaglerInstallNetworkStatusHooks === "function") {
\t\t\twindow.__eaglerInstallNetworkStatusHooks();
\t\t}
\t\tmain();"""


def main() -> int:
    text = WEB.read_text(encoding="utf-8")
    if OLD in text:
        text = text.replace(OLD, NEW_CLEAN, 1)
    elif "window.__eaglerInstallNetworkStatusHooks" in text and "__eaglerLaunchGame" in text:
        print("already patched")
        return 0
    else:
        text2 = re.sub(
            r"(\t\tif \(typeof main !== \"function\"\)[^\}]+\}\n)(\t\tmain\(\);)",
            r"\1\t\tif (typeof window.__eaglerShowLoadingSplashAfterMain === \"function\") {\n"
            r"\t\t\twindow.__eaglerShowLoadingSplashAfterMain();\n"
            r"\t\t}\n"
            r"\t\tif (typeof window.__eaglerInstallNetworkStatusHooks === \"function\") {\n"
            r"\t\t\twindow.__eaglerInstallNetworkStatusHooks();\n"
            r"\t\t}\n"
            r"\2",
            text,
            count=1,
        )
        if text2 == text:
            print("pattern not found")
            return 1
        text = text2
    WEB.write_text(text, encoding="utf-8")
    print("patched", WEB)
    return 0


if __name__ == "__main__":
    sys.exit(main())
