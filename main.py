#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - Tuesday 24 November 2026.

A program that draws one 1024x1024 newspaper front page summing up the
world's news of Tuesday 24 November 2026, for the make.fun bounty
news-image-20261124, entered by @badd-airdrop2.

Pure Python 3 standard library only: no network, no fonts on disk, no
randomness, no clock. It draws with a hand-written 5x7 bitmap font and a
hand-written PNG encoder, and writes /output/entry.png. Running it twice
writes the same bytes.

Every story on the page happened or was first reported on Tuesday
24 November 2026, as the named outlets reported it. Stories that look
like 24 November news but are not are listed in the red DATE CHECK box
with their real dates, not presented as the day's news.
"""

import os
import struct
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 242, 231)
INK = (17, 17, 17)
BLACK = (10, 10, 10)
RED = (178, 34, 34)
DARKRED = (139, 0, 0)
NAVY = (27, 42, 74)
GOLD = (201, 162, 39)
TEAL = (15, 118, 110)
GREY = (107, 114, 128)
LIGHTGREY = (220, 214, 200)
WHITE = (255, 255, 255)
CREAM2 = (238, 231, 214)
SKY = (70, 110, 160)
NIGHT = (16, 24, 48)

# ---------------------------------------------------------------- 5x7 font
# Each glyph is 7 rows of 5 characters; '#' is ink, '.' is blank.
# All page text is uppercase, so only uppercase letters are needed.
FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
    ".": [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
    ",": [".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."],
    ":": [".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."],
    ";": [".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    "?": [".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."],
    "'": ["..#..", "..#..", ".#...", ".....", ".....", ".....", "....."],
    '"': [".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."],
    "-": [".....", ".....", ".....", "#####", ".....", ".....", "....."],
    "(": ["...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."],
    ")": [".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    "%": ["##..#", "##.#.", "...#.", "..#..", ".#...", "#.#.#", "#..##"],
    "$": ["..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."],
    "&": [".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    "=": [".....", ".....", "#####", ".....", "#####", ".....", "....."],
    "*": [".....", ".#.#.", "..#..", "#####", "..#..", ".#.#.", "....."],
    "#": ["#.#.#", "#.#.#", "#####", "#.#.#", "#####", "#.#.#", "#.#.#"],
    "_": [".....", ".....", ".....", ".....", ".....", ".....", "#####"],
}

UNKNOWN = ["#####", "#...#", "#.#.#", "#...#", "#####", ".....", "....."]


def text_width(text, scale):
    """Pixel width of text at a font scale (1 unit = 6 px per char)."""
    return len(text) * 6 * scale - scale


def wrap_text(text, scale, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            # A single word too long: hard-split it.
            while text_width(word, scale) > max_width:
                cut = max_width // (6 * scale)
                lines.append(word[:cut])
                word = word[cut:]
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * w * h)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def frame(self, x, y, w, h, color, t=1):
        self.rect(x, y, w, t, color)
        self.rect(x, y + h - t, w, t, color)
        self.rect(x, y, t, h, color)
        self.rect(x + w - t, y, t, h, color)

    def hline(self, x, y, w, color, t=1):
        self.rect(x, y, w, t, color)

    def vline(self, x, y, h, color, t=1):
        self.rect(x, y, t, h, color)

    def line(self, x0, y0, x1, y1, color):
        """Bresenham line."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            self.set(x, y, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)

    def ring(self, cx, cy, r, color, t=2):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if (r - t) ** 2 <= d <= r * r:
                    self.set(xx, yy, color)

    def triangle(self, x0, y0, x1, y1, x2, y2, color):
        minx, maxx = min(x0, x1, x2), max(x0, x1, x2)
        miny, maxy = min(y0, y1, y2), max(y0, y1, y2)
        d = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if d == 0:
            return
        for yy in range(miny, maxy + 1):
            for xx in range(minx, maxx + 1):
                a = ((y1 - y2) * (xx - x2) + (x2 - x1) * (yy - y2)) / d
                b = ((y2 - y0) * (xx - x2) + (x0 - x2) * (yy - y2)) / d
                c = 1 - a - b
                if 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1:
                    self.set(xx, yy, color)

    def text(self, x, y, s, scale, color):
        """Draw text; returns the x position after the last character."""
        cx = x
        for ch in s:
            glyph = FONT.get(ch, UNKNOWN)
            for row in range(7):
                for col in range(5):
                    if glyph[row][col] == "#":
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, color)
            cx += 6 * scale
        return cx

    def text_center(self, cx, y, s, scale, color):
        self.text(cx - text_width(s, scale) // 2, y, s, scale, color)

    def text_right(self, right, y, s, scale, color):
        self.text(right - text_width(s, scale), y, s, scale, color)

    def para(self, x, y, s, scale, color, max_width, leading=None):
        """Wrapped paragraph; returns y after the last line."""
        if leading is None:
            leading = 9 * scale
        for line in wrap_text(s, scale, max_width):
            self.text(x, y, line, scale, color)
            y += leading
        return y


# ---------------------------------------------------------------- PNG encoder
def png_bytes(canvas):
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)
        start = y * stride
        raw.extend(canvas.px[start:start + stride])
    data = zlib.compress(bytes(raw), 9)

    def chunk(kind, payload):
        out = struct.pack(">I", len(payload)) + kind + payload
        out += struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", data) + chunk(b"IEND", b""))


