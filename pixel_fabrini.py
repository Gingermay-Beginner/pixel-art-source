from PIL import Image, ImageDraw
import math, random

S = 12
W, H = 64 * S, 36 * S
img = Image.new('RGB', (W, H), (255, 255, 255))

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
SKY    = (188, 205, 218)   # 湾区早晨灰蓝天
SKY_L  = (205, 218, 228)
WALL   = (178, 172, 165)   # 灰砖墙
WALL_L = (192, 185, 178)
WALL_D = (158, 152, 145)
TREE1  = (88, 128, 72)     # 深绿树
TREE1L = (108, 148, 88)
TREE2  = (118, 148, 95)    # 中绿
TREE3  = (72, 108, 65)     # 暗绿
TRUNK  = (118, 92, 65)     # 树干
TRUNK_D= (95, 72, 48)

# 遮阳伞
UMB_W  = (245, 245, 242)   # 白色
UMB_WD = (215, 215, 210)   # 白色暗
UMB_BK = (45, 42, 40)      # 黑色
UMB_BKL= (75, 72, 68)      # 黑色亮
UMB_POLE = (155, 148, 138) # 伞柱
UMB_POLE_D = (118, 112, 102)

# 取暖炉
HEAT_D = (62, 58, 55)      # 炉体深灰
HEAT_M = (88, 85, 80)      # 炉体中
HEAT_L = (118, 112, 105)   # 炉体亮
HEAT_F = (228, 145, 45)    # 火焰橙
HEAT_FL= (248, 195, 85)    # 火焰亮黄

# 桌椅地面
TABLE  = (38, 35, 32)      # 黑桌
TABLE_L= (62, 58, 55)
CHAIR  = (52, 48, 45)      # 黑椅
GROUND = (205, 195, 182)   # 户外地面暖灰
GROUND_D=(185, 175, 162)

# 食物
PLATE  = (242, 240, 235)   # 白盘
BREAD  = (198, 155, 88)    # 恰巴塔面包
BREAD_D= (165, 122, 62)    # 面包暗
BEEF   = (148, 75, 55)     # 牛肉
SHRIMP = (218, 128, 108)   # 虾
CHEESE = (228, 195, 88)    # 芝士黄
LETTUCE= (118, 168, 88)    # 蔬菜
CAKE_B = (148, 98, 65)     # 蛋糕棕
CAKE_BD= (118, 72, 45)
SOUFFLE= (238, 218, 178)   # 舒芙蕾
BERRY_B= (78, 52, 128)     # 蓝莓
BERRY_R= (198, 62, 75)     # 草莓
STRAW  = (198, 62, 75)     # 草莓底料
MANGO  = (228, 168, 55)    # 芒果底料
MATCHA = (88, 148, 72)     # 抹茶绿
MILK_F = (238, 232, 220)   # 奶泡
CUP    = (55, 52, 48)      # 黑杯

# 角色颜色
GB     = (232, 155, 82)
GBD    = (188, 122, 62)
GB_CHEEK=(252, 185, 118)
GB_EYE = (62, 38, 18)
HAT_RED= (188, 75, 62)
HAT_RD = (155, 55, 45)
BUN_B  = (105, 195, 255)
BUN_L  = (138, 210, 255)
BUN_D  = (72, 148, 228)
BUN_IN = (255, 195, 215)
BUN_EYE= (35, 55, 105)
TOOTH  = (248, 245, 238)

# ── 天空 ──
fl(0, 11, 0, 63, SKY)
fl(0, 5, 0, 63, SKY_L)

# ── 远景砖墙 y=6~14 ──
fl(6, 14, 0, 63, WALL)
# 砖缝
for _wy in range(6, 15, 2):
    for _wx in range(0, 64, 4):
        sp(_wx, _wy, WALL_D)
for _wy in range(7, 15, 2):
    for _wx in range(2, 64, 4):
        sp(_wx, _wy, WALL_D)
# 顶部亮线
wrow(6, 0, 63, WALL_L)

