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
GROUND = (212, 192, 182)   # 地面（石板）
BENCH   = (228, 215, 190)   # 石椅中色
BENCH_L = (245, 232, 208)   # 石椅亮色（椅面）
BENCH_D = (218, 202, 178)   # 石椅暗色（椅下）
SHRUB   = (102, 148,  82)   # 灌木深绿
SHRUB_L = (128, 178, 105)   # 灌木亮绿
SHRUB_D = ( 72, 112,  58)   # 灌木暗绿
GROUND_D = (205, 185, 176)

# 图书馆墙体（斯坦福暖砂岩色）
WALL   = (205, 188, 158)
WALL_D = (192, 178, 152)
WALL_L = (218, 202, 172)
ARCH   = (175, 158, 128)   # 拱廊暗色
WIN    = (118, 142, 172)   # 窗户（深蓝）
WIN_L  = (138, 158, 185)   # 窗户浅蓝

# 喷泉
FONT_S = (252, 228, 168)   # 喷泉暖橙亮
FONT_D = (232, 198, 130)   # 喷泉暖橙暗
FONT_M = (242, 213, 148)   # 喷泉中间色
WATER  = ( 65, 228, 198)   # 水色
WATER_L= (185, 245, 228)   # 水浅色
SPRAY  = (218, 238, 252)   # 水花

# 椅子（黑色铁艺）
CHAIR  = ( 55,  52,  48)
CHAIR_L= ( 88,  85,  78)

# 角色
GB       = (215, 135,  65)
GBD      = (168, 105,  48)
GB_EYE   = ( 62,  38,  18)
GB_CHEEK = (240, 168, 105)
HAT_RED  = (218,  75,  65)
HAT_DARK = (135,  32,  28)
HAT_LITE = (242, 115,  95)

BUN_B    = (125, 198, 255)
BUN_IN   = (255, 225, 235)
BUN_EYE  = ( 35,  55, 105)
BUN_D    = ( 95, 158, 228)

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
fl(10, 26, 4, 15, WALL)
fl(10, 26, 49, 60, WALL)

# 中间高墙梯形红屋顶（y=0~2，底x=16~48→顶x=22~42）
# y轴3层：y=0亮，y=1中，y=2暗
RTOP_R  = (188,  92,  72)
RTOP_RD = (168,  78,  62)
RTOP_RL = (208, 108,  88)
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
ARCHES = [(5,5),(10,5),(18,9),(28,9),(38,9),(50,5),(55,5)]
for ax, aw in ARCHES:
    iw = aw - 2  # 内宽
    dy = 3 if aw == 5 else 0  # 小拱门下移3格
    # 拱柱（暗色，延伸到地面）
    # 去掉两侧小拱所有柱子
    skip_left  = (ax in (2, 10) and aw == 5) or (ax == 2 and aw == 5)
    skip_right = (ax in (48, 55) and aw == 7) or (ax == 55 and aw == 5)
    # ax=2右柱(x=8) 和 ax=56左柱(x=56) 也去掉
    if ax == 2 and aw == 7:
        pass
    elif ax == 56 and aw == 7:
        pass
    else:
        if aw == 9:
            col_top = 7
            wcol(ax, col_top, 26, WALL_D)
            wcol(ax+aw-1, col_top, 26, WALL_D)
    # 拱内矩形部分
    _wfill = WIN if aw == 9 else WIN
    fl(11+dy, 26, ax+1, ax+aw-2, _wfill)
    if aw == 9:
        sp(ax+1, 26, WALL); sp(ax+aw-2, 26, WALL)
    wrow(10+dy, ax+1, ax+aw-2, _wfill)
    wrow(9+dy, ax+2, ax+aw-3, _wfill)
    sp(ax+1, 9+dy, WALL_D); sp(ax+aw-2, 9+dy, WALL_D)
    if iw >= 5:
        wrow(8+dy, ax+3, ax+aw-4, _wfill)
        sp(ax+2, 8+dy, WALL_D); sp(ax+aw-3, 8+dy, WALL_D)
    # 补墙（拱顶以上）
    wrow(7+dy, ax+1, ax+aw-2, WALL)
    # 拱内亮点
    sp(ax+2, 12+dy, WIN); sp(ax+aw-3, 12+dy, WIN)
    wrow(11+dy, ax+1, ax+aw-2, WIN)

