from PIL import Image, ImageDraw
import os, random

S = 12
W, H = 64, 36

def set_px(c, x, y, col):
    if 0 <= x < W and 0 <= y < H: c[y][x] = col

def fill(c, y1, y2, x1, x2, col):
    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            set_px(c, x, y, col)

def wrow(c, y, x1, x2, col):
    for x in range(x1, x2+1):
        set_px(c, x, y, col)

def blend(a, b, t):
    return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))

# ── Colors ─────────────────────────────────
THEATER   = (12, 10, 20)
FLOOR_L   = (28, 22, 38)
SPACE     = (4, 6, 28)
SPACE_D   = (1, 2, 14)
STAR_W    = (248, 120, 100)
STAR_B    = (178, 202, 255)
NEBULA    = (140, 20, 30)  # red nebula
NEBULA2   = (100, 10, 50)   # deep crimson nebula
SCR_GLOW  = (138, 182, 255)
SCR_FRAME = (38, 28, 18)
CURTAIN   = (98, 22, 22)
CURTAIN_L = (132, 48, 36)

SEAT_R    = (148, 58, 48)
SEAT_RL   = (178, 88, 72)
SEAT_D    = (88, 38, 32)
ARMREST   = (88, 62, 42)
ARMREST_L = (118, 88, 62)

GB    = (185, 108, 48)
GB_LT = (215, 148, 78)
GBD   = (128, 72, 28)
RED   = (192, 62, 48)
BUN   = (112, 172, 232)
BUN_LT= (155, 205, 248)
BUND  = (40, 75, 130)
BUN_EAR = (235, 165, 180)
POPCORN = (255, 228, 148)
BOX_R   = (215, 48, 38)
BOX_W   = (248, 240, 232)

def draw_gb_topdown(cx, cy):
    """Gingerbread top-down reclined: head at bottom (cy+5), feet at top (cy-5)"""
    # Feet (top of view = near screen)
    set_px(canvas, cx-1, cy-5, GB)
    set_px(canvas, cx+1, cy-5, GB)
    # Legs
    for dy in range(-4,-2):
        set_px(canvas, cx-1, cy+dy, GB)
        set_px(canvas, cx+1, cy+dy, GB)
    # Body
    for dy in range(-2,2):
        for dx in range(-1,2):
            set_px(canvas, cx+dx, cy+dy, GB_LT if dx==0 and dy==0 else GB)
    set_px(canvas, cx-1, cy-2, GB); set_px(canvas, cx+1, cy-2, GB)
    set_px(canvas, cx-1, cy+1, GB); set_px(canvas, cx+1, cy+1, GB)
    # Arms: outer = 45° up-left; inner (toward BUN) = flat right for handholding
    set_px(canvas, cx-2, cy, GB)
    set_px(canvas, cx-3, cy-1, GB)  # outer arm 45° up-left
    set_px(canvas, cx+2, cy-1, GB); set_px(canvas, cx+2, cy, GB)  # inner arm toward BUN
    # clear armpit pixels
    set_px(canvas, cx-2, cy-1, SEAT_R); set_px(canvas, cx-2, cy-2, SEAT_R)
    set_px(canvas, cx-2, cy+1, SEAT_R)
    set_px(canvas, cx+2, cy-2, SEAT_R); set_px(canvas, cx+2, cy+1, SEAT_R)
    # Head (round, center at cy+3)
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            if dx**2 + dy**2 <= 5:
                set_px(canvas, cx+dx, cy+dy+3, GB_LT if dx==0 and dy==0 else GB)
    # Eyes (looking toward screen = upward)
    set_px(canvas, cx-1, cy+3, (40,25,10))
    set_px(canvas, cx+1, cy+3, (40,25,10))
    # Smile
    set_px(canvas, cx-1, cy+5, GB)
    set_px(canvas, cx,   cy+6, GBD)
    set_px(canvas, cx+1, cy+5, GB)
    # Hat (on top of head = beyond head, away from screen)
    for dx in range(-1,2):
        set_px(canvas, cx-1+dx, cy+4, RED)
        set_px(canvas, cx-1+dx, cy+5, RED)
    set_px(canvas, cx-1, cy+6, RED)  # pompom below hat
    set_px(canvas, cx-2, cy+6, SEAT_D)   # show seat back colour
    set_px(canvas, cx,   cy+6, SEAT_D)   # show seat back colour
    # Popcorn removed

