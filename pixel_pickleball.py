from PIL import Image

W, H = 64, 36
SCALE = 12

def set_px(canvas, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        canvas[y][x] = color

def wrow(canvas, y, x1, x2, color):
    for x in range(x1, x2+1):
        set_px(canvas, x, y, color)

def wcol(canvas, x, y1, y2, color):
    for y in range(y1, y2+1):
        set_px(canvas, x, y, color)

def blend(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(c1[i]*(1-t)+c2[i]*t) for i in range(3))

SKY_TOP    = (130, 195, 240)
SKY_LIGHT  = (210, 235, 255)
COURT_MAIN = (108, 172,  72)
COURT_DARK = ( 72, 128,  48)
COURT_LINE = (240, 245, 215)
FENCE_POST = (148, 168, 148)
FENCE_WIRE = (172, 192, 172)
NET_WHITE  = (248, 248, 242)
NET_SHADOW = (195, 205, 195)
NET_POST   = (188, 200, 188)

GB_BODY  = (198, 118,  52)
GB_ICING = (250, 238, 215)
GB_EYE   = ( 58,  32,  12)
GB_CHEEK = (232, 158, 102)
GB_HAT   = (218,  52,  52)
GB_HAT_B = (185,  32,  32)

BUN_BODY  = (158, 208, 255)
BUN_LT    = (178, 220, 255)
BUN_INNER = (210, 168, 190)
BUN_EYE   = ( 42,  25,  72)
BROW_D    = (  8,   2,  25)   # 连心眉中间加深色
BUN_BLUSH = (248, 162, 182)
BUN_SMILE = (245, 238, 225)

PADDLE_R  = (200, 220, 240)  # GB 蓝拍
PADDLE_RD = ( 72, 118, 188)
PADDLE_B  = (228,  78,  48)  # BUN 红拍
PADDLE_BD = (185,  52,  28)
HANDLE    = (148,  98,  52)

OPP    = (175, 138, 218)
OPP_D  = (132,  98, 175)
OPP_H  = (215, 192, 245)
OPP_EYE = (45, 28, 12)
OPP2   = (118, 185, 128)
OPP2_D = ( 82, 145,  90)
OPP2_H = (168, 220, 178)

canvas = [[(0,0,0)] * W for _ in range(H)]

# ── 1. Sky
for y in range(16):
    t = y / 15.0
    c = blend(SKY_TOP, SKY_LIGHT, t)
    wrow(canvas, y, 0, W-1, c)

# 树（先画，围栏后画盖住下半）
TREE_T  = (228, 168, 188)   # 樱花粉主色
TREE_L  = (248, 210, 225)   # 亮粉/白
TREE_TK = ( 88,  62,  32)   # 树干
TREE_D  = (188, 118, 148)   # 深粉（花影）

# 左侧大树（整体右移1格）
for y, x1, x2 in [
    (2, 0, 5),(3, 0, 8),(4, 0, 7),(5, 0,11),(6, 0,10),
    (7, 0,13),(8, 0,12),(9, 0,14),(10,0,13),(11,0,15),
    (12,0,14),(13,0,15),(14,0,14),(15,0,15),
]:
    wrow(canvas, y, x1, x2, TREE_T)
set_px(canvas, 4, 3, TREE_L); set_px(canvas, 9, 5, TREE_L); set_px(canvas, 6, 7, TREE_L)
set_px(canvas, 11, 9, TREE_L); set_px(canvas, 8, 11, TREE_L); set_px(canvas, 13, 13, TREE_L)
set_px(canvas, 7, 4, TREE_D); set_px(canvas, 5, 6, TREE_D); set_px(canvas, 10, 8, TREE_D)
set_px(canvas, 6, 10, TREE_D); set_px(canvas, 12, 12, TREE_D)
wcol(canvas, 5, 10, 15, TREE_TK)
wcol(canvas, 6, 11, 15, TREE_TK)

# 右侧大树（整体左移1格）
for y, x1, x2 in [
    (3, 58, 63),(4, 56, 63),(5, 57, 63),(6, 54, 63),
    (7, 55, 63),(8, 53, 63),(9, 54, 63),(10,52, 63),
    (11,53, 63),(12,51, 63),(13,52, 63),(14,50, 63),(15,51, 63),
]:
    wrow(canvas, y, x1, x2, TREE_T)
set_px(canvas, 60, 4, TREE_L); set_px(canvas, 58, 6, TREE_L); set_px(canvas, 61, 8, TREE_L)
set_px(canvas, 54, 10, TREE_L); set_px(canvas, 57, 12, TREE_L); set_px(canvas, 52, 14, TREE_L)
set_px(canvas, 56, 5, TREE_D); set_px(canvas, 59, 7, TREE_D); set_px(canvas, 55, 9, TREE_D)
set_px(canvas, 58, 11, TREE_D); set_px(canvas, 53, 13, TREE_D)
wcol(canvas, 58, 10, 15, TREE_TK)
wcol(canvas, 57, 11, 15, TREE_TK)

# ── 2. Court
for y in range(16, H):
    wrow(canvas, y, 0, W-1, COURT_MAIN)
for y in range(16, H):
    wrow(canvas, y, 0, 9, COURT_DARK)
    wrow(canvas, y, 55, 63, COURT_DARK)
for y in range(32, H):
    wrow(canvas, y, 0, W-1, COURT_DARK)

# 透视边线：y=31（近端）左x=10，右x=54；y=18（远端）左x=16，右x=48
# 每行根据y插值算出左右边界
def court_x(y_val):
    t = (31 - y_val) / (31 - 18)
    half_near = 25  # 近端半宽（外扩1格，32-7=25）
    half_far  = 19  # 远端半宽（外扩1格，32-13=19）
    half = half_near - t * (half_near - half_far)
    lx = round(32 - half)
    rx = round(32 + half)
    return lx, rx

# 远端横线、底线、中横线、斜线 → 移到场内填色之后统一画
# （防止被 COURT_MAIN 覆盖）
# 深色两侧（y=16以下，斜线外侧）；斜线内侧填浅绿确保统一
for y in range(16, 32):
    lx, rx = court_x(y)
    wrow(canvas, y, lx, rx, COURT_MAIN)   # 场内统一浅绿
    wrow(canvas, y, 0, lx-1, COURT_DARK)
    wrow(canvas, y, rx+1, 63, COURT_DARK)
# 白线重新覆盖（浅绿填色之后画，防止被盖掉）
lx18, rx18 = court_x(18)
# 远端横线去掉（网底处不需要）
# wrow(canvas, 18, lx18, rx18, COURT_LINE)
lx31, rx31 = court_x(31)
wrow(canvas, 32, lx31, rx31, COURT_LINE)
lx24, rx24 = court_x(24)
wrow(canvas, 24, lx24, rx24, COURT_LINE)
wcol(canvas, 32, 24, 31, COURT_LINE)
for y in range(18, 32):
    lx, rx = court_x(y)
    set_px(canvas, lx, y, COURT_LINE)
    set_px(canvas, rx, y, COURT_LINE)

# ── 3. Fence
for y in range(8, 16):
    wrow(canvas, y, 0, 7, (155, 185, 200))
for x in range(1, 7, 2):
    wcol(canvas, x, 8, 15, FENCE_POST)
for y in range(9, 16, 2):
    wrow(canvas, y, 0, 7, FENCE_WIRE)
for y in range(8, 16):
    wrow(canvas, y, 57, 63, (155, 185, 200))
for x in range(58, 64, 2):
    wcol(canvas, x, 8, 15, FENCE_POST)
for y in range(9, 16, 2):
    wrow(canvas, y, 57, 63, FENCE_WIRE)

# ── 4. Opponents（网前画，网盖下半身）
# 对手是远处小人，整体缩小：头4格宽×4格高，体3格宽×3格高，腿2格×3格
# OCY是头顶y坐标

OCX1, OCY1 = 23, 6   # 小猫（紫色），向右挥拍

# 猫耳（尖耳，各1格）
set_px(canvas, OCX1-1, OCY1-1, OPP)
set_px(canvas, OCX1+1, OCY1-1, OPP)

# 头（4格宽×4格高，菱形裁角）
for dy in range(0, 4):
    for dx in range(-2, 3):
        if abs(dx) + (0 if 1<=dy<=2 else 1) <= 2:
            set_px(canvas, OCX1+dx, OCY1+dy, OPP)
set_px(canvas, OCX1,   OCY1+1, OPP_H)
set_px(canvas, OCX1-1, OCY1+1, OPP_EYE)
set_px(canvas, OCX1+1, OCY1+1, OPP_EYE)

# 身体（3格宽×3格高）
for dy in range(4, 7):
    wrow(canvas, OCY1+dy, OCX1-1, OCX1+1, OPP)

# 腿（各1格宽×3格高，分开）
wcol(canvas, OCX1-1, OCY1+7, OCY1+9, OPP_D)
wcol(canvas, OCX1+1, OCY1+7, OCY1+9, OPP_D)

# 左臂（平衡，向左）
set_px(canvas, OCX1-2, OCY1+5, OPP_D)
set_px(canvas, OCX1-3, OCY1+6, OPP_D)

# 右臂+拍（向右上挥）
set_px(canvas, OCX1+2, OCY1+4, OPP_D)
set_px(canvas, OCX1+3, OCY1+3, OPP_D)
# 拍面
wrow(canvas, OCY1+1, OCX1+4, OCX1+5, OPP_D)
wrow(canvas, OCY1+2, OCX1+4, OCX1+5, OPP_D)
wrow(canvas, OCY1+3, OCX1+4, OCX1+5, OPP_D)


OCX2, OCY2 = 40, 9   # 小狗（草绿），向左挥拍

# 狗耳（垂耳，各向外1格）
set_px(canvas, OCX2-2, OCY2,   OPP2_D)
set_px(canvas, OCX2-2, OCY2+1, OPP2_D)
set_px(canvas, OCX2+2, OCY2,   OPP2_D)
set_px(canvas, OCX2+2, OCY2+1, OPP2_D)

# 头（4格宽×4格高）
for dy in range(0, 4):
    for dx in range(-2, 3):
        if abs(dx) + (0 if 1<=dy<=2 else 1) <= 2:
            set_px(canvas, OCX2+dx, OCY2+dy, OPP2)
set_px(canvas, OCX2,   OCY2+1, OPP2_H)
set_px(canvas, OCX2-1, OCY2+1, OPP_EYE)
set_px(canvas, OCX2+1, OCY2+1, OPP_EYE)

# 身体（3格宽×3格高）
for dy in range(4, 7):
    wrow(canvas, OCY2+dy, OCX2-1, OCX2+1, OPP2)

# 腿（各1格宽×3格高，分开）
wcol(canvas, OCX2-1, OCY2+7, OCY2+9, OPP2_D)
wcol(canvas, OCX2+1, OCY2+7, OCY2+9, OPP2_D)

# 右臂（平衡，向右）
set_px(canvas, OCX2+2, OCY2+5, OPP2_D)
set_px(canvas, OCX2+3, OCY2+6, OPP2_D)

# 左臂+拍（向左上挥）
set_px(canvas, OCX2-2, OCY2+4, OPP2_D)
set_px(canvas, OCX2-3, OCY2+3, OPP2_D)
# 拍面
wrow(canvas, OCY2+1, OCX2-5, OCX2-4, OPP2_D)
wrow(canvas, OCY2+2, OCX2-5, OCX2-4, OPP2_D)
wrow(canvas, OCY2+3, OCX2-5, OCX2-4, OPP2_D)

# ── 5. Net
wcol(canvas, 10, 13, 18, NET_POST)
wcol(canvas, 11, 13, 18, NET_POST)
wcol(canvas, 53, 13, 18, NET_POST)
wcol(canvas, 54, 13, 18, NET_POST)
for y in range(14, 18):
    for x in range(12, 53):
        if (x + y) % 2 == 0:
            set_px(canvas, x, y, NET_WHITE)
        else:
            set_px(canvas, x, y, NET_SHADOW)
wrow(canvas, 14, 12, 52, NET_WHITE)

# ── 6. GINGERBREAD PERSON — 站姿 + 右臂挥拍
# 头 y=18~23，体 y=24~28，腿 y=27~30
GX, GY = 18, 30

# 头（圆润版：上下收角）
for y in range(19, 23):
    wrow(canvas, y, GX-3, GX+3, GB_BODY)
wrow(canvas, 18, GX-2, GX+2, GB_BODY)
wrow(canvas, 23, GX-2, GX+2, GB_BODY)
set_px(canvas, GX-1, 20, GB_EYE)
set_px(canvas, GX+1, 20, GB_EYE)
set_px(canvas, GX-2, 21, GB_CHEEK)
set_px(canvas, GX+2, 21, GB_CHEEK)
# 眉头（外侧上1格，比肤色深，表现紧张）
set_px(canvas, GX-2, 19, GB_EYE)
set_px(canvas, GX+2, 19, GB_EYE)
set_px(canvas, GX-1, 19, GB_EYE)
set_px(canvas, GX+1, 19, GB_EYE)
set_px(canvas, GX-1, 22, GB_ICING)
set_px(canvas,  GX,  22, GB_ICING)
set_px(canvas, GX+1, 22, GB_ICING)

# 身体（5格宽×4格高）
for y in range(24, 28):
    wrow(canvas, y, GX-2, GX+2, GB_BODY)
set_px(canvas, GX, 24, GB_ICING)
set_px(canvas, GX, 26, GB_ICING)

# 左臂（平衡，向左伸出）
set_px(canvas, GX-3, 24, GB_BODY)
set_px(canvas, GX-4, 25, GB_BODY)
set_px(canvas, GX-5, 26, GB_BODY)

# 右臂（挥拍，向右上伸出）
set_px(canvas, GX+3, 24, GB_BODY)
set_px(canvas, GX+4, 23, GB_BODY)
set_px(canvas, GX+5, 22, GB_BODY)

# 腿（各2格宽，上移一格）
wcol(canvas, GX-3, 27, GY-1, GB_BODY)
wcol(canvas, GX-2, 27, GY-1, GB_BODY)
wcol(canvas, GX+2, 27, GY-1, GB_BODY)
wcol(canvas, GX+3, 27, GY-1, GB_BODY)
set_px(canvas, GX-4, GY-1, GB_BODY)
set_px(canvas, GX+4, GY-1, GB_BODY)

# 帽子
for dx in range(-1, 4): set_px(canvas, GX+dx, 17, GB_HAT)
for dx in range(-1, 4): set_px(canvas, GX+dx, 18, GB_HAT)
set_px(canvas, GX-1, 17, GB_HAT_B); set_px(canvas, GX+3, 17, GB_HAT_B)
set_px(canvas, GX-1, 18, GB_HAT_B); set_px(canvas, GX+3, 18, GB_HAT_B)
set_px(canvas, GX+1, 16, GB_HAT_B)  # 啾啾
set_px(canvas, GX,   17, (248, 108, 88))  # 受光亮面

# 拍子（最后画）
wcol(canvas, GX+6, 20, 24, PADDLE_RD)
for y in range(16, 21):
    wrow(canvas, y, GX+6, GX+8, PADDLE_R)
for y in range(16, 21):
    set_px(canvas, GX+5, y, PADDLE_RD)
    set_px(canvas, GX+9, y, PADDLE_RD)
wrow(canvas, 16, GX+5, GX+9, PADDLE_RD)
wrow(canvas, 20, GX+5, GX+9, PADDLE_RD)

# ── 7. BLUE BUNNY — 站姿 + 左臂挥拍
BX, BY = 46, 30

# 耳朵（圆润版，底部2格宽，耳尖在内侧）
# 左耳（BX-2~BX-1）
set_px(canvas, BX-1, 12, BUN_BODY)                       # 耳尖内侧
wrow(canvas, 13, BX-2, BX-1, BUN_BODY)
wrow(canvas, 14, BX-2, BX-1, BUN_BODY)
wrow(canvas, 15, BX-2, BX-1, BUN_BODY)
wrow(canvas, 16, BX-2, BX-1, BUN_BODY)
wrow(canvas, 17, BX-2, BX-1, BUN_BODY)
set_px(canvas, BX-2, 14, BUN_INNER)                      # 内耳
set_px(canvas, BX-2, 15, BUN_INNER)
set_px(canvas, BX-2, 16, BUN_INNER)
# 右耳（BX+1~BX+2）
set_px(canvas, BX+1, 12, BUN_BODY)                       # 耳尖内侧
wrow(canvas, 13, BX+1, BX+2, BUN_BODY)
wrow(canvas, 14, BX+1, BX+2, BUN_BODY)
wrow(canvas, 15, BX+1, BX+2, BUN_BODY)
wrow(canvas, 16, BX+1, BX+2, BUN_BODY)
wrow(canvas, 17, BX+1, BX+2, BUN_BODY)
set_px(canvas, BX+2, 14, BUN_INNER)                      # 内耳（格子纹）
set_px(canvas, BX+1, 15, BUN_INNER)
set_px(canvas, BX+2, 16, BUN_INNER)

# 头（圆润版：上下收角）
for y in range(19, 23):
    wrow(canvas, y, BX-3, BX+3, BUN_BODY)
wrow(canvas, 18, BX-2, BX+2, BUN_BODY)
wrow(canvas, 23, BX-2, BX+2, BUN_BODY)
for y in range(19, 23):
    wrow(canvas, y, BX-1, BX+1, BUN_LT)
# 连心眉（y=19）
set_px(canvas, BX-2, 19, BUN_EYE)
set_px(canvas, BX-1, 19, BUN_EYE)
set_px(canvas, BX,   19, (118, 158, 215))
set_px(canvas, BX+1, 19, BUN_EYE)
set_px(canvas, BX+2, 19, BUN_EYE)
set_px(canvas, BX-1, 20, BROW_D)
set_px(canvas, BX+1, 20, BROW_D)
# 腮红保留
set_px(canvas, BX-2, 21, BUN_BLUSH)
set_px(canvas, BX+2, 21, BUN_BLUSH)
set_px(canvas, BX-1, 22, BUN_SMILE)
set_px(canvas,  BX,  22, BUN_SMILE)
set_px(canvas, BX+1, 22, BUN_SMILE)

# 身体（5格宽×4格高）
for y in range(24, 28):
    wrow(canvas, y, BX-2, BX+2, BUN_BODY)
wcol(canvas, BX, 24, 26, BUN_LT)

# 右臂（平衡，向右伸出）
set_px(canvas, BX+3, 24, BUN_BODY)
set_px(canvas, BX+4, 25, BUN_BODY)
set_px(canvas, BX+5, 26, BUN_BODY)

# 左臂（挥拍，向左上伸出）
set_px(canvas, BX-3, 24, BUN_BODY)
set_px(canvas, BX-4, 23, BUN_BODY)
set_px(canvas, BX-5, 22, BUN_BODY)

# 腿（各2格宽）
wcol(canvas, BX-3, 27, BY-1, BUN_BODY)
wcol(canvas, BX-2, 27, BY-1, BUN_BODY)
wcol(canvas, BX+2, 27, BY-1, BUN_BODY)
wcol(canvas, BX+3, 27, BY-1, BUN_BODY)
set_px(canvas, BX-4, BY-1, BUN_BODY)
set_px(canvas, BX+4, BY-1, BUN_BODY)

# 拍子（最后画）
wcol(canvas, BX-6, 20, 24, PADDLE_BD)
for y in range(16, 21):
    wrow(canvas, y, BX-8, BX-6, PADDLE_B)
for y in range(16, 21):
    set_px(canvas, BX-9, y, PADDLE_BD)
    set_px(canvas, BX-5, y, PADDLE_BD)
wrow(canvas, 16, BX-9, BX-5, PADDLE_BD)
wrow(canvas, 20, BX-9, BX-5, PADDLE_BD)

# ── 8. Ball（两拍正中，网上方天空）
BLX, BLY = 31, 11
set_px(canvas, BLX,   BLY,   (255, 240, 100))
set_px(canvas, BLX+1, BLY,   (255, 220, 50))
set_px(canvas, BLX,   BLY+1, (255, 220, 50))
set_px(canvas, BLX+1, BLY+1, (220, 185, 30))

# ── 右侧围栏外：水瓶 + 毛巾
BOTTLE  = (148, 198, 228)   # 浅蓝水瓶
BOTTLE_D= (108, 158, 198)   # 瓶身阴影
TOWEL   = (238, 178, 148)   # 毛巾橙粉
TOWEL_D = (198, 138, 108)   # 毛巾阴影
# 水瓶（x=58, y=20~25）
set_px(canvas, 58, 20, BOTTLE)
wrow(canvas, 21, 57, 59, BOTTLE)
wrow(canvas, 22, 57, 59, BOTTLE)
wrow(canvas, 23, 57, 59, BOTTLE)
set_px(canvas, 57, 22, BOTTLE_D)
wrow(canvas, 24, 57, 59, BOTTLE)
wrow(canvas, 25, 57, 59, BOTTLE)
set_px(canvas, 57, 24, BOTTLE_D); set_px(canvas, 57, 25, BOTTLE_D)
# 毛巾（x=60~62, y=21~25）
wrow(canvas, 21, 60, 62, TOWEL)
wrow(canvas, 22, 60, 62, TOWEL)
wrow(canvas, 23, 60, 62, TOWEL_D)
wrow(canvas, 24, 60, 62, TOWEL)
wrow(canvas, 25, 60, 62, TOWEL_D)
set_px(canvas, 62, 21, TOWEL_D)

set_px(canvas, 9, 29, COURT_MAIN)
set_px(canvas, 9, 30, COURT_MAIN)

# ── 观众小狗（左侧围栏外，站姿侧面朝右）
DOG_B = (242, 228, 198)
DOG_D = (198, 178, 145)
DOG_E = ( 45,  28,  12)
# 头
wrow(canvas, 21, 5, 7, DOG_B)
wrow(canvas, 22, 5, 7, DOG_B)
# 嘴巴
wrow(canvas, 23, 6, 8, DOG_B)
set_px(canvas, 8, 23, DOG_D)
# 耳朵
set_px(canvas, 4, 21, DOG_D)
set_px(canvas, 4, 22, DOG_D)
# 眼睛
set_px(canvas, 7, 22, DOG_E)
# 身体
wrow(canvas, 23, 3, 6, DOG_B)
wrow(canvas, 24, 3, 6, DOG_B)
wrow(canvas, 25, 3, 6, DOG_B)
# 腿
set_px(canvas, 6, 26, DOG_B)
set_px(canvas, 3, 25, DOG_B)
set_px(canvas, 3, 26, DOG_B)
# 尾巴
set_px(canvas, 2, 24, DOG_B)
set_px(canvas, 2, 23, DOG_B)
set_px(canvas, 1, 22, DOG_B)

# 孤儿像素覆盖：y=12 x=28,34 换天空色（渲染前）
set_px(canvas, 28, 12, (194, 227, 252))
set_px(canvas, 34, 12, (194, 227, 252))
set_px(canvas, 35, 12, (194, 227, 252))

img = Image.new("RGB", (W * SCALE, H * SCALE))
pixels = img.load()
for y in range(H):
    for x in range(W):
        c = canvas[y][x]
        for dy in range(SCALE):
            for dx in range(SCALE):
                pixels[x * SCALE + dx, y * SCALE + dy] = c

import os
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pixel_pickleball.png")

img.save(out_path)
print(f"Saved: {out_path}")
