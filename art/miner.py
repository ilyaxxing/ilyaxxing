"""Hand-built 8-bit miner sprite (me), 2 frames. Writes miner.json (+ a preview png)."""
import json
from pathlib import Path
from PIL import Image

OUT = Path(__file__).parent
W, H = 44, 30

PAL = {
    "H": "#7A4B2A", "h": "#4E2F1B",              # hair
    "S": "#EDBE93", "s": "#C98F66",              # skin
    "B": "#3E2617",                              # beard
    "E": "#141414",                              # eye
    "C": "#F4EEE2", "c": "#D6CCBA",              # cream hoodie
    "V": "#BAC4CE", "v": "#8794A1",              # grey vest
    "P": "#25282E",                              # pants
    "W": "#FFFFFF", "w": "#B8C0C8",              # sneakers
    "K": "#C3CCD5", "k": "#7B8590",              # pickaxe head
    "T": "#9A6233",                              # handle
    "R": "#8A9099", "r": "#5E646D",              # rock
    "G": "#FFD43B", "g": "#D99A00",              # gold
}

ROCK = [
    "....rrRRrr....",
    "..rRRRRRRRRr..",
    ".rRRGGRRRRRRr.",
    "rRRRGgRRRgGRRr",
    "RRRRRRRRRGgRRR",
    "RRGGRRRRRRRRRr",
    "RRgGRRRRGGRRRr",
    "rRRRRRRRgGRRrr",
    "rRRRRGGRRRRRrr",
    ".rrRRgGRRRRrr.",
    "..rrrrrrrrrr..",
]
ROCK_AT = (19, 29)

BODY = [
    # 0         1         2
    # 012345678901234567890123456789
    "..............................",  # 0
    "..............................",  # 1
    "..............................",  # 2
    "..............................",  # 3
    "..........hHHHH...............",  # 4
    ".........hHHHHHHH.............",  # 5
    "........hHHHHHHHHH............",  # 6
    "........hHHSSSSSSH............",  # 7
    "........hHSSSSESSS............",  # 8
    "........hHSSSSSSSSS...........",  # 9
    ".........hBBBBBBBS............",  # 10
    ".........BBBBBBBB.............",  # 11
    "........CCCBBBBBC.............",  # 12
    ".......CcVVVVVVVCC............",  # 13
    ".......CVVVVVVVVVC............",  # 14
    ".......CVVVVVvVVVC............",  # 15
    ".......CVVVVVvVVVC............",  # 16
    ".......CVVVVVvVVVC............",  # 17
    "........VVVVVvVVV.............",  # 18
    "........cCCCCCCCc.............",  # 19
    "........PPPPPPPPP.............",  # 20
    "........PPPP.PPPP.............",  # 21
    ".......PPPP...PPPP............",  # 22
    ".......PPP.....PPP............",  # 23
    "......PPP.......PPP...........",  # 24
    "......WWWW......WWWW..........",  # 25
    "......wwww......wwww..........",  # 26
]
BODY = ["." * W] * 3 + [r + "." * 14 for r in BODY]
assert all(len(r) == W for r in BODY) and len(BODY) == H, (len(BODY), {len(r) for r in BODY})


def put(g, r, c, ch):
    if 0 <= r < H and 0 <= c < W:
        g[r][c] = ch


def line(g, r0, c0, r1, c1, ch):
    dr, dc = abs(r1 - r0), abs(c1 - c0)
    sr, sc = (1 if r1 > r0 else -1), (1 if c1 > c0 else -1)
    err = dc - dr
    while True:
        put(g, r0, c0, ch)
        if (r0, c0) == (r1, c1):
            break
        e2 = 2 * err
        if e2 > -dr:
            err -= dr
            c0 += sc
        if e2 < dc:
            err += dc
            r0 += dr and sr or 0


def hair(g):
    for r, c in [(6, 11), (6, 13), (6, 15)]:
        put(g, r, c, "H")
    return g


def frame_up():
    g = hair([list(r) for r in BODY])
    # arms raised: sleeves from shoulder up to hands above the head
    for r in range(7, 16):
        put(g, r, 17, "C"); put(g, r, 18, "c" if r > 11 else "C")
    put(g, 16, 16, "C"); put(g, 16, 17, "C")
    for r, c in [(5, 17), (5, 18), (6, 17), (6, 18)]:
        put(g, r, c, "S")
    # handle goes back over the head
    line(g, 5, 16, 1, 9, "T")
    # pick head: a curved bar across the end of the handle
    for r, c, ch in [(0, 12, "k"), (0, 11, "K"), (0, 10, "K"), (1, 10, "K"), (1, 9, "K"), (1, 8, "K"), (2, 9, "K"), (2, 8, "K"), (2, 7, "K"),
                     (3, 8, "K"), (3, 7, "K"), (4, 7, "k"), (4, 6, "k"), (5, 6, "k")]:
        put(g, r, c, ch)
    return g


def frame_down():
    g = hair([list(r) for r in BODY])
    for r, c in [(16, 17), (17, 17), (17, 18), (18, 18), (18, 19), (19, 19), (19, 20), (20, 20)]:
        put(g, r, c, "C")
    for r, c in [(17, 19), (18, 20)]:
        put(g, r, c, "c")
    for r, c in [(20, 21), (20, 22), (21, 21), (21, 22)]:
        put(g, r, c, "S")
    line(g, 20, 22, 23, 27, "T")
    for r, c, ch in [(18, 27, "k"), (19, 27, "K"), (19, 28, "K"), (20, 27, "K"), (20, 28, "K"), (21, 28, "K"), (22, 28, "K"),
                     (23, 28, "K"), (24, 28, "K"), (24, 29, "k"), (25, 28, "k"), (25, 29, "k")]:
        put(g, r, c, ch)
    return g


def with_rock(g):
    r0, c0 = ROCK_AT
    for dr, row in enumerate(ROCK):
        for dc, ch in enumerate(row):
            if ch != ".":
                put(g, r0 + dr, c0 + dc, ch)
    return g


frames = [["".join(r) for r in frame_up()], ["".join(r) for r in frame_down()]]
preview_frames = [["".join(r) for r in with_rock(frame_up())], ["".join(r) for r in with_rock(frame_down())]]
json.dump({"w": W, "h": H, "palette": PAL, "frames": frames, "rock": ROCK, "rock_at": ROCK_AT}, open(OUT / "miner.json", "w"), indent=1)

S = 12
img = Image.new("RGB", (W * S * 2 + 40, H * S), (14, 17, 22))
px = img.load()
for f, rows in enumerate(preview_frames):
    ox = f * (W * S + 40)
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == ".":
                continue
            col = tuple(int(PAL[ch][i:i + 2], 16) for i in (1, 3, 5))
            for dy in range(S):
                for dx in range(S):
                    px[ox + c * S + dx, r * S + dy] = col
img.save(OUT / "miner_preview.png")
print("ok")
