from PIL import Image

W, H, S = 64, 36, 12
img = Image.new('RGB', (W*S, H*S), (255,255,255))

def sp(x, y, c):
    if 0<=x<W and 0<=y<H:
        for dy in range(S):
            for dx in range(S):
                img.putpixel((x*S+dx, y*S+dy), c)

def fl(y1, y2, x1, x2, c):
    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            sp(x, y, c)

def wrow(y, x1, x2, c):
    for x in range(x1, x2+1):
        sp(x, y, c)

def wcol(x, y1, y2, c):
    for y in range(y1, y2+1):
        sp(x, y, c)

# ── 颜色 ──
SKY_T  = (138, 195, 232)   # 天空上
SKY_B  = (175, 215, 240)   # 天空下
GROUND = (195, 182, 155)   # 地面（石板）
GROUND_D = (172, 158, 128)

# 图书馆墙体（斯坦福暖砂岩色）
WALL   = (212, 188, 148)
WALL_D = (182, 158, 118)
WALL_L = (232, 212, 175)
ARCH   = (155, 128,  88)   # 拱廊暗色
WIN    = ( 88, 118, 158)   # 窗户
WIN_L  = (128, 168, 205)

# 喷泉
FONT_S = (178, 195, 212)   # 水盆石头色
FONT_D = (148, 162, 178)
WATER  = ( 98, 168, 215)   # 水
WATER_L= (148, 205, 238)
SPRAY  = (218, 238, 252)   # 水花

# 椅子（黑色铁艺）
CHAIR  = ( 55,  52,  48)
CHAIR_L= ( 88,  85,  78)

# 角色
GB       = (185, 108,  48)
GBD      = (140,  82,  35)
GB_EYE   = ( 62,  38,  18)
GB_CHEEK = (215, 138,  82)
HAT_RED  = (188,  55,  48)
HAT_DARK = (135,  32,  28)
HAT_LITE = (215,  88,  72)

BUN_B    = ( 88, 158, 228)
BUN_IN   = (228, 185, 195)
BUN_EYE  = ( 35,  55, 105)
BUN_D    = ( 62, 118, 188)

# ── 天空 ──
fl(0, 14, 0, 63, SKY_T)
fl(15, 18, 0, 63, SKY_B)

# ── 图书馆主体（背景，宽64，y=4~18）──
# 屋顶线
fl(4, 5, 0, 63, WALL_D)
wrow(4, 0, 63, WALL)

# 墙体
fl(5, 18, 0, 63, WALL)

# 拱廊（7个拱，均匀分布 x=2~61）
ARCH_XS = [2, 11, 20, 29, 38, 47, 56]  # 每拱左起点，宽7格
for ax in ARCH_XS:
    # 拱内（窗户感）
    fl(8, 17, ax+1, ax+5, WIN)
    wrow(8, ax+1, ax+5, WIN_L)   # 顶亮
    # 拱柱（暗色）
    wcol(ax,   5, 17, WALL_D)
    wcol(ax+6, 5, 17, WALL_D)
    # 拱顶圆弧（手动2格）
    sp(ax+1, 7, WALL); sp(ax+5, 7, WALL)
    sp(ax+1, 6, WALL); sp(ax+5, 6, WALL)
    sp(ax+2, 5, WALL); sp(ax+4, 5, WALL)
    # 拱内亮点
    sp(ax+2, 9, WIN_L); sp(ax+4, 9, WIN_L)

# 墙体水平腰线
wrow(7, 0, 63, WALL_L)

# ── 地面 ──
fl(18, 35, 0, 63, GROUND)
wrow(18, 0, 63, GROUND_D)
# 石板纹理（横线）
for _gy in [21, 24, 27, 30, 33]:
    wrow(_gy, 0, 63, GROUND_D)
# 石板竖缝（错位）
for _gx in range(4, 64, 8):
    for _gy in [19, 20, 22, 23, 25, 26, 28, 29, 31, 32, 34]:
        sp(_gx, _gy, GROUND_D)
for _gx in range(8, 64, 8):
    for _gy in [21, 24, 27, 30, 33]:
        sp(_gx, _gy, GROUND_D)

