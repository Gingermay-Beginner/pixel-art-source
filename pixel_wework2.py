from PIL import Image

S = 12
W, H = 64, 36
canvas = [[(0,0,0)]*W for _ in range(H)]

def set_px(c, x, y, col):
    if 0 <= x < W and 0 <= y < H: c[y][x] = col

def fill(c, y1, y2, x1, x2, col):
    for y in range(y1, y2+1):
        for x in range(x1, x2+1): c[y][x] = col

def wrow(c, y, x1, x2, col):
    for x in range(x1, x2+1): c[y][x] = col

def blend(c1, c2, t):
    return tuple(int(a+t*(b-a)) for a,b in zip(c1,c2))

# ── COLORS ──
FLOOR       = (205, 198, 188)   # 偏冷灰米
FLOOR_D     = (185, 178, 168)   # 地板纹
FLOOR_L     = (218, 212, 202)   # 地板亮
TABLE       = (188, 145,  72)   # 中木棕
TABLE_D     = (172, 130,  60)   # 木纹暗线（弱）
TABLE_EDGE  = (138,  98,  40)   # 桌边
TABLE_LEG   = (115,  80,  32)   # 桌腿

# 角色色
GB          = (185, 108,  48)
GBD         = (140,  82,  35)
GBE         = ( 62,  35,  15)
GB_CHEEK    = (225, 148,  95)
GB_ICING    = (245, 232, 210)
HAT_RED     = (198,  42,  32)
HAT_DARK    = (140,  26,  20)
HAT_LITE    = (225,  72,  55)

BUN         = (118, 188, 248)
BUN_LT      = (168, 218, 255)
BUNK        = (235, 138, 165)
BUNE        = ( 42,  25,  65)
BUN_BLUSH   = (242, 148, 172)

# 科基
CORGI_B     = (225, 148,  55)   # 橘体
CORGI_D     = (188, 115,  35)   # 暗橘
CORGI_W     = (245, 235, 215)   # 白肚
CORGI_EAR   = (185, 108,  35)   # 耳
CORGI_NOSE  = ( 55,  38,  28)
CORGI_EYE   = ( 45,  30,  18)

# 桌上道具
LAPTOP_B    = ( 48,  58,  78)   # 笔电深蓝黑
LAPTOP_S    = (108, 128, 148)   # 笔电屏
LAPTOP_LT   = (158, 198, 228)   # 屏幕亮
CUP_W       = (245, 240, 232)   # 杯
CUP_D       = (210, 195, 172)
COFFEE      = (112,  75,  42)
PAPER       = (248, 244, 235)
PAPER_L     = (235, 228, 210)
PEN_R       = (205,  55,  48)

def draw_pompom(buf, x, y):
    """小啾啾，传入坐标(x,y)"""
    sp(buf, x, y, HAT_DARK)

# ── LAYER 1: FLOOR ──
fill(canvas, 0, H-1, 0, W-1, FLOOR)
import random

# ── LAYER 2: TABLE (俯视，竖向，y=2~33, x=26~44) ──
TX1, TX2 = 20, 44
TY1, TY2 = 2, 33
fill(canvas, TY1, TY2, TX1, TX2, TABLE)
# 桌面纹理（竖纹）
for x in range(TX1+2, TX2, 5):
    for y in range(TY1+1, TY2): set_px(canvas, x, y, TABLE_D)
# 桌边（阴影边）
for y in range(TY1, TY2+1): set_px(canvas, TX2, y, TABLE_EDGE)  # 右边
wrow(canvas, TY2, TX1, TX2, TABLE_EDGE)        # 底边
# 桌腿阴影
for corner in [(TX1, TY2+1),(TX2, TY2+1)]:
    if 0 <= corner[1] < H: set_px(canvas, corner[0], corner[1], TABLE_LEG)

# ── LAYER 3: 桌上道具 ──

