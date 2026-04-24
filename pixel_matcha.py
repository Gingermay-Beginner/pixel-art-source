from PIL import Image

W, H, S = 64, 36, 12
img = Image.new("RGB", (W*S, H*S), (255,255,255))
px = img.load()

def sp(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        for dy in range(S):
            for dx in range(S):
                px[x*S+dx, y*S+dy] = c

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
WALL     = (238, 228, 212)
WALL_D   = (212, 200, 182)
SKY      = (195, 225, 248)
FLOOR    = (178, 152, 108)   # 蜂蜜暖木
FLOOR_D  = (152, 128,  88)
FLOOR_L  = (198, 175, 128)

# 俯视桌面（奶油暖白）
TABLE    = (118, 108,  95)
TABLE_D  = ( 98,  88,  78)
TABLE_E  = ( 82,  72,  62)

# 后台架子
SHELF    = (215, 192, 152)   # 奶油暖木
SHELF_D  = (188, 162, 122)

MATCHA   = ( 88, 148,  72)
MATCHA_L = (118, 178,  95)
MATCHA_F = (148, 198, 118)
FOAM     = (198, 228, 168)  # 泡沫亮点
CUP_W    = (245, 248, 252)
STRAW    = (178, 158, 118)
SYRUP    = (225,  80, 100)
SYRUP_L  = (245, 140, 155)
MANGO    = (235, 148,  45)
MANGO_L  = (248, 198,  95)
CUP_T    = (148, 188, 218)   # 杯盖（加深蓝，更显眼）
ICE      = (215, 235, 248)
MILK     = (248, 245, 238)
MILK_D   = (215, 210, 200)

SYR_CO   = (228, 195, 148)
SYR_MG   = (235, 178,  72)
SYR_PS   = (228, 118,  88)
SYR_ST   = (215,  72,  88)
SYR_BL   = ( 88, 115, 195)

CAP_DARK = (245, 242, 235)   # 瓶盖深色
WHISK    = (208, 192,  95)
WHISK_D  = (168, 152,  68)
BOWL_W   = (238, 232, 220)
BOWL_D   = (205, 198, 182)

ICE_BK   = (175, 192, 208)
ICE_BK_D = (148, 168, 188)
MATCHA_TIN = ( 72, 128,  58)
MATCHA_TD  = ( 52, 105,  42)

GB       = (185, 108,  48)
GBD      = (140,  82,  35)
GB_EYE   = ( 62,  35,  15)
GB_CHEEK = (225, 148,  95)
HAT_RED  = (188,  55,  48)
HAT_DARK = (135,  32,  28)
HAT_LITE = (215,  88,  72)

BUN_B    = ( 88, 158, 228)
BUN_IN   = (215, 148, 168)
BUN_EYE  = ( 35,  55, 105)
BUN_D    = ( 62, 118, 188)

# ── 背景 ──
# 橘黄色方格瓷砖墙
TILE_A = (228, 185, 118)   # 主色（偏黄米，远离橙）
TILE_B = (218, 192, 142)   # 暗格（微暗，低调）
TILE_G = (238, 200, 138)   # 缝隙（比主色亮，柔和）
TILE_W = 4                  # 每块瓷砖宽/高（格子单位）
fl(0, 18, 0, 63, TILE_A)
# 缝隙（竖向）
for tx in range(0, 64, TILE_W):
    wcol(tx, 0, 18, TILE_G)
# 缝隙（横向）
for ty in range(0, 19, TILE_W):
    wrow(ty, 0, 63, TILE_G)
# 暗格（交错）
import random as _r2; _rng2 = _r2.Random(33)
for ty in range(0, 18, TILE_W):
    for tx in range(0, 63, TILE_W):
        if _rng2.random() < 0.3:
            fl(ty+1, ty+TILE_W-1, tx+1, tx+TILE_W-1, TILE_B)

# 地板（桌子下方可见）
fl(19, 35, 0, 63, FLOOR)
for row in range(20, 36, 3):
    wrow(row, 0, 63, FLOOR_L)
for row in range(22, 36, 3):
    wrow(row, 0, 63, FLOOR_D)

# ── 墙上架子（y=9~10, x=2~61）──
fl(10, 11, 2, 61, SHELF)
wrow(11, 2, 61, SHELF_D)
wrow(11, 2, 61, SHELF_D)

# 架子上物品：3个牛奶盒（尖顶） + 抹茶粉罐
# 牛奶盒（x=5~8, 10~13, 15~18），盒体 y=3~9，尖顶
for mx in [5, 10, 15]:
    fl(3, 9, mx, mx+3, MILK)
    wcol(mx, 3, 9, MILK_D)
    wcol(mx+3, 3, 9, MILK_D)
    wrow(9, mx, mx+3, MILK_D)
    sp(mx+1, 2, MILK); sp(mx+2, 2, MILK)
    sp(mx+1, 1, MILK); sp(mx+2, 1, MILK)
    sp(mx, 2, MILK_D); sp(mx+3, 2, MILK_D)
    sp(mx+1, 0, MILK_D)

# 抹茶粉罐（x=30~33, y=3~9，居中）

# 冰桶（右边，x=50~57, y=3~9）
fl(3, 9, 50, 57, ICE_BK)
fl(4, 8, 51, 56, ICE)
sp(51, 5, CUP_W); sp(53, 6, CUP_W); sp(55, 5, CUP_W)
wcol(50, 3, 9, ICE_BK_D)
wcol(57, 3, 9, ICE_BK_D)
wrow(9, 50, 57, ICE_BK_D)
sp(49, 3, ICE_BK_D); sp(58, 3, ICE_BK_D)

# ── 俯视桌面（y=19~35, x=4~59）──
fl(18, 35, 0, 63, TABLE)
# 杂质点（随机散布，模拟混凝土质感）
import random; _rng = random.Random(77)
GRAIN = [(128,118,105),(105,95,85),(138,128,115)]
for _ in range(200):
    gx = _rng.randint(1, 62); gy = _rng.randint(19, 35)
    sp(gx, gy, _rng.choice(GRAIN))

fl(28, 34, 38, 45, MATCHA_TIN)
wrow(27, 38, 45, MATCHA_TD)
wrow(34, 38, 45, MATCHA_TD)
wcol(38, 28, 34, MATCHA_TD)
wcol(45, 28, 34, MATCHA_TD)
sp(40, 30, MATCHA_F); sp(41, 30, MATCHA_F); sp(42, 30, MATCHA_F); sp(43, 30, MATCHA_F); sp(44, 30, MATCHA_F)
sp(40, 31, MATCHA_F); sp(41, 31, MATCHA_F); sp(42, 31, MATCHA_F); sp(43, 31, MATCHA_F); sp(44, 31, MATCHA_F)
# 桌边（上边 = 近景前缘）

GCX, GCY = 20, 3
# 头（9宽）
# 头（四角挖代码圆角）
wrow(GCY+3, GCX-3, GCX+3, GB)
fl(GCY+4, GCY+7, GCX-4, GCX+4, GB)
wrow(GCY+8, GCX-3, GCX+3, GB)
sp(GCX-2, GCY+5, GB_EYE); sp(GCX+2, GCY+5, GB_EYE)
sp(GCX-3, GCY+6, GB_CHEEK); sp(GCX+3, GCY+6, GB_CHEEK)
sp(GCX-1, GCY+7, GBD); sp(GCX, GCY+7, GBD); sp(GCX+1, GCY+7, GBD)
# 脖子
sp(GCX-2, GCY+9, GB); sp(GCX-1, GCY+9, GB); sp(GCX, GCY+9, GB); sp(GCX+1, GCY+9, GB); sp(GCX+2, GCY+9, GB)
# 帽子（右移1格，下移1格，顶行挖圆角）
wrow(GCY+1, GCX-1, GCX+3, HAT_RED)
fl(GCY+2, GCY+3, GCX-2, GCX+4, HAT_RED)
sp(GCX+1, GCY, HAT_DARK)
wcol(GCX-2, GCY+2, GCY+3, HAT_DARK)
wcol(GCX+4, GCY+2, GCY+3, HAT_DARK)
sp(GCX-1, GCY+1, HAT_DARK); sp(GCX, GCY+1, HAT_LITE); sp(GCX+3, GCY+1, HAT_DARK)
# 身体（藏桌后）
fl(GCY+10, GCY+14, GCX-2, GCX+2, GB)
sp(GCX, GCY+11, GB_CHEEK); sp(GCX, GCY+13, GB_CHEEK)
# 手臂伸向茶器（2格宽，肩膀圆角）
sp(GCX-3, GCY+10, GB)
for _ay in range(GCY+11, GCY+18):
    sp(GCX-3, _ay, GB); sp(GCX-4, _ay, GB)
sp(GCX+3, GCY+10, GB)
for _ay in range(GCY+11, GCY+18):
    sp(GCX+3, _ay, GB); sp(GCX+4, _ay, GB)
# 左臂延伸 x=13，右臂延伸 x=23（镜像）
sp(GCX-5, GCY+16, GB); sp(GCX-5, GCY+17, GB)
sp(GCX+5, GCY+16, GB); sp(GCX+5, GCY+17, GB)

# ── 蓝兔子（右，x=38~48, y=2~18）──
BCX, BCY = 45, 5
# 耳朵（左）顶部1格圆角在内侧
sp(BCX-1, BCY-3, BUN_B)
for _ey in range(BCY-2, BCY+1): sp(BCX-2, _ey, BUN_B); sp(BCX-1, _ey, BUN_B)
# 左耳内芯
for _ey in range(BCY-2, BCY): sp(BCX-1, _ey, BUN_IN)
# 耳朵（右）顶部1格圆角在内侧
sp(BCX+1, BCY-3, BUN_B)
for _ey in range(BCY-2, BCY+1): sp(BCX+1, _ey, BUN_B); sp(BCX+2, _ey, BUN_B)
# 右耳内芯
for _ey in range(BCY-2, BCY): sp(BCX+1, _ey, BUN_IN)
# 耳朵间底部
sp(BCX, BCY, BUN_B)
# 头（9宽，四角挖代码圆角）
wrow(BCY+1, BCX-3, BCX+3, BUN_B)
fl(BCY+2, BCY+5, BCX-4, BCX+4, BUN_B)
wrow(BCY+6, BCX-3, BCX+3, BUN_B)
for bx in [BCX-3, BCX-2, BCX-1]: sp(bx, BCY+2, BUN_EYE)
sp(BCX, BCY+2, BUN_D)
for bx in [BCX+1, BCX+2, BCX+3]: sp(bx, BCY+2, BUN_EYE)
sp(BCX-2, BCY+3, BUN_EYE); sp(BCX+2, BCY+3, BUN_EYE)
sp(BCX-3, BCY+4, BUN_IN); sp(BCX+3, BCY+4, BUN_IN)
# 嘴
sp(BCX-1, BCY+5, (245,240,235)); sp(BCX, BCY+5, (245,240,235)); sp(BCX+1, BCY+5, (245,240,235))
sp(BCX-1, BCY+6, BUN_B); sp(BCX, BCY+6, BUN_B); sp(BCX+1, BCY+6, BUN_B)
# 脖子
sp(BCX-2, BCY+7, BUN_B); sp(BCX-1, BCY+7, BUN_B); sp(BCX, BCY+7, BUN_B); sp(BCX+1, BCY+7, BUN_B); sp(BCX+2, BCY+7, BUN_B)
# 身体（藏桌后）
fl(BCY+8, BCY+12, BCX-2, BCX+2, BUN_B)
# 手臂伸向茶器（2格宽，肩膀圆角=外列从+1行开始）
sp(BCX-3, BCY+8, BUN_B)
for _ay in range(BCY+9, BCY+16):
    sp(BCX-3, _ay, BUN_B); sp(BCX-4, _ay, BUN_B)
sp(BCX+3, BCY+8, BUN_B)
for _ay in range(BCY+9, BCY+16):
    sp(BCX+3, _ay, BUN_B); sp(BCX+4, _ay, BUN_B)
# 两臂延伸（镜像）
sp(BCX-5, BCY+14, BUN_B); sp(BCX-5, BCY+15, BUN_B)
sp(BCX+5, BCY+14, BUN_B); sp(BCX+5, BCY+15, BUN_B)

# ── 桌上物品（俯视桌面上，侧视物品）──

# 5个糖浆瓶（底部居中，x=20~44, y=28~35）
syrup_colors = [SYR_CO, SYR_MG, SYR_PS, SYR_ST, SYR_BL]
for i, sc in enumerate(syrup_colors):
    bx = 2 + i*5
    fl(28, 32, bx, bx+3, sc)
    fl(33, 34, bx+1, bx+2, sc)
    sp(bx+1, 34, (245, 242, 235)); sp(bx+2, 34, (245, 242, 235))
    wcol(bx+3, 28, 32, (max(0,sc[0]-35), max(0,sc[1]-35), max(0,sc[2]-35)))
    # 瓶盖
    wrow(28, bx, bx+3, CAP_DARK)
    sp(bx+1, 27, CAP_DARK); sp(bx+2, 27, CAP_DARK)

# 抹茶碗（x=41~48, y=19~24，下移2格）
fl(20, 24, 43, 50, BOWL_W)
wrow(19, 44, 49, BOWL_D)
wcol(43, 20, 24, BOWL_D)
wcol(50, 20, 24, BOWL_D)
fl(20, 22, 44, 49, MATCHA)
wrow(20, 44, 49, MATCHA_F)
# 泡沫点
sp(44,20,FOAM); sp(46,20,FOAM); sp(48,20,FOAM)
sp(45,21,FOAM); sp(47,21,FOAM); sp(49,21,FOAM)
sp(44,22,FOAM); sp(46,22,FOAM); sp(48,22,FOAM)
# 碗底座
wrow(25, 45, 48, BOWL_D)
# 碗口右侧尖嘴（镜像）
sp(51, 21, BOWL_D)
sp(50, 21, MATCHA)

# 茶筅（右移2格，y=18~25）
sp(40,18,WHISK); sp(41,18,WHISK)
sp(40,19,WHISK); sp(41,19,WHISK_D)
sp(40,20,WHISK); sp(41,20,WHISK_D)
sp(39,21,WHISK_D); sp(40,21,WHISK); sp(41,21,WHISK_D); sp(42,21,WHISK)
sp(39,22,WHISK_D); sp(40,22,WHISK); sp(41,22,WHISK_D); sp(42,22,WHISK)
sp(38,23,WHISK); sp(39,23,WHISK_D); sp(40,23,WHISK); sp(41,23,WHISK_D); sp(42,23,WHISK); sp(43,23,WHISK_D)
sp(38,24,WHISK_D); sp(39,24,WHISK); sp(40,24,WHISK_D); sp(41,24,WHISK); sp(42,24,WHISK_D); sp(43,24,WHISK)
sp(38,25,WHISK_D); sp(39,25,WHISK); sp(40,25,WHISK_D); sp(41,25,WHISK); sp(42,25,WHISK_D); sp(43,25,WHISK)


# 草莓抹茶杯（左，cx=5，x=3~7，内移3格）
wcol(8, 12, 17, STRAW)
wrow(16, 6, 9, CUP_T)
wrow(17, 5, 10, CUP_T)
fl(23, 25, 6, 9, SYRUP)
wrow(23, 6, 9, SYRUP_L)
fl(21, 22, 6, 9, MILK)
fl(18, 20, 6, 9, MATCHA_L)
wrow(18, 6, 9, MATCHA)
sp(8, 19, ICE); sp(9, 19, ICE)
sp(6, 20, ICE); sp(6, 21, ICE)
sp(8, 21, ICE)

# 芒果抹茶杯（右，cx=58，x=56~60，内移3格）
wcol(55, 12, 17, STRAW)
wrow(16, 54, 57, CUP_T)
wrow(17, 53, 58, CUP_T)
fl(23, 25, 54, 57, MANGO)
wrow(23, 54, 57, MANGO_L)
fl(21, 22, 54, 57, MILK)
fl(18, 20, 54, 57, MATCHA_L)
wrow(18, 54, 57, MATCHA)
sp(54, 19, ICE); sp(55, 19, ICE)
sp(57, 20, ICE); sp(57, 21, ICE)
sp(55, 21, ICE)

# ── 姜饼人（左，x=16~26, y=3~18）──

# 姜饼人面前茶器（右移4格，碗x=18~25）
fl(20, 24, 18, 25, BOWL_W)
wrow(19, 19, 24, BOWL_D)
wcol(18, 20, 24, BOWL_D)
wcol(25, 20, 24, BOWL_D)
fl(20, 22, 19, 24, MATCHA)
wrow(20, 19, 24, MATCHA_F)
# 泡沫点
sp(19,20,FOAM); sp(21,20,FOAM); sp(23,20,FOAM)
sp(20,21,FOAM); sp(22,21,FOAM); sp(24,21,FOAM)
sp(19,22,FOAM); sp(21,22,FOAM); sp(23,22,FOAM)
# 碗底座
wrow(25, 20, 23, BOWL_D)
# 碗口右侧尖嘴
sp(26, 21, BOWL_D)
sp(25, 21, MATCHA)
# 茶筅（右移2格，y=18~25）
sp(15,18,WHISK); sp(16,18,WHISK)
sp(15,19,WHISK); sp(16,19,WHISK_D)
sp(15,20,WHISK); sp(16,20,WHISK_D)
sp(14,21,WHISK_D); sp(15,21,WHISK); sp(16,21,WHISK_D); sp(17,21,WHISK)
sp(14,22,WHISK_D); sp(15,22,WHISK); sp(16,22,WHISK_D); sp(17,22,WHISK)
sp(13,23,WHISK); sp(14,23,WHISK_D); sp(15,23,WHISK); sp(16,23,WHISK_D); sp(17,23,WHISK); sp(18,23,WHISK_D)
sp(13,24,WHISK_D); sp(14,24,WHISK); sp(15,24,WHISK_D); sp(16,24,WHISK); sp(17,24,WHISK_D); sp(18,24,WHISK)
sp(13,25,WHISK_D); sp(14,25,WHISK); sp(15,25,WHISK_D); sp(16,25,WHISK); sp(17,25,WHISK_D); sp(18,25,WHISK)
print(f"Saved: {W*S}x{H*S}px")

# ── 大凉水杯（x=29~35，居中，底部 y=35）──
PITCHER_G = (205, 228, 242)
PITCHER_W = (235, 245, 252)
PITCHER_D = (168, 195, 215)
WATER_C   = (148, 205, 235)

fl(23, 34, 28, 34, PITCHER_G)
fl(25, 34, 29, 33, WATER_C)
wcol(28, 23, 34, PITCHER_D)
wcol(34, 23, 34, PITCHER_D)
wrow(34, 28, 34, PITCHER_D)
wcol(29, 23, 34, PITCHER_W)
wrow(22, 28, 34, PITCHER_D)
wrow(23, 28, 34, PITCHER_G)
sp(29, 25, CUP_W); sp(31, 26, CUP_W); sp(33, 25, CUP_W)
sp(30, 28, CUP_W); sp(32, 29, CUP_W)
sp(35, 26, PITCHER_D); sp(35, 30, PITCHER_D)
sp(36, 26, PITCHER_D); sp(36, 27, PITCHER_D)
sp(36, 28, PITCHER_D)
sp(36, 29, PITCHER_D); sp(36, 30, PITCHER_D)

# ── 吸管筒（x=51~55, y=22~31）──
HOLDER   = ( 72,  58,  48)
HOLDER_L = ( 95,  78,  62)
STRAW_R  = (215,  88,  72)

fl(31, 34, 47, 51, HOLDER)
wcol(47, 31, 34, HOLDER_L)
wrow(30, 47, 51, HOLDER)
wrow(34, 47, 51, HOLDER)
sp(48, 27, STRAW); sp(48, 28, STRAW); sp(48, 29, STRAW); sp(48, 30, STRAW)
sp(49, 27, STRAW_R); sp(49, 28, STRAW_R); sp(49, 29, STRAW_R); sp(49, 30, STRAW_R)
sp(50, 27, STRAW); sp(50, 28, STRAW); sp(50, 29, STRAW); sp(50, 30, STRAW)


# ── 餐巾纸叠（右下角，x=55~61, y=29~34）──
NAPKIN   = (252, 250, 244)
NAPKIN_D = (225, 220, 210)
NAPKIN_S = (205, 200, 188)

fl(32, 34, 55, 61, NAPKIN)
wrow(31, 55, 61, NAPKIN_D)
wcol(55, 32, 34, NAPKIN_D)
wcol(61, 32, 34, NAPKIN_D)
wrow(34, 55, 61, NAPKIN_S)
fl(30, 32, 56, 60, NAPKIN)
wrow(29, 56, 60, NAPKIN_D)
wcol(56, 30, 32, NAPKIN_D)
wcol(60, 30, 32, NAPKIN_D)
fl(28, 30, 57, 59, NAPKIN)
wrow(27, 57, 59, NAPKIN_D)
wcol(57, 28, 30, NAPKIN_D)
wcol(59, 28, 30, NAPKIN_D)


img.save("pixel_matcha.png")
