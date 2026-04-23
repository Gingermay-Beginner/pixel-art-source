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
fl(19, 35, 4, 59, TABLE)
# 木纹（横向）
for row in range(21, 36, 4):
    wrow(row, 4, 59, TABLE_D)
# 桌边（上边 = 近景前缘）
wrow(35, 4, 59, TABLE_E)
wcol(4, 19, 35, TABLE_E)
wcol(59, 19, 35, TABLE_E)

# ── 桌上物品（俯视桌面上，侧视物品）──

# 5个糖浆瓶（前排，x=6~28, y=25~33）
syrup_colors = [SYR_CO, SYR_MG, SYR_PS, SYR_ST, SYR_BL]
for i, sc in enumerate(syrup_colors):
    bx = 6 + i*5
    fl(26, 32, bx, bx+3, sc)
    fl(23, 25, bx+1, bx+2, sc)
    sp(bx+1, 22, WALL_D); sp(bx+2, 22, WALL_D)
    wcol(bx+3, 26, 32, (max(0,sc[0]-35), max(0,sc[1]-35), max(0,sc[2]-35)))

# 抹茶碗（x=35~42, y=23~28）
fl(24, 28, 35, 42, BOWL_W)
wrow(23, 36, 41, BOWL_D)
wcol(35, 24, 28, BOWL_D)
wcol(42, 24, 28, BOWL_D)
fl(24, 26, 36, 41, MATCHA)
wrow(24, 36, 41, MATCHA_F)

# 茶筅：短柄（y=20~21）+ 长刷条（y=22~28）
# 柄（1/3）
wcol(44, 20, 21, WHISK)
wcol(45, 20, 21, WHISK)
# 刷条（2/3，向下散开）
for fx in range(41, 50):
    if fx in [44, 45]:
        for fy in range(22, 29): sp(fx, fy, WHISK)
    elif fx in [42, 43, 46, 47]:
        for fy in range(23, 29): sp(fx, fy, WHISK_D)
    elif fx in [41, 48]:
        for fy in range(25, 29): sp(fx, fy, WHISK_D)
# 刷条底端散开
for fx in range(40, 51):
    if fx % 2 == 0:
        sp(fx, 29, WHISK_D)

# 透明杯（x=49~55, y=20~31）
fl(20, 31, 49, 55, CUP_W)
wcol(49, 20, 31, CUP_T)
wcol(55, 20, 31, CUP_T)
wrow(31, 49, 55, CUP_T)
fl(23, 29, 50, 54, ICE)
sp(50, 25, CUP_W); sp(53, 26, CUP_W)
wrow(31, 50, 54, MATCHA)
wrow(30, 50, 54, MATCHA_L)
fl(18, 19, 49, 55, CUP_T)
wrow(17, 50, 54, CUP_T)
wcol(52, 13, 18, MATCHA)  # 吸管

# ── 姜饼人（左，x=14~24, y=3~18）──
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
sp(GCX-1, GCY+9, GB); sp(GCX, GCY+9, GB); sp(GCX+1, GCY+9, GB)
# 身体（藏桌后）
fl(GCY+10, GCY+14, GCX-3, GCX+3, GB)
sp(GCX, GCY+11, GB_CHEEK); sp(GCX, GCY+13, GB_CHEEK)
# 手臂搭桌（y=19）
sp(GCX-4, GCY+10, GB); sp(GCX-4, GCY+11, GB)
sp(GCX+4, GCY+10, GB); sp(GCX+4, GCY+11, GB)
sp(GCX+5, GCY+12, GB)

# ── 蓝兔子（右，x=38~48, y=2~18）──
BCX, BCY = 43, 3
# 耳朵
fl(BCY-3, BCY, BCX-1, BCX-1, BUN_B)
fl(BCY-3, BCY, BCX+1, BCX+1, BUN_B)
fl(BCY-2, BCY, BCX-2, BCX-2, BUN_IN)
fl(BCY-2, BCY, BCX+2, BCX+2, BUN_IN)
# 头（9宽）
fl(BCY+1, BCY+6, BCX-4, BCX+4, BUN_B)
sp(BCX-4, BCY+1, WALL); sp(BCX+4, BCY+1, WALL)
sp(BCX-4, BCY+6, WALL); sp(BCX+4, BCY+6, WALL)
for bx in [BCX-3, BCX-2]: sp(bx, BCY+3, BUN_D)
sp(BCX-1, BCY+3, BUN_IN); sp(BCX, BCY+3, BUN_IN); sp(BCX+1, BCY+3, BUN_IN)
for bx in [BCX+2, BCX+3]: sp(bx, BCY+3, BUN_D)
sp(BCX-2, BCY+4, BUN_EYE); sp(BCX+2, BCY+4, BUN_EYE)
sp(BCX-3, BCY+5, BUN_IN); sp(BCX+3, BCY+5, BUN_IN)
sp(BCX-1, BCY+6, BUN_B); sp(BCX, BCY+6, BUN_B); sp(BCX+1, BCY+6, BUN_B)
# 脖子
sp(BCX-1, BCY+7, BUN_B); sp(BCX, BCY+7, BUN_B); sp(BCX+1, BCY+7, BUN_B)
# 身体（藏桌后）
fl(BCY+8, BCY+14, BCX-3, BCX+3, BUN_B)
# 手臂
sp(BCX-4, BCY+9, BUN_B); sp(BCX-4, BCY+10, BUN_B)
sp(BCX+4, BCY+9, BUN_B); sp(BCX+4, BCY+10, BUN_B)

img.save('pixel_matcha.png')
print(f"Saved: {W*S}x{H*S}px")
