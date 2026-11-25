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
    tx, th = 120, 96
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


def hero_huawei(c, x, y, w, h):
    """Courthouse columns and the scales of justice."""
    c.rect(x, y, w, h, CREAM2)
    # Courthouse.
    cx, cy = x + w // 2, y + 14
    c.triangle(cx - 110, cy + 28, cx + 110, cy + 28, cx, cy, NAVY)
    c.rect(x + 42, cy + 28, w - 84, 6, NAVY)
    for i in range(5):
        px = x + 52 + i * 52
        c.rect(px, cy + 34, 14, 72, WHITE)
        c.frame(px, cy + 34, 14, 72, GREY)
    c.rect(x + 42, cy + 106, w - 84, 8, NAVY)
    # Scales, centre foreground.
    sx, sy = cx, y + h - 58
    c.rect(sx - 3, sy - 36, 6, 44, INK)
    c.rect(sx - 52, sy - 36, 104, 4, INK)
    c.line(sx - 52, sy - 32, sx - 78, sy - 6, INK)
    c.line(sx - 52, sy - 32, sx - 26, sy - 6, INK)
    c.line(sx + 52, sy - 32, sx + 26, sy - 6, INK)
    c.line(sx + 52, sy - 32, sx + 78, sy - 6, INK)
    c.triangle(sx - 88, sy - 6, sx - 16, sy - 6, sx - 52, sy + 10, GOLD)
    c.triangle(sx + 16, sy - 6, sx + 88, sy - 6, sx + 52, sy + 10, GOLD)
    c.rect(sx - 14, sy + 6, 28, 6, INK)
    # Gavel, lower right.
    gx, gy = x + w - 78, y + h - 30
    c.rect(gx, gy, 34, 12, (120, 72, 20))
    c.line(gx + 8, gy + 12, gx - 6, gy + 28, (120, 72, 20))
    c.line(gx + 9, gy + 12, gx - 5, gy + 28, (120, 72, 20))
    c.line(gx + 10, gy + 12, gx - 4, gy + 28, (120, 72, 20))


def hero_dronewar(c, x, y, w, h):
    """Night schematic: a swarm over Russia, Moscow marked, AWACS above."""
    c.rect(x, y, w, h, NIGHT)
    for sx, sy in [(16, 12), (52, 20), (96, 10), (140, 18), (180, 8),
                   (220, 16), (260, 10), (296, 18)]:
        c.set(x + sx % w, y + sy, GOLD)
        c.set(x + sx % w + 1, y + sy, GOLD)
    # Landmass, centre.
    c.rect(x + 60, y + 34, 190, 56, (128, 116, 82))
    c.rect(x + 30, y + 52, 60, 38, (128, 116, 82))
    c.rect(x + 230, y + 52, 62, 38, (128, 116, 82))
    # Sea, bottom.
    c.rect(x, y + h - 30, w, 30, (30, 48, 84))
    # Drone swarm: white dots with short trails.
    for dx, dy in [(70, 24), (100, 30), (130, 22), (160, 32), (190, 24),
                   (220, 30), (250, 22), (280, 30), (85, 44), (150, 46),
                   (215, 46), (265, 44)]:
        c.line(x + dx - 8, y + dy, x + dx, y + dy, WHITE)
        c.circle(x + dx, y + dy, 3, WHITE)
    # Moscow, marked.
    mx, my = x + 208, y + 62
    c.circle(mx, my, 5, WHITE)
    c.ring(mx, my, 10, RED, 2)
    c.text(mx + 14, my - 4, "MOSCOW", 1, WHITE)
    # Poland, left edge.
    c.rect(x + 8, y + 62, 18, 6, WHITE)
    c.rect(x + 8, y + 68, 18, 6, RED)
    c.text(x + 8, y + 78, "POLAND", 1, WHITE)
    # AWACS plane, upper right.
    ax, ay = x + w - 66, y + 58
    c.rect(ax, ay, 26, 6, WHITE)
    c.line(ax + 6, ay + 6, ax + 20, ay - 6, WHITE)
    c.line(ax + 6, ay + 6, ax + 20, ay + 14, WHITE)
    c.text(ax - 4, ay + 18, "AWACS", 1, WHITE)
    # Big 699 badge, bottom left.
    c.rect(x + 10, y + h - 40, 118, 28, RED)
    c.text(x + 18, y + h - 34, "699", 3, WHITE)
    c.text(x + 74, y + h - 28, "DOWNED", 1, WHITE)


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


