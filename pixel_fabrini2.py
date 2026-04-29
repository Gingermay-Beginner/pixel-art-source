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
STRAW_C = (198, 62, 75)
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
                    if style == 'white':
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

# 左上伞（白色）：圆心在左边界外，cx=-2, cy=9, r=13 → 露右侧约1/4
draw_umbrella_top(-2, 9, 13, 'white')
# 左下伞（细条）：cx=-2, cy=27, r=13 → 露右侧约1/4
draw_umbrella_top(-2, 27, 13, 'thin_stripe')
# 右伞（宽条）：圆心在右边界，cx=63, cy=18, r=14 → 露左侧约半圆
draw_umbrella_top(65, 18, 14, 'wide_stripe')

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

# 桌子两侧暖炉
draw_heater(17, 5, 22)
draw_heater(47, 5, 22)

# ── 桌子（俯视矩形，扩大）──
fl(12, 28, 18, 46, TABLE_L)

# 白纸（x=20, y=12~16）
for _py in range(12,17): sp(20, _py, (248, 246, 240))
for _py in range(12,17): sp(30, _py, (248, 246, 240))
# ── 左盘：三明治（桌子左上角）──
fl(17, 17, 19, 31, PLATE)
sp(19, 17, TABLE_L); sp(31, 17, TABLE_L)
# 面包底层
fl(15, 17, 21, 29, BREAD_D)
fl(14, 16, 21, 29, BREAD)
sp(21, 14, BREAD_D); sp(29, 14, BREAD_D)
for _sy in range(14,18): sp(21, _sy, BREAD_D); sp(29, _sy, BREAD_D)
# 夹层
wrow(14, 21, 24, BEEF)
wrow(14, 25, 26, SHRIMP)
wrow(14, 27, 29, CHEESE)
sp(21, 13, LETTUCE); sp(24, 13, LETTUCE); sp(27, 13, LETTUCE); sp(29, 13, LETTUCE)
# 面包顶层
fl(11, 13, 21, 29, BREAD)
wrow(11, 21, 29, BREAD_D)
sp(21, 11, BREAD_D); sp(29, 11, BREAD_D)
for _sy in range(12,14): sp(21, _sy, BREAD_D); sp(29, _sy, BREAD_D)
# 圆角用背景色挖掉
sp(21, 11, GROUND); sp(29, 11, GROUND)
sp(21, 17, GROUND); sp(29, 17, GROUND)
# 牙签
sp(25, 9, (228, 55, 55))
sp(25, 10, (188, 155, 88))

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
fl(21, 33, 33, 45, PLATE_C)
# 盘圆角
sp(33, 21, TABLE_L); sp(45, 21, TABLE_L)
sp(33, 33, TABLE_L); sp(45, 33, TABLE_L)

# 云朵形蛋糕体（中心 x=39, y=26，适配13×13盘）
_cx, _cy = 39, 25
SOU_L = (252, 250, 245)   # 舒芙蕾高光
SOU_D = (222, 215, 200)   # 舒芙蕾阴影
# 中央椭圆（宽5高3）
for _dy in range(-1,2):
    for _dx in range(-2,3):
        sp(_cx+_dx, _cy+_dy, CARAMEL)
# 左鼓包（r=2）
for _dy in range(-1,2):
    for _dx in range(-2,3):
        if _dx*_dx + _dy*_dy <= 4:
            sp(_cx-4+_dx, _cy+_dy, CARAMEL)
# 右鼓包（r=2）
for _dy in range(-1,2):
    for _dx in range(-2,3):
        if _dx*_dx + _dy*_dy <= 4:
            sp(_cx+4+_dx, _cy+_dy, CARAMEL)
# 上鼓包（偏上）
for _dy in range(-2,1):
    for _dx in range(-1,2):
        if _dx*_dx + _dy*_dy <= 2:
            sp(_cx+_dx, _cy-2+_dy, CARAMEL)
# 蛋糕暗边（底部）
wrow(_cy+2, _cx-3, _cx+3, CARAMEL_D)
sp(_cx-4, _cy+1, CARAMEL_D); sp(_cx+4, _cy+1, CARAMEL_D)

