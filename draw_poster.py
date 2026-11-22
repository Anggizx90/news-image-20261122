#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Sunday, 22 November 2026.

A dense one-page newspaper summarising the day's world news, drawn from
scratch with Pillow. Fully deterministic: fixed layout, fixed text, no
timestamps, no randomness. Run: python3 draw_poster.py -> entry.png
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (90, 86, 76)
RULE = (40, 40, 40)
BOX = (255, 253, 246)
BLUE = (28, 68, 128)
GREEN = (28, 110, 60)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text into lines that fit `width` pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, text, fnt, width, leading, color=INK, max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


# ---------------------------------------------------------------- icons
def icon_globe(d, x, y, s):
    d.ellipse([x, y, x + s, y + s], outline=BLUE, width=4)
    d.ellipse([x + s * 0.18, y + s * 0.18, x + s * 0.82, y + s * 0.82],
              outline=BLUE, width=2)
    d.line([x, y + s / 2, x + s, y + s / 2], fill=BLUE, width=2)
    d.arc([x + s * 0.32, y, x + s * 0.68, y + s], 270, 90, fill=BLUE, width=2)
    d.arc([x + s * 0.32, y, x + s * 0.68, y + s], 90, 270, fill=BLUE, width=2)
    # rising heat arrow
    d.line([x + s * 0.78, y + s * 0.75, x + s * 0.78, y + s * 0.28],
           fill=RED, width=4)
    d.polygon([(x + s * 0.68, y + s * 0.38), (x + s * 0.88, y + s * 0.38),
               (x + s * 0.78, y + s * 0.18)], fill=RED)


def icon_zeta(d, x, y, s):
    f = font(SERIF, int(s * 0.85))
    d.text((x + s * 0.08, y - s * 0.06), "\u03b6", font=f, fill=INK)
    d.line([x + s * 0.55, y + s * 0.72, x + s * 0.72, y + s * 0.55],
           fill=GREEN, width=5)
    d.line([x + s * 0.72, y + s * 0.55, x + s * 0.88, y + s * 0.72],
           fill=GREEN, width=5)


def icon_flag(d, x, y, s):
    d.line([x + s * 0.15, y + s * 0.08, x + s * 0.15, y + s * 0.92],
           fill=INK, width=4)
    d.polygon([(x + s * 0.15, y + s * 0.08), (x + s * 0.85, y + s * 0.22),
               (x + s * 0.15, y + s * 0.38)], fill=RED)
    d.ellipse([x + s * 0.45, y + s * 0.55, x + s * 0.85, y + s * 0.9],
              outline=GREEN, width=3)


def icon_cricket(d, x, y, s):
    d.line([x + s * 0.2, y + s * 0.15, x + s * 0.55, y + s * 0.6],
           fill=(150, 100, 40), width=7)
    d.rounded_rectangle([x + s * 0.42, y + s * 0.5, x + s * 0.78, y + s * 0.92],
                        radius=6, outline=(150, 100, 40), width=4)
    d.ellipse([x + s * 0.05, y + s * 0.05, x + s * 0.28, y + s * 0.28],
              fill=RED)
    d.arc([x + s * 0.05, y + s * 0.05, x + s * 0.28, y + s * 0.28],
          0, 360, fill=(255, 255, 255), width=2)


def icon_chart_down(d, x, y, s):
    d.line([x + s * 0.1, y + s * 0.2, x + s, y + s * 0.2], fill=GREY, width=2)
    d.line([x + s * 0.1, y + s * 0.2, x + s * 0.1, y + s * 0.9], fill=GREY, width=2)
    d.line([x + s * 0.15, y + s * 0.3, x + s * 0.4, y + s * 0.5,
            x + s * 0.6, y + s * 0.42, x + s * 0.85, y + s * 0.8],
           fill=RED, width=5)
    d.polygon([(x + s * 0.72, y + s * 0.8), (x + s * 0.92, y + s * 0.8),
               (x + s * 0.85, y + s * 0.62)], fill=RED)


def icon_dome(d, x, y, s):
    d.polygon([(x + s * 0.1, y + s * 0.85), (x + s * 0.9, y + s * 0.85),
               (x + s * 0.9, y + s * 0.72), (x + s * 0.1, y + s * 0.72)],
              fill=INK)
    d.rectangle([x + s * 0.2, y + s * 0.55, x + s * 0.8, y + s * 0.72],
                outline=INK, width=3)
    d.pieslice([x + s * 0.28, y + s * 0.18, x + s * 0.72, y + s * 0.62],
               180, 360, fill=INK)
    d.line([x + s * 0.5, y + s * 0.05, x + s * 0.5, y + s * 0.18],
           fill=INK, width=3)


def icon_bridge(d, x, y, s):
    d.line([x + s * 0.05, y + s * 0.75, x + s * 0.95, y + s * 0.75],
           fill=INK, width=4)
    d.arc([x + s * 0.08, y + s * 0.3, x + s * 0.92, y + s * 1.2],
          180, 360, fill=INK, width=4)
    d.line([x + s * 0.2, y + s * 0.75, x + s * 0.2, y + s * 0.42],
           fill=INK, width=3)
    d.line([x + s * 0.8, y + s * 0.75, x + s * 0.8, y + s * 0.42],
           fill=INK, width=3)
    d.line([x + s * 0.5, y + s * 0.75, x + s * 0.5, y + s * 0.32],
           fill=INK, width=3)


