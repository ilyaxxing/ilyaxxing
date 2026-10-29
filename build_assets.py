#!/usr/bin/env python3
"""Draws every image used in README.md (dark + light versions).

    python3 build_assets.py

When a new project goes public: add it to PROJECTS, re-run, commit.
"""
from pathlib import Path

# newest last; status is "live" or "in progress"
PROJECTS = [
    dict(n=1, name="Cash for Cars", line1="QR lead system for car buyers.", line2="You set it up. They pay you.", status="live"),
    dict(n=2, name="Next up", line1="", line2="", status="cookin'"),
]

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(bg="#0E1116", line="#262C36", card="#161B22", text="#F0F6FC", muted="#8B949E",
                 faint="#21262D", accent="#3FB950", accent_soft="#3FB95026", warm="#F0883E",
                 block_hi="#7EE787", block_lo="#1A7F37", dirt="#2A2118", dirt2="#3A2D20", coin_text="#FFD43B"),
    "light": dict(bg="#FFFFFF", line="#D0D7DE", card="#F6F8FA", text="#1F2328", muted="#59636E",
                  faint="#E1E6EB", accent="#1A7F37", accent_soft="#1A7F3720", warm="#BC4C00",
                  block_hi="#7EE787", block_lo="#116329", dirt="#C9A97A", dirt2="#B8956A", coin_text="#9A6700"),
}




import colorsys
import json
import sys
sys.path.insert(0, str(Path(__file__).parent / "art"))
from props import BLOCK, COIN  # noqa: E402

ME = json.loads((Path(__file__).parent / "art" / "me.json").read_text())


