#!/usr/bin/env python3
"""
THE MIDNIGHT WIRE — front-page generator for news-image-20261120.
Renders one 1024x1024 broadsheet front page for Friday 20 November 2026
from the verified story file (candidates/stories.md). All art is drawn
procedurally with Pillow: no photographs, no external images.

Iteration 2 (art pass): painted hero scene, multi-element panel scenes,
three dot-globes instead of a dot strip, taller first panel row,
larger briefs type (28 briefs).
"""
from PIL import Image, ImageDraw, ImageFont
import math, os, random

BASE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.expanduser(
    "~/workspace/multi-agent-system/agents/makefun-hunter/data/makefun/assets/fonts")
OUT = os.path.join(BASE, "entry.png")

W = H = 1024
M = 24                      # page margin

# ---------------------------------------------------------------- palette
PAPER   = (10, 13, 26)      # near-black indigo "midnight" paper
PANEL   = (19, 24, 44)      # panel fill
PANEL2  = (24, 30, 54)      # lighter panel fill (scene strip sky base)
INK     = (240, 233, 214)   # cream ink
MUTED   = (154, 163, 184)   # grey-blue secondary text
FAINT   = (96, 104, 128)
RED     = (229, 72, 77)
GOLD    = (232, 179, 75)
CYAN    = (87, 199, 212)
GREEN   = (125, 216, 125)
RIVER   = (38, 84, 124)

REGION_COLORS = {
    "EUROPE":    (110, 168, 254),
    "ASIA":      (232, 179, 75),
    "MIDDLE EAST": (240, 140, 74),
    "N AMERICA": (125, 216, 125),
    "S AMERICA": (74, 210, 194),
    "AFRICA":    (228, 138, 212),
    "OCEANIA":   (157, 138, 255),
}

