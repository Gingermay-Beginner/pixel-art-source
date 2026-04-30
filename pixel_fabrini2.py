from PIL import Image
import math

S = 12
W, H = 64 * S, 36 * S
img = Image.new('RGB', (W, H), (205, 195, 182))

def sp(x, y, c):
    if 0 <= x < 64 and 0 <= y < 36:
        px = Image.new('RGB', (S, S), c)
        img.paste(px, (x * S, y * S))

def fl(y1, y2, x1, x2, c):
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            sp(x, y, c)

def wrow(y, x1, x2, c):
    for x in range(x1, x2 + 1): sp(x, y, c)

def wcol(x, y1, y2, c):
    for y in range(y1, y2 + 1): sp(x, y, c)

# ── 颜色 ──
GROUND  = (205, 195, 182)
GROUND_D= (185, 175, 162)
TABLE   = (38, 35, 32)
TABLE_L = (62, 58, 55)
PLATE   = (242, 240, 235)
BREAD   = (198, 155, 88)
BREAD_D = (165, 122, 62)
BEEF    = (148, 75, 55)
SHRIMP  = (218, 128, 108)
CHEESE  = (228, 195, 88)
LETTUCE = (118, 168, 88)
CAKE_B  = (148, 98, 65)
SOUFFLE = (238, 218, 178)
BERRY_B = (78, 52, 128)
BERRY_R = (198, 62, 75)
MATCHA  = (88, 148, 72)
MANGO   = (228, 168, 55)
STRAW_C = (235, 155, 175)
MILK_F  = (238, 232, 220)
CUP     = (55, 52, 48)

# 遮阳伞俯视（圆盘）
UMB_W   = (245, 245, 242)
UMB_WD  = (215, 215, 210)
UMB_BK  = (45, 42, 40)
UMB_BKL = (75, 72, 68)
UMB_POLE= (155, 148, 138)

# 角色颜色
GB      = (232, 155, 82)
GBD     = (188, 122, 62)
GB_EYE  = (62, 38, 18)
HAT_RED = (188, 75, 62)
BUN_B   = (105, 195, 255)
BUN_D   = (72, 148, 228)
BUN_IN  = (255, 195, 215)
BUN_EYE = (35, 55, 105)

# 取暖炉
HEAT_D  = (62, 58, 55)
HEAT_M  = (125, 138, 155)
HEAT_L  = (148, 158, 172)
HEAT_F  = (228, 145, 45)
HEAT_FL = (248, 195, 85)

# ── 地面（石板砖）──
fl(0, 35, 0, 63, GROUND)
for _gy in range(0, 36, 4):
    wrow(_gy, 0, 63, GROUND_D)
for _gx in range(0, 64, 8):
    wcol(_gx, 0, 35, GROUND_D)

# ── 遮阳伞（俯视圆盘）──
def draw_umbrella_top(cx, cy, r, style):
    """俯视遮阳伞圆盘，只画在画布内的部分"""
    for dy in range(-r, r+1):
        for dx in range(-r, r+1):
            if dx*dx + dy*dy <= r*r:
                x, y = cx+dx, cy+dy
                if 0 <= x < 64 and 0 <= y < 36:
                    # 决定颜色
                    angle = math.degrees(math.atan2(dy, dx)) % 360
                    dist = math.sqrt(dx*dx + dy*dy)
                    if style == 'ring':
                        col = UMB_W if int(dist) % 4 < 2 else UMB_BK
                    elif style == 'white':
                        col = UMB_W if int(dist) % 3 != 0 else UMB_WD
                    elif style == 'wide_stripe':
                        # 宽条：按角度分8段，黑白交替
                        seg = int(angle / 45)
                        col = UMB_BK if seg % 2 == 0 else UMB_W
                    elif style == 'thin_stripe':
                        # 细条：按角度分16段
                        seg = int(angle / 22.5)
                        col = UMB_BK if seg % 2 == 0 else UMB_W
                    # 边缘暗色
                    if dist >= r - 0.5:
                        col = UMB_WD if col == UMB_W else UMB_BKL
                    sp(x, y, col)
    # 中心伞柱
    sp(cx, cy, UMB_POLE)

# 伞移到最上层（见文件末尾）