# 深色电脑横躺镜像（键盘左，屏幕右，x=27~36, y=6~14）
LPSX, LPSY = 21, 20
fill(canvas, LPSY, LPSY+8, LPSX, LPSX+9, LAPTOP_B)
fill(canvas, LPSY+1, LPSY+7, LPSX+5, LPSX+8, LAPTOP_S)    # 屏面（右侧4列）
fill(canvas, LPSY+1, LPSY+3, LPSX+6, LPSX+8, LAPTOP_LT)   # 亮区
for y in range(LPSY, LPSY+9): set_px(canvas, LPSX+4, y, LAPTOP_B)  # 分隔竖线
KB_BG = blend(LAPTOP_B, (90,95,105), 0.4)
KB_KEY = LAPTOP_B
fill(canvas, LPSY+1, LPSY+7, LPSX+1, LPSX+3, KB_BG)       # 键盘区（左侧3列）
for ky in [LPSY+2, LPSY+4, LPSY+6]:
    wrow(canvas, ky, LPSX+1, LPSX+3, KB_KEY)
for ky in range(LPSY+1, LPSY+8): set_px(canvas, LPSX+2, ky, KB_KEY)

# 银色电脑横躺镜像（键盘左，屏幕右，x=27~36, y=18~26）
LP2X, LP2Y = 21, 6
SIL_B  = (205, 210, 218)   # 边框更浅
SIL_S  = (88, 95, 108)     # 屏幕深色
SIL_LT = (108, 118, 135)   # 屏幕亮点
SIL_KB = (155, 160, 170)   # 键盘稍深于边框
fill(canvas, LP2Y, LP2Y+8, LP2X, LP2X+9, SIL_B)
fill(canvas, LP2Y+1, LP2Y+7, LP2X+5, LP2X+8, SIL_S)
fill(canvas, LP2Y+1, LP2Y+3, LP2X+6, LP2X+8, SIL_LT)
for y in range(LP2Y, LP2Y+9): set_px(canvas, LP2X+4, y, SIL_B)
fill(canvas, LP2Y+1, LP2Y+7, LP2X+1, LP2X+3, SIL_KB)
for ky in [LP2Y+2, LP2Y+4, LP2Y+6]:
    wrow(canvas, ky, LP2X+1, LP2X+3, SIL_B)
for ky in range(LP2Y+1, LP2Y+8): set_px(canvas, LP2X+2, ky, SIL_B)

# 银色电脑2（旋转180°，放右侧）
LP3X, LP3Y = LP2X + 12, LP2Y
fill(canvas, LP3Y, LP3Y+8, LP3X, LP3X+9, SIL_B)
fill(canvas, LP3Y+1, LP3Y+7, LP3X+1, LP3X+4, SIL_S)
fill(canvas, LP3Y+1, LP3Y+3, LP3X+1, LP3X+3, SIL_LT)
for y in range(LP3Y, LP3Y+9): set_px(canvas, LP3X+5, y, SIL_B)
fill(canvas, LP3Y+1, LP3Y+7, LP3X+6, LP3X+8, SIL_KB)
for ky in [LP3Y+2, LP3Y+4, LP3Y+6]:
    wrow(canvas, ky, LP3X+6, LP3X+8, SIL_B)
for ky in range(LP3Y+1, LP3Y+8): set_px(canvas, LP3X+7, ky, SIL_B)

# ── 俯视咖啡杯（圆形外圈+咖啡色内圆）──
BOOK_A = (168, 108,  88)   # 书封面砖红
BOOK_B = (108, 148, 118)   # 书封面绿
BOOK_P = (240, 235, 220)   # 书页白

def draw_topdown_cup(cx, cy):
    # 4×4格俯视杯，cx/cy为左上角
    # 外圈（深色电脑色杯壁）
    for dx in range(4):
        canvas[cy][cx+dx]   = LAPTOP_B
        canvas[cy+3][cx+dx] = LAPTOP_B
    for dy in range(1, 3):
        canvas[cy+dy][cx]   = LAPTOP_B
        canvas[cy+dy][cx+3] = LAPTOP_B
    # 内部咖啡色（暖棕）
    canvas[cy+1][cx+1] = (138,  92,  52)
    canvas[cy+1][cx+2] = (158, 108,  62)
    canvas[cy+2][cx+1] = (148, 100,  56)
    canvas[cy+2][cx+2] = (138,  92,  52)
    # 四角圆角（用桌面色覆盖）
    canvas[cy][cx]     = TABLE
    canvas[cy][cx+3]   = TABLE
    canvas[cy+3][cx]   = TABLE
    canvas[cy+3][cx+3] = TABLE