def draw_bun_topdown(cx, cy):
    """Bunny top-down reclined: head at bottom, feet at top"""
    # Ears (on top of head = beyond head, away from screen)
    for dy in range(6,9):
        set_px(canvas, cx-1, cy+dy, BUN_EAR)
        set_px(canvas, cx+1, cy+dy, BUN_EAR)
    # Feet
    set_px(canvas, cx-1, cy-5, BUN)
    set_px(canvas, cx+1, cy-5, BUN)
    # Legs
    for dy in range(-4,-2):
        set_px(canvas, cx-1, cy+dy, BUN)
        set_px(canvas, cx+1, cy+dy, BUN)
    # Body
    for dy in range(-2,2):
        for dx in range(-1,2):
            set_px(canvas, cx+dx, cy+dy, BUN_LT if dx==0 and dy==0 else BUN)
    set_px(canvas, cx-1, cy-2, BUN); set_px(canvas, cx+1, cy-2, BUN)
    set_px(canvas, cx-1, cy+1, BUN); set_px(canvas, cx+1, cy+1, BUN)
    # Arms
    # Arms: inner (toward GB) = flat left for handholding; outer = 45° up-right
    set_px(canvas, cx-2, cy-1, BUN); set_px(canvas, cx-2, cy, BUN)  # inner arm toward GB
    set_px(canvas, cx+2, cy, BUN)
    set_px(canvas, cx+3, cy-1, BUN)  # outer arm 45° up-right
    # clear armpit pixels
    set_px(canvas, cx-2, cy-2, SEAT_R); set_px(canvas, cx-2, cy+1, SEAT_R)
    set_px(canvas, cx+2, cy-1, SEAT_R); set_px(canvas, cx+2, cy-2, SEAT_R)
    set_px(canvas, cx+2, cy+1, SEAT_R)
    # Head (round, center at cy+3)
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            if dx**2 + dy**2 <= 5:
                set_px(canvas, cx+dx, cy+dy+3, BUN_LT if dx==0 and dy==0 else BUN)
    # Eyes
    set_px(canvas, cx-1, cy+3, (25,45,88))
    set_px(canvas, cx+1, cy+3, (25,45,88))
    # Nose removed
    # Smile
    set_px(canvas, cx-1, cy+5, BUN)
    # set_px(canvas, cx,   cy+6, BUND)  # removed
    set_px(canvas, cx+1, cy+5, BUN)
    # Ears (2 rows)
    for dy in range(7,9):
        set_px(canvas, cx-1, cy+dy, BUN_EAR)
        set_px(canvas, cx+1, cy+dy, BUN_EAR)
    # Popcorn removed

# ── Canvas ─────────────────────────────────
canvas = [[THEATER]*W for _ in range(H)]

# Theater floor (dark gradient)
for y in range(H):
    t = y / (H-1)
    col = blend(THEATER, FLOOR_L, t*0.6)
    wrow(canvas, y, 0, W-1, col)

# ══════════════════════════════════════════
# SCREEN (y=0~14, wider and taller)
# ══════════════════════════════════════════
fill(canvas, 0, 18, 3, 60, SPACE_D)

