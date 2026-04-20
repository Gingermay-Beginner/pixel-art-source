from PIL import Image

W, H = 64, 36
SCALE = 12
canvas = [[(0,0,0)]*W for _ in range(H)]

def set_px(c, x, y, col):
    if 0<=x<W and 0<=y<H: c[y][x] = col

def fill(c, y1, y2, x1, x2, col):
    for y in range(y1, y2+1):
        for x in range(x1, x2+1): set_px(c,x,y,col)

def wrow(c, y, x1, x2, col):
    for x in range(x1, x2+1): set_px(c,x,y,col)

def blend(a, b, t):
    return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))


PALM_SIL     = blend((118, 188, 242), (42, 58, 35), 0.65)  # strong silhouette
PALM_SIL_DIM = blend((118, 188, 242), (42, 58, 35), 0.38)  # weak silhouette
def draw_palm_silhouette(cx, base_y, lean_dir=1, color=None, droop=0, crown_dx=0, crown_dy=0):
    col = color if color else PALM_SIL
    for i in range(12):
        lx = cx + round(lean_dir * i / 4)
        # droop: upper part curves downward
        dy = round(droop * (i / 11) ** 2) if droop else 0
        ly = base_y - i + dy
        set_px(canvas, lx,   ly, col)
        set_px(canvas, lx+1, ly, col)
        if abs(lean_dir) >= 2 and i > 0:
            prev_lx = cx + round(lean_dir * (i-1) / 4)
            if abs(lx - prev_lx) > 1:
                mid = (lx + prev_lx) // 2
                set_px(canvas, mid,   ly+1, col)
                set_px(canvas, mid+1, ly+1, col)
    top_x = cx + lean_dir * 3 + crown_dx
    top_y = base_y - 11 + crown_dy
    if lean_dir >= 0:
        leaf_dirs = [(-4,0),(-3,-2),(-2,-3),(-5,1),(6,0),(5,-1),(4,-3),(7,1),(0,-4),(2,-4),(-1,-4),(3,-3),(-3,1),(5,1)]
    else:
        leaf_dirs = [(4,0),(3,-2),(2,-3),(5,1),(-6,0),(-5,-1),(-4,-3),(-7,1),(0,-4),(-2,-4),(1,-4),(-3,-3),(3,1),(-5,1)]
    for lx, ly in leaf_dirs:
        for i in range(5):
            t = i / 4.0
            px2 = round(top_x + lx*t)
            py2 = round(top_y + ly*t)
            set_px(canvas, px2, py2, col)
            if i == 2:
                set_px(canvas, px2-1, py2, col)
                set_px(canvas, px2+1, py2, col)

def draw_palm(cx, base_y, lean_dir=1, crown_dx=0):
    for i in range(12):
        lx = cx + round(lean_dir * i / 4)
        ly = base_y - i
        set_px(canvas, lx,   ly, TRUNK)
        set_px(canvas, lx+1, ly, TRUNK_D)
        # fill gap when lean is steep
        if abs(lean_dir) >= 2 and i > 0:
            prev_lx = cx + round(lean_dir * (i-1) / 4)
            if abs(lx - prev_lx) > 1:
                mid = (lx + prev_lx) // 2
                set_px(canvas, mid, ly+1, TRUNK)
                set_px(canvas, mid+1, ly+1, TRUNK_D)
    top_x = cx + lean_dir * 3 + crown_dx
    top_y = base_y - 11
    for nx, ny in [(0,0),(1,0),(0,-1)]:
        set_px(canvas, top_x+nx, top_y+ny, COCONUT)
    if lean_dir >= 0:
        leaf_dirs = [(-4,0),(-3,-2),(-2,-3),(-5,1),(6,0),(5,-1),(4,-3),(7,1),(0,-4),(2,-4),(-1,-4),(3,-3),(-3,1),(5,1)]
    else:
        leaf_dirs = [(4,0),(3,-2),(2,-3),(5,1),(-6,0),(-5,-1),(-4,-3),(-7,1),(0,-4),(-2,-4),(1,-4),(-3,-3),(3,1),(-5,1)]
    for lx, ly in leaf_dirs:
        # Draw leaf with rounded puff: paint 5 steps + side pixels for fullness
        for i in range(5):
            t = i / 4.0
            px2 = round(top_x + lx*t)
            py2 = round(top_y + ly*t)
            col = blend(LEAF_L, LEAF_D, t)
            set_px(canvas, px2,   py2,   col)
            set_px(canvas, px2,   py2-1, blend(col, SKY_B, 0.35))
            # side fill for roundness
            if i == 2:
                set_px(canvas, px2-1, py2,   blend(col, LEAF_D, 0.3))
                set_px(canvas, px2+1, py2,   blend(col, LEAF_D, 0.3))
                set_px(canvas, px2,   py2+1, blend(col, LEAF_D, 0.4))


