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
                 faint="#21262D", accent="#3FB950", accent_soft="#3FB95026", warm="#F0883E"),
    "light": dict(bg="#FFFFFF", line="#D0D7DE", card="#F6F8FA", text="#1F2328", muted="#59636E",
                  faint="#E1E6EB", accent="#1A7F37", accent_soft="#1A7F3720", warm="#BC4C00"),
}




import json
MINER = json.loads((Path(__file__).parent / "art" / "miner.json").read_text())


def miner(t: dict, x: int, y: int, u: int = 4) -> str:
    """Me, mining gold ore. Two frames swap, the rock shakes, sparks fly."""
    pal = MINER["palette"]

    def outlined(rows):
        """Add a 1-cell dark outline around every sprite, NES style."""
        h, w = len(rows), max(len(r) for r in rows)
        grid = [list(r.ljust(w, ".")) for r in rows]
        out = [row[:] for row in grid]
        for r in range(h):
            for c in range(w):
                if grid[r][c] != ".":
                    continue
                if any(0 <= r + dr < h and 0 <= c + dc < w and grid[r + dr][c + dc] not in ".O"
                       for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    out[r][c] = "O"
        return ["".join(row) for row in out]

    pal = {**pal, "O": "#101216"}

    def pixels(rows, r0=0, c0=0):
        rows = outlined(rows)
        return "".join(f'<rect x="{x + (c0 + c) * u}" y="{y + (r0 + r) * u}" width="{u}" height="{u}" fill="{pal[ch]}"/>'
                       for r, row in enumerate(rows) for c, ch in enumerate(row) if ch != ".")
    rr, rc = MINER["rock_at"]
    hx, hy = x + rc * u, y + (rr + 3) * u          # where the pick lands
    sparks = "".join(
        f'<rect class="spark s{k}" x="{hx}" y="{hy}" width="{u}" height="{u}" fill="{c}"/>'
        for k, c in enumerate(["#FFD43B", "#FFF3B0", "#FFD43B", "#D99A00"]))
    floor = y + MINER["h"] * u
    return f"""<g shape-rendering="crispEdges">
    <rect x="{x + 4 * u}" y="{floor}" width="{(MINER['w'] - 2) * u}" height="4" fill="{t['line']}"/>
    <g class="rock">{pixels(MINER["rock"], rr, rc)}</g>
    <g class="f0">{pixels(MINER["frames"][0])}</g>
    <g class="f1">{pixels(MINER["frames"][1])}</g>
    {sparks}
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

    # stacked cards on the right: the one in progress peeks out behind
    cards = ""
    for p in behind:
        cards += card(716, 50, p, t, front=False, opacity=0.9)
    cards += card(690, 112, front, t, front=True)


    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" width="1200" height="600" role="img" aria-label="Clone it. Launch it. Get paid.">
  <style>
    .blink {{ animation: blink 1.8s ease-in-out infinite; }}
    @keyframes blink {{ 0%,100% {{ opacity: 1 }} 50% {{ opacity: .25 }} }}
    .f0 {{ animation: f0 1.1s steps(1) infinite; }}
    .f1 {{ animation: f1 1.1s steps(1) infinite; }}
    @keyframes f0 {{ 0% {{ opacity: 1 }} 55% {{ opacity: 0 }} }}
    @keyframes f1 {{ 0% {{ opacity: 0 }} 55% {{ opacity: 1 }} }}
    .rock {{ animation: shake 1.1s infinite; }}
    @keyframes shake {{ 0%,55% {{ transform: translateX(0) }} 60% {{ transform: translateX(3px) }} 66% {{ transform: translateX(-2px) }} 72%,100% {{ transform: translateX(0) }} }}
    .spark {{ opacity: 0; animation: spark 1.1s ease-out infinite; }}
    @keyframes spark {{ 0%,54% {{ opacity: 0; transform: translate(0,0) }} 56% {{ opacity: 1; transform: translate(0,0) }} 95% {{ opacity: 0; transform: translate(var(--dx), var(--dy)) }} 100% {{ opacity: 0 }} }}
    .s0 {{ --dx: -26px; --dy: -48px; }} .s1 {{ --dx: 8px; --dy: -60px; }} .s2 {{ --dx: -42px; --dy: -20px; }} .s3 {{ --dx: 24px; --dy: -34px; }}
    @media (prefers-reduced-motion: reduce) {{ .blink, .f0, .f1, .rock, .spark {{ animation: none; }} .f1, .spark {{ opacity: 0; }} }}
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

  {cards}

  <text x="696" y="498" font-family="{MONO}" font-size="20" fill="{t['muted']}">grindin' on</text>
  <text x="696" y="526" font-family="{MONO}" font-size="20" fill="{t['muted']}">the next one<tspan class="blink">_</tspan></text>
  {miner(t, 846, 380, 6)}

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
