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
SKY_T  = (148, 205, 228)   # 天空上
SKY_B  = (148, 205, 228)   # 天空下（同上）
GROUND = (225, 205, 188)   # 地面（暖沙粉）
BENCH   = (168, 188, 208)   # 石椅冷蓝（同喷泉材质）
BENCH_L = (185, 205, 222)   # 石椅亮冷蓝
BENCH_D = (148, 168, 188)   # 石椅暗冷蓝
LEAF    = ( 78, 138,  98)   # 大树叶主绿
LLEAF   = (135, 158, 118)   # 左侧树叶低饱和
LLEAF_L = (148, 168, 130)   # 左侧树叶低饱和亮
LLEAF_D = (118, 142, 102)   # 左侧树叶低饱和暗
LEAF_L  = ( 92, 152, 112)   # 大树叶亮绿
LEAF_D  = ( 58, 112,  75)   # 大树叶暗绿
SHRUB   = (108, 158,  85)   # 灌木深绿
SHRUB_L = (135, 185, 108)   # 灌木亮绿
SHRUB_D = ( 72, 112,  58)   # 灌木暗绿
GROUND_D = (212, 192, 175)

# 图书馆墙体（斯坦福暖砂岩色）
WALL   = (228, 208, 168)
WALL_D = (215, 198, 155)
WALL_L = (238, 218, 178)
ARCH   = (188, 168, 138)   # 拱廊暗色
WIN    = (152, 185, 178)   # 窗户（动森蓝绿）
WIN_L  = (168, 198, 192)   # 窗户浅蓝绿

# 喷泉
FONT_S = (178, 208, 228)   # 喷泉冷蓝亮
FONT_D = (138, 168, 198)   # 喷泉冷蓝暗
FONT_M = (158, 188, 215)   # 喷泉冷蓝中
WATER  = ( 65, 228, 198)   # 水色
WATER_L= (185, 245, 228)   # 水浅色
SPRAY  = (218, 238, 252)   # 水花

# 椅子（黑色铁艺）
CHAIR  = ( 55,  52,  48)
CHAIR_L= ( 88,  85,  78)

# 角色
GB       = (232, 155,  82)
GBD      = (188, 122,  62)
GB_EYE   = ( 62,  38,  18)
GB_CHEEK = (252, 185, 118)
HAT_RED  = (218,  75,  65)
HAT_DARK = (135,  32,  28)
HAT_LITE = (242, 115,  95)

BUN_B    = (125, 198, 255)
BUN_LIGHT = (168, 218, 255)
BUN_IN   = (255, 225, 235)
BUN_EYE  = ( 35,  55, 105)
BUN_D    = ( 95, 158, 228)

# ── 天空 ──
fl(0, 14, 0, 63, SKY_T)
fl(15, 18, 0, 63, SKY_B)
fl(19, 20, 0, 63, SKY_T)  # y=19~20 天空底色