def draw_topdown_latte(cx, cy):
    # 拿铁：奶棕底+奶泡亮点
    for dx in range(4):
        canvas[cy][cx+dx]   = LAPTOP_B
        canvas[cy+3][cx+dx] = LAPTOP_B
    for dy in range(1, 3):
        canvas[cy+dy][cx]   = LAPTOP_B
        canvas[cy+dy][cx+3] = LAPTOP_B
    canvas[cy+1][cx+1] = (192, 148,  98)
    canvas[cy+1][cx+2] = (192, 148,  98)
    canvas[cy+2][cx+1] = (192, 148,  98)
    canvas[cy+2][cx+2] = (235, 218, 195)  # 奶泡亮点
    canvas[cy][cx]     = TABLE
    canvas[cy][cx+3]   = TABLE
    canvas[cy+3][cx]   = TABLE
    canvas[cy+3][cx+3] = TABLE

def draw_topdown_book(bx, by, bw, bh, color):
    for ry in range(by, by+bh):
        for rx in range(bx, bx+bw):
            canvas[ry][rx] = color
    # 书页（右侧1格白）
    for ry in range(by, by+bh):
        canvas[ry][bx+bw] = BOOK_P

# 杯1：下移5格左移5格
draw_topdown_latte(32, 20)
# 杯1右下角再加一杯
draw_topdown_cup(39, 17)
# 杯2：桌面中段
draw_topdown_cup(37, 23)
# 书1：桌面右侧（砖红，电脑下方）
draw_topdown_book(32, 16, 5, 3, BOOK_A)
# 书2：桌面右下（绿）
draw_topdown_book(33, 28, 6, 4, BOOK_B)


# ── 科基 侧躺（右下，CRX=52, CRY=27）──
CRX, CRY = 52, 27
# 垫子（圆角矩形，柯基之前画）
PAD   = (178, 178, 178)
PAD_D = (148, 148, 148)
fill(canvas, 23, 31, TX2+1, 60, PAD)
# 圆角（四角去掉）
for corner in [(TX2+1,23),(TX2+2,23),(60,23),(60,24),(59,23),
               (TX2+1,31),(TX2+2,31),(60,31),(60,30),(59,31)]:
    set_px(canvas, corner[0], corner[1], FLOOR)
# 垫子边缘暗色（已移除）
CORGI_B   = (225, 148,  55)
CORGI_D   = (188, 115,  35)
CORGI_W   = (245, 235, 215)
CORGI_EAR = (185, 108,  35)
CORGI_NOSE= ( 55,  38,  28)
CORGI_EYE = ( 45,  30,  18)
# 身体
fill(canvas, CRY-3, CRY+1, CRX-5, CRX+3, CORGI_B)
# 肚子下缘奶油色
for bx in range(CRX-5, CRX+4): set_px(canvas, bx, CRY+1, CORGI_W)
fill(canvas, CRY-2, CRY,   CRX-3, CRX+1, CORGI_B)
set_px(canvas, CRX-5, CRY-3, PAD); set_px(canvas, CRX+3, CRY-3, FLOOR)
set_px(canvas, CRX-5, CRY+1, FLOOR); set_px(canvas, CRX+3, CRY+1, FLOOR)
# 头
fill(canvas, CRY-4, CRY-1, CRX+2, CRX+5, CORGI_B)
set_px(canvas, CRX+2, CRY-4, FLOOR); set_px(canvas, CRX+5, CRY-4, FLOOR)
set_px(canvas, CRX+2, CRY-1, FLOOR); set_px(canvas, CRX+5, CRY-1, FLOOR)
# 耳（大三角竖耳）
fill(canvas, CRY-5, CRY-5, CRX+3, CRX+3, CORGI_EAR)
set_px(canvas, CRX+2, CRY-6, CORGI_EAR)
set_px(canvas, CRX+3, CRY-5, CORGI_EAR); set_px(canvas, CRX+3, CRY-4, CORGI_EAR)
# 耳朵补格
set_px(canvas, 55, 22, CORGI_EAR); set_px(canvas, 55, 23, CORGI_EAR)
set_px(canvas, 54, 22, CORGI_EAR); set_px(canvas, 54, 23, CORGI_EAR)
set_px(canvas, 57, 22, CORGI_EAR); set_px(canvas, 57, 23, CORGI_EAR)
# 口吻（突出两格）
fill(canvas, CRY-2, CRY-1, CRX+5, CRX+6, CORGI_W)
set_px(canvas, CRX+6, CRY-1, CORGI_NOSE)  # 鼻子
# 眼
set_px(canvas, CRX+4, CRY-3, CORGI_EYE)
# 短腿
for lx in [CRX-4, CRX-6]:
    set_px(canvas, lx, CRY+2, CORGI_W)
    set_px(canvas, lx, CRY+3, CORGI_W)