def icon_shield(d, x, y, s):
    d.polygon([(x + s * 0.5, y + s * 0.05), (x + s * 0.9, y + s * 0.2),
               (x + s * 0.9, y + s * 0.55), (x + s * 0.5, y + s * 0.95),
               (x + s * 0.1, y + s * 0.55), (x + s * 0.1, y + s * 0.2)],
              outline=BLUE, width=4)
    d.ellipse([x + s * 0.35, y + s * 0.32, x + s * 0.65, y + s * 0.58],
              outline=BLUE, width=3)
    d.ellipse([x + s * 0.45, y + s * 0.42, x + s * 0.55, y + s * 0.5],
              fill=BLUE)


def icon_gate(d, x, y, s):
    d.line([x + s * 0.1, y + s * 0.15, x + s * 0.1, y + s * 0.85],
           fill=INK, width=4)
    d.line([x + s * 0.9, y + s * 0.15, x + s * 0.9, y + s * 0.85],
           fill=INK, width=4)
    d.line([x + s * 0.05, y + s * 0.3, x + s * 0.95, y + s * 0.3],
           fill=RED, width=6)
    for i in range(5):
        xx = x + s * (0.2 + i * 0.15)
        d.line([xx, y + s * 0.3, xx, y + s * 0.62], fill=INK, width=3)
    d.line([x + s * 0.1, y + s * 0.62, x + s * 0.9, y + s * 0.62],
           fill=INK, width=3)


def icon_torii(d, x, y, s):
    d.polygon([(x + s * 0.08, y + s * 0.18), (x + s * 0.92, y + s * 0.18),
               (x + s * 0.85, y + s * 0.3), (x + s * 0.15, y + s * 0.3)],
              fill=RED)
    d.line([x + s * 0.2, y + s * 0.38, x + s * 0.8, y + s * 0.38],
           fill=RED, width=5)
    d.line([x + s * 0.28, y + s * 0.38, x + s * 0.28, y + s * 0.88],
           fill=INK, width=5)
    d.line([x + s * 0.72, y + s * 0.38, x + s * 0.72, y + s * 0.88],
           fill=INK, width=5)


def icon_cyclone(d, x, y, s):
    cx, cy = x + s / 2, y + s / 2
    for i, r in enumerate([s * 0.42, s * 0.32, s * 0.22, s * 0.12]):
        d.arc([cx - r, cy - r, cx + r, cy + r], 200 + i * 40, 200 + i * 40 + 240,
              fill=BLUE, width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)


def icon_search(d, x, y, s):
    d.ellipse([x + s * 0.08, y + s * 0.08, x + s * 0.62, y + s * 0.62],
              outline=INK, width=4)
    d.line([x + s * 0.55, y + s * 0.55, x + s * 0.9, y + s * 0.9],
           fill=INK, width=5)
    d.text((x + s * 0.22, y + s * 0.16), "?", font=font(SANS_BOLD, int(s * 0.4)),
           fill=RED)


ICONS = {
    "globe": icon_globe, "zeta": icon_zeta, "flag": icon_flag,
    "cricket": icon_cricket, "chart": icon_chart_down, "dome": icon_dome,
    "bridge": icon_bridge, "shield": icon_shield, "gate": icon_gate,
    "torii": icon_torii, "cyclone": icon_cyclone, "search": icon_search,
}

# ---------------------------------------------------------------- stories
# (kicker, headline, summary, icon)
LEAD = ("CLIMATE  •  ANTALYA",
        "No deal yet as COP31 talks run into Sunday",
        "Climate talks in Antalya dragged past their deadline with nearly 200 "
        "countries still split over fossil fuels and finance. The latest draft "
        "drops every mention of them; the EU warns it will be a good deal or "
        "no deal.",
        "globe")

