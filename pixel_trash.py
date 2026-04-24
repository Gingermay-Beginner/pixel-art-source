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
fl(28, 31, 0, 63, SIDE)
fl(32, 35, 0, 63, ROAD)

# ── 房子 x=17~47 ──
HX1, HX2, HC = 13, 51, 32
fl(11, 27, HX1, HX2, WALL)
wcol(HX1, 11, 27, WALL_D); wcol(HX2, 11, 27, WALL_D)
fl(11, 13, HX1+1, HX2-1, WALL_S)

# 斜屋顶（峰顶y=5，屋檐y=12）
for y in range(3, 12):
    t = (y - 3) / 8
    x1 = round(HC - t * (HC - HX1))
    x2 = round(HC + t * (HX2 - HC))
    for x in range(x1, x2+1):
        sp(x, y, ROOF_L if x < HC else (RIDGE if x == HC else ROOF_R))
wrow(11, HX1, HX2, ROOF_E)

# 正门（x=27~37，y=12~27）拱门
fl(15, 27, 27, 37, DOOR)
wcol(27, 15, 27, DOOR_D); wcol(37, 15, 27, DOOR_D)
wrow(27, 27, 37, DOOR_D)
for dx in range(-4, 5): sp(32+dx, 14, DOOR)
sp(27, 14, WALL); sp(37, 14, WALL)
for dx in [-3,-2,-1,0,1,2,3]: sp(32+dx, 13, DOOR)
for dx in [-2,-1,0,1,2]: sp(32+dx, 12, DOOR)
fl(15, 20, 28, 36, DOOR_W)
wcol(28, 15, 20, DOOR_D); wcol(36, 15, 20, DOOR_D)
wrow(15, 28, 36, DOOR_D)
wcol(32, 20, 27, DOOR_D)
sp(36, 23, (215, 188, 95)); sp(36, 24, (215, 188, 95))
wrow(28, 26, 38, WALL_D)

# 左窗（x=18~25）
fl(13, 19, 18, 25, WIN)
wcol(18, 13, 19, WIN_D); wcol(25, 13, 19, WIN_D)
wrow(13, 18, 25, WIN_D); wrow(19, 18, 25, WIN_D)
fl(14, 18, 19, 24, WIN_G)
wcol(21, 13, 19, WIN_F); wrow(16, 18, 25, WIN_F)
for wy in [14,15,17,18]: wrow(wy, 19, 20, WIN_D); wrow(wy, 22, 24, WIN_D)
wrow(20, 17, 26, WALL_D)

# 右窗（x=39~46）
fl(13, 19, 39, 46, WIN)
wcol(39, 13, 19, WIN_D); wcol(46, 13, 19, WIN_D)
wrow(13, 39, 46, WIN_D); wrow(19, 39, 46, WIN_D)
fl(14, 18, 40, 45, WIN_G)
wcol(42, 13, 19, WIN_F); wrow(16, 39, 46, WIN_F)
for wy in [14,15,17,18]: wrow(wy, 40, 41, WIN_D); wrow(wy, 43, 45, WIN_D)
wrow(20, 38, 47, WALL_D)

# ── 灌木（全宽，门前断开）──
rng = random.Random(7)
for bx in list(range(0, 25)) + list(range(40, 64)):
    top = 23 - (1 if rng.random() > 0.5 else 0)
    for by in range(top, 28):
        r2 = rng.random()
        sp(bx, by, BUSH_L if r2 > 0.72 else (BUSH_D if r2 < 0.22 else BUSH))
for fx, fy in [(3,23),(7,22),(11,23),(15,22),(19,23),(22,22),(41,23),(44,22),(48,23),(52,22),(56,23),(60,22)]:
    sp(fx, fy, FLOWER); sp(fx, fy+1, (232,212,108))

# ── 蓝花楹（右侧，x≈50~58）──
wcol(53, 19, 24, JAC_T); wcol(54, 19, 24, JAC_T)
rng2 = random.Random(5)
cx, cy_mid, half_h, max_r = 53, 11, 7, 5
for jy in range(4, 19):
    dy = abs(jy - cy_mid)
    r = round(max_r * math.sqrt(max(0, 1-(dy/half_h)**2)))
    if r < 1: r = 1
    for jx in range(cx-r, cx+r+1):
        if rng2.random() > 0.15:
            sp(jx, jy, JAC_L if rng2.random() > 0.45 else JAC)

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