def F(name, size):
    paths = {
        "black":  f"{FONTS}/archivo-black/ArchivoBlack-Regular.ttf",
        "oswB":   f"{FONTS}/oswald/Oswald-Bold.ttf",
        "oswS":   f"{FONTS}/oswald/Oswald-SemiBold.ttf",
        "pjR":    f"{FONTS}/plus-jakarta-sans/PlusJakartaSans-Regular.ttf",
        "pjM":    f"{FONTS}/plus-jakarta-sans/PlusJakartaSans-Medium.ttf",
        "pjSB":   f"{FONTS}/plus-jakarta-sans/PlusJakartaSans-SemiBold.ttf",
        "pjB":    f"{FONTS}/plus-jakarta-sans/PlusJakartaSans-Bold.ttf",
        "pjXB":   f"{FONTS}/plus-jakarta-sans/PlusJakartaSans-ExtraBold.ttf",
    }
    return ImageFont.truetype(paths[name], size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")
rng = random.Random(20261120)

def tw(text, font):
    return d.textlength(text, font=font)

def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w_
    if cur: lines.append(cur)
    return lines

def ellipsize(text, font, maxw):
    if tw(text, font) <= maxw: return text
    while text and tw(text + "…", font) > maxw:
        text = text[:-1]
    return text.rstrip() + "…"

def text_block(x, y, text, font, fill, maxw, lh, max_lines=None, align="left"):
    lines = wrap(text, font, maxw)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = ellipsize(lines[-1], font, maxw)
    for ln in lines:
        lx = x if align == "left" else x + (maxw - tw(ln, font)) / 2
        d.text((lx, y), ln, font=font, fill=fill)
        y += lh
    return y

def chip(x, y, text, font, fg, bg=None, pad=5, h=None):
    w_ = tw(text, font) + pad * 2
    h = h or (font.size + 7)
    if bg: d.rounded_rectangle([x, y, x + w_, y + h], 3, fill=bg)
    d.text((x + pad, y + (h - font.size) / 2 - 1), text, font=font, fill=fg)
    return x + w_

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def vgrad(x0, y0, x1, y1, top, bot, steps=2):
    """Vertical gradient fill in horizontal bands."""
    hgt = y1 - y0
    n = max(2, int(hgt // steps))
    for i in range(n):
        t = i / (n - 1)
        yy0 = y0 + i * hgt / n
        yy1 = y0 + (i + 1) * hgt / n + 1
        d.rectangle([x0, yy0, x1, yy1], fill=lerp(top, bot, t))

def bez(p0, p1, p2, n=40):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    return pts

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 6], fill=RED)
y = 11
line = "T H E   M I D N I G H T   W I R E"
f = F("pjB", 13)
d.text(((W - tw(line, f)) / 2, y), line, font=f, fill=GOLD)
y += 20
f = F("pjM", 10)
sub = "GLOBAL FRONT PAGE  ·  ALL TIMES UTC  ·  NO PHOTOGRAPHS — EVERY PICTURE DRAWN IN CODE"
d.text(((W - tw(sub, f)) / 2, y), sub, font=f, fill=MUTED)
y += 14
f = F("black", 58)
date = "FRIDAY 20 NOVEMBER 2026"
while tw(date, f) > W - 2 * M:
    f = F("black", f.size - 2)
d.text(((W - tw(date, f)) / 2, y - 2), date, font=f, fill=INK)
y += 62
d.line([M, y, W - M, y], fill=INK, width=2)
d.line([M, y + 3, W - M, y + 3], fill=FAINT, width=1)
y += 8
f = F("pjB", 12.5)
count_line = "44 STORIES · 6 CONTINENTS · 15 DRAWN PANELS · WORLD MAP IN 3 GLOBES · EVERY STORY SOURCED & TAGGED"
d.text(((W - tw(count_line, f)) / 2, y), count_line, font=f, fill=CYAN)
y += 17
d.line([M, y, W - M, y], fill=FAINT, width=1)

# ---------------------------------------------------------------- hero
HY = y + 8
HH = 204
d.rectangle([M, HY, W - M, HY + HH], fill=PANEL)
ax0, ay0, ax1, ay1 = M, HY, M + 372, HY + HH
HOR = ay0 + 140                     # horizon / deck level
BOT = ay1 - 16                      # caption bar top

# --- dawn sky: indigo -> ember glow at the horizon
for i in range(int(HOR - ay0)):
    t = i / (HOR - ay0)
    if t < 0.55:
        c = lerp((11, 13, 33), (46, 34, 64), t / 0.55)
    else:
        c = lerp((46, 34, 64), (172, 88, 58), (t - 0.55) / 0.45)
    d.line([ax0, ay0 + i, ax1, ay0 + i], fill=c)
# sun glow behind the crossings
gx, gy = ax0 + 196, HOR - 4
for r_, a in [(120, 26), (88, 40), (58, 62), (34, 92)]:
    d.ellipse([gx - r_, gy - r_ * 0.62, gx + r_, gy + r_ * 0.62],
              fill=(255, 166, 88, a))
# stars, fading toward the horizon
for _ in range(80):
    sx = rng.uniform(ax0 + 3, ax1 - 3)
    sy = rng.uniform(ay0 + 3, ay0 + 86)
    a = int(200 * (1 - (sy - ay0) / 92)) + 30
    s = rng.choice([1, 1, 1, 2])
    d.ellipse([sx, sy, sx + s, sy + s], fill=(235, 238, 255, max(0, min(230, a))))

# --- searchlight cones (behind skyline glow, above sky)
def searchlight(bx, tx, ty):
    d.polygon([(bx, HOR), (tx - 13, ty), (tx + 13, ty)], fill=(140, 170, 220, 22))
    d.polygon([(bx, HOR), (tx - 6, ty), (tx + 6, ty)], fill=(160, 190, 235, 30))
    d.ellipse([bx - 2, HOR - 3, bx + 2, HOR + 1], fill=(220, 235, 255))
searchlight(ax0 + 44, ax0 + 168, ay0 + 22)
searchlight(ax0 + 330, ax0 + 210, ay0 + 10)

# --- skyline silhouettes, both banks
def skyline(x0, x1, base, heights, col):
    x = x0
    i = 0
    while x < x1 - 8:
        bw = 15 + (i * 7) % 13
        bh = heights[i % len(heights)]
        d.rectangle([x, base - bh, x + bw, base], fill=col)
        for wy in range(base - bh + 6, base - 7, 9):
            for wx in range(x + 3, x + bw - 3, 7):
                if (wx * 3 + wy * 7 + i) % 5 == 0:
                    d.point((wx, wy), fill=(255, 196, 96))
        x += bw + 2
        i += 1
SIL = (7, 9, 18)
skyline(ax0 + 3, ax0 + 122, HOR, [36, 54, 29, 60, 42, 26, 48], SIL)
skyline(ax0 + 252, ax1 - 3, HOR, [46, 27, 56, 34, 62, 29, 40], SIL)
# Pechersk-style golden dome + bell tower on the right bank (kept clear of the cable fan)
dx_ = ax0 + 348
d.rectangle([dx_ - 7, HOR - 46, dx_ + 7, HOR], fill=SIL)                    # tower
d.pieslice([dx_ - 11, HOR - 62, dx_ + 11, HOR - 36], 180, 360, fill=(150, 106, 44))
d.rectangle([dx_ - 5, HOR - 36, dx_ + 5, HOR - 27], fill=(150, 106, 44))
d.line([dx_, HOR - 70, dx_, HOR - 60], fill=GOLD, width=2)                  # cross
d.line([dx_ - 4, HOR - 67, dx_ + 4, HOR - 67], fill=GOLD, width=2)
dx2 = ax0 + 84                                                              # left-bank dome
d.pieslice([dx2 - 10, HOR - 56, dx2 + 10, HOR - 34], 180, 360, fill=(140, 100, 42))
d.line([dx2, HOR - 62, dx2, HOR - 54], fill=GOLD, width=2)
d.line([dx2 - 3, HOR - 60, dx2 + 3, HOR - 60], fill=GOLD, width=2)

# --- the Dnipro
vgrad(ax0, HOR, ax1, BOT, (30, 56, 90), (11, 22, 42), steps=2)
for i in range(10):  # current streaks
    yy = HOR + 8 + i * 5
    d.line([ax0 + 10 + (i * 41) % 70, yy, ax0 + 66 + (i * 57) % 210, yy],
           fill=(96, 142, 192), width=1)

def bridge_lights(cx_, half):
    for lx_ in range(int(cx_ - half), int(cx_ + half), 11):
        d.ellipse([lx_ - 1, HOR - 4, lx_ + 1, HOR - 2], fill=(255, 205, 110))
        d.line([lx_, HOR + 5, lx_, HOR + 9], fill=(255, 190, 100, 120), width=1)

# bridge 1 — intact arch (left)
b1 = ax0 + 68
d.line([b1 - 46, HOR, b1 + 46, HOR], fill=(226, 228, 236), width=4)
d.arc([b1 - 46, HOR - 22, b1 + 46, HOR + 26], 180, 360, fill=(200, 204, 216), width=2)
for hx_ in range(-40, 41, 10):
    top = HOR - 2 - int(11 * (1 - (hx_ / 46) ** 2))
    d.line([b1 + hx_, top, b1 + hx_, HOR], fill=(170, 175, 190), width=1)
d.rectangle([b1 - 40, HOR, b1 - 34, BOT], fill=(16, 22, 38))
d.rectangle([b1 + 34, HOR, b1 + 40, BOT], fill=(16, 22, 38))
bridge_lights(b1, 42)

# bridge 3 — cable-stayed (right)
b3 = ax0 + 302
d.line([b3 - 48, HOR, b3 + 48, HOR], fill=(226, 228, 236), width=4)
d.line([b3, HOR - 52, b3, HOR], fill=(210, 213, 222), width=3)
for k in range(1, 6):
    d.line([b3, HOR - 52 + k * 3, b3 - k * 9, HOR], fill=(168, 172, 186), width=1)
    d.line([b3, HOR - 52 + k * 3, b3 + k * 9, HOR], fill=(168, 172, 186), width=1)
d.rectangle([b3 - 42, HOR, b3 - 36, BOT], fill=(16, 22, 38))
d.rectangle([b3 + 36, HOR, b3 + 42, BOT], fill=(16, 22, 38))
bridge_lights(b3, 44)

# bridge 2 — BROKEN (centre): split deck, fire, smoke
b2 = ax0 + 186
d.line([b2 - 58, HOR, b2 - 8, HOR], fill=(226, 228, 236), width=4)
d.line([b2 + 12, HOR + 1, b2 + 58, HOR + 13], fill=(226, 228, 236), width=4)  # dipped segment
d.line([b2 - 8, HOR, b2 - 3, HOR + 5], fill=(200, 200, 210), width=2)         # jagged ends
d.line([b2 + 12, HOR + 1, b2 + 7, HOR + 6], fill=(200, 200, 210), width=2)
d.rectangle([b2 - 52, HOR, b2 - 46, BOT], fill=(16, 22, 38))
d.rectangle([b2 + 44, HOR + 10, b2 + 50, BOT], fill=(16, 22, 38))
d.line([b2 + 2, HOR + 16, b2 + 22, HOR + 24], fill=(150, 152, 164), width=3)  # fallen deck in the water
for rr in range(3):  # ripples around the wreck
    d.arc([b2 - 6 - rr * 7, HOR + 20 - rr * 2, b2 + 30 + rr * 7, HOR + 30 + rr * 2],
          15, 165, fill=(120, 160, 205, 130), width=1)
# smoke plume: growing ellipses drifting up-right
smoke = [(0, 0, 9, 120), (10, -14, 13, 104), (22, -28, 17, 88), (36, -42, 21, 72),
         (52, -54, 25, 56), (70, -64, 29, 42), (90, -72, 33, 30)]
for ox, oy, r_, a in smoke:
    d.ellipse([b2 + 2 + ox - r_, HOR - 6 + oy - r_ * 0.7, b2 + 2 + ox + r_, HOR - 6 + oy + r_ * 0.7],
              fill=(22, 22, 30, a))
# fire at the break: glow, layered flames, tongues, sparks
fx, fy = b2 + 2, HOR - 3
for r_, col in [(30, (255, 120, 50, 46)), (20, (255, 110, 45, 80))]:
    d.ellipse([fx - r_, fy - r_, fx + r_, fy + r_], fill=col)
for r_, col in [(13, (229, 72, 55)), (9, (243, 130, 60)), (5.5, (255, 190, 84)), (2.6, (255, 232, 160))]:
    d.ellipse([fx - r_, fy - r_ - 3, fx + r_, fy + r_], fill=col)
for tx_, th_ in [(-7, 15), (0, 20), (6, 12)]:
    d.polygon([(fx + tx_ - 3, fy - 4), (fx + tx_ + 3, fy - 4), (fx + tx_, fy - 4 - th_)],
              fill=(255, 176, 80))
for i in range(9):  # sparks
    sx = fx + rng.randint(-13, 13)
    sy = fy - rng.randint(8, 30)
    d.point((sx, sy), fill=(255, 205, 110))
    d.point((sx, sy - 1), fill=(255, 160, 70))
# firelight shimmering on the water
for i in range(7):
    yy = HOR + 5 + i * 6
    wd = 16 - i * 1.6
    off = rng.randint(-3, 3)
    d.line([fx - wd + off, yy, fx + wd + off, yy], fill=(255, 150, 70, 150 - i * 16), width=2)

# --- missiles: glowing curved trails; one intercepted mid-sky
def missile(p0, p1, p2, burst=False):
    pts = bez(p0, p1, p2, 44)
    for wd, col in [(5, (255, 110, 80, 52)), (2, (255, 148, 98, 170)), (1, (255, 222, 172, 235))]:
        d.line(pts, fill=col, width=wd)
    ex, ey = pts[-1]
    if burst:
        for a_ in range(0, 360, 45):
            dxr, dyr = math.cos(math.radians(a_)), math.sin(math.radians(a_))
            d.line([ex, ey, ex + dxr * 11, ey + dyr * 11], fill=(255, 214, 140), width=2)
        d.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=(255, 190, 100, 90))
        d.ellipse([ex - 2.5, ey - 2.5, ex + 2.5, ey + 2.5], fill=(255, 240, 200))
    else:
        d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 190, 100, 110))
        d.ellipse([ex - 2, ey - 2, ex + 2, ey + 2], fill=(255, 238, 200))
missile((ax1 - 6, ay0 + 14), (ax0 + 268, ay0 + 30), (b2 + 4, HOR - 12))
missile((ax0 + 252, ay0 + 2), (ax0 + 168, ay0 + 26), (ax0 + 116, HOR - 8))
missile((ax1 - 34, ay0 + 44), (ax0 + 300, ay0 + 52), (ax0 + 272, ay0 + 76), burst=True)

# --- air-defence tracer arcs (dotted)
def tracers(p0, p1, p2):
    for (x_, y_) in bez(p0, p1, p2, 26)[::2]:
        d.ellipse([x_ - 1.3, y_ - 1.3, x_ + 1.3, y_ + 1.3], fill=(255, 196, 96))
