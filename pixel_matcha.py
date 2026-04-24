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
WALL     = (225, 218, 205)
WALL_D   = (198, 190, 175)
SKY      = (235, 240, 248)
FLOOR    = (198, 182, 158)
FLOOR_D  = (175, 158, 132)
FLOOR_L  = (218, 205, 182)

# 俯视桌面（暖木色，参考 Bagel Day）
TABLE    = (188, 162, 118)
TABLE_D  = (168, 142,  98)
TABLE_E  = (138, 112,  72)

# 后台架子
SHELF    = (212, 200, 178)
SHELF_D  = (185, 172, 148)

MATCHA   = ( 88, 148,  72)
MATCHA_L = (118, 178,  95)
MATCHA_F = (148, 198, 118)
CUP_W    = (245, 248, 252)
STRAW    = (228, 218, 198)
SYRUP    = (225,  80, 100)
SYRUP_L  = (245, 140, 155)
MANGO    = (235, 148,  45)
MANGO_L  = (248, 198,  95)
CUP_T    = (195, 215, 232)
ICE      = (215, 235, 248)
MILK     = (248, 245, 238)
MILK_D   = (215, 210, 200)

SYR_CO   = (228, 195, 148)
SYR_MG   = (235, 178,  72)
SYR_PS   = (228, 118,  88)
SYR_ST   = (215,  72,  88)
SYR_BL   = ( 88, 115, 195)

WHISK    = (148, 118,  72)
WHISK_D  = (108,  82,  48)
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
BUN_IN   = (228, 185, 195)
BUN_EYE  = ( 35,  55, 105)
BUN_D    = ( 62, 118, 188)

# ── 背景 ──
fl(0, 18, 0, 63, WALL)

# 窗（两扇）
fl(1, 16, 2, 22, SKY)
fl(1, 16, 40, 61, SKY)
for wx1, wx2 in [(2,22),(40,61)]:
    wrow(0, wx1, wx2, WALL_D)
    wrow(17, wx1, wx2, WALL_D)
    wcol(wx1-1, 1, 16, WALL_D)
    wcol(wx2+1, 1, 16, WALL_D)

# 地板（桌子下方可见）
fl(19, 35, 0, 63, FLOOR)
for row in range(20, 36, 3):
    wrow(row, 0, 63, FLOOR_L)
for row in range(22, 36, 3):
    wrow(row, 0, 63, FLOOR_D)

# ── 后台架子（y=16~18, x=4~59）──
fl(16, 18, 4, 59, SHELF)
wrow(16, 4, 59, SHELF_D)
wrow(18, 4, 59, SHELF_D)

# 架子上物品：3个牛奶盒 + 冰桶 + 抹茶粉罐
# 牛奶盒（x=5~8, 10~13, 15~18）
for mx in [5, 10, 15]:
    fl(12, 15, mx, mx+3, MILK)
    wcol(mx, 12, 15, MILK_D)
    wcol(mx+3, 12, 15, MILK_D)
    wrow(15, mx, mx+3, MILK_D)
    sp(mx+1, 11, MILK); sp(mx+2, 11, MILK)
    sp(mx, 12, MILK_D); sp(mx+3, 12, MILK_D)
    sp(mx+1, 10, MILK); sp(mx+2, 10, MILK)

# 冰桶（x=21~26, y=10~15）
fl(10, 15, 21, 26, ICE_BK)
fl(11, 14, 22, 25, ICE)
sp(22, 12, CUP_W); sp(24, 13, CUP_W)
wcol(21, 10, 15, ICE_BK_D)
wcol(26, 10, 15, ICE_BK_D)
wrow(15, 21, 26, ICE_BK_D)
sp(20, 10, ICE_BK_D); sp(27, 10, ICE_BK_D)

# 抹茶粉罐（x=29~32, y=11~15）
fl(11, 15, 29, 32, MATCHA_TIN)
wrow(10, 29, 32, MATCHA_TD)
wcol(29, 11, 15, MATCHA_TD)
wcol(32, 11, 15, MATCHA_TD)
sp(30, 13, MATCHA_F); sp(31, 13, MATCHA_F)

# ── 俯视桌面（y=19~35, x=4~59）──
fl(19, 35, 0, 63, TABLE)
# 木纹（横向）
for row in range(21, 36, 4):
    wrow(row, 0, 63, TABLE_D)
# 桌边（上边 = 近景前缘）

# ── 桌上物品（俯视桌面上，侧视物品）──