def icon_oil(c, x, y, s):
    """Oil derrick: two legs, a crossbar and a crown."""
    c.line(x + 4, y + s, x + s // 2 - 2, y + 2, INK)
    c.line(x + s - 4, y + s, x + s // 2 + 2, y + 2, INK)
    c.line(x + 6, y + s - 8, x + s - 6, y + s - 8, INK)
    c.rect(x + s // 2 - 5, y, 10, 6, INK)


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
# Badge: REPORTED = wires, OFFICIAL = on the record, CLAIM = one side says.
# (place, category, headline, summary, source, lon, lat, badge)
HEROES = [
    ("MOSCOW", "WAR",
     "RUSSIA SAYS 699 DRONES DOWNED",
     "Overnight barrage, 355 aimed at Moscow; a drone strays into Poland. Zaporizhzhia strike kills 2.",
     "REUTERS - AL JAZEERA", 37.6, 55.8, "REPORTED"),
    ("RIYADH", "MIDDLE EAST",
     "SECOND DRONE HITS RIYADH TOWER",
     "Saudi blames a Houthi drone for the strike on the PIF Tower, the capital's tallest. 11 people wounded.",
     "REUTERS", 46.7, 24.7, "REPORTED"),
    ("NEW YORK", "JUSTICE",
     "HUAWEI GUILTY ON 10 OF 12 COUNTS",
     "Brooklyn jury convicts the Chinese telecom giant of fraud and sanctions breaches.",
     "REUTERS - WSJ", -74.0, 40.7, "OFFICIAL"),
]

GRID = [
    ("DAKAR", "SPORT",
     "SENEGAL ARE CHAMPIONS AGAIN",
     "Top sports court restores the AFCON title, overturning the forfeit to Morocco.",
     "REUTERS - AP", -17.4, 14.7, icon_trophy, "REPORTED"),
    ("GULF OF FINLAND", "WAR",
     "ZELENSKYY CONFIRMS SHIP STRIKE",
     "President confirms Ukraine's drone strike on the Sparta II; he says it carried weapons.",
     "BLOOMBERG - REUTERS", 27.0, 59.5, icon_ship, "REPORTED"),
    ("GAZA CITY", "MIDDLE EAST",
     "HAMAS SECURITY CHIEF KILLED",
     "Israeli strike kills Naeem Abu Nahel and six others, including two police officers.",
     "REUTERS", 34.5, 31.5, icon_shield, "REPORTED"),
    ("PARIS", "BUSINESS",
     "SANOFI BUYS INSMED FOR $41BN",
     "French drugmaker agrees its biggest deal in years, at $175 a share, for lung medicines.",
     "REUTERS", 2.35, 48.85, icon_pill, "OFFICIAL"),
    ("KUALA LUMPUR", "ASIA",
     "MALAYSIA TO SEND 6,803 BACK TO MYANMAR",
     "Anwar tells parliament 6,803 Myanmar nationals will go back, 1,500 by ship and 5,303 by air.",
     "REUTERS", 101.7, 3.1, icon_anchor, "OFFICIAL"),
    ("BAGHDAD", "MIDDLE EAST",
     "BAGHDAD SEIZES KURDISH OILFIELDS",
     "PM puts fields in Kirkuk, Diyala, Salahuddin and Nineveh under the federal Oil Ministry.",
     "AL JAZEERA - REUTERS", 44.4, 33.3, icon_oil, "REPORTED"),
]

# One-line stories, numbers 10-30. Each is "PLACE - HEADLINE".
ALSO = [
    "ESKISEHIR - ARMY HELICOPTER CRASH KILLS 5",
    "HORMUZ - IRAN SAYS 4TH TANKER HIT MINE (CLAIM)",
    "HANOI - RESTAURANT BLAST KILLS 6",
    "DHAKA - HASINA TO FLY HOME 16 DEC",
    "NEW YORK - UN: 47,000 WOMEN KILLED BY PARTNERS",
    "ULLEUNG - RUSSIAN JET TRIGGERS 3-MIN ALERT",
    "BOUGAINVILLE - VOTE ON NATIONHOOD BEGINS",
    "TAPLEJUNG - QUAKE M5.6, NO CASUALTIES",
    "CIKANDE - FACTORY-FIRE TOLL RISES TO 26",
    "HONIARA - SOLOMONS ENDS CHINA PACT",
    "BERLIN - WORLD CHESS MATCH OPENS",
    "NEW YORK - UN DEBATES AI AND WAR'S FUTURE",
    "BRUSSELS - EU CAPS CHINESE HYBRID CARS AT 350K",
    "MEXICO CITY - MEXICO TO TRY \"EL CHAPO ISIDRO\"",
    "VILLAVICENCIO - CAR BOMB AT GOVERNOR'S OFFICE",
    "WASHINGTON - MEGASPEED BLACKLISTED IN NVIDIA CASE",
    "PENNSYLVANIA - 9TH US MEASLES DEATH THIS YEAR",
    "CHILE - MOST DISTANT BLACK HOLE FOUND",
    "JAKARTA - INDONESIA NAMES TWO VP CANDIDATES",
    "BEIJING - OFFICIAL SENTENCED TO DEATH FOR SPYING",
    "LISBON - PORTUGAL BUDGET VOTE, 2,864 AMENDMENTS",
]

STATS = [
    ("699", "DRONES DOWNED, RUSSIA SAYS"),
    ("11", "WOUNDED IN RIYADH STRIKE"),
    ("10/12", "COUNTS: HUAWEI GUILTY"),
    ("$41BN", "SANOFI BUYS INSMED"),
    ("6,803", "MYANMAR NATIONALS TO RETURN"),
    ("26", "DEAD IN CIKANDE FIRE"),
]

# Stories that look like 24 November news but are not. Each carries its
# real date; none of them is presented as the day's news.
DATE_CHECK = [
    "ICJ MYANMAR RULING - 19 NOV",
    "COP31 ENDS WITH NO DEAL - 22 NOV",
    "VERSTAPPEN WINS LAS VEGAS GP - 22 NOV",
    "NVIDIA REINSTATES HUANG - 23 NOV",
    "RUSSIA WARNS ESTONIA - 23 NOV",
    "RUTTE SPACE-DEFENCE VOW - 23 NOV",
    "UK WINS 2035 WOMEN'S CUP - 23 NOV",
    "YEMEN BUS STRIKE IN LAHJ - 23 NOV",
    "GUTERRES AI CALL IN BARBADOS - 23 NOV",
    "DENMARK 'GHETTO LAW' RULING - 23 NOV",
    "EU 22ND SANCTIONS - 23 NOV",
    "SHENZHOU-24 LAUNCH - 25 NOV",
]

# Numbered map pins: the 13 most locatable stories.
PINS = [
    (1, 37.6, 55.8), (2, 46.7, 24.7), (3, -74.0, 40.7), (4, -17.4, 14.7),
    (5, 27.0, 59.5), (6, 34.5, 31.5), (7, 2.35, 48.85), (8, 101.7, 3.1),
    (9, 44.4, 33.3), (10, 30.5, 39.8), (11, 56.5, 26.5), (12, 105.8, 21.0),
    (13, 90.4, 23.8),
]


# ---------------------------------------------------------------- layout
def draw_masthead(c):
    c.rect(0, 0, W, 108, BLACK)
    c.text(16, 16, "THE WORLD IN ONE DAY", 5, WHITE)
    c.text(16, 66, "ALL TIMES UTC - ONE DAY - ONE PAGE - 30 STORIES", 2, GOLD)
    c.text_right(1008, 12, "TUESDAY", 2, WHITE)
    c.text_right(1008, 34, "24 NOVEMBER", 3, WHITE)
    c.text_right(1008, 66, "2026", 3, RED)
    c.rect(0, 108, W, 4, RED)


def draw_region_strip(c):
    c.text_center(512, 118, "EUROPE 7 - MIDDLE EAST 4 - ASIA 8 - "
                 "AFRICA 1 - AMERICAS 7 - OCEANIA 2 - GLOBAL 1", 2, NAVY)


def draw_timeline(c):
    y = 140
    c.text(12, y, "THE DAY IN UTC", 2, INK)
    c.text_right(1012, y, "RED DOTS MARK STORIES WITH A REPORTED TIME",
                 1, GREY)
    bx, bw = 12, 248
    blocks = [
        ("00-06 OVERNIGHT - DRONE WAR 1", 1),
        ("06-12 MORNING - DEAL 7, 06:43 UTC", 7),
        ("12-18 AFTERNOON", None),
        ("18-24 NIGHT - CRASH 10, 19:52 UTC", 10),
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


BADGE_COLORS = {"REPORTED": (70, 90, 120), "OFFICIAL": (46, 125, 50),
                "CLAIM": (178, 34, 34)}


def draw_badge(c, right, y, text):
    """Small filled badge, right-aligned at x=right, top y."""
    bw = len(text) * 5 + 10
    c.rect(right - bw, y, bw, 12, BADGE_COLORS[text])
    c.text(right - bw + 5, y + 2, text, 1, WHITE)


def draw_hero(c, x, y, w, h, num, art, place, cat, headline, summary,
              source, badge):
    c.rect(x, y, w, h, WHITE)
    c.frame(x, y, w, h, INK, 2)
    art(c, x + 2, y + 2, w - 4, 130)
    c.rect(x + 2, y + 2, 24, 24, RED)
    c.text(x + 9, y + 8, str(num), 2, WHITE)
    ty = y + 138
    c.text(x + 10, ty, place + " - " + cat, 1, RED)
    draw_badge(c, x + w - 10, ty - 2, badge)
    ty += 14
    ty = c.para(x + 10, ty, headline, 2, INK, w - 20, leading=17)
    ty += 2
    ty = c.para(x + 10, ty, summary, 1, INK, w - 20, leading=10)
    c.text(x + 10, y + h - 14, source, 1, GREY)


def draw_grid_card(c, x, y, w, h, num, icon, place, cat, headline,
                   summary, source, badge):
    c.rect(x, y, w, h, WHITE)
    c.frame(x, y, w, h, GREY)
    c.rect(x, y, 22, 22, RED)
    c.text(x + 7, y + 7, str(num), 1, WHITE)
    c.text(x + 30, y + 6, place + " - " + cat, 1, RED)
    draw_badge(c, x + w - 10, y + 4, badge)
    ty = c.para(x + 10, y + 28, headline, 2, INK, w - 20, leading=17)
    ty = c.para(x + 10, ty + 2, summary, 1, INK, w - 40, leading=10)
    icon(c, x + w - 28, y + h - 30, 20)
    c.text(x + 10, y + h - 14, source, 1, GREY)


def draw_stats(c):
    y, h = 416, 56
    c.rect(0, y, W, h, NAVY)
    cw = W // 6
    for i, (num, label) in enumerate(STATS):
        x0 = i * cw
        if i:
            c.vline(x0, y + 8, h - 16, (90, 105, 140), 1)
        c.text_center(x0 + cw // 2, y + 8, num, 3, GOLD)
        c.text_center(x0 + cw // 2, y + 36, label, 1, WHITE)


def draw_map_and_also(c):
    y, h = 720, 168
    # Map, left.
    c.text(12, y, "WHERE IT HAPPENED", 2, INK)
    c.text_right(372, y + 3, "PINS CARRY THE STORY NUMBERS", 1, GREY)
    draw_map(c, 12, y + 22, 360, h - 26, PINS)
    # Also list, right: two columns of one-liners, numbers 10-30.
    ax = 392
    c.text(ax, y, "ALSO ON TUESDAY 24 NOV", 2, INK)
    for j, item in enumerate(ALSO):
        col = j // 11
        row = j % 11
        ix = ax + col * 306
        iy = y + 22 + row * 13
        c.text(ix, iy, "%d %s" % (10 + j, item), 1, INK)


def draw_datecheck(c):
    y, h = 894, 64
    c.rect(12, y, W - 24, h, WHITE)
    c.frame(12, y, W - 24, h, RED, 2)
    c.rect(12, y, W - 24, 22, RED)
    c.text(22, y + 4, "DATE CHECK", 2, WHITE)
    c.text_right(1002, y + 7, "EXCLUDED AS THE WRONG DAY", 1, WHITE)
    for i, item in enumerate(DATE_CHECK):
        ix = 22 + (i % 4) * 250
        iy = y + 28 + (i // 4) * 12
        c.text(ix, iy, "X " + item, 1, DARKRED)


def draw_footer(c):
    y = 962
    c.hline(12, y, W - 24, GREY, 1)
    c.text_center(512, y + 8,
                  "EVERY STORY ABOVE HAPPENED OR WAS FIRST REPORTED ON "
                  "TUESDAY 24 NOVEMBER 2026, AS THE NAMED OUTLETS "
                  "REPORTED IT.", 1, INK)
    c.text_center(512, y + 22,
                  "CERTAINTY: REPORTED = WIRES - OFFICIAL = ON THE "
                  "RECORD - CLAIM = ONE SIDE SAYS", 1, INK)
    c.text_center(512, y + 36,
                  "MAP AND DRAWINGS ARE ORIGINAL VECTOR ART.", 1, GREY)
    c.text_center(512, y + 50,
                  "SOURCES: REUTERS - BLOOMBERG - WSJ - AP - CNN - "
                  "AL JAZEERA - IRNA - JMIC - YONHAP - XINHUA - UN", 1, GREY)


def build():
    c = Canvas(W, H, PAPER)
    draw_masthead(c)
    draw_region_strip(c)
    draw_timeline(c)
    arts = [hero_dronewar, hero_riyadh, hero_huawei]
    for i, (place, cat, headline, summary, source, _, _, badge) in \
            enumerate(HEROES):
        draw_hero(c, 12 + i * 336, 188, 328, 222, i + 1, arts[i],
                  place, cat, headline, summary, source, badge)
    draw_stats(c)
    for i, (place, cat, headline, summary, source, _, _, icon, badge) in \
            enumerate(GRID):
        gx = 12 + (i % 3) * 336
        gy = 480 + (i // 3) * 120
        draw_grid_card(c, gx, gy, 328, 112, i + 4, icon,
                       place, cat, headline, summary, source, badge)
    draw_map_and_also(c)
    draw_datecheck(c)
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
