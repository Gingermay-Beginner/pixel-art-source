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
SPACE     = (6, 8, 38)
SPACE_D   = (2, 4, 22)
STAR_W    = (255, 255, 240)
STAR_B    = (178, 202, 255)
NEBULA    = (68, 28, 88)
SCR_GLOW  = (138, 182, 255)
SCR_FRAME = (38, 28, 18)
CURTAIN   = (88, 18, 18)
CURTAIN_L = (118, 38, 28)

SEAT_R    = (78, 38, 32)
SEAT_RL   = (105, 56, 48)
SEAT_D    = (48, 24, 20)
ARMREST   = (32, 22, 14)
ARMREST_L = (52, 38, 26)

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
    set_px(canvas, cx-1, cy-5, GBD)
    set_px(canvas, cx+1, cy-5, GBD)
    # Legs
    for dy in range(-4,-2):
        set_px(canvas, cx-1, cy+dy, GB)
        set_px(canvas, cx+1, cy+dy, GB)
    # Body
    for dy in range(-2,2):
        for dx in range(-1,2):
            set_px(canvas, cx+dx, cy+dy, GB_LT if dx==0 and dy==0 else GB)
    set_px(canvas, cx-1, cy-2, GBD); set_px(canvas, cx+1, cy-2, GBD)
    set_px(canvas, cx-1, cy+1, GBD); set_px(canvas, cx+1, cy+1, GBD)
    # Arms (spread to sides at mid-body)
    set_px(canvas, cx-2, cy-1, GB); set_px(canvas, cx-2, cy, GB)
    set_px(canvas, cx+2, cy-1, GB); set_px(canvas, cx+2, cy, GB)
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
        set_px(canvas, cx+dx, cy+7, RED)
        set_px(canvas, cx+dx, cy+8, RED)
    # Popcorn box on belly
    fill(canvas, cy-1, cy, cx-1, cx+1, BOX_R)
    wrow(canvas, cy-1, cx-1, cx+1, BOX_W)
    for dx,dy in [(-1,-2),(0,-2),(1,-2),(0,-3),(-1,-3),(1,-3)]:
        set_px(canvas, cx+dx, cy+dy, POPCORN)

def draw_bun_topdown(cx, cy):
    """Bunny top-down reclined: head at bottom, feet at top"""
    # Ears (on top of head = beyond head, away from screen)
    for dy in range(6,10):
        set_px(canvas, cx-1, cy+dy, BUN_EAR)
        set_px(canvas, cx+1, cy+dy, BUN_EAR)
    # Feet
    set_px(canvas, cx-1, cy-5, BUND)
    set_px(canvas, cx+1, cy-5, BUND)
    # Legs
    for dy in range(-4,-2):
        set_px(canvas, cx-1, cy+dy, BUN)
        set_px(canvas, cx+1, cy+dy, BUN)
    # Body
    for dy in range(-2,2):
        for dx in range(-1,2):
            set_px(canvas, cx+dx, cy+dy, BUN_LT if dx==0 and dy==0 else BUN)
    set_px(canvas, cx-1, cy-2, BUND); set_px(canvas, cx+1, cy-2, BUND)
    set_px(canvas, cx-1, cy+1, BUND); set_px(canvas, cx+1, cy+1, BUND)
    # Arms
    set_px(canvas, cx-2, cy-1, BUN); set_px(canvas, cx-2, cy, BUN)
    set_px(canvas, cx+2, cy-1, BUN); set_px(canvas, cx+2, cy, BUN)
    # Head (round, center at cy+3)
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            if dx**2 + dy**2 <= 5:
                set_px(canvas, cx+dx, cy+dy+3, BUN_LT if dx==0 and dy==0 else BUN)
    # Eyes
    set_px(canvas, cx-1, cy+3, (25,45,88))
    set_px(canvas, cx+1, cy+3, (25,45,88))
    # Nose
    set_px(canvas, cx, cy+5, (228,148,165))
    # Smile
    set_px(canvas, cx-1, cy+5, BUN)
    set_px(canvas, cx,   cy+6, BUND)
    set_px(canvas, cx+1, cy+5, BUN)
    # Ears (2 rows)
    for dy in range(7,9):
        set_px(canvas, cx-1, cy+dy, BUN_EAR)
        set_px(canvas, cx+1, cy+dy, BUN_EAR)
    # Popcorn box
    fill(canvas, cy-1, cy, cx-1, cx+1, BOX_R)
    wrow(canvas, cy-1, cx-1, cx+1, BOX_W)
    for dx,dy in [(-1,-2),(0,-2),(1,-2),(0,-3),(-1,-3),(1,-3)]:
        set_px(canvas, cx+dx, cy+dy, POPCORN)

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

# Nebula (softer, wider)
for dy in range(1, 18):
    for dx in range(10, 54):
        t = abs((dx-32)/22.0)
        if t < 1:
            col = blend(NEBULA, SPACE_D, t**0.7)
            set_px(canvas, dx, dy, blend(canvas[dy][dx], col, 0.4))