# ---------------------------------------------------------------- illustrations
def hero_riyadh(c, x, y, w, h):
    """Night skyline: the PIF Tower struck, a drone overhead."""
    c.rect(x, y, w, h, NIGHT)
    for sx, sy in [(12, 14), (40, 8), (70, 20), (110, 10), (150, 18),
                   (190, 8), (230, 16), (260, 10), (290, 20)]:
        c.set(x + sx % w, y + sy, GOLD)
        c.set(x + sx % w + 1, y + sy, GOLD)
    # Distant towers.
    for tx, th in [(8, 70), (48, 95), (250, 80), (288, 60)]:
        c.rect(x + tx, y + h - 24 - th, 26, th + 24, (38, 52, 86))
        for wy in range(6, th, 12):
            for wx in range(5, 22, 8):
                c.set(x + tx + wx, y + h - 24 - th + wy, GOLD)
    # The PIF Tower, tallest, centre. Height capped so the tower and
    # its antenna stay inside the art box (top edge y).
    tx, th = 120, 118
    c.rect(x + tx, y + h - 24 - th, 66, th + 24, (52, 70, 110))
    c.rect(x + tx + 28, y + h - 24 - th - 6, 10, 6, (52, 70, 110))
    for wy in range(8, th, 11):
        for wx in range(6, 60, 10):
            c.set(x + tx + wx, y + h - 24 - th + wy, GOLD)
    # Impact burst at the tower top.
    bx, by = x + tx + 33, y + h - 24 - th + 6
    c.circle(bx, by, 16, RED)
    c.circle(bx, by, 9, GOLD)
    for dx, dy in [(-24, -10), (24, -12), (-20, 12), (26, 10), (0, -26)]:
        c.line(bx, by, bx + dx, by + dy, RED)
    # Drone, upper right.
    dx, dy = x + w - 52, y + 26
    c.rect(dx, dy, 16, 6, INK)
    c.line(dx - 8, dy + 3, dx + 24, dy + 3, INK)
    c.circle(dx - 8, dy + 3, 3, INK)
    c.circle(dx + 24, dy + 3, 3, INK)
    c.line(dx + 4, dy + 6, dx + 12, dy + 14, GOLD)
    # Ground.
    c.rect(x, y + h - 24, w, 24, (24, 32, 56))


