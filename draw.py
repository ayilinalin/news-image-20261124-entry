#!/usr/bin/env python3
"""Draw the front page for Tuesday 24 November 2026.

Everything is drawn from scratch with PIL: geometric shapes only, no
photos, no network. Output: entry.png, 1024x1024, under 1 MiB.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (178, 34, 34)
GREY = (110, 108, 100)
LIGHT = (233, 228, 214)
BLUE = (38, 84, 124)
DARKBLUE = (24, 52, 82)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = "DejaVuSerif-Bold.ttf"
SERIF_R = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_hero(draw, x, y, w, h):
    """Collapsed apartment block in Dymer: intact flats, broken wing,
    rubble, smoke, crane and rescuers. All flat geometry."""
    # sky
    draw.rectangle([x, y, x + w, y + h], fill=(214, 226, 232))
    # ground
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(196, 188, 168))
    bx, by = x + 30, y + 18
    bw, bh = 300, h - 70
    # intact block, 5 floors
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(168, 158, 138))
    draw.rectangle([bx, by, bx + bw, by + 12], fill=(120, 110, 92))
    for floor in range(5):
        wy = by + 22 + floor * ((bh - 30) // 5)
        for col in range(4):
            wx = bx + 16 + col * 70
            lit = (floor + col) % 3 == 0
            draw.rectangle([wx, wy, wx + 44, wy + 30],
                           fill=(255, 214, 120) if lit else (70, 76, 88),
                           outline=INK, width=2)
    # broken wing: jagged edge + rubble
    rx = bx + bw
    draw.polygon([(rx, by + 12), (rx + 150, by + 40), (rx + 120, by + 90),
                  (rx + 160, by + 130), (rx + 110, by + bh)],
                 fill=(140, 130, 112))
    draw.polygon([(rx, by + bh), (rx + 260, by + bh), (rx + 230, by + bh - 55),
                  (rx + 150, by + bh - 78), (rx + 60, by + bh - 40)],
                 fill=(120, 110, 92))
    # rubble chunks
    for cx, cy, s in [(rx + 60, by + bh - 34, 26), (rx + 120, by + bh - 22, 30),
                      (rx + 190, by + bh - 30, 24), (rx + 90, by + bh - 58, 20)]:
        draw.rectangle([cx, cy, cx + s, cy + s // 2], fill=(90, 84, 74))
    # smoke
    for sx, sy, r in [(rx + 90, by + 8, 26), (rx + 130, by - 6, 32),
                      (rx + 70, by - 18, 22)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(200, 200, 196))
    # crane
    cx0 = x + w - 190
    draw.rectangle([cx0, y + 10, cx0 + 10, y + h - 26], fill=(214, 164, 32))
    draw.rectangle([cx0 - 60, y + 10, cx0 + 130, y + 22], fill=(214, 164, 32))
    draw.line([(cx0 + 120, y + 22), (cx0 + 120, y + 70)], fill=INK, width=3)
    draw.rectangle([cx0 + 108, y + 70, cx0 + 132, y + 84], fill=RED)
    # rescuers with stretcher
    gy = y + h - 26
    for px in (x + 60, x + 110):
        draw.ellipse([px, gy - 34, px + 14, gy - 20], fill=(232, 190, 150))
        draw.rectangle([px + 2, gy - 20, px + 12, gy], fill=(214, 90, 40))
    draw.rectangle([x + 74, gy - 12, x + 122, gy - 6], fill=(240, 240, 230))
    # clouds
    for cx, cy in [(x + 640, y + 26), (x + 780, y + 48)]:
        draw.ellipse([cx - 34, cy - 12, cx + 34, cy + 12], fill=(240, 242, 244))
        draw.ellipse([cx - 18, cy - 20, cx + 18, cy + 8], fill=(240, 242, 244))


def draw_ship(draw, x, y, s):
    """Corvette on waves, drone above, blast star."""
    draw.rectangle([x, y, x + s, y + s], fill=(196, 216, 228))
    wy = y + s * 0.62
    for i in range(4):
        draw.arc([x + i * 30 - 10, wy - 8, x + i * 30 + 34, wy + 14],
                 180, 360, fill=BLUE, width=3)
    draw.rectangle([x + 14, wy - 26, x + s - 14, wy - 6], fill=(90, 96, 104))
    draw.rectangle([x + 44, wy - 40, x + 60, wy - 26], fill=(70, 76, 84))
    draw.rectangle([x + 60, wy - 52, x + 66, wy - 40], fill=(70, 76, 84))
    # blast
    bx, by = x + s - 26, wy - 44
    pts = []
    for i in range(8):
        ang = i * 3.14159 / 4
        r = 18 if i % 2 == 0 else 8
        pts.append((bx + r * __import__("math").cos(ang),
                    by + r * __import__("math").sin(ang)))
    draw.polygon(pts, fill=(255, 170, 30))
    # drone
    draw.ellipse([x + 16, y + 12, x + 30, y + 22], fill=INK)
    draw.line([(x + 8, y + 10), (x + 38, y + 10)], fill=INK, width=2)


def draw_fire(draw, x, y, s):
    """Factory with flame and smoke."""
    draw.rectangle([x, y, x + s, y + s], fill=(232, 214, 190))
    draw.rectangle([x + 12, y + s * 0.55, x + s - 12, y + s - 10],
                   fill=(150, 142, 128))
    draw.rectangle([x + 16, y + s * 0.42, x + 34, y + s * 0.55],
                   fill=(120, 114, 102))
    for wx in (x + 22, x + 52, x + 82):
        draw.rectangle([wx, y + s * 0.66, wx + 18, y + s * 0.80],
                       fill=(255, 214, 120))
    # flame
    fx, fy = x + s // 2, y + s * 0.40
    draw.polygon([(fx - 26, fy + 18), (fx - 12, fy - 22), (fx, fy + 2),
                  (fx + 12, fy - 30), (fx + 26, fy + 18)],
                 fill=(230, 90, 30))
    draw.polygon([(fx - 12, fy + 18), (fx - 4, fy - 6), (fx + 4, fy + 6),
                  (fx + 12, fy + 18)], fill=(255, 200, 60))
    for sx, sy, r in [(x + 24, y + 14, 14), (x + 44, y + 6, 18),
                      (x + 70, y + 16, 12)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(190, 188, 182))


def draw_train(draw, x, y, s):
    """Front of a train on a track, two carriages."""
    draw.rectangle([x, y, x + s, y + s], fill=(206, 226, 210))
    draw.rectangle([x + 10, y + s * 0.30, x + s - 10, y + s * 0.72],
                   fill=(178, 34, 34))
    draw.rectangle([x + 10, y + s * 0.30, x + s - 10, y + s * 0.40],
                   fill=(240, 240, 230))
    draw.rectangle([x + 22, y + s * 0.44, x + 52, y + s * 0.60],
                   fill=(180, 220, 235))
    draw.rectangle([x + 62, y + s * 0.44, x + 92, y + s * 0.60],
                   fill=(180, 220, 235))
    draw.ellipse([x + 26, y + s * 0.64, x + 40, y + s * 0.70],
                 fill=(255, 230, 120))
    draw.ellipse([x + 76, y + s * 0.64, x + 90, y + s * 0.70],
                 fill=(255, 230, 120))
    draw.line([(x, y + s * 0.82), (x + s, y + s * 0.82)], fill=INK, width=4)
    for tx in range(0, s, 22):
        draw.line([(x + tx, y + s * 0.82), (x + tx, y + s * 0.92)],
                  fill=INK, width=3)


def draw_chess(draw, x, y, s):
    """Chessboard with king and queen."""
    draw.rectangle([x, y, x + s, y + s], fill=(233, 228, 214))
    cell = s // 4
    for r in range(4):
        for c in range(4):
            if (r + c) % 2 == 0:
                draw.rectangle([x + c * cell, y + r * cell,
                                x + (c + 1) * cell, y + (r + 1) * cell],
                               fill=(60, 60, 60))
    # white king
    kx, ky = x + cell, y + cell
    draw.rectangle([kx + 6, ky + 18, kx + cell - 6, ky + cell - 4],
                   fill=(250, 250, 245), outline=INK, width=2)
    draw.ellipse([kx + 8, ky + 2, kx + cell - 8, ky + 20],
                 fill=(250, 250, 245), outline=INK, width=2)
    draw.line([(kx + cell // 2, ky - 2), (kx + cell // 2, ky + 8)],
              fill=INK, width=3)
    draw.line([(kx + cell // 2 - 5, ky + 2), (kx + cell // 2 + 5, ky + 2)],
              fill=INK, width=3)
    # black queen
    qx, qy = x + 2 * cell, y + 2 * cell
    draw.polygon([(qx + 4, qy + cell - 4), (qx + 8, qy + 10),
                  (qx + cell // 2, qy + 20), (qx + cell - 8, qy + 10),
                  (qx + cell - 4, qy + cell - 4)], fill=INK)
    draw.ellipse([qx + cell // 2 - 5, qy + 2, qx + cell // 2 + 5, qy + 12],
                 fill=INK)


def panel(draw, x, y, w, h, kicker, title, body, art):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + 4], fill=RED)
    tx = x + 14
    ty = y + 14
    draw.text((tx, ty), kicker, font=font(SANS_B, 15), fill=RED)
    ty += 24
    tlines = wrap(draw, title, font(SERIF, 24), w - 150)
    ty = text_block(draw, tx, ty, tlines, font(SERIF, 24), INK, 27)
    ty += 6
    blines = wrap(draw, body, font(SANS, 17), w - 150)
    text_block(draw, tx, ty, blines, font(SANS, 17), (40, 40, 40), 21)
    art(draw, x + w - 128, y + h - 128, 116)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 28  # margin

    # ---- masthead ----
    y = 18
    mast = font(SERIF, 78)
    d.text(((W - d.textlength("THE WORLD TODAY", font=mast)) / 2, y),
           "THE WORLD TODAY", font=mast, fill=INK)
    y += 94
    rule(d, m, y, W - m, 3)
    y += 8
    rule(d, m, y, W - m, 1)
    y += 10
    # ---- date banner ----
    d.rectangle([m, y, W - m, y + 46], fill=INK)
    date_f = font(SANS_B, 30)
    date_t = "TUESDAY 24 NOVEMBER 2026"
    d.text(((W - d.textlength(date_t, font=date_f)) / 2, y + 7),
           date_t, font=date_f, fill=(255, 255, 255))
    y += 46 + 12

    # ---- headline ----
    d.text((m, y), "UKRAINE  •  KYIV REGION", font=font(SANS_B, 16), fill=RED)
    y += 26
    hl = font(SERIF, 47)
    for line in ["ELEVEN DEAD AS RESCUERS",
                 "DIG ON IN KYIV REGION"]:
        d.text((m, y), line, font=hl, fill=INK)
        y += 54
    sub = ("A Russian drone strike hit flats in Dymer; a boy of 7 was "
           "pulled alive after 22 hours under the rubble, and two people "
           "are still unaccounted for.")
    y = text_block(d, m, y + 2,
                   wrap(d, sub, font(SERIF_R, 21), W - 2 * m),
                   font(SERIF_R, 21), (40, 40, 40), 27) + 8

    # ---- hero illustration ----
    hero_h = 158
    draw_hero(d, m, y, W - 2 * m, hero_h)
    d.rectangle([m, y, W - m, y + hero_h], outline=INK, width=2)
    y += hero_h + 10

    # ---- 2x2 panels ----
    pw = (W - 2 * m - 14) // 2
    ph = 168
    panel(d, m, y, pw, ph, "LIBYA  •  WAR AT SEA",
          "Ukraine sinks Russian warship off Libya",
          "Sea drones hit the corvette Merkury at Benghazi; Kyiv says a "
          "cargo ship and a helicopter were hit too.", draw_ship)
    panel(d, m + pw + 14, y, pw, ph, "INDONESIA  •  BANTEN",
          "24 dead in factory fire; search goes on",
          "Bodies recovered in Cikande after Saturday's blaze at a candy "
          "factory; about 30 workers are still missing.", draw_fire)
    y += ph + 10
    panel(d, m, y, pw, ph, "INDIA & NEPAL",
          "New train links Ayodhya and Janakpur",
          "Modi and PM Shah launch the Ayodhya-Janakpur train, sign eight "
          "deals and a Rs 15,000-crore package.", draw_train)
    panel(d, m + pw + 14, y, pw, ph, "GENEVA  •  CHESS",
          "Chess crown defence begins today",
          "Champion Gukesh, 20, meets challenger Sindarov, 20, in Game 1 "
          "of the youngest title match ever.", draw_chess)
    y += ph + 10

    # ---- bottom strip: also today ----
    rule(d, m, y, W - m, 2)
    y += 8
    d.text((m, y), "ALSO TODAY", font=font(SANS_B, 16), fill=RED)
    y += 24
    also = ("SEOUL — Lee reshuffles his cabinet and names the first woman "
            "to lead the spy agency.   GAZA — Oxfam: signs of toxic "
            "contamination across 99% of the Strip.   LISBON — Unions rally "
            "as MPs vote on the budget.")
    y = text_block(d, m, y, wrap(d, also, font(SANS, 18), W - 2 * m),
                   font(SANS, 18), (40, 40, 40), 23)
    rule(d, m, H - 22, W - m, 1)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print(out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