# 5个糖浆瓶（底部居中，x=20~44, y=28~35）
syrup_colors = [SYR_CO, SYR_MG, SYR_PS, SYR_ST, SYR_BL]
for i, sc in enumerate(syrup_colors):
    bx = 20 + i*5
    fl(28, 32, bx, bx+3, sc)
    fl(33, 34, bx+1, bx+2, sc)
    sp(bx+1, 35, WALL_D); sp(bx+2, 35, WALL_D)
    wcol(bx+3, 28, 32, (max(0,sc[0]-35), max(0,sc[1]-35), max(0,sc[2]-35)))

# 抹茶碗（x=41~48, y=19~24，下移2格）
fl(20, 24, 41, 48, BOWL_W)
wrow(19, 42, 47, BOWL_D)
wcol(41, 20, 24, BOWL_D)
wcol(48, 20, 24, BOWL_D)
fl(20, 22, 42, 47, MATCHA)
wrow(20, 42, 47, MATCHA_F)
# 碗底座
wrow(25, 43, 46, BOWL_D)
# 碗口右侧尖嘴（镜像）
sp(49, 21, BOWL_D)
sp(48, 21, MATCHA)

# 茶筅（下移2格，y=18~25）
sp(38,18,WHISK); sp(39,18,WHISK)
sp(38,19,WHISK); sp(39,19,WHISK_D)
sp(38,20,WHISK); sp(39,20,WHISK_D)
sp(37,21,WHISK_D); sp(38,21,WHISK); sp(39,21,WHISK_D); sp(40,21,WHISK)
sp(37,22,WHISK_D); sp(38,22,WHISK); sp(39,22,WHISK_D); sp(40,22,WHISK)
sp(36,23,WHISK); sp(37,23,WHISK_D); sp(38,23,WHISK); sp(39,23,WHISK_D); sp(40,23,WHISK); sp(41,23,WHISK_D)
sp(36,24,WHISK_D); sp(37,24,WHISK); sp(38,24,WHISK_D); sp(39,24,WHISK); sp(40,24,WHISK_D); sp(41,24,WHISK)
sp(36,25,WHISK_D); sp(37,25,WHISK); sp(38,25,WHISK_D); sp(39,25,WHISK); sp(40,25,WHISK_D); sp(41,25,WHISK)


# 草莓抹茶杯（左，cx=5，x=3~7，内移3格）
wcol(5, 16, 21, STRAW)
wrow(20, 3, 7, CUP_T)
wrow(21, 2, 8, CUP_T)
fl(29, 31, 3, 7, SYRUP)
wrow(29, 3, 7, SYRUP_L)
fl(25, 28, 3, 7, MILK)
fl(22, 24, 3, 7, MATCHA_L)
wrow(22, 3, 7, MATCHA)
sp(6, 23, ICE); sp(7, 23, ICE)
sp(4, 24, ICE); sp(4, 25, ICE)
sp(6, 25, ICE)

# 芒果抹茶杯（右，cx=58，x=56~60，内移3格）
wcol(58, 16, 21, STRAW)
wrow(20, 56, 60, CUP_T)
wrow(21, 55, 61, CUP_T)
fl(29, 31, 56, 60, MANGO)
wrow(29, 56, 60, MANGO_L)
fl(25, 28, 56, 60, MILK)
fl(22, 24, 56, 60, MATCHA_L)
wrow(22, 56, 60, MATCHA)
sp(57, 23, ICE); sp(58, 23, ICE)
sp(59, 24, ICE); sp(59, 25, ICE)
sp(57, 25, ICE)

# ── 姜饼人（左，x=14~24, y=3~18）──