# ── 远景树木（墙后探出树冠）──
# 左侧高树 x=2~5, y=0~8
def draw_tree(cx, top, h, c, cl, cd):
    # 树冠不规则
    for dy in range(h):
        y = top + dy
        w = max(1, 3 - abs(dy - h//3))
        for dx in range(-w, w+1):
            col = cl if dx == -w else (cd if dx == w else c)
            sp(cx+dx, y, col)

draw_tree(3, 0, 9, TREE1, TREE1L, TREE3)
draw_tree(8, 1, 7, TREE2, TREE1L, TREE3)
draw_tree(13, 0, 10, TREE1, TREE1L, TREE3)
draw_tree(20, 2, 6, TREE2, TREE1L, TREE3)
draw_tree(28, 0, 8, TREE3, TREE2, TREE3)
draw_tree(38, 1, 7, TREE1, TREE1L, TREE3)
draw_tree(48, 0, 9, TREE2, TREE1L, TREE3)
draw_tree(55, 2, 6, TREE1, TREE1L, TREE3)
draw_tree(61, 0, 8, TREE3, TREE2, TREE3)

# 树干（墙前露出部分）
for _tx, _ty in [(3,9),(8,8),(13,10),(28,9),(48,10),(55,8),(61,9)]:
    for _dy in range(2):
        sp(_tx, _ty+_dy, TRUNK)

# ── 地面 y=28~35 ──
fl(28, 35, 0, 63, GROUND)
wrow(28, 0, 63, GROUND_D)
# 地砖缝
for _gx in range(0, 64, 8):
    wcol(_gx, 28, 35, GROUND_D)
for _gy in range(30, 36, 3):
    wrow(_gy, 0, 63, GROUND_D)

# ── 三把遮阳伞 ──
# 伞形：梯形顶 + 柱子
def draw_umbrella(cx, pole_top, pole_bot, canopy_y, canopy_w, style):
    # 伞柱
    for _y in range(pole_top, pole_bot+1):
        sp(cx, _y, UMB_POLE)
        if _y == pole_bot: sp(cx, _y, UMB_POLE_D)
    # 伞蓬（梯形，从canopy_y开始，往下3行，宽从窄到宽）
    for _dy in range(4):
        _y = canopy_y + _dy
        _w = canopy_w * (_dy+1) // 4
        for _dx in range(-_w, _w+1):
            _x = cx + _dx
            if 0 <= _x < 64:
                if style == 'white':
                    col = UMB_W if _dy < 3 else UMB_WD
                    if _dy == 0: col = UMB_WD
                elif style == 'wide_stripe':
                    # 宽条：每4格交替黑白
                    seg = (_dx + _w) // 4
                    col = UMB_BK if seg % 2 == 0 else UMB_W
                    if _dy == 0: col = UMB_BKL if seg%2==0 else UMB_WD
                elif style == 'thin_stripe':
                    # 细条：每2格交替
                    seg = (_dx + _w) // 2
                    col = UMB_BK if seg % 2 == 0 else UMB_W
                    if _dy == 0: col = UMB_BKL if seg%2==0 else UMB_WD
                sp(_x, _y, col)
    # 伞蓬底边（加暗色）
    _y = canopy_y + 3
    sp(cx - canopy_w, _y, UMB_WD)
    sp(cx + canopy_w, _y, UMB_WD)

# 左伞（白色）x=12, 伞冠y=10, 宽11
draw_umbrella(12, 14, 27, 10, 11, 'white')
# 中伞（黑白宽条）x=32, 伞冠y=9, 宽13
draw_umbrella(32, 14, 27, 9, 13, 'wide_stripe')
# 右伞（黑白细条）x=52, 伞冠y=10, 宽11
draw_umbrella(52, 14, 27, 10, 11, 'thin_stripe')

# ── 取暖炉（两侧，高细柱形）──
def draw_heater(cx, y_top, y_bot):
    # 底座
    fl(y_bot-1, y_bot, cx-2, cx+2, HEAT_D)
    sp(cx-2, y_bot, HEAT_M); sp(cx+2, y_bot, HEAT_M)
    # 细柱
    for _y in range(y_top+3, y_bot-1):
        sp(cx, _y, HEAT_M)
        sp(cx-1, _y, HEAT_D)
        sp(cx+1, _y, HEAT_D)
    # 头部火焰罩
    fl(y_top, y_top+2, cx-2, cx+2, HEAT_D)
    sp(cx-1, y_top, HEAT_L); sp(cx, y_top, HEAT_L); sp(cx+1, y_top, HEAT_L)
    # 火焰
    sp(cx, y_top+1, HEAT_F)
    sp(cx-1, y_top+1, HEAT_FL); sp(cx+1, y_top+1, HEAT_FL)
    sp(cx, y_top, HEAT_FL)

draw_heater(0, 14, 27)
draw_heater(63, 14, 27)

# ── 黑色桌子（侧视，居中）──
# 桌面 y=22, x=20~43
fl(22, 22, 20, 43, TABLE_L)
wrow(22, 20, 43, TABLE)
fl(23, 23, 20, 43, TABLE)
# 桌腿
wcol(21, 24, 27, TABLE)
wcol(42, 24, 27, TABLE)

# ── 食物（桌上）──
# 左盘：三明治（恰巴塔），x=23~30, y=20~22
# 白盘底
fl(21, 21, 22, 31, PLATE)
# 面包底层
fl(20, 21, 23, 30, BREAD_D)
fl(19, 20, 24, 29, BREAD)
# 夹层：牛肉、虾、芝士、蔬菜
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
sp(27, 16, (228, 55, 55))  # 牙签头红色

# 右盘：蛋糕，x=33~41, y=19~22
fl(21, 21, 33, 42, PLATE)
# 蛋糕块1
fl(19, 21, 34, 37, CAKE_B)
wrow(19, 34, 37, CAKE_BD)
sp(34, 19, CAKE_BD); sp(37, 19, CAKE_BD)
# 舒芙蕾（圆顶）
sp(35, 18, SOUFFLE); sp(36, 18, SOUFFLE)
sp(34, 19, SOUFFLE); sp(37, 19, SOUFFLE)  # 圆弧边
# 蛋糕块2（小）
fl(20, 21, 38, 40, CAKE_B)
wrow(20, 38, 40, CAKE_BD)
# 浆果
sp(35, 21, BERRY_B); sp(36, 21, BERRY_R)
sp(39, 20, BERRY_B); sp(40, 21, BERRY_R)

# ── 两杯抹茶拿铁（桌上，角色旁）──
# 左杯（芒果底料）x=20~21, y=19~22
fl(19, 21, 20, 21, CUP)
fl(20, 21, 20, 21, MANGO)   # 底部芒果黄
sp(20, 19, MATCHA); sp(21, 19, MATCHA)  # 抹茶层
sp(20, 18, MILK_F); sp(21, 18, MILK_F) # 奶泡

# 右杯（草莓底料）x=43~44, y=19~22
fl(19, 21, 43, 44, CUP)
fl(20, 21, 43, 44, STRAW)   # 草莓红底
sp(43, 19, MATCHA); sp(44, 19, MATCHA)
sp(43, 18, MILK_F); sp(44, 18, MILK_F)

# ── 姜饼人（左，GCX=15, GCY=21）──
GCX, GCY = 15, 21
S2 = S  # 用sp()直接画

# 帽子
fl(GCY-5, GCY-4, GCX-1, GCX+2, HAT_RED)
wrow(GCY-5, GCX-1, GCX+2, HAT_RD)
fl(GCY-3, GCY-3, GCX-2, GCX+3, HAT_RED)

# 头
fl(GCY-2, GCY+2, GCX-2, GCX+2, GB)
# 圆角
sp(GCX-2, GCY-2, SKY); sp(GCX+2, GCY-2, SKY)
sp(GCX-2, GCY+2, SKY); sp(GCX+2, GCY+2, SKY)
# 眼
sp(GCX-1, GCY, GB_EYE); sp(GCX+1, GCY, GB_EYE)
# 腮红
sp(GCX-2, GCY+1, GB_CHEEK); sp(GCX+2, GCY+1, GB_CHEEK)
# 嘴（微笑）
sp(GCX-1, GCY+2, GB_EYE); sp(GCX, GCY+2, GB_EYE); sp(GCX+1, GCY+2, GB_EYE)
# 身体
fl(GCY+3, GCY+6, GCX-2, GCX+2, GB)
sp(GCX-2, GCY+3, GBD); sp(GCX+2, GCY+3, GBD)
sp(GCX-2, GCY+6, GBD); sp(GCX+2, GCY+6, GBD)
# 扣子
sp(GCX, GCY+4, GB_CHEEK); sp(GCX, GCY+6, GB_CHEEK)
# 手臂（向右伸向桌子）
sp(GCX+3, GCY+4, GB); sp(GCX+4, GCY+4, GB)
sp(GCX+3, GCY+5, GBD)
# 腿
fl(GCY+7, GCY+8, GCX-1, GCX+1, GB_CHEEK)

# ── 蓝兔子（右，BCX=49, BCY=21）──
BCX, BCY = 49, 21

# 耳朵
fl(BCY-5, BCY-3, BCX-1, BCX, BUN_B)
fl(BCY-4, BCY-3, BCX-1, BCX, BUN_IN)  # 内侧粉
fl(BCY-5, BCY-3, BCX+1, BCX+2, BUN_B)
fl(BCY-4, BCY-3, BCX+1, BCX+1, BUN_IN)
# 头
fl(BCY-2, BCY+2, BCX-2, BCX+2, BUN_B)
sp(BCX-2, BCY-2, SKY); sp(BCX+2, BCY-2, SKY)
sp(BCX-2, BCY+2, SKY); sp(BCX+2, BCY+2, SKY)
# 眼（两格宽）
sp(BCX-2, BCY, BUN_EYE); sp(BCX-1, BCY, BUN_EYE)
sp(BCX+1, BCY, BUN_EYE); sp(BCX+2, BCY, BUN_EYE)
# 腮红
sp(BCX-2, BCY+1, BUN_IN); sp(BCX+2, BCY+1, BUN_IN)
# 嘴（白色）
sp(BCX-1, BCY+2, TOOTH); sp(BCX, BCY+2, TOOTH); sp(BCX+1, BCY+2, TOOTH)
# 身体
fl(BCY+3, BCY+6, BCX-2, BCX+2, BUN_B)
sp(BCX-2, BCY+3, BUN_D); sp(BCX+2, BCY+3, BUN_D)
sp(BCX-2, BCY+6, BUN_D); sp(BCX+2, BCY+6, BUN_D)
# 手臂（向左伸向桌子）
sp(BCX-3, BCY+4, BUN_B); sp(BCX-4, BCY+4, BUN_B)
sp(BCX-3, BCY+5, BUN_D)
# 腿
fl(BCY+7, BCY+8, BCX-1, BCX+1, BUN_L)

img.save('pixel_fabrini.png')
print('Saved')
