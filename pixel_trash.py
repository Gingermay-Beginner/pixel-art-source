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

SKY    = (185, 215, 238)
SKY_B  = (155, 192, 220)
GROUND = (148, 170, 112)
SIDE   = (198, 192, 178)
ROAD   = (158, 152, 140)
WALL   = (238, 232, 215)
WALL_D = (208, 200, 182)
WALL_S = (252, 248, 235)
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
BUSH   = ( 95, 148,  72)
BUSH_D = ( 68, 112,  48)
BUSH_L = (132, 182,  98)
FLOWER = (248, 248, 242)
JAC    = (148, 108, 188)
JAC_L  = (185, 148, 222)
JAC_T  = (112,  78,  52)

GB       = (185, 108,  48)
GBD      = (140,  82,  35)
GB_EYE   = ( 62,  35,  15)
GB_CHEEK = (225, 148,  95)
HAT_RED  = (188,  55,  48)
HAT_DARK = (135,  32,  28)
HAT_LITE = (215,  88,  72)

BUN    = ( 95, 158, 215)
BUN_D  = ( 68, 118, 178)
BUN_IN = (235, 148, 178)
BUN_EYE= ( 22,  48, 108)
BUN_LT = (148, 198, 245)
BUN_BL = (235, 155, 172)

BIN_BLK= ( 52,  52,  55)
BIN_BKD= ( 32,  32,  35)
BIN_LID= ( 78,  78,  82)
BIN_BLU= ( 55,  98, 175)
BIN_BLD= ( 35,  68, 138)
BIN_LB = ( 72, 115, 195)
BIN_WHL= ( 88,  85,  80)

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
ROOF_B  = (115,  75,  48)
ROOF_BL = (145,  98,  65)
DOOR_B  = ( 88,  52,  35)
DOOR_BD = ( 62,  35,  22)
WIN_B   = (148, 172, 195)
WIN_BD  = (195, 200, 192)
WIN_BF  = (172, 192, 212)
BRICK   = (188, 105,  72)
BRICK_D = (155,  78,  48)
BEAM    = (142, 105,  68)
GAR     = (218, 212, 198)
GAR_D   = (178, 170, 155)
GAR_S   = (148, 138, 122)
GAR_WIN = ( 62,  88, 112)
AWN_W   = (252, 250, 242)
AWN_S   = (225, 218, 205)
AWN_E   = (225, 218, 205)
WR_GD   = ( 48,  88,  42)
WR_GL   = ( 98, 148,  85)
WR_R    = (212,  62,  52)
WR_BOW  = (212,  48,  48)

fl(11, 27, HX1, HX2, WALL_B)
wcol(HX1, 11, 27, WALL_BD); wcol(HX2, 11, 27, WALL_BD)
# 屋顶（无竖杠）
for y in range(3, 11):
    t = (y - 3) / 7
    x1 = round(HC - t * (HC - (HX1-2)))
    x2 = round(HC + t * ((HX2+2) - HC))
    for x in range(x1, x2+1):
        sp(x, y, ROOF_BL if x <= HC else ROOF_B)
wrow(11, HX1-2, HX2+2, BEAM)
# 烟囱（右移11格：x=46~48）
fl(4, 10, 46, 48, BRICK); wrow(3, 46, 48, BRICK_D); wrow(10, 46, 48, WALL_BL)
# 门（纯实木，双圆角，x=29~35，y=17~27）
fl(17, 27, 29, 35, DOOR_B)
wcol(29, 17, 27, DOOR_BD); wcol(35, 17, 27, DOOR_BD)
wrow(17, 29, 35, DOOR_BD); wrow(27, 29, 35, DOOR_BD)
sp(29, 17, WALL_B); sp(30, 17, DOOR_BD)
sp(35, 17, WALL_B); sp(34, 17, DOOR_BD)
wrow(28, 28, 36, BEAM); wrow(27, 29, 35, BEAM)
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
        for _y in range(14, 17): sp(_x, _y, _c)
    wrow(16, _wx1, _wx2, AWN_E); wrow(13, _wx1, _wx2, AWN_E)
# 车库门（x=16~25，y=21~28）
fl(21, 27, 16, 25, GAR)
wcol(16, 21, 27, GAR_D); wcol(25, 21, 27, GAR_D)
wrow(21, 16, 25, GAR_D); wrow(27, 16, 25, GAR_D)
for _gy in [22, 23, 25]: wrow(_gy, 17, 24, GAR_D)
wcol(19, 21, 27, GAR_D); wcol(22, 21, 27, GAR_D)
for _wx in [17, 18, 20, 21, 23, 24]: sp(_wx, 22, GAR_WIN)

# ── 灌木（全宽，门前断开）──
rng = random.Random(7)
for bx in list(range(0, 12)) + list(range(39, 63)):
    top = 23 - (1 if rng.random() > 0.5 else 0)
    for by in range(top, 28):
        r2 = rng.random()
        sp(bx, by, BUSH_L if r2 > 0.72 else (BUSH_D if r2 < 0.22 else BUSH))
for fx, fy in [(3,23),(7,22),(11,23),(41,23),(44,22),(48,23),(52,22),(56,23),(60,22)]:
    sp(fx, fy, FLOWER); sp(fx, fy+1, (232,212,108))