# ── 喷泉（中央，CX=32）──
FX = 32

# 水盆外缘（椭圆感，y=22~27，x=22~41）
fl(23, 26, 22, 41, FONT_S)
wrow(22, 24, 39, FONT_S)
wrow(27, 24, 39, FONT_D)
wcol(22, 23, 26, FONT_D)
wcol(41, 23, 26, FONT_D)
# 圆角
sp(23, 22, GROUND); sp(40, 22, GROUND)
sp(22, 23, GROUND); sp(41, 23, GROUND)
sp(22, 26, GROUND); sp(41, 26, GROUND)
sp(23, 27, GROUND); sp(40, 27, GROUND)

# 水面（盆内 y=23~26, x=23~40）
fl(23, 26, 23, 40, WATER)
# 水面亮点
wrow(23, 25, 38, WATER_L)
for _wx in [26, 29, 33, 37]:
    sp(_wx, 25, WATER_L)

# 喷水柱（中央 x=31~32, y=18~23）
for _wy in range(18, 23):
    sp(31, _wy, WATER)
    sp(32, _wy, WATER_L)
# 水花发散（y=18~20）
for _wy in [18, 19]:
    _w = 19 - _wy
    for _wx in range(FX-_w, FX+_w+1):
        if abs(_wx - FX) >= _w-1:
            sp(_wx, _wy, SPRAY)
sp(FX-2, 18, SPRAY); sp(FX+2, 18, SPRAY)
sp(FX-1, 17, SPRAY); sp(FX, 17, SPRAY); sp(FX+1, 17, SPRAY)
sp(FX, 16, SPRAY)

# 喷泉底座（y=27~28）
fl(27, 28, 26, 37, FONT_D)
wrow(27, 27, 36, FONT_S)
sp(26, 28, GROUND); sp(37, 28, GROUND)

# 第二层水盆（更大，y=28~31，x=18~45）
fl(29, 30, 18, 45, FONT_S)
wrow(28, 20, 43, FONT_S)
wrow(31, 20, 43, FONT_D)
wcol(18, 29, 30, FONT_D)
wcol(45, 29, 30, FONT_D)
# 圆角（四角不画）
sp(18, 28, GROUND); sp(19, 28, GROUND); sp(44, 28, GROUND); sp(45, 28, GROUND)
sp(18, 31, GROUND); sp(19, 31, GROUND); sp(44, 31, GROUND); sp(45, 31, GROUND)
# 第二层水面
fl(29, 30, 19, 44, WATER)
wrow(29, 20, 43, WATER_L)
for _wx in [22, 27, 32, 37, 42]:
    sp(_wx, 30, WATER_L)
# 第二层底座
fl(31, 32, 22, 41, FONT_D)
wrow(31, 23, 40, FONT_S)
sp(22, 32, GROUND); sp(41, 32, GROUND)

# ── 椅子圈（围绕喷泉，前景左右各一把）──
# 左椅（x=14~18, y=26~31）-- 姜饼人坐
def draw_chair(cx, cy):
    # 椅座
    fl(cy+3, cy+4, cx-2, cx+2, CHAIR)
    wrow(cy+3, cx-2, cx+2, CHAIR_L)
    # 椅背（4格高）
    fl(cy, cy+2, cx-2, cx+2, CHAIR)
    wrow(cy, cx-1, cx+1, CHAIR_L)
    # 腿（4根）
    wcol(cx-2, cy+5, cy+6, CHAIR)
    wcol(cx+2, cy+5, cy+6, CHAIR)
    wcol(cx-1, cy+5, cy+6, CHAIR_L)
    wcol(cx+1, cy+5, cy+6, CHAIR_L)

draw_chair(16, 24)   # 左椅
draw_chair(47, 24)   # 右椅

# 后排椅子（较小/远处感）
for _cx in [8, 56]:
    fl(23, 24, _cx-1, _cx+1, CHAIR)
    wrow(23, _cx-1, _cx+1, CHAIR_L)
    wcol(_cx-1, 25, 26, CHAIR)
    wcol(_cx+1, 25, 26, CHAIR)

# ── 姜饼人（左椅，GCX=16, GCY=21）──
GCX, GCY = 16, 21