# ── Colors ──
SKY_A    = (108, 165, 205)   # AC: 偏灰蓝绿，衬托兔子
SKY_B    = (135, 188, 218)   # 更亮，带点灰
SKY_HZ   = (158, 205, 225)   # 地平线几乎白

OCEAN_T  = (72, 192, 202)    # AC: 浅碧绿
OCEAN_M  = (42, 158, 178)
OCEAN_D  = (25, 118, 148)
OCEAN_SH = (168, 238, 242)   # 高光更亮

SAND     = (62, 52, 38)      # 黑沙保留，稍暖
SAND_L   = (85, 72, 55)
SAND_D   = (42, 35, 25)

# Hut
HUT_W    = (252, 245, 228)   # 奶白
HUT_SH   = (208, 198, 178)
HUT_RF   = (222, 205, 175)   # 茅草暖棕
HUT_RFD  = (188, 168, 138)
HUT_WIN  = (108, 158, 195)   # 窗户天蓝
HUT_DOOR = (112, 98, 78)
HUT_STLT = (178, 158, 128)
HUT_RED  = (215, 55, 42)     # AC暖红
HUT_RAIL = (232, 222, 202)

# Palms
TRUNK    = (128, 95, 48)
TRUNK_D  = (95, 68, 28)
LEAF     = (72, 165, 68)     # AC绿，饱和
LEAF_D   = (48, 122, 48)
LEAF_L   = (112, 205, 88)
COCONUT  = (95, 112, 58)

# Kayak
KAYAK_Y  = (238, 195, 45)    # AC黄，更亮
KAYAK_YD = (188, 148, 22)
KAYAK_YL = (255, 228, 95)
KAYAK_IN = (118, 95, 65)
KAYAK_RIM= (162, 122, 15)

# Characters
GB       = (198, 122, 58)    # 姜饼暖橙
GBD      = (152, 92, 40)
GBE      = (65, 38, 18)
GB_CHEEK = (235, 158, 105)
GB_ICING = (248, 238, 215)
HAT_RED  = (205, 52, 38)
HAT_DARK = (148, 30, 22)
HAT_LITE = (232, 82, 62)

BUN      = (168, 215, 255)   # 蓝兔：更清透
BUNK     = (235, 158, 178)
BUN_LT   = (205, 235, 255)
BUNE     = (42, 25, 65)
BUN_BLUSH= (242, 165, 182)
BUN_SMILE= (248, 240, 225)

# ══════════════════════════════════════════
# LAYER 1: SKY  (y=0~13)
# ══════════════════════════════════════════
for y in range(0, 14):
    t = y / 13
    col = blend(SKY_A, SKY_B, t)
    wrow(canvas, y, 0, W-1, col)
# Horizon glow
for y in range(14, 16):
    t = (y-14)
    col = blend(SKY_B, SKY_HZ, t)
    wrow(canvas, y, 0, W-1, col)

# ══════════════════════════════════════════
# LAYER 2: OCEAN  (base fill, mostly covered by wave logic)
# ══════════════════════════════════════════
for y in range(32, H):
    t = min((y-32)/4, 1)
    col = blend(OCEAN_T, OCEAN_D, t)
    wrow(canvas, y, 0, W-1, col)