# 左侧树叶（下移翻转，建筑后）
for _lx, _ly, _lc in [
    (0,24,LLEAF),
    (1,24,LLEAF),
    (2,24,LLEAF),
    (3,24,LLEAF),
    (4,24,LLEAF),
    (5,24,LLEAF),
    (6,24,LLEAF),
    (7,24,LLEAF),
    (8,24,LLEAF),
    (9,24,LLEAF),
    (10,24,LLEAF),
    (11,24,LLEAF),
    (12,24,LLEAF),
    (13,24,LLEAF),
    (14,24,LLEAF),
    (15,24,LLEAF),
    (16,24,LLEAF),
    (17,24,LLEAF),
    (18,24,LLEAF),
    (19,24,LLEAF),
    (20,24,LLEAF),
    (21,24,LLEAF),
    (22,24,LLEAF),
    (0,23,LLEAF),
    (1,23,LLEAF),
    (2,23,LLEAF),
    (3,23,LLEAF),
    (4,23,LLEAF),
    (5,23,LLEAF),
    (6,23,LLEAF),
    (7,23,LLEAF),
    (8,23,LLEAF),
    (9,23,LLEAF),
    (10,23,LLEAF),
    (11,23,LLEAF),
    (12,23,LLEAF),
    (13,23,LLEAF),
    (14,23,LLEAF),
    (15,23,LLEAF),
    (16,23,LLEAF),
    (17,23,LLEAF),
    (18,23,LLEAF),
    (19,23,LLEAF),
    (20,23,LLEAF),
    (21,23,LLEAF),
    (22,23,LLEAF),
    (23,23,LLEAF),
    (24,23,LLEAF),
    (0,22,LLEAF),
    (1,22,LLEAF),
    (2,22,LLEAF),
    (3,22,LLEAF),
    (4,22,LLEAF),
    (5,22,LLEAF),
    (6,22,LLEAF),
    (7,22,LLEAF),
    (8,22,LLEAF),
    (9,22,LLEAF),
    (10,22,LLEAF),
    (11,22,LLEAF),
    (12,22,LLEAF),
    (13,22,LLEAF),
    (14,22,LLEAF),
    (15,22,LLEAF),
    (16,22,LLEAF),
    (17,22,LLEAF),
    (18,22,LLEAF),
    (19,22,LLEAF),
    (20,22,LLEAF),
    (21,22,LLEAF),
    (22,22,LLEAF),
    (23,22,LLEAF),
    (0,21,LLEAF),
    (1,21,LLEAF),
    (2,21,LLEAF),
    (3,21,LLEAF),
    (4,21,LLEAF),
    (5,21,LLEAF),
    (6,21,LLEAF),
    (7,21,LLEAF),
    (8,21,LLEAF),
    (9,21,LLEAF),
    (10,21,LLEAF),
    (11,21,LLEAF),
    (12,21,LLEAF),
    (13,21,LLEAF),
    (14,21,LLEAF),
    (15,21,LLEAF),
    (16,21,LLEAF),
    (17,21,LLEAF),
    (18,21,LLEAF),
    (19,21,LLEAF),
    (20,21,LLEAF),
    (21,21,LLEAF),
    (22,21,LLEAF),
    (23,21,LLEAF),
    (24,21,LLEAF),
    (0,20,LLEAF),
    (1,20,LLEAF),
    (2,20,LLEAF),
    (3,20,LLEAF),
    (4,20,LLEAF),
    (5,20,LLEAF),
    (6,20,LLEAF),
    (7,20,LLEAF),
    (8,20,LLEAF),
    (9,20,LLEAF),
    (10,20,LLEAF),
    (11,20,LLEAF),
    (12,20,LLEAF),
    (13,20,LLEAF),
    (14,20,LLEAF),
    (15,20,LLEAF),
    (16,20,LLEAF),
    (17,20,LLEAF),
    (18,20,LLEAF),
    (19,20,LLEAF),
    (20,20,LLEAF),
    (21,20,LLEAF),
    (22,20,LLEAF),
    (0,19,LLEAF),
    (1,19,LLEAF),
    (2,19,LLEAF),
    (3,19,LLEAF),
    (4,19,LLEAF),
    (5,19,LLEAF),
    (6,19,LLEAF),
    (7,19,LLEAF),
    (8,19,LLEAF),
    (9,19,LLEAF),
    (10,19,LLEAF),
    (11,19,LLEAF),
    (12,19,LLEAF),
    (13,19,LLEAF),
    (14,19,LLEAF),
    (15,19,LLEAF),
    (16,19,LLEAF),
    (17,19,LLEAF),
    (18,19,LLEAF),
    (19,19,LLEAF),
    (20,19,LLEAF),
    (0,18,LLEAF),
    (1,18,LLEAF),
    (2,18,LLEAF),
    (3,18,LLEAF),
    (4,18,LLEAF),
    (5,18,LLEAF),
    (6,18,LLEAF),
    (7,18,LLEAF),
    (8,18,LLEAF),
    (9,18,LLEAF),
    (10,18,LLEAF),
    (11,18,LLEAF),
    (12,18,LLEAF),
    (13,18,LLEAF),
    (14,18,LLEAF),
    (15,18,LLEAF),
    (16,18,LLEAF),
    (17,18,LLEAF),
    (0,17,LLEAF),
    (1,17,LLEAF),
    (2,17,LLEAF),
    (3,17,LLEAF),
    (4,17,LLEAF),
    (5,17,LLEAF),
    (6,17,LLEAF),
    (7,17,LLEAF),
    (8,17,LLEAF),
    (9,17,LLEAF),
    (10,17,LLEAF),
    (11,17,LLEAF),
    (12,17,LLEAF),
    (13,17,LLEAF),
    (14,17,LLEAF),
    (15,17,LLEAF),
    (0,16,LLEAF),
    (1,16,LLEAF),
    (2,16,LLEAF),
    (3,16,LLEAF),
    (4,16,LLEAF),
    (5,16,LLEAF),
    (6,16,LLEAF),
    (7,16,LLEAF),
    (8,16,LLEAF),
    (9,16,LLEAF),
    (10,16,LLEAF),
    (11,16,LLEAF),
    (12,16,LLEAF),
    (0,15,LLEAF),
    (1,15,LLEAF),
    (2,15,LLEAF),
    (3,15,LLEAF),
    (4,15,LLEAF),
    (5,15,LLEAF),
    (6,15,LLEAF),
    (7,15,LLEAF),
    (8,15,LLEAF),
    (9,15,LLEAF),
    (10,15,LLEAF),
    (0,14,LLEAF),
    (1,14,LLEAF),
    (2,14,LLEAF),
    (3,14,LLEAF),
    (4,14,LLEAF),
    (5,14,LLEAF),
    (6,14,LLEAF),
    (7,14,LLEAF),
    (0,13,LLEAF),
    (1,13,LLEAF),
    (2,13,LLEAF),
    (3,13,LLEAF),
    (4,13,LLEAF),
    (0,12,LLEAF),
    (1,12,LLEAF),
    (2,12,LLEAF),
]:
    sp(_lx, _ly, _lc)

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
    (225, 212, 182),  # y=27 最浅暖（跟建筑走）
    (212, 198, 168),  # y=28
    (198, 185, 155),  # y=29
    (182, 168, 138),  # y=30 最深暖
]
for _sw, _sc in enumerate(STEPS):
    _y = 27 + _sw
    _x1 = 18 - _sw - 2
    _x2 = 48 + _sw
    wrow(_y, _x1, _x2, _sc)

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
sp(GCX, GCY+5, GB_CHEEK); sp(GCX, GCY+7, GB_CHEEK)
# 手臂
sp(GCX-3, GCY+5, GB); sp(GCX-3, GCY+6, GB); sp(GCX-4, GCY+6, GB); sp(GCX-4, GCY+7, GB)
sp(GCX+3, GCY+5, GB); sp(GCX+3, GCY+6, GB); sp(GCX+4, GCY+6, GB); sp(GCX+4, GCY+7, GB)
# 腿
fl(GCY+8, GCY+10, GCX-2, GCX-1, GB_CHEEK)
fl(GCY+8, GCY+10, GCX+1, GCX+2, GB_CHEEK)

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
sp(BCX-1, BCY+4, (255,255,255)); sp(BCX, BCY+4, (255,255,255)); sp(BCX+1, BCY+4, (255,255,255))
# 身体
fl(BCY+5, BCY+8, BCX-2, BCX+2, BUN_B)
# 手臂
sp(BCX-3, BCY+5, BUN_B); sp(BCX-3, BCY+6, BUN_B); sp(BCX-4, BCY+6, BUN_B); sp(BCX-4, BCY+7, BUN_B)
sp(BCX+3, BCY+5, BUN_B); sp(BCX+3, BCY+6, BUN_B); sp(BCX+4, BCY+6, BUN_B); sp(BCX+4, BCY+7, BUN_B)
# 腿
fl(BCY+8, BCY+10, BCX-2, BCX-1, BUN_LIGHT)
fl(BCY+8, BCY+10, BCX+1, BCX+2, BUN_LIGHT)







