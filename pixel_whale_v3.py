"""
pixel_whale_v3.py — 观鲸场景（水线分割版）
上半：天空+小船+两人，下半：水下鲸鱼，水线高光
"""
from PIL import Image
import math

W, H = 64, 36
SCALE = 12

# ── 颜色 ──
SKY_TOP  = (178, 210, 235)
SKY_MID  = (212, 232, 245)
SKY_LOW  = (212, 232, 245)

OCEAN_SURF  = (48, 172, 178)
OCEAN_MID1  = (28, 122, 148)
OCEAN_MID2  = (10, 60, 92)
OCEAN_DEEP  = (10, 60, 92)

WHALE_CORE  = (15, 48, 98)
WHALE_MID   = (28, 72, 128)
WHALE_HAZE  = (45, 102, 158)
WHALE_BELLY = (108, 185, 195)
BELLY_STR   = (85, 158, 175)

BOAT_HULL   = (238, 242, 245)
BOAT_DARK   = (155, 175, 200)
BOAT_LIGHT  = (252, 255, 255)
BOAT_INSIDE = (208, 228, 238)
BOAT_SIDE   = (178, 198, 218)

GB_BODY  = (185, 108, 48)
GB_EYE   = (62, 35, 15)
GB_CHEEK = (225, 148, 95)
HAT_RED  = (188, 55, 48)
HAT_DARK = (135, 32, 28)
HAT_LITE = (215, 88, 72)

BUN_BODY  = (95, 158, 215)
BUN_INNER = (210, 168, 190)
BUN_EYE   = (38, 22, 60)
BUN_BLUSH = (235, 155, 172)

# ── 布局 ──
WL       = 18   # 水线 y（画面 15/36 ≈ 42%，接近黄金分割）
BOAT_RIM = 13
FIG_Y    = 23
GB_CX    = 28
BUN_CX   = 36
CX       = 32

def blend(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(c1[i]*(1-t)+c2[i]*t) for i in range(3))