# ══════════════════════════════════════════
draw_palm_silhouette(22, 17, lean_dir=-3, droop=2, crown_dx=1, crown_dy=1)
draw_palm_silhouette(42, 16, lean_dir=-1)
draw_palm_silhouette(32, 15, lean_dir=1)
draw_palm_silhouette(43, 15, lean_dir=2, color=PALM_SIL_DIM)
# LAYER 3: BLACK SAND  (y=16~35)
# ══════════════════════════════════════════
fill(canvas, 16, H-1, 0, W-1, SAND)
wrow(canvas, 16, 0, W-1, SAND_L)
wrow(canvas, 17, 0, W-1, blend(SAND, SAND_L, 0.5))
# Sand texture
for x in range(0, W, 6):
    set_px(canvas, x,   19, SAND_L)
    set_px(canvas, x+2, 21, SAND_D)
    set_px(canvas, x+4, 23, SAND_L)
    set_px(canvas, x+1, 24, SAND_D)
    set_px(canvas, x+3, 27, SAND_L)
    set_px(canvas, x,   30, SAND_D)
    set_px(canvas, x+5, 32, SAND_L)

# ══════════════════════════════════════════
# WAVE EDGE — 海浪冲上沙滩，像素锯齿波形
# wave_profile[x] = 海水顶部 y 值（越小越往上冲）
# ══════════════════════════════════════════
FOAM   = (235, 248, 252)   # 泡沫白
FOAM_D = (172, 218, 228)   # 泡沫阴影
WAVE_C = (68, 182, 202)    # 波峰亮色

# 手绘波形：每格定义海水顶边 y（基准 y=25，波峰可到 y=22，退潮 y=26）
wave_top = [
    35,35,34,34,33,33,32,32,33,33,34,34,35,35,35,35,34,34,33,33,
    32,32,33,33,34,34,35,35,35,35,34,34,33,33,32,32,33,33,34,34,
    35,35,35,35,34,34,33,33,32,32,33,33,34,34,35,35,35,35,34,34,
    33,33,32,32
]

for x in range(W):
    wy = wave_top[x]
    # 海水从 wy 往下填
    for y in range(wy, H):
        t = min((y-32)/4, 1)
        col = blend(OCEAN_T, OCEAN_D, max(t,0))
        set_px(canvas, x, y, col)
    # 波峰亮线
    set_px(canvas, x, wy, WAVE_C)
    # 泡沫（波峰上方1~2格）
    if wy <= 34:
        set_px(canvas, x, wy-1, FOAM)
    if wy <= 33:
        set_px(canvas, x, wy-2, FOAM_D)
    # 泡沫渗入沙中
    if wy == 35 or wy == 36:
        if x % 3 == 0:
            set_px(canvas, x, wy-1, FOAM_D)
# Sparkles on water
for x in [2,8,14,20,27,34,40,47,54,60]: set_px(canvas, x, 37 if 37<H else H-1, OCEAN_SH)
for x in [5,11,17,24,31,37,44,51,58]:   set_px(canvas, x, 39 if 39<H else H-1, OCEAN_SH)

# ══════════════════════════════════════════
# PALMS — symmetric: left x=3, right x=59
# ══════════════════════════════════════════

# ── Silhouette palms (bottom layer) ──
# ── Coloured palms (above silhouettes) ──
draw_palm(50, 17, lean_dir=2, crown_dx=-1)
draw_palm(14,  17, lean_dir=-2, crown_dx=1)
draw_palm(50, 15, lean_dir=-3)
draw_palm(16,  16, lean_dir=2)


# Behind hut placeholder (drawn at end)

# ══════════════════════════════════════════
# Silhouette palms — bottom layer (drawn first)


# HUT — centered at x=27~37, elevated on stilts
# ══════════════════════════════════════════
HX1, HX2 = 27, 37
SY = 18              # deck level (-4)

# ── All palms (drawn before house) ──

# Stilts
for sx in [28,29,35,36]:
    for sy in range(SY+1, 25): set_px(canvas, sx, sy, HUT_STLT)
wrow(canvas, 17, 28, 36, HUT_STLT)  # cross-brace

# Deck platform
wrow(canvas, SY+1, HX1-1, HX2+1, HUT_SH)

# ── Ladder (right of hut, going down) ──
LADDER   = (178, 152, 112)
LADDER_D = (138, 115, 82)
LDX = HX2 + 2   # x=39, ladder left rail
# Two vertical rails
for ly in range(SY, SY+6):
    set_px(canvas, LDX,   ly, LADDER)
    set_px(canvas, LDX+2, ly, LADDER)
# Rungs (every 2 rows, full width between rails)
for ly in [SY+1, SY+3, SY+5]:
    wrow(canvas, ly, LDX, LDX+2, LADDER)