# 头（宽7格，四角挖）
fl(GCY, GCY+4, GCX-3, GCX+3, GB)
sp(GCX-3, GCY, GROUND); sp(GCX+3, GCY, GROUND)
sp(GCX-3, GCY+4, GROUND); sp(GCX+3, GCY+4, GROUND)
# 五官
sp(GCX-1, GCY+1, GB_EYE); sp(GCX+1, GCY+1, GB_EYE)
sp(GCX-2, GCY+2, GB_CHEEK); sp(GCX+2, GCY+2, GB_CHEEK)
sp(GCX-1, GCY+3, GBD); sp(GCX, GCY+3, GBD); sp(GCX+1, GCY+3, GBD)
# 帽子（右偏1格）
wrow(GCY-2, GCX-1, GCX+3, HAT_RED)
fl(GCY-1, GCY-1, GCX-2, GCX+4, HAT_RED)
sp(GCX+1, GCY-3, HAT_DARK)   # 小啾啾
wcol(GCX-2, GCY-1, GCY-1, HAT_DARK)
wcol(GCX+4, GCY-1, GCY-1, HAT_DARK)
sp(GCX-1, GCY-2, HAT_DARK); sp(GCX, GCY-2, HAT_LITE); sp(GCX+3, GCY-2, HAT_DARK)
# 身体
fl(GCY+5, GCY+8, GCX-2, GCX+2, GB)
sp(GCX, GCY+6, GB_CHEEK); sp(GCX, GCY+8, GB_CHEEK)
# 手臂
sp(GCX-3, GCY+5, GB); sp(GCX-3, GCY+6, GB); sp(GCX-4, GCY+6, GB); sp(GCX-4, GCY+7, GB)
sp(GCX+3, GCY+5, GB); sp(GCX+3, GCY+6, GB); sp(GCX+4, GCY+6, GB); sp(GCX+4, GCY+7, GB)

# ── 蓝兔子（右椅，BCX=47, BCY=21）──
BCX, BCY = 47, 21

# 耳朵
sp(BCX-1, BCY-4, BUN_B)
for _ey in range(BCY-3, BCY): sp(BCX-2, _ey, BUN_B); sp(BCX-1, _ey, BUN_B)
for _ey in range(BCY-3, BCY): sp(BCX-1, _ey, BUN_IN)
sp(BCX+1, BCY-4, BUN_B)
for _ey in range(BCY-3, BCY): sp(BCX+1, _ey, BUN_B); sp(BCX+2, _ey, BUN_B)
for _ey in range(BCY-3, BCY): sp(BCX+1, _ey, BUN_IN)

# 头（宽7格，四角挖）
fl(BCY, BCY+4, BCX-3, BCX+3, BUN_B)
sp(BCX-3, BCY, GROUND); sp(BCX+3, BCY, GROUND)
sp(BCX-3, BCY+4, GROUND); sp(BCX+3, BCY+4, GROUND)
# 五官
for bx in [BCX-2, BCX-1]: sp(bx, BCY+1, BUN_EYE)
sp(BCX, BCY+1, BUN_D)
for bx in [BCX+1, BCX+2]: sp(bx, BCY+1, BUN_EYE)
sp(BCX-1, BCY+2, BUN_EYE); sp(BCX+1, BCY+2, BUN_EYE)
sp(BCX-2, BCY+3, BUN_IN); sp(BCX+2, BCY+3, BUN_IN)
sp(BCX-1, BCY+4, (255,255,255)); sp(BCX, BCY+4, (255,255,255))
# 身体
fl(BCY+5, BCY+8, BCX-2, BCX+2, BUN_B)
# 手臂
sp(BCX-3, BCY+5, BUN_B); sp(BCX-3, BCY+6, BUN_B); sp(BCX-4, BCY+6, BUN_B); sp(BCX-4, BCY+7, BUN_B)
sp(BCX+3, BCY+5, BUN_B); sp(BCX+3, BCY+6, BUN_B); sp(BCX+4, BCY+6, BUN_B); sp(BCX+4, BCY+7, BUN_B)

img.save('pixel_stanford.png')
print('Saved')