# ── 左组：黑桶 + 姜饼人 ──
# 黑桶（x=2~6，y=25~33）
fl(25, 33, 2, 6, BIN_BLK)
wrow(24, 2, 6, BIN_LID)
wcol(2, 25, 33, BIN_BKD); wcol(6, 25, 33, BIN_BKD)
wrow(33, 2, 6, BIN_BKD); wrow(29, 3, 5, BIN_BKD)
sp(3, 34, BIN_WHL); sp(5, 34, BIN_WHL)

# 姜饼人（GX=12，匹克球原版坐标搬来，y不变）
GX, GY = 12, 30
# 头（圆润版：上下收角）
for y in range(19, 23): wrow(y, GX-3, GX+3, GB)
wrow(18, GX-2, GX+2, GB)
wrow(23, GX-2, GX+2, GB)
sp(GX-1, 20, GB_EYE); sp(GX+1, 20, GB_EYE)
sp(GX-2, 21, GB_CHEEK); sp(GX+2, 21, GB_CHEEK)
sp(GX-2, 19, GB_EYE); sp(GX+2, 19, GB_EYE)
sp(GX-1, 19, GB_EYE); sp(GX+1, 19, GB_EYE)
sp(GX-1, 22, GB_CHEEK); sp(GX, 22, GB_CHEEK); sp(GX+1, 22, GB_CHEEK)
# 身体
for y in range(24, 28): wrow(y, GX-2, GX+2, GB)
sp(GX, 24, GB_CHEEK); sp(GX, 26, GB_CHEEK)
# 左臂（推桶，向左下伸）
sp(GX-3, 24, GB); sp(GX-4, 25, GB); sp(GX-5, 26, GB)
wrow(26, 6, GX-5, BIN_BKD)  # 手碰桶边线
# 右臂（平衡）
sp(GX+3, 24, GB); sp(GX+4, 25, GB)
# 腿
wcol(GX-3, 27, GY-1, GB); wcol(GX-2, 27, GY-1, GB)
wcol(GX+2, 27, GY-1, GB); wcol(GX+3, 27, GY-1, GB)
sp(GX-4, GY-1, GB); sp(GX+4, GY-1, GB)
# 帽子
for dx in range(-1, 4): sp(GX+dx, 17, HAT_RED)
for dx in range(-1, 4): sp(GX+dx, 18, HAT_RED)
sp(GX-1, 17, HAT_DARK); sp(GX+3, 17, HAT_DARK)
sp(GX-1, 18, HAT_DARK); sp(GX+3, 18, HAT_DARK)
sp(GX+1, 16, HAT_DARK)  # 啾啾
sp(GX, 17, HAT_LITE)

# ── 右组：蓝桶 + 蓝兔子 ──
# 蓝桶（x=49~53，y=25~33）
fl(25, 33, 49, 53, BIN_BLU)
wrow(24, 49, 53, BIN_LB)
wcol(49, 25, 33, BIN_BLD); wcol(53, 25, 33, BIN_BLD)
wrow(33, 49, 53, BIN_BLD); wrow(29, 50, 52, BIN_BLD)
sp(50, 34, BIN_WHL); sp(52, 34, BIN_WHL)

# 蓝兔子（BX=58，匹克球原版坐标搬来，y不变）
BX, BY = 58, 30
# 耳朵
sp(BX-1, 12, BUN); 
for y in range(13,18): wrow(y, BX-2, BX-1, BUN)
sp(BX-2, 14, BUN_IN); sp(BX-2, 15, BUN_IN); sp(BX-2, 16, BUN_IN)
sp(BX+1, 12, BUN)
for y in range(13,18): wrow(y, BX+1, BX+2, BUN)
sp(BX+2, 14, BUN_IN); sp(BX+1, 15, BUN_IN); sp(BX+2, 16, BUN_IN)
# 头
for y in range(19, 23): wrow(y, BX-3, BX+3, BUN)
wrow(18, BX-2, BX+2, BUN)
wrow(23, BX-2, BX+2, BUN)
for y in range(19, 23): wrow(y, BX-1, BX+1, BUN_LT)
# 连心眉
sp(BX-2,19,BUN_EYE);sp(BX-1,19,BUN_EYE);sp(BX,19,(118,158,215));sp(BX+1,19,BUN_EYE);sp(BX+2,19,BUN_EYE)
sp(BX-1, 20, BUN_D); sp(BX+1, 20, BUN_D)
sp(BX-2, 21, BUN_BL); sp(BX+2, 21, BUN_BL)
sp(BX-1, 22, BUN_IN); sp(BX, 22, BUN_IN); sp(BX+1, 22, BUN_IN)
# 身体
for y in range(24, 28): wrow(y, BX-2, BX+2, BUN)
wcol(BX, 24, 26, BUN_LT)
# 左臂（推桶）
sp(BX-3, 24, BUN); sp(BX-4, 25, BUN); sp(BX-5, 26, BUN)
wrow(26, 53, BX-5, BIN_BLD)
# 右臂（平衡）
sp(BX+3, 24, BUN); sp(BX+4, 25, BUN)
# 腿
wcol(BX-3, 27, BY-1, BUN); wcol(BX-2, 27, BY-1, BUN)
wcol(BX+2, 27, BY-1, BUN); wcol(BX+3, 27, BY-1, BUN)
sp(BX-4, BY-1, BUN); sp(BX+4, BY-1, BUN)


img.save("/home/azureuser/.openclaw/workspace/pixel_trash.png")
print("Saved")