# Nebula (diagonal band, top-left to bottom-right)
for dy in range(0, 18):
    for dx in range(3, 61):
        # diagonal distance from band center line: dx - dy*2.5 - 8
        band_pos = dx - dy * 2.2 - 5
        t = abs(band_pos / 18.0)
        if t < 1:
            col = blend(NEBULA, SPACE_D, t**0.6)
            set_px(canvas, dx, dy, blend(canvas[dy][dx], col, 0.92))
# teal nebula fringe (offset diagonal)
for dy in range(0, 18):
    for dx in range(3, 61):
        band_pos = dx - dy * 2.2 - 24
        t = abs(band_pos / 12.0)
        if t < 1:
            col = blend(NEBULA2, SPACE_D, t**0.8)
            set_px(canvas, dx, dy, blend(canvas[dy][dx], col, 0.72))

# Stars (fewer, cleaner) — avoid glass dome area (x=21~43, y=3~16)
# two brightness levels for depth effect
STAR_DIM  = (168, 50, 60)
random.seed(77)
star_count = 0
attempts = 0
while star_count < 10 and attempts < 500:
    sx = random.randint(5, 58)
    sy = random.randint(1, 16)
    if not (21 <= sx <= 43 and 3 <= sy <= 16):
        col = STAR_W if random.random() < 0.4 else STAR_DIM
        set_px(canvas, sx, sy, col)
        star_count += 1
    attempts += 1

# Screen glow border
wrow(canvas, 0, 3, 60, SCR_GLOW)
for y in range(0, 19):
    set_px(canvas, 3, y, SCR_GLOW)
    set_px(canvas, 60, y, SCR_GLOW)

# Rocky (side view, spider-like: stone body + 4 downward umbrella legs)
RX, RY = 32, 9
ROCKY    = (148, 118, 78)
ROCKY_D  = (108,  85, 52)
ROCKY_LT = (188, 158, 108)
ROCKY_LEG = (118, 92, 58)  # outer legs slightly darker
# Central stone body (taller oval)
for dx in range(-3, 4):
    for dy in range(-2, 3):
        if dx**2*0.35 + dy**2 <= 2.2:
            set_px(canvas, RX+dx, RY+dy, ROCKY)
# Body highlight
for dx,dy in [(0,-2),(1,-2),(-1,-2),(0,-1),(1,-1)]:
    set_px(canvas, RX+dx, RY+dy, ROCKY_LT)

def draw_leg(canvas, x0, y0, x1, y1, col):
    """Bresenham line, 2px thick"""
    dx = abs(x1-x0); dy = abs(y1-y0)
    sx = 1 if x1>x0 else -1; sy = 1 if y1>y0 else -1
    err = dx - dy
    while True:
        set_px(canvas, x0, y0, col)
        set_px(canvas, x0, y0+1, col)
        if x0==x1 and y0==y1: break
        e2 = 2*err
        if e2 > -dy: err -= dy; x0 += sx
        if e2 < dx:  err += dx; y0 += sy

# 4 legs all going downward, umbrella spread
JOINT = (97, 168, 129)