tracers((ax0 + 138, HOR - 2), (ax0 + 190, ay0 + 44), (ax0 + 252, ay0 + 52))
tracers((ax0 + 330, HOR - 2), (ax0 + 306, ay0 + 50), (ax0 + 276, ay0 + 72))

# foreground bank silhouettes at the water's edge
d.polygon([(ax0, BOT), (ax0, BOT - 12), (ax0 + 52, BOT)], fill=(5, 6, 12))
d.polygon([(ax1, BOT), (ax1, BOT - 10), (ax1 - 58, BOT)], fill=(5, 6, 12))
d.rectangle([ax0, ay0, ax1, ay1], outline=FAINT, width=1)
cap = "DRAWN: the Dnipro crossings at dawn — Podilsko-Voskresenskyi, Darnytskyi, Pivdennyi"
f = F("pjM", 9)
d.rectangle([ax0, ay1 - 16, ax1, ay1], fill=(6, 8, 16))
d.text((ax0 + 6, ay1 - 13), cap, font=f, fill=MUTED)

# hero text
hx = ax1 + 18
hw = W - M - hx
hy = HY + 10
f = F("pjB", 11)
x = chip(hx, hy, "THE BIG STORY", f, (10, 13, 26), bg=RED)
x = chip(x + 6, hy, "EUROPE", f, REGION_COLORS["EUROPE"], bg=(30, 44, 74))
x = chip(x + 6, hy, "CONFIRMED", f, GREEN, bg=(24, 52, 32))
hy += 24
f = F("black", 37)
hy = text_block(hx, hy, "BALLISTIC BARRAGE BATTERS KYIV'S BRIDGES", f, INK, hw, 39, 3)
hy += 2
f = F("pjR", 12.5)
hy = text_block(hx, hy,
    "Russian ballistic missiles struck three bridges over the Dnipro — the biggest attack on the "
    "capital's river crossings of the war — hours after the Trump–Putin–Xi talks in Shenzhen. "
    "Kyiv counts three dead and some 15 injured; nationwide, ~100 missiles and ~400 drones killed eight.",
    f, (214, 208, 192), hw, 16.5, 6)
hy += 6
f = F("pjXB", 12)
cx = hx
for stat in ["±100 MISSILES", "±400 DRONES", "3 BRIDGES HIT", "8 DEAD"]:
    cx = chip(cx, hy, stat, f, GOLD, bg=(46, 38, 18)) + 8
hy += 24
f = F("pjM", 10)
d.text((hx, hy), "Sources: Reuters (Kyiv, Nov 20) · CNN · Kyiv City Military Administration", font=f, fill=MUTED)
hy += 18
d.text((hx, hy), "INSIDE — Cyclone landfall · COP31 deadlock · Asia's AI rout · GTA VI's record day · panels 1–15 below",
       font=F("pjB", 10.5), fill=CYAN)

# ---------------------------------------------------------------- UTC rail
RY = HY + HH + 8
RH = 40
d.rectangle([M, RY, W - M, RY + RH], fill=PANEL)
f = F("pjXB", 11)
d.rectangle([M, RY, M + 86, RY + RH], fill=(46, 38, 18))
d.text((M + 9, RY + 6), "THE DAY", font=f, fill=GOLD)
d.text((M + 9, RY + 21), "IN UTC", font=f, fill=GOLD)
RAIL = [
    ("23:25", "Kyiv: first explosions as the barrage begins"),
    ("03:00", "Akvan crosses the coast near Gopalpur"),
    ("06:00", "Tokyo close: Nikkei −5%, 7-month low"),
    ("07:20", "Brent $92.57 as Riyadh attack assessed"),
    ("12:00", "COP31 endgame: “no deal in sight”"),
    ("14:30", "Wall St opens: S&P extends losing run"),
]
rx = M + 98
rw = (W - M - rx - 6) / 6
d.line([rx + 4, RY + 12, W - M - 10, RY + 12], fill=FAINT, width=1)
for i, (t, label) in enumerate(RAIL):
    x = rx + i * rw
    d.ellipse([x + 2, RY + 9, x + 8, RY + 15], fill=RED)
    d.text((x + 12, RY + 4), t, font=F("oswB", 12), fill=GOLD)
    text_block(x + 2, RY + 21, label, F("pjR", 7.8), MUTED, rw - 8, 8.8, 2)

# ---------------------------------------------------------------- panels
PANELS = [
 dict(n=1, region="ASIA", tag="CONFIRMED", icon="cyclone", pin=(85, 19),
      place="GOPALPUR, INDIA",
      head="Cyclone Akvan makes landfall on Odisha coast",
      summ="Third cyclone in a month; 300,000+ evacuated ahead of 90 km/h gusts.",
      src="Reuters"),
 dict(n=2, region="ASIA", tag="CONFIRMED", icon="climate", pin=(29, 37),
      place="ANTALYA, TÜRKIYE",
      head="COP31 final day: deadlock, draft gutted",
      summ="Fossil-fuel language stripped, 21 issues open; talks run into overtime.",
      src="UN News"),
 dict(n=3, region="ASIA", tag="CONFIRMED", icon="crash", pin=(140, 36),
      place="TOKYO–TAIPEI",
      head="Asia's AI sell-off: worst week since 2020",
      summ="Nikkei −5%, KOSPI −5.2%; Taiwan −17.5% on the week, its worst since 1990.",
      src="Reuters"),
 dict(n=4, region="N AMERICA", tag="CONFIRMED", icon="ipo", pin=(-74, 41),
      place="NEW YORK, USA",
      head="Record $81bn Anthropic IPO can't lift AI stocks",
      summ="Largest IPO ever opened +34% Thursday — then the sector sold off again.",
      src="Reuters"),
 dict(n=5, region="ASIA", tag="CONFIRMED", icon="summit", pin=(114, 23),
      place="SHENZHEN, CHINA",
      head="Trump–Xi–Putin trilateral: declaration, no deal",
      summ="First three-power summit: UN reform pledged, Ukraine unresolved.",
      src="The Times"),
 dict(n=6, region="MIDDLE EAST", tag="CLAIM", icon="missile", pin=(43, 22),
      place="RIYADH · HORMUZ",
      head="Missiles on Riyadh; tankers 'mined' in Hormuz",
      summ="Houthis fire on the Saudi capital; IRGC says two tankers hit mines.",
      src="Reuters"),
 dict(n=7, region="N AMERICA", tag="ESTIMATE", icon="game", pin=(-118, 34),
      place="LOS ANGELES, USA",
      head="GTA VI: biggest launch in entertainment history",
      summ="Est. $2.36bn and 24.6m copies in 24 hours — nearly 3× GTA V's record.",
      src="VGC"),
 dict(n=8, region="MIDDLE EAST", tag="CONFIRMED", icon="oil", pin=(60, 19),
      place="LONDON · GULF",
      head="Oil slides a third week despite Riyadh attack",
      summ="Brent ~$92, yet Hormuz shipments are back at pre-war levels.",
      src="Reuters"),
 dict(n=9, region="EUROPE", tag="CONFIRMED", icon="border", pin=(24, 60),
      place="TALLINN, ESTONIA",
      head="Estonia to close Russian border crossings",
      summ="Crossings shut from December after an attack bid on a defence firm.",
      src="The Munich Eye"),
 dict(n=10, region="EUROPE", tag="CONFIRMED", icon="flags", pin=(12, 52),
      place="BERLIN, GERMANY",
      head="25+ allies rally in Berlin behind Kyiv",
      summ="Coalition of the Willing wants a European seat at peace talks.",
      src="CNN"),
 dict(n=11, region="S AMERICA", tag="CONFIRMED", icon="bank", pin=(-48, -16),
      place="BRASÍLIA, BRAZIL",
      head="Brazil sells $1bn of reserves to defend real",
      summ="Real down ~18% in a month, near 5.93 per dollar, as outflows grow.",
      src="One Turn News"),
 dict(n=12, region="AFRICA", tag="CONFIRMED", icon="coins", pin=(34, 26),
      place="CAIRO, EGYPT",
      head="Egypt repays $38.2bn as reserves hit record",
      summ="Finance ministry touts record foreign reserves after the debt payments.",
      src="Egypt Independent"),
 dict(n=13, region="OCEANIA", tag="CONFIRMED", icon="island", pin=(-175, -21),
      place="TONGA",
      head="Tonga declares 27-day drought emergency",
      summ="El Niño dry spell deepens across the Pacific; water, crops strained.",
      src="RNZ Pacific"),
 dict(n=14, region="MIDDLE EAST", tag="CONFIRMED", icon="ships", pin=(58, 30),
      place="PERSIAN GULF",
      head="US widens Iran blockade; crude transfer seen",
      summ="Sanctioned Suezmax in first ship-to-ship transfer seen since July.",
      src="Bloomberg"),
 dict(n=15, region="N AMERICA", tag="CONFIRMED", icon="pulsar", pin=(-77, 39),
      place="WASHINGTON, USA",
      head="Crypto-math finds a pulsar in 15 yrs of data",
      summ="Lattice search spots a 261 Hz pulsar in 10 CPU-hours — not 600 years.",
      src="NASA · PRL"),
]