# 舒芙蕾（r=2圆形，盖在蛋糕上方）
_sx, _sy = _cx, _cy
for _dy in range(-2,3):
    for _dx in range(-2,3):
        if _dx*_dx + _dy*_dy <= 4:
            sp(_sx+_dx, _sy+_dy, SOU)
# 高光（左上1格）
sp(_sx-1, _sy-1, SOU_L)
# 阴影（右下边缘）
sp(_sx+1, _sy+1, SOU_D); sp(_sx, _sy+2, SOU_D)
# 圆形边缘用蛋糕色描边（让圆形轮廓更清晰）
sp(_sx-2, _sy-1, CARAMEL); sp(_sx+2, _sy-1, CARAMEL)
sp(_sx-2, _sy+1, CARAMEL); sp(_sx+2, _sy+1, CARAMEL)
sp(_sx-1, _sy-2, CARAMEL); sp(_sx+1, _sy-2, CARAMEL)
sp(_sx-1, _sy+2, CARAMEL_D); sp(_sx+1, _sy+2, CARAMEL_D)
sp(_sx, _sy+2, CARAMEL_D)

# 深焦糖酱小圆碗（4×4，灰边去四角）
_BE = (168, 165, 160)
_bx1, _by1 = _cx, _cy+4
# 顶行（去角，中间2格）
sp(_bx1,   _by1-1, _BE); sp(_bx1+1, _by1-1, _BE)
# 中两行（全4格，边灰内酱）
sp(_bx1-1, _by1,   _BE); sp(_bx1, _by1, (210,158,88)); sp(_bx1+1, _by1, CARAMEL_D); sp(_bx1+2, _by1, _BE)
sp(_bx1-1, _by1+1, _BE); sp(_bx1, _by1+1, (118,72,28)); sp(_bx1+1, _by1+1, CARAMEL_D); sp(_bx1+2, _by1+1, _BE)
# 底行（去角，中间2格）
sp(_bx1,   _by1+2, _BE); sp(_bx1+1, _by1+2, _BE)
# 曲奇酱小圆碗
_bx2, _by2 = _cx+3, _cy+4
sp(_bx2,   _by2-1, _BE); sp(_bx2+1, _by2-1, _BE)
sp(_bx2-1, _by2,   _BE); sp(_bx2, _by2, (238,205,148)); sp(_bx2+1, _by2, COOKIE); sp(_bx2+2, _by2, _BE)
sp(_bx2-1, _by2+1, _BE); sp(_bx2, _by2+1, (168,132,72)); sp(_bx2+1, _by2+1, COOKIE); sp(_bx2+2, _by2+1, _BE)
sp(_bx2,   _by2+2, _BE); sp(_bx2+1, _by2+2, _BE)

# 装饰
sp(_cx-4, _cy-3, BERRY_S); sp(_cx+1, _cy-3, BERRY_S); sp(_cx+3, _cy+3, BERRY_S)
sp(_cx-2, _cy+3, BLUE_B); sp(_cx+3, _cy-3, BLUE_B); sp(_cx+5, _cy, BLUE_B)
sp(_cx-5, _cy-1, ALMOND); sp(_cx+2, _cy-4, ALMOND); sp(_cx+5, _cy+3, ALMOND)
sp(_cx-3, _cy+4, SUGAR); sp(_cx+4, _cy-4, SUGAR); sp(_cx-5, _cy+3, SUGAR)

# ── 两杯抹茶（俯视圆形）──
# 左杯（芒果底）x=24~25, y=13~14
fl(12, 13, 24, 25, CUP)
sp(24, 13, MANGO); sp(25, 13, MANGO)
sp(24, 12, MATCHA); sp(25, 12, MATCHA)
# 右杯（草莓底）x=38~39, y=13~14
fl(12, 13, 38, 39, CUP)
sp(38, 13, STRAW_C); sp(39, 13, STRAW_C)
sp(38, 12, MATCHA); sp(39, 12, MATCHA)


img.save('pixel_fabrini2.png')
print('Saved')