set_px(canvas, 55, 28, CORGI_W); set_px(canvas, 54, 28, CORGI_W); set_px(canvas, 56, 28, CORGI_W); set_px(canvas, 57, 28, CORGI_W)
set_px(canvas, 55, 29, CORGI_W); set_px(canvas, 55, 30, CORGI_W)
set_px(canvas, 47, 28, CORGI_W)
set_px(canvas, 46, 28, CORGI_B)
set_px(canvas, 46, 27, CORGI_B)
set_px(canvas, 54, 26, CORGI_W); set_px(canvas, 54, 27, CORGI_W)
set_px(canvas, 55, 27, CORGI_W)
set_px(canvas, 53, 27, CORGI_W)
# （尾巴已移除）

# ── 垫子+柯基 旋转90°（顺时针）──
# 截取区域 x=44~61, y=22~31
_cx1, _cy1, _cx2, _cy2 = 44, 22, 61, 31
_region_w = (_cx2 - _cx1 + 1) * S
_region_h = (_cy2 - _cy1 + 1) * S
_region = Image.new('RGB', (_region_w, _region_h))
_region_px = _region.load()
for ry in range(_cy1, _cy2+1):
    for rx in range(_cx1, _cx2+1):
        c = canvas[ry][rx]
        for dy in range(S):
            for dx in range(S):
                _region_px[(rx-_cx1)*S+dx, (ry-_cy1)*S+dy] = c
_rotated = _region.rotate(-90, expand=True)  # 顺时针90°
# 清除原区域（用FLOOR填）
for ry in range(_cy1, _cy2+1):
    for rx in range(_cx1, _cx2+1):
        canvas[ry][rx] = FLOOR
# 柯基清除覆盖了桌边线，补回
for y in range(TY1, TY2+1): set_px(canvas, TX2, y, TABLE_EDGE)
# 姜饼人胳膊延伸（x=20~22, y=19~20）
for _ay in range(19, 21):
    for _ax in range(20, 23):
        canvas[_ay][_ax] = GB
# 复制胳膊（y=28~29）
for _ay in range(28, 30):
    for _ax in range(20, 23):
        canvas[_ay][_ax] = GB
# 兔子胳膊（y=5~6 和 y=14~15）
for _ay in range(5, 7):
    for _ax in range(20, 23):
        canvas[_ay][_ax] = BUN
for _ay in range(14, 16):
    for _ax in range(20, 23):
        canvas[_ay][_ax] = BUN
# 贴回（左上角对齐 x=44, y=22）
_rot_px = _rotated.load()
_rot_w, _rot_h = _rotated.size
for py in range(_rot_h):
    for px_i in range(_rot_w):
        gx = _cx1 + 1 + px_i // S
        gy = _cy1 - 5 + py // S
        if 0 <= gx < W and 0 <= gy < H:
            canvas[gy][gx] = _rot_px[px_i, py]