# Stars (fewer, cleaner) — avoid glass dome area (x=21~43, y=3~16)
random.seed(77)
star_count = 0
attempts = 0
while star_count < 40 and attempts < 500:
    sx = random.randint(5, 58)
    sy = random.randint(1, 16)
    if not (21 <= sx <= 43 and 3 <= sy <= 16):
        set_px(canvas, sx, sy, STAR_W)
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
set_px(canvas, RX+6, RY+6, ROCKY_D)
# Body shadow bottom moved to end of file

# Ryland Grace (clearer silhouette, left)
# head
for dx,dy in [(0,0),(1,0),(-1,0),(0,-1),(0,1),(1,-1),(-1,-1)]:
    set_px(canvas, 14+dx, 5+dy, (205,168,128))
# body
for dy in range(6,10):
    for dx in [-1,0,1]:
        set_px(canvas, 14+dx, dy, (168,128,88))
# arms
set_px(canvas, 12, 7, (168,128,88)); set_px(canvas, 13, 7, (168,128,88))
set_px(canvas, 15, 7, (168,128,88)); set_px(canvas, 16, 7, (168,128,88))
# legs
set_px(canvas, 13, 10, (148,108,68)); set_px(canvas, 13, 11, (148,108,68))
set_px(canvas, 15, 10, (148,108,68)); set_px(canvas, 15, 11, (148,108,68))

# Planet removed

# Screen title text area (bottom of screen)
# Screen title text area removed

# Curtains
for y in range(0, 19):
    t = y/18.0
    fill(canvas, y, y, 0, 2, blend(CURTAIN_L, CURTAIN, t))
    fill(canvas, y, y, 61, 63, blend(CURTAIN_L, CURTAIN, t))

# Screen bottom frame
wrow(canvas, 18, 2, 61, SCR_FRAME)
fill(canvas, 19, 20, 2, 61, blend(THEATER, SCR_FRAME, 0.4))

# Seats: 6 chairs, each 8px wide, 2px armrests
# x layout: 0-1(wall) | 2-9(s1) | 10-11(arm) | 12-19(s2) | 20-21(arm) | 22-29(s3/GB) | 30-31(C-arm) | 32-39(s4/BUN) | 40-41(arm) | 42-49(s5) | 50-51(arm) | 52-59(s6) | 60-61(arm) | 62-63(wall)
SEATS = [(2,9),(12,19),(22,29),(32,39),(42,49),(52,59)]
ARMS  = [(0,1),(10,11),(20,21),(30,31),(40,41),(50,51),(60,63)]

for xa, xb in SEATS:
    fill(canvas, 21, 22, xa, xb, SEAT_RL)   # footrest
    wrow(canvas, 21, xa, xb, blend(SEAT_RL,(245,225,195),0.15))
    wrow(canvas, 22, xa, xb, SEAT_D)
    fill(canvas, 23, 28, xa, xb, SEAT_R)    # seat cushion
    wrow(canvas, 23, xa, xb, SEAT_RL)
    wrow(canvas, 28, xa, xb, SEAT_D)        # dividing line
    fill(canvas, 29, 35, xa, xb, SEAT_D)    # reclined back
    wrow(canvas, 29, xa, xb, blend(SEAT_D, SEAT_R, 0.35))
    for y in [24,26]:
        for x in range(xa+1, xb, 3):
            set_px(canvas, x, y, blend(SEAT_R, SEAT_D, 0.45))

for xa, xb in ARMS:
    fill(canvas, 21, 35, xa, xb, ARMREST)
    wrow(canvas, 21, xa, xb, ARMREST_L)

# ══════════════════════════════════════════
# GINGERBREAD (seat3, center x=25)
# BUNNY (seat4, center x=36)
# cy=26: feet at y=21, head at y=31
draw_gb_topdown(25, 26)
draw_bun_topdown(36, 26)
# Remove arm pixels at y=25 (cy-1)
set_px(canvas, 27, 25, SEAT_R)
set_px(canvas, 34, 25, SEAT_R)

# Holding hands — extend arms across the armrest
for x in range(28, 31):
    set_px(canvas, x, 26, GB)    # GB right arm reaching right
for x in range(31, 35):
    set_px(canvas, x, 26, BUN)   # BUN left arm reaching left
# clasped hands at x=30,31
set_px(canvas, 30, 26, GB)
set_px(canvas, 31, 26, BUN)

# Rocky body shadow bottom — drawn last so nothing overwrites it
for dx in range(-1,2):
    set_px(canvas, RX+dx, RY+2, ROCKY)   # fill gap between body and shadow
for dx in range(-1,2):
    set_px(canvas, RX+dx, RY+3, ROCKY_D)

# Glass dome around Rocky — smooth arc, no gaps
GLASS   = (98, 158, 188)
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
# clear (38,14)(38,15) — overwrite leg pixels
set_px(canvas, 38, 14, SPACE_D)
set_px(canvas, 38, 15, SPACE_D)
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
