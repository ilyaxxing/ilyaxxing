#!/usr/bin/env python3
"""Draws every image used in README.md (dark + light versions).

    python3 build_assets.py

The banner: me underground, taking a breather against a thin wall,
with diamonds right behind it. The HUD numbers live in HUD below.
"""
import colorsys
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "art"))
from props import DIAMOND, SPARKLE  # noqa: E402

HUD = [("SHIPPED", "01", "text"), ("LATEST", "CASH FOR CARS", "text"), ("NEXT", "COOKIN'", "warm")]

OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)
ME = json.loads((ROOT / "art" / "me.json").read_text())

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(bg="#0E1116", line="#262C36", text="#F0F6FC", muted="#8B949E", accent="#3FB950", warm="#F0883E"),
    "light": dict(bg="#FFFFFF", line="#D0D7DE", text="#1F2328", muted="#59636E", accent="#1A7F37", warm="#BC4C00"),
}

# underground palette (same in both themes: it's dirt)
EARTH = dict(dirt="#5A3B24", dirt_dk="#47301E", speck="#6E4B2F", stone="#6F6C6A", stone_dk="#55524F",
             cave="#1A120C", cave_lit="#24190F", grass="#3FB950", grass_dk="#2A8A3B", outline="#101216")
GEM = {"O": "#0A3C46", "C": "#4FD8EB", "c": "#1D98AE", "W": "#E9FDFF"}

# terrain grid
TX, TY, CELL = 700, 214, 8          # top-left of the dirt, cell size
COLS, ROWS = 63, 49
SURFACE = 3                         # grass row
FLOOR = 40                          # tunnel floor row (exclusive)
WALL = (41, 43)                     # the thin wall, columns [41, 43)


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
    pad = [["."] * (w + 2) for _ in range(h + 2)]
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            pad[r + 1][c + 1] = ch
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


def tunnel_cells():
    """Which terrain cells are dug out: a slanted shaft from the surface, then a flat tunnel."""
    dug = set()
    for r in range(SURFACE, FLOOR):
        a = 4 + (r - SURFACE) * 2 // 3
        for c in range(a, a + 8):
            dug.add((r, c))
    for r in range(FLOOR - 18, FLOOR):
        for c in range(14, WALL[0]):
            dug.add((r, c))
    return dug


def underground() -> str:
    rnd = random.Random(7)
    dug = tunnel_cells()
    x1, y1 = TX + COLS * CELL, TY + ROWS * CELL
    parts = [f'<rect x="{TX}" y="{TY + (SURFACE + 1) * CELL}" width="{COLS * CELL}" height="{(ROWS - SURFACE - 1) * CELL}" fill="{EARTH["dirt"]}"/>']

    # texture: specks and a few stones in the solid dirt
    for r in range(SURFACE + 1, ROWS):
        for c in range(COLS):
            if (r, c) in dug:
                continue
            v = rnd.random()
            if v < 0.10:
                parts.append(f'<rect x="{TX + c * CELL}" y="{TY + r * CELL}" width="{CELL}" height="{CELL}" fill="{EARTH["dirt_dk"]}"/>')
            elif v < 0.16:
                parts.append(f'<rect x="{TX + c * CELL}" y="{TY + r * CELL}" width="{CELL}" height="{CELL}" fill="{EARTH["speck"]}"/>')
    for r, c in [(9, 30), (14, 48), (27, 6), (36, 9), (8, 52), (31, 54)]:
        if (r, c) not in dug:
            parts.append(f'<rect x="{TX + c * CELL}" y="{TY + r * CELL}" width="{CELL * 2}" height="{CELL * 2}" fill="{EARTH["stone"]}"/>'
                         f'<rect x="{TX + c * CELL + CELL}" y="{TY + r * CELL + CELL}" width="{CELL}" height="{CELL}" fill="{EARTH["stone_dk"]}"/>')

    # grass on top (with a gap where the shaft starts)
    for c in range(COLS):
        if (SURFACE, c) in dug:
            continue
        parts.append(f'<rect x="{TX + c * CELL}" y="{TY + SURFACE * CELL}" width="{CELL}" height="{CELL}" fill="{EARTH["grass"]}"/>')
        if rnd.random() < 0.35:
            parts.append(f'<rect x="{TX + c * CELL}" y="{TY + (SURFACE - 1) * CELL + 4}" width="{CELL // 2}" height="{CELL // 2 + 0}" fill="{EARTH["grass"]}"/>')
        parts.append(f'<rect x="{TX + c * CELL}" y="{TY + (SURFACE + 1) * CELL}" width="{CELL}" height="{CELL // 2}" fill="{EARTH["grass_dk"]}"/>')

    # the dug-out tunnel, row by row
    for r in range(SURFACE, FLOOR):
        cs = sorted(c for (rr, c) in dug if rr == r)
        if not cs:
            continue
        start = prev = cs[0]
        for c in cs[1:] + [None]:
            if c is not None and c == prev + 1:
                prev = c
                continue
            parts.append(f'<rect x="{TX + start * CELL}" y="{TY + r * CELL}" width="{(prev - start + 1) * CELL}" height="{CELL}" fill="{EARTH["cave"]}"/>')
            if c is not None:
                start = prev = c
    # a little light on the floor
    parts.append(f'<rect x="{TX + 14 * CELL}" y="{TY + (FLOOR - 1) * CELL}" width="{(WALL[0] - 14) * CELL}" height="{CELL}" fill="{EARTH["cave_lit"]}"/>')

    # diamonds behind the wall
    gems, sparks = [], []
    spots = [(26, 45), (31, 49), (35, 44), (28, 51), (35, 51), (32, 45)]
    for k, (r, c) in enumerate(spots):
        gx, gy = TX + c * CELL, TY + r * CELL
        gems.append(pixels(outlined(DIAMOND), {**GEM, "!": "#0A2E35"}, gx - 4, gy - 4, 4))
        sparks.append(f'<g class="spark" style="animation-delay:{k * 0.45:.2f}s">'
                      f'{pixels(SPARKLE, {"W": GEM["W"]}, gx + 22, gy - 10, 3)}</g>')
    return "".join(parts) + "".join(gems) + "".join(sparks)