def lighten_vest(hexcol: str) -> str:
    """The vest should read as very light grey: lift mid greys toward white."""
    r, g, b = (int(hexcol[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if s < 0.25 and 0.45 < l < 0.85:
        l = l + (0.97 - l) * 0.55
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#%02X%02X%02X" % (round(r * 255), round(g * 255), round(b * 255))


def outlined(rows):
    """1-cell dark outline around a sprite, NES style."""
    h, w = len(rows), max(len(r) for r in rows)
    grid = [list(r.ljust(w, ".")) for r in rows]
    pad = [["."] * (w + 2) for _ in range(h + 2)]
    for r in range(h):
        for c in range(w):
            pad[r + 1][c + 1] = grid[r][c]
    out = [row[:] for row in pad]
    for r in range(h + 2):
        for c in range(w + 2):
            if pad[r][c] == "." and any(0 <= r + dr < h + 2 and 0 <= c + dc < w + 2 and pad[r + dr][c + dc] != "."
                                        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[r][c] = "!"
    return ["".join(row) for row in out]


def pixels(rows, pal, x, y, u):
    return "".join(f'<rect x="{x + c * u}" y="{y + r * u}" width="{u}" height="{u}" fill="{pal[ch]}"/>'
                   for r, row in enumerate(rows) for c, ch in enumerate(row) if ch != ".")


def scene(t: dict, ground: int) -> str:
    """Me jumping into a mystery block; a coin pops out."""
    u = 3
    me_pal = {k: lighten_vest(v) for k, v in ME["palette"].items()}
    me_pal["!"] = "#101216"
    body = outlined(ME["rows"])
    mw, mh = len(body[0]), len(body)
    mx, my = 868, ground - mh * u
    fist_x = mx + 7 * u                       # raised fist, near the top-left of the sprite
    jump = 46

    bu = 4
    prop_pal = {"O": "#101216", "L": t["block_hi"], "A": t["accent"], "D": t["block_lo"], "W": "#FFFFFF",
                "Y": "#FFD43B", "y": "#D99A00", "Z": "#FFF6C4"}
    bx = fist_x - len(BLOCK[0]) * bu // 2
    by = my - jump - len(BLOCK) * bu + 12
    cx = fist_x - len(COIN[0]) * bu // 2

    ground_tiles = "".join(
        f'<rect x="{x}" y="{ground + 8}" width="14" height="8" fill="{t["dirt"] if (x // 16) % 2 else t["dirt2"]}"/>'
        f'<rect x="{x + 8}" y="{ground + 18}" width="14" height="8" fill="{t["dirt2"] if (x // 16) % 2 else t["dirt"]}"/>'
        for x in range(700, 1136, 16))
    return f"""<g shape-rendering="crispEdges">
    <rect x="700" y="{ground}" width="450" height="6" fill="{t['accent']}"/>
    {ground_tiles}
    <g class="coin" style="transform-origin:{fist_x}px {by}px">{pixels(COIN, prop_pal, cx, by + 8, bu)}</g>
    <g class="block">{pixels(BLOCK, prop_pal, bx, by, bu)}</g>
    <g class="hero">{pixels(body, me_pal, mx - u, my - u, u)}</g>
    <text class="plus" x="{bx - 44}" y="{by + 10}" font-family="{MONO}" font-size="22" font-weight="700" fill="{t['coin_text']}">+1</text>
  </g>"""


def card(x, y, p, t, front: bool, opacity=1.0) -> str:
    w, h = 440, 236
    live = p["status"] == "live"
    color = t["accent"] if live else t["warm"]
    pill_w = int(len(p["status"]) * 9.7 + 46)
    body = ""
    if front:
        body = (f'<text x="{x + 32}" y="{y + 132}" font-family="{SANS}" font-size="40" font-weight="700" fill="{t["text"]}">{p["name"]}</text>'
                f'<text x="{x + 32}" y="{y + 176}" font-family="{SANS}" font-size="23" fill="{t["muted"]}">{p["line1"]}</text>'
                f'<text x="{x + 32}" y="{y + 208}" font-family="{SANS}" font-size="23" fill="{t["muted"]}">{p["line2"]}</text>')
    return f"""<g opacity="{opacity}">
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{t['card']}" stroke="{t['line']}" stroke-width="2"/>
    <text x="{x + 32}" y="{y + 58}" font-family="{MONO}" font-size="24" fill="{t['muted']}">{"Fresh drop" if p["status"] == "live" else "Next up"}</text>
    <rect x="{x + w - 32 - pill_w}" y="{y + 36}" width="{pill_w}" height="30" rx="15" fill="{t['accent_soft'] if live else 'none'}" stroke="{color if not live else 'none'}" stroke-dasharray="4 4"/>
    <circle class="{'blink' if live else ''}" cx="{x + w - 32 - pill_w + 18}" cy="{y + 51}" r="5" fill="{color}"/>
    <text x="{x + w - 32 - pill_w + 31}" y="{y + 57}" font-family="{MONO}" font-size="16" fill="{color}">{p['status']}</text>
    {body}
  </g>"""


def banner(t: dict) -> str:
    live = [p for p in PROJECTS if p["status"] == "live"]
    front = live[-1]
    behind = [p for p in PROJECTS if p is not front][-1:]
    done = len(live)



    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" width="1200" height="600" role="img" aria-label="Clone it. Launch it. Get paid.">
  <style>
    .blink {{ animation: blink 1.8s ease-in-out infinite; }}
    @keyframes blink {{ 0%,100% {{ opacity: 1 }} 50% {{ opacity: .25 }} }}
    .hero {{ animation: hop 1.8s infinite; }}
    @keyframes hop {{
      0%,34% {{ transform: translateY(0); animation-timing-function: ease-out; }}
      46% {{ transform: translateY(-46px); animation-timing-function: ease-in; }}
      60% {{ transform: translateY(0); }}
      64% {{ transform: translateY(2px); }}
      68%,100% {{ transform: translateY(0); }}
    }}
    .block {{ animation: bump 1.8s infinite; }}
    @keyframes bump {{ 0%,45% {{ transform: translateY(0) }} 49% {{ transform: translateY(-10px) }} 54%,100% {{ transform: translateY(0) }} }}
    .coin {{ opacity: 0; animation: coin 1.8s infinite; }}
    @keyframes coin {{
      0%,45% {{ opacity: 0; transform: translateY(0) scaleX(1); }}
      47% {{ opacity: 1; transform: translateY(-20px) scaleX(1); }}
      56% {{ transform: translateY(-44px) scaleX(.15); }}
      65% {{ transform: translateY(-58px) scaleX(1); }}
      74% {{ opacity: 1; transform: translateY(-48px) scaleX(.15); }}
      80%,100% {{ opacity: 0; transform: translateY(-36px) scaleX(1); }}
    }}
    .plus {{ opacity: 0; animation: plus 1.8s infinite; }}
    @keyframes plus {{ 0%,62% {{ opacity: 0; transform: translateY(0) }} 68% {{ opacity: 1 }} 90% {{ opacity: 1; transform: translateY(-12px) }} 100% {{ opacity: 0; transform: translateY(-14px) }} }}
    @media (prefers-reduced-motion: reduce) {{ .blink, .hero, .block, .coin, .plus {{ animation: none; }} .coin, .plus {{ opacity: 0; }} }}
  </style>
  <rect x="1" y="1" width="1198" height="598" rx="32" fill="{t['bg']}" stroke="{t['line']}" stroke-width="2"/>

  <text x="72" y="112" font-family="{MONO}" font-size="24" letter-spacing="1" fill="{t['muted']}">@ilyaxxing</text>
  <g font-family="{SANS}" font-size="84" font-weight="800" letter-spacing="-2.5">
    <text x="68" y="212" fill="{t['text']}">Clone it.</text>
    <text x="68" y="306" fill="{t['text']}">Launch it.</text>
    <text x="68" y="400" fill="{t['accent']}">Get paid.</text>
  </g>
  <text x="72" y="472" font-family="{SANS}" font-size="29" fill="{t['muted']}">Ready-to-run businesses, tested IRL.</text>
  <text x="72" y="512" font-family="{SANS}" font-size="29" fill="{t['muted']}">The code is free. The hustle is yours.</text>

  <g font-family="{MONO}" font-size="17" text-anchor="end">
    <text x="1130" y="98" fill="{t['muted']}">SHIPPED <tspan fill="{t['text']}" font-weight="700">01</tspan></text>
    <text x="1130" y="128" fill="{t['muted']}">LATEST <tspan fill="{t['text']}">CASH FOR CARS</tspan></text>
    <text x="1130" y="158" fill="{t['muted']}">NEXT <tspan fill="{t['warm']}">COOKIN'<tspan class="blink">_</tspan></tspan></text>
  </g>
  {scene(t, 540)}

</svg>
"""


def instagram(t: dict) -> str:
    """Pill-shaped Instagram link for the footer."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 64" width="340" height="64" role="img" aria-label="Instagram: @ilyaxxing">
  <rect x="1" y="1" width="338" height="62" rx="31" fill="{t['bg']}" stroke="{t['line']}" stroke-width="1.5"/>
  <g fill="none" stroke="{t['text']}" stroke-width="2">
    <rect x="26" y="20" width="24" height="24" rx="7"/>
    <circle cx="38" cy="32" r="5.5"/>
  </g>
  <circle cx="45" cy="25" r="1.6" fill="{t['text']}"/>
  <text x="66" y="38.5" font-family="{SANS}" font-size="19" font-weight="600" fill="{t['text']}">@ilyaxxing</text>
  <text x="306" y="38" text-anchor="end" font-family="{SANS}" font-size="20" fill="{t['accent']}">→</text>
</svg>
"""


for old in OUT.glob("*.svg"):
    old.unlink()
for name, t in THEMES.items():
    (OUT / f"banner-{name}.svg").write_text(banner(t), encoding="utf-8")
    (OUT / f"instagram-{name}.svg").write_text(instagram(t), encoding="utf-8")
print("done:", sorted(p.name for p in OUT.iterdir()))