# ---- multi-element mini-scenes, drawn in a w x h strip at (x, y)
def _strip_bg(x, y, w, h):
    vgrad(x, y, x + w, y + h, (27, 35, 60), (33, 42, 70), steps=2)

def _palm(cx_, base, hgt, col, bend=6, droop=False):
    top = (cx_ + bend, base - hgt)
    d.line(bez((cx_, base), (cx_ + bend * 0.3, base - hgt * 0.6), top, 10), fill=col, width=2)
    for a_ in (-160, -115, -70, -25, 15):
        ex = top[0] + math.cos(math.radians(a_)) * hgt * 0.42
        ey = top[1] + abs(math.sin(math.radians(a_))) * hgt * (0.30 if droop else 0.16) \
             - (hgt * 0.10 if not droop else 0)
        d.line(bez(top, (top[0] + (ex - top[0]) * 0.5, top[1] - hgt * 0.14), (ex, ey), 8),
               fill=col, width=1)

def _waves(x, y, w, base, col=(120, 165, 215)):
    for i in range(3):
        for k in range(4):
            wx = x + 6 + k * (w / 4) + (i % 2) * 9
            d.arc([wx, base + i * 4 - 2, wx + 13, base + i * 4 + 3], 180, 360, fill=col, width=1)

def scene(name, x, y, w, h):
    _strip_bg(x, y, w, h)
    cx, cy = x + w / 2, y + h / 2
    if name == "cyclone":
        sea = y + h * 0.64
        d.polygon([(x + w * 0.52, sea), (x + w, y + h * 0.44), (x + w, y + h),
                   (x + w * 0.52, y + h)], fill=(56, 58, 42))          # coastline
        d.rectangle([x, sea, x + w, y + h], fill=(23, 52, 84))
        d.polygon([(x + w * 0.52, sea), (x + w, y + h * 0.44), (x + w, sea)], fill=(56, 58, 42))
        _waves(x, y, w * 0.6, sea + 3)
        ccx, ccy = x + w * 0.34, y + h * 0.40
        for r_, a0 in [(h * 0.34, 15), (h * 0.24, 195), (h * 0.15, 45)]:
            d.arc([ccx - r_, ccy - r_, ccx + r_, ccy + r_], a0, a0 + 255, fill=CYAN, width=2)
        d.ellipse([ccx - 2, ccy - 2, ccx + 2, ccy + 2], fill=INK)
        for i in range(6):  # rain streaks
            rx_ = x + w * 0.58 + i * w * 0.07
            d.line([rx_, y + h * 0.14, rx_ - 4, y + h * 0.42], fill=(140, 180, 230, 130), width=1)
        _palm(x + w * 0.80, y + h * 0.94, h * 0.52, (14, 24, 18), bend=8)
        _palm(x + w * 0.93, y + h * 0.97, h * 0.40, (14, 24, 18), bend=7)
    elif name == "climate":
        sx, sy, sr = x + w * 0.22, y + h * 0.38, h * 0.20
        for a_ in range(0, 360, 45):
            d.line([sx + math.cos(math.radians(a_)) * (sr + 2), sy + math.sin(math.radians(a_)) * (sr + 2),
                    sx + math.cos(math.radians(a_)) * (sr + 6), sy + math.sin(math.radians(a_)) * (sr + 6)],
                   fill=GOLD, width=2)
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=GOLD)
        tx_ = x + w * 0.60                                     # thermometer
        d.rounded_rectangle([tx_ - 3, y + h * 0.10, tx_ + 3, y + h * 0.72], 3, outline=INK, width=2)
        d.rectangle([tx_ - 1.5, y + h * 0.22, tx_ + 1.5, y + h * 0.72], fill=RED)
        d.ellipse([tx_ - 6, y + h * 0.66, tx_ + 6, y + h * 0.66 + 12], fill=RED)
        for k in range(3):
            d.line([tx_ + 5, y + h * (0.2 + k * 0.16), tx_ + 9, y + h * (0.2 + k * 0.16)], fill=MUTED, width=1)
        d.rectangle([x, y + h * 0.80, x + w, y + h], fill=(66, 50, 32))   # cracked earth
        for k in range(5):
            px_ = x + w * (0.08 + k * 0.2)
            d.line([px_, y + h * 0.82, px_ + 7, y + h * 0.90, px_ + 2, y + h * 0.97],
                   fill=(30, 22, 14), width=1)
        for k in range(3):  # heat shimmer
            hx_ = x + w * (0.36 + k * 0.09)
            d.line(bez((hx_, y + h * 0.74), (hx_ + 3, y + h * 0.6), (hx_, y + h * 0.46), 8),
                   fill=(240, 140, 74, 120), width=1)
    elif name == "crash":
        base = y + h * 0.86
        bx = x + 4
        for bw, bh in [(16, 0.30), (12, 0.44), (18, 0.24), (13, 0.52), (16, 0.36), (12, 0.28)]:
            d.rectangle([bx, base - h * bh, bx + bw, base], fill=(11, 15, 29))
            bx += bw + 4
        d.line([x + 4, y + h * 0.60, x + w - 4, y + h * 0.60], fill=(150, 156, 175, 110), width=1)
        candles = [(0.16, 0.30, GREEN), (0.28, 0.38, GREEN), (0.40, 0.34, RED),
                   (0.52, 0.48, RED), (0.64, 0.44, RED), (0.76, 0.62, RED)]
        for fx_, fy_, col in candles:
            px_, py_ = x + w * fx_, y + h * fy_
            d.line([px_, py_ - 5, px_, py_ + 9], fill=col, width=1)
            d.rectangle([px_ - 3, py_ - 3, px_ + 3, py_ + 6], fill=col)
        pts = [(x + w * 0.58, y + h * 0.30), (x + w * 0.74, y + h * 0.52), (x + w * 0.94, y + h * 0.82)]
        d.line(pts, fill=RED, width=3)
        d.polygon([(x + w * 0.94, y + h * 0.82), (x + w * 0.86, y + h * 0.80),
                   (x + w * 0.92, y + h * 0.70)], fill=RED)
    elif name == "ipo":
        base = y + h * 0.88
        bx = x + 4
        for bw, bh in [(14, 0.34), (11, 0.52), (16, 0.28), (12, 0.62), (15, 0.40)]:
            d.rectangle([bx, base - h * bh, bx + bw, base], fill=(11, 15, 29))
            bx += bw + 3
        for i, bh in enumerate([0.18, 0.30, 0.44, 0.60]):
            d.rectangle([x + w * 0.52 + i * w * 0.11, base - h * bh,
                         x + w * 0.59 + i * w * 0.11, base], fill=GREEN)
        pts = [(x + w * 0.50, base - h * 0.30), (x + w * 0.68, base - h * 0.52),
               (x + w * 0.95, base - h * 0.78)]
        d.line(pts, fill=GREEN, width=2)
        d.polygon([(x + w * 0.95, base - h * 0.78), (x + w * 0.88, base - h * 0.76),
                   (x + w * 0.93, base - h * 0.66)], fill=GREEN)
        bellx, belly = x + w * 0.20, y + h * 0.34              # opening bell
        d.arc([bellx - 10, belly - 8, bellx + 10, belly + 10], 180, 360, fill=GOLD, width=2)
        d.rectangle([bellx - 10, belly, bellx + 10, belly + 2], fill=GOLD)
        d.line([bellx - 13, belly + 6, bellx + 13, belly + 6], fill=GOLD, width=2)
        d.ellipse([bellx - 2, belly + 7, bellx + 2, belly + 11], fill=GOLD)
    elif name == "summit":
        bx = x + 6
        for bw, bh in [(15, 0.30), (12, 0.46), (17, 0.36), (12, 0.55), (15, 0.26)]:
            d.rectangle([bx, y + h * 0.66 - h * bh, bx + bw, y + h * 0.66], fill=(13, 17, 32))
            bx += bw + 3
        def flag(px_, kind):
            d.line([px_, y + h * 0.10, px_, y + h * 0.70], fill=MUTED, width=1)
            fw, fh = w * 0.15, h * 0.26
            wave = [(px_, y + h * 0.10), (px_ + fw * 0.5, y + h * 0.07), (px_ + fw, y + h * 0.11),
                    (px_ + fw, y + h * 0.11 + fh), (px_ + fw * 0.5, y + h * 0.13 + fh),
                    (px_, y + h * 0.10 + fh)]
            if kind == "us":
                d.polygon(wave, fill=(178, 34, 52))
                d.rectangle([px_, y + h * 0.10, px_ + fw * 0.42, y + h * 0.10 + fh * 0.5],
                            fill=(40, 54, 122))
            elif kind == "cn":
                d.polygon(wave, fill=(206, 42, 42))
                for ddx, ddy in [(3, 3), (8, 2), (9, 6)]:
                    d.point((px_ + ddx, y + h * 0.10 + ddy), fill=GOLD)
            else:
                d.polygon(wave, fill=(235, 235, 240))
                d.polygon([(px_, y + h * 0.10 + fh / 3), (px_ + fw * 0.5, y + h * 0.075 + fh / 3),
                           (px_ + fw, y + h * 0.115 + fh / 3), (px_ + fw, y + h * 0.115 + fh * 2 / 3),
                           (px_ + fw * 0.5, y + h * 0.135 + fh * 2 / 3), (px_, y + h * 0.10 + fh * 2 / 3)],
                          fill=(52, 84, 168))
                d.polygon([(px_, y + h * 0.10 + fh * 2 / 3), (px_ + fw * 0.5, y + h * 0.135 + fh * 2 / 3),
                           (px_ + fw, y + h * 0.115 + fh * 2 / 3), (px_ + fw, y + h * 0.11 + fh),
                           (px_ + fw * 0.5, y + h * 0.13 + fh), (px_, y + h * 0.10 + fh)], fill=(206, 52, 52))
        flag(x + w * 0.16, "us"); flag(x + w * 0.44, "cn"); flag(x + w * 0.72, "ru")
        d.rectangle([x + w * 0.10, y + h * 0.72, x + w * 0.90, y + h * 0.80], fill=(96, 76, 50))
        d.rectangle([x + w * 0.14, y + h * 0.80, x + w * 0.86, y + h * 0.94], fill=(70, 55, 36))
        for fx_ in (0.26, 0.50, 0.74):
            d.line([x + w * fx_, y + h * 0.72, x + w * fx_, y + h * 0.62], fill=INK, width=1)
            d.ellipse([x + w * fx_ - 2, y + h * 0.58, x + w * fx_ + 2, y + h * 0.58 + 4], fill=INK)
    elif name == "missile":
        sea = y + h * 0.66
        d.rectangle([x, sea, x + w, y + h], fill=(23, 52, 84))
        _waves(x, y, w, sea + 3)
        hx0, hx1 = x + w * 0.06, x + w * 0.52                     # tanker
        d.polygon([(hx0, sea + 2), (hx1, sea + 2), (hx1 - 6, sea + 9), (hx0 + 4, sea + 9)], fill=INK)
        d.rectangle([hx0 + 8, sea - 5, hx0 + 26, sea + 2], fill=INK)
        d.rectangle([hx1 - 14, sea - 8, hx1 - 8, sea + 2], fill=INK)
        d.line([hx0 + 17, sea - 12, hx0 + 17, sea - 5], fill=INK, width=1)
        mx_, my_ = x + w * 0.78, sea - 1                           # naval mine
        mr = max(5, h * 0.13)
        for a_ in range(0, 360, 45):
            d.line([mx_, my_, mx_ + math.cos(math.radians(a_)) * (mr + 3),
                    my_ + math.sin(math.radians(a_)) * (mr + 3)], fill=(200, 90, 80), width=1)
        d.ellipse([mx_ - mr, my_ - mr, mx_ + mr, my_ + mr], fill=(150, 60, 55))
        d.ellipse([mx_ - 2, my_ - 2, mx_ + 2, my_ + 2], fill=(255, 190, 90))
        d.arc([mx_ - 8, my_ + 2, mx_ + 10, my_ + 16], 20, 160, fill=MUTED, width=1)  # chain
        pts = bez((x + w * 0.08, y + h * 0.06), (x + w * 0.4, y + h * 0.02),
                  (x + w * 0.66, y + h * 0.30), 20)               # missile trail
        d.line(pts, fill=(255, 120, 90), width=2)
        ex, ey = pts[-1]
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(255, 220, 150))
    elif name == "game":
        for i, col in enumerate([(58, 30, 62), (104, 44, 66), (156, 66, 62), (206, 104, 62), (232, 140, 66)]):
            d.rectangle([x, y + h * i / 5, x + w, y + h * (i + 1) / 5 + 1], fill=col)
        sx, sy, sr = cx, y + h * 0.66, h * 0.30
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 186, 92))
        d.rectangle([x, y + h * 0.86, x + w, y + h], fill=(16, 14, 26))
        _palm(x + w * 0.10, y + h * 0.92, h * 0.62, (12, 10, 20), bend=-5)
        _palm(x + w * 0.90, y + h * 0.92, h * 0.56, (12, 10, 20), bend=6)
        gx0, gy0, gx1, gy1 = cx - w * 0.17, y + h * 0.34, cx + w * 0.17, y + h * 0.80
        d.rounded_rectangle([gx0, gy0, gx1, gy1], 9, fill=(13, 15, 27), outline=INK, width=2)
        d.line([cx - w * 0.10, cy + h * 0.02, cx - w * 0.10, cy + h * 0.14], fill=INK, width=2)
        d.line([cx - w * 0.135, cy + h * 0.08, cx - w * 0.065, cy + h * 0.08], fill=INK, width=2)
        for ddx, ddy, col in [(0.085, 0.0, RED), (0.125, 0.05, GOLD), (0.045, 0.05, CYAN)]:
            d.ellipse([cx + w * ddx - 2.5, cy + h * ddy - 2.5, cx + w * ddx + 2.5, cy + h * ddy + 2.5],
                      fill=col)
    elif name == "oil":
        gy_ = y + h * 0.84
        d.line([x + 3, gy_, x + w - 3, gy_], fill=MUTED, width=1)
        jx = x + w * 0.08                                          # pumpjack
        d.line([jx, gy_, jx + w * 0.10, y + h * 0.30], fill=INK, width=2)
        d.line([jx + w * 0.20, gy_, jx + w * 0.10, y + h * 0.30], fill=INK, width=2)
        d.line([jx - w * 0.02, y + h * 0.26, jx + w * 0.34, y + h * 0.40], fill=INK, width=3)
        d.arc([jx + w * 0.30, y + h * 0.34, jx + w * 0.40, y + h * 0.52], 270, 90, fill=INK, width=2)
        d.line([jx + w * 0.35, y + h * 0.48, jx + w * 0.35, gy_], fill=INK, width=1)
        bx_, bw_, bh_ = x + w * 0.64, w * 0.15, h * 0.52          # barrel
        d.rounded_rectangle([bx_, gy_ - bh_, bx_ + bw_, gy_], 3, outline=GOLD, width=2)
        d.line([bx_, gy_ - bh_ * 0.66, bx_ + bw_, gy_ - bh_ * 0.66], fill=GOLD, width=1)
        d.line([bx_, gy_ - bh_ * 0.33, bx_ + bw_, gy_ - bh_ * 0.33], fill=GOLD, width=1)
        d.polygon([(bx_ + bw_ / 2, y + h * 0.06), (bx_ + bw_ / 2 + 4, y + h * 0.20),
                   (bx_ + bw_ / 2 - 4, y + h * 0.20)], fill=CYAN)
        pts = [(x + w * 0.06, y + h * 0.14), (x + w * 0.36, y + h * 0.24), (x + w * 0.94, y + h * 0.44)]
        d.line(pts, fill=RED, width=2)
    elif name == "border":
        gy_ = y + h * 0.88
        for i in range(7):
            px_ = x + w * (0.06 + i * 0.15)
            d.line([px_, y + h * 0.14, px_, gy_], fill=MUTED, width=2)
        for k in range(3):
            yy = y + h * (0.28 + k * 0.2)
            d.line([x + w * 0.04, yy, x + w * 0.97, yy], fill=(120, 128, 150, 90), width=1)
        d.line([x + w * 0.04, y + h * 0.16, x + w * 0.97, gy_ - 2], fill=(120, 128, 150, 60), width=1)
        d.line([x + w * 0.04, gy_ - 2, x + w * 0.97, y + h * 0.16], fill=(120, 128, 150, 60), width=1)
        post = x + w * 0.10                                        # barrier arm
        d.rectangle([post - 3, y + h * 0.30, post + 3, gy_], fill=INK)
        ax_, ay_ = post, y + h * 0.34
        ex, ey = x + w * 0.86, y + h * 0.58
        seg = 7
        for i in range(seg):
            t0, t1 = i / seg, (i + 1) / seg
            col = RED if i % 2 == 0 else (235, 235, 240)
            d.line([ax_ + (ex - ax_) * t0, ay_ + (ey - ay_) * t0,
                    ax_ + (ex - ax_) * t1, ay_ + (ey - ay_) * t1], fill=col, width=4)
        d.rectangle([post - 7, y + h * 0.06, post + 12, y + h * 0.24], fill=(240, 140, 74))
        d.line([x + w * 0.03, gy_, x + w * 0.97, gy_], fill=MUTED, width=1)
    elif name == "flags":
        gy_ = y + h * 0.90
        d.line([x + 3, gy_, x + w - 3, gy_], fill=MUTED, width=1)
        cols5 = [(64, 110, 220), GOLD, GREEN, RED, CYAN]
        for i, col in enumerate(cols5):
            px_ = x + w * (0.10 + i * 0.19)
            d.line([px_, y + h * 0.12, px_, gy_], fill=MUTED, width=1)
            d.ellipse([px_ - 1.5, y + h * 0.09, px_ + 1.5, y + h * 0.09 + 3], fill=GOLD)
            fw, fh = w * 0.13, h * 0.24
            d.polygon([(px_, y + h * 0.12), (px_ + fw * 0.55, y + h * 0.09),
                       (px_ + fw, y + h * 0.13), (px_ + fw, y + h * 0.13 + fh),
                       (px_ + fw * 0.55, y + h * 0.15 + fh), (px_, y + h * 0.12 + fh)], fill=col)
    elif name == "bank":
        cx_ = x + w * 0.34
        d.polygon([(cx_, y + h * 0.06), (cx_ - w * 0.20, y + h * 0.24),
                   (cx_ + w * 0.20, y + h * 0.24)], fill=GOLD)
        d.ellipse([cx_ - 3, y + h * 0.10, cx_ + 3, y + h * 0.10 + 6], outline=GOLD, width=1)
        for i in range(4):
            d.rectangle([cx_ - w * 0.16 + i * w * 0.085, y + h * 0.30,
                         cx_ - w * 0.13 + i * w * 0.085, y + h * 0.76], fill=GOLD)
        d.rectangle([cx_ - w * 0.21, y + h * 0.78, cx_ + w * 0.21, y + h * 0.84], fill=GOLD)
        d.rectangle([cx_ - w * 0.23, y + h * 0.88, cx_ + w * 0.23, y + h * 0.93], fill=GOLD)
        ccx, ccy = x + w * 0.76, y + h * 0.34                       # falling coin
        d.ellipse([ccx - 9, ccy - 9, ccx + 9, ccy + 9], outline=GOLD, width=2)
        d.ellipse([ccx - 5, ccy - 5, ccx + 5, ccy + 5], outline=GOLD, width=1)
        pts = [(x + w * 0.58, y + h * 0.58), (x + w * 0.74, y + h * 0.66), (x + w * 0.94, y + h * 0.88)]
        d.line(pts, fill=RED, width=2)
        d.polygon([(x + w * 0.94, y + h * 0.88), (x + w * 0.87, y + h * 0.86),
                   (x + w * 0.92, y + h * 0.77)], fill=RED)
    elif name == "coins":
        base = y + h * 0.90
        d.polygon([(x + w * 0.03, base), (x + w * 0.24, y + h * 0.14),
                   (x + w * 0.45, base)], fill=(86, 68, 38))       # pyramid
        d.polygon([(x + w * 0.24, y + h * 0.14), (x + w * 0.45, base),
                   (x + w * 0.30, base)], fill=(64, 50, 28))
        d.ellipse([x + w * 0.06, y + h * 0.08, x + w * 0.06 + 9, y + h * 0.08 + 9], fill=GOLD)
        for i, sh in enumerate([0.16, 0.30, 0.46]):
            sx_ = x + w * (0.56 + i * 0.15)
            for k in range(int(sh / 0.09) + 1):
                d.ellipse([sx_, base - 6 - k * 5, sx_ + 13, base - k * 5], outline=GOLD, width=1)
        pts = [(x + w * 0.52, y + h * 0.62), (x + w * 0.72, y + h * 0.40), (x + w * 0.95, y + h * 0.16)]
        d.line(pts, fill=GREEN, width=2)
        d.polygon([(x + w * 0.95, y + h * 0.16), (x + w * 0.88, y + h * 0.17),
                   (x + w * 0.93, y + h * 0.26)], fill=GREEN)
    elif name == "island":
        sx, sy, sr = x + w * 0.82, y + h * 0.24, h * 0.13          # hard sun
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=GOLD)
        for a_ in range(0, 360, 60):
            d.line([sx + math.cos(math.radians(a_)) * (sr + 2), sy + math.sin(math.radians(a_)) * (sr + 2),
                    sx + math.cos(math.radians(a_)) * (sr + 5), sy + math.sin(math.radians(a_)) * (sr + 5)],
                   fill=GOLD, width=1)
        d.rectangle([x, y + h * 0.86, x + w, y + h], fill=(23, 52, 84))   # receded sea
        d.arc([x + w * 0.06, y + h * 0.82, x + w * 0.26, y + h * 0.94], 180, 360, fill=CYAN, width=1)
        d.arc([x + w * 0.66, y + h * 0.82, x + w * 0.86, y + h * 0.94], 180, 360, fill=CYAN, width=1)
        d.polygon([(x + w * 0.16, y + h * 0.86), (x + w * 0.34, y + h * 0.60),
                   (x + w * 0.62, y + h * 0.58), (x + w * 0.84, y + h * 0.86)],
                  fill=(100, 80, 44))                                       # dry island
        for k in range(4):  # cracks
            px_ = x + w * (0.30 + k * 0.13)
            d.line([px_, y + h * 0.68, px_ + 5, y + h * 0.76, px_ + 1, y + h * 0.84],
                   fill=(44, 34, 18), width=1)
        _palm(x + w * 0.48, y + h * 0.62, h * 0.44, (120, 96, 50), bend=4, droop=True)
    elif name == "ships":
        sea = y + h * 0.62
        d.rectangle([x, sea, x + w, y + h], fill=(23, 52, 84))
        _waves(x, y, w, sea + 4)
        def tanker(hx0, hx1, col):
            d.polygon([(hx0, sea + 1), (hx1, sea + 1), (hx1 - 5, sea + 8), (hx0 + 3, sea + 8)], fill=col)
            d.rectangle([hx0 + 6, sea - 5, hx0 + 20, sea + 1], fill=col)
            d.rectangle([hx1 - 12, sea - 7, hx1 - 7, sea + 1], fill=col)
        tanker(x + w * 0.03, x + w * 0.40, INK)
        tanker(x + w * 0.60, x + w * 0.97, (178, 184, 200))
        d.arc([x + w * 0.36, y + h * 0.16, x + w * 0.64, y + h * 0.52], 300, 60, fill=GOLD, width=2)
        for t_ in (0.25, 0.5, 0.75):  # droplets along the transfer arc
            a_ = math.radians(300 + (60 - 300) * t_ + 360) % (2 * math.pi)
            ex = x + w * 0.50 + (w * 0.14) * math.cos(math.radians(300 + 120 * t_))
            ey = y + h * 0.34 + (h * 0.18) * math.sin(math.radians(300 + 120 * t_))
            d.ellipse([ex - 1.5, ey - 1.5, ex + 1.5, ey + 1.5], fill=GOLD)
    elif name == "pulsar":
        for i in range(22):  # star field (deterministic)
            sx = x + ((i * 53) % int(w - 8)) + 4
            sy = y + ((i * 29) % int(h - 8)) + 4
            d.point((sx, sy), fill=(230, 233, 245) if i % 3 else GOLD)
        pcx, pcy = x + w * 0.58, y + h * 0.42
        d.polygon([(pcx, pcy), (pcx - w * 0.20, pcy - h * 0.34), (pcx - w * 0.13, pcy - h * 0.40)],
                  fill=(87, 199, 212, 110))
        d.polygon([(pcx, pcy), (pcx + w * 0.20, pcy + h * 0.34), (pcx + w * 0.13, pcy + h * 0.40)],
                  fill=(87, 199, 212, 110))
        for r_ in (7, 12):
            d.arc([pcx - r_, pcy - r_, pcx + r_, pcy + r_], 300, 130, fill=CYAN, width=1)
        d.ellipse([pcx - 3.5, pcy - 3.5, pcx + 3.5, pcy + 3.5], fill=INK)
        dx_, dy_ = x + w * 0.16, y + h * 0.80                        # radio dish
        d.arc([dx_ - 13, dy_ - 12, dx_ + 13, dy_ + 10], 300, 130, fill=INK, width=2)
        d.line([dx_ - 11, dy_ - 7, dx_ + 4, dy_ - 2], fill=INK, width=1)
        d.line([dx_ + 11, dy_ - 7, dx_ + 4, dy_ - 2], fill=INK, width=1)
        d.polygon([(dx_ - 3, dy_ + 4), (dx_ + 3, dy_ + 4), (dx_, dy_ + 11)], fill=INK)
        for t_ in (0.3, 0.55, 0.8):  # signal path dish -> pulsar
            sx = dx_ + (pcx - dx_) * t_
            sy = dy_ - 4 + (pcy - dy_ + 4) * t_
            d.ellipse([sx - 1.2, sy - 1.2, sx + 1.2, sy + 1.2], fill=(87, 199, 212, 170))

