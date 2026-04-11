"""
pixel_whale.py — 观鲸场景
姜饼人+蓝兔子坐小船，座头鲸从船底横向穿过
画面分层：夜空 / 海面+小船 / 深海鲸影
"""

from PIL import Image
import math

W, H = 64, 36
SCALE = 12

# ─── 天空（动森风，暖蓝偏青）───
SKY_TOP  = ( 88, 168, 225)   # 略深的天蓝
SKY_MID  = (120, 195, 235)
SKY_LOW  = (158, 218, 242)
HORIZON  = (195, 232, 248)

# ─── 太阳 & 云（颜色在 draw() 内定义）───
# ─── 海洋（动森风，青绿透亮）───
OCEAN_SURF  = ( 48, 168, 178)   # 偏青绿
OCEAN_MID1  = ( 28, 130, 158)
OCEAN_MID2  = ( 15,  98, 138)
OCEAN_DEEP  = (  8,  65, 115)

# ─── 鲸鱼影 ───
WHALE_CORE  = ( 15,  48,  98)
WHALE_MID   = ( 28,  72, 128)
WHALE_HAZE  = ( 45, 102, 158)
WHALE_BELLY = (125, 178, 208)   # 稍暖的腹部
BELLY_STR   = (100, 152, 188)   # 腹部条纹（略深）
# ─── 小船（动森白船，略带暖白）───
BOAT_HULL   = (238, 242, 245)
BOAT_DARK   = (155, 175, 200)   # 船轮廓
BOAT_LIGHT  = (252, 255, 255)
BOAT_INSIDE = (208, 228, 238)

# ─── 姜饼人 ───
GB_BODY  = (185, 108,  48)
GB_ICING = (245, 232, 210)
GB_EYE   = ( 62,  35,  15)
GB_CHEEK = (225, 148,  95)

# ─── 蓝兔子 ───
BUN_BODY  = ( 95, 158, 215)
BUN_LT    = (175, 218, 248)   # 备用（未用于当前高光）
BUN_INNER = (210, 168, 190)
BUN_EYE   = ( 38,  22,  60)
BUN_BLUSH = (235, 155, 172)
BUN_SMILE = (242, 235, 220)

# ─── 布局 ───
WATER_LINE = 18   # 下移2格
BOAT_RIM   = 14   # 下移2格
FIG_Y      = 24   # 下移2格
GB_CX      = 28
BUN_CX     = 36

# ─────────────────────────────────────────────
def blend(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(c1[i]*(1-t) + c2[i]*t) for i in range(3))

