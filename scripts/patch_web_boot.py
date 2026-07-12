#!/usr/bin/env python3
"""Safely patch web/index.html without corrupting the large file."""

from __future__ import annotations

import os
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "web" / "index.html"

OLD_LAUNCH = """var launchInterval = -1;
\tvar launchCounter = 1;
\tvar launchCountdownNumberElement = null;
\tvar launchCountdownProgressElement = null;
\tvar launchSkipCountdown = false;

\tvar launchTick = function() {
\t\tlaunchCountdownNumberElement.innerText = "" + Math.floor(6.0 - launchCounter * 0.06);
\t\tlaunchCountdownProgressElement.style.width = "" + launchCounter + "%";
\t\tif(++launchCounter > 100 || launchSkipCountdown) {
\t\t\tclearInterval(launchInterval);
\t\t\tsetTimeout(function() { document.body.removeChild(document.getElementById("launch_countdown_screen")); document.body.style.backgroundColor = "black"; main(); }, 50);
\t\t}
\t};

\twindow.addEventListener("load", function() {
\t\tlaunchCountdownNumberElement = document.getElementById("launchCountdownNumber");
\t\tlaunchCountdownProgressElement = document.getElementById("launchCountdownProgress");
\t\tlaunchInterval = setInterval(launchTick, 50);
\t\tdocument.getElementById("skipCountdown").addEventListener("click", function() {
\t\t\tlaunchSkipCountdown = true;
\t\t});
\t});"""

NEW_LAUNCH = """\tfunction __eaglerLaunchGame() {
\t\twindow.removeEventListener("keydown", __eaglerLaunchGame);
\t\twindow.removeEventListener("mousedown", __eaglerLaunchGame);
\t\twindow.removeEventListener("touchstart", __eaglerLaunchGame);
\t\tvar boot = document.getElementById("launch_countdown_screen");
\t\tif (boot && boot.parentNode) boot.parentNode.removeChild(boot);
\t\tdocument.body.style.backgroundColor = "black";
\t\tif (typeof main !== "function") {
\t\t\talert("게임 로딩 실패: main() 없음");
\t\t\treturn;
\t\t}
\t\tmain();
\t\tif (typeof window.__eaglerShowLoadingSplashAfterMain === "function") {
\t\t\twindow.__eaglerShowLoadingSplashAfterMain();
\t\t} else if (typeof window.__eaglerShowLoadingSplash === "function") {
\t\t\tvar frame = document.getElementById("game_frame");
\t\t\tif (frame) window.__eaglerShowLoadingSplash(frame);
\t\t}
\t\tif (typeof window.__eaglerStartLoadingOverlayWatch === "function") {
\t\t\twindow.__eaglerStartLoadingOverlayWatch();
\t\t}
\t}

\twindow.addEventListener("load", function() {
\t\twindow.addEventListener("keydown", __eaglerLaunchGame);
\t\twindow.addEventListener("mousedown", __eaglerLaunchGame);
\t\twindow.addEventListener("touchstart", __eaglerLaunchGame);
\t});"""

OLD_BODY = """<body style="margin:0px;width:100%;height:100%;overflow:hidden;background-color:white;" id="game_frame">
<div style="margin:0px;width:100%;height:100%;font-family:sans-serif;display:flex;align-items:center;user-select:none;" id="launch_countdown_screen">
<div style="margin:auto;text-align:center;">
<h1>This file is from <span style="color:#AA0000;">03/30/2025</span></h1>
<h2>Game will launch in <span id="launchCountdownNumber">5</span>...</h2>
<div style="border:2px solid black;width:100%;height:15px;padding:1px;margin-bottom:20vh;"><div id="launchCountdownProgress" style="background-color:#555555;width:0%;height:100%;"></div>
<p style="margin-top:30px;"><button id="skipCountdown" autofocus>Skip Countdown</button></p></div>
</div>
</div>"""

NEW_BODY = """<body style="margin:0px;width:100%;height:100%;overflow:hidden;background-color:black;" id="game_frame">
<div style="margin:0px;width:100%;height:100%;image-rendering:pixelated;background:center / contain no-repeat url(splash.png?v=21), 0px 0px / 1000000% 1000000% no-repeat url(splash.png?v=21) black;user-select:none;" id="launch_countdown_screen">
</div>"""

OLD_OPTS = """window.eaglercraftXOpts = {
\tcontainer: "game_frame",
\tworldsDB: "worlds"
};"""

NEW_OPTS = """window.eaglercraftXOpts = {
\tcontainer: "game_frame",
\tworldsDB: "worlds",
\tshowBootMenuOnLaunch: false,
\tallowBootMenu: false,
\tbootMenuBlocksUnsignedClients: false,
\tcheckRelaysForUpdates: true,
\tallowServerRedirects: true,
\trelays: [
\t\t{ addr: "wss://relay.deev.is/", comment: "relay #1", primary: relayId === 0 },
\t\t{ addr: "wss://relay.lax1dude.net/", comment: "relay #2", primary: relayId === 1 },
\t\t{ addr: "wss://relay.shhnowisnottheti.me/", comment: "relay #3", primary: relayId === 2 }
\t]
};

(function() {
\tvar q = window.location.search;
\tif ((typeof q === "string") && q[0] === "?" && (typeof URLSearchParams !== "undefined")) {
\t\tvar s = new URLSearchParams(q).get("server");
\t\tif (s) window.eaglercraftXOpts.joinServer = s;
\t}
})();"""


def main() -> int:
    text = WEB.read_text(encoding="utf-8")
    before = len(text)
    if OLD_LAUNCH not in text:
        print("launch block missing")
        return 1
    if OLD_BODY not in text:
        print("body block missing")
        return 1
    if OLD_OPTS not in text:
        print("opts block missing")
        return 1
    text = text.replace("<title>Eaglercraft 1.12 WASM-GC</title>", "<title>Minecraft By Jaewon</title>", 1)
    if "jaewon-boot.js" not in text:
        text = text.replace(
            "<title>Minecraft By Jaewon</title>",
            '<title>Minecraft By Jaewon</title>\n'
            '<link type="image/png" rel="shortcut icon" href="favicon.png?v=21" />\n'
            '<script type="text/javascript">window.__eaglerOverlayMode="timer";'
            'window.__eaglerOverlayMinMs=10000;</script>\n'
            '<script type="text/javascript" src="jaewon-boot.js?v=21"></script>',
            1,
        )
    text = text.replace(OLD_OPTS, NEW_OPTS, 1)
    text = text.replace(OLD_LAUNCH, NEW_LAUNCH, 1)
    text = text.replace(OLD_BODY, NEW_BODY, 1)
    if "</html>" not in text or "<body" not in text:
        print("refusing to write: html structure broken")
        return 1
    tmp = WEB.with_suffix(".html.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, WEB)
    print("patched", WEB, "size", before, "->", len(text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
