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

# ── Colors ──
SKY_A    = (88, 158, 228)
SKY_B    = (138, 198, 248)
SKY_HZ   = (195, 228, 252)

OCEAN_T  = (68, 178, 198)
OCEAN_M  = (38, 145, 168)
OCEAN_D  = (22, 108, 135)
OCEAN_SH = (152, 228, 238)

SAND     = (48, 42, 35)
SAND_L   = (68, 60, 50)
SAND_D   = (35, 30, 22)

# Hut
HUT_W    = (245, 242, 235)
HUT_SH   = (195, 188, 172)
HUT_RF   = (188, 172, 148)
HUT_RFD  = (152, 138, 118)
HUT_WIN  = (145, 188, 222)
HUT_DOOR = (105, 95, 78)
HUT_STLT = (168, 152, 125)
HUT_RED  = (208, 42, 32)
HUT_RAIL = (222, 215, 198)

# Palms
TRUNK    = (120, 88, 42)
TRUNK_D  = (88, 62, 25)
LEAF     = (58, 148, 62)
LEAF_D   = (38, 108, 44)
LEAF_L   = (98, 188, 82)
COCONUT  = (88, 105, 55)

# Kayak
KAYAK_Y  = (228, 185, 35)
KAYAK_YD = (178, 138, 18)
KAYAK_YL = (255, 222, 82)
KAYAK_IN = (78, 58, 38)
KAYAK_RIM= (152, 115, 12)

# Characters
GB       = (185, 108, 48)
GBD      = (140, 82, 35)
GBE      = (62, 35, 15)
GB_CHEEK = (225, 148, 95)
GB_ICING = (245, 232, 210)
HAT_RED  = (198, 42, 32)
HAT_DARK = (140, 26, 20)
HAT_LITE = (225, 72, 55)