STORIES = [
    ("SCIENCE",
     "Anthropic's AI-assisted Riemann proof checks out",
     "Lean verifiers finished checking the 17m-line proof on Saturday; "
     "experts say months of study remain.",
     "zeta"),
    ("MIDDLE EAST",
     "Israel says Hamas tightening its grip on Gaza",
     "Israel alleges the group is intensifying its hold on the Strip as the "
     "fragile ceasefire faces fresh strain.",
     "flag"),
    ("CRICKET  •  WELLINGTON",
     "India build a 261-run lead on day four",
     "India reached 629 for 6 in the first Test, stretching their lead at "
     "Basin Reserve on Sunday.",
     "cricket"),
    ("MARKETS",
     "Wall Street reels in AI sell-off",
     "The S&P 500 slid into correction; the Nasdaq had its worst week since "
     "2020. Anthropic fell 8.5% on Friday.",
     "chart"),
    ("UNITED STATES",
     "Trump threatens tax on overseas AI data centres",
     "US firms building data centres overseas face a 'tremendous tax', "
     "Trump said, naming no rate.",
     "dome"),
    ("UKRAINE",
     "Zelensky: Bridge strikes 'a fair response'",
     "Kyiv defended the strikes as Zelensky met Britain's Wes Streeting, "
     "after Trump called Putin a friend.",
     "bridge"),
    ("EUROPE",
     "Denmark accuses Russia of plot to kill rapper",
     "Copenhagen says Russian intelligence plotted to kill a Ukrainian-"
     "American rapper near the capital.",
     "shield"),
    ("EUROPE",
     "Estonia to shut Russia border from 1 December",
     "Tallinn will close all road crossings for six months after blaming "
     "Russia's GRU for a sabotage attempt.",
     "gate"),
    ("ASIA",
     "Japanese forces to train in India for first time",
     "A Tokyo letter of intent opens Indian ranges to Japanese live-fire "
     "drills, missiles included.",
     "torii"),
    ("WEATHER  •  INDIA",
     "Cyclone Akvan disrupts flights in eastern India",
     "Fourteen flights were cancelled at Ranchi on Saturday as the storm's "
     "remnants cut visibility.",
     "cyclone"),
]

WIDE = ("UNITED STATES",
        "FBI investigates apparent hack of its crime database",
        "The bureau is probing a possible breach of its crime database, the "
        "latest in a string of suspected cyberattacks.",
        "search")


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer frame
    d.rectangle([10, 10, W - 11, H - 11], outline=RULE, width=3)

    # ---- header
    f_small = font(SANS_BOLD, 17)
    d.text((28, 26), "SUNDAY", font=f_small, fill=INK)
    date_txt = "22 NOVEMBER 2026"
    d.text((W - 28 - d.textlength(date_txt, font=f_small), 26),
           date_txt, font=f_small, fill=INK)
    d.line([28, 52, W - 28, 52], fill=RULE, width=2)

    f_mast = font(SERIF, 74)
    mast = "THE WORLD TODAY"
    mw = d.textlength(mast, font=f_mast)
    d.text(((W - mw) / 2, 56), mast, font=f_mast, fill=INK)
    d.line([28, 138, W - 28, 138], fill=RULE, width=3)
    d.line([28, 143, W - 28, 143], fill=RULE, width=1)

    f_date = font(SANS_BOLD, 19)
    dl = "SUNDAY, 22 NOVEMBER 2026   •   THE DAY'S WORLD NEWS IN ONE PAGE"
    dw = d.textlength(dl, font=f_date)
    d.text(((W - dw) / 2, 152), dl, font=f_date, fill=RED)

    # ---- lead story
    lx, ly, lw = 28, 186, W - 56
    d.rectangle([lx, ly, lx + lw, ly + 200], fill=BOX, outline=RULE, width=2)
    d.rectangle([lx, ly, lx + 7, ly + 200], fill=RED)
    f_kick = font(SANS_BOLD, 16)
    d.text((lx + 22, ly + 12), LEAD[0], font=f_kick, fill=RED)
    f_lead_h = font(SERIF, 33)
    y = draw_text_block(d, lx + 22, ly + 36, LEAD[1], f_lead_h, 720, 40,
                        max_lines=2)
    f_lead_s = font(SANS, 17)
    draw_text_block(d, lx + 22, y + 4, LEAD[2], f_lead_s, 720, 22,
                    max_lines=3)
    # lead illustration: globe with heat
    icon_globe(d, lx + lw - 200, ly + 34, 140)

    # ---- grid of stories, 2 columns x 5 rows
    gx, gy = 28, 394
    cw, ch, gap = 476, 103, 16
    f_head = font(SERIF, 20)
    f_sum = font(SANS, 14)
    f_k = font(SANS_BOLD, 13)
    for i, (kicker, head, summ, icon) in enumerate(STORIES):
        row, col = divmod(i, 2)
        x = gx + col * (cw + gap)
        y = gy + row * (ch + 6)
        d.rectangle([x, y, x + cw, y + ch], fill=BOX, outline=RULE, width=1)
        ICONS[icon](d, x + 12, y + 20, 64)
        tx = x + 88
        d.text((tx, y + 6), kicker, font=f_k, fill=RED)
        yy = draw_text_block(d, tx, y + 24, head, f_head, cw - 104, 22,
                             max_lines=2)
        draw_text_block(d, tx, yy + 2, summ, f_sum, cw - 104, 16,
                        max_lines=2, color=(40, 40, 40))

    # ---- wide bottom story
    wx, wy, ww, wh = 28, 384 + 5 * (ch + 6) + 6, W - 56, 56
    d.rectangle([wx, wy, wx + ww, wy + wh], fill=BOX, outline=RULE, width=1)
    ICONS[WIDE[3]](d, wx + 12, wy + 9, 44)
    tx = wx + 68
    f_whead = font(SERIF, 20)
    d.text((tx, wy + 8), WIDE[0] + "  —  " + WIDE[1], font=f_whead, fill=INK)
    draw_text_block(d, tx, wy + 34, WIDE[2], f_sum, ww - 84, 18, max_lines=1,
                    color=(40, 40, 40))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    draw()