# ── 取暖炉（俯视圆柱截面）──
def draw_heater(cx, y_top, y_bot):
    # 底座（互换：下行全宽，上行两端挖掉）
    fl(y_bot-1, y_bot, cx-2, cx+2, HEAT_D)
    sp(cx-2, y_bot-1, GROUND); sp(cx+2, y_bot-1, GROUND)
    # 细柱
    for _y in range(y_top+10, y_bot-1):
        sp(cx, _y, HEAT_M)
        sp(cx-1, _y, HEAT_M)
        sp(cx+1, _y, HEAT_M)
        sp(cx-2, _y, HEAT_L)
        sp(cx+2, _y, HEAT_L)
    # 火焰区（高8格）
    BARREL = (148, 95, 52)
    GLASS_Y = (225, 205, 88)
    fl(y_top+2, y_top+9, cx-1, cx+1, BARREL)
    # 罩子壁（亮黄描边）
    for _fy in range(y_top+2, y_top+10):
        sp(cx-2, _fy, GLASS_Y)
        sp(cx+2, _fy, GLASS_Y)
    sp(cx, y_top+9, HEAT_F)
    sp(cx-1, y_top+8, HEAT_F); sp(cx, y_top+8, HEAT_FL); sp(cx+1, y_top+8, HEAT_F)
    sp(cx-1, y_top+7, HEAT_FL); sp(cx, y_top+7, HEAT_FL); sp(cx+1, y_top+7, HEAT_FL)
    sp(cx-1, y_top+6, HEAT_F); sp(cx, y_top+6, HEAT_FL); sp(cx+1, y_top+6, HEAT_F)
    sp(cx, y_top+5, HEAT_FL); sp(cx-1, y_top+5, HEAT_F); sp(cx+1, y_top+5, HEAT_F)
    sp(cx, y_top+4, HEAT_FL)
    sp(cx, y_top+3, HEAT_F)
    sp(cx, y_top+2, HEAT_FL)
    # 蘑菇盖（上窄下宽，盖子独立上移2格）
    BARREL = (148, 95, 52)
    _ct = y_top
    fl(_ct, _ct+1, cx-3, cx+3, HEAT_M)
    wrow(_ct+1, cx-3, cx+3, HEAT_M)   # 下行全宽（炉身蓝灰色）
    wrow(_ct,   cx-2, cx+2, HEAT_L)   # 上行窄
    sp(cx-3, _ct, GROUND); sp(cx+3, _ct, GROUND)

# ── 桌子（俯视矩形，扩大）──
_TDY = -4  # 桌面偏移量（负=上移）
def tsp(x, y, c): sp(x, y + _TDY, c)
def tfl(y1, y2, x1, x2, c): fl(y1+_TDY, y2+_TDY, x1, x2, c)
def twrow(y, x1, x2, c): wrow(y+_TDY, x1, x2, c)
def twcol(x, y1, y2, c): wcol(x, y1+_TDY, y2+_TDY, c)
# 暖炉固定位置（不随桌面移动）
draw_heater(17, 5, 22)
draw_heater(47, 5, 22)
# 桌面竖条颜色计算函数
def _TBC(x): return (72,76,82) if ((x-18)%4)==0 else (95,100,108)
# 桌面金属竖条（每4格一组，两色交替）
_MA = (72, 76, 82)   # 深色
_MB = (95, 100, 108) # 稍亮色
for _bx in range(26, 47):
    _col = _MA if ((_bx - 18) % 4) == 0 else _MB
    for _by in range(12, 33):
        tsp(_bx, _by, _col)

# 食物 x 偏移（右移8格）
_FOOD_DX = 11
def ftsp(x, y, c): tsp(x+_FOOD_DX, y, c)
def ftfl(y1, y2, x1, x2, c): tfl(y1, y2, x1+_FOOD_DX, x2+_FOOD_DX, c)
def ftwrow(y, x1, x2, c): twrow(y, x1+_FOOD_DX, x2+_FOOD_DX, c)

