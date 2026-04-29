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
    # 底座
    fl(y_bot-1, y_bot, cx-2, cx+2, HEAT_D)
    sp(cx-2, y_bot, HEAT_M); sp(cx+2, y_bot, HEAT_M)
    # 细柱
    for _y in range(y_top+10, y_bot-1):
        sp(cx, _y, HEAT_M)
        sp(cx-1, _y, HEAT_M)
        sp(cx+1, _y, HEAT_M)
        sp(cx-2, _y, (195, 192, 188))
        sp(cx+2, _y, (195, 192, 188))
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
    # 蘑菇盖（宽5格，两行）
    BARREL = (148, 95, 52)
    fl(y_top, y_top+1, cx-3, cx+3, HEAT_M)
    sp(cx-3, y_top, BARREL); sp(cx+3, y_top, BARREL)
    sp(cx-3, y_top+1, BARREL); sp(cx+3, y_top+1, BARREL)
    wrow(y_top, cx-3, cx+3, HEAT_M)
    wrow(y_top+1, cx-2, cx+2, HEAT_L)

# 桌子两侧暖炉
draw_heater(17, 5, 27)
draw_heater(47, 5, 27)

# ── 桌子（俯视矩形）──
fl(14, 22, 22, 42, TABLE_L)

# ── 左盘：三明治（侧视）──
fl(21, 21, 22, 31, PLATE)
# 面包底层
fl(20, 21, 23, 30, BREAD_D)
fl(19, 20, 24, 29, BREAD)
# 夹层
wrow(20, 24, 25, BEEF)
wrow(20, 26, 27, SHRIMP)
wrow(20, 28, 29, CHEESE)
sp(24, 19, LETTUCE); sp(27, 19, LETTUCE); sp(29, 19, LETTUCE)
# 面包顶层
fl(18, 19, 24, 29, BREAD)
wrow(18, 24, 29, BREAD_D)
# 牙签
sp(27, 17, (188, 155, 88))
sp(27, 18, (188, 155, 88))
sp(27, 16, (228, 55, 55))

# ── 右盘：蛋糕（俯视）──
fl(15, 21, 33, 41, PLATE)
fl(16, 20, 34, 38, CAKE_B)
sp(35, 16, SOUFFLE); sp(36, 16, SOUFFLE)
sp(35, 17, SOUFFLE); sp(36, 17, SOUFFLE)
sp(35, 19, BERRY_B); sp(36, 19, BERRY_R)
sp(37, 18, BERRY_B); sp(38, 20, BERRY_R)

# ── 两杯抹茶（俯视圆形）──
# 左杯（芒果底）x=24~25, y=13~14
fl(12, 13, 24, 25, CUP)
sp(24, 13, MANGO); sp(25, 13, MANGO)
sp(24, 12, MATCHA); sp(25, 12, MATCHA)
# 右杯（草莓底）x=38~39, y=13~14
fl(12, 13, 38, 39, CUP)
sp(38, 13, STRAW_C); sp(39, 13, STRAW_C)
sp(38, 12, MATCHA); sp(39, 12, MATCHA)

# ── 姜饼人（俯视，上方，GCX=30, GCY=11）──
GCX, GCY = 30, 10
# 帽子（俯视看顶部小红方块）
fl(GCY-2, GCY-1, GCX-1, GCX+1, HAT_RED)
# 头（圆形俯视）
fl(GCY, GCY+2, GCX-2, GCX+2, GB)
sp(GCX-2, GCY, GROUND); sp(GCX+2, GCY, GROUND)
sp(GCX-2, GCY+2, GROUND); sp(GCX+2, GCY+2, GROUND)
# 眼（俯视看头顶，两小点）
sp(GCX-1, GCY+1, GB_EYE); sp(GCX+1, GCY+1, GB_EYE)
# 身体
fl(GCY+3, GCY+5, GCX-1, GCX+1, GB)

# ── 蓝兔子（俯视，下方，BCX=33, BCY=25）──
BCX, BCY = 33, 25
# 耳朵（俯视两条长条）
sp(BCX-1, BCY+2, BUN_B); sp(BCX-1, BCY+3, BUN_B)
sp(BCX+1, BCY+2, BUN_B); sp(BCX+1, BCY+3, BUN_B)
sp(BCX-1, BCY+2, BUN_IN); sp(BCX+1, BCY+2, BUN_IN)
# 头
fl(BCY, BCY+1, BCX-2, BCX+2, BUN_B)
sp(BCX-2, BCY, GROUND); sp(BCX+2, BCY, GROUND)
# 眼
sp(BCX-1, BCY, BUN_EYE); sp(BCX+1, BCY, BUN_EYE)
# 身体
fl(BCY-2, BCY-1, BCX-1, BCX+1, BUN_B)

img.save('pixel_fabrini2.png')
print('Saved')