img.save('pixel_stanford.png')

img2 = img.copy()
S2 = 12
def sp2(x, y, c):
    px = Image.new('RGB',(S2,S2),c)
    img2.paste(px,(x*S2,y*S2))
def wrow2(y, x1, x2, c):
    for _x in range(x1, x2+1): sp2(_x, y, c)
def fl2(y1, y2, x1, x2, c):
    for _y in range(y1, y2+1):
        for _x in range(x1, x2+1): sp2(_x, _y, c)
def wcol2(x, y1, y2, c):
    for _y in range(y1, y2+1): sp2(x, _y, c)

# ── 喷泉（中央，CX=32）新版 ──
FX = 32
SPRAY = (185, 245, 228)

# 第一层水盆外缘 x=22~42
fl2(21, 22, 22, 42, FONT_S)
fl2(23, 24, 23, 41, FONT_S)
wrow2(20, 24, 40, FONT_S)
fl2(21, 24, 23, 41, FONT_S)
sp2(23, 21, FONT_D); sp2(27, 21, FONT_D); sp2(32, 21, FONT_D); sp2(37, 21, FONT_D); sp2(41, 21, FONT_D)

# 喷水柱
for _wy in range(18, 20):
    sp2(31, _wy, WATER)
    sp2(32, _wy, WATER_L)
    sp2(33, _wy, WATER)
