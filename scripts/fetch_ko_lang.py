import json
import os
import urllib.request

manifest = json.load(urllib.request.urlopen("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"))
v = next(x for x in manifest["versions"] if x["id"] == "1.8.8")
vjson = json.load(urllib.request.urlopen(v["url"]))
idx = json.load(urllib.request.urlopen(vjson["assetIndex"]["url"]))
obj = idx["objects"].get("minecraft/lang/ko_kr.lang") or idx["objects"].get("minecraft/lang/ko_KR.lang")
if not obj:
    raise SystemExit("ko_kr.lang not in 1.8.8 asset index")

url = f"https://resources.download.minecraft.net/{obj['hash'][:2]}/{obj['hash']}"
data = urllib.request.urlopen(url).read()

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for sub in ("eaglymc/lang", "eaglymc-wasm/lang"):
    out_dir = os.path.join(base, sub)
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "ko_kr.lang")
    with open(out, "wb") as f:
        f.write(data)
    print(f"saved {len(data)} bytes -> {out}")