# left outer: spread wide at top, slightly curve in at bottom
draw_leg(canvas, RX-5, RY-1, RX-7, RY+2, ROCKY_LEG)   # upper half: spread out
set_px(canvas, RX-7, RY+2, JOINT); set_px(canvas, RX-7, RY+3, JOINT)
set_px(canvas, RX-6, RY+2, JOINT); set_px(canvas, RX-6, RY+3, JOINT)  # joint 2×2
draw_leg(canvas, RX-7, RY+2, RX-6, RY+5, ROCKY_LEG)  # lower half: slight curve in
set_px(canvas, RX-6, RY+6, ROCKY_D)
# left inner: bracket ( shape — curves left then back
draw_leg(canvas, RX-2, RY-1, RX-4, RY+1, ROCKY)   # upper arc going left
draw_leg(canvas, RX-4, RY+1, RX-4, RY+3, ROCKY)    # vertical middle
draw_leg(canvas, RX-4, RY+3, RX-3, RY+5, ROCKY)    # lower arc coming back
set_px(canvas, RX-4, RY+1, JOINT); set_px(canvas, 30, 8, JOINT)  # joint
set_px(canvas, RX-4, RY+3, JOINT)  # joint (drawn after leg)
set_px(canvas, 28, 8, ROCKY_LEG)  # extra pixel (drawn after leg)
set_px(canvas, 36, 8, ROCKY_LEG)  # mirror extra pixel
# shift (26,14)(26,15) left by 1
set_px(canvas, 26, 14, SPACE_D)
set_px(canvas, 26, 15, SPACE_D)
set_px(canvas, 25, 14, ROCKY_LEG)
set_px(canvas, 25, 15, ROCKY_LEG)
# mirror: shift (38,14)(38,15) right by 1
# mirror: shift (38,14)(38,15) right by 1 — cleared after draw_leg
# (moved to end to avoid being overwritten by draw_leg)
# mirror: shift (38,14)(38,15) right by 1 — cleared after draw_leg
# (moved to end to avoid being overwritten by draw_leg)
# right inner: bracket ) shape
draw_leg(canvas, RX+2, RY-1, RX+4, RY+1, ROCKY)
set_px(canvas, RX+4, RY+1, JOINT); set_px(canvas, 34, 8, JOINT)  # joint
draw_leg(canvas, RX+4, RY+1, RX+4, RY+3, ROCKY)
draw_leg(canvas, RX+4, RY+3, RX+3, RY+5, ROCKY)
set_px(canvas, RX+4, RY+3, JOINT)  # joint (drawn after leg)
# right outer: spread wide at top, slightly curve in at bottom
draw_leg(canvas, RX+5, RY-1, RX+7, RY+2, ROCKY_LEG)   # upper half: spread out
set_px(canvas, RX+7, RY+2, JOINT); set_px(canvas, RX+7, RY+3, JOINT)
set_px(canvas, RX+6, RY+2, JOINT); set_px(canvas, RX+6, RY+3, JOINT)  # joint 2×2
draw_leg(canvas, RX+7, RY+2, RX+6, RY+5, ROCKY_LEG)  # lower half: slight curve in
set_px(canvas, RX+6, RY+5, blend(NEBULA, SPACE_D, 0.55))  # (38,14) restore nebula bg in leg gap
set_px(canvas, RX+6, RY+6, blend(NEBULA, SPACE_D, 0.45))  # (38,15) restore nebula bg in leg gap
set_px(canvas, RX+6, RY+7, blend(NEBULA, SPACE_D, 0.38))  # (38,16) restore nebula bg
# Body shadow bottom moved to end of file

# Planet removed

# Screen title text area (bottom of screen)
# Screen title text area removed

# Curtains (screen area only)
for y in range(0, 19):
    t = y/18.0
    fill(canvas, y, y, 0, 2, blend(CURTAIN_L, CURTAIN, t))
    fill(canvas, y, y, 61, 63, blend(CURTAIN_L, CURTAIN, t))
# Theater walls below screen — use theater bg
_tbg = blend(THEATER, SCR_FRAME, 0.4)
fill(canvas, 19, 35, 0, 1, _tbg)
fill(canvas, 19, 35, 62, 63, _tbg)

# Screen bottom frame — drawn AFTER glass dome so it overlaps

# Seats: 6 chairs, each 8px wide, 2px armrests
# x layout: 0-1(wall) | 2-9(s1) | 10-11(arm) | 12-19(s2) | 20-21(arm) | 22-29(s3/GB) | 30-31(C-arm) | 32-39(s4/BUN) | 40-41(arm) | 42-49(s5) | 50-51(arm) | 52-59(s6) | 60-61(arm) | 62-63(wall)
SEATS = [(-8,2),(2,11),(12,21),(22,31),(32,41),(42,51),(52,61),(61,71)]
ARMS  = [(-9,-8),(1,2),(11,12),(21,22),(31,32),(41,42),(51,52),(61,62),(71,72)]

