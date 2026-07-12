#!/usr/bin/env python3
"""Split web-js monolithic index into shell + classes.js + assets.epk."""

from __future__ import annotations

import base64
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB_JS = ROOT / "web-js"
INDEX = WEB_JS / "index.html"
CLASSES = WEB_JS / "classes.js"
ASSETS = WEB_JS / "assets.epk"
CACHE = "v=19"

CLIENT_MARK = 'if(typeof window !== "undefined") window.eaglercraftXClientScriptElement = document.currentScript;'
MAP_MARK = "//# sourceMappingURL=../classes.js.map"
ASSETS_MARK = 'window.eaglercraftXOpts.assetsURI = "data:application/octet-stream;base64,'


def extract_assets_b64(text: str) -> bytes:
    start = text.find(ASSETS_MARK)
    if start == -1:
        raise ValueError("embedded assetsURI not found")
    start += len(ASSETS_MARK)
    end = text.find('";', start)
    if end == -1:
        raise ValueError("assetsURI string not terminated")
    b64 = text[start:end]
    return base64.b64decode(b64)


def main() -> int:
    if not INDEX.is_file():
        print("missing", INDEX)
        return 1
    text = INDEX.read_text(encoding="utf-8")
    if CLIENT_MARK not in text or MAP_MARK not in text:
        print("classes.js inline block not found (already split?)")
        return 1

    ci = text.find(CLIENT_MARK)
    mi = text.find(MAP_MARK)
    si = text.rfind("<script", 0, ci)
    script_end = text.find("</script>", mi)
    if script_end == -1:
        raise ValueError("classes.js closing </script> not found")
    classes_body = text[ci:script_end].rstrip() + "\n"

    assets = extract_assets_b64(text)
    ASSETS.write_bytes(assets)
    print("wrote assets.epk", len(assets))

    CLASSES.write_text(classes_body, encoding="utf-8")
    print("wrote classes.js", len(classes_body))

    # Remove inline classes script block
    ei = script_end + len("</script>")
    shell = text[:si] + text[ei:]

    # Remove embedded assetsURI assignment (keep launch IIFE)
    shell = re.sub(
        r'\s*window\.eaglercraftXOpts\.assetsURI = "data:application/octet-stream;base64,[^"]+";\s*',
        "\n",
        shell,
        count=1,
    )

    # Inject external classes URL + assetsURI in opts if missing
    if 'assetsURI: "assets.epk"' not in shell:
        shell = shell.replace(
            'worldsDB: "worlds",',
            'worldsDB: "worlds",\n            assetsURI: "assets.epk",',
            1,
        )

    if "__eaglerClassesJSURL" not in shell:
        shell = shell.replace(
            f'src="jaewon-boot.js?{CACHE}"',
            f'src="jaewon-boot.js?{CACHE}"></script>\n'
            f'    <script type="text/javascript">window.__eaglerClassesJSURL="classes.js?{CACHE}";'
            f'window.__eaglerShowLoadingStatus=true;window.__eaglerOverlayMinMs=20000;',
            1,
        )

    shell = shell.replace("?v=18", f"?{CACHE}")
    shell = shell.replace("?v=17", f"?{CACHE}")

    # Update launch to staged load
    old_launch = """                if (typeof main !== "function") {
                    alert("게임 로딩 실패: main() 없음");
                    return;
                }
                main();
                if (typeof window.__eaglerShowLoadingSplashAfterMain === "function") {
                    window.__eaglerShowLoadingSplashAfterMain();
                } else if (typeof window.__eaglerShowLoadingSplash === "function") {
                    var frame = document.getElementById("game_frame");
                    if (frame) window.__eaglerShowLoadingSplash(frame);
                }
                if (typeof window.__eaglerStartLoadingOverlayWatch === "function") {
                    window.__eaglerStartLoadingOverlayWatch();
                }"""

    new_launch = """                if (typeof window.__eaglerShowLoadingSplashAfterMain === "function") {
                    window.__eaglerShowLoadingSplashAfterMain();
                }
                if (typeof window.__eaglerInstallNetworkStatusHooks === "function") {
                    window.__eaglerInstallNetworkStatusHooks();
                }
                if (typeof window.__eaglerSetLoadingStatus === "function") {
                    window.__eaglerSetLoadingStatus("게임 파일 준비 중...");
                }
                function __eaglerStartMain() {
                    if (typeof main !== "function") {
                        alert("게임 로딩 실패: main() 없음");
                        return;
                    }
                    if (typeof window.__eaglerSetLoadingStatus === "function") {
                        window.__eaglerSetLoadingStatus("게임 엔진 시작 중...");
                    }
                    main();
                    if (typeof window.__eaglerStartLoadingOverlayWatch === "function") {
                        window.__eaglerStartLoadingOverlayWatch();
                    }
                }
                if (typeof main === "function") {
                    __eaglerStartMain();
                } else if (typeof window.__eaglerEnsureClassesLoaded === "function") {
                    window.__eaglerEnsureClassesLoaded(__eaglerStartMain);
                } else {
                    alert("게임 로딩 실패: classes.js 없음");
                }"""

    if old_launch in shell:
        shell = shell.replace(old_launch, new_launch, 1)
    elif "__eaglerEnsureClassesLoaded" not in shell:
        print("warning: launch block pattern not found")

    tmp = INDEX.with_suffix(".html.tmp")
    tmp.write_text(shell, encoding="utf-8")
    os.replace(tmp, INDEX)
    print("wrote shell index.html", len(shell))
    return 0


if __name__ == "__main__":
    sys.exit(main())
