"""Pixel props for the banner: a mystery block and a coin. Keys -> colors are
resolved per theme in build_assets.py ("A" family follows the accent)."""

BLOCK = [
    "..OOOOOOOOOO..",
    ".OLLLLLLLLLLO.",
    "OLLAAAAAAAAADO",
    "OLAAAAWWWAAADO",
    "OLAAAWAAAWAADO",
    "OLAAAAAAAWAADO",
    "OLAAAAAAWAAADO",
    "OLAAAAAWAAAADO",
    "OLAAAAAWAAAADO",
    "OLAAAAAAAAAADO",
    "OLAAAAAWAAAADO",
    "OLAAAAAAAAAADO",
    ".ODDDDDDDDDDO.",
    "..OOOOOOOOOO..",
]

COIN = [
    "..OOOO..",
    ".OYYYYO.",
    "OYYZYYYO",
    "OYZYYYyO",
    "OYZYYYyO",
    "OYZYYYyO",
    "OYYYYyyO",
    ".OyyyyO.",
    "..OOOO..",
]

assert all(len(r) == 14 for r in BLOCK) and all(len(r) == 8 for r in COIN)
