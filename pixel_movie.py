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
    set_px(canvas, cx-1, cy+4, (40,25,10))
    set_px(canvas, cx+1, cy+4, (40,25,10))
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
    set_px(canvas, cx-1, cy+4, (25,45,88))
    set_px(canvas, cx+1, cy+4, (25,45,88))
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

# Stars (fewer, cleaner)
random.seed(77)
for _ in range(40):
    sx = random.randint(5, 58)
    sy = random.randint(1, 16)
    set_px(canvas, sx, sy, STAR_W)

# Screen glow border
wrow(canvas, 0, 3, 60, SCR_GLOW)
for y in range(0, 19):
    set_px(canvas, 3, y, SCR_GLOW)
    set_px(canvas, 60, y, SCR_GLOW)

# Rocky (clean circle, center screen)
RX, RY = 32, 9
# outer ring
for dx,dy in [(-3,0),(3,0),(0,-3),(0,3),(-2,-2),(2,-2),(-2,2),(2,2),(-3,-1),(3,-1),(-3,1),(3,1),(-1,-3),(1,-3),(-1,3),(1,3)]:
    set_px(canvas, RX+dx, RY+dy, (118,78,198))
# main body
for dx in range(-2,3):
    for dy in range(-2,3):
        if dx**2+dy**2 <= 6:
            set_px(canvas, RX+dx, RY+dy, (178,138,255))
# bright core
for dx,dy in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]:
    set_px(canvas, RX+dx, RY+dy, (218,195,255))
# cross glow
for i in range(-5,6):
    if abs(i) > 2:
        set_px(canvas, RX+i, RY, (148,108,228))
        set_px(canvas, RX, RY+i, (148,108,228))

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

# Planet (right, cleaner)
for dx in range(-2,4):
    for dy in range(-2,4):
        if dx**2+dy**2 <= 8:
            set_px(canvas, 50+dx, 8+dy, blend((88,178,138),(58,138,108),0.3))
# highlight
set_px(canvas, 49, 6, (138,218,178)); set_px(canvas, 50,6,(138,218,178)); set_px(canvas, 51,6,(138,218,178))

# Screen title text area (bottom of screen)
wrow(canvas, 13, 8, 55, blend(SPACE_D,(18,12,48),0.5))

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