def set_px(canvas, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        canvas[y][x] = color

def wrow(canvas, y, x1, x2, color):
    for x in range(x1, min(x2+1, W)):
        set_px(canvas, x, y, color)

def draw():
    canvas = [[SKY_TOP]*W for _ in range(H)]

    # ── 天空渐变（海龟版）──
    for y in range(WL):
        for x in range(W):
            canvas[y][x] = blend(SKY_TOP, SKY_MID, y/WL)

    # ── 5格海面色（海龟版 SEA_FAR）──
    SEA_FAR = (85, 162, 185)
    for y in range(WL-3, WL):
        t = (y-(WL-3))/3
        col = blend(SEA_FAR, blend(SEA_FAR,(42,105,135),0.5), t)
        for x in range(W):
            canvas[y][x] = col

    # ── 云 ──
    CLOUD  = (210, 230, 242)
    CLOUD_D= (188, 215, 232)
    def draw_cloud(cx, cy, s=1):
        for dx in range(-2*s, 2*s+1): set_px(canvas, cx+dx, cy,   CLOUD)
        for dx in range(-2*s, 2*s+1): set_px(canvas, cx+dx, cy-1, CLOUD)
        for dx in range(-s,   s+1):   set_px(canvas, cx+dx, cy-2, CLOUD)
        for dx in range(-2*s+1, 2*s): set_px(canvas, cx+dx, cy+1, CLOUD_D)
    draw_cloud(10, 10, 3)
    draw_cloud(16, 6, 2)

    # ── 海底渐变（海龟版）──
    SURF_U = (48, 172, 178)
    MID_W  = (28, 122, 148)
    DEEP_W = (10, 60, 92)
    for y in range(WL+2, H):
        t = (y-WL-2)/(H-WL-2)
        col = blend(SURF_U, blend(MID_W, DEEP_W, t), t)
        for x in range(W):
            canvas[y][x] = col

    # ── 水线（海龟版）──
    SURF_LINE = (88, 198, 205)
    wrow(canvas, WL,   0, W-1, SURF_LINE)
    wrow(canvas, WL+1, 0, W-1, (68, 175, 185))
    # 尾柄处 WL+1 恢复鲸鱼色
    set_px(canvas, 53, WL+1, WHALE_CORE)
    set_px(canvas, 54, WL+1, WHALE_CORE)
    set_px(canvas, 55, WL+1, WHALE_CORE)
    # WL行与尾柄交汇的3格用亮色
    for tx in [53, 54, 55]:
        set_px(canvas, tx, WL, (185, 245, 240))
    for rx in [CX-8, CX-3, CX+3, CX+8, CX+14, CX-14]:
        set_px(canvas, rx,   WL, (138, 228, 222))
        set_px(canvas, rx+1, WL, (118, 212, 208))

    # ── 水下光束（2条，略偏左右）──
    for rx in [CX-9, CX+9]:
        for y in range(WL+1, WL+14):
            alpha = max(0, 0.15 - (y-WL)*0.009)
            for dx in [-1,0,1]:
                nx = rx+dx
                if 0<=nx<W:
                    cur = canvas[y][nx]
                    canvas[y][nx] = blend(cur, (138, 222, 218), alpha)

    # ── 座头鲸（上移3格，居中）──
    # 原 y-3：使鲸鱼主体 y=18~28
    def wy(y): return y

    wrow(canvas, wy(21), 10, 52, WHALE_MID)
    wrow(canvas, wy(22),  7, 52, WHALE_CORE)
    wrow(canvas, wy(23),  5, 54, WHALE_CORE)
    wrow(canvas, wy(24),  4, 53, WHALE_CORE)
    wrow(canvas, wy(25),  5, 51, WHALE_CORE)
    wrow(canvas, wy(26),  7, 48, WHALE_MID)
    wrow(canvas, wy(27), 11, 45, WHALE_HAZE)
    wrow(canvas, wy(28), 16, 42, WHALE_HAZE)

    # 腹部
    wrow(canvas, wy(24),  4, 11, WHALE_BELLY)
    wrow(canvas, wy(25),  4, 28, WHALE_BELLY)
    wrow(canvas, wy(26),  6, 30, WHALE_BELLY)
    wrow(canvas, wy(27),  8, 32, WHALE_BELLY)
    wrow(canvas, wy(28), 10, 34, WHALE_BELLY)
    wrow(canvas, wy(29), 12, 36, WHALE_BELLY)
    wrow(canvas, wy(30), 14, 36, WHALE_BELLY)
    wrow(canvas, wy(25), 38, 51, WHALE_BELLY)
    wrow(canvas, wy(26), 39, 48, WHALE_BELLY)
    wrow(canvas, wy(27), 40, 45, WHALE_BELLY)
    wrow(canvas, wy(28), 40, 42, WHALE_BELLY)
    wrow(canvas, wy(29), 40, 39, WHALE_BELLY)
    wrow(canvas, wy(30), 40, 37, WHALE_MID)

    # 腹部条纹
    for x, y in [
        (5,wy(24)),(6,wy(25)),(7,wy(25)),(8,wy(26)),(9,wy(26)),(10,wy(27)),(11,wy(27)),
        (12,wy(28)),(13,wy(28)),(14,wy(28)),(15,wy(28)),(16,wy(28)),(17,wy(28)),(18,wy(28)),
        (19,wy(28)),(20,wy(28)),(21,wy(28)),(22,wy(28)),(23,wy(28)),(24,wy(28)),(25,wy(28)),
        (26,wy(28)),(27,wy(28)),(28,wy(28)),(29,wy(28)),(30,wy(28)),(31,wy(28)),(32,wy(28)),(33,wy(28)),
        (39,wy(26)),(40,wy(26)),(41,wy(26)),(42,wy(26)),(43,wy(26)),(44,wy(26)),(45,wy(26)),
        (46,wy(25)),(47,wy(25)),(48,wy(25)),(49,wy(25)),(50,wy(25)),
    ]:
        set_px(canvas, x, y, BELLY_STR)
    for x, y in [
        (7,wy(24)),(8,wy(24)),(9,wy(25)),(10,wy(25)),(11,wy(26)),(12,wy(26)),(13,wy(27)),
        (14,wy(26)),(15,wy(26)),(16,wy(26)),(17,wy(26)),(18,wy(26)),(19,wy(26)),(20,wy(26)),
        (21,wy(26)),(22,wy(26)),(23,wy(26)),(24,wy(26)),(25,wy(26)),(26,wy(26)),(27,wy(26)),(28,wy(26)),(29,wy(26)),
    ]:
        set_px(canvas, x, y, BELLY_STR)

    set_px(canvas, 17, wy(23), WHALE_BELLY)

    # 胸鳍
    wrow(canvas, wy(25), 28, 37, WHALE_CORE)
    wrow(canvas, wy(26), 30, 38, WHALE_CORE)
    wrow(canvas, wy(27), 32, 39, WHALE_CORE)
    wrow(canvas, wy(28), 34, 39, WHALE_CORE)
    wrow(canvas, wy(29), 36, 39, WHALE_CORE)
    wrow(canvas, wy(30), 38, 39, WHALE_CORE)
    wrow(canvas, wy(31), 39, 39, WHALE_CORE)
    set_px(canvas, 39, wy(32), WHALE_MID)

    # 尾柄（向上穿过水线）
    for y in range(11, 23):
        for x in range(53, 56):
            set_px(canvas, x, y, WHALE_CORE)
    # 尾柄斜坡接身体
    wrow(canvas, wy(22), 49, 52, WHALE_CORE)
    wrow(canvas, wy(21), 51, 52, WHALE_CORE)
    wrow(canvas, wy(20), 52, 53, WHALE_CORE)

    # 水线交界高光（尾巴出水处）
    TAIL_WET = (115, 198, 215)
    # 水线完整切割尾柄，TAIL_WET去掉，wrow已覆盖

    # WL-1 行尾柄：用同行海水色（完全融入背景）
    _y17 = WL-1
    _t17 = (_y17-(WL-3))/3
    _col17 = blend(SEA_FAR, blend(SEA_FAR,(42,105,135),0.5), _t17)
    for x in range(53, 56):
        set_px(canvas, x, _y17, _col17)

    # 尾鳍
    wrow(canvas, 11,  47, 53, WHALE_CORE)
    wrow(canvas, 12, 47, 53, WHALE_CORE)
    wrow(canvas, 13, 48, 53, WHALE_CORE)
    wrow(canvas, 14, 50, 53, WHALE_CORE)
    wrow(canvas, 11,  55, 61, WHALE_CORE)
    wrow(canvas, 12, 55, 61, WHALE_CORE)
    wrow(canvas, 13, 55, 60, WHALE_CORE)
    wrow(canvas, 14, 55, 58, WHALE_CORE)
    # V缺口：用对应y的实际背景色（镂空）
    SEA_FAR_C = (85, 162, 185)
    for _y, _xs in [(11,[53,54,55]),(12,[53,54,55]),(13,[54])]:
        if _y < WL-3:
            _col = blend(SKY_TOP, SKY_MID, _y/WL)
        else:
            _t = (_y-(WL-3))/3
            _col = blend(SEA_FAR_C, blend(SEA_FAR_C,(42,105,135),0.5), _t)
        for _x in _xs:
            set_px(canvas, _x, _y, _col)

    # ── 水线重绘（覆盖鲸鱼尾柄）──
    SURF_LINE = (88, 198, 205)
    wrow(canvas, WL,   0, W-1, SURF_LINE)
    wrow(canvas, WL+1, 0, W-1, (68, 175, 185))
    # 尾柄处 WL+1 恢复鲸鱼色
    set_px(canvas, 53, WL+1, WHALE_CORE)
    set_px(canvas, 54, WL+1, WHALE_CORE)
    set_px(canvas, 55, WL+1, WHALE_CORE)
    # WL行与尾柄交汇的3格用亮色
    for tx in [53, 54, 55]:
        set_px(canvas, tx, WL, (185, 245, 240))
    for rx in [CX-8, CX-3, CX+3, CX+8, CX+14, CX-14]:
        set_px(canvas, rx,   WL, (138, 228, 222))
        set_px(canvas, rx+1, WL, (118, 212, 208))

    # ── 小船 ──
    for x in range(25, 40):
        set_px(canvas, x, WL, blend(OCEAN_SURF, BOAT_DARK, 0.35))
    for y in range(BOAT_RIM+1, WL-1):
        for x in range(25, 40):
            set_px(canvas, x, y, BOAT_INSIDE)
    for y in range(BOAT_RIM, WL-1):
        set_px(canvas, 24, y, BOAT_HULL); set_px(canvas, 23, y, BOAT_SIDE)
        set_px(canvas, 40, y, BOAT_HULL); set_px(canvas, 41, y, BOAT_SIDE)
    # 船底触水行：中心最亮，向两侧渐暗，带水光反射
    # 船底用海水亮色，中心最亮，两侧稍深
    for x in range(24, 42):
        t = abs(x - CX) / 9.0
        col = blend((165, 240, 235), (115, 215, 218), t**0.4)
        set_px(canvas, x, WL, col)
    # 船体水下部分（WL+2，15格居中）
    HULL_SHADOW = (185, 245, 240)
    for x in range(CX-7, CX+8):
        set_px(canvas, x, WL+1, HULL_SHADOW)
    for x in range(23, 42):
        set_px(canvas, x, BOAT_RIM, BOAT_LIGHT)
    set_px(canvas, 22, BOAT_RIM, BOAT_HULL)
    set_px(canvas, 42, BOAT_RIM, BOAT_HULL)
    for x in range(26, 40, 4):
        for y in range(BOAT_RIM+1, WL-1):
            set_px(canvas, x, y, blend(BOAT_INSIDE, BOAT_DARK, 0.2))

    # ── 角色 ──
    def draw_gb(cx, gy):
        for dx in [-1,0,1]:        set_px(canvas, cx+dx, gy-16, GB_BODY)
        for dx in range(-2,3):     set_px(canvas, cx+dx, gy-15, GB_BODY)
        for dx in range(-3,4):
            for oy in [14,13,12,11]: set_px(canvas, cx+dx, gy-oy, GB_BODY)
        for dx in range(-2,3):     set_px(canvas, cx+dx, gy-11, GB_BODY)
        set_px(canvas, cx-2, gy-14, GB_EYE);  set_px(canvas, cx+2, gy-14, GB_EYE)
        set_px(canvas, cx-3, gy-13, GB_CHEEK);set_px(canvas, cx+3, gy-13, GB_CHEEK)
        set_px(canvas, cx,   gy-12, GB_EYE)
        set_px(canvas, cx,   gy-11, (95,52,20))
        set_px(canvas, cx+1, gy-17, HAT_DARK)
        for dx in range(-1,4): set_px(canvas, cx+dx, gy-16, HAT_RED)
        for dx in range(-1,4): set_px(canvas, cx+dx, gy-15, HAT_RED)
        set_px(canvas, cx-1, gy-16, HAT_DARK); set_px(canvas, cx+3, gy-16, HAT_DARK)
        set_px(canvas, cx-1, gy-15, HAT_DARK); set_px(canvas, cx+3, gy-15, HAT_DARK)
        set_px(canvas, cx,   gy-16, HAT_LITE)
        set_px(canvas, cx-4, gy-10, GB_BODY); set_px(canvas, cx-5, gy-10, GB_BODY)
        set_px(canvas, cx+4, gy-10, GB_BODY); set_px(canvas, cx+5, gy-10, GB_BODY)

    def draw_bun(cx, gy):
        for y2 in range(gy-20, gy-15):
            set_px(canvas, cx-1, y2, BUN_BODY); set_px(canvas, cx,   y2, BUN_BODY)
            set_px(canvas, cx+2, y2, BUN_BODY); set_px(canvas, cx+3, y2, BUN_BODY)
        for y2 in range(gy-19, gy-17):
            set_px(canvas, cx, y2, BUN_INNER); set_px(canvas, cx+2, y2, BUN_INNER)
        for dx in [-1,0,1]:        set_px(canvas, cx+dx, gy-16, BUN_BODY)
        for dx in range(-2,3):     set_px(canvas, cx+dx, gy-15, BUN_BODY)
        for dx in range(-3,4):
            for oy in [14,13,12,11]: set_px(canvas, cx+dx, gy-oy, BUN_BODY)
        for dx in range(-2,3):     set_px(canvas, cx+dx, gy-11, BUN_BODY)
        set_px(canvas, cx-2, gy-14, BUN_EYE);  set_px(canvas, cx+2, gy-14, BUN_EYE)
        set_px(canvas, cx-3, gy-13, BUN_BLUSH);set_px(canvas, cx+3, gy-13, BUN_BLUSH)
        set_px(canvas, cx,   gy-13, BUN_INNER)
        set_px(canvas, cx,   gy-12, BUN_EYE)
        set_px(canvas, cx,   gy-11, (38,45,88))
        set_px(canvas, cx-4, gy-10, BUN_BODY); set_px(canvas, cx-5, gy-10, BUN_BODY)
        set_px(canvas, cx+4, gy-10, BUN_BODY); set_px(canvas, cx+5, gy-10, BUN_BODY)

    draw_gb(GB_CX, FIG_Y)
    draw_bun(BUN_CX, FIG_Y)


    # ── 海底杂质（避开鲸鱼区域，颜色偏暗）──
    import random as _rnd
    _rnd.seed(42)
    DEBRIS_COLORS = [
        (55, 145, 158), (65, 155, 168), (45, 132, 148),
        (72, 162, 175), (50, 138, 155), (60, 150, 162),
    ]
    for _ in range(55):
        _dx = _rnd.randint(1, W-2)
        _dy = _rnd.randint(WL+4, H-2)
        # 避开鲸鱼主体区域 x:1~56, y:19~33
        if 1 <= _dx <= 56 and 19 <= _dy <= 33:
            continue
        set_px(canvas, _dx, _dy, _rnd.choice(DEBRIS_COLORS))

    # 左下角补几颗
    for _dx, _dy in [(3,30),(6,32),(2,32),(5,28),(4,25)]:
        set_px(canvas, _dx, _dy, (60, 150, 162))

    return canvas

def render(canvas, output="pixel_whale_v3.png"):
    img = Image.new("RGB", (W*SCALE, H*SCALE))
    px  = img.load()
    for y in range(H):
        for x in range(W):
            c = canvas[y][x]
            for sy in range(SCALE):
                for sx in range(SCALE):
                    px[x*SCALE+sx, y*SCALE+sy] = c
    img.save(output)
    print(f"Saved: {output}")

if __name__ == "__main__":
    canvas = draw()
    render(canvas)
