#!/usr/bin/env python3
"""news-image-20261122 — B16 utc-timeline. Draws the 1024x1024 front page with PIL."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (26, 26, 26)
RED = (164, 30, 34)
DARKBLUE = (31, 58, 95)
GREY = (90, 90, 90)
OCEAN = (207, 227, 238)
LAND = (232, 220, 192)
LANDLINE = (184, 169, 122)

FDIR = "/usr/share/fonts/truetype/dejavu"

def fserif(bold, size):
    return ImageFont.truetype(os.path.join(FDIR, "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"), size)

def fsans(bold, size):
    return ImageFont.truetype(os.path.join(FDIR, "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)

def wrap(d, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

CHIPCOL = {"CONFIRMED": (39, 103, 73), "REPORTED": (43, 108, 176), "CLAIM": (183, 121, 31),
           "OFFICIAL": (74, 85, 104), "FORECAST": (107, 70, 193), "ONGOING": (180, 83, 9),
           "PENDING": (113, 113, 113)}

def chip(d, x, y, label):
    f = fsans(True, 9)
    w = int(d.textlength(label, font=f)) + 10
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=CHIPCOL[label])
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w

def scene_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 58, 92))
    d.ellipse([x + w // 2 - 26, y + 8, x + w // 2 + 26, y + 60], fill=(120, 170, 210))
    d.line([x + w // 2 - 26, y + 34, x + w // 2 + 26, y + 34], fill=(38, 58, 92), width=2)
    d.line([x + w // 2 - 8, y + 12, x + w // 2 + 14, y + 56], fill=(38, 58, 92), width=2)
    # flags row
    cols = [(164, 30, 34), (255, 255, 255), (43, 108, 176), (255, 200, 40), (39, 103, 73), (200, 120, 40)]
    for i, c in enumerate(cols):
        fx = x + 14 + i * 52
        d.line([fx, y + h - 26, fx, y + h - 8], fill=(220, 220, 220), width=2)
        d.rectangle([fx, y + h - 26, fx + 34, y + h - 14], fill=c)
    # hall base
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(20, 32, 54))

def scene_drones(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 22, 48))
    # moon
    d.ellipse([x + w - 52, y + 8, x + w - 20, y + 40], fill=(240, 230, 180))
    # buildings
    import random
    rnd = random.Random(7)
    bx = x + 6
    while bx < x + w - 30:
        bw = rnd.randint(22, 40)
        bh = rnd.randint(22, 52)
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(40, 48, 80))
        for wy in range(y + h - bh + 5, y + h - 4, 9):
            for wx in range(bx + 4, bx + bw - 4, 9):
                if rnd.random() < 0.5:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 200, 90))
        bx += bw + 4
    # explosion
    ex, ey = x + w // 2 + 30, y + 18
    d.ellipse([ex - 14, ey - 12, ex + 14, ey + 12], fill=(255, 140, 40))
    d.ellipse([ex - 7, ey - 6, ex + 7, ey + 6], fill=(255, 220, 120))
    # drones
    for dx, dy in [(x + 40, y + 14), (x + 90, y + 8), (x + w - 90, y + 30)]:
        d.polygon([(dx, dy), (dx + 12, dy + 4), (dx, dy + 8)], fill=(255, 90, 60))
        d.line([dx, dy + 4, dx - 22, dy + 10], fill=(255, 90, 60), width=1)

def scene_radar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 26, 52))
    d.ellipse([x + 18, y + 10, x + 42, y + 34], fill=(235, 225, 175))
    # radar dish
    cx, cy = x + w // 2 + 10, y + h - 26
    d.pieslice([cx - 44, cy - 44, cx + 44, cy + 44], start=200, end=340, fill=(180, 185, 195))
    d.line([cx, cy, cx + 34, cy - 34], fill=(220, 225, 235), width=3)
    d.line([cx - 6, cy, cx + 6, cy], fill=(150, 155, 165), width=3)
    d.rectangle([cx - 3, cy, cx + 3, y + h], fill=(150, 155, 165))
    # fire glow at base
    d.ellipse([x + w - 62, y + h - 22, x + w - 26, y + h - 2], fill=(255, 140, 40))
    d.ellipse([x + w - 52, y + h - 16, x + w - 36, y + h - 4], fill=(255, 220, 120))
    # ground lights
    for gx in range(x + 8, x + w - 8, 26):
        d.ellipse([gx, y + h - 6, gx + 4, y + h - 2], fill=(255, 200, 90))

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 5], fill=RED)

    # ---- masthead ----
    d.text((16, 10), "THE WORLD IN ONE DAY", font=fsans(True, 13), fill=RED)
    d.text((W - 16 - d.textlength("36 STORIES · 7 REGIONS", font=fsans(True, 13)), 10),
           "36 STORIES · 7 REGIONS", font=fsans(True, 13), fill=INK)
    d.text((16, 26), "Sunday 22 November 2026", font=fserif(True, 34), fill=INK)
    d.text((16, 64), "COP31 fails  ·  186 drones  ·  Bahrain radar claim — the day the world said no",
           font=fsans(True, 13), fill=RED)

    # ---- number strip ----
    strip = [("186", "drones fired"), ("161", "shot down"), ("720/9", "India declare"),
             ("98.79%", "HK turnout"), ("$120bn", "adaptation dropped"), ("35%", "2035 power kept"),
             ("44h", "COP31 overtime"), ("258", "Dems seats")]
    x0, y0, cw = 16, 84, 124
    for i, (num, lab) in enumerate(strip):
        x = x0 + i * cw
        fnum = fserif(True, 26 if len(num) <= 5 else 22)
        d.text((x + (cw - d.textlength(num, font=fnum)) / 2, y0), num, font=fnum, fill=INK)
        fl = fsans(False, 10)
        d.text((x + (cw - d.textlength(lab, font=fl)) / 2, y0 + 30), lab, font=fl, fill=GREY)
        if i:
            d.line([x, y0 + 2, x, y0 + 42], fill=(200, 190, 170), width=1)
    d.line([16, 130, 1008, 130], fill=INK, width=1)

    # ---- region bar ----
    regs = [("EUROPE 8", (43, 108, 176)), ("MIDDLE EAST 7", (192, 86, 33)), ("ASIA-PACIFIC 7", (47, 133, 90)),
            ("AMERICAS 5", (107, 70, 193)), ("AFRICA 3", (151, 90, 22)), ("OCEANIA 3", (44, 122, 123)),
            ("WORLD 3", (74, 85, 104))]
    x = 16
    fb = fsans(True, 11)
    for lab, col in regs:
        w = int(d.textlength(lab, font=fb)) + 18
        d.rectangle([x, 134, x + w, 152], fill=col)
        d.text((x + 9, 137), lab, font=fb, fill=(255, 255, 255))
        x += w + 2

    # ---- UTC strip ----
    d.text((16, 156), "THE DAY IN UTC", font=fsans(True, 11), fill=RED)
    utc = "01:00 HK polls open   ·   03:00 COP31 objections close   ·   06:00 adoption vote   ·   ~16:00 COP31 fails   ·   18:13 Dems 258   ·   20:43 Alcaraz wins"
    d.text((150, 156), utc, font=fsans(False, 11), fill=INK)

    # ---- 24h timeline spine ----
    d.text((16, 176), "24 HOURS IN UTC — THE DAY UNFOLDS", font=fsans(True, 11), fill=INK)
    nodes = [("OVERNIGHT", "186 drones over Ukraine"), ("01:00", "HK polls open"),
             ("03:00", "COP31 objections close"), ("06:00", "Adoption vote · Cikande fire"),
             ("12:00", "India 720/9 · Wembanyama 50"), ("~16:00", "COP31 fails — NO DEAL"),
             ("17:00", "Alcaraz wins · Dems 258"), ("~20:00", "Bahrain radar claim"),
             ("23:00", "Ebola 11,613 · Bitcoin $60k")]
    ly = 214
    d.line([60, ly, 964, ly], fill=RED, width=2)
    seg = (964 - 60) / (len(nodes) - 1)
    ftime = fsans(True, 10)
    fstory = fsans(False, 9)
    for i, (t, s) in enumerate(nodes):
        nx = 60 + i * seg
        d.ellipse([nx - 5, ly - 5, nx + 5, ly + 5], fill=RED)
        tw = d.textlength(t, font=ftime)
        tx = min(max(nx - tw / 2, 16), 1008 - tw)
        d.text((tx, 192), t, font=ftime, fill=RED)
        lines = wrap(d, s, fstory, 100)
        for j, ln in enumerate(lines[:2]):
            lw = d.textlength(ln, font=fstory)
            lx = min(max(nx - lw / 2, 16), 1008 - lw)
            d.text((lx, 224 + j * 11), ln, font=fstory, fill=INK)
    d.line([16, 248, 1008, 248], fill=(200, 190, 170), width=1)

    # ---- heroes ----
    heroes = [
        ("ANTALYA · POLITICS", "COP31 collapses — NO DEAL",
         "Final text drops all fossil-fuel language; the EU and ~130 parties refuse it. Talks end after 44 hours overtime — the first summit to fail since 2009.",
         "CONFIRMED", "Source: AP · Reuters · Guardian", scene_cop31),
        ("KYIV · WAR", "186 drones fired, 161 shot down",
         "Russia fires 186 drones overnight; 161 shot down or jammed. A five-storey flat in Dymer falls: 1 dead, 14 unaccounted for. Strikes hit 18 sites.",
         "REPORTED", "Source: Ukrainian Air Force · AP", scene_drones),
        ("BAHRAIN · WAR", "Iran claims 2 Patriot radars hit",
         "Tehran says US Patriot radars at al-Riffa and Awali were hit. Bahrain denies a military strike — a civilian site at Sitra burns, 2 hurt, no deaths.",
         "CLAIM", "Source: IRGC vs Bahrain MoI · Reuters", scene_radar),
    ]
    hx, hy, hw = 16, 256, 326
    for i, (kick, title, body, chipl, src, fn) in enumerate(heroes):
        x = hx + i * (hw + 2)
        fn(d, x, hy, hw, 66)
        d.text((x, hy + 72), kick, font=fsans(True, 10), fill=RED)
        ftitle = fserif(True, 16)
        for j, ln in enumerate(wrap(d, title, ftitle, hw)[:2]):
            d.text((x, hy + 86 + j * 19), ln, font=ftitle, fill=INK)
        fbody = fsans(False, 11)
        for j, ln in enumerate(wrap(d, body, fbody, hw)[:3]):
            d.text((x, hy + 126 + j * 13), ln, font=fbody, fill=INK)
        cw_ = chip(d, x, hy + 168, chipl)
        d.text((x + cw_ + 6, hy + 170), src, font=fsans(False, 9), fill=GREY)
        d.line([x, hy + 186, x + hw, hy + 186], fill=(200, 190, 170), width=1)

    # ---- small cards (2 rows x 5) ----
    cards = [
        ("HONG KONG · POLITICS", "Hong Kong votes: 98.79% turnout", "856 candidates, 723 seats.", "CONFIRMED", "SCMP · Reuters", (43, 108, 176)),
        ("LAS VEGAS · SPORT", "Verstappen wins by 0.639s", "Beats Norris; Piastri 3rd; 75th win.", "CONFIRMED", "F1 · Reuters", (47, 133, 90)),
        ("TURIN · SPORT", "Alcaraz takes ATP Finals", "Beats Zverev 6–2, 7–6(7); first title.", "CONFIRMED", "ATP · BBC", (47, 133, 90)),
        ("NEW ZEALAND · SPORT", "India declare 720/9", "Highest Test total in NZ; Rahul 136.", "CONFIRMED", "ESPNcricinfo", (47, 133, 90)),
        ("CIKANDE · SOCIETY", "Candy-factory fire: 3 dead, 36 missing", "Fire began Sat. night; 15 survived.", "REPORTED", "Detiknews · Basarnas", (192, 86, 33)),
        ("TEHRAN · SOCIETY", "Iran starts power rationing", "Blackouts ~2h a day; gas output hit.", "REPORTED", "Reuters", (192, 86, 33)),
        ("SEOUL · SOCIETY", "Minister quits in AI-cheat scandal", "111 device cases; Choi resigns.", "CONFIRMED", "Yonhap", (192, 86, 33)),
        ("CAPE CANAVERAL · SCIENCE", "Falcon 9 launches NROL-136", "Record 32h turnaround; booster lands.", "OFFICIAL", "SpaceX", (74, 85, 104)),
        ("DR CONGO · HEALTH", "Ebola cases reach 11,613", "WHO count; fighting traps medics.", "OFFICIAL", "WHO · Reuters", (151, 90, 22)),
        ("LIVERPOOL · SPORT", "Liverpool rout Man Utd 4–0", "Pochettino debut ends in a rout.", "CONFIRMED", "BBC Sport", (47, 133, 90)),
    ]
    cardw, cardh = 196, 66
    for idx, (kick, title, body, chipl, src, col) in enumerate(cards):
        r, c = divmod(idx, 5)
        x = 16 + c * (cardw + 2)
        y = 448 + r * (cardh + 2)
        d.rectangle([x, y, x + cardw, y + cardh], outline=(200, 190, 170), width=1)
        d.rectangle([x, y, x + cardw, y + 12], fill=col)
        d.text((x + 4, y + 1), kick, font=fsans(True, 8), fill=(255, 255, 255))
        ftitle = fsans(True, 11)
        tlines = wrap(d, title, ftitle, cardw - 8)[:2]
        for j, ln in enumerate(tlines):
            d.text((x + 4, y + 15 + j * 13), ln, font=ftitle, fill=INK)
        by = y + 15 + len(tlines) * 13
        fbody = fsans(False, 9)
        while body and d.textlength(body, font=fbody) > cardw - 8:
            body = body[:-1]
        d.text((x + 4, by), body, font=fbody, fill=INK)
        cw_ = chip(d, x + 4, y + cardh - 16, chipl)
        d.text((x + 4 + cw_ + 4, y + cardh - 14), src, font=fsans(False, 8), fill=GREY)

    # ---- map + ALSO ----
    my0, my1, mx0, mx1 = 610, 826, 16, 428
    d.text((16, 590), "THE WORLD — WHERE IT HAPPENED", font=fsans(True, 11), fill=RED)
    d.text((mx1 - d.textlength("pin = story number", font=fsans(False, 9)), 592),
           "pin = story number", font=fsans(False, 9), fill=GREY)
    d.rectangle([mx0, my0, mx1, my1], fill=OCEAN, outline=(180, 190, 200), width=1)

    def lonlat(lon, lat):
        return (mx0 + (lon + 180) / 360 * (mx1 - mx0), my0 + (90 - lat) / 180 * (my1 - my0))

    continents = [
        [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70), (-75, 62), (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35), (-80, 32), (-85, 30), (-90, 21), (-97, 16), (-105, 20), (-115, 23), (-125, 32), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
        [(-58, 64), (-45, 60), (-40, 70), (-30, 76), (-20, 70), (-25, 65), (-45, 60)],
        [(-80, 10), (-75, 5), (-60, 10), (-50, 5), (-35, -5), (-40, -20), (-50, -30), (-60, -38), (-70, -45), (-73, -50), (-70, -55), (-65, -45), (-70, -35), (-75, -20), (-80, -10)],
        [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15), (48, 11), (51, 12), (44, 0), (40, -10), (35, -20), (32, -28), (25, -34), (18, -35), (12, -18), (9, -1), (9, 4), (-8, 5)],
        [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 70), (40, 68), (45, 65), (40, 60), (35, 55), (30, 50), (28, 45), (23, 40), (20, 40), (15, 44), (12, 44), (8, 44), (3, 42), (0, 38), (-5, 36)],
        [(30, 70), (40, 68), (50, 70), (60, 70), (70, 72), (80, 73), (90, 75), (100, 77), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 66), (170, 66), (178, 65), (170, 60), (162, 60), (158, 53), (150, 60), (142, 50), (140, 40), (135, 35), (130, 33), (127, 35), (122, 30), (120, 25), (115, 22), (110, 20), (108, 12), (105, 8), (100, 7), (97, 10), (95, 16), (92, 21), (90, 22), (88, 22), (85, 19), (80, 13), (77, 8), (75, 12), (72, 20), (70, 23), (66, 25), (62, 25), (58, 26), (56, 27), (52, 28), (50, 30), (48, 30), (44, 29), (42, 30), (40, 32), (38, 36), (36, 36), (33, 36), (30, 36), (30, 42), (28, 45), (30, 50), (32, 55), (35, 58), (38, 62), (40, 68)],
        [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32), (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (150, -27), (146, -19), (142, -11), (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
        [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (-1, 51)],
    ]
    for poly in continents:
        d.polygon([lonlat(lon, lat) for lon, lat in poly], fill=LAND, outline=LANDLINE)
    # grid
    for lon in range(-150, 181, 30):
        gx, _ = lonlat(lon, 0)
        d.line([gx, my0, gx, my1], fill=(255, 255, 255), width=1)
    for lat in range(-60, 91, 30):
        _, gy = lonlat(0, lat)
        d.line([mx0, gy, mx1, gy], fill=(255, 255, 255), width=1)

    # pins: (num, lon, lat, dx, dy, claim?)
    pins = [(1, 30.5, 50.4, 0, 0, False), (2, 114.2, 22.3, 0, 0, False), (3, -115.1, 36.2, 0, 0, False),
            (4, 7.7, 45.1, 0, 12, False), (5, 24.7, 59.4, 10, -6, False), (6, 12.6, 55.7, 10, -8, False),
            (7, 4.4, 50.8, -14, 0, False), (8, 20.0, 36.0, 0, 12, False), (9, 30.7, 36.9, 0, 12, False),
            (10, 50.6, 26.2, 12, 0, True), (11, 20.1, 32.1, -12, 8, True), (12, 51.4, 35.7, 12, -6, False),
            (13, 34.5, 31.5, -2, -12, False), (14, 34.8, 32.1, 12, -10, False), (15, 35.2, 32.0, 14, 8, False),
            (16, 106.3, -6.2, 0, 0, False), (17, 174.8, -41.3, 0, 0, False), (18, 127.0, 37.5, 0, 0, False),
            (19, 77.2, 28.6, 0, 0, False), (20, 93.9, 24.8, 10, 8, False), (21, 106.8, -6.2, 0, 12, False),
            (22, 149.1, -35.3, 0, 0, False), (23, -77.0, 38.9, 0, 0, False), (24, -47.9, -15.8, 0, 0, False),
            (25, -98.5, 29.4, 0, 0, False), (26, -80.6, 28.4, 0, 0, False), (27, -122.3, 47.6, 0, 0, False),
            (28, 32.5, 15.5, 0, 0, False), (29, 6.3, 4.8, 0, 0, False), (30, 23.5, -2.9, 0, 0, False),
            (31, 145.0, -37.8, -12, 0, False), (32, 151.2, -33.9, 10, -10, False), (33, 151.2, -33.9, 12, 10, False),
            (34, 0.0, 51.5, 0, 0, False), (35, -122.4, 37.4, 0, 12, False), (36, -3.0, 53.4, -12, -8, False)]
    fpin = fsans(True, 8)
    for num, lon, lat, dx, dy, claim in pins:
        px, py = lonlat(lon, lat)
        cx, cy = px + dx, py + dy
        if dx or dy:
            d.line([px, py, cx, cy], fill=(120, 120, 120), width=1)
        col = (183, 121, 31) if claim else (164, 30, 34)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=col, outline=(255, 255, 255), width=1)
        t = str(num)
        d.text((cx - d.textlength(t, font=fpin) / 2, cy - 5), t, font=fpin, fill=(255, 255, 255))

    # ALSO list
    ax0 = 440
    d.text((ax0, 590), "ALSO ON SUNDAY — 23 MORE STORIES", font=fsans(True, 11), fill=RED)
    also = [(5, "Estonia closes 5 Russia crossings"), (6, "Denmark expels Russian attaché"),
            (7, "Belgium controllers join Monday strike"), (8, "Sparta II still burning, towed home"),
            (11, "Merkury corvette hit off Benghazi"), (13, "Gaza: 4 killed; aid-van strike kills 3"),
            (14, "Eisenkot invites Likud to coalition talks"), (15, "Settlers torch 12 cars in West Bank"),
            (19, "Nepal PM lands in Delhi, first trip abroad"), (20, "Manipur liquor toll rises; ~600 treated"),
            (21, "EU–Indonesia deal signed (date split)"), (22, "Marles rejects US AUKUS sub report"),
            (23, "Democrats take House: 258 seats"), (24, "Bolsonaro in intensive care"),
            (25, "Wembanyama scores 50"), (27, "FBI probes NCIC crime-database hack"),
            (28, "Drones kill 4 near Khartoum"), (29, "Mourners' boat capsizes: 24 dead"),
            (31, "Melbourne: 70 yrs since 1956 Games"), (32, "Fred Nile dies, 92"),
            (33, "Cummins stays Test captain"), (34, "Bitcoin back above $60,000"),
            (35, "Nvidia faces SEC accounting probe")]
    fa = fsans(False, 11)
    for i, (num, txt) in enumerate(also):
        col = i % 2
        row = i // 2
        x = ax0 + col * 288
        y = 612 + row * 18
        d.text((x, y), f"{num}", font=fsans(True, 11), fill=RED)
        d.text((x + 22, y), txt, font=fa, fill=INK)

    # ---- DATE CHECK ----
    dy0, dy1 = 836, 952
    d.rectangle([16, dy0, 1008, dy1], outline=RED, width=2)
    d.text((24, dy0 + 6), "DATE CHECK", font=fsans(True, 12), fill=RED)
    d.text((24, dy0 + 6), "DATE CHECK", font=fsans(True, 12), fill=RED)
    fdc = fsans(False, 11)
    fdcb = fsans(True, 11)
    d.text((120, dy0 + 7), "Every story above happened or was first reported on Sunday 22 November 2026. Wires read up to 23:00 UTC.",
           font=fdc, fill=INK)
    d.text((24, dy0 + 28), "LEFT OUT (not 22 Nov):", font=fdcb, fill=INK)
    left = ("400-drone barrage (19–20 Nov) · El Chapo Isidro captured (20 Nov) · BepiColombo Mercury orbit (21 Nov, burn 18:24 GMT) · "
            "Kryvyi Rih (20 Nov night) · Peru quake (20 Nov) · Hormuz tankers hit (Sat 21 Nov 05:00 GMT, reported Sun 17:13 UTC) · "
            "Mongolia snap vote · Paolo Bulgari dies (21 Nov)")
    for j, ln in enumerate(wrap(d, left, fdc, 960)[:2]):
        d.text((24, dy0 + 44 + j * 14), ln, font=fdc, fill=INK)
    d.text((24, dy0 + 74), "NOT YET:", font=fdcb, fill=INK)
    notyet = ("Dymer final toll · 4 House races uncalled · EU–Indonesia deal date split (Sat 21 vs Sun 22) · "
              "Nigeria boat date (Fri 20 vs Sun 22) · FBI hack date split (Fri 20 / Sat 21) · Sparta II hit Sat 21, still burning Sun · COP32 venue undecided")
    for j, ln in enumerate(wrap(d, notyet, fdc, 940)[:2]):
        d.text((24, dy0 + 90 + j * 14), ln, font=fdc, fill=INK)

    # ---- footer ----
    d.text((16, 960), "SOURCES: AP · Reuters · BBC · CNN · Guardian · France 24 · Al Jazeera · Yonhap · Anadolu · Detiknews · WHO · SpaceX",
           font=fsans(False, 9), fill=GREY)
    d.text((16, 974), "CONFIRMED = 2+ outlets · REPORTED = carried by the wires today · CLAIM = one side, unverified · OFFICIAL = recorded result · FORECAST = not yet decided",
           font=fsans(False, 9), fill=GREY)
    d.text((16, 988), "Scenes are drawn illustrations, not photographs.", font=fsans(False, 9), fill=GREY)
    d.text((W - 16 - d.textlength("THE WORLD IN ONE DAY · SUNDAY 22 NOVEMBER 2026", font=fsans(True, 9)), 988),
           "THE WORLD IN ONE DAY · SUNDAY 22 NOVEMBER 2026", font=fsans(True, 9), fill=RED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")

if __name__ == "__main__":
    main()