# 姜饼人面前茶器（整体居中 GCX=18，碗x=17~23，茶筅cx=16，下移2格）
fl(20, 24, 17, 23, BOWL_W)
wrow(19, 18, 22, BOWL_D)
wcol(17, 20, 24, BOWL_D)
wcol(23, 20, 24, BOWL_D)
fl(20, 22, 18, 22, MATCHA)
wrow(20, 18, 22, MATCHA_F)
wrow(25, 19, 22, BOWL_D)
# 碗口右侧尖嘴
sp(24, 21, BOWL_D)
sp(23, 21, MATCHA)
# 茶筅（下移2格，y=18~25）
sp(16,18,WHISK); sp(17,18,WHISK)
sp(16,19,WHISK); sp(17,19,WHISK_D)
sp(16,20,WHISK); sp(17,20,WHISK_D)
sp(15,21,WHISK_D); sp(16,21,WHISK); sp(17,21,WHISK_D); sp(18,21,WHISK)
sp(15,22,WHISK_D); sp(16,22,WHISK); sp(17,22,WHISK_D); sp(18,22,WHISK)
sp(14,23,WHISK); sp(15,23,WHISK_D); sp(16,23,WHISK); sp(17,23,WHISK_D); sp(18,23,WHISK); sp(19,23,WHISK_D)
sp(14,24,WHISK_D); sp(15,24,WHISK); sp(16,24,WHISK_D); sp(17,24,WHISK); sp(18,24,WHISK_D); sp(19,24,WHISK)
sp(14,25,WHISK_D); sp(15,25,WHISK); sp(16,25,WHISK_D); sp(17,25,WHISK); sp(18,25,WHISK_D); sp(19,25,WHISK)
GCX, GCY = 18, 3
# 帽子
fl(GCY, GCY+2, GCX-3, GCX+3, HAT_RED)
sp(GCX, GCY-1, HAT_DARK)
wcol(GCX-3, GCY, GCY+2, HAT_DARK)
wcol(GCX+3, GCY, GCY+2, HAT_DARK)
sp(GCX-2, GCY, HAT_LITE)
# 头（9宽）
fl(GCY+3, GCY+8, GCX-4, GCX+4, GB)
sp(GCX-4, GCY+3, WALL); sp(GCX+4, GCY+3, WALL)
sp(GCX-4, GCY+8, WALL); sp(GCX+4, GCY+8, WALL)
sp(GCX-2, GCY+5, GB_EYE); sp(GCX+2, GCY+5, GB_EYE)
sp(GCX-3, GCY+6, GB_CHEEK); sp(GCX+3, GCY+6, GB_CHEEK)
sp(GCX-1, GCY+7, GBD); sp(GCX, GCY+7, GBD); sp(GCX+1, GCY+7, GBD)
# 脖子
sp(GCX-2, GCY+9, GB); sp(GCX-1, GCY+9, GB); sp(GCX, GCY+9, GB); sp(GCX+1, GCY+9, GB); sp(GCX+2, GCY+9, GB)
# 身体（藏桌后）
fl(GCY+10, GCY+14, GCX-3, GCX+3, GB)
sp(GCX, GCY+11, GB_CHEEK); sp(GCX, GCY+13, GB_CHEEK)
# 手臂伸向茶器（2格宽，肩膀圆角）
sp(GCX-4, GCY+11, GB)
for _ay in range(GCY+12, GCY+21):
    sp(GCX-4, _ay, GB); sp(GCX-5, _ay, GB)
sp(GCX+4, GCY+11, GB)
for _ay in range(GCY+12, GCY+21):
    sp(GCX+4, _ay, GB); sp(GCX+5, _ay, GB)

# ── 蓝兔子（右，x=38~48, y=2~18）──
BCX, BCY = 43, 5
# 耳朵（左）顶部1格圆角在外侧
sp(BCX-2, BCY-3, BUN_B)
for _ey in range(BCY-2, BCY+1): sp(BCX-2, _ey, BUN_B); sp(BCX-1, _ey, BUN_B)
# 左耳内芯
for _ey in range(BCY-2, BCY): sp(BCX-2, _ey, BUN_IN)
# 耳朵（右）顶部1格圆角在外侧
sp(BCX+2, BCY-3, BUN_B)
for _ey in range(BCY-2, BCY+1): sp(BCX+1, _ey, BUN_B); sp(BCX+2, _ey, BUN_B)
# 右耳内芯
for _ey in range(BCY-2, BCY): sp(BCX+2, _ey, BUN_IN)
# 耳朵间底部
sp(BCX, BCY, BUN_B)
# 头（9宽）
fl(BCY+1, BCY+6, BCX-4, BCX+4, BUN_B)
sp(BCX-4, BCY+1, WALL); sp(BCX+4, BCY+1, WALL)
sp(BCX-4, BCY+6, WALL); sp(BCX+4, BCY+6, WALL)
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
fl(BCY+8, BCY+12, BCX-3, BCX+3, BUN_B)
# 手臂伸向茶器（2格宽，肩膀圆角=外列从+1行开始）
sp(BCX-4, BCY+9, BUN_B)
for _ay in range(BCY+10, BCY+19):
    sp(BCX-4, _ay, BUN_B); sp(BCX-5, _ay, BUN_B)
sp(BCX+4, BCY+9, BUN_B)
for _ay in range(BCY+10, BCY+19):
    sp(BCX+4, _ay, BUN_B); sp(BCX+5, _ay, BUN_B)

img.save('pixel_matcha.png')
print(f"Saved: {W*S}x{H*S}px")