# 内侧柱子线各向内移2格（x=14→x=16, x=50→x=48）
wcol(14, 10, 26, WALL)   # 覆盖旧x=14深色线
wcol(50, 10, 26, WALL)   # 覆盖旧x=50深色线
wcol(16, 7, 26, WALL_D) # 新x=16深色线
wcol(48, 7, 26, WALL_D) # 新x=48深色线

# 小拱门 y=20以下变墙色（变成窗户）
for ax, aw in [(5,5),(10,5),(50,5),(55,5)]:
    fl(20, 26, ax+1, ax+aw-2, WALL)

# 大拱门 y=20~22 变墙色（截断，上移1格）
for ax, aw in [(18,9),(28,9),(38,9)]:
    fl(20, 22, ax+1, ax+aw-2, WALL)

# 红瓦屋顶（y=21~23，四根大柱子外侧）
ROOF_R  = (188,  92,  72)
ROOF_RD = (168,  78,  62)
ROOF_RL = (208, 108,  88)
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
_CWIN = WIN
fl(24, 26, 0, 15, _CWIN)
fl(24, 26, 49, 63, _CWIN)
for _cx in range(1, 16, 2):
    wcol(_cx, 24, 26, WALL)
for _cx in range(49, 64, 2):
    wcol(_cx, 24, 26, WALL)

# 墙体水平腰线（只保留四根大柱子之间 x=16~48）
wrow(6, 16, 48, WALL_L)

# 腰线上方廊柱窗（三组大拱门正上方，y=2~5）
WIN_T  = WIN   # 窗色（同大拱门）
for ax, aw in [(18,9),(28,9),(38,9)]:
    x1, x2 = ax+1, ax+aw-2
    fl(4, 5, x1, x2, WIN_T)
    for _cx in range(x1+1, x2, 2):
        wcol(_cx, 4, 5, WALL)

# 两侧 y=5 用天空色清除多余线条（y=6~8留给红瓦）
fl(5, 5, 0, 15, SKY_T)
fl(5, 5, 49, 63, SKY_T)

# ── 地面 ──
fl(31, 35, 0, 63, GROUND)
wrow(31, 0, 63, GROUND_D)
# 正方形小砖（两排错列）
# 上排 y=31~32：竖缝 x%4==3
for _gx in range(3, 64, 4):
    sp(_gx, 31, GROUND_D); sp(_gx, 32, GROUND_D)
# 下排 y=34：竖缝错位2格 (x+2)%4==3
for _gx in range(1, 64, 4):
    sp(_gx, 34, GROUND_D)
# 横缝
wrow(33, 0, 63, GROUND_D)
wrow(35, 0, 63, GROUND_D)

# 中间拱门顶部阴影（x=31~33, y=6，柱子色）
# 大拱门 y=23~26 改为深蓝色
for _ax in [18, 28, 38]:
    fl(23, 26, _ax+1, _ax+7, WIN)
sp(31, 7, WALL_D); sp(32, 7, WALL_D); sp(33, 7, WALL_D)
# 中间拱门底部中柱（x=32, y=23~26）
wcol(32, 23, 26, WALL)
# 左右拱门底部中柱
wcol(22, 23, 26, WALL)
wcol(42, 23, 26, WALL)

# 左右大拱门竖线+拱顶阴影（ax=18, ax=38）
for _ax in [18, 38]:
    wcol(_ax+2, 8, 8, WALL_D); wcol(_ax+2, 9, 19, WIN_L)
    wcol(_ax+6, 8, 8, WALL_D); wcol(_ax+6, 9, 19, WIN_L)
    sp(_ax+3, 7, WALL_D); sp(_ax+4, 7, WALL_D); sp(_ax+5, 7, WALL_D)

# 中间拱门内竖线柱（x=30, x=34，y=8~19，在喷泉前画被遮盖）
wcol(30, 8, 8, WALL_D); wcol(30, 9, 19, WIN_L)
wcol(34, 8, 8, WALL_D); wcol(34, 9, 19, WIN_L)