# ── 左盘：三明治（桌子左上角）──
# 面包底层（1行，上移1格）
ftfl(17, 17, 21, 29, BREAD)
ftwrow(18, 21, 29, BREAD_D)
ftsp(21, 17, BREAD_D); ftsp(29, 17, BREAD_D)
ftsp(21, 18, BREAD_D); ftsp(29, 18, BREAD_D)
# 夹层
ftwrow(16, 21, 24, BEEF)
ftwrow(16, 25, 26, SHRIMP)
ftwrow(16, 27, 29, CHEESE)
ftsp(21, 15, LETTUCE); ftsp(24, 15, LETTUCE); ftsp(27, 15, LETTUCE); ftsp(29, 15, LETTUCE)
# 面包顶层
ftfl(13, 14, 21, 29, BREAD)
ftwrow(13, 21, 29, BREAD_D)
ftsp(21, 13, BREAD_D); ftsp(29, 13, BREAD_D)
for _sy in range(14,15): ftsp(21, _sy, BREAD_D); ftsp(29, _sy, BREAD_D)
# 圆角用背景色挖掉
ftsp(21, 13, _TBC(21)); ftsp(29, 13, _TBC(29))
# 牙签
ftsp(25, 11, (228, 55, 55))
ftsp(25, 12, (188, 155, 88))

# ── 右盘：蛋糕（俯视，桌子右下角）──
PLATE_C  = (245, 242, 238)   # 白瓷盘
CARAMEL  = (185, 128, 62)    # 焦糖蛋糕体
CARAMEL_D= (148, 95,  42)    # 深焦糖酱
COOKIE   = (215, 178, 118)   # 曲奇色酱
SOU      = (242, 238, 228)   # 乳白舒芙蕾
BERRY_S  = (215, 62,  62)    # 草莓碎
BLUE_B   = (72,  88,  175)   # 蓝莓
ALMOND   = (218, 188, 145)   # 杏仁片
SUGAR    = (248, 245, 252)   # 糖霜

# 盘子（正方形 13×13格）
tfl(20, 32, 30, 42, PLATE_C)
# 盘圆角
tsp(30, 20, _TBC(30)); tsp(42, 20, _TBC(42))
tsp(30, 32, _TBC(30)); tsp(42, 32, _TBC(42))

# 云朵形蛋糕体（中心 x=39, y=26，适配13×13盘）
_cx, _cy = 36, 24
SOU_L = (252, 250, 245)   # 舒芙蕾高光
SOU_D = (222, 215, 200)   # 舒芙蕾阴影
# 中央椭圆（宽5高3）
for _dy in range(-1,2):
    for _dx in range(-2,3):
        tsp(_cx+_dx, _cy+_dy, CARAMEL)
# 左鼓包（r=2）
for _dy in range(-1,2):
    for _dx in range(-2,3):
        if _dx*_dx + _dy*_dy <= 4:
            tsp(_cx-4+_dx, _cy+_dy, CARAMEL)
# 右鼓包（r=2）
for _dy in range(-1,2):
    for _dx in range(-2,3):
        if _dx*_dx + _dy*_dy <= 4:
            tsp(_cx+4+_dx, _cy+_dy, CARAMEL)
# 上鼓包（偏上）
for _dy in range(-2,1):
    for _dx in range(-1,2):
        if _dx*_dx + _dy*_dy <= 2:
            tsp(_cx+_dx, _cy-2+_dy, CARAMEL)
# 蛋糕暗边（底部）
twrow(_cy+2, _cx-3, _cx+3, CARAMEL_D)
tsp(_cx-4, _cy+1, CARAMEL_D); tsp(_cx+4, _cy+1, CARAMEL_D)

# 舒芙蕾（r=2圆形，盖在蛋糕上方）
_sx, _sy = _cx, _cy
for _dy in range(-2,3):
    for _dx in range(-2,3):
        if _dx*_dx + _dy*_dy <= 4:
            tsp(_sx+_dx, _sy+_dy, SOU)
# 高光（左上1格）
tsp(_sx-1, _sy-1, SOU_L)
# 阴影（右下边缘）
tsp(_sx+1, _sy+1, SOU_D); tsp(_sx, _sy+2, SOU_D)
# 圆形边缘用蛋糕色描边（让圆形轮廓更清晰）
tsp(_sx-2, _sy-1, CARAMEL); tsp(_sx+2, _sy-1, CARAMEL)
tsp(_sx-2, _sy+1, CARAMEL); tsp(_sx+2, _sy+1, CARAMEL)
tsp(_sx-1, _sy-2, CARAMEL); tsp(_sx+1, _sy-2, CARAMEL)
tsp(_sx-1, _sy+2, CARAMEL_D); tsp(_sx+1, _sy+2, CARAMEL_D)
tsp(_sx, _sy+2, CARAMEL_D)