PY = RY + RH + 8
ROW_H = [122, 102, 102]
cols = 5
gap = 8
cw = (W - 2 * M - (cols - 1) * gap) / cols
row_y = [PY]
for rh_ in ROW_H[:-1]:
    row_y.append(row_y[-1] + rh_ + gap)
for i, p in enumerate(PANELS):
    r, c = divmod(i, cols)
    x0 = M + c * (cw + gap); y0 = row_y[r]
    x1, y1 = x0 + cw, y0 + ROW_H[r]
    d.rectangle([x0, y0, x1, y1], fill=PANEL)
    rc = REGION_COLORS[p["region"]]
    d.rectangle([x0, y0, x0 + 3, y1], fill=rc)
    big = (r == 0)
    sh = 48 if big else 32                     # scene strip height
    scene(p["icon"], x0 + 3, y0, cw - 3, sh)
    # number badge + place, overlaid on the scene
    br = 13 if big else 11
    bcx, bcy = x0 + 9 + br, y0 + sh / 2
    d.ellipse([bcx - br, bcy - br, bcx + br, bcy + br], fill=RED, outline=(8, 10, 18), width=2)
    nf = F("oswB", 15 if big else 12.5)
    num = str(p["n"])
    d.text((bcx - tw(num, nf) / 2, bcy - nf.size / 2 - 1), num, font=nf, fill=(255, 255, 255))
    tf = F("pjB", 8)
    place = ellipsize(p["place"], tf, (x1 - 6) - (bcx + br + 6))
    pw_ = tw(place, tf)
    d.rectangle([bcx + br + 3, bcy - 8, bcx + br + 9 + pw_, bcy + 9], fill=(8, 10, 20, 165))
    d.text((bcx + br + 6, bcy - 4.5), place, font=tf, fill=(226, 229, 238))
    # tag row: proof tag + region + source
    ty = y0 + sh + 5
    tcol = GREEN if p["tag"] == "CONFIRMED" else (GOLD if p["tag"] == "ESTIMATE" else RED)
    x = chip(x0 + 8, ty, p["tag"], F("pjB", 7.5), tcol, bg=(16, 20, 36))
    rf = F("pjB", 7.5)
    d.text((x + 5, ty + 1), p["region"], font=rf, fill=rc)
    d.text((x + 5 + tw(p["region"], rf) + 5, ty + 1), "· " + p["src"], font=F("pjM", 7.5), fill=FAINT)
    # headline + summary
    hyy = text_block(x0 + 8, ty + 13, p["head"], F("oswS", 12), INK, cw - 15, 14.5, 2)
    text_block(x0 + 8, hyy + 1, p["summ"], F("pjR", 8.6), (196, 200, 214), cw - 15, 10.7, 2)

