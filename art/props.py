"""Pixel props for the banner. Each key maps to a colour in build_assets.py."""

DIAMOND = [
    "..OOOOO..",
    ".OCWCCcO.",
    "OCWCCCCcO",
    ".OCCCCcO.",
    "..OCCcO..",
    "...OcO...",
    "....O....",
]

SPARKLE = [
    "..W..",
    "..W..",
    "WWWWW",
    "..W..",
    "..W..",
]

assert all(len(r) == 9 for r in DIAMOND) and all(len(r) == 5 for r in SPARKLE)