# 水花
for _wy in [17, 18]:
    _w = 18 - _wy
    for _wx in range(FX-_w, FX+_w+1):
        if abs(_wx - FX) >= _w-1:
            sp2(_wx, _wy, SPRAY)
sp2(FX-2, 18, SPRAY); sp2(FX+2, 18, SPRAY)
sp2(FX-1, 17, SPRAY); sp2(FX, 17, SPRAY); sp2(FX+1, 17, SPRAY)
sp2(FX, 16, SPRAY)

# 底座 x=26~38
fl2(25, 26, 29, 35, FONT_D)
wrow2(25, 27, 37, FONT_S)

# 连接柱 x=29~35
fl2(26, 29, 28, 36, FONT_M)
wcol2(28, 26, 28, FONT_M)
wcol2(36, 26, 28, FONT_M)

# 第二层水盆 x=18~46
fl2(30, 31, 18, 46, FONT_S)
wrow2(32, 20, 44, FONT_S)
wcol2(16, 30, 31, FONT_S)
wcol2(16, 32, 32, FONT_S)
wcol2(17, 30, 32, FONT_S)
wcol2(47, 30, 32, FONT_S)
wcol2(48, 32, 32, FONT_S)
wcol2(48, 30, 31, FONT_S)
fl2(30, 30, 19, 45, WATER)
for _wx in [22, 18, 32, 46, 42]:
    sp2(_wx, 30, WATER_L)

# 第二层底座 x=22~42
fl2(32, 32, 22, 42, FONT_S)
wrow2(32, 23, 41, FONT_S)

for _wx in [23, 27, 32, 37, 41]:
    sp2(_wx, 20, WATER)
# 水流及盆面细节
sp2(18, 25, (65, 228, 198)); sp2(18, 26, (65, 228, 198)); sp2(18, 27, (65, 228, 198))
sp2(18, 28, (65, 228, 198)); sp2(18, 29, (65, 228, 198))
sp2(19, 23, (185, 245, 228)); sp2(19, 24, (65, 228, 198)); sp2(22, 29, (65, 228, 198))
sp2(20, 22, (185, 245, 228))
sp2(21, 21, (185, 245, 228))
sp2(22, 20, FONT_S); sp2(22, 21, (185, 245, 228)); sp2(22, 22, FONT_S)
sp2(22, 26, WATER); sp2(22, 27, WATER); sp2(22, 28, WATER); sp2(22, 29, (65, 228, 198)); sp2(42, 26, WATER); sp2(42, 27, WATER); sp2(42, 28, WATER); sp2(42, 29, (65, 228, 198))
sp2(23, 20, (65, 228, 198)); sp2(23, 22, FONT_S); sp2(23, 23, (185, 245, 228)); sp2(23, 24, (65, 228, 198)); sp2(23, 25, (65, 228, 198))
sp2(24, 22, (185, 245, 228)); sp2(24, 23, FONT_S)
sp2(25, 21, (185, 245, 228)); sp2(25, 22, FONT_S)
sp2(26, 21, (185, 245, 228))
sp2(27, 20, (65, 228, 198))
sp2(26, 25, FONT_S); sp2(38, 25, FONT_S)
sp2(41, 20, (65, 228, 198)); sp2(41, 22, FONT_S); sp2(41, 23, (185, 245, 228)); sp2(41, 24, (65, 228, 198)); sp2(41, 25, (65, 228, 198))
sp2(42, 20, FONT_S); sp2(42, 21, (185, 245, 228)); sp2(42, 22, FONT_S)
sp2(43, 21, (185, 245, 228))
sp2(44, 22, (185, 245, 228))
sp2(45, 23, (185, 245, 228)); sp2(45, 24, (65, 228, 198))
sp2(46, 25, (65, 228, 198)); sp2(46, 26, (65, 228, 198)); sp2(46, 27, (65, 228, 198)); sp2(46, 28, (65, 228, 198)); sp2(46, 29, (65, 228, 198))
sp2(39, 21, (185, 245, 228)); sp2(38, 21, (185, 245, 228))
sp2(40, 22, (185, 245, 228))
sp2(40, 23, FONT_S)
sp2(37, 20, (65, 228, 198))
sp2(32, 22, WATER_L); sp2(32, 23, WATER_L)
sp2(32, 24, WATER); sp2(32, 25, WATER); sp2(32, 26, WATER); sp2(32, 27, WATER); sp2(32, 28, WATER); sp2(32, 29, WATER)