# 耳朵尖修正
canvas[21][54] = FLOOR
canvas[27][55] = (185, 108, 35)

# 地毯已移除

# ── 左右两侧半张桌子（各露出4格）──
# 左桌：x=0~7（拓宽到8格），含木纹和桌腿
fill(canvas, TY1, TY2, 0, 7, TABLE)
for x in range(2, 8, 5):
    for y in range(TY1+1, TY2): set_px(canvas, x, y, TABLE_D)
for y in range(TY1, TY2+1): set_px(canvas, 7, y, TABLE_EDGE)
wrow(canvas, TY2, 0, 7, TABLE_EDGE)
if TY2+1 < H: set_px(canvas, 7, TY2+1, TABLE_LEG)
# 右桌：x=58~63（左移2格），含木纹和桌腿
fill(canvas, TY1, TY2, 58, W-1, TABLE)
for x in range(60, W-1, 5):
    for y in range(TY1+1, TY2): set_px(canvas, x, y, TABLE_D)
for y in range(TY1, TY2+1): set_px(canvas, 58, y, TABLE_EDGE)
wrow(canvas, TY2, 58, W-1, TABLE_EDGE)
if TY2+1 < H: set_px(canvas, 58, TY2+1, TABLE_LEG)

# 水磨石纹理（最后画，覆盖地板区域）
random.seed(42)
TERRAZZO_DOTS = [(192,185,178),(198,192,185),(210,205,198),(185,178,170)]
for _ in range(320):
    rx = random.randint(0, W-1)
    ry = random.randint(0, H-1)
    c = canvas[ry][rx]
    if abs(c[0]-FLOOR[0])<20 and abs(c[1]-FLOOR[1])<20 and abs(c[2]-FLOOR[2])<20:
        canvas[ry][rx] = random.choice(TERRAZZO_DOTS)

# ── 俯视角色：正面画 → 旋转-90°贴入 ──
from PIL import Image as PILImage

def make_char_img(draw_fn, w, h):
    buf = [[(0,0,0,0)]*w for _ in range(h)]
    draw_fn(buf, w, h)
    img = PILImage.new('RGBA', (w*S, h*S), (0,0,0,0))
    px2 = img.load()
    for cy in range(h):
        for cx in range(w):
            col = buf[cy][cx]
            if col[3] > 0:
                for dy in range(S):
                    for dx in range(S):
                        px2[cx*S+dx, cy*S+dy] = col
    return img

def sp(buf, x, y, col):
    if 0<=y<len(buf) and 0<=x<len(buf[0]): buf[y][x]=col+(255,)
def fl(buf, y1, y2, x1, x2, col):
    for yy in range(y1,y2+1):
        for xx in range(x1,x2+1): sp(buf,xx,yy,col)

def draw_bun(buf, w, h):
    # 耳朵（y=0~4，头从y=5开始）
    fl(buf,0,4,4,4,BUN); fl(buf,0,4,6,6,BUN)
    fl(buf,1,3,4,4,BUNK); fl(buf,1,3,6,6,BUNK)
    # 头（y=5~10，x=2~8）
    fl(buf,5,10,2,8,BUN)
    sp(buf,2,5,(0,0,0,0)); sp(buf,8,5,(0,0,0,0))
    sp(buf,2,10,(0,0,0,0)); sp(buf,8,10,(0,0,0,0))
    # 连心眉 y=6
    BUN_EYE_D = (120,168,210)
    sp(buf,3,6,BUNE); sp(buf,4,6,BUNE); sp(buf,5,6,BUN_EYE_D); sp(buf,6,6,BUNE); sp(buf,7,6,BUNE)
    # 眼睛 y=7
    sp(buf,4,7,BUNE); sp(buf,6,7,BUNE)
    # 腮红 y=8
    sp(buf,3,8,BUN_BLUSH); sp(buf,7,8,BUN_BLUSH)
    # 嘴 y=9
    sp(buf,4,9,(255,255,255)); sp(buf,5,9,(255,255,255))
    # 身体（y=11~15）
    fl(buf,11,15,2,8,BUN)
    # 身体底端圆角
    for x in range(2,9): sp(buf,x,15,(0,0,0,0))
    sp(buf,1,12,BUN); sp(buf,9,12,BUN)
    sp(buf,1,13,BUN); sp(buf,9,13,BUN)
    # 手臂
    fl(buf,12,14,1,1,BUN)
    fl(buf,12,14,9,9,BUN)
    # 手臂顶角圆角
    sp(buf,0,12,(0,0,0,0)); sp(buf,10,12,(0,0,0,0))