def hero_zaporizhzhia(c, x, y, w, h):
    """Apartment block hit overnight: smoke, broken corner, rescue."""
    c.rect(x, y, w, h, (196, 205, 214))
    c.rect(x, y + h - 30, w, 30, (120, 128, 138))
    # Block, left-centre.
    bx, by, bw, bh = x + 30, y + 34, 150, h - 64
    c.rect(bx, by, bw, bh, (148, 152, 158))
    c.rect(bx, by, bw, 10, (120, 124, 130))
    for row in range(5):
        for col in range(5):
            wx = bx + 12 + col * 28
            wy = by + 22 + row * 26
            lit = (row + col) % 3 == 0
            c.rect(wx, wy, 16, 18, GOLD if lit else (60, 64, 72))
    # Broken top-right corner.
    c.triangle(bx + bw - 52, by, bx + bw, by, bx + bw, by + 44, (196, 205, 214))
    c.triangle(bx + bw - 52, by, bx + bw, by + 44, bx + bw - 52, by + 44,
               (90, 94, 100))
    # Smoke.
    for sx, sy, sr in [(bx + bw - 30, by - 6, 12), (bx + bw - 8, by - 16, 15),
                       (bx + bw + 14, by - 26, 11)]:
        c.circle(sx, sy, sr, (110, 116, 124))
    # Second block, right.
    c.rect(x + 205, y + 70, 84, h - 100, (168, 172, 178))
    for row in range(3):
        for col in range(2):
            c.rect(x + 217 + col * 34, y + 84 + row * 28, 18, 18,
                   (60, 64, 72))
    # Rescuers on the ground, and a red-cross flag.
    for fx in (x + 60, x + 84):
        c.circle(fx, y + h - 40, 4, NAVY)
        c.rect(fx - 4, y + h - 35, 8, 14, NAVY)
    c.line(x + 268, y + h - 48, x + 268, y + h - 24, INK)
    c.rect(x + 268, y + h - 48, 22, 12, WHITE)
    c.rect(x + 274, y + h - 44, 10, 3, RED)
    c.rect(x + 278, y + h - 47, 3, 9, RED)


def hero_huawei(c, x, y, w, h):
    """Courthouse columns and the scales of justice."""
    c.rect(x, y, w, h, CREAM2)
    # Courthouse.
    cx, cy = x + w // 2, y + 18
    c.triangle(cx - 110, cy + 34, cx + 110, cy + 34, cx, cy, NAVY)
    c.rect(x + 42, cy + 34, w - 84, 8, NAVY)
    for i in range(5):
        px = x + 52 + i * 52
        c.rect(px, cy + 42, 14, 96, WHITE)
        c.frame(px, cy + 42, 14, 96, GREY)
    c.rect(x + 42, cy + 138, w - 84, 10, NAVY)
    # Scales, centre foreground.
    sx, sy = cx, y + h - 78
    c.rect(sx - 3, sy - 44, 6, 52, INK)
    c.rect(sx - 52, sy - 44, 104, 4, INK)
    c.line(sx - 52, sy - 40, sx - 78, sy - 8, INK)
    c.line(sx - 52, sy - 40, sx - 26, sy - 8, INK)
    c.line(sx + 52, sy - 40, sx + 26, sy - 8, INK)
    c.line(sx + 52, sy - 40, sx + 78, sy - 8, INK)
    c.triangle(sx - 88, sy - 8, sx - 16, sy - 8, sx - 52, sy + 12, GOLD)
    c.triangle(sx + 16, sy - 8, sx + 88, sy - 8, sx + 52, sy + 12, GOLD)
    c.rect(sx - 14, sy + 8, 28, 6, INK)
    # Gavel, lower right.
    gx, gy = x + w - 78, y + h - 44
    c.rect(gx, gy, 34, 12, (120, 72, 20))
    c.line(gx + 8, gy + 12, gx - 6, gy + 30, (120, 72, 20))
    c.line(gx + 9, gy + 12, gx - 5, gy + 30, (120, 72, 20))
    c.line(gx + 10, gy + 12, gx - 4, gy + 30, (120, 72, 20))