def me(ground_y: int, wall_x: int) -> str:
    """Me sitting on the tunnel floor, back to the wall."""
    u = 2
    pal = {k: lighten_vest(v) for k, v in ME["palette"].items()}
    pal["!"] = EARTH["outline"]
    body = outlined(ME["rows"])
    w, h = len(body[0]), len(body)
    x, y = wall_x - w * u, ground_y - h * u
    return f'<g class="breathe" style="transform-origin:{x + w * u // 2}px {ground_y}px">{pixels(body, pal, x, y, u)}</g>'


def crumbs() -> str:
    """Dirt crumbs falling from the tunnel ceiling."""
    out = []
    for k, c in enumerate([22, 30, 37]):
        x = TX + c * CELL + 2
        y = TY + (FLOOR - 18) * CELL
        out.append(f'<rect class="crumb" style="animation-delay:{k * 1.3:.1f}s" x="{x}" y="{y}" width="4" height="4" fill="{EARTH["speck"]}"/>')
    return "".join(out)


def banner(t: dict) -> str:
    ground_y = TY + FLOOR * CELL
    wall_x = TX + WALL[0] * CELL
    hud = "".join(
        f'<text x="1130" y="{86 + i * 28}" fill="{t["muted"]}">{k} <tspan fill="{t[col]}"{" font-weight=\"700\"" if i == 0 else ""}>{v}</tspan>'
        f'{"<tspan class=\"blink\" fill=\"" + t[col] + "\">_</tspan>" if i == len(HUD) - 1 else ""}</text>'
        for i, (k, v, col) in enumerate(HUD))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" width="1200" height="600" role="img" aria-label="Clone it. Launch it. Get paid.">
  <style>
    .blink {{ animation: blink 1.8s ease-in-out infinite; }}
    @keyframes blink {{ 0%,100% {{ opacity: 1 }} 50% {{ opacity: .25 }} }}
    .spark {{ opacity: 0; animation: spark 2.7s steps(1) infinite; }}
    @keyframes spark {{ 0% {{ opacity: 0 }} 8% {{ opacity: 1 }} 16% {{ opacity: .4 }} 22%,100% {{ opacity: 0 }} }}
    .breathe {{ animation: breathe 2.6s ease-in-out infinite; }}
    @keyframes breathe {{ 0%,100% {{ transform: scaleY(1) }} 50% {{ transform: scaleY(1.012) }} }}
    .crumb {{ opacity: 0; animation: crumb 3.9s ease-in infinite; }}
    @keyframes crumb {{ 0% {{ opacity: 0; transform: translateY(0) }} 5% {{ opacity: 1 }} 30% {{ opacity: 1; transform: translateY(136px) }} 31%,100% {{ opacity: 0; transform: translateY(136px) }} }}
    @media (prefers-reduced-motion: reduce) {{ .blink, .spark, .breathe, .crumb {{ animation: none; }} .crumb {{ opacity: 0; }} }}
  </style>
  <defs><clipPath id="card"><rect x="1" y="1" width="1198" height="598" rx="32"/></clipPath></defs>
  <rect x="1" y="1" width="1198" height="598" rx="32" fill="{t['bg']}"/>

  <text x="72" y="112" font-family="{MONO}" font-size="24" letter-spacing="1" fill="{t['muted']}">@ilyaxxing</text>
  <g font-family="{SANS}" font-size="84" font-weight="800" letter-spacing="-2.5">
    <text x="68" y="212" fill="{t['text']}">Clone it.</text>
    <text x="68" y="306" fill="{t['text']}">Launch it.</text>
    <text x="68" y="400" fill="{t['accent']}">Get paid.</text>
  </g>
  <text x="72" y="472" font-family="{SANS}" font-size="29" fill="{t['muted']}">Ready-to-run businesses, tested IRL.</text>
  <text x="72" y="512" font-family="{SANS}" font-size="29" fill="{t['muted']}">The code is free. The hustle is yours.</text>

  <g font-family="{MONO}" font-size="17" text-anchor="end">{hud}</g>

  <g clip-path="url(#card)" shape-rendering="crispEdges">
    {underground()}
    {crumbs()}
    {me(ground_y, wall_x)}
  </g>
  <rect x="1" y="1" width="1198" height="598" rx="32" fill="none" stroke="{t['line']}" stroke-width="2"/>
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