# ── 椅子去掉 ──

# 四根大柱合并台阶（整体，y=27~30，逐行向外扩，越低越深越冷）
STEPS = [
    (195, 192, 188),  # y=27 最浅灰
    (182, 180, 175),  # y=28
    (172, 168, 165),  # y=29
    (158, 155, 152),  # y=30 最深灰
]
for _sw, _sc in enumerate(STEPS):
    _y = 27 + _sw
    _x1 = 18 - _sw - 2
    _x2 = 48 + _sw
    wrow(_y, _x1, _x2, _sc)

# ── 喷泉（中央，CX=32）新版 ──
FX = 32
SPRAY = (185, 245, 228)

# 第一层水盆外缘 x=22~42
fl(20, 21, 22, 42, FONT_S)
fl(22, 23, 23, 41, FONT_S)
wrow(19, 24, 40, FONT_S)
fl(20, 23, 23, 41, FONT_S)
sp(23, 20, FONT_D); sp(27, 20, FONT_D); sp(32, 20, FONT_D); sp(37, 20, FONT_D); sp(41, 20, FONT_D)

# 喷水柱
for _wy in range(17, 19):
    sp(31, _wy, WATER)
    sp(32, _wy, WATER_L)
    sp(33, _wy, WATER)
# 水花
for _wy in [17, 18]:
    _w = 18 - _wy
    for _wx in range(FX-_w, FX+_w+1):
        if abs(_wx - FX) >= _w-1:
            sp(_wx, _wy, SPRAY)
sp(FX-2, 17, SPRAY); sp(FX+2, 17, SPRAY)
sp(FX-1, 16, SPRAY); sp(FX, 16, SPRAY); sp(FX+1, 16, SPRAY)
sp(FX, 15, SPRAY)

# 底座 x=26~38
fl(24, 25, 29, 35, FONT_D)
wrow(24, 27, 37, FONT_S)

# 连接柱 x=29~35
fl(25, 28, 28, 36, FONT_M)
wcol(28, 25, 27, FONT_M)
wcol(36, 25, 27, FONT_M)

# 第二层水盆 x=18~46
fl(29, 30, 18, 46, FONT_S)
wrow(31, 20, 44, FONT_S)
wcol(16, 29, 30, FONT_S)
wcol(16, 31, 31, FONT_S)
wcol(17, 29, 31, FONT_S)
wcol(47, 29, 31, FONT_S)
wcol(48, 31, 31, FONT_S)
wcol(48, 29, 30, FONT_S)
fl(29, 30, 19, 45, WATER)
wrow(30, 18, 46, WATER_L)
wrow(30, 20, 44, WATER_L)
for _wx in [22, 18, 32, 46, 42]:
    sp(_wx, 29, WATER_L)
    sp(_wx, 30, WATER)

# 第二层底座 x=22~42
fl(31, 32, 22, 42, FONT_S)
wrow(31, 23, 41, FONT_S)

for _wx in [23, 27, 32, 37, 41]:
    sp(_wx, 19, WATER)