for xa, xb in SEATS:
    fill(canvas, 21, 22, xa, xb, SEAT_RL)   # footrest
    wrow(canvas, 21, xa, xb, blend(SEAT_RL,(245,225,195),0.15))
    wrow(canvas, 22, xa, xb, SEAT_D)
    fill(canvas, 23, 28, xa, xb, SEAT_R)    # seat cushion
    wrow(canvas, 23, xa, xb, SEAT_RL)
    wrow(canvas, 28, xa, xb, SEAT_D)        # dividing line
    # round corners of footrest top
    _c21 = blend(THEATER, SCR_FRAME, 0.4)
    set_px(canvas, xa+1, 21, _c21); set_px(canvas, xb-1, 21, _c21)
    # round corners of seat cushion bottom only
    set_px(canvas, xa+1, 29, _c21); set_px(canvas, xb-1, 29, _c21)
    # round corners of reclined back
    fill(canvas, 29, 35, xa, xb, SEAT_D)    # reclined back
    wrow(canvas, 29, xa, xb, blend(SEAT_D, SEAT_R, 0.35))
    set_px(canvas, xa+1, 35, _c21); set_px(canvas, xb-1, 35, _c21)
    for y in [24,26]:
        cx = (xa + xb) // 2
        for x in [cx-1, cx+2]:
            set_px(canvas, x, y, blend(SEAT_R, SEAT_D, 0.45))

for xa, xb in ARMS:
    fill(canvas, 24, 28, xa, xb, ARMREST)
    wrow(canvas, 24, xa, xb, ARMREST_L)
    # clear armrest columns to show theater bg (footrest area + backrest area)
    _bg = blend(THEATER, SCR_FRAME, 0.4)
    for y in range(21, 24):
        for x in range(xa, xb+1):
            set_px(canvas, x, y, _bg)
    for y in range(29, 36):
        for x in range(xa, xb+1):
            set_px(canvas, x, y, _bg)

# restore edge seat corners (overwritten by adjacent arm _bg)
_c21 = blend(THEATER, SCR_FRAME, 0.4)
for y in [21, 29, 35]:
    set_px(canvas, 1,  y, _c21)   # left edge seat xb-1=1
    set_px(canvas, 62, y, _c21)   # right edge seat xa+1=62
# outer corners of edge seats (x=0 and x=63 at corner rows)
for y in [21, 35]:
    set_px(canvas, 0,  y, _c21)   # left edge seat outer corner
    set_px(canvas, 63, y, _c21)   # right edge seat outer corner

# ══════════════════════════════════════════
# GINGERBREAD (seat3, center x=25)
# BUNNY (seat4, center x=36)
# cy=26: feet at y=21, head at y=31
draw_gb_topdown(27, 26)
draw_bun_topdown(36, 26)
# Remove arm pixels at y=25 (cy-1)
set_px(canvas, 29, 25, SEAT_R)
set_px(canvas, 34, 25, SEAT_R)

# Holding hands — extend arms across the armrest
for x in range(30, 32):
    set_px(canvas, x, 26, GB)    # GB right arm reaching right
for x in range(32, 35):
    set_px(canvas, x, 26, BUN)   # BUN left arm reaching left
# clasped hands at x=31,32
set_px(canvas, 31, 26, GB)
set_px(canvas, 32, 26, BUN)

# Rocky body shadow bottom — drawn last so nothing overwrites it
for dx in range(-1,2):
    set_px(canvas, RX+dx, RY+2, ROCKY)   # fill gap between body and shadow
for dx in range(-1,2):
    set_px(canvas, RX+dx, RY+3, ROCKY_D)

# Glass dome around Rocky — smooth arc, no gaps
GLASS   = (148, 198, 228)
GLASS_H = (178, 228, 248)