PANEL_END = row_y[-1] + ROW_H[-1]

# ---------------------------------------------------------------- map band: three dot-globes
BY = PANEL_END + 8
BH = 120
d.rectangle([M, BY, W - M, BY + BH], fill=PANEL)
f = F("pjXB", 11)
d.text((M + 10, BY + 5), "WHERE IT HAPPENED — HERO + 15 PANELS, PINNED", font=f, fill=INK)
d.text((M + 330, BY + 5), "dot-globes, drawn in code", font=F("pjM", 9), fill=FAINT)

BLOBS = [  # (lon, lat, rx, ry) rough continent ellipses
    (-100, 49, 30, 12), (-86, 39, 15, 8), (-155, 64, 11, 5), (-42, 74, 9, 5),
    (-88, 21, 7, 4), (-84, 15, 5, 3),
    (-62, -11, 11, 13), (-69, -26, 6, 10), (-53, -4, 8, 6),
    (15, 52, 17, 8), (11, 63, 10, 5), (-4, 43, 6, 4), (20, 41, 7, 4),
    (20, 7, 17, 15), (25, -19, 11, 10), (47, 4, 6, 6), (47, -19, 2.5, 4),
    (62, 52, 36, 12), (95, 47, 26, 10), (106, 33, 13, 9), (78, 21, 6.5, 7),
    (45, 25, 9, 6), (35, 39, 7, 4), (102, 15, 5, 6), (115, -2, 11, 2.5),
    (138, 37, 4, 4), (122, 13, 3, 4),
    (134, -25, 12, 6), (172, -42, 2.5, 3),
]
def is_land(lon, lat):
    lon = (lon + 180) % 360 - 180
    return any(((lon - lo) / rx) ** 2 + ((lat - la) / ry) ** 2 <= 1
               for lo, la, rx, ry in BLOBS)