# 水流及盆面细节
sp(18, 24, (65, 228, 198)); sp(18, 25, (65, 228, 198)); sp(18, 26, (65, 228, 198))
sp(18, 27, (65, 228, 198)); sp(18, 28, (65, 228, 198))
sp(19, 22, (185, 245, 228)); sp(19, 23, (65, 228, 198)); sp(22, 28, (65, 228, 198))
sp(20, 21, (185, 245, 228))
sp(21, 20, (185, 245, 228))
sp(22, 19, FONT_S); sp(22, 20, (185, 245, 228)); sp(22, 21, FONT_S)
sp(22, 25, WATER); sp(22, 26, WATER); sp(22, 27, WATER); sp(22, 28, (65, 228, 198)); sp(42, 25, WATER); sp(42, 26, WATER); sp(42, 27, WATER); sp(42, 28, (65, 228, 198))
sp(23, 19, (65, 228, 198)); sp(23, 21, FONT_S); sp(23, 22, (185, 245, 228)); sp(23, 23, (65, 228, 198)); sp(23, 24, (65, 228, 198))
sp(24, 21, (185, 245, 228)); sp(24, 22, FONT_S)
sp(25, 20, (185, 245, 228)); sp(25, 21, FONT_S)
sp(26, 20, (185, 245, 228))
sp(27, 19, (65, 228, 198))
sp(26, 24, FONT_S); sp(38, 24, FONT_S)
sp(41, 19, (65, 228, 198)); sp(41, 21, FONT_S); sp(41, 22, (185, 245, 228)); sp(41, 23, (65, 228, 198)); sp(41, 24, (65, 228, 198))
sp(42, 19, FONT_S); sp(42, 20, (185, 245, 228)); sp(42, 21, FONT_S)
sp(43, 20, (185, 245, 228))
sp(44, 21, (185, 245, 228))
sp(45, 22, (185, 245, 228)); sp(45, 23, (65, 228, 198))
sp(46, 24, (65, 228, 198)); sp(46, 25, (65, 228, 198)); sp(46, 26, (65, 228, 198)); sp(46, 27, (65, 228, 198)); sp(46, 28, (65, 228, 198))
sp(39, 20, (185, 245, 228)); sp(38, 20, (185, 245, 228))
sp(40, 21, (185, 245, 228))
sp(40, 22, FONT_S)
sp(37, 19, (65, 228, 198))
sp(32, 21, WATER_L); sp(32, 22, WATER_L)
sp(32, 23, WATER); sp(32, 24, WATER); sp(32, 25, WATER); sp(32, 26, WATER); sp(32, 27, WATER); sp(32, 28, WATER)

# 喷泉底层（台阶之后画，不被覆盖）
wrow(31, 18, 46, FONT_S)
sp(18, 31, FONT_S); sp(46, 31, FONT_S)
wrow(32, 17, 47, FONT_S)





# 灌木（台阶两侧，y=27~30）
for _bx, _by, _bc in [
    # 左侧灌木
    (14,27,SHRUB_L),(15,27,SHRUB),(16,27,SHRUB),(17,27,SHRUB_L),
    (13,28,SHRUB),(14,28,SHRUB),(15,28,SHRUB_L),(16,28,SHRUB),(17,28,SHRUB_D),
    (13,29,SHRUB_D),(14,29,SHRUB),(15,29,SHRUB),(16,29,SHRUB_D),
    (14,30,SHRUB_D),(15,30,SHRUB_D),
    # 右侧灌木（对称）
    (46,27,SHRUB_L),(47,27,SHRUB),(48,27,SHRUB),(49,27,SHRUB_L),
    (46,28,SHRUB_D),(47,28,SHRUB),(48,28,SHRUB_L),(49,28,SHRUB),(50,28,SHRUB),
    (47,29,SHRUB_D),(48,29,SHRUB),(49,29,SHRUB),(50,29,SHRUB_D),
    (48,30,SHRUB_D),(49,30,SHRUB_D),
]:
    sp(_bx, _by, _bc)

# 姜饼人石椅
fl(26, 28, 0, 12, BENCH)     # 左椅背
wrow(29, 0, 12, BENCH_L)     # 左椅面亮
fl(30, 32, 0, 12, BENCH_D)   # 左椅底暗
fl(26, 28, 51, 63, BENCH)    # 右椅背
wrow(29, 51, 63, BENCH_L)    # 右椅面亮
fl(30, 32, 51, 63, BENCH_D)  # 右椅底暗
# ── 姜饼人（左椅，GCX=16, GCY=21）──
GCX, GCY = 9, 21

# 头（宽7格，四角挖）
for _hy in range(GCY, GCY+5):
    for _hx in range(GCX-3, GCX+4):
        if (_hx, _hy) in [(GCX-3,GCY),(GCX+3,GCY),(GCX-3,GCY+4),(GCX+3,GCY+4)]:
            continue
        sp(_hx, _hy, GB)
