from PIL import Image, ImageDraw
import random, math

W, H, S = 64, 36, 12
img = Image.new("RGB", (W*S, H*S), (255,255,255))
draw = ImageDraw.Draw(img)

def sp(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        draw.rectangle([x*S, y*S, x*S+S-1, y*S+S-1], fill=c)
def fl(y1, y2, x1, x2, c):
    for y in range(y1, y2+1):
        for x in range(x1, x2+1): sp(x, y, c)
def wrow(y, x1, x2, c):
    for x in range(x1, x2+1): sp(x, y, c)
def wcol(x, y1, y2, c):
    for y in range(y1, y2+1): sp(x, y, c)

SKY    = (195, 228, 242)
SKY_B  = (172, 210, 232)
GROUND = (155, 185, 98)
SIDE   = (195, 198, 205)
ROAD   = (162, 168, 178)
WALL   = (245, 238, 218)
WALL_D = (218, 208, 188)
WALL_S = (255, 250, 235)
RIDGE  = ( 98,  75,  48)
ROOF_L = (168, 138, 105)
ROOF_R = (122,  95,  65)
ROOF_E = (108,  82,  52)
DOOR   = (175,  78,  58)
DOOR_D = (138,  52,  35)
DOOR_W = (215, 195, 158)
WIN    = (152, 198, 228)
WIN_D  = ( 75, 125, 165)
WIN_F  = ( 98, 158, 198)
WIN_G  = (188, 218, 238)
BUSH   = ( 38,  88,  68)
BUSH_D = ( 22,  58,  45)
BUSH_L = ( 62, 118,  92)
FLOWER = (252, 245, 215)
JAC    = (148, 108, 188)
JAC_L  = (185, 148, 222)
JAC_T  = (112,  78,  52)

GB       = (198, 128,  58)
GBD      = (155,  98,  42)
GB_EYE   = ( 62,  35,  15)
GB_CHEEK = (238, 165, 105)
HAT_RED  = (188,  55,  48)
HAT_DARK = (135,  32,  28)
HAT_LITE = (215,  88,  72)

BUN    = ( 88, 162, 228)
BUN_D  = (  8,  18,  48)
BUN_IN = (235, 148, 178)
BUN_EYE= (  2,   4,  12)
BUN_LT = (158, 212, 252)
BUN_BL = (235, 155, 172)

BIN_BLK= ( 88,  88,  92)
BIN_BKD= ( 62,  62,  68)
BIN_LID= (118, 118, 125)
BIN_BLU= ( 72, 128, 212)
BIN_BLD= ( 48,  95, 175)
BIN_LB = ( 95, 148, 228)
BIN_WHL= ( 65,  58,  52)

# ── 天空 ──
fl(0, 21, 0, 63, SKY)
fl(19, 21, 0, 63, SKY_B)
fl(22, 27, 0, 63, GROUND)
fl(25, 28, 0, 63, SIDE)
fl(29, 35, 0, 63, ROAD)

# ── 房子（更新版）──
HX1, HX2, HC = 12, 52, 32
WALL_B  = (195, 172, 138)
WALL_BD = (158, 135, 102)
WALL_BL = (218, 198, 165)
ROOF_B  = (122, 102,  72)
ROOF_BL = (152, 128,  95)
DOOR_B  = ( 88,  52,  35)
DOOR_BD = ( 62,  35,  22)
WIN_B   = (148, 172, 195)
WIN_BD  = (195, 200, 192)
WIN_BF  = (172, 192, 212)
BRICK   = (188, 105,  72)
BRICK_D = (155,  78,  48)
BEAM    = (102,  82,  52)
GAR     = (228, 222, 208)
GAR_D   = (195, 200, 192)
GAR_S   = (148, 138, 122)
GAR_WIN = (148, 172, 195)
AWN_W   = (252, 250, 242)
AWN_S   = (225, 218, 205)
AWN_E   = (225, 218, 205)
WR_GD   = ( 48,  88,  42)
WR_GL   = ( 98, 148,  85)
WR_R    = (212,  62,  52)
WR_BOW  = (212,  48,  48)

fl(11, 27, HX1, HX2, WALL_B)
wcol(HX1, 11, 27, WALL_BD); wcol(HX2, 11, 27, WALL_BD)
# 屋顶（横向瓦片纹：奇偶行交替深浅，模拟瓦片）
for y in range(3, 11):
    t = (y - 3) / 7
    x1 = round(HC - t * (HC - (HX1-2)))
    x2 = round(HC + t * ((HX2+2) - HC))
    row_c = ROOF_BL if y % 2 == 0 else ROOF_B
    for x in range(x1, x2+1):
        sp(x, y, row_c)
wrow(11, HX1-2, HX2+2, BEAM)
# 烟囱（右移11格：x=46~48）
fl(4, 10, 46, 48, BRICK); wrow(3, 46, 48, BRICK_D); wrow(10, 46, 48, WALL_BL)
# 门（纯实木，双圆角，x=29~35，y=17~27）
fl(17, 27, 29, 35, DOOR_B)
wcol(29, 17, 27, DOOR_BD); wcol(35, 17, 27, DOOR_BD)
wrow(17, 29, 35, DOOR_BD); wrow(27, 29, 35, DOOR_BD)
sp(29, 17, WALL_B); sp(30, 17, DOOR_BD)
sp(35, 17, WALL_B); sp(34, 17, DOOR_BD)
wrow(28, 28, 36, (158, 118, 75)); wrow(27, 29, 35, (158, 118, 75))
wrow(27, 29, 35, (135, 92, 62))  # 门底深色
sp(34, 23, (215, 188, 95))
# 圣诞花环
import math as _math
cx_wr, cy_wr = 32, 20
for _ang in range(0, 360, 20):
    _rad = _math.radians(_ang)
    for _r in [1.5, 2.0]:
        _px = round(cx_wr + _r * _math.cos(_rad))
        _py = round(cy_wr + _r * _math.sin(_rad))
        sp(_px, _py, WR_GL if (_ang // 40) % 2 == 0 else WR_GD)
for _ang in [45, 135, 225, 315]:
    _rad = _math.radians(_ang)
    sp(round(cx_wr + 1.6*_math.cos(_rad)), round(cy_wr + 1.6*_math.sin(_rad)), WR_R)
sp(32, 18, WR_BOW); sp(31, 18, WR_BOW); sp(33, 18, WR_BOW)
# 左窗（x=16~25，三等分）
fl(13, 19, 16, 25, WIN_B)
wcol(16, 13, 19, WIN_BD); wcol(25, 13, 19, WIN_BD)
wrow(13, 16, 25, WIN_BD); wrow(19, 16, 25, WIN_BD)
wcol(19, 13, 19, WIN_BD); wcol(22, 13, 19, WIN_BD)
wrow(16, 16, 25, WIN_BF)
# 右窗（x=39~48，三等分）
fl(13, 19, 39, 48, WIN_B)
wcol(39, 13, 19, WIN_BD); wcol(48, 13, 19, WIN_BD)
wrow(13, 39, 48, WIN_BD); wrow(19, 39, 48, WIN_BD)
wcol(42, 13, 19, WIN_BD); wcol(45, 13, 19, WIN_BD)
wrow(16, 39, 48, WIN_BF)
# 遮雨棚（左 x=16~25，右 x=39~48，y=14~16）
for _wx1, _wx2 in [(16, 25), (39, 48)]:
    for _x in range(_wx1, _wx2+1):
        _c = AWN_W if (_x - _wx1) % 2 == 0 else AWN_S
        for _y in range(13, 17): sp(_x, _y, _c)
    wrow(16, _wx1, _wx2, AWN_E)
# 车库门（x=16~25，y=21~28）
fl(21, 27, 16, 25, GAR)
wcol(16, 21, 27, GAR_D); wcol(25, 21, 27, GAR_D)
wrow(21, 16, 25, GAR_D); wrow(27, 16, 25, GAR_D)
for _gy in [22, 23, 25]: wrow(_gy, 17, 24, GAR_D)
wcol(19, 21, 27, GAR_D); wcol(22, 21, 27, GAR_D)
for _wx in [17, 18, 20, 21, 23, 24]: sp(_wx, 22, GAR_WIN)

# ── 柠檬树（左 cx=5，右 cx=58）──
LM_TRUNK = (142, 105,  68)
LM_LF    = ( 95, 158,  72)
LM_LFD   = ( 68, 122,  52)
LM_LFL   = (128, 192, 102)
LM_FR    = (252, 225,  65)
LM_FRD   = (218, 188,  52)

def draw_lemon_tree(cx, base_y, max_left=None, max_right=None):
    # 树干
    for y in range(base_y - 4, base_y + 1):
        sp(cx, y, LM_TRUNK)
        sp(cx+1, y, LM_TRUNK)
    import random as _rng
    _r = _rng.Random(cx * 17 + 3)
    crown_map = {}
    # 宽树冠：半径9格，高18格，内侧（靠房子）做不规则锯齿而非硬截断
    jagged_r = _rng.Random(cx * 31 + 7)
    for dy in range(0, 18):
        cy = base_y - 5 - dy
        hw = max(2, round(9.0 - abs(dy - 9) * 0.45) if dy < 9 else round(9.0 - abs(dy - 9) * 0.65))
        for dx in range(-hw, hw+1):
            nx = cx + dx
            if max_left is not None and nx < max_left: continue
            if max_right is not None and nx > max_right: continue
            # 内侧（靠房子方向）最外1~2格做锯齿：随机跳过
            if max_right is not None and nx >= max_right - 2:
                if jagged_r.random() < 0.45: continue
            if max_left is not None and nx <= max_left + 2:
                if jagged_r.random() < 0.45: continue
            crown_map[(nx, cy)] = True
    # 不规则边缘凸出（外侧）
    extras = [(cx-7, base_y-8),(cx-7, base_y-11),(cx-6, base_y-6),(cx-6, base_y-14),
              (cx+7, base_y-9),(cx+7, base_y-12),(cx+6, base_y-7),(cx+6, base_y-15),
              (cx-3, base_y-22),(cx, base_y-22),(cx+3, base_y-21),(cx-1, base_y-23),(cx+1, base_y-23)]
    for p in extras:
        nx, cy = p
        if max_left is not None and nx < max_left: continue
        if max_right is not None and nx > max_right: continue
        crown_map[p] = True
    # 填满每行 min~max 之间的空隙
    from collections import defaultdict
    row_xs = defaultdict(list)
    for (nx, cy) in crown_map: row_xs[cy].append(nx)
    for cy, xs in row_xs.items():
        for fx in range(min(xs), max(xs)+1):
            crown_map[(fx, cy)] = True

    for (nx, cy) in crown_map:
        r2 = _r.random()
        c = LM_LFL if r2 > 0.65 else (LM_LFD if r2 < 0.25 else LM_LF)
        sp(nx, cy, c)
    # 柠檬果
    lemons = [(cx-2, base_y-7),(cx+2, base_y-8),(cx-1, base_y-11),(cx+3, base_y-10),
              (cx-3, base_y-14),(cx+1, base_y-5),(cx-5, base_y-10),(cx+5, base_y-13),
              (cx, base_y-17),(cx-4, base_y-7),(cx+4, base_y-8)]
    for (lx, ly) in lemons:
        if (lx, ly) in crown_map:
            sp(lx, ly, LM_FR)
            sp(lx, ly+1, LM_FRD)

# 底层柠檬树（更靠外，先画）
draw_lemon_tree(61, 27, max_left=None, max_right=None)
# 上层柠檬树（靠内，后画，遮住底层）
draw_lemon_tree(6, 27, max_left=None, max_right=None)
draw_lemon_tree(59, 27, max_left=None, max_right=None)
# ── 小私人飞机 ──
PL_BODY = (245, 245, 242); PL_WING = (228, 228, 222); PL_WIN = (148, 195, 225)
# 机身
wrow(3, 15, 19, PL_BODY)
wrow(4, 14, 19, PL_BODY)
# 机头
sp(20, 3, PL_BODY); sp(20, 4, PL_BODY); sp(21, 4, PL_BODY)
# 机尾竖尾翼
sp(14, 2, PL_WING)
# 上翼
wrow(2, 14, 17, PL_WING)
# 下翼
wrow(1, 13, 15, PL_WING)
# 窗
sp(18, 3, PL_WIN); sp(19, 3, PL_WIN)
# 尾气
wrow(4, 12, 13, PL_BODY)
wrow(3, 11, 12, PL_BODY)


# ── 灌木（全宽，门前断开）──
rng = random.Random(7)
for bx in list(range(0, 12)) + list(range(39, 63)):
    top = 23 - (1 if rng.random() > 0.5 else 0)
    for by in range(top, 28):
        r2 = rng.random()
        sp(bx, by, BUSH_L if r2 > 0.72 else (BUSH_D if r2 < 0.22 else BUSH))
for fx, fy in [(0,23),(3,23),(7,22),(11,23),(41,23),(44,22),(48,23),(52,22),(56,23),(60,22),(62,23)]:
    sp(fx, fy, FLOWER); sp(fx, fy+1, (148,198,235))
# x=12 y=23,24,26,27 灌木（被墙体覆盖修补）
sp(12, 23, BUSH); sp(12, 24, BUSH); sp(12, 26, BUSH); sp(12, 27, BUSH)

# x=63 y=22~27 填灌木色（柠檬树边缘修补）
import random as _rng2
_r63 = random.Random(63)
for _y63 in range(22, 28):
    _c63 = BUSH_D if _r63.random() < 0.22 else (BUSH_L if _r63.random() > 0.72 else BUSH)
    sp(63, _y63, _c63)



# ── 左组：黑桶 + 姜饼人 ──
# 黑桶（x=6~10，y=24~32）
fl(24, 32, 6, 10, BIN_BLK)
wrow(23, 6, 10, BIN_LID)
wcol(6, 24, 32, BIN_BKD); wcol(10, 24, 32, BIN_BKD)
wrow(32, 6, 10, BIN_BKD); wrow(28, 7, 9, BIN_BKD)
sp(9, 31, BIN_WHL); sp(10, 31, BIN_WHL); sp(9, 32, BIN_WHL); sp(10, 32, (115,105,95))

# 姜饼人（GX=12，匹克球原版坐标搬来，y不变）
GX, GY = 16, 33
# 头（圆润版：上下收角）
for y in range(22, 26): wrow(y, GX-3, GX+3, GB)
wrow(21, GX-2, GX+2, GB)
wrow(26, GX-2, GX+2, GB)
sp(GX-1, 23, GB_EYE); sp(GX+1, 23, GB_EYE)
sp(GX-2, 24, GB_CHEEK); sp(GX+2, 24, GB_CHEEK)

sp(GX-1, 25, (165,100,38)); sp(GX, 25, (165,100,38)); sp(GX+1, 25, (165,100,38))
# 身体
for y in range(27, 31): wrow(y, GX-2, GX+2, GB)
sp(GX, 27, GB_CHEEK); sp(GX, 29, GB_CHEEK)
# 左臂（推桶，向左下伸）
sp(GX-3, 24, GB); sp(GX-4, 25, GB); sp(GX-5, 26, GB)
wrow(26, 10, GX-5, BIN_BKD)
sp(GX-5, 25, GB)  # 手碰桶边线
# 右臂（平衡）
sp(GX+3, 27, GB); sp(GX+4, 28, GB)
# 腿
wcol(GX-3, 30, GY-1, GB); wcol(GX-2, 30, GY-1, GB)
wcol(GX+2, 30, GY-1, GB); wcol(GX+3, 30, GY-1, GB)
sp(GX-4, GY-1, GB); sp(GX+4, GY-1, GB)
# 帽子
for dx in range(-1, 4): sp(GX+dx, 20, HAT_RED)
for dx in range(-1, 4): sp(GX+dx, 21, HAT_RED)
sp(GX-1, 20, HAT_DARK); sp(GX+3, 20, HAT_DARK)
sp(GX-1, 21, HAT_DARK); sp(GX+3, 21, HAT_DARK)
sp(GX+1, 19, HAT_DARK)  # 啾啾
sp(GX, 20, HAT_LITE)

# ── 右组：蓝桶 + 蓝兔子 ──
# 蓝桶（x=45~49，y=24~32）
fl(24, 32, 44, 48, BIN_BLU)
wrow(23, 44, 48, BIN_LB)
wcol(44, 24, 32, BIN_BLD); wcol(48, 24, 32, BIN_BLD)
wrow(32, 44, 48, BIN_BLD); wrow(28, 45, 47, BIN_BLD)
sp(47, 31, BIN_WHL); sp(48, 31, BIN_WHL); sp(47, 32, BIN_WHL); sp(48, 32, (115,105,95))

# 蓝兔子（BX=58，匹克球原版坐标搬来，y不变）
BX, BY = 54, 33
# 耳朵
# 左耳：y=18顶行只画内列（外列不画=圆角），y=19~20双列
sp(BX-1, 18, BUN)
for y in range(19,21): wrow(y, BX-2, BX-1, BUN)
sp(BX-1, 19, BUN_IN); sp(BX-1, 20, BUN_IN)
# 右耳：y=18顶行只画内列
sp(BX+1, 18, BUN)
for y in range(19,21): wrow(y, BX+1, BX+2, BUN)
sp(BX+1, 19, BUN_IN); sp(BX+1, 20, BUN_IN)
# 头
for y in range(22, 26): wrow(y, BX-3, BX+3, BUN)
wrow(21, BX-2, BX+2, BUN)
wrow(26, BX-2, BX+2, BUN)
for y in range(22, 26): wrow(y, BX-1, BX+1, BUN)
# 连心眉
sp(BX-2,22,BUN_EYE);sp(BX-1,22,BUN_EYE);sp(BX,22,(62,128,188));sp(BX+1,22,BUN_EYE);sp(BX+2,22,BUN_EYE)
sp(BX-1, 23, BUN_D); sp(BX+1, 23, BUN_D)
sp(BX-2, 24, BUN_BL); sp(BX+2, 24, BUN_BL)
sp(BX-1, 25, (245,245,242)); sp(BX, 25, (245,245,242)); sp(BX+1, 25, (245,245,242))
# 身体
for y in range(27, 31): wrow(y, BX-2, BX+2, BUN)
wcol(BX, 27, 29, BUN_LT)
# 左臂（推桶）
sp(BX-3, 24, BUN); sp(BX-4, 25, BUN); sp(BX-5, 26, BUN)
wrow(26, 48, BX-5, BIN_BLD)
sp(BX-5, 25, BUN)
# 右臂（平衡）
sp(BX+3, 27, BUN); sp(BX+4, 28, BUN)
# 腿
wcol(BX-3, 30, BY-1, BUN); wcol(BX-2, 30, BY-1, BUN)
wcol(BX+2, 30, BY-1, BUN); wcol(BX+3, 30, BY-1, BUN)
sp(BX-4, BY-1, BUN); sp(BX+4, BY-1, BUN)


img.save("/home/azureuser/.openclaw/workspace/pixel_trash.png")
print("Saved")
