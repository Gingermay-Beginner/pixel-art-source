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
SKY_TOP  = (58, 42, 105)
SKY_MID  = (148, 65, 108)
SKY_WARM = (218, 98, 68)
SKY_HOR  = (245, 178, 72)
SUN_C    = (255, 242, 118)
SUN_O    = (248, 195, 65)
SUN_GLOW = (238, 138, 48)

SEA_NEAR = (68, 88, 148)
SEA_MID  = (108, 138, 188)
REFL_HI  = (248, 195, 85)
REFL_MID = (205, 128, 58)

CLIFF    = (38, 32, 48)
CLIFF_LT = (62, 52, 72)

# 堤坝/栈桥颜色
PIER     = (82, 72, 62)     # 石头堤坝
PIER_LT  = (118, 105, 88)   # 顶面亮色
PIER_DK  = (55, 48, 40)     # 侧面暗色

GB       = (188, 112, 50)
GBD      = (145, 80, 32)
GBE      = (62, 35, 15)
GB_ICING = (245, 232, 210)
GB_CHEEK = (228, 152, 98)
HAT_RED  = (198, 42, 32)
HAT_DARK = (140, 26, 20)
HAT_LITE = (225, 72, 55)

BUN      = (98, 162, 218)
BUND     = (68, 112, 182)
BUNE     = (38, 22, 60)
BUN_LT   = (148, 198, 242)
BUN_BLUSH= (238, 158, 175)

CAM      = (42, 38, 52)
CAM_LT   = (72, 68, 82)
CAM_LENS = (168, 195, 215)