def draw_gb(buf, w, h):
    # 头（y=5~10，x=2~8）
    fl(buf,5,10,2,8,GB)
    sp(buf,2,5,(0,0,0,0)); sp(buf,8,5,(0,0,0,0))
    sp(buf,2,10,(0,0,0,0)); sp(buf,8,10,(0,0,0,0))
    # 眼睛 y=7
    sp(buf,4,7,GBE); sp(buf,6,7,GBE)
    # 腮红 y=8
    sp(buf,3,8,GB_CHEEK); sp(buf,7,8,GB_CHEEK)
    # 嘴 y=9
    sp(buf,4,9,GBE); sp(buf,5,9,GBE)
    # 帽子（头之后画，盖住头顶）
    HAT_TOP = 4
    draw_pompom(buf, 6, HAT_TOP-1)
    fl(buf, HAT_TOP, HAT_TOP+1, 4, 8, HAT_RED)
    sp(buf,4,HAT_TOP,HAT_DARK); sp(buf,8,HAT_TOP,HAT_DARK)
    sp(buf,4,HAT_TOP+1,HAT_DARK); sp(buf,8,HAT_TOP+1,HAT_DARK)
    sp(buf,5,HAT_TOP,HAT_LITE)
    # 身体（y=11~15）
    fl(buf,11,15,2,8,GB)
    # 身体底端圆角
    for x in range(2,9): sp(buf,x,15,(0,0,0,0))
    sp(buf,1,12,GB); sp(buf,9,12,GB)
    sp(buf,1,13,GB); sp(buf,9,13,GB)
    # 手臂
    fl(buf,12,14,1,1,GB)
    fl(buf,12,14,9,9,GB)
    # 手臂顶角圆角
    sp(buf,0,12,(0,0,0,0)); sp(buf,10,12,(0,0,0,0))
    # 扣子（2颗，腮红色，间隔一格垂直排列）
    sp(buf,5,12,GB_CHEEK); sp(buf,5,14,GB_CHEEK)

CW, CH = 11, 19
bun_img = make_char_img(draw_bun, CW, CH)
gb_img  = make_char_img(draw_gb,  CW, CH)

# 逆时针旋转90° → 头朝左俯视坐姿
bun_rot = bun_img.rotate(90, expand=True, resample=PILImage.NEAREST)
gb_rot  = gb_img.rotate(90, expand=True, resample=PILImage.NEAREST)

# 渲染当前 canvas → PIL Image，贴上角色
_img = PILImage.new('RGB', (W*S, H*S))
_px = _img.load()
for y in range(H):
    for x in range(W):
        col = canvas[y][x]
        for dy in range(S):
            for dx in range(S):
                _px[x*S+dx, y*S+dy] = col
_rgba = _img.convert('RGBA')

# 椅背（正面画上圆角矩形，旋转后贴在角色之前）
CHAIR_C  = (198, 168,  55)   # 芥末黄椅背
CHAIR_D  = (158, 130,  35)   # 椅背暗色
CBW, CBH = 9, 6              # 正面宽×高

def draw_chairback(buf, w, h):
    fl(buf, 0, 5, 0, 8, CHAIR_C)
    for x in range(1, 8): sp(buf, x, 0, CHAIR_D)
    for y in range(0, 6): sp(buf, 0, y, CHAIR_D)
    for y in range(0, 6): sp(buf, 8, y, CHAIR_D)
    sp(buf, 8, 0, (0,0,0,0))
    sp(buf, 0, 0, (0,0,0,0))

