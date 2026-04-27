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
# 屋顶线（只在四根大柱子之间 x=16~48）
fl(5, 5, 16, 48, WALL_D)
wrow(4, 16, 48, WALL)

# 墙体
# 墙体（中间 x=16~48 从y=3，两侧从y=9）
fl(3, 26, 16, 48, WALL)
fl(9, 26, 0, 15, WALL)
fl(9, 26, 49, 63, WALL)

# 中间高墙梯形红屋顶（y=0~2，底x=16~48→顶x=22~42）
# y轴3层：y=0亮，y=1中，y=2暗
RTOP_R  = (188,  68,  52)
RTOP_RD = (148,  48,  35)
RTOP_RL = (215,  98,  72)
_roof_rows = [(2,16,48,RTOP_RD),(1,19,45,RTOP_R),(0,22,42,RTOP_RL)]
for _ry_actual, _rx1, _rx2, _base_c in _roof_rows:
    wrow(_ry_actual, _rx1, _rx2, _base_c)
    for _cx in range(_rx1+1, _rx2+1, 3):
        sp(_cx, _ry_actual, RTOP_RD)
    for _cx in range(_rx1+2, _rx2+1, 3):
        sp(_cx, _ry_actual, RTOP_RL)
# 左右屋檐探出1格
wrow(2, 15, 15, RTOP_RD)
wrow(2, 49, 49, RTOP_RD)

# 拱廊（7个拱，中间3个宽9格，两侧各宽7格）
# (起点x, 拱总宽)
ARCHES = [(2,7),(8,7),(18,9),(28,9),(38,9),(50,7),(56,7)]
for ax, aw in ARCHES:
    iw = aw - 2  # 内宽
    dy = 3 if aw == 7 else 0  # 小拱门下移3格
    # 拱柱（暗色，延伸到地面）
    # 去掉两侧小拱所有柱子
    skip_left  = (ax in (2, 10) and aw == 7) or (ax == 2 and aw == 7)
    skip_right = (ax in (48, 56) and aw == 7) or (ax == 56 and aw == 7)
    # ax=2右柱(x=8) 和 ax=56左柱(x=56) 也去掉
    if ax == 2 and aw == 7:
        pass
    elif ax == 56 and aw == 7:
        pass
    else:
        if not (ax == 8 and aw == 7):
            wcol(ax, 6, 26, WALL_D)
        if not (ax == 50 and aw == 7):
            wcol(ax+aw-1, 6, 26, WALL_D)
    # 拱内矩形部分
    fl(11+dy, 26, ax+1, ax+aw-2, WIN)
    # 大拱门底角圆角（挖代码）
    if aw == 9:
        sp(ax+1, 26, WALL); sp(ax+aw-2, 26, WALL)
    # 拱顶弧形
    wrow(10+dy, ax+1, ax+aw-2, WIN)
    wrow(9+dy, ax+2, ax+aw-3, WIN)
    sp(ax+1, 9+dy, WALL_D); sp(ax+aw-2, 9+dy, WALL_D)
    if iw >= 5:
        wrow(8+dy, ax+3, ax+aw-4, WIN)
        sp(ax+2, 8+dy, WALL_D); sp(ax+aw-3, 8+dy, WALL_D)
    # 补墙（拱顶以上）
    wrow(7+dy, ax+1, ax+aw-2, WALL)
    # 拱内亮点
    sp(ax+2, 12+dy, WIN_L); sp(ax+aw-3, 12+dy, WIN_L)
    wrow(11+dy, ax+1, ax+aw-2, WIN_L)

# 内侧柱子线各向内移2格（x=14→x=16, x=50→x=48）
wcol(14, 6, 26, WALL)   # 覆盖旧x=14深色线
wcol(50, 6, 26, WALL)   # 覆盖旧x=50深色线
wcol(16, 6, 26, WALL_D) # 新x=16深色线
wcol(48, 6, 26, WALL_D) # 新x=48深色线

# 小拱门 y=20以下变墙色（变成窗户）
for ax, aw in [(2,7),(8,7),(50,7),(56,7)]:
    fl(20, 26, ax+1, ax+aw-2, WALL)

# 大拱门 y=20~22 变墙色（截断，上移1格）
for ax, aw in [(18,9),(28,9),(38,9)]:
    fl(20, 22, ax+1, ax+aw-2, WALL)