# top flat edge
for dx in range(-3, 4):
    set_px(canvas, RX+dx, RY-6, GLASS)
# upper arc — no gaps (each step ≤1px)
set_px(canvas, RX-4,  RY-5, GLASS); set_px(canvas, RX+4,  RY-5, GLASS)
set_px(canvas, RX-5,  RY-5, GLASS); set_px(canvas, RX+5,  RY-5, GLASS)
set_px(canvas, RX-6,  RY-4, GLASS); set_px(canvas, RX+6,  RY-4, GLASS)
set_px(canvas, RX-7,  RY-4, GLASS); set_px(canvas, RX+7,  RY-4, GLASS)
set_px(canvas, RX-8,  RY-3, GLASS); set_px(canvas, RX+8,  RY-3, GLASS)
set_px(canvas, RX-9,  RY-3, GLASS); set_px(canvas, RX+9,  RY-3, GLASS)
set_px(canvas, RX-10, RY-2, GLASS); set_px(canvas, RX+10, RY-2, GLASS)
set_px(canvas, RX-11, RY-1, GLASS); set_px(canvas, RX+11, RY-1, GLASS)
# sides
for dy in range(0, 7):
    set_px(canvas, RX-11, RY+dy, GLASS)
    set_px(canvas, RX+11, RY+dy, GLASS)
# lower arc (cropped by screen)
set_px(canvas, RX-11, RY+7,  GLASS); set_px(canvas, RX+11, RY+7,  GLASS)
set_px(canvas, RX-10, RY+8,  GLASS); set_px(canvas, RX+10, RY+8,  GLASS)
set_px(canvas, RX-9,  RY+8,  GLASS); set_px(canvas, RX+9,  RY+8,  GLASS)
set_px(canvas, RX-8,  RY+9,  GLASS); set_px(canvas, RX+8,  RY+9,  GLASS)
set_px(canvas, RX-7,  RY+9,  GLASS); set_px(canvas, RX+7,  RY+9,  GLASS)
set_px(canvas, RX-6,  RY+10, GLASS); set_px(canvas, RX+6,  RY+10, GLASS)
set_px(canvas, RX-5,  RY+10, GLASS); set_px(canvas, RX+5,  RY+10, GLASS)
set_px(canvas, RX-4,  RY+11, GLASS); set_px(canvas, RX+4,  RY+11, GLASS)
# highlight removed
set_px(canvas, 28, 12, GLASS)  # test point
set_px(canvas, 23, 17, GLASS)  # point
# measurement points — restored to GLASS
set_px(canvas, 21, 9,  GLASS)
set_px(canvas, 21, 15, GLASS)
set_px(canvas, 29, 3,  GLASS)
set_px(canvas, 35, 3,  GLASS)
set_px(canvas, 43, 9,  GLASS)
# line from (21,8) to (28,12)
def draw_line_1px(x0, y0, x1, y1, col):
    dx = abs(x1-x0); dy = abs(y1-y0)
    sx = 1 if x1>x0 else -1; sy = 1 if y1>y0 else -1
    err = dx - dy
    while True:
        set_px(canvas, x0, y0, col)
        if x0==x1 and y0==y1: break
        e2 = 2*err
        if e2 > -dy: err -= dy; x0 += sx
        if e2 < dx:  err += dx; y0 += sy
draw_line_1px(21, 8, 28, 12, GLASS)
draw_line_1px(29, 3, 28, 12, GLASS)
draw_line_1px(43, 9, 28, 12, GLASS)
draw_line_1px(36, 20, 28, 12, GLASS)
draw_line_1px(23, 17, 28, 12, GLASS)

