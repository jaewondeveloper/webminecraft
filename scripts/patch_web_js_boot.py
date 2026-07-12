#!/usr/bin/env python3
"""Patch web-js/index.html from upstream: Jaewon boot, key splash, branding."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB_JS = ROOT / "web-js"
UPSTREAM = WEB_JS / "index.html.upstream"
OUT = WEB_JS / "index.html"

OLD_OPTS = """        window.eaglercraftXOpts = {
            container: "game_frame",
            worldsDB: "worlds"
        };"""

NEW_OPTS = """        window.eaglercraftXOpts = {
            container: "game_frame",
            worldsDB: "worlds",
            showBootMenuOnLaunch: false,
            allowBootMenu: false,
            bootMenuBlocksUnsignedClients: false,
            checkRelaysForUpdates: true,
            allowServerRedirects: true,
            relays: [
                { addr: "wss://relay.deev.is/", comment: "relay #1", primary: relayId === 0 },
                { addr: "wss://relay.lax1dude.net/", comment: "relay #2", primary: relayId === 1 },
                { addr: "wss://relay.shhnowisnottheti.me/", comment: "relay #3", primary: relayId === 2 }
            ]
        };

        (function() {
            var q = window.location.search;
            if ((typeof q === "string") && q[0] === "?" && (typeof URLSearchParams !== "undefined")) {
                var s = new URLSearchParams(q).get("server");
                if (s) window.eaglercraftXOpts.joinServer = s;
            }
        })();"""

OLD_LAUNCH = """            var launchInterval = -1;
            var launchCounter = 1;
            var launchCountdownNumberElement = null;
            var launchCountdownProgressElement = null;
            var launchSkipCountdown = false;

            var launchTick = function() {
                launchCountdownNumberElement.innerText = "" + Math.floor(6.0 - launchCounter * 0.06);
                launchCountdownProgressElement.style.width = "" + launchCounter + "%";
                if(++launchCounter > 100 || launchSkipCountdown) {
                    clearInterval(launchInterval);
                    setTimeout(function() {
                        document.body.removeChild(document.getElementById("launch_countdown_screen"));
                        document.body.style.backgroundColor = "black";
                        main();
                    }, 50);
                }
            };

            window.addEventListener("load", function() {
                launchCountdownNumberElement = document.getElementById("launchCountdownNumber");
                launchCountdownProgressElement = document.getElementById("launchCountdownProgress");
                launchInterval = setInterval(launchTick, 50);
                document.getElementById("skipCountdown").addEventListener("click", function() {
                    launchSkipCountdown = true;
                });
                document.getElementById("skipCountdown").focus();
                /*
                document.getElementById("bootMenu").addEventListener("click", function() {
                    launchSkipCountdown = true;
                    window.eaglercraftXOpts.showBootMenuOnLaunch = true;
                });
                */
            });"""

NEW_LAUNCH = """            function __eaglerLaunchGame() {
                window.removeEventListener("keydown", __eaglerLaunchGame);
                window.removeEventListener("mousedown", __eaglerLaunchGame);
                window.removeEventListener("touchstart", __eaglerLaunchGame);
                var boot = document.getElementById("launch_countdown_screen");
                if (boot && boot.parentNode) boot.parentNode.removeChild(boot);
                document.body.style.backgroundColor = "black";
                if (typeof window.__eaglerShowLoadingSplashAfterMain === "function") {
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
                }
            }

            window.addEventListener("load", function() {
                window.addEventListener("keydown", __eaglerLaunchGame);
                window.addEventListener("mousedown", __eaglerLaunchGame);
                window.addEventListener("touchstart", __eaglerLaunchGame);
            });"""

OLD_BODY = """<body style="margin:0px;width:100%;height:100%;overflow:hidden;background-color:#121212;" id="game_frame">
    <div style="margin:0px;width:100%;height:100%;font-family:sans-serif;display:flex;align-items:center;user-select:none;" id="launch_countdown_screen">
        <div style="margin:auto;text-align:center;color:#FFFFFF;">
            <h1>This file is from <span style="color:#FF5555;">03/30/2025</span></h1>
            <h2>Game will launch in <span id="launchCountdownNumber">5</span>...</h2>
            <div style="border:2px solid #FFFFFF;width:100%;height:15px;padding:1px;margin-bottom:20vh;">
                <div id="launchCountdownProgress" style="background-color:#555555;width:0%;height:100%;"></div>
            </div>
            <button id="skipCountdown" autofocus style="padding:10px 20px;font-size:1rem;color:#FFFFFF;background-color:#333333;border:none;cursor:pointer;border-radius:5px;">Skip</button>
        </div>
    </div>
