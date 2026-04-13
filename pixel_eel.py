from PIL import Image
import math

W, H = 64, 36
SCALE = 12

def blend(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(c1[i]*(1-t) + c2[i]*t) for i in range(3))

def set_px(canvas, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        canvas[y][x] = list(color)

def wrow(canvas, y, x1, x2, color):
    for x in range(x1, min(x2+1, W)):
        set_px(canvas, x, y, color)

# ── 水色：热带蓝绿 ────────────────────────────────────────────────────────────
DEEP    = (10,  48,  72)   # 深水：偏暖深蓝
MID     = (22,  98, 128)   # 中水：蓝绿偏暖
SURF    = (45, 158, 162)   # 浅水：蓝绿暖
SURF_LT = (75, 198, 192)   # 水面：偏绿暖

# ── 角色 ──────────────────────────────────────────────────────────────────────
GB       = (185, 108,  48)
GBD      = (110,  65,  22)
GBE      = ( 62,  35,  15)
GB_CHEEK = (225, 148,  95)
GB_ICING = (245, 232, 210)
HAT_RED  = (198,  42,  32)
HAT_DARK = (140,  26,  20)
HAT_LITE = (225,  72,  55)

BUN      = (112, 172, 232)
BUN_LT   = (155, 205, 248)
BUND     = ( 40,  75, 130)
BUN_EYE  = ( 38,  22,  60)
BUN_BLUSH= (235, 155, 172)
BUN_SMILE= (242, 235, 220)

# ── 鳗鱼 ──────────────────────────────────────────────────────────────────────
EEL_BASE  = (195, 158,  68)   # 鳗鱼体：暖黄褐
EEL_PAT   = ( 88,  52,  18)   # 斑纹：深棕
EEL_BELLY = (232, 212, 148)   # 腹部：奶黄
EEL_EYE   = ( 20,  15,   8)

# ── 珊瑚 ──────────────────────────────────────────────────────────────────────
CORAL_PINK   = (232, 108,  95)   # 粉红：动森珊瑚粉，偏暖
CORAL_ORANGE = (225, 138,  55)   # 橙：暖橙
CORAL_GREEN  = ( 82, 168,  98)   # 绿：动森草绿
CORAL_PURPLE = (145,  98, 182)   # 紫：柔紫
CORAL_BLUE   = ( 78, 155, 182)   # 蓝：动森天蓝

canvas = [[list(DEEP)] * W for _ in range(H)]

# 背景渐变
for y in range(H):
    t = y / (H - 1)
    if t < 0.25:
        col = blend(SURF_LT, SURF, t / 0.25)
    elif t < 0.55:
        col = blend(SURF, MID, (t - 0.25) / 0.3)
    else:
        col = blend(MID, DEEP, (t - 0.55) / 0.45)
    for x in range(W):
        canvas[y][x] = list(col)

# 光线（斜射，几条浅竖条）
for rx in [10, 24, 40, 54]:
    for y in range(0, 20):
        t = y / 20
        alpha = 0.18 * (1 - t)
        c = tuple(canvas[y][rx])
        canvas[y][rx] = list(blend(c, (200, 240, 248), alpha))

# ── 中层：球状珊瑚 ─────────────────────────────────────────────────────────────
def draw_coral(cx, cy, r, col):
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                set_px(canvas, cx + dx, cy + dy, col)
    # 暗边
    dk = blend(col, (20, 20, 20), 0.25)
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            dist2 = dx * dx + dy * dy
            if r * r - 2 * r < dist2 <= r * r:
                set_px(canvas, cx + dx, cy + dy, dk)
    # 材质：竖向沟纹
    groove = blend(col, (10, 10, 10), 0.15)
    inner = r - 1
    for dx in range(-inner, inner + 1, 2):
        for dy in range(-inner, inner + 1):
            if dx * dx + dy * dy <= inner * inner:
                set_px(canvas, cx + dx, cy + dy, groove)
    # 高光
    hi = blend(col, (255, 255, 255), 0.32)
    set_px(canvas, cx - 1, cy - r + 1, hi)
    set_px(canvas, cx,     cy - r,     hi)

corals = [
    ( 7, 26, 6, CORAL_PINK),
    (18, 24, 5, CORAL_ORANGE),
    (29, 27, 7, CORAL_GREEN),
    (40, 25, 5, CORAL_PURPLE),
    (50, 26, 6, CORAL_BLUE),
    (59, 24, 4, CORAL_ORANGE),
    (22, 31, 4, CORAL_PINK),
    (44, 30, 5, CORAL_GREEN),
    (54, 30, 3, CORAL_PURPLE),
]

# ── 鳗鱼 Z字型（绘制顺序：远→珊瑚盖住→斜→近）────────────────────────────────
# 预存需要去掉的角落水色
water_36_20 = tuple(canvas[20][36])
water_28_34 = tuple(canvas[34][28])
water_mouth1 = tuple(canvas[22][20])  # HY=22, HX-3=20
water_mouth2 = tuple(canvas[22][21])  # HY=22, HX-2=21
EEL_BASE_FAR  = (140, 118,  50)
EEL_PAT_FAR   = ( 55,  35,  10)
EEL_BELLY_FAR = (185, 168, 112)

def draw_eel_seg(x0, y0, x1, y1, base, belly, pat, thick=2):
    dx = x1 - x0; dy = y1 - y0
    steps = max(abs(dx), abs(dy))
    if steps == 0: return
    for i in range(steps + 1):
        t = i / steps
        cx = int(x0 + dx * t); cy = int(y0 + dy * t)
        for dk in range(-thick, thick + 1):
            set_px(canvas, cx, cy + dk, belly if dk == 0 else base)
        if i % 4 == 0:
            set_px(canvas, cx, cy - thick, pat)
            if thick > 1: set_px(canvas, cx, cy - thick + 1, pat)

# 1. 顶段（远/暗）先画，最底层 → 现在在下方 y=32
draw_eel_seg(28, 32, 61, 32, EEL_BASE_FAR, EEL_BELLY_FAR, EEL_PAT_FAR, thick=2)

# 2. 珊瑚（有前后顺序：先画后层，后画前层）
# 右侧珊瑚丛（后→前）
draw_coral(63, 26, 4, CORAL_ORANGE)
draw_coral(60, 32, 3, CORAL_PURPLE)
draw_coral(54, 28, 6, CORAL_BLUE)
draw_coral(48, 32, 5, CORAL_GREEN)
draw_coral(44, 27, 5, CORAL_PURPLE)

# 左侧珊瑚丛（绿在最后面，橙/粉压在前）
draw_coral(16, 33, 7, CORAL_GREEN)   # 绿色左移，最后面
draw_coral(13, 34, 4, CORAL_PURPLE)    # 原粉球改紫色，左移2格
draw_coral(3,  33, 6, CORAL_PINK)
draw_coral(9, 29, 5, CORAL_ORANGE)  # 橙在最前面压绿

# 小鱼（珊瑚上方游动，热带蓝绿配色）
FISH = (38, 82, 118)
def draw_fish(fx, fy, d):
    wrow(canvas, fy-1, fx+1, fx+3, FISH)
    wrow(canvas, fy,   fx,   fx+4, FISH)
    wrow(canvas, fy+1, fx+1, fx+3, FISH)
    water_eye = tuple(canvas[fy][fx+3 if d==1 else fx+2])
    if d == 1:
        set_px(canvas, fx+3, fy, water_eye)
        set_px(canvas, fx-1, fy-1, FISH)
        set_px(canvas, fx-1, fy+1, FISH)
    else:
        set_px(canvas, fx+1, fy, water_eye)
        set_px(canvas, fx+5, fy-1, FISH)
        set_px(canvas, fx+5, fy+1, FISH)

for fx, fy, d in [(12,20,1),(3,18,-1),(8,14,1),(50,19,-1),(58,17,1)]:
    draw_fish(fx, fy, d)

# 3. 斜段画在珊瑚之后（从 y=32 斜到 y=22）
for i in range(9):
    t = i / 8
    cx = 28 + i; cy = 32 - int(10 * t)
    bc = blend(EEL_BASE_FAR, EEL_BASE, t)
    blc = blend(EEL_BELLY_FAR, EEL_BELLY, t)
    pc = blend(EEL_PAT_FAR, EEL_PAT, t)
    for dk in range(-2, 3):
        set_px(canvas, cx, cy + dk, blc if dk == 0 else bc)
    if i % 2 == 0:
        set_px(canvas, cx, cy - 2, pc)

# 4. 底段（近/亮）最后画，在最前层 → 现在在上方 y=22
draw_eel_seg(23, 22, 36, 22, EEL_BASE, EEL_BELLY, EEL_PAT, thick=2)

# 头部（底段左端，近处）
HX = 23
HY = 22
wrow(canvas, HY - 2, HX - 2, HX + 1, EEL_BASE)
wrow(canvas, HY - 1, HX - 2, HX + 1, EEL_BASE)
wrow(canvas, HY,     HX - 2, HX + 1, EEL_BELLY)
wrow(canvas, HY + 1, HX - 2, HX + 1, EEL_BASE)
wrow(canvas, HY + 2, HX - 2, HX + 1, EEL_BASE)
set_px(canvas, HX - 3, HY - 1, EEL_BASE)
set_px(canvas, HX - 3, HY + 1, EEL_BASE)
set_px(canvas, HX - 3, HY,     EEL_BELLY)
set_px(canvas, HX, HY - 1, EEL_EYE)
# 右上角第一格去掉（用水色覆盖）
set_px(canvas, 36, 20, water_36_20)
set_px(canvas, 28, 34, water_28_34)
# 嘴张开：belly行左侧两格用水色覆盖
set_px(canvas, 20, 22, water_mouth1)
set_px(canvas, 21, 22, water_mouth2)

# ── 上层：姜饼人（横漂，头朝右，比例同 manta）──────────────────────────────
GHX, GHY = 24, 9   # 头中心

# 帽子（头顶，朝上）
set_px(canvas, GHX, GHY-5, HAT_DARK)
wrow(canvas, GHY-4, GHX-1, GHX+1, HAT_RED)
wrow(canvas, GHY-3, GHX-2, GHX+2, HAT_RED)
set_px(canvas, GHX, GHY-4, HAT_LITE)
set_px(canvas, GHX-1, GHY-4, HAT_DARK); set_px(canvas, GHX+1, GHY-4, HAT_DARK)

# 头（大，7宽×6高）
wrow(canvas, GHY-3, GHX-1, GHX+3, GB)
wrow(canvas, GHY-2, GHX-2, GHX+4, GB)
wrow(canvas, GHY-1, GHX-3, GHX+4, GB)
wrow(canvas, GHY,   GHX-3, GHX+4, GB)
wrow(canvas, GHY+1, GHX-3, GHX+4, GB)
wrow(canvas, GHY+2, GHX-2, GHX+3, GB)

# 面镜（占满右半脸，4格宽×4格高）
GOGGLE    = (45, 45, 45)
GOGGLE_IN = (215, 168, 108)
for dy in [-2, -1, 0]:
    wrow(canvas, GHY+dy, GHX+1, GHX+4, GOGGLE_IN)
set_px(canvas, GHX+3, GHY-1, GBE); set_px(canvas, GHX+1, GHY-1, GBE)
# 镜框
wrow(canvas, GHY-3, GHX+1, GHX+4, GOGGLE)
wrow(canvas, GHY+1, GHX+1, GHX+4, GOGGLE)
for dy in [-2, -1, 0]: set_px(canvas, GHX+5, GHY+dy, GOGGLE)
for dy in [-2, -1, 0]: set_px(canvas, GHX,   GHY+dy, GOGGLE)

# 吸管（右侧脸朝上）
TUBE = (45, 45, 45)
for dy in range(-8, -3): set_px(canvas, GHX+5, GHY+dy, TUBE)
set_px(canvas, GHX+4, GHY-8, TUBE)

# 身体（向左延伸，3格高）
for dy in [-1, 0, 1]:
    wrow(canvas, GHY+dy, GHX-7, GHX-4, GB)
set_px(canvas, GHX-6, GHY, GB_ICING)
set_px(canvas, GHX-4, GHY, GB_ICING)

# 手臂
set_px(canvas, GHX-5, GHY-2, GB); set_px(canvas, GHX-6, GHY-3, GB)
set_px(canvas, GHX-5, GHY+2, GB)

# 腿（从身体左端向左伸直，上下两条）
wrow(canvas, GHY-1, GHX-10, GHX-8, GB)
wrow(canvas, GHY+1, GHX-10, GHX-8, GB)

# ── 上层：蓝兔子（横漂，头朝右，比例同 manta）──────────────────────────────
BHX, BHY = 44, 9   # 头中心

# 耳朵（头顶，两耳向上，2列各3格）
for dy in range(-7, -3):
    set_px(canvas, BHX-1, BHY+dy, BUN); set_px(canvas, BHX, BHY+dy, BUN_LT)
    set_px(canvas, BHX+2, BHY+dy, BUN); set_px(canvas, BHX+3, BHY+dy, BUN_LT)
set_px(canvas, BHX-1, BHY-6, BUN_BLUSH); set_px(canvas, BHX+2, BHY-6, BUN_BLUSH)

# 头（大，7宽×6高）
wrow(canvas, BHY-3, BHX-1, BHX+3, BUN)
wrow(canvas, BHY-2, BHX-2, BHX+4, BUN)
wrow(canvas, BHY-1, BHX-3, BHX+4, BUN)
wrow(canvas, BHY,   BHX-3, BHX+4, BUN)
wrow(canvas, BHY+1, BHX-3, BHX+4, BUN)
wrow(canvas, BHY+2, BHX-2, BHX+3, BUN)

# 面镜（右半脸）
BGOGGLE    = (45, 45, 45)
BGOGGLE_IN = (148, 188, 215)
for dy in [-2, -1, 0]:
    wrow(canvas, BHY+dy, BHX+1, BHX+4, BGOGGLE_IN)
set_px(canvas, BHX+3, BHY-1, BUN_EYE); set_px(canvas, BHX+1, BHY-1, BUN_EYE)
wrow(canvas, BHY-3, BHX+1, BHX+4, BGOGGLE)
wrow(canvas, BHY+1, BHX+1, BHX+4, BGOGGLE)
for dy in [-2, -1, 0]: set_px(canvas, BHX+5, BHY+dy, BGOGGLE)
for dy in [-2, -1, 0]: set_px(canvas, BHX,   BHY+dy, BGOGGLE)

# 吸管（左侧脸朝上）
BTUBE = (45, 45, 45)
for dy in range(-8, -3): set_px(canvas, BHX+5, BHY+dy, BTUBE)
set_px(canvas, BHX+4, BHY-8, BTUBE)

# 身体（向左延伸）
for dy in [-1, 0, 1]:
    wrow(canvas, BHY+dy, BHX-7, BHX-4, BUN)

# 手臂
set_px(canvas, BHX-5, BHY-2, BUN); set_px(canvas, BHX-6, BHY-3, BUN)
set_px(canvas, BHX-5, BHY+2, BUN)

# 腿（从身体左端向左伸直，上下两条）
wrow(canvas, BHY-1, BHX-10, BHX-8, BUN)
wrow(canvas, BHY+1, BHX-10, BHX-8, BUN)

# ── 输出 ──────────────────────────────────────────────────────────────────────
img = Image.new('RGB', (W * SCALE, H * SCALE))
px = img.load()
for y in range(H):
    for x in range(W):
        c = tuple(canvas[y][x])
        for sy in range(SCALE):
            for sx in range(SCALE):
                px[x * SCALE + sx, y * SCALE + sy] = c

img.save('pixel_eel.png')
print(f'Saved: {W*SCALE}×{H*SCALE}px')