# Walls
# Wall with trapezoid shape: top 19px wide, bottom 11px wide
CX = (HX1 + HX2) // 2  # center x = 32
wall_top = 7; wall_bot = SY - 1
wall_rows = wall_bot - wall_top  # 10
for wy in range(wall_top, wall_bot + 1):
    t = (wy - wall_top) / wall_rows if wall_rows > 0 else 0
    half = round(9.5 - t * 4)  # top half=9.5→19px, bot half=5.5→11px
    wx1 = CX - half; wx2 = CX + half
    wrow(canvas, wy, wx1, wx2, HUT_W)

# Roof pitched
# Two symmetric roofs, centered at x=27 and x=37
for rc in [26, 32, 38]:
    wrow(canvas, 6, rc-3, rc+3, HUT_RF)
    wrow(canvas, 5, rc-2, rc+2, HUT_RF)
    if rc != 32:
        wrow(canvas, 4, rc-1, rc+1, HUT_RF)
wrow(canvas, 6, 32-3, 32+3, HUT_RF)
wrow(canvas, 5, 32-2, 32+2, HUT_RF)
# trim corners
for tx, ty in [(27,4),(28,5)]:
    set_px(canvas, tx, ty, blend(SKY_A, SKY_B, ty/13))
for tx, ty in [(37,4),(36,5)]:
    set_px(canvas, tx, ty, blend(SKY_A, SKY_B, ty/13))
# One wide window following wall trapezoid shape, 2px inset from each side
wall_top = 7; wall_bot = SY - 1; wall_rows = wall_bot - wall_top
for wy in range(8, 13):
    t = (wy - wall_top) / wall_rows if wall_rows > 0 else 0
    half = round(9.5 - t * 4)
    wx1 = CX - half; wx2 = CX + half
    wrow(canvas, wy, wx1+2, wx2-2, HUT_WIN)
    # two vertical dividers at 1/3 and 2/3 of window width, shifted outward 1px, house color
    wl = wx1+2; wr = wx2-2
    set_px(canvas, round(wl + (wr-wl)/3)   - 2, wy, HUT_W)
    set_px(canvas, round(wl + (wr-wl)*2/3) + 2, wy, HUT_W)

wrow(canvas, SY, 22, 42, HUT_RAIL)  # top rail
wrow(canvas, SY-3, 22, 42, HUT_RAIL)  # bottom rail
for rx in [22, 42]:
    for ry in range(SY-3, SY+1): set_px(canvas, rx, ry, HUT_RAIL)
# vertical pickets every 2 cols
for px in range(24, 42, 2):
    for ry in range(SY-3, SY+1): set_px(canvas, px, ry, HUT_RAIL)


# Door
# Door is on the side/back, not visible

# ══════════════════════════════════════════
# GINGERBREAD — front puller (GCX=12, GFY=26)
# ══════════════════════════════════════════

GCX, GFY = 12, 24

# Legs
set_px(canvas, GCX-1, GFY, GB); set_px(canvas, GCX, GFY, GB)
# Body
fill(canvas, GFY-5, GFY-1, GCX-2, GCX+2, GB)
set_px(canvas, GCX, GFY-4, GB_CHEEK); set_px(canvas, GCX, GFY-2, GB_CHEEK)
# Head
fill(canvas, GFY-11, GFY-6, GCX-3, GCX+3, GB)
# Remove head corners
set_px(canvas, GCX-3, GFY-11, blend(SKY_A, SKY_B, (GFY-11)/13))
set_px(canvas, GCX+3, GFY-11, blend(SKY_A, SKY_B, (GFY-11)/13))
set_px(canvas, GCX-3, GFY-6,  blend(GB, SAND_L, 0.5))
set_px(canvas, GCX+3, GFY-6,  blend(GB, SAND_L, 0.5))
# Face
set_px(canvas, GCX-1, GFY-9, GBE)
set_px(canvas, GCX+1, GFY-9, GBE)
set_px(canvas, GCX-2, GFY-8, GB_CHEEK)
set_px(canvas, GCX+2, GFY-8, GB_CHEEK)
for dx in [-1,0,1]: set_px(canvas, GCX+dx, GFY-7, GB_ICING)
# Hat
set_px(canvas, GCX+1, GFY-13, HAT_DARK)
for dx in range(-1,4): set_px(canvas, GCX+dx, GFY-12, HAT_RED)
for dx in range(-1,4): set_px(canvas, GCX+dx, GFY-11, HAT_RED)
set_px(canvas, GCX-1, GFY-12, HAT_DARK); set_px(canvas, GCX+3, GFY-12, HAT_DARK)
set_px(canvas, GCX-1, GFY-11, HAT_DARK); set_px(canvas, GCX+3, GFY-11, HAT_DARK)
set_px(canvas, GCX, GFY-12, HAT_LITE)
# Forward arm (placeholder, redrawn below)
set_px(canvas, GCX-3, GFY-4, GB)