def project(lon, lat, clon, clat):
    """Orthographic projection -> (x, y) in unit disc, y up; None if back side."""
    la, lo = math.radians(lat), math.radians(lon)
    la0, lo0 = math.radians(clat), math.radians(clon)
    cosc = math.sin(la0) * math.sin(la) + math.cos(la0) * math.cos(la) * math.cos(lo - lo0)
    if cosc <= 0.02:
        return None
    return (math.cos(la) * math.sin(lo - lo0),
            math.cos(la0) * math.sin(la) - math.sin(la0) * math.cos(la) * math.cos(lo - lo0))

def unproject(X, Y, clon, clat):
    rho = math.hypot(X, Y)
    if rho < 1e-9:
        return clon, clat
    la0, lo0 = math.radians(clat), math.radians(clon)
    c = math.asin(min(1, rho))
    lat = math.degrees(math.asin(math.cos(c) * math.sin(la0)
                                 + Y * math.sin(c) * math.cos(la0) / rho))
    lon = math.degrees(lo0 + math.atan2(X * math.sin(c),
                                        rho * math.cos(la0) * math.cos(c)
                                        - Y * math.sin(la0) * math.sin(c)))
    return lon, lat

GLOBES = [(-95, 18, "AMERICAS"), (18, 26, "EUROPE · AFRICA"), (105, 12, "ASIA · OCEANIA")]
GR = 46
GCY = BY + 64
GCXS = [118 + M, 294 + M, 470 + M]
NUDGE = {(0, 4): (5, -3), (0, 15): (-4, 4), (0, 13): (-6, -4),
         (1, "H"): (3, -1), (1, 9): (-2, -4), (1, 6): (4, 3), (1, 12): (-2, -2)}

def globe_idx(lon):
    if lon <= -30: return 0
    if lon < 62: return 1
    return 2