chair_img = make_char_img(draw_chairback, CBW, CBH)
chair_rot = chair_img.rotate(90, expand=True, resample=PILImage.NEAREST)

# 兔子：头对齐桌左沿 x=TX1，y=4~11
BUN_X = (TX1 - CH) * S + 4 * S
BUN_Y = 5 * S
# 椅背贴在兔子之前（x 稍右，y 对齐兔子中心偏上）
BUNCHAIR_X = BUN_X - CBH * S + 13 * S
BUNCHAIR_Y = 6 * S   # 居中对齐垫子(y=5~15中心10.5，椅背9格→y=6~14)
_rgba.paste(chair_rot, (BUNCHAIR_X, BUNCHAIR_Y), chair_rot)
_rgba.paste(bun_rot, (BUN_X, BUN_Y), bun_rot)

# 姜饼人：y=17~24
GB_X = (TX1 - CH) * S + 4 * S
GB_Y = 19 * S
GBCHAIR_X = GB_X - CBH * S + 13 * S
GBCHAIR_Y = GB_Y + 1 * S   # 居中对齐垫子
_rgba.paste(chair_rot, (GBCHAIR_X, GBCHAIR_Y), chair_rot)
_rgba.paste(gb_rot, (GB_X, GB_Y), gb_rot)

# 两人椅背左侧扶手已被桌子遮挡，不单独绘制

# 兔子对面椅子（桌右侧，旋转270°，右移9格）
# 单独画一张右下角直角版
def draw_chairback_opp(buf, w, h):
    fl(buf, 0, 5, 0, 8, CHAIR_C)
    for x in range(1, 8): sp(buf, x, 0, CHAIR_D)
    for y in range(0, 6): sp(buf, 0, y, CHAIR_D)
    sp(buf, 8, 0, (0,0,0,0))
    sp(buf, 0, 0, (0,0,0,0))
    sp(buf, 0, 5, CHAIR_D)
    sp(buf, 8, 5, CHAIR_D)

chair_img_opp = make_char_img(draw_chairback_opp, CBW, CBH)
chair_rot_opp = chair_img_opp.rotate(270, expand=True, resample=PILImage.NEAREST)
OPP_X = (TX2 + 10) * S
OPP_Y = BUN_Y + S
# 椅垫（椅背和桌子之间，9×9格，贴在_rgba上椅背之前）
CUSH_X1 = TX2 + 1
CUSH_X2 = TX2 + 9
CUSH_Y1 = BUN_Y // S
CUSH_Y2 = CUSH_Y1 + 10
_cush = PILImage.new('RGBA', ((CUSH_X2-CUSH_X1+1)*S, (CUSH_Y2-CUSH_Y1+1)*S), (168, 72, 58, 255))
_cush_px = _cush.load()
# 圆角透明
for cdx, cdy in [(0,0),((CUSH_X2-CUSH_X1)*S,0),(0,(CUSH_Y2-CUSH_Y1)*S),((CUSH_X2-CUSH_X1)*S,(CUSH_Y2-CUSH_Y1)*S)]:
    for dy in range(S):
        for dx in range(S):
            _cush_px[cdx+dx, cdy+dy] = (0,0,0,0)
_rgba.paste(_cush, (CUSH_X1*S, CUSH_Y1*S), _cush)
# 扶手（上下各一条，椅背色，各向外移1格）
ARM_C = (228, 218, 198, 255)
ARM_D = (188, 172, 148, 255)
_arm = PILImage.new('RGBA', ((CUSH_X2-CUSH_X1+1)*S, 2*S), ARM_C)
_arm_px = _arm.load()
# 上扶手：再上移1格
_rgba.paste(_arm, (CUSH_X1*S, (CUSH_Y1-2)*S), _arm)
# 下扶手
_rgba.paste(_arm, (CUSH_X1*S, (CUSH_Y2+1)*S), _arm)
_rgba.paste(chair_rot_opp, (OPP_X, OPP_Y), chair_rot_opp)