# 红瓦屋顶（y=21~23，四根大柱子外侧）
ROOF_R  = (188,  68,  52)
ROOF_RD = (148,  48,  35)
ROOF_RL = (215,  98,  72)
# 左段 x=0~15，右段 x=48~63
for _seg in [(0, 15), (48, 63)]:
    fl(21, 23, _seg[0], _seg[1], ROOF_R)
    wrow(21, _seg[0], _seg[1], ROOF_RL)
    wrow(23, _seg[0], _seg[1], ROOF_RD)
    # 纵向瓦片：每3格一道暗线+亮线（瓦楞感）
    for _rx in range(_seg[0]+1, _seg[1]+1, 3):
        wcol(_rx, 21, 23, ROOF_RD)
    for _rx in range(_seg[0]+2, _seg[1]+1, 3):
        wcol(_rx, 21, 23, ROOF_RL)

# 连廊（y=24~26，四根大柱子外侧）：窗色背景+墙色分隔柱
_CWIN = (108, 158, 198)
fl(24, 26, 0, 15, _CWIN)
fl(24, 26, 49, 63, _CWIN)
for _cx in range(1, 16, 2):
    wcol(_cx, 24, 26, WALL)
for _cx in range(49, 64, 2):
    wcol(_cx, 24, 26, WALL)

# 墙体水平腰线（只保留四根大柱子之间 x=16~48）
wrow(6, 16, 48, WALL_L)

# 腰线上方廊柱窗（三组大拱门正上方，y=2~5）
WIN_T  = (108, 158, 198)   # 窗色（同大拱门）
for ax, aw in [(18,9),(28,9),(38,9)]:
    x1, x2 = ax+1, ax+aw-2
    fl(4, 5, x1, x2, WIN_T)
    for _cx in range(x1+1, x2, 2):
        wcol(_cx, 4, 5, WALL)

# 两侧 y=5~8 用天空色清除多余线条
fl(5, 8, 0, 15, SKY_T)
fl(5, 8, 49, 63, SKY_T)

# ── 地面 ──
fl(27, 35, 0, 63, GROUND)
wrow(27, 0, 63, GROUND_D)
# 石板纹理（横线）
for _gy in [29, 31, 33]:
    wrow(_gy, 0, 63, GROUND_D)
# 石板竖缝（错位）
for _gx in range(4, 64, 8):
    for _gy in [28, 30, 32, 34]:
        sp(_gx, _gy, GROUND_D)
for _gx in range(8, 64, 8):
    for _gy in [29, 31, 33]:
        sp(_gx, _gy, GROUND_D)

# ── 喷泉（中央，CX=32）──
FX = 32

# 水盆外缘（y=19~24，x=22~41）
fl(20, 23, 22, 41, FONT_S)
wrow(19, 24, 39, FONT_S)
wrow(24, 24, 39, FONT_D)
wcol(22, 20, 23, FONT_D)
wcol(41, 20, 23, FONT_D)
# 圆角
sp(23, 19, GROUND); sp(40, 19, GROUND)
sp(22, 20, GROUND); sp(41, 20, GROUND)
sp(22, 23, GROUND); sp(41, 23, GROUND)
sp(23, 24, GROUND); sp(40, 24, GROUND)

# 水面（盆内 y=20~23, x=23~40）
fl(20, 23, 23, 40, WATER)
# 水面亮点
wrow(20, 25, 38, WATER_L)
for _wx in [26, 29, 33, 37]:
    sp(_wx, 22, WATER_L)

# 喷水柱（中央 x=31~32, y=15~20）
for _wy in range(15, 20):
    sp(31, _wy, WATER)
    sp(32, _wy, WATER_L)
# 水花发散（y=15~16）
for _wy in [15, 16]:
    _w = 16 - _wy
    for _wx in range(FX-_w, FX+_w+1):
        if abs(_wx - FX) >= _w-1:
            sp(_wx, _wy, SPRAY)
sp(FX-2, 15, SPRAY); sp(FX+2, 15, SPRAY)
sp(FX-1, 14, SPRAY); sp(FX, 14, SPRAY); sp(FX+1, 14, SPRAY)
sp(FX, 13, SPRAY)

# 喷泉底座（y=24~25）
fl(24, 25, 26, 37, FONT_D)
wrow(24, 27, 36, FONT_S)
sp(26, 25, GROUND); sp(37, 25, GROUND)

# 连接柱（y=25~28，x=30~33）
fl(25, 28, 30, 33, FONT_D)
wcol(30, 25, 28, FONT_S)
wcol(33, 25, 28, FONT_S)

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

# ── 椅子去掉 ──

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