</body>"""

NEW_BODY = """<body style="margin:0px;width:100%;height:100%;overflow:hidden;background-color:black;" id="game_frame">
    <div style="margin:0px;width:100%;height:100%;image-rendering:pixelated;background:center / contain no-repeat url(splash.png?v=19), 0px 0px / 1000000% 1000000% no-repeat url(splash.png?v=19) black;user-select:none;" id="launch_countdown_screen">
    </div>
</body>"""

BRANDING: list[tuple[bytes, bytes]] = [
    (b"PeytonPlayz585", b"Jaewon        "),
    (b"Eaglercraft 1.12.2", b"Minecraft By Jaewo"),
    (b"Eaglercraft 1.12", b"Minecraft 1.12  "),
    (b"Launch EaglercraftX", b"Launch Game Now    "),
    (b"Yes, Eaglercraft 1.12.2", b"Yes, Minecraft By Jaewo"),
]


def copy_assets() -> None:
    web = ROOT / "web"
    for name in ("favicon.png", "splash.png", "splash2.png", "jaewon-boot.js"):
        src = web / name
        if not src.is_file():
            src = ROOT / "eaglymc" / name
        if src.is_file():
            shutil.copy2(src, WEB_JS / name)


def main() -> int:
    if not UPSTREAM.is_file():
        print("missing upstream", UPSTREAM)
        return 1

    copy_assets()
    text = UPSTREAM.read_text(encoding="utf-8")
    before = len(text)

    text = text.replace("<title>Eaglercraft 1.12.2</title>", "<title>Minecraft By Jaewon</title>", 1)
    text = text.replace(
        '<meta name="description" content="Eaglercraft 1.12.2 Offline Download">',
        '<meta name="description" content="Minecraft By Jaewon">',
        1,
    )
    if "jaewon-boot.js" not in text:
        text = text.replace(
            "<title>Minecraft By Jaewon</title>",
            '<title>Minecraft By Jaewon</title>\n'
            '    <link type="image/png" rel="shortcut icon" href="favicon.png?v=19" />\n'
            '    <script type="text/javascript">window.__eaglerOverlayMode="timer";'
            'window.__eaglerOverlayMinMs=20000;window.__eaglerShowLoadingStatus=true;'
            'window.__eaglerClassesJSURL="classes.js?v=19";</script>\n'
            '    <script type="text/javascript" src="jaewon-boot.js?v=19"></script>',
            1,
        )

    if OLD_OPTS not in text:
        print("opts block missing")
        return 1
    if OLD_LAUNCH not in text:
        print("launch block missing")
        return 1
    if OLD_BODY not in text:
        print("body block missing")
        return 1

    text = text.replace(OLD_OPTS, NEW_OPTS, 1)
    text = text.replace(OLD_LAUNCH, NEW_LAUNCH, 1)
    text = text.replace(OLD_BODY, NEW_BODY, 1)

    if "</html>" not in text or "<body" not in text:
        print("refusing to write: broken html")
        return 1

    data = bytearray(text.encode("utf-8"))
    for old, new in BRANDING:
        if len(old) != len(new):
            raise ValueError(f"length mismatch {old!r} vs {new!r}")
        count = data.count(old)
        if count:
            data = data.replace(old, new)
            print(f"branding {old!r}: {count}")

    tmp = OUT.with_suffix(".html.tmp")
    tmp.write_bytes(data)
    os.replace(tmp, OUT)
    print("patched", OUT, "size", before, "->", len(data))

    # Split monolithic into shell + classes.js + assets.epk
    import subprocess
    split = ROOT / "scripts" / "split_web_js_layout.py"
    if split.is_file():
        r = subprocess.run([sys.executable, str(split)], cwd=ROOT)
        if r.returncode != 0:
            print("warning: split_web_js_layout failed", r.returncode)
    return 0


if __name__ == "__main__":
    sys.exit(main())