# 喷泉底层
wrow2(32, 18, 46, FONT_S)
sp2(18, 32, FONT_S); sp2(46, 32, FONT_S)



# 两侧斜红瓦屋顶（最后画，y=6~8，靠柱x=15顶y=6，靠边x=0顶y=8）
_SRL = (208,108,88); _SRD = (168,78,62); _SR = (188,92,72)
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
# 右上角大树叶（img2顶层）
for _lx, _ly, _lc in [
    (42,0,LEAF),
    (44,0,LEAF),
    (45,0,LEAF_L),
    (46,0,LEAF),
    (47,0,LEAF),
    (48,0,LEAF_D),
    (49,0,LEAF),
    (50,0,LEAF),
    (51,0,LEAF),
    (52,0,LEAF_L),
    (53,0,LEAF),
    (54,0,LEAF),
    (55,0,LEAF_D),
    (56,0,LEAF),
    (57,0,LEAF),
    (58,0,LEAF_D),
    (59,0,LEAF),
    (60,0,LEAF_D),
    (61,0,LEAF),
    (62,0,LEAF),
    (63,0,LEAF),
    (40,1,LEAF),
    (41,1,LEAF_D),
    (42,1,LEAF),
    (43,1,LEAF),
    (44,1,LEAF_L),
    (45,1,LEAF_L),
    (46,1,LEAF),
    (47,1,LEAF),
    (48,1,LEAF),
    (49,1,LEAF_D),
    (50,1,LEAF_L),
    (51,1,LEAF),
    (52,1,LEAF_D),
    (53,1,LEAF),
    (54,1,LEAF),
    (55,1,LEAF_D),
    (56,1,LEAF),
    (57,1,LEAF_D),
    (58,1,LEAF_D),
    (59,1,LEAF_L),
    (60,1,LEAF),
    (61,1,LEAF),
    (62,1,LEAF),
    (63,1,LEAF_D),
    (38,2,LEAF),
    (39,2,LEAF),
    (40,2,LEAF_L),
    (41,2,LEAF),
    (42,2,LEAF_D),
    (43,2,LEAF),
    (44,2,LEAF_D),
    (45,2,LEAF),
    (46,2,LEAF_D),
    (47,2,LEAF),
    (48,2,LEAF),
    (49,2,LEAF_D),
    (50,2,LEAF_D),
    (51,2,LEAF),
    (52,2,LEAF),
    (53,2,LEAF),
    (54,2,LEAF_D),
    (55,2,LEAF),
    (56,2,LEAF_D),
    (57,2,LEAF),
    (58,2,LEAF_D),
    (59,2,LEAF),
    (60,2,LEAF_L),
    (61,2,LEAF_D),
    (62,2,LEAF_L),
    (63,2,LEAF),
    (38,3,LEAF_L),
    (39,3,LEAF_D),
    (40,3,LEAF_L),
    (41,3,LEAF),
    (42,3,LEAF),
    (43,3,LEAF),
    (44,3,LEAF),
    (45,3,LEAF),
    (46,3,LEAF),
    (47,3,LEAF_D),
    (48,3,LEAF),
    (49,3,LEAF_D),
    (50,3,LEAF_L),
    (51,3,LEAF),
    (52,3,LEAF_L),
    (53,3,LEAF),
    (54,3,LEAF_D),
    (55,3,LEAF),
    (56,3,LEAF),
    (57,3,LEAF_D),
    (58,3,LEAF_L),
    (59,3,LEAF),
    (60,3,LEAF),
    (61,3,LEAF),
    (62,3,LEAF_L),
    (63,3,LEAF_L),
    (40,4,LEAF_L),
    (41,4,LEAF),
    (42,4,LEAF),
    (43,4,LEAF),
    (44,4,LEAF),
    (45,4,LEAF),
    (46,4,LEAF_D),
    (47,4,LEAF_D),
    (48,4,LEAF),
    (49,4,LEAF),
    (50,4,LEAF),
    (51,4,LEAF_D),
    (52,4,LEAF_L),
    (53,4,LEAF_D),
    (54,4,LEAF_L),
    (55,4,LEAF),
    (56,4,LEAF),
    (57,4,LEAF),
    (58,4,LEAF_L),
    (59,4,LEAF),
    (60,4,LEAF),
    (61,4,LEAF),
    (62,4,LEAF_D),
    (63,4,LEAF_L),
    (41,5,LEAF),
    (42,5,LEAF_L),
    (43,5,LEAF_L),
    (44,5,LEAF_L),
    (45,5,LEAF),
    (46,5,LEAF),
    (47,5,LEAF_L),
    (48,5,LEAF_L),
    (49,5,LEAF_D),
    (50,5,LEAF),
    (51,5,LEAF_L),
    (52,5,LEAF),
    (53,5,LEAF),
    (54,5,LEAF_L),
    (55,5,LEAF),
    (56,5,LEAF),
    (57,5,LEAF_D),
    (58,5,LEAF),
    (59,5,LEAF_L),
    (60,5,LEAF),
    (61,5,LEAF),
    (62,5,LEAF),
    (63,5,LEAF),
    (43,6,LEAF),
    (44,6,LEAF),
    (45,6,LEAF),
    (46,6,LEAF_L),
    (47,6,LEAF_L),
    (48,6,LEAF_L),
    (49,6,LEAF),
    (50,6,LEAF),
    (51,6,LEAF_L),
    (52,6,LEAF_L),
    (53,6,LEAF_D),
    (54,6,LEAF),
    (55,6,LEAF),
    (56,6,LEAF_L),
    (57,6,LEAF_D),
    (58,6,LEAF),
    (59,6,LEAF_L),
    (60,6,LEAF),
    (61,6,LEAF_L),
    (62,6,LEAF),
    (63,6,LEAF),
    (38,7,LEAF),
    (39,7,LEAF),
    (40,7,LEAF),
    (41,7,LEAF),
    (42,7,LEAF),
    (43,7,LEAF),
    (44,7,LEAF_L),
    (45,7,LEAF_D),
    (46,7,LEAF),
    (47,7,LEAF),
    (48,7,LEAF),
    (49,7,LEAF),
    (50,7,LEAF),
    (51,7,LEAF_L),
    (52,7,LEAF_D),
    (53,7,LEAF),
    (54,7,LEAF_D),
    (55,7,LEAF_D),
    (56,7,LEAF),
    (57,7,LEAF),
    (58,7,LEAF_D),
    (59,7,LEAF_D),
    (60,7,LEAF),
    (61,7,LEAF_L),
    (62,7,LEAF_D),
    (63,7,LEAF_L),
    (33,8,LEAF_L),
    (34,8,LEAF_L),
    (35,8,LEAF_L),
    (36,8,LEAF),
    (37,8,LEAF_L),
    (38,8,LEAF_L),
    (39,8,LEAF),
    (40,8,LEAF),
    (41,8,LEAF),
    (42,8,LEAF),
    (43,8,LEAF_L),
    (44,8,LEAF),
    (45,8,LEAF),
    (46,8,LEAF),
    (47,8,LEAF_D),
    (48,8,LEAF),
    (49,8,LEAF),
    (50,8,LEAF),
    (51,8,LEAF_D),
    (52,8,LEAF),
    (53,8,LEAF_D),
    (54,8,LEAF),
    (55,8,LEAF),
    (56,8,LEAF_D),
    (57,8,LEAF),
    (58,8,LEAF),
    (59,8,LEAF),
    (60,8,LEAF_D),
    (61,8,LEAF_L),
    (62,8,LEAF),
    (63,8,LEAF),
    (33,9,LEAF),
    (34,9,LEAF_D),
    (35,9,LEAF),
    (36,9,LEAF_L),
    (37,9,LEAF),
    (38,9,LEAF),
    (39,9,LEAF_L),
    (40,9,LEAF_L),
    (41,9,LEAF_L),
    (42,9,LEAF_L),
    (43,9,LEAF),
    (44,9,LEAF),
    (45,9,LEAF),
    (46,9,LEAF),
    (47,9,LEAF),
    (48,9,LEAF),
    (49,9,LEAF_L),
    (50,9,LEAF),
    (51,9,LEAF_D),
    (52,9,LEAF),
    (53,9,LEAF),
    (54,9,LEAF_D),
    (55,9,LEAF),
    (56,9,LEAF),
    (57,9,LEAF_D),
    (58,9,LEAF),
    (59,9,LEAF_D),
    (60,9,LEAF),
    (61,9,LEAF),
    (62,9,LEAF),
    (63,9,LEAF_D),
    (40,10,LEAF),
    (41,10,LEAF),
    (42,10,LEAF),
    (43,10,LEAF),
    (44,10,LEAF_D),
    (45,10,LEAF_D),
    (46,10,LEAF_D),
    (47,10,LEAF),
    (48,10,LEAF),
    (49,10,LEAF_D),
    (50,10,LEAF),
    (51,10,LEAF),
    (52,10,LEAF_L),
    (53,10,LEAF),
    (54,10,LEAF),
    (55,10,LEAF_D),
    (56,10,LEAF_L),
    (57,10,LEAF),
    (58,10,LEAF),
    (59,10,LEAF),
    (60,10,LEAF),
    (61,10,LEAF_L),
    (62,10,LEAF),
    (63,10,LEAF),
    (48,11,LEAF_D),
    (49,11,LEAF),
    (50,11,LEAF_L),
    (51,11,LEAF),
    (52,11,LEAF),
    (53,11,LEAF),
    (54,11,LEAF),
    (55,11,LEAF),
    (56,11,LEAF),
    (57,11,LEAF_L),
    (58,11,LEAF),
    (59,11,LEAF),
    (60,11,LEAF),
    (61,11,LEAF_L),
    (62,11,LEAF_D),
    (63,11,LEAF_D),
    (52,12,LEAF),
    (53,12,LEAF_L),
    (54,12,LEAF),
    (55,12,LEAF),
    (56,12,LEAF),
    (57,12,LEAF_L),
    (58,12,LEAF),
    (59,12,LEAF_L),
    (60,12,LEAF),
    (61,12,LEAF_L),
    (62,12,LEAF),
    (63,12,LEAF),
    (49,13,LEAF),
    (50,13,LEAF),
    (51,13,LEAF),
    (52,13,LEAF),
    (53,13,LEAF),
    (54,13,LEAF),
    (55,13,LEAF_D),
    (56,13,LEAF_L),
    (57,13,LEAF),
    (58,13,LEAF_D),
    (59,13,LEAF_D),
    (60,13,LEAF_L),
    (61,13,LEAF),
    (62,13,LEAF),
    (63,13,LEAF_D),
    (52,14,LEAF_D),
    (53,14,LEAF),
    (54,14,LEAF),
    (55,14,LEAF),
    (56,14,LEAF),
    (57,14,LEAF_D),
    (58,14,LEAF),
    (59,14,LEAF_L),
    (60,14,LEAF),
    (61,14,LEAF),
    (62,14,LEAF),
    (63,14,LEAF),
    (57,15,LEAF),
    (58,15,LEAF),
    (59,15,LEAF_D),
    (60,15,LEAF),
    (61,15,LEAF_D),
    (62,15,LEAF),
    (63,15,LEAF),
    (62,16,LEAF_D),
    (63,16,LEAF_L),
]:
    sp2(_lx, _ly, _lc)
img2.save('pixel_stanford.png')
print('Saved')