# 五官
sp(GCX-1, GCY+1, GB_EYE); sp(GCX+1, GCY+1, GB_EYE)
sp(GCX-2, GCY+2, GB_CHEEK); sp(GCX+2, GCY+2, GB_CHEEK)
sp(GCX-1, GCY+3, GBD); sp(GCX, GCY+3, GBD); sp(GCX+1, GCY+3, GBD)
# 帽子（右偏1格，整体下移1行）
wrow(GCY-1, GCX-1, GCX+3, HAT_RED)
wrow(GCY, GCX-1, GCX+3, HAT_RED)
sp(GCX+1, GCY-2, HAT_DARK)   # 小啾啾
wcol(GCX-1, GCY, GCY, HAT_DARK)
wcol(GCX+3, GCY, GCY, HAT_DARK)
sp(GCX-1, GCY-1, HAT_DARK); sp(GCX, GCY-1, HAT_LITE); sp(GCX+3, GCY-1, HAT_DARK)
# 身体
fl(GCY+5, GCY+8, GCX-2, GCX+2, GB)
sp(GCX, GCY+6, GB_CHEEK); sp(GCX, GCY+8, GB_CHEEK)
# 手臂
sp(GCX-3, GCY+5, GB); sp(GCX-3, GCY+6, GB); sp(GCX-4, GCY+6, GB); sp(GCX-4, GCY+7, GB)
sp(GCX+3, GCY+5, GB); sp(GCX+3, GCY+6, GB); sp(GCX+4, GCY+6, GB); sp(GCX+4, GCY+7, GB)
# 腿
fl(GCY+9, GCY+10, GCX-2, GCX-1, GB)
fl(GCY+9, GCY+10, GCX+1, GCX+2, GB)

# ── 蓝兔子（右椅，BCX=47, BCY=21）──
BCX, BCY = 54, 21

# 耳朵
sp(BCX-1, BCY-4, BUN_B)
for _ey in range(BCY-3, BCY): sp(BCX-2, _ey, BUN_B); sp(BCX-1, _ey, BUN_B)
for _ey in range(BCY-3, BCY): sp(BCX-1, _ey, BUN_IN)
sp(BCX+1, BCY-4, BUN_B)
for _ey in range(BCY-3, BCY): sp(BCX+1, _ey, BUN_B); sp(BCX+2, _ey, BUN_B)
for _ey in range(BCY-3, BCY): sp(BCX+1, _ey, BUN_IN)

# 头（宽7格，四角挖）
for _hy in range(BCY, BCY+5):
    for _hx in range(BCX-3, BCX+4):
        if (_hx, _hy) in [(BCX-3,BCY),(BCX+3,BCY),(BCX-3,BCY+4),(BCX+3,BCY+4)]:
            continue
        sp(_hx, _hy, BUN_B)
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
# 腿
fl(BCY+9, BCY+10, BCX-2, BCX-1, BUN_B)
fl(BCY+9, BCY+10, BCX+1, BCX+2, BUN_B)


img.save('pixel_stanford.png')

# 两侧斜红瓦屋顶（最后画，y=6~8，靠柱x=15顶y=6，靠边x=0顶y=8）
_SRL = (208,108,88); _SRD = (168,78,62); _SR = (188,92,72)
S2 = 12
def sp2(x, y, c):
    px = Image.new('RGB',(S2,S2),c)
    img2.paste(px,(x*S2,y*S2))
img2 = img.copy()
for _wx in range(3, 16):
    _rtop = 7 + round(2 * (15 - _wx) / 12)
    for _wr in range(_rtop, 10):
        _c = _SRL if _wr == _rtop else (_SR if _wr == _rtop+1 else _SRD)
        if _wx % 3 == 1: _c = _SRD
        elif _wx % 3 == 2: _c = _SRL
        sp2(_wx, _wr, _c)
for _wx in range(49, 62):
    _rtop = 9 - round(2 * (61 - _wx) / 12)
    for _wr in range(_rtop, 10):
        _c = _SRL if _wr == _rtop else (_SR if _wr == _rtop+1 else _SRD)
        if _wx % 3 == 1: _c = _SRD
        elif _wx % 3 == 2: _c = _SRL
        sp2(_wx, _wr, _c)
img2.save('pixel_stanford.png')
print('Saved')
