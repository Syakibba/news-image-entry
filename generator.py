#!/usr/bin/env python3
"""Draws the make.fun news-image-01 entry: a newspaper front page summing up
the world news of Friday 13 November 2026. Pure PIL, no network. Output:
entry.png (1024x1024 PNG, well under 1 MiB)."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

CREAM = (246, 242, 232)
INK = (24, 24, 28)
RED = (178, 30, 30)
BLUE = (28, 60, 120)
GREY = (110, 106, 98)
RULE = (60, 58, 54)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, f, max_w, fill=INK, leading=1.18, max_lines=99):
    """Draw a wrapped paragraph; return the y just below its last line."""
    x, y = xy
    step = int(f.size * leading)
    lines = wrap(draw, text, f, max_w)[:max_lines]
    for i, line in enumerate(lines):
        draw.text((x, y + i * step), line, font=f, fill=fill)
    return y + len(lines) * step


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# ---- masthead -------------------------------------------------------------
d.rectangle([0, 0, W, 96], fill=INK)
d.text((28, 16), "THE WORLD", font=font(SERIF, 52), fill=CREAM)
d.text((560, 24), "FRIDAY 13 NOVEMBER 2026", font=font(SANS, 26), fill=(200, 196, 186))
d.text((560, 58), "one page, one day", font=font(SERIF_R, 20), fill=(150, 146, 138))

# ---- lead story: US-Iran --------------------------------------------------
y = 118
d.text((28, y), "US AND IRAN TRADE NEW STRIKES", font=font(SERIF, 44), fill=RED)
y += 60
y = para(d, (28, y), "Iran's IRGC says it destroyed a US early-warning radar in Bahrain — "
                     "its first direct strike on US forces in months. Tankers hit in the Gulf.",
         font(SERIF_R, 24), 600)
y += 10

# map vignette: Strait of Hormuz
mx, my, mw, mh = 28, y, 300, 200
d.rectangle([mx, my, mx + mw, my + mh], fill=(224, 232, 238), outline=RULE)
d.polygon([(mx, my), (mx + 110, my), (mx + 90, my + 80), (mx + 30, my + 130), (mx, my + 130)], fill=(214, 202, 176))
d.polygon([(mx + 190, my + mh), (mx + mw, my + mh), (mx + mw, my + 60), (mx + 230, my + 100), (mx + 205, my + 170)], fill=(214, 202, 176))
d.text((mx + 8, my + 6), "IRAN", font=font(SANS, 20), fill=INK)
d.text((mx + 236, my + 176), "Oman", font=font(SANS, 15), fill=GREY)
d.line([(mx + 120, my + 110), (mx + 205, my + 130)], fill=RED, width=6)
d.polygon([(mx + 205, my + 130), (mx + 186, my + 120), (mx + 192, my + 142)], fill=RED)
d.text((mx + 40, my + 148), "STRAIT OF HORMUZ", font=font(SANS, 16), fill=RED)
d.ellipse([mx + 210, my + 40, mx + 250, my + 80], outline=RED, width=4)
d.line([(mx + 214, my + 44), (mx + 246, my + 76)], fill=RED, width=3)
d.line([(mx + 246, my + 44), (mx + 214, my + 76)], fill=RED, width=3)
d.text((mx + 172, my + 88), "Bahrain", font=font(SANS, 15), fill=GREY)

# side notes next to map
sy = y + 10
sy = para(d, (352, sy), "Trump: 'No hesitation' to strike Iran again — but Gulf states urge calm.",
          font(SERIF_R, 23), 640, max_lines=2)
sy += 8
sy = para(d, (352, sy), "Houthis claim attacks on Saudi oil sites; UKMTO reports tankers hit.",
          font(SERIF_R, 23), 640, fill=GREY, max_lines=2)
sy += 8
para(d, (352, sy), "Gaza: strike on Nasser Hospital kills six, wounds 28.",
     font(SERIF_R, 23), 640, fill=RED, max_lines=2)
y = my + mh + 16

d.line([28, y, W - 28, y], fill=RULE, width=2)
y += 16

# ---- Ukraine --------------------------------------------------------------
d.text((28, y), "UKRAINE: 1,200 DRONES IN ONE NIGHT", font=font(SERIF, 38), fill=INK)
y += 50
line1 = para(d, (28, y), "Russia says it downed 1,198 drones overnight; Odesa port hit and Volgograd refinery ablaze.",
             font(SERIF_R, 23), 800, max_lines=2)
line1 += 8
line1 = para(d, (28, line1), "Peace talks widen: Europe to join next round; biggest prisoner swap of the war agreed.",
             font(SERIF_R, 23), 800, fill=BLUE, max_lines=2)

# drone swarm vignette
vx, vy, vw, vh = 866, y - 6, 130, 96
d.rectangle([vx, vy, vx + vw, vy + vh], fill=(232, 228, 220), outline=RULE)
for i in range(9):
    ex = vx + 14 + (i % 3) * 34
    ey = vy + 14 + (i // 3) * 26
    d.polygon([(ex, ey), (ex + 20, ey), (ex + 10, ey - 11)], fill=INK)
d.text((vx + 14, vy + vh + 4), "drone attacks", font=font(SANS, 13), fill=GREY)

y = line1 + 24
d.line([28, y, W - 28, y], fill=RULE, width=2)
y += 16

# ---- COP31 ---------------------------------------------------------------
d.text((28, y), "COP31: WEEK ONE ENDS IN TURKEY", font=font(SERIF, 38), fill=BLUE)
y += 50
y = para(d, (28, y), "Leaders clash over pace of climate action in Antalya; Greta Thunberg tells summit "
                     "'even a snail would agree' more must be done.",
         font(SERIF_R, 23), 800, max_lines=2)

# earth vignette
ex, ey = 896, y - 74
d.ellipse([ex, ey, ex + 62, ey + 62], fill=(60, 130, 170), outline=RULE)
d.arc([ex + 6, ey + 6, ex + 56, ey + 56], 200, 340, fill=(230, 226, 210), width=5)
d.text((ex + 4, ey + 64), "COP31", font=font(SANS, 14), fill=GREY)

y += 8
d.line([28, y, W - 28, y], fill=RULE, width=2)
y += 16

# ---- bottom row: three briefs --------------------------------------------
col_w = 300
gap = 24
cols = [
    ("GAZA", RED, "Israeli strike on Nasser Hospital kills six, wounds 28; Israel says it targeted Hamas."),
    ("TECH", INK, "Nvidia CEO Jensen Huang resigns; board probes chip exports. Shares slide."),
    ("INDIA", (140, 100, 30), "Delhi becomes world's most polluted city — hazardous smog, AQI 334."),
]
for i, (head, col, body) in enumerate(cols):
    cx = 28 + i * (col_w + gap)
    d.text((cx, y), head, font=font(SANS, 26), fill=col)
    para(d, (cx, y + 38), body, font(SERIF_R, 21), col_w, max_lines=2)

# vignettes under each brief, bottom-anchored on the canvas
vh2 = 96
vy2 = H - vh2 - 20

# GAZA: candle vigil
gx, gy = 28, vy2
d.rectangle([gx, gy, gx + col_w, gy + vh2], fill=(40, 34, 30))
d.rectangle([gx + 140, gy + 34, gx + 164, gy + 70], fill=(240, 200, 90))
d.polygon([(gx + 140, gy + 34), (gx + 152, gy + 14), (gx + 164, gy + 34)], fill=(240, 150, 60))
d.rectangle([gx + 132, gy + 70, gx + 172, gy + 78], fill=(200, 190, 170))
d.text((gx + 6, gy + 6), "grief in Gaza", font=font(SANS, 15), fill=(200, 190, 170))

# TECH: falling chip
tx = 28 + (col_w + gap)
d.rectangle([tx, vy2, tx + col_w, vy2 + vh2], fill=(232, 228, 220), outline=RULE)
d.line([(tx + 30, vy2 + 18), (tx + 90, vy2 + 82)], fill=RED, width=5)
d.polygon([(tx + 90, vy2 + 82), (tx + 66, vy2 + 74), (tx + 82, vy2 + 58)], fill=RED)
d.rectangle([tx + 120, vy2 + 26, tx + 180, vy2 + 64], fill=(70, 130, 70), outline=INK)
d.text((tx + 6, vy2 + 6), "chip shares slide", font=font(SANS, 15), fill=GREY)

# INDIA: smog over Delhi
sx = 28 + 2 * (col_w + gap)
d.rectangle([sx, vy2, sx + col_w, vy2 + vh2], fill=(190, 170, 130))
d.rectangle([sx, vy2 + 36, sx + col_w, vy2 + vh2], fill=(160, 144, 112))
d.rectangle([sx + 40, vy2 + 48, sx + 72, vy2 + vh2], fill=INK)
d.rectangle([sx + 104, vy2 + 62, sx + 136, vy2 + vh2], fill=INK)
d.rectangle([sx + 168, vy2 + 54, sx + 200, vy2 + vh2], fill=INK)
d.text((sx + 6, vy2 + 6), "smog over Delhi", font=font(SANS, 15), fill=(70, 56, 24))

img.save("entry.png", optimize=True)
print("wrote entry.png", img.size)
