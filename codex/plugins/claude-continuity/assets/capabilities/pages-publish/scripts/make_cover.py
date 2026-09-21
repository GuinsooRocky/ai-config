#!/usr/bin/env python3
"""make_cover.py — 為 pages 頁面生成一張品牌封面 banner(公众号式圖文卡的封面來源)。

pages 的飛書卡片封面 = 頁面文檔順序第一張 <img>。純文字頁 / 想要設計感封面時,
用這支腳本生成一張暗色暖調 banner,嵌成頁面第一張圖,publish 後 share 就自動出封面。

流程:HTML+CSS 模板 → Chrome 無頭渲染成 2x PNG(CJK 字體最穩)→ sips/PIL 壓成 1200 寬 JPEG。
純 stdlib + 系統 Chrome;沒有 sips/PIL 時退回輸出 PNG(較大但可用)。

用法:
  python3 make_cover.py --title "一句話,把內網頁面[[發成飛書卡片]]" \
      --subtitle "封面圖 · 標題 · 描述 · 可點按鈕" \
      --chips "發卡片給我,公众号式閱讀,大圖不卡" \
      --brand PAGES --url pages.pkbops.com --out /tmp/cover.jpg

  # 標題裡用 [[...]] 標記要用主色高亮的詞。
  # --accent 換主色(預設琥珀 #e89a5f);--theme dark(預設)。

輸出:把最終圖片路徑印到 stdout。拿去當頁面第一張 <img src="data:image/jpeg;base64,...">。
"""
import argparse
import base64
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]

# 现成主题:每套都是「近黑底 + 单一强调色」的暗色调(遵循 taste-skill:不用纯黑、不用 AI 紫)。
# 选一个 --theme 即可;想微调强调色再叠 --accent。c1/c2/c3=背景渐层,glow=角落光晕,
# sun=光球主色,accent=点缀(点/横线/chip),hl=标题高亮字色。
THEMES = {
    "amber":  {"c1": "#140d0a", "c2": "#0b0706", "c3": "#080505",
               "glow": "rgba(232,154,95,0.42)", "sun": "rgba(246,196,142,0.90)",
               "sunmid": "rgba(232,154,95,0.35)", "accent": "#e89a5f", "hl": "#f6c48e"},
    "indigo": {"c1": "#0b0f18", "c2": "#080b12", "c3": "#05070c",
               "glow": "rgba(110,168,254,0.38)", "sun": "rgba(180,208,255,0.88)",
               "sunmid": "rgba(110,168,254,0.32)", "accent": "#6ea8fe", "hl": "#a9c9ff"},
    "forest": {"c1": "#0a1210", "c2": "#07100c", "c3": "#050b08",
               "glow": "rgba(79,208,160,0.34)", "sun": "rgba(160,235,205,0.85)",
               "sunmid": "rgba(79,208,160,0.30)", "accent": "#4fd0a0", "hl": "#96e6c4"},
    "rose":   {"c1": "#150a0e", "c2": "#0e0609", "c3": "#080406",
               "glow": "rgba(232,115,154,0.36)", "sun": "rgba(246,180,205,0.86)",
               "sunmid": "rgba(232,115,154,0.32)", "accent": "#e8739a", "hl": "#f6a9c4"},
    "slate":  {"c1": "#111318", "c2": "#0c0e12", "c3": "#08090c",
               "glow": "rgba(90,209,224,0.32)", "sun": "rgba(175,235,243,0.85)",
               "sunmid": "rgba(90,209,224,0.28)", "accent": "#5ad1e0", "hl": "#a8ebf3"},
}


def find_chrome() -> str:
    for p in CHROME_CANDIDATES:
        if os.path.exists(p):
            return p
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge"):
        p = shutil.which(name)
        if p:
            return p
    sys.exit("找不到 Chrome/Chromium,無法渲染 banner。裝一個或改用有圖的頁面。")


def hl(title: str) -> str:
    """[[...]] → 主色 <span>;其餘 escape。"""
    out, i = [], 0
    for m in re.finditer(r"\[\[(.+?)\]\]", title):
        out.append(html.escape(title[i:m.start()]))
        out.append(f'<span class="hl">{html.escape(m.group(1))}</span>')
        i = m.end()
    out.append(html.escape(title[i:]))
    return "".join(out).replace("\n", "<br>")


def build_html(a, t) -> str:
    accent = a.accent or t["accent"]
    hl_color = t["hl"] if not a.accent else accent  # 覆盖 accent 时高亮字跟着走
    chips = [c.strip() for c in a.chips.split(",") if c.strip()] if a.chips else []
    chip_html = ""
    for j, c in enumerate(chips):
        cls = "chip amber" if j == 0 else "chip"
        chip_html += f'<span class="{cls}">{html.escape(c)}</span>'
    sub = f'<p class="sub">{html.escape(a.subtitle)}</p>' if a.subtitle else ""
    url = f'<span class="u">{html.escape(a.url)}</span>' if a.url else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1200px;height:630px;overflow:hidden}}
