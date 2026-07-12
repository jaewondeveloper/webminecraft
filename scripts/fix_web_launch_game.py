#!/usr/bin/env python3
"""Fix corrupted __eaglerLaunchGame in web/index.html."""

from __future__ import annotations

import re
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "web" / "index.html"

FIXED = r"""	function __eaglerLaunchGame() {
		window.removeEventListener("keydown", __eaglerLaunchGame, true);
		window.removeEventListener("mousedown", __eaglerLaunchGame, true);
		window.removeEventListener("touchstart", __eaglerLaunchGame, true);
		var boot = document.getElementById("launch_countdown_screen");
		if (boot && boot.parentNode) boot.parentNode.removeChild(boot);
		document.body.style.backgroundColor = "black";
		if (typeof main !== "function") {
			alert("게임 로딩 실패: main() 없음");
			return;
		}
		if (typeof window.__eaglerShowLoadingSplashAfterMain === "function") {
			window.__eaglerShowLoadingSplashAfterMain();
		} else if (typeof window.__eaglerShowLoadingSplash === "function") {
			var frame = document.getElementById("game_frame");
			if (frame) window.__eaglerShowLoadingSplash(frame);
		}
		if (typeof window.__eaglerInstallNetworkStatusHooks === "function") {
			window.__eaglerInstallNetworkStatusHooks();
		}
		main();
		if (typeof window.__eaglerStartLoadingOverlayWatch === "function") {
			window.__eaglerStartLoadingOverlayWatch();
		}
	}

	window.addEventListener("load", function() {
		window.addEventListener("keydown", __eaglerLaunchGame, true);
		window.addEventListener("mousedown", __eaglerLaunchGame, true);
		window.addEventListener("touchstart", __eaglerLaunchGame, true);
	});"""


def main() -> int:
    text = WEB.read_text(encoding="utf-8")
    pattern = re.compile(
        r"\tfunction __eaglerLaunchGame\(\) \{.*?\twindow\.addEventListener\(\"load\", function\(\) \{"
        r".*?\t\twindow\.addEventListener\(\"touchstart\", __eaglerLaunchGame\);\n\t\}\);",
        re.S,
    )
    if not pattern.search(text):
        print("launch block not found")
        return 1
    text = pattern.sub(FIXED, text, count=1)
    WEB.write_text(text, encoding="utf-8")
    print("fixed", WEB)
    return 0


if __name__ == "__main__":
    sys.exit(main())
