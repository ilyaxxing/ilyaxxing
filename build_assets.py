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
                 hair="#5A4030", eyes="#0E1116", hoodie="#2EA043", hoodie_dark="#238636", lid="#C9D1D9", logo="#FFFFFF"),
    "light": dict(bg="#FFFFFF", line="#D0D7DE", card="#F6F8FA", text="#1F2328", muted="#59636E",
                  faint="#E1E6EB", accent="#1A7F37", accent_soft="#1A7F3720", warm="#BC4C00",
                  hair="#3B2A1F", eyes="#1F2328", hoodie="#2DA44E", hoodie_dark="#1A7F37", lid="#8C959F", logo="#FFFFFF"),
}



# pixel me at a laptop, 20 x 21 cells
ME = [
    "......HHHHHHHH......",
    ".....HHHHHHHHHH.....",
    "....HHHHHHHHHHHH....",
    "....HHHHHHHHHHHH....",
    "....HHSSSSSSSSHH....",
    "....HSSSSSSSSSSH....",
    "....SSEESSSSEESS....",
    "....SSEESSSSEESS....",
    "....SSSSSSSSSSSS....",
    "....SSSSSMMSSSSS....",
    ".....SSSSSSSSSS.....",
    "........SSSS........",
    "....DDDDWDDWDDDD....",
    "..DDDDDDWDDWDDDDDD..",
    ".DDDDDDDWDDWDDDDDDD.",
    ".AAALLLLLLLLLLLLBBB.",
    ".AAALLLLLLLLLLLLBBB.",
    ".AAALLLLLGGLLLLLBBB.",
    ".AAALLLLLGGLLLLLBBB.",
    ".AAALLLLLLLLLLLLBBB.",
    ".aaaLLLLLLLLLLLLbbb.",
]
assert all(len(r) == 20 for r in ME)


def me(t: dict, x: int, y: int, u: int = 6) -> str:
    """Me, typing away. Eyes blink, head nods, hands tap, code floats up."""
    pal = {"H": t["hair"], "S": "#E8B98F", "M": "#B9785A", "E": t["eyes"], "D": t["hoodie"],
           "W": "#F0F6FC", "A": t["hoodie"], "B": t["hoodie"], "a": t["hoodie_dark"], "b": t["hoodie_dark"],
           "L": t["lid"], "G": t["logo"]}

    def px(rows, keys, cls=""):
        out = "".join(f'<rect x="{x + c * u}" y="{y + r * u}" width="{u}" height="{u}" fill="{pal[ch]}"/>'
                      for r in rows for c, ch in enumerate(ME[r]) if ch in keys)
        return f'<g class="{cls}">{out}</g>' if cls else out

    head = range(0, 12)
    body = range(12, len(ME))
    floor = y + len(ME) * u
    cx = x + 10 * u
    bits = "".join(
        f'<text class="bit b{k}" x="{bx}" y="{y + 15 * u}" font-family="{MONO}" font-size="16" fill="{c}">{s}</text>'
        for k, (bx, s, c) in enumerate([(cx + 70, "{ }", t["accent"]), (cx - 110, "&lt;/&gt;", t["muted"]), (cx + 82, "✓", t["accent"])]))
    return f"""<g shape-rendering="crispEdges">
    {bits}
    <g class="nod">{px(head, "HSM")}{px(head, "E", "eyes")}</g>
    {px(body, "DWL")}
    {px(body, "Aa", "tapL")}{px(body, "Bb", "tapR")}
    {px(body, "G", "logo")}
    <rect x="{x - 24}" y="{floor}" width="{20 * u + 48}" height="4" fill="{t['line']}"/>
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
        cards += card(716, 84, p, t, front=False, opacity=0.9)
    cards += card(690, 150, front, t, front=True)


    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" width="1200" height="600" role="img" aria-label="Clone it. Launch it. Get paid.">
  <style>
    .blink {{ animation: blink 1.8s ease-in-out infinite; }}
    @keyframes blink {{ 0%,100% {{ opacity: 1 }} 50% {{ opacity: .25 }} }}
    .tapL {{ animation: tap .36s ease-in-out infinite; }}
    .tapR {{ animation: tap .36s ease-in-out .18s infinite; }}
    @keyframes tap {{ 0%,100% {{ transform: translateY(0) }} 50% {{ transform: translateY(3px) }} }}
    .nod {{ animation: nod 2.2s ease-in-out infinite; }}
    @keyframes nod {{ 0%,100% {{ transform: translateY(0) }} 50% {{ transform: translateY(2px) }} }}
    .eyes {{ transform-box: fill-box; transform-origin: center; animation: wink 3.6s infinite; }}
    @keyframes wink {{ 0%,92%,100% {{ transform: scaleY(1) }} 95% {{ transform: scaleY(.1) }} }}
    .logo {{ animation: glow 2.4s ease-in-out infinite; }}
    @keyframes glow {{ 0%,100% {{ opacity: 1 }} 50% {{ opacity: .35 }} }}
    .bit {{ opacity: 0; animation: rise 3.6s ease-out infinite; }}
    .b1 {{ animation-delay: 1.2s; }} .b2 {{ animation-delay: 2.4s; }}
    @keyframes rise {{ 0% {{ opacity: 0; transform: translateY(0) }} 15% {{ opacity: 1 }} 100% {{ opacity: 0; transform: translateY(-70px) }} }}
    @media (prefers-reduced-motion: reduce) {{ .blink, .tapL, .tapR, .nod, .eyes, .logo, .bit {{ animation: none; }} .bit {{ opacity: 0; }} }}
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

  <text x="700" y="490" font-family="{MONO}" font-size="19" fill="{t['muted']}">cookin' the</text>
  <text x="700" y="516" font-family="{MONO}" font-size="19" fill="{t['muted']}">next one<tspan class="blink">_</tspan></text>
  {me(t, 966, 404, 7)}

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