def set_px(canvas, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        canvas[y][x] = color

def wrow(canvas, y, x1, x2, color):
    for x in range(x1, min(x2+1, W)):
        set_px(canvas, x, y, color)

# ─────────────────────────────────────────────
def draw():
    canvas = [[SKY_TOP]*W for _ in range(H)]

    # ── 天空渐变 ──
    for y in range(WATER_LINE):
        for x in range(W):
            t = y / (WATER_LINE - 1)
            if t < 0.5:
                canvas[y][x] = blend(SKY_TOP, SKY_MID, t * 2)
            else:
                canvas[y][x] = blend(SKY_MID, SKY_LOW, (t - 0.5) * 2)

    # ── 地平线发光（已去掉）──

    # ── 海洋渐变 ──
    for y in range(WATER_LINE, H):
        for x in range(W):
            depth = (y - WATER_LINE) / (H - WATER_LINE)
            if depth < 0.12:
                canvas[y][x] = blend(HORIZON, OCEAN_SURF, depth / 0.12)
            elif depth < 0.35:
                canvas[y][x] = blend(OCEAN_SURF, OCEAN_MID1, (depth-0.12)/0.23)
            elif depth < 0.60:
                canvas[y][x] = blend(OCEAN_MID1, OCEAN_MID2, (depth-0.35)/0.25)
            else:
                canvas[y][x] = blend(OCEAN_MID2, OCEAN_DEEP, (depth-0.60)/0.40)

    # 海面高光线
    for x in range(W):
        noise = (x * 11 + 7) % 7
        if noise == 0:
            set_px(canvas, x, WATER_LINE,   (68, 128, 185))
        elif noise == 1:
            set_px(canvas, x, WATER_LINE+1, (52, 102, 162))

    # ── 水面波纹（避开船区 x=22-42）──
    RIPPLE_HI = (78, 188, 198)
    RIPPLE_LO = (28, 118, 145)
    ripples = [
        # 水面两侧，稀疏几点
        (19, [5, 14, 52, 62], RIPPLE_HI),
        (20, [7, 46, 58],     RIPPLE_LO),
        (21, [11, 49, 59],    RIPPLE_HI),
        # 鲸鱼周边（稀疏）
        (24, [50, 58],   RIPPLE_LO),
        (25, [3, 62],    RIPPLE_LO),
        # 水底深处（更稀）
        (28, [5, 60],    RIPPLE_LO),
        (30, [18, 62],   RIPPLE_LO),
    ]
    for ry, xs, col in ripples:
        for rx in xs:
            if 0 <= rx < W:
                set_px(canvas, rx, ry, col)

    # ── 太阳（已去掉）──

    # ── 云朵（阴天灰蓝云）──
    CLOUD_GREY = (168, 222, 240)   # 接近浅天空色
    CLOUD_DARK = (145, 200, 222)   # 云底稍暗
    def draw_cloud(cx, cy, size=1):
        for dx in range(-2*size, 2*size+1):
            set_px(canvas, cx+dx, cy,   CLOUD_GREY)
            set_px(canvas, cx+dx, cy-1, CLOUD_GREY)   # 加厚一行
        for dx in range(-size, size+1):
            set_px(canvas, cx+dx, cy-2, CLOUD_GREY)
        set_px(canvas, cx, cy-3, CLOUD_GREY)
        for dx in range(-2*size+1, 2*size):
            set_px(canvas, cx+dx, cy+1, CLOUD_DARK)

    draw_cloud(9, 11, 3)
    draw_cloud(15, 7, 2)   # 左侧云右上方，靠近左云

    # ── 座头鲸影（透过深海的恍惚影子）──
    # 身体+头部（去掉最上两行，背部从 y=21 开始）
    wrow(canvas, 21, 10, 52, WHALE_MID)
    wrow(canvas, 22,  7, 53, WHALE_CORE)
    wrow(canvas, 23,  5, 54, WHALE_CORE)
    wrow(canvas, 24,  4, 53, WHALE_CORE)   # 右下角减一格，更圆润
    wrow(canvas, 25,  5, 51, WHALE_CORE)   # 右截到腹部右边 x=51
    wrow(canvas, 26,  7, 48, WHALE_MID)    # 右截到腹部右边 x=48
    wrow(canvas, 27, 11, 45, WHALE_HAZE)   # 右截到腹部右边 x=45
    wrow(canvas, 28, 16, 42, WHALE_HAZE)   # 右截到腹部右边 x=42

    # 腹部左截（右边界紧贴胸鳍左边缘，无缝）
    wrow(canvas, 24,  4, 11, WHALE_BELLY)
    wrow(canvas, 25,  4, 28, WHALE_BELLY)  # 胸鳍左边x=27
    wrow(canvas, 26,  6, 30, WHALE_BELLY)  # 胸鳍左边x=29
    wrow(canvas, 27,  8, 32, WHALE_BELLY)  # 胸鳍左边x=31
    wrow(canvas, 28, 10, 34, WHALE_BELLY)  # 胸鳍左边x=33
    wrow(canvas, 29, 12, 36, WHALE_BELLY)
    wrow(canvas, 30, 14, 36, WHALE_BELLY)
    # wrow(canvas, 31, 16, 38, WHALE_MID)  # 去掉：深色末行
    # 去掉：原来多余的深色末行
    # 腹部右截（左边界跟鳍右边缘走）
    wrow(canvas, 25, 38, 51, WHALE_BELLY)  # 紧贴鳍右边x=36
    wrow(canvas, 26, 39, 48, WHALE_BELLY)  # 紧贴鳍右边x=37
    wrow(canvas, 27, 40, 45, WHALE_BELLY)  # 紧贴鳍右边x=38
    wrow(canvas, 28, 40, 42, WHALE_BELLY)
    wrow(canvas, 29, 40, 39, WHALE_BELLY)
    wrow(canvas, 30, 40, 37, WHALE_MID)
    # wrow(canvas, 31, 40, 35, WHALE_HAZE)  # 去掉最底行
    # 腹部条纹（2条弧线，跟随腹部下边缘弧度，延伸到胸鳍左边缘）
    # 条纹1（延伸到胸鳍左边缘）
    for x, y in [
        (5,24),(6,25),(7,25),(8,26),(9,26),(10,27),(11,27),(12,28),(13,28),
        (14,28),(15,28),(16,28),(17,28),(18,28),(19,28),(20,28),
        (21,28),(22,28),(23,28),(24,28),(25,28),(26,28),(27,28),(28,28),(29,28),(30,28),(31,28),(32,28),(33,28),
        # 鳍右侧一条
        (39,26),(40,26),(41,26),(42,26),(43,26),(44,26),(45,26),(46,25),(47,25),(48,25),(49,25),(50,25),
    ]:
        set_px(canvas, x, y, BELLY_STR)
    # 条纹2（左侧，鳍右侧不画）
    for x, y in [
        (7,24),(8,24),(9,25),(10,25),(11,26),(12,26),(13,27),
        (14,26),(15,26),(16,26),(17,26),(18,26),(19,26),(20,26),
        (21,26),(22,26),(23,26),(24,26),(25,26),(26,26),(27,26),(28,26),(29,26),
    ]:
        set_px(canvas, x, y, BELLY_STR)

    # 眼睛
    set_px(canvas, 17, 23, WHALE_BELLY)

    # 胸鳍（左斜右也微斜，向右伸）
    wrow(canvas, 25, 28, 37, WHALE_CORE)   # 右边缘 x=36
    wrow(canvas, 26, 30, 38, WHALE_CORE)   # 右边缘 x=37
    wrow(canvas, 27, 32, 39, WHALE_CORE)   # 右边缘 x=38
    wrow(canvas, 28, 34, 39, WHALE_CORE)
    wrow(canvas, 29, 36, 39, WHALE_CORE)
    wrow(canvas, 30, 38, 38, WHALE_CORE)   # fin tip
    wrow(canvas, 30, 38, 39, WHALE_CORE)
    wrow(canvas, 31, 39, 39, WHALE_CORE)   # fin tip y=31
    # wrow(canvas, 31, 39, 39, WHALE_CORE)  # 去掉
    set_px(canvas, 39, 32, WHALE_MID)

    # 尾鳍（出水，尾柄 x=52-54）
    TAIL_WET = (78, 118, 168)   # 出水横线反光色
    for y in range(12, 23):
        for x in range(53, 56):
            set_px(canvas, x, y, WHALE_CORE)
    # 水面交界横线（反光）
    for x in range(53, 56):
        set_px(canvas, x, WATER_LINE, TAIL_WET)
    # 尾柄底部向左斜坡，接身体背部
    wrow(canvas, 22, 49, 53, WHALE_CORE)   # 向左4格
    wrow(canvas, 21, 51, 53, WHALE_CORE)   # 向左2格
    wrow(canvas, 20, 52, 53, WHALE_CORE)   # 向左1格（再往上一格）

    # 左叶（外边缘向左展，内边缘向右收向尾柄）
    wrow(canvas, 9, 47, 53, WHALE_CORE)   # 内边x=51，不碰缺口
    wrow(canvas, 10, 47, 53, WHALE_CORE)
    wrow(canvas, 11, 48, 53, WHALE_CORE)   # 收一格
    wrow(canvas, 12, 50, 53, WHALE_CORE)   # 贴尾柄左边

    # 右叶（左移1格）
    wrow(canvas, 9, 55, 61, WHALE_CORE)
    wrow(canvas, 10, 55, 61, WHALE_CORE)
    wrow(canvas, 11, 55, 60, WHALE_CORE)
    wrow(canvas, 12, 55, 58, WHALE_CORE)

    # V缺口：用对应高度天空色（y=9-11 在画面偏上，用SKY_MID）
    wrow(canvas, 9, 53, 55, SKY_MID)
    wrow(canvas, 10, 53, 55, SKY_MID)
    set_px(canvas, 54, 11, SKY_LOW)

    # ── 小船 ──
    # 船底触水线
    for x in range(24, 41):
        set_px(canvas, x, WATER_LINE, blend(OCEAN_SURF, BOAT_DARK, 0.35))

    # 船舱内部
    for y in range(BOAT_RIM+1, WATER_LINE):
        for x in range(25, 40):
            set_px(canvas, x, y, BOAT_INSIDE)

    # ── 角色：只露头+手扒船舷 ──
    def draw_gb(cx, gy):
        # 帽子颜色（降饱和红，与阴天海景和谐）
        HAT_RED  = (188,  55,  48)
        HAT_DARK = (135,  32,  28)
        HAT_LITE = (215,  88,  72)
        # 头（gy-10是船舷，头从gy-11往上露出）
        for dx in [-1,0,1]:           set_px(canvas, cx+dx, gy-16, GB_BODY)
        for dx in [-2,-1,0,1,2]:      set_px(canvas, cx+dx, gy-15, GB_BODY)
        for dx in range(-3,4):        set_px(canvas, cx+dx, gy-14, GB_BODY)
        for dx in range(-3,4):        set_px(canvas, cx+dx, gy-13, GB_BODY)
        for dx in range(-3,4):        set_px(canvas, cx+dx, gy-12, GB_BODY)
        for dx in [-2,-1,0,1,2]:      set_px(canvas, cx+dx, gy-11, GB_BODY)
        # 脸
        set_px(canvas, cx-2, gy-14, GB_EYE);   set_px(canvas, cx+2, gy-14, GB_EYE)
        set_px(canvas, cx-3, gy-13, GB_CHEEK); set_px(canvas, cx+3, gy-13, GB_CHEEK)
        # O型嘴：竖着两格，下格浅一点
        set_px(canvas, cx, gy-12, GB_EYE)
        set_px(canvas, cx, gy-11, (95, 52, 20))
        # 帽子（盖在头顶）
        set_px(canvas, cx+1, gy-17, HAT_DARK)                             # 小啾啾
        for dx in range(-1, 4): set_px(canvas, cx+dx, gy-16, HAT_RED)     # 帽身第1行
        for dx in range(-1, 4): set_px(canvas, cx+dx, gy-15, HAT_RED)     # 帽身第2行
        set_px(canvas, cx-1, gy-16, HAT_DARK); set_px(canvas, cx+3, gy-16, HAT_DARK)
        set_px(canvas, cx-1, gy-15, HAT_DARK); set_px(canvas, cx+3, gy-15, HAT_DARK)
        set_px(canvas, cx,   gy-16, HAT_LITE)                              # 高光
        # 两只手扒在船舷（gy-10）
        set_px(canvas, cx-4, gy-10, GB_BODY);  set_px(canvas, cx-5, gy-10, GB_BODY)
        set_px(canvas, cx+4, gy-10, GB_BODY);  set_px(canvas, cx+5, gy-10, GB_BODY)

    def draw_bun(cx, gy):
        # 耳朵
        for y2 in range(gy-20, gy-15):
            set_px(canvas, cx-1, y2, BUN_BODY); set_px(canvas, cx,   y2, BUN_BODY)
            set_px(canvas, cx+2, y2, BUN_BODY); set_px(canvas, cx+3, y2, BUN_BODY)
        for y2 in range(gy-19, gy-17):
            set_px(canvas, cx, y2, BUN_INNER);  set_px(canvas, cx+2, y2, BUN_INNER)
        # 头
        for dx in [-1,0,1]:           set_px(canvas, cx+dx, gy-16, BUN_BODY)
        for dx in [-2,-1,0,1,2]:      set_px(canvas, cx+dx, gy-15, BUN_BODY)
        for dx in range(-3,4):        set_px(canvas, cx+dx, gy-14, BUN_BODY)
        for dx in range(-3,4):        set_px(canvas, cx+dx, gy-13, BUN_BODY)
        for dx in range(-3,4):        set_px(canvas, cx+dx, gy-12, BUN_BODY)
        for dx in [-2,-1,0,1,2]:      set_px(canvas, cx+dx, gy-11, BUN_BODY)
        # 脸
        set_px(canvas, cx-2, gy-15, BUN_BODY);    set_px(canvas, cx-3, gy-14, BUN_BODY)
        set_px(canvas, cx-2, gy-14, BUN_EYE);   set_px(canvas, cx+2, gy-14, BUN_EYE)
        set_px(canvas, cx-3, gy-13, BUN_BLUSH); set_px(canvas, cx+3, gy-13, BUN_BLUSH)
        set_px(canvas, cx, gy-13, BUN_INNER)
        # O型嘴：竖着两格，下格浅一点
        set_px(canvas, cx, gy-12, BUN_EYE)
        set_px(canvas, cx, gy-11, (38, 45, 88))
        # 两只手扒在船舷（gy-10）
        set_px(canvas, cx-4, gy-10, BUN_BODY);  set_px(canvas, cx-5, gy-10, BUN_BODY)
        set_px(canvas, cx+4, gy-10, BUN_BODY);  set_px(canvas, cx+5, gy-10, BUN_BODY)

    draw_gb(GB_CX, FIG_Y)
    draw_bun(BUN_CX, FIG_Y)

    # ── 船舷盖在角色腿上 ──
    # 左右船帮
    BOAT_SIDE = (178, 198, 218)   # 船帮侧面浅灰
    for y in range(BOAT_RIM, WATER_LINE):
        set_px(canvas, 24, y, BOAT_HULL); set_px(canvas, 23, y, BOAT_SIDE)
        set_px(canvas, 40, y, BOAT_HULL); set_px(canvas, 41, y, BOAT_SIDE)

    # 船底（2像素圆角）—— 中段亮，两侧收暗
    for x in range(26, 39):
        t = abs(x - 32) / 8.0   # 0=中心最亮，1=边缘偏暗
        col = blend(BOAT_HULL, BOAT_DARK, t * 0.6)
        set_px(canvas, x, WATER_LINE, col)
    # 左圆角过渡
    set_px(canvas, 24, WATER_LINE,   BOAT_DARK)
    set_px(canvas, 25, WATER_LINE,   BOAT_DARK)
    set_px(canvas, 23, WATER_LINE-1, BOAT_DARK)
    set_px(canvas, 24, WATER_LINE-1, BOAT_DARK)
    # 右圆角过渡
    set_px(canvas, 39, WATER_LINE,   BOAT_DARK)
    set_px(canvas, 40, WATER_LINE,   BOAT_DARK)
    set_px(canvas, 41, WATER_LINE-1, BOAT_DARK)
    set_px(canvas, 40, WATER_LINE-1, BOAT_DARK)

    # 船舷顶部横梁
    for x in range(23, 42):
        set_px(canvas, x, BOAT_RIM, BOAT_LIGHT)
    set_px(canvas, 22, BOAT_RIM,   BOAT_HULL)
    set_px(canvas, 42, BOAT_RIM,   BOAT_HULL)

    # 木纹
    for x in range(26, 40, 4):
        for y in range(BOAT_RIM+1, WATER_LINE):
            set_px(canvas, x, y, blend(BOAT_INSIDE, BOAT_DARK, 0.2))

    return canvas


def render(canvas, output="pixel_whale.png"):
    img = Image.new("RGB", (W * SCALE, H * SCALE))
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