# 深焦糖酱小圆碗（4×4，灰边去四角）
_BE = (168, 165, 160)
_bx1, _by1 = _cx, _cy+4
# 顶行（去角，中间2格）
tsp(_bx1,   _by1-1, _BE); tsp(_bx1+1, _by1-1, _BE)
# 中两行（全4格，边灰内酱）
tsp(_bx1-1, _by1,   _BE); tsp(_bx1, _by1, (210,158,88)); tsp(_bx1+1, _by1, CARAMEL_D); tsp(_bx1+2, _by1, _BE)
tsp(_bx1-1, _by1+1, _BE); tsp(_bx1, _by1+1, (118,72,28)); tsp(_bx1+1, _by1+1, CARAMEL_D); tsp(_bx1+2, _by1+1, _BE)
# 底行（去角，中间2格）
tsp(_bx1,   _by1+2, _BE); tsp(_bx1+1, _by1+2, _BE)
# 曲奇酱小圆碗
_bx2, _by2 = _cx+3, _cy+4
tsp(_bx2,   _by2-1, _BE); tsp(_bx2+1, _by2-1, _BE)
tsp(_bx2-1, _by2,   _BE); tsp(_bx2, _by2, (238,205,148)); tsp(_bx2+1, _by2, COOKIE); tsp(_bx2+2, _by2, _BE)
tsp(_bx2-1, _by2+1, _BE); tsp(_bx2, _by2+1, (168,132,72)); tsp(_bx2+1, _by2+1, COOKIE); tsp(_bx2+2, _by2+1, _BE)
tsp(_bx2,   _by2+2, _BE); tsp(_bx2+1, _by2+2, _BE)

# 装饰
tsp(_cx-4, _cy-3, BERRY_S); tsp(_cx+1, _cy-3, BERRY_S); tsp(_cx+3, _cy+3, BERRY_S)
tsp(_cx-2, _cy+3, BLUE_B); tsp(_cx+3, _cy-3, BLUE_B); tsp(_cx+5, _cy, BLUE_B)
tsp(_cx-5, _cy-1, ALMOND); tsp(_cx+2, _cy-4, ALMOND); tsp(_cx+5, _cy+3, ALMOND)
tsp(_cx-3, _cy+4, SUGAR); tsp(_cx+4, _cy-4, SUGAR); tsp(_cx-5, _cy+3, SUGAR)
# 左下角装饰
tsp(_cx-5, _cy+5, BERRY_S); tsp(_cx-4, _cy+6, BERRY_S)
tsp(_cx-3, _cy+6, BLUE_B); tsp(_cx-5, _cy+7, BLUE_B)
tsp(_cx-4, _cy+5, ALMOND); tsp(_cx-2, _cy+7, ALMOND)
tsp(_cx-3, _cy+7, SUGAR); tsp(_cx-5, _cy+6, SUGAR)

# ── 两杯抹茶（侧视图）──
CUP_W  = (245, 248, 252)  # 透明杯身
CUP_RIM= (75, 70, 65)     # 杯口/底描边
ICE    = (215, 235, 248)  # 冰块
MT_L   = (118, 178, 95)   # 抹茶浅

# 左杯（x=18~21, y=20~26）芒果底
# 杯身（无描边，3格宽）
for _y in range(13, 19):
    tsp(28, _y, CUP_W); tsp(29, _y, CUP_W); tsp(30, _y, CUP_W)
tsp(28, 13, ICE); tsp(29, 13, ICE); tsp(30, 13, ICE)
tsp(28, 14, ICE); tsp(29, 14, ICE); tsp(30, 14, ICE)
tsp(28, 15, MANGO); tsp(29, 15, MANGO); tsp(30, 15, MANGO)
tsp(28, 16, MANGO); tsp(29, 16, MANGO); tsp(30, 16, MANGO)
tsp(28, 17, MATCHA); tsp(29, 17, MT_L); tsp(30, 17, MATCHA)
tsp(28, 18, MATCHA); tsp(29, 18, MT_L); tsp(30, 18, MATCHA)
# 吸管（红色）
tsp(29, 10, (228, 80, 80)); tsp(29, 11, (228, 80, 80)); tsp(29, 12, (228, 80, 80))

