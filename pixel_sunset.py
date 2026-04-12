from PIL import Image

W, H = 64, 36
S = 12

def set_px(canvas, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        canvas[y][x] = color

def wrow(canvas, y, x1, x2, color):
    for x in range(x1, min(x2+1, W)):
        set_px(canvas, x, y, color)

def fill(canvas, y1, y2, x1, x2, color):
    for y in range(y1, y2+1):
        wrow(canvas, y, x1, x2, color)

def blend(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(c1[i]*(1-t) + c2[i]*t) for i in range(3))

# ── Colors ───────────────────────────────────────────────────────────────────
SKY_TOP   = (58, 42, 105)   # 动森顶部：蓝紫偏暖
SKY_MID   = (148, 65, 108)  # 中部：玫瑰紫
SKY_WARM  = (218, 98, 68)   # 橙红（动森暖）
SKY_HOR   = (245, 178, 72)  # 地平线：暖黄橙
SUN_C     = (255, 242, 118) # 太阳中心：柔黄
SUN_O     = (248, 195, 65)  # 太阳外圈
SUN_GLOW  = (238, 138, 48)  # 光晕

SEA_TOP   = (215, 185, 165)  # 云海顶部：暖米白
SEA_DARK  = (148, 132, 158)  # 云海深处：冷紫灰
REFL_HI   = (248, 168, 85)   # 云顶受光：橙红
REFL_MID  = (205, 112, 58)   # 云中阴影：深橙红

ROCK      = (242, 228, 205)  # 云峰主色：奶白
ROCK_LIT  = (255, 245, 225)  # 云峰亮面：纯白
ROCK_RIM  = (255, 252, 240)  # 云峰顶边：最亮

GB        = (188, 112, 50)
GBD       = (145, 80, 32)
GBE       = (62, 35, 15)
GB_ICING  = (245, 232, 210)
GB_CHEEK  = (228, 152, 98)
HAT_RED   = (198, 42, 32)
HAT_DARK  = (140, 26, 20)
HAT_LITE  = (225, 72, 55)

BUN       = (98, 162, 218)
BUND      = (68, 112, 182)
BUNE      = (38, 22, 60)
BUN_LT    = (148, 198, 242)
BUN_BLUSH = (238, 158, 175)
BUNK      = (228, 148, 168)

def draw():
    HORIZON = 23  # 海平线 y
    ROCK_TOP = 27  # 礁石顶面 y

    canvas = [[SKY_TOP]*W for _ in range(H)]

    # ── Sky gradient (y=0–22) ─────────────────────────────────────────────────
    for y in range(HORIZON):
        t = y / (HORIZON - 1)
        if t < 0.35:
            col = blend(SKY_TOP, SKY_MID, t / 0.35)
        elif t < 0.65:
            col = blend(SKY_MID, SKY_WARM, (t - 0.35) / 0.30)
        else:
            col = blend(SKY_WARM, SKY_HOR, (t - 0.65) / 0.35)
        wrow(canvas, y, 0, W-1, col)

    # ── Sun (half-submerged at horizon, center x=18) ──────────────────────────
    SX, SY = 13, HORIZON - 1   # 太阳中心
    # 椭圆形太阳：宽6格，高5格（半没入海平线）
    for dy in range(-4, 5):
        for dx in range(-6, 7):
            if (dx*dx)/36.0 + (dy*dy)/16.0 <= 1.0:
                gy = SY + dy
                gx = SX + dx
                if gy < HORIZON:  # 只画海面以上部分
                    inner = (dx*dx)/16.0 + (dy*dy)/9.0 <= 1.0
                    col = SUN_C if inner else SUN_O
                    set_px(canvas, gx, gy, col)

    # 光晕（太阳周围1行）
    for y in range(HORIZON-2, HORIZON):
        for x in range(SX-9, SX+10):
            d = abs(x - SX) / 9.0
            if canvas[y][x] not in [SUN_C, SUN_O]:
                t = max(0, 1.0 - d)
                canvas[y][x] = blend(canvas[y][x], SUN_GLOW, t * 0.45)

    # ── 云海 (y=23–31) ────────────────────────────────────────────────────────
    for y in range(HORIZON, 32):
        t = (y - HORIZON) / 8
        col = blend(SEA_TOP, SEA_DARK, t)
        wrow(canvas, y, 0, W-1, col)

    # 太阳倒影在云海上（橙金光带）
    for y in range(HORIZON, ROCK_TOP):
        rw = max(1, 5 - (y - HORIZON))
        for dx in range(-rw, rw+1):
            rx = SX + dx
            if 0 <= rx < W:
                t2 = (y - HORIZON) / (ROCK_TOP - HORIZON)
                rc = blend(REFL_HI, REFL_MID, t2)
                set_px(canvas, rx, y, rc)
        if (y - HORIZON) % 2 == 1:
            set_px(canvas, SX - rw - 2, y, REFL_MID)
            set_px(canvas, SX + rw + 2, y, REFL_MID)

    # 云海表面波纹（浅色横纹）
    CLOUD_WAVE = (238, 205, 172)
    for y in range(HORIZON+1, ROCK_TOP, 2):
        for x in range(0, W, 4):
            set_px(canvas, x, y, CLOUD_WAVE)
            set_px(canvas, x+1, y, CLOUD_WAVE)

    # ── 远处岛屿/山影改为远处云团 ────────────────────────────────────────────
    CLOUD_FAR = (198, 158, 128)  # 远处云：暖灰
    for y, x1, x2 in [
        (20, 44, 58), (21, 42, 60), (22, 41, 62),
    ]:
        wrow(canvas, y, x1, x2, CLOUD_FAR)
    wrow(canvas, 20, 44, 58, blend(CLOUD_FAR, ROCK_RIM, 0.4))

    # ── 云峰前景（角色坐在上面）────────────────────────────────────────────────
    # 主云峰：圆顶，中央隆起
    for y, x1, x2 in [
        (ROCK_TOP-1, 26, 38),    # 云顶最高处
        (ROCK_TOP,   22, 42),
        (ROCK_TOP+1, 18, 46),
        (ROCK_TOP+2, 14, 50),
        (ROCK_TOP+3, 10, 54),
        (ROCK_TOP+4,  6, 58),
        (ROCK_TOP+5,  0, 63),
        (ROCK_TOP+6,  0, 63),
        (ROCK_TOP+7,  0, 63),
        (ROCK_TOP+8,  0, 63),
    ]:
        wrow(canvas, y, x1, x2, ROCK)

    # 云顶亮面
    for y, x1, x2 in [
        (ROCK_TOP-1, 26, 38),
        (ROCK_TOP,   22, 42),
        (ROCK_TOP+1, 18, 24),
        (ROCK_TOP+1, 40, 46),
    ]:
        wrow(canvas, y, x1, x2, ROCK_RIM)
    # 云中阴影（下方两侧）
    CLOUD_SHADOW = (205, 178, 148)
    for y, x1, x2 in [
        (ROCK_TOP+3, 10, 14),
        (ROCK_TOP+3, 50, 54),
        (ROCK_TOP+4,  6, 12),
        (ROCK_TOP+4, 52, 58),
    ]:
        wrow(canvas, y, x1, x2, CLOUD_SHADOW)

    # 左侧小云峰（往左移）
    for y, x1, x2 in [
        (25, -2, 4), (26, -2, 6), (27, -2, 8), (28, -2, 10),
    ]:
        wrow(canvas, y, max(0,x1), x2, ROCK)
    wrow(canvas, 25, 0, 4, ROCK_RIM)

    # 右侧远云峰
    for y, x1, x2 in [
        (25, 54, 60), (26, 52, 62), (27, 50, 63), (28, 48, 63),
    ]:
        wrow(canvas, y, x1, x2, ROCK)
    wrow(canvas, 25, 54, 60, ROCK_RIM)

    # ── 姜饼人（左，GCX=27）坐姿 ──────────────────────────────────────────────
    GCX = 27
    # 头 y=18–23
    fill(canvas, 18, 23, GCX-3, GCX+3, GB)
    set_px(canvas, GCX-3, 18, blend(SKY_WARM, GB, 0.3))
    set_px(canvas, GCX+3, 18, blend(SKY_WARM, GB, 0.3))
    # 糖霜点
    for dx in [-2, 0, 2]:
        set_px(canvas, GCX+dx, 18, GB_ICING)
    # 眼睛
    set_px(canvas, GCX-2, 20, GBE); set_px(canvas, GCX+2, 20, GBE)
    # 腮红
    set_px(canvas, GCX-3, 21, GB_CHEEK); set_px(canvas, GCX+3, 21, GB_CHEEK)
    # 嘴（微笑）
    set_px(canvas, GCX-1, 22, GBE); set_px(canvas, GCX+1, 22, GBE)
    set_px(canvas, GCX,   23, GBE)
    # 帽子
    set_px(canvas, GCX+1, 16, HAT_DARK)
    for dx in range(-1, 4): set_px(canvas, GCX+dx, 17, HAT_RED)
    for dx in range(-1, 4): set_px(canvas, GCX+dx, 18, HAT_RED)
    set_px(canvas, GCX-1, 17, HAT_DARK); set_px(canvas, GCX+3, 17, HAT_DARK)
    set_px(canvas, GCX-1, 18, HAT_DARK); set_px(canvas, GCX+3, 18, HAT_DARK)
    set_px(canvas, GCX,   17, HAT_LITE)
    # 身体（坐姿，压缩）y=23–26
    fill(canvas, 23, 26, GCX-2, GCX+2, GB)
    # 腿悬空 y=27–29（在礁石下）
    wrow(canvas, 27, GCX-2, GCX-1, GBD)
    wrow(canvas, 28, GCX-2, GCX-1, GBD)
    wrow(canvas, 29, GCX-2, GCX-1, GBD)
    wrow(canvas, 27, GCX+1, GCX+2, GBD)
    wrow(canvas, 28, GCX+1, GCX+2, GBD)
    wrow(canvas, 29, GCX+1, GCX+2, GBD)
    # 手臂搭在礁石上
    set_px(canvas, GCX-3, 25, GB); set_px(canvas, GCX-4, 25, GB)
    set_px(canvas, GCX+3, 25, GB); set_px(canvas, GCX+4, 25, GB)

    # ── 蓝兔子（右，BCX=37）坐姿 ──────────────────────────────────────────────
    BCX = 37
    # 耳朵 y=12–17
    for ey in range(12, 18):
        set_px(canvas, BCX-2, ey, BUN)
        set_px(canvas, BCX-1, ey, BUN_LT)
    for ey in range(12, 18):
        set_px(canvas, BCX+2, ey, BUN)
        set_px(canvas, BCX+1, ey, BUN_LT)
    # 头 y=17–22
    fill(canvas, 17, 22, BCX-3, BCX+3, BUN)
    set_px(canvas, BCX-3, 17, blend(SKY_WARM, BUN, 0.3))
    set_px(canvas, BCX+3, 17, blend(SKY_WARM, BUN, 0.3))
    # 高光
    set_px(canvas, BCX-1, 17, BUN_LT); set_px(canvas, BCX+1, 17, BUN_LT)
    # 眼睛
    set_px(canvas, BCX-2, 19, BUNE); set_px(canvas, BCX+2, 19, BUNE)
    # 腮红
    set_px(canvas, BCX-3, 20, BUN_BLUSH); set_px(canvas, BCX+3, 20, BUN_BLUSH)
    # 嘴
    set_px(canvas, BCX-1, 21, BUNE); set_px(canvas, BCX+1, 21, BUNE)
    set_px(canvas, BCX,   22, BUNE)
    # 身体 y=22–26
    fill(canvas, 22, 26, BCX-2, BCX+2, BUN)
    # 腿悬空 y=27–29
    wrow(canvas, 27, BCX-2, BCX-1, BUND)
    wrow(canvas, 28, BCX-2, BCX-1, BUND)
    wrow(canvas, 29, BCX-2, BCX-1, BUND)
    wrow(canvas, 27, BCX+1, BCX+2, BUND)
    wrow(canvas, 28, BCX+1, BCX+2, BUND)
    wrow(canvas, 29, BCX+1, BCX+2, BUND)
    # 手臂
    set_px(canvas, BCX-3, 25, BUN); set_px(canvas, BCX-4, 25, BUN)
    set_px(canvas, BCX+3, 25, BUN); set_px(canvas, BCX+4, 25, BUN)

    # 两人之间牵手（x=31–33, y=25）
    set_px(canvas, GCX+4, 25, GB)
    set_px(canvas, GCX+5, 25, blend(GB, BUN, 0.5))
    set_px(canvas, BCX-4, 25, BUN)

    # ── 输出 ─────────────────────────────────────────────────────────────────
    img = Image.new('RGB', (W*S, H*S))
    pixels = img.load()
    for y in range(H):
        for x in range(W):
            col = tuple(canvas[y][x])
            for dy in range(S):
                for dx in range(S):
                    pixels[x*S+dx, y*S+dy] = col
    img.save('pixel_sunset.png')
    print(f"Saved: {W*S}×{H*S}px")

draw()
