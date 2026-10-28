#!/usr/bin/env python3
"""Draws the banner used in README.md (dark + light versions).

    python3 build_assets.py

When a business from the 100 goes public, bump PUBLIC by one and re-run.
The grid fills up and the counter changes. That's it.
"""
from pathlib import Path

PUBLIC = 1  # how many of the 100 are out in the world

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
SERIF = "Georgia, 'Iowan Old Style', 'Times New Roman', serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(text="#F0F0EC", muted="#8B9098", faint="#30363D", accent="#8FD694", glow="#FFFFFF", glow_op="0.07"),
    "light": dict(text="#1F2328", muted="#656D76", faint="#D8DEE4", accent="#3F9A4A", glow="#000000", glow_op="0"),
}


def clover(cx: float, cy: float, r: float, color: str) -> str:
    """Three round leaves and a stem. Sways a little."""
    leaves = "".join(
        f'<circle cx="{cx + dx * r:.1f}" cy="{cy + dy * r:.1f}" r="{r:.1f}" fill="{color}"/>'
        for dx, dy in [(0, -0.95), (-0.85, 0.35), (0.85, 0.35)]
    )
    stem = (f'<path d="M{cx:.1f},{cy + 0.4 * r:.1f} q{0.3 * r:.1f},{1.6 * r:.1f} {1.3 * r:.1f},{2.4 * r:.1f}" '
            f'stroke="{color}" stroke-width="{0.38 * r:.1f}" stroke-linecap="round" fill="none"/>')
    return (f'<g class="sway" style="transform-origin:{cx:.0f}px {cy + 2.6 * r:.0f}px">'
            f'{leaves}{stem}</g>')


def header(t: dict) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 400" width="760" height="400" role="img" aria-label="ilyas. I build things on the internet, mostly to see what happens.">
  <style>
    .sway {{ animation: sway 7s ease-in-out infinite; }}
    @keyframes sway {{ 0%,100% {{ transform: rotate(-7deg) }} 50% {{ transform: rotate(7deg) }} }}
    @media (prefers-reduced-motion: reduce) {{ .sway {{ animation: none; }} }}
  </style>
  <defs>
    <radialGradient id="lamp" gradientUnits="userSpaceOnUse" cx="260" cy="215" r="200">
      <stop offset="0" stop-color="{t['glow']}" stop-opacity="{t['glow_op']}"/>
      <stop offset="1" stop-color="{t['glow']}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="760" height="400" fill="url(#lamp)"/>

  <text x="0" y="214" font-family="{SANS}" font-size="168" font-weight="700" letter-spacing="-8" fill="{t['text']}">ilyas</text>
  {clover(402, 104, 12, t['accent'])}

  <text x="8" y="300" font-family="{SERIF}" font-style="italic" font-size="38" fill="{t['muted']}">I build things on the internet,</text>
  <text x="8" y="350" font-family="{SERIF}" font-style="italic" font-size="38" fill="{t['muted']}">mostly to see what happens.</text>
</svg>
"""


def progress(t: dict) -> str:
    x0, x1, y = 56, 580, 40
    x = x0 + (x1 - x0) * PUBLIC / 100
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 90" width="640" height="90" role="img" aria-label="{PUBLIC} of 100 businesses public">
  <style>
    .ring {{ animation: ring 3.2s ease-out infinite; transform-origin: {x:.0f}px {y}px; }}
    @keyframes ring {{ 0% {{ transform: scale(1); opacity: .55 }} 100% {{ transform: scale(3.2); opacity: 0 }} }}
    @media (prefers-reduced-motion: reduce) {{ .ring {{ animation: none; opacity: 0 }} }}
  </style>
  <text x="{x0 - 16}" y="{y + 5}" text-anchor="end" font-family="{MONO}" font-size="18" fill="{t['text']}">{PUBLIC:02d}</text>
  <line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{t['faint']}" stroke-width="1.5" stroke-dasharray="2 6" stroke-linecap="round"/>
  <line x1="{x0}" y1="{y}" x2="{x:.1f}" y2="{y}" stroke="{t['accent']}" stroke-width="2" stroke-linecap="round"/>
  <circle class="ring" cx="{x:.1f}" cy="{y}" r="5" fill="none" stroke="{t['accent']}" stroke-width="1.5"/>
  <circle cx="{x:.1f}" cy="{y}" r="5" fill="{t['accent']}"/>
  <text x="{x1 + 14}" y="{y + 5}" font-family="{MONO}" font-size="18" fill="{t['muted']}">100</text>
  <text x="{x:.1f}" y="{y + 38}" font-family="{SERIF}" font-style="italic" font-size="19" fill="{t['muted']}">you are here</text>
</svg>
"""


def banner(t: dict) -> str:
    """Big 'N / 100' with a 10x10 grid, one cell per business."""
    cell, gap = 16, 6
    gx, gy = 1280 - 72 - (10 * cell + 9 * gap), (360 - (10 * cell + 9 * gap)) / 2
    cells = "".join(
        f'<rect x="{gx + (i % 10) * (cell + gap)}" y="{gy + (i // 10) * (cell + gap):.0f}" width="{cell}" height="{cell}" rx="4" '
        f'fill="{t["accent"] if i < PUBLIC else t["faint"]}"/>'
        for i in range(100)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 360" width="1280" height="360" role="img" aria-label="{PUBLIC} of 100 open-source businesses">
  <text x="72" y="86" font-family="{MONO}" font-size="20" letter-spacing="0.5" fill="{t['muted']}">@ilyaxxing</text>
  <text x="64" y="236" font-family="{SANS}" font-size="156" font-weight="700" letter-spacing="-6"><tspan fill="{t['accent']}">{PUBLIC}</tspan><tspan fill="{t['muted']}" font-weight="500"> / 100</tspan></text>
  <text x="72" y="290" font-family="{SANS}" font-size="28" font-weight="600" fill="{t['text']}">Open-Source Businesses</text>
  <text x="72" y="326" font-family="{MONO}" font-size="18" fill="{t['muted']}">clone → deploy → sell</text>
  {cells}
</svg>
"""


for name, t in THEMES.items():
    (OUT / f"banner-{name}.svg").write_text(banner(t), encoding="utf-8")
print("done:", sorted(p.name for p in OUT.iterdir()))
