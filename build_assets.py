#!/usr/bin/env python3
"""Generates the SVG assets for the profile README.

Run:  python3 build_assets.py

When a business from the "100" is released, add its slot number to RELEASED.
The grid fills that cell with the accent colour and moves the "next" marker.
Example:  RELEASED = [1, 2]
"""
from pathlib import Path

RELEASED: list[int] = []  # slot numbers (1..100) that are public

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(
        bg="#0B0B0C", border="#26262A", text="#F3F3F0", sub="#A0A0A6",
        muted="#6A6A70", cell="#1B1B1F", cell_line="#2A2A2F",
        accent="#FF5B1F", dot="#FFFFFF", dot_op="0.10",
    ),
    "light": dict(
        bg="#FAFAF7", border="#E3E3DD", text="#0B0B0C", sub="#55555B",
        muted="#8B8B90", cell="#F0F0EA", cell_line="#DEDED7",
        accent="#E8480C", dot="#000000", dot_op="0.10",
    ),
}


def banner(t: dict) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 320" width="1200" height="320" role="img" aria-label="Ilyas. Builder working toward 100 real businesses.">
  <style>
    .blink {{ animation: blink 1.1s steps(1) infinite; }}
    @keyframes blink {{ 0%,49% {{ opacity: 1 }} 50%,100% {{ opacity: 0 }} }}
    @media (prefers-reduced-motion: reduce) {{ .blink {{ animation: none; }} }}
  </style>
  <defs>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="{t['dot']}" fill-opacity="{t['dot_op']}"/>
    </pattern>
    <linearGradient id="fade" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0.35" stop-color="#fff" stop-opacity="0"/>
      <stop offset="1" stop-color="#fff" stop-opacity="1"/>
    </linearGradient>
    <mask id="m"><rect width="1200" height="320" fill="url(#fade)"/></mask>
  </defs>
  <rect x="0.5" y="0.5" width="1199" height="319" rx="20" fill="{t['bg']}" stroke="{t['border']}"/>
  <rect x="1" y="1" width="1198" height="318" rx="20" fill="url(#dots)" mask="url(#m)"/>

  <text x="64" y="68" font-family="{MONO}" font-size="16" letter-spacing="3" fill="{t['muted']}">BUILDER  /  EARLY STAGE</text>

  <text x="60" y="176" font-family="{SANS}" font-size="116" font-weight="700" letter-spacing="-5" fill="{t['text']}">Ilyas<tspan fill="{t['accent']}">.</tspan></text>

  <text x="64" y="246" font-family="{SANS}" font-size="30" fill="{t['sub']}">I build products and test them on real people.</text>
  <text x="64" y="280" font-family="{SANS}" font-size="30" fill="{t['sub']}">The ones that work, I plan to give away.</text>

  <text x="1136" y="68" text-anchor="end" font-family="{MONO}" font-size="16" fill="{t['muted']}">slot 001 / in progress<tspan class="blink" fill="{t['accent']}"> &#9610;</tspan></text>
</svg>
"""


def grid(t: dict) -> str:
    cols, rows, size, gap = 20, 5, 36, 8
    w = cols * size + (cols - 1) * gap          # 872
    pad = 4
    top = 0
    gh = rows * size + (rows - 1) * gap          # 212
    foot = 44
    total_w, total_h = w + pad * 2, gh + foot + pad * 2
    released = set(RELEASED)
    nxt = next((i for i in range(1, 101) if i not in released), None)

    cells = []
    for i in range(1, 101):
        r, c = divmod(i - 1, cols)
        x = pad + c * (size + gap)
        y = pad + top + r * (size + gap)
        if i in released:
            cells.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="8" fill="{t["accent"]}"/>')
        elif i == nxt:
            cells.append(
                f'<rect class="next" x="{x+1}" y="{y+1}" width="{size-2}" height="{size-2}" rx="8" '
                f'fill="none" stroke="{t["accent"]}" stroke-width="2"/>'
                f'<text x="{x+size/2}" y="{y+size/2+4}" text-anchor="middle" font-family="{MONO}" '
                f'font-size="11" fill="{t["accent"]}">{i:03d}</text>'
            )
        else:
            cells.append(
                f'<rect x="{x+0.5}" y="{y+0.5}" width="{size-1}" height="{size-1}" rx="8" '
                f'fill="{t["cell"]}" stroke="{t["cell_line"]}"/>'
            )

    fy = pad + gh + 30
    count = f"{len(released):03d} / 100 released"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {total_h}" width="{total_w}" height="{total_h}" role="img" aria-label="{len(released)} of 100 businesses released">
  <style>
    .next {{ animation: pulse 2.4s ease-in-out infinite; }}
    @keyframes pulse {{ 0%,100% {{ opacity: 1 }} 50% {{ opacity: 0.35 }} }}
    @media (prefers-reduced-motion: reduce) {{ .next {{ animation: none; }} }}
  </style>
  {chr(10).join('  ' + c for c in cells).strip()}
  <text x="{pad}" y="{fy}" font-family="{MONO}" font-size="16" letter-spacing="1" fill="{t['sub']}">{count}</text>
</svg>
"""


for name, t in THEMES.items():
    (OUT / f"banner-{name}.svg").write_text(banner(t), encoding="utf-8")
    (OUT / f"grid-{name}.svg").write_text(grid(t), encoding="utf-8")
print("assets written to", OUT)
