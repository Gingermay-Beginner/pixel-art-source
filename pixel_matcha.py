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
SKY      = (235, 240, 248)   # 室内背景（浅蓝灰）
WALL     = (225, 218, 205)   # 墙面
WALL_D   = (198, 190, 175)   # 墙面暗
FLOOR    = (198, 182, 158)   # 地板暖木色
FLOOR_D  = (175, 158, 132)   # 地板纹
FLOOR_L  = (218, 205, 182)   # 地板亮

TABLE    = (228, 215, 192)   # 桌面
TABLE_D  = (195, 182, 158)   # 桌面暗边
TABLE_E  = (175, 162, 138)   # 桌沿

# 抹茶相关
MATCHA   = ( 88, 148,  72)   # 抹茶绿
MATCHA_L = (118, 178,  95)   # 抹茶亮
MATCHA_F = (148, 198, 118)   # 抹茶泡沫
CUP_W    = (245, 248, 252)   # 透明杯（接近白）
CUP_T    = (195, 215, 232)   # 杯壁透明感
BOWL_W   = (238, 232, 220)   # 茶碗米白
BOWL_D   = (205, 198, 182)   # 茶碗暗
ICE      = (215, 235, 248)   # 冰块
MILK     = (248, 245, 238)   # 牛奶白

# 糖浆瓶颜色
SYR_CO   = (228, 195, 148)   # 椰子
SYR_MG   = (235, 178,  72)   # 芒果
SYR_PS   = (228, 118,  88)   # 热情果
SYR_ST   = (215,  72,  88)   # 草莓
SYR_BL   = ( 88, 115, 195)   # 蓝莓

# 茶筅（小扫帚刷）
WHISK    = (148, 118,  72)   # 竹色
WHISK_D  = (108,  82,  48)   # 竹暗

# 角色
GB       = (185, 108,  48)
GBD      = (140,  82,  35)
GB_EYE   = ( 62,  35,  15)
GB_CHEEK = (225, 148,  95)
HAT_RED  = (188,  55,  48)
HAT_DARK = (135,  32,  28)
HAT_LITE = (215,  88,  72)

BUN_B    = ( 88, 158, 228)   # 蓝兔子身体
BUN_IN   = (228, 185, 195)   # 耳朵内粉
BUN_EYE  = ( 35,  55, 105)
BUN_D    = ( 62, 118, 188)   # 暗蓝

# ── 背景 ──
# 墙
fl(0, 22, 0, 63, WALL)
# 窗户（WeWork大窗）
fl(2, 18, 4, 28, SKY)
fl(2, 18, 32, 58, SKY)
# 窗框
wrow(1, 4, 28, WALL_D)
wrow(1, 32, 58, WALL_D)
wrow(19, 4, 28, WALL_D)
wrow(19, 32, 58, WALL_D)
wcol(3, 2, 18, WALL_D)
wcol(29, 2, 18, WALL_D)
wcol(31, 2, 18, WALL_D)
wcol(59, 2, 18, WALL_D)
# 中间隔断
wcol(30, 0, 22, WALL)

# 地板
fl(23, 35, 0, 63, FLOOR)
# 地板木纹
for row in range(23, 36, 3):
    wrow(row, 0, 63, FLOOR_L)
for row in range(25, 36, 3):
    wrow(row, 0, 63, FLOOR_D)

# WeWork logo 区域（墙中间）
fl(8, 12, 30, 32, WALL_D)

# ── 操作台（桌子）──
# 桌面 y=20~22，x=8~55
fl(20, 21, 8, 55, TABLE)
wrow(20, 8, 55, TABLE_D)   # 桌面前缘暗边
wrow(22, 8, 55, TABLE_E)   # 桌沿底
wcol(8, 20, 22, TABLE_D)
wcol(55, 20, 22, TABLE_D)

# ── 糖浆瓶（5个，x=10~28，y=13~20）──
syrup_colors = [SYR_CO, SYR_MG, SYR_PS, SYR_ST, SYR_BL]
for i, sc in enumerate(syrup_colors):
    bx = 10 + i*4
    # 瓶身
    fl(15, 20, bx, bx+2, sc)
    # 瓶颈
    fl(13, 14, bx+1, bx+1, sc)
    # 瓶盖
    sp(bx+1, 12, WALL_D)
    # 瓶身暗边
    wcol(bx+2, 15, 20, (max(0,sc[0]-30), max(0,sc[1]-30), max(0,sc[2]-30)))

# ── 抹茶碗（x=35~41, y=17~20）──
fl(18, 20, 35, 41, BOWL_W)
wrow(17, 36, 40, BOWL_D)   # 碗口
wcol(35, 18, 20, BOWL_D)
wcol(41, 18, 20, BOWL_D)
# 抹茶液
fl(18, 19, 36, 40, MATCHA)
wrow(18, 36, 40, MATCHA_F)  # 泡沫