# ══════════════════════════════════════════
# BUNNY — back pusher (BCX=51, BFY=26)
# ══════════════════════════════════════════
BCX, BFY = 51, 24

# Ears
for y in range(BFY-15, BFY-11):
    set_px(canvas, BCX-2, y, BUN_LT); set_px(canvas, BCX-1, y, BUNK)
    set_px(canvas, BCX+1, y, BUN_LT); set_px(canvas, BCX+2, y, BUNK)
set_px(canvas, BCX-2, BFY-15, BUN); set_px(canvas, BCX+1, BFY-15, BUN)
# Legs
set_px(canvas, BCX-1, BFY, BUN); set_px(canvas, BCX, BFY, BUN)
# Body
fill(canvas, BFY-5, BFY-1, BCX-2, BCX+2, BUN)
# Head
fill(canvas, BFY-11, BFY-6, BCX-3, BCX+3, BUN)
# Round BUN head corners
set_px(canvas, BCX-3, BFY-11, blend(SKY_A, SKY_B, (BFY-11)/13))
set_px(canvas, BCX+3, BFY-11, blend(SKY_A, SKY_B, (BFY-11)/13))
set_px(canvas, BCX-3, BFY-6,  blend(BUN, SAND_L, 0.5))
set_px(canvas, BCX+3, BFY-6,  blend(BUN, SAND_L, 0.5))
set_px(canvas, BCX-2, BFY-10, BUN_LT)
set_px(canvas, BCX-1, BFY-9, BUNE); set_px(canvas, BCX+1, BFY-9, BUNE)
# 连心眉 (y=BFY-10)
set_px(canvas, BCX-2, BFY-10, BUNE)
set_px(canvas, BCX-1, BFY-10, BUNE)
set_px(canvas, BCX,   BFY-10, blend(BUN, BUNE, 0.3))
set_px(canvas, BCX+1, BFY-10, BUNE)
set_px(canvas, BCX+2, BFY-10, BUNE)
set_px(canvas, BCX-1, BFY-9, BUNE)
set_px(canvas, BCX+1, BFY-9, BUNE)
set_px(canvas, BCX-2, BFY-8, BUN_BLUSH); set_px(canvas, BCX+2, BFY-8, BUN_BLUSH)
set_px(canvas, BCX, BFY-8, BUNK)
for dx in [-1,0,1]: set_px(canvas, BCX+dx, BFY-7, BUN_SMILE)
# Back arm (placeholder)
set_px(canvas, BCX+3, BFY-4, BUN)

# ══════════════════════════════════════════
# GB legs (split, thick)
for py in [GFY+1, GFY+2]:
    set_px(canvas, GCX-2, py, GB); set_px(canvas, GCX-1, py, GB)
    set_px(canvas, GCX+1, py, GB); set_px(canvas, GCX+2, py, GB)
# BUN legs (split, thick)
for py in [BFY+1, BFY+2]:
    set_px(canvas, BCX-2, py, BUN); set_px(canvas, BCX-1, py, BUN)
    set_px(canvas, BCX+1, py, BUN); set_px(canvas, BCX+2, py, BUN)

# KAYAK — x=11~52, y=24~26
# ══════════════════════════════════════════
KX1, KX2 = 11, 52
KY1, KY2 = 24, 26