# 右杯（草莓底，左移2格）
for _y in range(13, 19):
    tsp(42, _y, CUP_W); tsp(43, _y, CUP_W); tsp(44, _y, CUP_W)
tsp(42, 13, ICE); tsp(43, 13, ICE); tsp(44, 13, ICE)
tsp(42, 14, ICE); tsp(43, 14, ICE); tsp(44, 14, ICE)
tsp(42, 15, STRAW_C); tsp(43, 15, STRAW_C); tsp(44, 15, STRAW_C)
tsp(42, 16, STRAW_C); tsp(43, 16, STRAW_C); tsp(44, 16, STRAW_C)
tsp(42, 17, MATCHA); tsp(43, 17, MT_L); tsp(44, 17, MATCHA)
tsp(42, 18, MATCHA); tsp(43, 18, MT_L); tsp(44, 18, MATCHA)
# 吸管（绿色）
tsp(43, 10, (88, 178, 95)); tsp(43, 11, (88, 178, 95)); tsp(43, 12, (88, 178, 95))









# ── 两个小人（从 pixel_kiwi.py 移植）──
from PIL import Image as PILImage

# 颜色
_GB       = (185, 108,  48)
_GBE      = ( 62,  35,  15)
_GB_CHEEK = (225, 148,  95)
_HAT_RED  = (198,  42,  32)
_HAT_DARK = (140,  26,  20)
_HAT_LITE = (225,  72,  55)
_BUN      = (118, 188, 248)
_BUNK     = (235, 138, 165)
_BUNE     = ( 42,  25,  65)
_BUN_BLUSH= (242, 148, 172)

def _ksp(buf, x, y, col):
    if 0<=y<len(buf) and 0<=x<len(buf[0]):
        buf[y][x] = col if len(col)==4 else col+(255,)
def _kfl(buf, y1, y2, x1, x2, col):
    for yy in range(y1,y2+1):
        for xx in range(x1,x2+1): _ksp(buf,xx,yy,col)

def _pompom(buf, x, y):
    _ksp(buf, x-1, y, _HAT_DARK); _ksp(buf, x, y-1, _HAT_DARK)
    _ksp(buf, x, y, _HAT_DARK); _ksp(buf, x+1, y, _HAT_DARK)
    _ksp(buf, x, y+1, _HAT_DARK)

def _make_char(draw_fn, w, h):
    buf = [[(0,0,0,0) for _ in range(w)] for _ in range(h)]
    draw_fn(buf, w, h)
    ci = PILImage.new('RGBA', (w, h))
    for y in range(h):
        for x in range(w):
            ci.putpixel((x,y), buf[y][x])
    return ci

def _draw_bun(buf, w, h):
    # 耳朵（y=2~4，外侧顶部圆角）
    _kfl(buf,2,4,3,4,_BUN); _kfl(buf,2,4,6,7,_BUN)
    _ksp(buf,3,2,(0,0,0,0)); _ksp(buf,7,2,(0,0,0,0))  # 外侧顶圆角
    # 粉色内侧下移1格（y=3~4）
    _kfl(buf,3,4,4,4,_BUNK); _kfl(buf,3,4,6,6,_BUNK)
    _kfl(buf,5,10,2,8,_BUN)
    for corner in [(2,5),(8,5),(2,10),(8,10)]: _ksp(buf,corner[0],corner[1],(0,0,0,0))
    _ksp(buf,3,6,_BUNE); _ksp(buf,4,6,_BUNE); _ksp(buf,5,6,(120,168,210))
    _ksp(buf,6,6,_BUNE); _ksp(buf,7,6,_BUNE)
    _ksp(buf,4,7,_BUNE); _ksp(buf,6,7,_BUNE)
    _ksp(buf,3,8,_BUN_BLUSH); _ksp(buf,7,8,_BUN_BLUSH)
    _ksp(buf,4,9,(255,255,255)); _ksp(buf,5,9,(255,255,255)); _ksp(buf,6,9,(255,255,255))
    _kfl(buf,11,15,2,8,_BUN)
    for x in range(2,9): _ksp(buf,x,15,(0,0,0,0))
    _ksp(buf,1,12,_BUN); _ksp(buf,9,12,_BUN)
    _ksp(buf,1,13,_BUN); _ksp(buf,9,13,_BUN)
    _kfl(buf,12,14,0,1,_BUN); _kfl(buf,12,14,9,10,_BUN)
    _ksp(buf,0,12,(0,0,0,0)); _ksp(buf,10,12,(0,0,0,0))