# Screen bottom frame — over glass dome
wrow(canvas, 18, 3, 60, SCR_GLOW)
fill(canvas, 19, 20, 2, 61, blend(THEATER, SCR_FRAME, 0.4))
# restore glass dome pixels overwritten by fill above (RY+11 = y=20) — removed per user request
set_px(canvas, 43, 16, GLASS)  # fill missing right dome pixel — moved, placeholder
# Screen glow spill downward (cold blue fade)
SCR_GLOW2 = (62, 88, 138)
for y, t in [(19, 0.22), (20, 0.14), (21, 0.10), (22, 0.06)]:
    for x in range(2, 62):
        set_px(canvas, x, y, blend(canvas[y][x], SCR_GLOW2, t))

# Ryland Grace (right side of screen, red spacesuit) — drawn after dome so arms overlap
GRACE_SKIN = (178, 118, 118)
GRACE_SUIT = (192, 62, 48)
GRACE_SUIT_D = (140, 42, 32)
# head (bigger)
for dx,dy in [(0,0),(1,0),(-1,0),(2,0),(-2,0),(0,-1),(0,1),(1,-1),(-1,-1),(2,-1),(-2,-1),(1,1),(-1,1),(0,-2),(1,-2),(-1,-2)]:
    set_px(canvas, 47+dx, 5+dy, GRACE_SKIN)
# helmet ring
set_px(canvas, 44, 4, GRACE_SUIT); set_px(canvas, 50, 4, GRACE_SUIT)
set_px(canvas, 44, 5, GRACE_SUIT); set_px(canvas, 50, 5, GRACE_SUIT)
# body (red suit, wider)
for dy in range(7,12):
    for dx in [-2,-1,0,1,2]:
        set_px(canvas, 47+dx, dy, GRACE_SUIT)
# arms
for dx in range(-6,-2):
    set_px(canvas, 47+dx, 8, GRACE_SUIT); set_px(canvas, 47+dx, 9, GRACE_SUIT)
for dx in range(3,5):
    set_px(canvas, 47+dx, 8, GRACE_SUIT); set_px(canvas, 47+dx, 9, GRACE_SUIT)
# legs
# legs (clean)
for dy in [12, 13, 14]:
    set_px(canvas, 45, dy, GRACE_SUIT_D); set_px(canvas, 46, dy, GRACE_SUIT_D)
    set_px(canvas, 48, dy, GRACE_SUIT_D); set_px(canvas, 49, dy, GRACE_SUIT_D)
set_px(canvas, 50, 13, GRACE_SUIT_D); set_px(canvas, 51, 13, GRACE_SUIT_D)
set_px(canvas, 50, 14, GRACE_SUIT_D); set_px(canvas, 51, 14, GRACE_SUIT_D)
set_px(canvas, 47, 13, GRACE_SUIT_D); set_px(canvas, 47, 14, GRACE_SUIT_D)
set_px(canvas, 43, 16, GLASS)  # restore dome pixel
# clear stray leg pixels
for x, y in [(45, 14), (48, 14), (45, 15), (48, 15)]:
    dx = x - RX; dy = y - RY
    v1 = dx - dy * 2.2 - 5; v2 = dx - dy * 2.2 - 24
    col = SPACE_D
    t1 = max(0, 1 - abs(v1/18.0)); t2 = max(0, 1 - abs(v2/18.0))
    if t1 > 0: col = blend(NEBULA, col, t1 * 0.92)
    if t2 > 0: col = blend(NEBULA2, col, t2 * 0.72)
    set_px(canvas, x, y, col)
# clear (38,14)(38,15) — overwrite leg pixels
set_px(canvas, 39, 14, ROCKY_LEG)
set_px(canvas, 39, 15, ROCKY_LEG)


# ── RENDER ─────────────────────────────────
img = Image.new('RGB', (W*S, H*S))
draw = ImageDraw.Draw(img)
for y in range(H):
    for x in range(W):
        r,g,b = canvas[y][x]
        draw.rectangle([x*S, y*S, x*S+S-1, y*S+S-1], fill=(r,g,b))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pixel_movie.png')
img.save(out)
print(f'Saved: {W*S}×{H*S}px')