# Top row (narrower)
wrow(canvas, KY1,   10, 53, KAYAK_YL)
# Middle row (widest, with tapered tips)
wrow(canvas, KY1+1, KX1+2, KX2-2, KAYAK_Y)
set_px(canvas, KX1+1, KY1+1, KAYAK_Y)
set_px(canvas, KX1,   KY1+1, KAYAK_Y)
set_px(canvas, KX2-1, KY1+1, KAYAK_Y)
set_px(canvas, KX2,   KY1+1, KAYAK_Y)
# Bottom row (narrower)
wrow(canvas, KY2,   13, 50, KAYAK_YD)
# Rim lines
wrow(canvas, KY1-1, 11, 52, KAYAK_Y)
wrow(canvas, KY2+1, KX1+4, KX2-4, KAYAK_RIM)
# Cockpits
fill(canvas, KY1, KY1+1, 17, 22, KAYAK_IN)
fill(canvas, KY1, KY1+1, 40, 45, KAYAK_IN)
# Seat bottom corners (round)
set_px(canvas, 17, KY1+1, KAYAK_Y); set_px(canvas, 22, KY1+1, KAYAK_Y)
set_px(canvas, 40, KY1+1, KAYAK_Y); set_px(canvas, 45, KY1+1, KAYAK_Y)

# Arms redrawn after kayak
# GB forward arm (left, horizontal)
set_px(canvas, GCX-3, GFY-4, GB); set_px(canvas, GCX-4, GFY-4, GB); set_px(canvas, GCX-5, GFY-4, GB)
# GB inner arm (right, toward kayak)
set_px(canvas, GCX+3, GFY-4, GB); set_px(canvas, GCX+4, GFY-3, GB)
set_px(canvas, GCX+5, GFY-2, GB)
set_px(canvas, GCX+5, GFY-1, GB)
# GB paddle (vertical, 1px shaft, blades top and bottom)
PADDLE_W = (178, 138, 88)
PADDLE_D = (128, 95, 55)
for py in range(GFY-9, GFY-1):
    set_px(canvas, GCX-6, py, PADDLE_W)
# Top blade (rounded corners), connected to shaft top
for py in range(GFY-16, GFY-9):
    if py in [GFY-16, GFY-10]:
        set_px(canvas, GCX-6, py, PADDLE_W)
    else:
        for px in [GCX-5, GCX-6, GCX-7]:
            set_px(canvas, px, py, PADDLE_D if px == GCX-5 else PADDLE_W)
# Bottom blade up 2, rounded corners
for py in range(GFY-3, GFY+4):
    if py in [GFY-3, GFY+3]:
        set_px(canvas, GCX-6, py, PADDLE_W)
    else:
        for px in [GCX-5, GCX-6, GCX-7]:
            set_px(canvas, px, py, PADDLE_D if px == GCX-5 else PADDLE_W)
# BUN back arm (right, horizontal)
set_px(canvas, BCX+3, BFY-4, BUN); set_px(canvas, BCX+4, BFY-4, BUN); set_px(canvas, BCX+5, BFY-4, BUN)
# BUN inner arm (left, toward kayak)
set_px(canvas, BCX-3, BFY-4, BUN); set_px(canvas, BCX-4, BFY-3, BUN)
set_px(canvas, BCX-5, BFY-2, BUN); set_px(canvas, BCX-5, BFY-1, BUN)
# BUN paddle (vertical, 1px shaft, mirror of GB)
for py in range(BFY-9, BFY-1):
    set_px(canvas, BCX+6, py, PADDLE_W)
# Top blade
for py in range(BFY-16, BFY-9):
    if py in [BFY-16, BFY-10]:
        set_px(canvas, BCX+6, py, PADDLE_W)
    else:
        for px in [BCX+5, BCX+6, BCX+7]:
            set_px(canvas, px, py, PADDLE_D if px == BCX+7 else PADDLE_W)
# Bottom blade up 2
for py in range(BFY-3, BFY+4):
    if py in [BFY-3, BFY+3]:
        set_px(canvas, BCX+6, py, PADDLE_W)
    else:
        for px in [BCX+5, BCX+6, BCX+7]:
            set_px(canvas, px, py, PADDLE_D if px == BCX+7 else PADDLE_W)

# ══════════════════════════════════════════

# Save
# ══════════════════════════════════════════
img = Image.new('RGB', (W*SCALE, H*SCALE))
for y in range(H):
    for x in range(W):
        col = canvas[y][x]
        for sy in range(SCALE):
            for sx in range(SCALE):
                img.putpixel((x*SCALE+sx, y*SCALE+sy), col)
img.save('pixel_beachhut.png')
print(f'Saved: {W*SCALE}×{H*SCALE}px')