def _draw_gb(buf, w, h):
    _kfl(buf,5,10,2,8,_GB)
    for corner in [(2,5),(8,5),(2,10),(8,10)]: _ksp(buf,corner[0],corner[1],(0,0,0,0))
    _ksp(buf,4,7,_GBE); _ksp(buf,6,7,_GBE)
    _ksp(buf,3,8,_GB_CHEEK); _ksp(buf,7,8,_GB_CHEEK)
    _ksp(buf,4,9,_GBE); _ksp(buf,5,9,_GBE); _ksp(buf,6,9,_GBE)
    HAT_TOP = 4
    _pompom(buf, 6, HAT_TOP-1)
    _kfl(buf,HAT_TOP,HAT_TOP+1,4,8,_HAT_RED)
    _ksp(buf,4,HAT_TOP,_HAT_DARK); _ksp(buf,8,HAT_TOP,_HAT_DARK)
    _ksp(buf,4,HAT_TOP+1,_HAT_DARK); _ksp(buf,8,HAT_TOP+1,_HAT_DARK)
    _ksp(buf,5,HAT_TOP,_HAT_LITE)
    _kfl(buf,11,15,2,8,_GB)
    for x in range(2,9): _ksp(buf,x,15,(0,0,0,0))
    _ksp(buf,1,12,_GB); _ksp(buf,9,12,_GB)
    _ksp(buf,1,13,_GB); _ksp(buf,9,13,_GB)
    _kfl(buf,12,14,0,1,_GB); _kfl(buf,12,14,9,10,_GB)
    _ksp(buf,0,12,(0,0,0,0)); _ksp(buf,10,12,(0,0,0,0))
    _ksp(buf,5,12,_GB_CHEEK); _ksp(buf,5,14,_GB_CHEEK)

_CW, _CH = 11, 19
_bun_img = _make_char(_draw_bun, _CW, _CH)
_gb_img  = _make_char(_draw_gb,  _CW, _CH)
# 旋转后放大 S 倍
def _scale_up(im, s):
    w, h = im.size
    big = PILImage.new('RGBA', (w*s, h*s))
    px = im.load(); bp = big.load()
    for y in range(h):
        for x in range(w):
            for dy in range(s):
                for dx in range(s):
                    bp[x*s+dx, y*s+dy] = px[x,y]
    return big

_bun_crop = _bun_img.crop((0, 0, _CW, _CH - 2))
_gb_crop  = _gb_img.crop((0, 0, _CW, _CH - 2))
_bun_rot = _bun_crop.rotate(90, expand=True, resample=PILImage.NEAREST)
_gb_rot  = _gb_crop.rotate(90, expand=True, resample=PILImage.NEAREST)
_bun_big = _scale_up(_bun_rot, S)
_gb_big  = _scale_up(_gb_rot,  S)

# 桌面快照（偏移后位置，用于压回角色上层）
_TY1 = (12 + _TDY) * S  # 桌面顶部
_TY2 = (33 + _TDY) * S  # 桌面底部
_table_snap = img.crop((26*S, _TY1, 47*S, _TY2))

# 合成到 img（先转 RGBA）
_rgba2 = img.convert('RGBA')

# 姜饼人
_GB_X = 5 * S
_GB_Y = 22 * S
_rgba2.paste(_gb_big, (_GB_X, _GB_Y), _gb_big)

# 兔子右侧（镜像）
_bun_mirror = _bun_big.transpose(PILImage.FLIP_LEFT_RIGHT)
_BUN_R_X = 43 * S
_BUN_R_Y = 22 * S
_rgba2.paste(_bun_mirror, (_BUN_R_X, _BUN_R_Y), _bun_mirror)

img = _rgba2.convert('RGB')

# 桌面（含食物）压回角色上层
img.paste(_table_snap, (26*S, _TY1))

# ── 伞（最上层）──
draw_umbrella_top(-2, 9, 13, 'white')       # 左上伞
draw_umbrella_top(-4, 27, 13, 'thin_stripe') # 左下伞（左移2格）
draw_umbrella_top(62, 13, 13, 'ring')        # 右伞（同心环）

img.save('pixel_fabrini2.png')
print('Saved')