for gi, (clon, clat, label) in enumerate(GLOBES):
    cxg = GCXS[gi]
    d.ellipse([cxg - GR, GCY - GR, cxg + GR, GCY + GR], fill=(14, 19, 36),
              outline=(70, 82, 110), width=1)
    step = 3.3
    gy_ = -GR + 1.6
    while gy_ <= GR - 1:
        gx_ = -GR + 1.6
        while gx_ <= GR - 1:
            if gx_ ** 2 + gy_ ** 2 <= (GR - 1.5) ** 2:
                lon, lat = unproject(gx_ / GR, -gy_ / GR, clon, clat)
                if is_land(lon, lat):
                    d.ellipse([cxg + gx_ - 1.5, GCY + gy_ - 1.5, cxg + gx_ + 1.5, GCY + gy_ + 1.5],
                              fill=(92, 108, 144))
                elif (round(gx_ * 10) + round(gy_ * 10)) % 3 == 0:
                    d.point((cxg + gx_, GCY + gy_), fill=(26, 34, 58))
            gx_ += step
        gy_ += step
    lf = F("pjB", 7.5)
    d.text((cxg - tw(label, lf) / 2, BY + 111), label, font=lf, fill=MUTED)

def draw_pin(gi, key, lon, lat, text, hero=False):
    pr = project(lon, lat, GLOBES[gi][0], GLOBES[gi][1])
    if pr is None: return
    px = GCXS[gi] + pr[0] * GR
    py = GCY - pr[1] * GR
    ox, oy = NUDGE.get((gi, key), (0, 0))
    px, py = px + ox, py + oy
    r_ = 6.5 if hero else 5
    d.ellipse([px - r_, py - r_, px + r_, py + r_],
              fill=GOLD if hero else RED, outline=(8, 10, 18), width=1)
    nf = F("oswB", 9 if hero else 7.5)
    d.text((px - tw(text, nf) / 2, py - nf.size / 2 - 0.5), text, font=nf,
           fill=(10, 13, 26) if hero else (255, 255, 255))

draw_pin(1, "H", 30.5, 50.4, "H", hero=True)
for p in PANELS:
    draw_pin(globe_idx(p["pin"][0]), p["n"], p["pin"][0], p["pin"][1], str(p["n"]))

# date check + how we count (right of globes)
DX = M + 540
DW = W - M - DX
f = F("pjXB", 11)
d.text((DX, BY + 5), "DATE CHECK ✔", font=f, fill=GREEN)
text_block(DX, BY + 22,
    "Verified three ways before publication: Reuters wire datelines read “Nov 20” from Kyiv, "
    "Hong Kong and London; India's IMD bulletin dates Cyclone Akvan's landfall to 20 November; "
    "UN News' COP31 daily is dated Friday. Calendar cross-check: 20 Nov 2026 is a Friday.",
    F("pjR", 9.3), (196, 200, 214), DW, 12, 6)
d.line([DX, BY + 100, W - M, BY + 100], fill=FAINT, width=1)
d.text((DX, BY + 105),
       "PINS — gold H = the hero (Kyiv) · red 1–15 = the panels above, in order.",
       font=F("pjM", 8.6), fill=MUTED)

# ---------------------------------------------------------------- ALSO band
AY = BY + BH + 8
d.rectangle([M, AY, W - M, 985], fill=PANEL)
f = F("pjXB", 12)
d.text((M + 10, AY + 5), "ALSO ON THE WIRE — 28 MORE STORIES", font=f, fill=INK)
d.text((M + 310, AY + 7), "numbered 16–43 · 44 total = 1 hero + 15 panels + 28 briefs", font=F("pjM", 9), fill=FAINT)
BRIEFS = [
    (16, "EUROPE", "PRAGUE", "Mass march defends free media", "Munich Eye"),
    (17, "EUROPE", "BRUSSELS", "EU delays methane import rules 2 yrs", "OlivLaw"),
    (18, "EUROPE", "BRUSSELS", "AI cyberattack disrupts Commission", "OlivLaw"),
    (19, "EUROPE", "HAMBURG", "Metalworkers' first strike in 8 yrs", "Europa Exp."),
    (20, "EUROPE", "THE HAGUE", "Dutch summon Russian envoy", "The Times"),
    (21, "EUROPE", "LONDON", "E3 urges winter energy ceasefire", "The Times"),
    (22, "EUROPE", "FRANKFURT", "Lagarde farewell: pay upfront", "Europa Exp."),
    (23, "EUROPE", "PARIS", "Youth protests span 25+ countries", "Europa Exp."),
    (24, "N AMERICA", "NEW YORK", "S&P 500: sixth straight daily fall", "Reuters"),
    (25, "N AMERICA", "SACRAMENTO", "California probes Nvidia–China claim", "CNBC"),
    (26, "N AMERICA", "WASHINGTON", "Trump: will meet Kim “at some point”", "NBC News"),
    (27, "N AMERICA", "NEW YORK", "Gold, silver at one-year lows", "Dow Jones"),
    (28, "ASIA", "TAIPEI", "Taiex −6.75%; MediaTek −10%", "Reuters"),
    (29, "ASIA", "KOLKATA", "Akvan remnants drench Kolkata", "Hindu BL"),
    (30, "AFRICA", "NAIROBI", "Opposition walks out of IEBC talks", "The Standard"),
    (31, "AFRICA", "PRAIA", "Neves wins 2nd term with ~64%", "Afr. Spectator"),
    (32, "AFRICA", "DAKAR", "Youth Olympics open — first in Africa", "Nation Africa"),
    (33, "AFRICA", "OLD DONGOLA", "Medieval cathedral floor uncovered", "Nation Africa"),
    (34, "AFRICA", "HARARE", "250,000 landmines destroyed", "Nation Africa"),
    (35, "AFRICA", "ADDIS ABABA", "Ethiopia–Eritrea border build-up", "Afr. Spectator"),
    (36, "AFRICA", "NAIROBI", "Solar imports 26 GW, installs 10 GW", "IEA"),
    (37, "S AMERICA", "MATO GROSSO", "Lula recognises Raoni's lands", "One Turn"),
    (38, "S AMERICA", "RIO", "Tourism target beaten 2 months early", "Embratur"),
    (39, "S AMERICA", "SÃO PAULO", "Norris wins GP; Mercedes champions", "Al Jazeera"),
    (40, "S AMERICA", "UBERLÂNDIA", "53 red cards: world-record brawl", "Al Jazeera"),
    (41, "S AMERICA", "BOGOTÁ", "UN: Colombia peace deal under strain", "UN"),
    (42, "OCEANIA", "PERTH", "Lab-hatched turtle survives wild", "Scimex"),
    (43, "ASIA", "ANTALYA", "Bowen: negotiate “until consensus”", "AFP"),
]
acols = 4
acw = (W - 2 * M - 20) / acols
bf_p, bf_h, bf_s = F("pjB", 9.0), F("pjR", 9.0), F("pjM", 8.2)
for i, (n, region, place, head, src) in enumerate(BRIEFS):
    col, row = divmod(i, 7)
    x = M + 10 + col * acw
    yy = AY + 24 + row * 11.6
    rc = REGION_COLORS[region]
    s = f"{n} {place}"
    d.text((x, yy), s, font=bf_p, fill=rc)
    hx2 = x + tw(s, bf_p) + 4
    avail = (M + 10 + (col + 1) * acw - 6) - hx2
    head_e = ellipsize(head, bf_h, avail - tw(" · " + src, bf_s) - 2)
    d.text((hx2, yy), head_e, font=bf_h, fill=(214, 208, 192))
    d.text((hx2 + tw(head_e, bf_h) + 2, yy), "· " + src, font=bf_s, fill=FAINT)

# ---------------------------------------------------------------- footer
fy = 991
f = F("pjM", 8.6)
srcs = ("SOURCES — Reuters · CNN · UN News · The Times · Bloomberg · AFP · NBC News · CNBC · VGC · NASA · "
        "RNZ Pacific · Al Jazeera · The Standard · Nation Africa · Egypt Independent")
tail = "THE MIDNIGHT WIRE · generated offline in code · © 2026"
d.text((W - M - tw(tail, f), fy), tail, font=f, fill=FAINT)
d.text((M, fy), ellipsize(srcs, f, W - 2 * M - tw(tail, f) - 14), font=f, fill=MUTED)
d.text((M, fy + 13), "Also: OlivLaw · Europa Express · One Turn News · Embratur · Hindu BusinessLine · The Munich Eye · Sensor Tower · Dow Jones · PRL · IEA · Scimex — full story file: candidates/stories.md in this repo.", font=f, fill=FAINT)

img.save(OUT)
print("saved", OUT, img.size)