.stage{{width:1200px;height:630px;position:relative;
  background:
    radial-gradient(120% 90% at 84% 18%, {t["glow"]}, transparent 46%),
    radial-gradient(90% 80% at 12% 96%, rgba(120,120,120,0.10), transparent 52%),
    linear-gradient(150deg,{t["c1"]} 0%,{t["c2"]} 58%,{t["c3"]} 100%);
  font-family:"PingFang TC","PingFang SC",-apple-system,"Helvetica Neue",sans-serif;
  color:#f3efe9;overflow:hidden}}
.horizon{{position:absolute;left:0;right:0;top:60%;height:1px;
  background:linear-gradient(90deg,transparent,{accent}8c,transparent);opacity:.7}}
.sun{{position:absolute;right:150px;top:130px;width:220px;height:220px;border-radius:50%;
  background:radial-gradient(circle,{t["sun"]},{t["sunmid"]} 55%,transparent 72%);filter:blur(2px)}}
.grain{{position:absolute;inset:0;opacity:.05;
  background-image:repeating-linear-gradient(0deg,#fff 0 1px,transparent 1px 3px)}}
.wrap{{position:absolute;inset:0;padding:74px 80px;display:flex;flex-direction:column;justify-content:space-between}}
.brand{{display:flex;align-items:center;gap:14px;letter-spacing:.26em;font-size:16px;font-weight:700;color:#f0ede8}}
.brand .dot{{width:9px;height:9px;border-radius:50%;background:{accent};box-shadow:0 0 14px 2px {accent}b3}}
.brand .u{{margin-left:auto;letter-spacing:.04em;font-weight:500;font-size:15px;color:rgba(240,237,232,0.55)}}
h1{{font-size:74px;line-height:1.14;font-weight:650;letter-spacing:-0.01em;max-width:15ch;
  text-shadow:0 2px 30px rgba(0,0,0,.5)}}
h1 .hl{{color:{hl_color}}}
.sub{{margin-top:22px;font-size:24px;line-height:1.5;color:rgba(240,237,232,0.66);max-width:32ch;font-weight:400}}
.foot{{display:flex;align-items:center;gap:18px;flex-wrap:wrap}}
.chip{{font-size:16px;color:rgba(240,237,232,0.72);border:1px solid rgba(240,237,232,0.16);
  border-radius:999px;padding:9px 18px;background:rgba(255,255,255,0.03)}}
.chip.amber{{color:#0c0c0e;background:linear-gradient(135deg,{accent},{t["hl"]});border:none;font-weight:650}}
</style></head><body><div class="stage">
<div class="sun"></div><div class="horizon"></div><div class="grain"></div>
<div class="wrap">
  <div class="brand"><span class="dot"></span>{html.escape(a.brand)}{url}</div>
  <div><h1>{hl(a.title)}</h1>{sub}</div>
  <div class="foot">{chip_html}</div>
</div></div></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True, help="主標題;[[詞]] 高亮;\\n 換行")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--chips", default="", help="逗號分隔,第一個高亮")
    ap.add_argument("--brand", default="PAGES")
    ap.add_argument("--url", default="pages.pkbops.com")
    ap.add_argument("--theme", default="amber", choices=sorted(THEMES),
                    help="配色主题:amber(暖)/indigo(冷蓝)/forest(绿)/rose(玫)/slate(青灰)")
    ap.add_argument("--accent", default="", help="覆盖主题强调色 hex(选填)")
    ap.add_argument("--out", default="/tmp/pages_cover.jpg")
    a = ap.parse_args()
    a.title = a.title.replace("\\n", "\n")
    t = THEMES[a.theme]

    chrome = find_chrome()
    with tempfile.TemporaryDirectory() as d:
        hp = os.path.join(d, "banner.html")
        pp = os.path.join(d, "banner.png")
        with open(hp, "w") as f:
            f.write(build_html(a, t))
        subprocess.run([chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=2", "--window-size=1200,630",
                        f"--screenshot={pp}", f"file://{hp}"],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not os.path.exists(pp):
            sys.exit("Chrome 渲染失敗,沒產出 PNG")

        # 壓成 1200 寬 JPEG:優先 sips(mac),再 PIL,都沒有就輸出 PNG
        out = a.out
        if shutil.which("sips"):
            subprocess.run(["sips", "-Z", "1200", "-s", "format", "jpeg",
                            "-s", "formatOptions", "86", pp, "--out", out],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            try:
                from PIL import Image
                im = Image.open(pp).convert("RGB")
                im.thumbnail((1200, 1200))
                im.save(out, "JPEG", quality=86)
            except Exception:
                out = os.path.splitext(a.out)[0] + ".png"
                shutil.copy(pp, out)

    size = os.path.getsize(out)
    b64 = base64.b64encode(open(out, "rb").read()).decode()
    sys.stderr.write(f"[make_cover] {out} ({size // 1024} KB, base64 {len(b64) // 1024} KB)\n")
    print(out)


if __name__ == "__main__":
    main()