BUN      = (158, 208, 255)
BUNK     = (228, 148, 168)
BUN_LT   = (198, 228, 255)
BUNE     = (38, 22, 60)
BUN_BLUSH= (235, 155, 172)
BUN_SMILE= (242, 235, 220)

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
def draw_palm(cx, base_y, lean_dir=1):
    for i in range(12):
        lx = cx + lean_dir * (i // 4)
        ly = base_y - i
        set_px(canvas, lx,   ly, TRUNK)
        set_px(canvas, lx+1, ly, TRUNK_D)
    top_x = cx + lean_dir * 3
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

draw_palm(4,  17, lean_dir=1)
draw_palm(10, 17, lean_dir=1)
draw_palm(59, 17, lean_dir=-1)
draw_palm(53, 17, lean_dir=-1)
# Extra trees — different heights and lean angles
draw_palm(0,  20, lean_dir=1)   # far left, shorter, slight lean
draw_palm(7,  14, lean_dir=-1)  # left inner, taller, leans back
draw_palm(14, 19, lean_dir=1)   # left mid, medium
draw_palm(63, 20, lean_dir=-1)  # far right, shorter
draw_palm(56, 14, lean_dir=1)   # right inner, taller, leans back
draw_palm(49, 19, lean_dir=-1)  # right mid, medium

# ══════════════════════════════════════════
# HUT — centered at x=27~37, elevated on stilts
# ══════════════════════════════════════════
HX1, HX2 = 27, 37
SY = 15              # deck level (-4)

# Stilts
for sx in [28,29,35,36]:
    for sy in range(SY+1, 25): set_px(canvas, sx, sy, HUT_STLT)
wrow(canvas, 17, 28, 36, HUT_STLT)  # cross-brace

# Deck platform
wrow(canvas, SY,   HX1-1, HX2+1, HUT_W)
wrow(canvas, SY+1, HX1-1, HX2+1, HUT_SH)

# Railing
wrow(canvas, SY-1, HX1+1, HX2-1, HUT_RAIL)
for rx in [HX1+1, HX2-1]:
    set_px(canvas, rx, SY-2, HUT_RAIL)
    set_px(canvas, rx, SY-1, HUT_RAIL)

# Walls
fill(canvas, 7, SY-1, HX1, HX2, HUT_W)
fill(canvas, 7, SY-1, HX2, HX2, HUT_SH)

# Roof pitched
wrow(canvas, 6, HX1-1, HX2+1, HUT_RFD)
wrow(canvas, 5, HX1,   HX2,   HUT_RF)
wrow(canvas, 4, HX1+1, HX2-1, HUT_RF)
wrow(canvas, 3, HX1+2, HX2-2, HUT_RF)
set_px(canvas, 31, 2, HUT_RFD)
set_px(canvas, 32, 2, HUT_RFD)
set_px(canvas, 32, 1, HUT_RFD)

# Two windows
fill(canvas, 8, 12, HX1+1, HX1+4, HUT_WIN)
wrow(canvas, 10, HX1+1, HX1+4, HUT_SH)
for y in range(8,13): set_px(canvas, HX1+2, y, HUT_SH)

fill(canvas, 8, 12, HX2-4, HX2-1, HUT_WIN)
wrow(canvas, 10, HX2-4, HX2-1, HUT_SH)
for y in range(8,13): set_px(canvas, HX2-3, y, HUT_SH)

# Door
fill(canvas, 12, SY-1, 31, 33, HUT_DOOR)

# ══════════════════════════════════════════
# GINGERBREAD — front puller (GCX=12, GFY=26)
# ══════════════════════════════════════════
GCX, GFY = 12, 24

# Legs
set_px(canvas, GCX-1, GFY, GB); set_px(canvas, GCX, GFY, GB)
# Body
fill(canvas, GFY-5, GFY-1, GCX-2, GCX+2, GB)
fill(canvas, GFY-5, GFY-1, GCX-2, GCX-2, GBD)
fill(canvas, GFY-5, GFY-1, GCX+2, GCX+2, GBD)
for by in [GFY-4, GFY-3]: set_px(canvas, GCX, by, GB_ICING)
# Head
fill(canvas, GFY-11, GFY-6, GCX-3, GCX+3, GB)
for dx,dy in [(-3,-5),(3,-5),(-3,0),(3,0)]:
    set_px(canvas, GCX+dx, GFY-11+5+dy, blend(GB, SKY_B, 0.6))
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
# Forward arm
set_px(canvas, GCX-3, GFY-4, GB)
set_px(canvas, GCX-4, GFY-3, GB)

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
fill(canvas, BFY-5, BFY-1, BCX-2, BCX-2, blend(BUN,(80,80,80),0.12))
fill(canvas, BFY-5, BFY-1, BCX+2, BCX+2, blend(BUN,(80,80,80),0.12))
# Head
fill(canvas, BFY-11, BFY-6, BCX-3, BCX+3, BUN)
set_px(canvas, BCX-2, BFY-10, BUN_LT)
set_px(canvas, BCX-1, BFY-9, BUNE); set_px(canvas, BCX+1, BFY-9, BUNE)
set_px(canvas, BCX-2, BFY-8, BUN_BLUSH); set_px(canvas, BCX+2, BFY-8, BUN_BLUSH)
set_px(canvas, BCX, BFY-8, BUNK)
for dx in [-1,0,1]: set_px(canvas, BCX+dx, BFY-7, BUN_SMILE)
# Back arm
set_px(canvas, BCX+3, BFY-4, BUN)
set_px(canvas, BCX+4, BFY-3, BUN)

# ══════════════════════════════════════════
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

# Arms redrawn after kayak
# GB forward arm (left)
set_px(canvas, GCX-3, GFY-4, GB); set_px(canvas, GCX-4, GFY-3, GB)
# GB inner arm (right, toward kayak)
set_px(canvas, GCX+3, GFY-4, GB); set_px(canvas, GCX+4, GFY-3, GB)
set_px(canvas, GCX+5, GFY-2, GB)
set_px(canvas, GCX+5, GFY-1, GB)
# BUN back arm (right)
set_px(canvas, BCX+3, BFY-4, BUN); set_px(canvas, BCX+4, BFY-3, BUN)
# BUN inner arm (left, toward kayak)
set_px(canvas, BCX-3, BFY-4, BUN); set_px(canvas, BCX-4, BFY-3, BUN)
set_px(canvas, BCX-5, BFY-2, BUN); set_px(canvas, BCX-5, BFY-1, BUN)

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