def draw():
    HORIZON = 20
    canvas = [[SKY_TOP]*W for _ in range(H)]

    # ── Sky gradient ─────────────────────────────────────────────────────────
    for y in range(HORIZON):
        t = y / (HORIZON - 1)
        if t < 0.35:
            col = blend(SKY_TOP, SKY_MID, t / 0.35)
        elif t < 0.65:
            col = blend(SKY_MID, SKY_WARM, (t - 0.35) / 0.30)
        else:
            col = blend(SKY_WARM, SKY_HOR, (t - 0.65) / 0.35)
        wrow(canvas, y, 0, W-1, col)

    # ── Sun（居中，x=32）────────────────────────────────────────────────────
    SX, SY = 32, HORIZON - 1
    for dy in range(-4, 5):
        for dx in range(-5, 6):
            if (dx*dx)/25.0 + (dy*dy)/16.0 <= 1.0:
                gy = SY + dy
                gx = SX + dx
                if 0 <= gx < W and gy < HORIZON:
                    inner = (dx*dx)/12.0 + (dy*dy)/9.0 <= 1.0
                    set_px(canvas, gx, gy, SUN_C if inner else SUN_O)
    # 光晕
    for y in range(HORIZON-3, HORIZON):
        for x in range(SX-10, SX+11):
            d = abs(x - SX) / 10.0
            if canvas[y][x] not in [SUN_C, SUN_O]:
                t = max(0, 1.0 - d)
                canvas[y][x] = blend(canvas[y][x], SUN_GLOW, t * 0.5)

    # ── 晚霞云彩 ─────────────────────────────────────────────────────────────
    CLOUD_C = (248, 188, 130)  # 淡橙
    # 中部淡云条（y=7–9，太阳上方）
    for x in range(22, 38):  set_px(canvas, x, 7, CLOUD_C)
    for x in range(18, 32):  set_px(canvas, x, 9, CLOUD_C)

    # ── 海面（y=20–35，右侧全海水）──────────────────────────────────────────
    for y in range(HORIZON, H):
        t = min((y - HORIZON) / 10, 1.0)
        wrow(canvas, y, 0, W-1, blend(SEA_MID, SEA_NEAR, t))
    # 太阳倒影（靠近堤坝处隔行被海水横穿）
    BREAK_ROWS = {24, 26, 28, 30}  # 横穿行（海水穿越倒影）
    for y in range(HORIZON, 31):
        rw = max(1, 5 - (y - HORIZON))
        rc = blend(REFL_HI, REFL_MID, (y-HORIZON)/9)
        if y in BREAK_ROWS:
            pass  # 海水横穿，跳过倒影
        else:
            for dx in range(-rw, rw+1):
                set_px(canvas, SX+dx, y, rc)
            if (y - HORIZON) % 2 == 1:
                set_px(canvas, SX-rw-2, y, REFL_MID)
                set_px(canvas, SX+rw+2, y, REFL_MID)
    # 海面波光
    for yi, y in enumerate([21, 23, 25, 27]):
        offset = yi * 2
        for x in range(offset, W, 5):
            if canvas[y][x] not in [REFL_HI, REFL_MID]:
                set_px(canvas, x, y, SEA_MID)

    # ── 陆地/悬崖（左侧，y=31–35，x=0–14）──────────────────────────────────
    for y in range(31, H):
        wrow(canvas, y, 0, 14, CLIFF)
    wrow(canvas, 31, 0, 14, CLIFF_LT)

    # ── 堤坝（顶面 y=29–30，末端 x=52）────────────────────────────────────
    PIER_Y1 = 29
    PIER_X2 = 52
    wrow(canvas, PIER_Y1,   0, PIER_X2, PIER_LT)
    wrow(canvas, PIER_Y1+1, 0, PIER_X2, PIER)
    for y in range(31, H):
        wrow(canvas, y, 0, PIER_X2, PIER_DK)
    # 堤坝侧面材质：横向石缝
    PIER_CRACK = (38, 32, 28)   # 深缝
    PIER_HI    = (82, 70, 58)   # 高光点
    for y in [32, 34]:
        for x in range(2, PIER_X2, 8):
            set_px(canvas, x, y, PIER_CRACK)
            set_px(canvas, x+1, y, PIER_CRACK)
    # 竖向分隔缝（石块间距）
    for x in range(6, PIER_X2, 10):
        for y in range(31, H):
            if (x + y) % 2 == 0:
                set_px(canvas, x, y, PIER_CRACK)
    # 偶发高光点（模拟湿石反光）
    for x in range(4, PIER_X2, 13):
        set_px(canvas, x, 33, PIER_HI)
        set_px(canvas, x+5, 35, PIER_HI)

    # ── 姜饼人（GCX=40，堤坝末端）──────────────────────────────────────────
    GCX = 48
    set_px(canvas, GCX+1, 17, HAT_DARK)
    for dx in range(-1, 4): set_px(canvas, GCX+dx, 18, HAT_RED)
    for dx in range(-1, 4): set_px(canvas, GCX+dx, 19, HAT_RED)
    set_px(canvas, GCX-1, 18, HAT_DARK); set_px(canvas, GCX+3, 18, HAT_DARK)
    set_px(canvas, GCX-1, 19, HAT_DARK); set_px(canvas, GCX+3, 19, HAT_DARK)
    set_px(canvas, GCX,   18, HAT_LITE)
    fill(canvas, 19, 24, GCX-3, GCX+3, GB)
    set_px(canvas, GCX-3, 19, blend(SKY_WARM, GB, 0.3))
    set_px(canvas, GCX+3, 19, blend(SKY_WARM, GB, 0.3))
    set_px(canvas, GCX-2, 21, GBE); set_px(canvas, GCX+2, 21, GBE)
    set_px(canvas, GCX-3, 22, GB_CHEEK); set_px(canvas, GCX+3, 22, GB_CHEEK)
    set_px(canvas, GCX-1, 23, GBE); set_px(canvas, GCX, 23, GBE); set_px(canvas, GCX+1, 23, GBE)
    fill(canvas, 24, 28, GCX-2, GCX+2, GB)
    set_px(canvas, GCX, 25, GB_ICING)
    wrow(canvas, 29, GCX-2, GCX-1, GBD); wrow(canvas, 29, GCX+1, GCX+2, GBD)
    set_px(canvas, GCX-3, 26, GB); set_px(canvas, GCX-4, 26, GB)
    set_px(canvas, GCX+3, 26, GB); set_px(canvas, GCX+4, 26, GB)

    # ── 蓝兔子（BCX=14，堤坝左端，面右，举相机）────────────────────────────
    BCX = 14
    for ey in range(14, 20):
        set_px(canvas, BCX-2, ey, BUN); set_px(canvas, BCX-1, ey, BUN_LT)
        set_px(canvas, BCX+2, ey, BUN); set_px(canvas, BCX+1, ey, BUN_LT)
    fill(canvas, 19, 24, BCX-3, BCX+3, BUN)
    set_px(canvas, BCX-3, 19, blend(SKY_WARM, BUN, 0.3))
    set_px(canvas, BCX+3, 19, blend(SKY_WARM, BUN, 0.3))
    set_px(canvas, BCX-1, 19, BUN_LT); set_px(canvas, BCX+1, 19, BUN_LT)
    set_px(canvas, BCX+1, 21, BUNE); set_px(canvas, BCX+2, 21, BUNE)
    set_px(canvas, BCX-2, 22, BUN_BLUSH); set_px(canvas, BCX+3, 22, BUN_BLUSH)
    BUN_SMILE = (242, 235, 220)
    set_px(canvas, BCX, 23, BUN_SMILE); set_px(canvas, BCX+1, 23, BUN_SMILE); set_px(canvas, BCX+2, 23, BUN_SMILE)
    fill(canvas, 24, 26, BCX-2, BCX+2, BUN)
    wrow(canvas, 27, BCX-2, BCX-1, BUND); wrow(canvas, 27, BCX+1, BCX+2, BUND)
    wrow(canvas, 28, BCX-2, BCX-1, BUND); wrow(canvas, 28, BCX+1, BCX+2, BUND)
    # 右手臂举相机
    set_px(canvas, BCX+3, 25, BUN); set_px(canvas, BCX+4, 25, BUN); set_px(canvas, BCX+5, 25, BUN)
    # 左手臂
    set_px(canvas, BCX-3, 25, BUN); set_px(canvas, BCX-3, 26, BUN)
    # 相机
    fill(canvas, 24, 26, BCX+6, BCX+8, CAM)
    wrow(canvas, 24, BCX+6, BCX+8, CAM_LT)
    set_px(canvas, BCX+8, 25, CAM_LENS)
    set_px(canvas, BCX+7, 23, CAM); set_px(canvas, BCX+8, 23, CAM)

    # ── 输出 ─────────────────────────────────────────────────────────────────
    img = Image.new('RGB', (W*S, H*S))
    pixels = img.load()
    for y in range(H):
        for x in range(W):
            col = tuple(canvas[y][x])
            for dy in range(S):
                for dx in range(S):
                    pixels[x*S+dx, y*S+dy] = col
    img.save('pixel_beach_sunset.png')
    print(f"Saved: {W*S}×{H*S}px")

draw()