# ---------------------------------------------------------------- grid icons
def icon_trophy(c, x, y, s):
    c.rect(x + s // 3, y, s // 3, s // 2, GOLD)
    c.rect(x + s // 4, y + s // 2, s // 2, s // 6, GOLD)
    c.rect(x + s // 3, y + 2 * s // 3, s // 3, s // 6, GOLD)
    c.rect(x + s // 5, y + 5 * s // 6, 3 * s // 5, s // 6, GOLD)
    c.line(x, y + 2, x + s // 3, y + 6, GOLD)
    c.line(x + s, y + 2, x + 2 * s // 3, y + 6, GOLD)


def icon_ship(c, x, y, s):
    c.triangle(x, y + s // 2, x + s, y + s // 2, x + s // 2, y + s, NAVY)
    c.rect(x + s // 2 - 1, y, 2, s // 2, INK)
    c.rect(x + s // 2, y + 2, s // 3, s // 5, RED)
    c.line(x, y + s - 2, x + s, y + s - 2, SKY)
    c.line(x + 2, y + s - 5, x + s - 2, y + s - 5, SKY)


def icon_shield(c, x, y, s):
    c.rect(x + s // 4, y, s // 2, s // 2, RED)
    c.triangle(x + s // 4, y + s // 2, x + 3 * s // 4, y + s // 2,
               x + s // 2, y + s, RED)
    c.text(x + s // 2 - 3, y + 2, "7", 1, WHITE)


def icon_pill(c, x, y, s):
    c.rect(x + 2, y + s // 4, s - 4, s // 2, TEAL)
    c.rect(x + 2, y + s // 4, s // 2 - 1, s // 2, WHITE)
    c.frame(x + 2, y + s // 4, s - 4, s // 2, INK)
    c.text(x + s // 4, y + s // 4 + 1, "$", 1, TEAL)


def icon_heli(c, x, y, s):
    c.line(x, y + 2, x + s, y + 2, INK)
    c.circle(x + s // 2, y + s // 2, s // 4, GREY)
    c.rect(x + s // 2, y + s // 2 - 2, s // 2, 4, GREY)
    c.line(x + s // 4, y + 3 * s // 4, x + s // 2, y + s // 2, INK)
    c.circle(x + s // 3, y + 3 * s // 4, 3, INK)
    c.circle(x + 2 * s // 3, y + 3 * s // 4, 3, INK)


def icon_anchor(c, x, y, s):
    c.ring(x + s // 2, y + 4, 4, INK)
    c.line(x + s // 2, y + 8, x + s // 2, y + s - 4, INK)
    c.line(x + s // 4, y + s // 2, x + 3 * s // 4, y + s // 2, INK)
    c.line(x + 2, y + s - 8, x + s // 2, y + s - 2, INK)
    c.line(x + s - 2, y + s - 8, x + s // 2, y + s - 2, INK)


# ---------------------------------------------------------------- world map
# Coarse land mask: 28 rows (lat 90 to -90), each a list of (lo, hi)
# column ranges over 64 columns (lon -180 to 180). Drawn as dots.
LAND = [
    [(24, 26)],
    [(10, 18), (23, 27)],
    [(6, 20), (22, 27), (34, 36)],
    [(3, 22), (33, 36), (37, 58)],
    [(4, 22), (31, 31), (33, 36), (37, 60)],
    [(5, 24), (30, 38), (39, 58)],
    [(7, 24), (30, 38), (39, 55), (58, 58)],
    [(8, 24), (30, 37), (38, 54), (57, 58)],
    [(9, 24), (30, 38), (39, 44), (48, 55), (57, 57)],
    [(10, 16), (30, 40), (40, 45), (46, 48), (49, 55)],
    [(11, 15), (31, 41), (47, 49), (50, 53)],
    [(13, 16), (32, 42), (50, 53)],
    [(16, 20), (33, 42), (51, 54)],
    [(17, 22), (34, 41), (51, 56)],
    [(18, 23), (35, 40), (52, 57)],
    [(19, 24), (35, 40), (55, 59)],
    [(20, 25), (35, 39), (54, 60)],
    [(21, 25), (35, 39), (41, 42), (54, 60)],
    [(21, 25), (36, 38), (55, 59), (61, 62)],
    [(22, 24), (56, 58), (61, 61)],
    [(22, 24), (61, 61)],
    [(22, 23)],
    [], [], [], [], [], [],
]


def draw_map(c, x, y, w, h, pins):
    """Dotted world map; pins is a list of (number, lon, lat)."""
    step_x = w / 64.0
    step_y = h / 28.0
    for r, spans in enumerate(LAND):
        cy = int(y + (r + 0.5) * step_y)
        for lo, hi in spans:
            for col in range(lo, hi + 1):
                cx = int(x + (col + 0.5) * step_x)
                c.circle(cx, cy, 2, (150, 158, 168))
    for num, lon, lat in pins:
        px = int(x + (lon + 180.0) / 360.0 * w)
        py = int(y + (90.0 - lat) / 180.0 * h)
        c.circle(px, py, 7, RED)
        c.ring(px, py, 7, WHITE, 1)
        c.text(px - 3, py - 3, str(num), 1, WHITE)


# ---------------------------------------------------------------- stories
# Every item happened or was first reported on Tuesday 24 November 2026.
# (place, category, headline, summary, source, lon, lat)
HEROES = [
    ("RIYADH", "MIDDLE EAST",
     "HOUTHI DRONE HITS RIYADH TOWER",
     "Second strike in less than a week on the PIF Tower, the capital's tallest. 11 people wounded.",
     "REUTERS", 46.7, 24.7),
    ("ZAPORIZHZHIA", "EUROPE",
     "OVERNIGHT STRIKE HITS FLATS",
     "Russian attack kills 2 and wounds 40, including four children, in the south-eastern city.",
     "REUTERS", 35.2, 47.8),
    ("NEW YORK", "JUSTICE",
     "HUAWEI GUILTY ON 10 OF 12 COUNTS",
     "Brooklyn jury convicts the Chinese telecom giant of fraud and sanctions breaches.",
     "REUTERS - WSJ", -74.0, 40.7),
]

GRID = [
    ("DAKAR", "SPORT",
     "SENEGAL ARE CHAMPIONS AGAIN",
     "Top sports court restores the AFCON title, overturning the forfeit to Morocco.",
     "REUTERS - AP", -17.4, 14.7, icon_trophy),
    ("GULF OF FINLAND", "WAR",
     "ZELENSKYY CONFIRMS SHIP STRIKE",
     "President confirms Ukraine's drone strike on the Sparta II; he says it carried weapons.",
     "BLOOMBERG - REUTERS", 27.0, 59.5, icon_ship),
    ("GAZA CITY", "MIDDLE EAST",
     "HAMAS SECURITY CHIEF KILLED",
     "Israeli strike kills Naeem Abu Nahel and six others, including two police officers.",
     "REUTERS", 34.5, 31.5, icon_shield),
    ("PARIS", "BUSINESS",
     "SANOFI BUYS INSMED FOR $41BN",
     "French drugmaker agrees its biggest deal in years, at $175 a share, for lung medicines.",
     "REUTERS", 2.35, 48.85, icon_pill),
    ("ESKISEHIR", "ACCIDENT",
     "ARMY HELICOPTER CRASH KILLS 5",
     "Turkish Air Force AS-532 comes down on a training flight; cause not yet known.",
     "REUTERS", 30.5, 39.8, icon_heli),
    ("STRAIT OF HORMUZ", "SHIPPING",
     "IRAN SAYS 4 TANKERS HIT MINES",
     "Tehran reports explosions east of the strait; maritime centre says the claim is unverified.",
     "IRNA - JMIC", 56.5, 26.5, icon_anchor),
]

STATS = [
    ("11", "WOUNDED IN RIYADH TOWER STRIKE"),
    ("40", "WOUNDED IN ZAPORIZHZHIA"),
    ("10/12", "COUNTS: HUAWEI GUILTY"),
    ("$41BN", "SANOFI BUYS INSMED"),
    ("5", "KILLED IN TURKISH CRASH"),
]

# Stories that look like 24 November news but are not. Each carries its
# real date; none of them is presented as the day's news.
DATE_CHECK = [
    "ICJ: MYANMAR GENOCIDE RULING - 19 NOV",
    "COP31 ENDS WITH NO DEAL - 22 NOV",
    "NVIDIA REINSTATES HUANG - 23 NOV",
    "RUSSIA WARNS ESTONIA - 23 NOV",
    "RUTTE SPACE-DEFENCE VOW - 23 NOV",
    "UK WINS 2035 WOMEN'S WORLD CUP - 23 NOV",
    "SHENZHOU-24 LAUNCH - 25 NOV",
]

PINS = [(i + 1, lon, lat) for i, (_, _, _, _, _, lon, lat)
        in enumerate(HEROES)]
PINS += [(i + 4, lon, lat) for i, (_, _, _, _, _, lon, lat, _)
         in enumerate(GRID)]


# ---------------------------------------------------------------- layout
def draw_masthead(c):
    c.rect(0, 0, W, 108, BLACK)
    c.text(16, 16, "THE WORLD IN ONE DAY", 5, WHITE)
    c.text(16, 66, "ALL TIMES UTC - ONE DAY - ONE PAGE", 2, GOLD)
    c.text_right(1008, 12, "TUESDAY", 2, WHITE)
    c.text_right(1008, 34, "24 NOVEMBER", 3, WHITE)
    c.text_right(1008, 66, "2026", 3, RED)
    c.rect(0, 108, W, 4, RED)


def draw_region_strip(c):
    c.text_center(512, 118, "9 STORIES - MIDDLE EAST 3 - EUROPE 3 - "
                 "AFRICA 1 - AMERICAS 1 - ASIA 1", 2, NAVY)


def draw_timeline(c):
    y = 140
    c.text(12, y, "THE DAY IN UTC", 2, INK)
    c.text_right(1012, y, "RED DOTS MARK STORIES WITH A REPORTED TIME",
                 1, GREY)
    bx, bw = 12, 248
    blocks = [
        ("00-06 OVERNIGHT - STRIKE 2", 2),
        ("06-12 MORNING - DEAL 7, 06:43 UTC", 7),
        ("12-18 AFTERNOON", None),
        ("18-24 NIGHT - CRASH 8, 19:52 UTC", 8),
    ]
    for i, (lab, num) in enumerate(blocks):
        x0 = bx + i * bw
        c.rect(x0, y + 22, bw - 4, 18, CREAM2)
        c.frame(x0, y + 22, bw - 4, 18, GREY)
        tx = x0 + 6
        if num is not None:
            c.circle(x0 + 12, y + 31, 7, RED)
            c.text(x0 + 9, y + 28, str(num), 1, WHITE)
            tx = x0 + 24
        c.text(tx, y + 27, lab, 1, INK)


def draw_hero(c, x, y, w, h, num, art, place, cat, headline, summary,
              source):
    c.rect(x, y, w, h, WHITE)
    c.frame(x, y, w, h, INK, 2)
    art(c, x + 2, y + 2, w - 4, 148)
    c.rect(x + 2, y + 2, 24, 24, RED)
    c.text(x + 9, y + 8, str(num), 2, WHITE)
    ty = y + 158
    c.text(x + 10, ty, place + " - " + cat, 1, RED)
    ty += 14
    ty = c.para(x + 10, ty, headline, 2, INK, w - 20, leading=17)
    ty += 2
    ty = c.para(x + 10, ty, summary, 1, INK, w - 20, leading=10)
    c.text(x + 10, y + h - 16, source, 1, GREY)


def draw_grid_card(c, x, y, w, h, num, icon, place, cat, headline,
                   summary, source):
    c.rect(x, y, w, h, WHITE)
    c.frame(x, y, w, h, GREY)
    c.rect(x, y, 22, 22, RED)
    c.text(x + 7, y + 7, str(num), 1, WHITE)
    c.text(x + 30, y + 6, place + " - " + cat, 1, RED)
    icon(c, x + w - 32, y + 6, 24)
    ty = c.para(x + 10, y + 30, headline, 2, INK, w - 20, leading=17)
    ty = c.para(x + 10, ty + 2, summary, 1, INK, w - 20, leading=10)
    c.text(x + 10, y + h - 15, source, 1, GREY)


def draw_stats(c):
    y, h = 458, 62
    c.rect(0, y, W, h, NAVY)
    cw = W // 5
    for i, (num, label) in enumerate(STATS):
        x0 = i * cw
        if i:
            c.vline(x0, y + 8, h - 16, (90, 105, 140), 1)
        c.text_center(x0 + cw // 2, y + 8, num, 3, GOLD)
        c.text_center(x0 + cw // 2, y + 38, label, 1, WHITE)


def draw_map_and_datecheck(c):
    y, h = 792, 158
    # Map, left.
    c.text(12, y, "WHERE IT HAPPENED", 2, INK)
    draw_map(c, 12, y + 22, 600, h - 26, PINS)
    # Date check, right.
    dx, dw = 640, 372
    c.rect(dx, y, dw, h, WHITE)
    c.frame(dx, y, dw, h, RED, 2)
    c.rect(dx, y, dw, 26, RED)
    c.text(dx + 10, y + 6, "DATE CHECK", 2, WHITE)
    c.text_right(dx + dw - 10, y + 9, "EXCLUDED AS THE WRONG DAY", 1, WHITE)
    iy = y + 34
    for item in DATE_CHECK:
        c.text(dx + 10, iy, "X " + item, 1, DARKRED)
        iy += 16


def draw_footer(c):
    y = 962
    c.hline(12, y, W - 24, GREY, 1)
    c.text_center(512, y + 10,
                  "EVERY STORY ABOVE HAPPENED OR WAS FIRST REPORTED ON "
                  "TUESDAY 24 NOVEMBER 2026, AS THE NAMED OUTLETS "
                  "REPORTED IT.", 1, INK)
    c.text_center(512, y + 26,
                  "MAP AND DRAWINGS ARE ORIGINAL VECTOR ART.", 1, GREY)
    c.text_center(512, y + 42,
                  "SOURCES: REUTERS - BLOOMBERG - WSJ - AP - CNN - "
                  "AL JAZEERA - IRNA - JMIC", 1, GREY)


def build():
    c = Canvas(W, H, PAPER)
    draw_masthead(c)
    draw_region_strip(c)
    draw_timeline(c)
    arts = [hero_riyadh, hero_zaporizhzhia, hero_huawei]
    for i, (place, cat, headline, summary, source, _, _) in enumerate(HEROES):
        draw_hero(c, 12 + i * 336, 188, 328, 262, i + 1, arts[i],
                  place, cat, headline, summary, source)
    draw_stats(c)
    for i, (place, cat, headline, summary, source, _, _, icon) in \
            enumerate(GRID):
        gx = 12 + (i % 3) * 336
        gy = 528 + (i // 3) * 128
        draw_grid_card(c, gx, gy, 328, 120, i + 4, icon,
                       place, cat, headline, summary, source)
    draw_map_and_datecheck(c)
    draw_footer(c)
    return c


def main():
    canvas = build()
    data = png_bytes(canvas)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(outdir, exist_ok=True)
        path = os.path.join(outdir, "entry.png")
        with open(path, "wb") as f:
            f.write(data)
    except OSError:
        os.makedirs("out", exist_ok=True)
        path = os.path.join("out", "entry.png")
        with open(path, "wb") as f:
            f.write(data)
    print("wrote %s (%d bytes)" % (path, len(data)))


if __name__ == "__main__":
    main()