# 清除孤立深色点 (54,17)（在所有paste之后直接修改_rgba像素）
_rgba_px = _rgba.load()
S_ = 12
for dy in range(S_):
    for dx in range(S_):
        _rgba_px[54*S_+dx, 17*S_+dy] = (222, 208, 182, 255)

# 清除垫子上的孤立格 (46,18) 和 (53,18)
for gx in [46, 52, 53]:
    for dy in range(S_):
        for dx in range(S_):
            _rgba_px[gx*S_+dx, 18*S_+dy] = (205, 198, 188, 255)
# (55~58,14) 补椅背暗色
for gx in [55, 56, 57, 58]:
    for dy in range(S_):
        for dx in range(S_):
            _rgba_px[gx*S_+dx, 14*S_+dy] = (158, 130, 35, 255)
CREAM = (228, 218, 198, 255)
for gx in range(18, 20):
    for gy in list(range(4, 6)) + list(range(15, 17)) + list(range(18, 20)) + list(range(29, 31)):
        for dy in range(S_):
            for dx in range(S_):
                _rgba_px[gx*S_+dx, gy*S_+dy] = CREAM

_final = _rgba.convert('RGB')
_fpx = _final.load()

# ── 地毯+双肩包（直接画在 _final 像素层）──
import math

RUG_C  = ( 48,  68, 108)
RUG_D  = ( 35,  50,  85)
BAG_MG = ( 88, 128,  88)
BAG_MG_D=(62,  95,  62)
BAG_MT = (128, 195, 172)
BAG_MT_D=(95, 155, 132)

def fpx_fill(gy1, gy2, gx1, gx2, color):
    for gy in range(gy1, gy2+1):
        for gx in range(gx1, gx2+1):
            for dy in range(S):
                for dx in range(S):
                    _fpx[gx*S+dx, gy*S+dy] = color

def fpx_set(gx, gy, color):
    for dy in range(S):
        for dx in range(S):
            _fpx[gx*S+dx, gy*S+dy] = color

# 半圆地毯已移至 canvas 层（角色之下）

# 双肩包函数
def draw_bag_fpx(bx, by, color, dark):
    fpx_fill(by, by+6, bx, bx+5, color)
    for cx2, cy2 in [(bx,by),(bx+5,by),(bx,by+6),(bx+5,by+6)]:
        fpx_set(cx2, cy2, RUG_C)
    for _y in range(by+1, by+6):
        fpx_set(bx+1, _y, dark)
        fpx_set(bx+4, _y, dark)
    for _x in range(bx+1, bx+5):
        fpx_set(_x, by+3, dark)

def draw_bag_fpx_rot(bx, by, color, dark):
    # 旋转90°：横向包，宽7格高6格，左直角右圆角
    fpx_fill(by, by+5, bx, bx+6, color)
    # 右侧圆角（靠近人一侧，露出下层桌面色）
    fpx_set(bx+6, by,   TABLE)
    fpx_set(bx+6, by+5, TABLE)
    # 肩带（两条横线）
    for _x in range(bx+1, bx+6):
        fpx_set(_x, by+1, dark)
        fpx_set(_x, by+4, dark)
    # 拉链（中间竖线）
    for _y in range(by+1, by+5):
        fpx_set(bx+3, _y, dark)

draw_bag_fpx_rot(0, 14, BAG_MG, BAG_MG_D)   # 军绿（兔子和姜饼人之间）
draw_bag_fpx_rot(0, 26, BAG_MT, BAG_MT_D)   # 薄荷绿（姜饼人侧，靠下）

_final.save("pixel_wework2.png")
print(f"Saved: {W*S}×{H*S}px")
import sys; sys.exit(0)

# ── Render ──
img = Image.new('RGB', (W*S, H*S))
px = img.load()
for y in range(H):
    for x in range(W):
        col = canvas[y][x]
        for dy in range(S):
            for dx in range(S):
                px[x*S+dx, y*S+dy] = col

img.save("pixel_wework2.png")
print(f"Saved: {W*S}×{H*S}px")