# ── 茶筅（x=43~44, y=14~20）──
# 柄
wcol(43, 14, 18, WHISK)
wcol(44, 14, 18, WHISK)
# 刷毛（下端散开）
for fx in range(41, 47):
    sp(fx, 19, WHISK_D)
    if fx % 2 == 0:
        sp(fx, 20, WHISK_D)

# ── 透明杯（x=47~52, y=13~20）──
fl(13, 20, 47, 52, CUP_W)
wcol(47, 13, 20, CUP_T)
wcol(52, 13, 20, CUP_T)
wrow(20, 47, 52, CUP_T)
# 冰块
fl(16, 19, 48, 51, ICE)
for ix in [48, 50]:
    sp(ix, 17, CUP_W)
# 抹茶层（底部）
wrow(20, 48, 51, MATCHA)
wrow(19, 48, 51, MATCHA_L)
# 杯盖
fl(12, 12, 47, 52, CUP_T)
wrow(11, 48, 51, CUP_T)
# 吸管
wcol(50, 9, 12, MATCHA)

# ── 牛奶盒（x=32~34, y=14~20）──
fl(14, 20, 32, 34, MILK)
wrow(14, 32, 34, WALL_D)
wcol(32, 14, 20, TABLE_D)
wcol(34, 14, 20, TABLE_D)
# 牛奶盒顶三角
sp(32, 13, MILK); sp(33, 12, MILK); sp(34, 13, MILK)

# ── 姜饼人（打抹茶，站在桌后 x=38~44, y=10~19）──
GCX, GCY = 40, 10
# 帽子
fl(GCY, GCY+1, GCX-2, GCX+2, HAT_RED)
sp(GCX, GCY-1, HAT_DARK)  # 小啾啾
wcol(GCX-2, GCY, GCY+1, HAT_DARK)
wcol(GCX+2, GCY, GCY+1, HAT_DARK)
sp(GCX-1, GCY, HAT_LITE)
# 头
fl(GCY+2, GCY+5, GCX-3, GCX+3, GB)
sp(GCX-3, GCY+2, WALL); sp(GCX+3, GCY+2, WALL)  # 圆角
sp(GCX-3, GCY+5, WALL); sp(GCX+3, GCY+5, WALL)
# 眼睛腮红
sp(GCX-1, GCY+3, GB_EYE); sp(GCX+1, GCY+3, GB_EYE)
sp(GCX-2, GCY+4, GB_CHEEK); sp(GCX+2, GCY+4, GB_CHEEK)
sp(GCX-1, GCY+5, GBD); sp(GCX, GCY+5, GBD)  # 嘴
# 身体
fl(GCY+6, GCY+9, GCX-2, GCX+2, GB)
sp(GCX, GCY+7, GB_CHEEK); sp(GCX, GCY+9, GB_CHEEK)  # 扣子
# 手臂（往下持茶筅）
sp(GCX-3, GCY+7, GB); sp(GCX-3, GCY+8, GB)
sp(GCX+3, GCY+7, GB); sp(GCX+3, GCY+8, GB)
sp(GCX+4, GCY+8, GB)  # 右手延伸持茶筅

# ── 蓝兔子（选糖浆，x=16~22, y=10~19）──
BCX, BCY = 18, 10
# 耳朵
fl(BCY-3, BCY, BCX-1, BCX-1, BUN_B)
fl(BCY-3, BCY, BCX+1, BCX+1, BUN_B)
fl(BCY-2, BCY, BCX-2, BCX-2, BUN_IN)
fl(BCY-2, BCY, BCX+2, BCX+2, BUN_IN)
# 头
fl(BCY+1, BCY+4, BCX-3, BCX+3, BUN_B)
sp(BCX-3, BCY+1, WALL); sp(BCX+3, BCY+1, WALL)
sp(BCX-3, BCY+4, WALL); sp(BCX+3, BCY+4, WALL)
# 连心眉
for bx in [BCX-2, BCX-1]: sp(bx, BCY+2, BUN_D)
sp(BCX, BCY+2, BUN_IN)
for bx in [BCX+1, BCX+2]: sp(bx, BCY+2, BUN_D)
# 眼睛腮红
sp(BCX-1, BCY+3, BUN_EYE); sp(BCX+1, BCY+3, BUN_EYE)
sp(BCX-2, BCY+4, BUN_IN); sp(BCX+2, BCY+4, BUN_IN)
sp(BCX-1, BCY+5, BUN_B); sp(BCX, BCY+5, BUN_B); sp(BCX+1, BCY+5, BUN_B)  # 嘴白
# 身体
fl(BCY+5, BCY+9, BCX-2, BCX+2, BUN_B)
sp(BCX-3, BCY+6, BUN_B); sp(BCX-3, BCY+7, BUN_B)  # 手臂
sp(BCX+3, BCY+6, BUN_B); sp(BCX+3, BCY+7, BUN_B)
sp(BCX+4, BCY+7, BUN_B)  # 右手伸向糖浆瓶

img.save('pixel_matcha.png')
print(f"Saved: {W*S}x{H*S}px")
