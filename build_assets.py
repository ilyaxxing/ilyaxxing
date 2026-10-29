#!/usr/bin/env python3
"""Draws every image used in README.md (dark + light versions).

    python3 build_assets.py

When a new project goes public: add it to PROJECTS, re-run, commit.
"""
from pathlib import Path

# newest last; status is "live" or "in progress"
PROJECTS = [
    dict(n=1, name="Cash for Cars", line1="QR card on a windshield.", line2="Buyer gets the lead instantly.", status="live"),
    dict(n=2, name="Next", line1="", line2="", status="in progress"),
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
    <text x="{x + 32}" y="{y + 58}" font-family="{MONO}" font-size="24" fill="{t['muted']}">{"Latest" if p["status"] == "live" else "Next"}</text>
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
        cards += card(716, 124, p, t, front=False, opacity=0.9)
    cards += card(690, 190, front, t, front=True)


    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 576" width="1200" height="576" role="img" aria-label="Build it. Test it. Share it.">
  <style>
    .blink {{ animation: blink 1.8s ease-in-out infinite; }}
    @keyframes blink {{ 0%,100% {{ opacity: 1 }} 50% {{ opacity: .25 }} }}
    @media (prefers-reduced-motion: reduce) {{ .blink {{ animation: none; }} }}
  </style>
  <rect x="1" y="1" width="1198" height="574" rx="32" fill="{t['bg']}" stroke="{t['line']}" stroke-width="2"/>

  <text x="72" y="96" font-family="{MONO}" font-size="24" letter-spacing="1" fill="{t['muted']}">@ilyaxxing</text>
  <g font-family="{SANS}" font-size="84" font-weight="800" letter-spacing="-2.5">
    <text x="68" y="196" fill="{t['text']}">Build it.</text>
    <text x="68" y="290" fill="{t['text']}">Test it.</text>
    <text x="68" y="384" fill="{t['accent']}">Share it.</text>
  </g>
  <text x="72" y="456" font-family="{SANS}" font-size="29" fill="{t['muted']}">Real projects, tried on real people.</text>
  <text x="72" y="496" font-family="{SANS}" font-size="29" fill="{t['muted']}">The ones that work are open source.</text>

  {cards}

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
