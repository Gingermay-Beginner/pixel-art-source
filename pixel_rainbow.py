from PIL import Image
import math

W, H, S = 64, 36, 12
img = Image.new('RGB', (W*S, H*S), (185, 218, 242))

def sp(x, y, c):
    if 0 <= x < W and 0 <= y < H:
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

# ── Colors ──
SKY     = (185, 218, 242)
SKY_TOP = (178, 212, 238)
SKY_HZ  = (205, 228, 245)   # horizon glow

WW_WALL = (28,  38,  55)
WW_WIN  = (58, 112, 175)
WW_WIN_L= (88, 148, 205)
WW_EDGE = ( 35,  52,  82)   # 深蓝灰（不再纯黑）
WW_TOP  = ( 48,  68, 105)   # 楼顶稍亮

BRIDGE  = (175, 168, 152)
BRIDGE_D= (145, 138, 120)
BRIDGE_L= (200, 195, 180)
ROAD_L  = (232, 225, 192)

TES     = ( 55, 105, 188)
TES_D   = ( 35,  75, 148)
TES_LT  = ( 88, 138, 218)
TES_CHR = (248, 248, 220)
WIND    = (172, 212, 238)
WIND_D  = (142, 185, 215)
WIND_RF = (215, 235, 248)  # windshield reflection

GB      = (185, 108,  48)
GBD     = (140,  82,  35)
GB_EYE  = ( 62,  35,  15)
GB_CHK  = (225, 148,  95)
HAT_R   = (198,  42,  32)
HAT_D   = (140,  26,  20)

BUN     = (108, 182, 248)
BUN_D   = ( 78, 145, 205)
BUN_EY  = ( 25,  45,  88)
BUN_IN  = (178, 215, 248)

# ── Sky (最底层) ──
fl(0, 35, 0, 63, SKY)


# ── Rainbow ──
RB_RAW = [(215,48,35),(235,138,45),(232,215,58),(95,185,78),(55,148,215),(82,75,192),(158,75,188)]
SKY_C = (185, 218, 242)
_fade_start_x = 21
_fade_full_x  = 43   # 此处以右完全显示（画面2/3处）
for _bi, _rc in enumerate(RB_RAW):
    _r1 = 13.0 + _bi * 1.2
    _r2 = _r1 + 1.2
    for _x in range(0, 64):
        for _y in range(0, 27):
            _dist = math.sqrt(((_x - 34)/1.5)**2 + (_y - 23)**2)
            if _r1 <= _dist < _r2:
                # x < fade_start: 完全天空色（不画）
                if _x < _fade_start_x:
                    continue
                # 渐变区
                if _x < _fade_full_x:
                    _t = (_x - _fade_start_x) / (_fade_full_x - _fade_start_x)
                else:
                    _t = 1.0
                _mix = _t * 0.85
                _rb = tuple(round(_rc[i]*_mix + SKY_C[i]*(1-_mix)) for i in range(3))
                sp(_x, _y, _rb)

# ── WeWork building (left x=0~16) ──
fl(22, 35, 0, 16, WW_WALL)  # 墙体保持 x=0~16
# 楼顶：深蓝 + 顶部反光线
fl(18, 21, 0, 16, WW_TOP)
wrow(18, 0, 16, (88, 118, 168))   # 顶部亮反光
wrow(21, 0, 16, (55, 78, 118))    # 楼顶底边暗线
# 楼层（x=0~16，全宽）
for wy in range(22, 36, 8):
    wrow(wy-1, 0, 15, (52, 78, 118))   # 楼层间暗腰线
    fl(wy,   wy+3, 0, 15, WW_WIN)
    wrow(wy, 0, 15, WW_WIN_L)
    wrow(wy+1, 0, 15, (72, 128, 192))
    fl(wy+4, min(wy+7, 35), 0, 15, WW_EDGE)
    wrow(wy+4, 0, 15, (52, 75, 115))
    if wy+7 <= 35: wrow(wy+7, 0, 15, (28, 42, 68))
# 竖向分隔线（x=4,8,12）
for vx in range(3, 16, 4):
    for wy in range(22, 36, 8):
        wcol(vx, wy, min(wy+3, 35), WW_WALL)
# Right edge shadow
wcol(15, 18, 35, WW_EDGE)
wcol(16, 18, 35, WW_EDGE)

# ── Trees along left road edge ──
PALM_TR  = ( 82,  58,  28)   # 棕榈干棕
PALM_TRD = ( 52,  38,  18)   # 干暗色
PALM_LF  = ( 48, 128,  38)   # 棕榈叶亮绿
PALM_LFD = ( 28,  88,  22)   # 叶深绿
PALM_LFY = (148, 178,  38)   # 叶黄绿
TREE_TR2 = ( 72,  52,  28)

def draw_palm(cx, base_y, height=10):
    """棕榈树：细直树干+顶部大型放射状叶冠"""
    # 树干（略微弯曲）
    for i in range(height):
        c = PALM_TR if i % 2 == 0 else PALM_TRD
        dx = 1 if i < height//3 else 0
        sp(cx+dx, base_y - i, c)
    ty = base_y - height
    # 大型发散叶片（辐射状，每片5~7格长）
    # 每片叶子是一条斜线，从中心往外
    # 用扇形填充：在叶片之间插值补格，确保不断开
    import math as _pm
    # 定义扇区角度和长度（角度从正右顺时针，y轴向下）
    # 上半圆（-180~0度）= 上方；下半圆 = 下方
    # 用极坐标逐格扫描填充
    _leaf_sectors = [
        # (angle_deg, length, color)
        (180, 6, PALM_LF),   # 正左
        (150, 5, PALM_LF),
        (135, 5, PALM_LFD),
        (120, 5, PALM_LFD),
        (105, 5, PALM_LFY),
        ( 90, 5, PALM_LFY),  # 正上
        ( 75, 5, PALM_LFY),
        ( 60, 5, PALM_LFD),
        ( 45, 5, PALM_LFD),
        ( 30, 5, PALM_LF),
        (  0, 6, PALM_LF),   # 正右
        (210, 4, PALM_LFD),  # 左下
        (240, 3, PALM_LFD),
        (300, 3, PALM_LFD),
        (330, 4, PALM_LFD),  # 右下
    ]
    for ang, length, lc in _leaf_sectors:
        rad = _pm.radians(ang)
        # 沿方向逐步走，每步补两格宽
        dx = _pm.cos(rad); dy = -_pm.sin(rad)  # y轴向下取反
        for step in range(1, length+1):
            bx = round(cx + dx*step)
            by = round(ty + dy*step)
            sp(bx, by, lc)
            # 垂直方向加粗（补相邻格）
            pbx = round(cx + dx*(step-0.5))
            pby = round(ty + dy*(step-0.5))
            sp(pbx, pby, lc)
    leaf_dirs = []  # 已用扇形替代
    sp(cx, ty, PALM_LFY); sp(cx+1, ty, PALM_LFY)


# 沿路左侧摆树（base_y=路面行，树干贴路边xl左1格）
# 近处：橡树打底，棕榈探出树顶
draw_palm(5, 34, height=25) # 橡树旁棕榈探高
# 中近：橡树+棕榈
draw_palm(13, 30, height=17)# 棕榈探出
# 中段：橡树+棕榈
draw_palm(19, 27, height=13)# 棕榈
# 远处：小橡树+棕榈
draw_palm(26, 23, height=8) # 远处棕榈

# ── Road: 弧形弯道（向右弯出画面）──
import math as _math
for y in range(18, 36):
    t = (y - 18) / 17.0  # 0=远端, 1=近端
    # 透视宽度
    w = round(10 + t * 36)
    # 弧形：四次曲线，中段紧贴中心，远端大幅右弯延伸
    cx = round(29 + (1 - t) ** 4 * 34)
    xl = cx - w // 2
    xr = cx + w // 2
    xl = max(0, xl); xr = min(63, xr)
    if y <= 19: xl -= 5; xr -= 5  # y=18~19 路远端左移5格
    wrow(y, xl, xr, BRIDGE)
    sp(xl, y, BRIDGE_D)
    sp(xr, y, BRIDGE_D)
    if xl - 1 >= 0: sp(xl - 1, y, BRIDGE_L)

# 路顶弧形（实心填充）

# 中心虚线（跟着弯，每4格画3格）
for y in range(19, 36):
    if y % 4 != 0:
        t = (y - 18) / 17.0
        cx = round(29 + (1 - t) ** 4 * 34)
        sp(cx, y, ROAD_L)

# ── Wheels (车体之前画) ──
TIRE  = ( 22,  22,  26)
TIRE_D= ( 12,  12,  15)
RIM   = ( 22,  22,  26)
fl(24, 27, 23, 26, TIRE)
sp(23, 27, TIRE_D); sp(26, 27, TIRE_D)
fl(24, 26, 24, 25, RIM)

fl(24, 27, 37, 40, TIRE)
sp(37, 27, TIRE_D); sp(40, 27, TIRE_D)
fl(24, 26, 38, 39, RIM)


# ── Tesla car front (x=17~46, y=20~34) ──
# Roof
fl(13, 15, 24, 39, TES)
wrow(13, 24, 39, TES_D)

# A-pillars
wcol(23, 16, 20, TES_D)
wcol(40, 16, 20, TES_D)

# 车顶圆角（天空色挖角）
sp(24, 13, SKY); sp(39, 13, SKY)
sp(25, 13, SKY); sp(38, 13, SKY)
# Windshield
fl(14, 20, 24, 39, WIND)
# Windshield reflection stripe
wrow(15, 25, 38, WIND_RF)
wrow(20, 24, 39, WIND_D)
# 玻璃上角圆角（天空色挖角）
sp(24, 14, SKY); sp(25, 14, TES)
sp(39, 14, SKY); sp(38, 14, TES)
sp(24, 15, TES_D); sp(39, 15, TES_D)

# Hood
wrow(20, 22, 41, TES)  # 车头顶行，x=21/42圆角挖掉
fl(21, 23, 21, 42, TES)
wrow(20, 22, 41, TES_D)  # 圆角挖空x=21/42
wcol(21, 21, 23, TES_D)
wcol(42, 21, 23, TES_D)


# Lower bumper / no grille (Tesla)
fl(24, 23, 22, 41, TES_D)
wrow(24, 22, 41, TES_D)  # 车头底部描边

# 轮子圆角（精确路面色挖角）
_WBG = (175, 168, 152)
sp(23, 27, _WBG); sp(26, 27, _WBG)
sp(37, 27, _WBG); sp(40, 27, _WBG)
# 车头圆角（四角用天空/地面色挖）
ROAD = (88, 85, 82)   # 路面色（近似）
# 车身底角圆角
sp(20, 27, BRIDGE); sp(43, 27, BRIDGE)
sp(20, 26, BRIDGE); sp(43, 26, BRIDGE)
# 车头四角圆角
_WIN_BG = (35, 75, 148)   # 车窗背景色
sp(20, 27, BRIDGE); sp(43, 27, BRIDGE)  # 底角
sp(21, 27, BRIDGE); sp(42, 27, BRIDGE)  # 底角内侧
# ── 姜饼人 in windshield (left) GCX=26 ──
GCX, GCY = 28, 19   # 头底部 y=19
HAT_LITE = (225,  72,  55)
# 头（7格宽，四角圆角）
wrow(GCY-3, GCX-2, GCX+2, GB)
fl(GCY-2, GCY,   GCX-3, GCX+3, GB)
# 圆角
sp(GCX-3, GCY-3, WIND); sp(GCX+3, GCY-3, WIND)
sp(GCX-3, GCY,   WIND); sp(GCX+3, GCY,   WIND)
# 眼
sp(GCX-1, GCY-2, GB_EYE); sp(GCX+1, GCY-2, GB_EYE)
# 腮红
sp(GCX-2, GCY-1, GB_CHK); sp(GCX+2, GCY-1, GB_CHK)
# 嘴
sp(GCX-1, GCY, GBD); sp(GCX, GCY, GBD); sp(GCX+1, GCY, GBD)
# 帽子（火山版，右偏1格）
sp(GCX+1, GCY-5, HAT_D)                           # 小啾啾
for _dx in range(-1, 4): sp(GCX+_dx, GCY-4, HAT_R)
for _dx in range(-1, 4): sp(GCX+_dx, GCY-3, HAT_R)
sp(GCX-1, GCY-4, HAT_D); sp(GCX+3, GCY-4, HAT_D)
sp(GCX-1, GCY-3, HAT_D); sp(GCX+3, GCY-3, HAT_D)
sp(GCX,   GCY-4, HAT_LITE)

# ── 蓝兔子 in windshield (right) BCX=37 ──
BCX, BCY = 36, 19   # 头底部 y=19
BUN_BLUSH = (235, 148, 178)
BUN_BROW  = ( 35,  68, 135)
BUN_EAR_P = (235, 148, 178)   # 耳内粉色
# 耳朵（去掉顶行，外侧圆角）
for _ey in range(BCY-7, BCY-4):
    sp(BCX-2, _ey, BUN); sp(BCX-1, _ey, BUN)
    sp(BCX+1, _ey, BUN); sp(BCX+2, _ey, BUN)
# 外侧圆角：顶行只留内列（挖掉外列顶格）
sp(BCX-1, BCY-7, BUN)  # 左耳顶只留内列
sp(BCX+1, BCY-7, BUN)  # 右耳顶只留内列
sp(BCX-2, BCY-7, WIND)  # 左耳外列顶格挖掉
sp(BCX+2, BCY-7, WIND)  # 右耳外列顶格挖掉
# 底部2格粉色内侧
sp(BCX-1, BCY-6, BUN_EAR_P); sp(BCX-1, BCY-5, BUN_EAR_P)
sp(BCX+1, BCY-6, BUN_EAR_P); sp(BCX+1, BCY-5, BUN_EAR_P)
# 修复 WIND_RF 横条覆盖耳朵底部（BCY-4）
sp(BCX-2, BCY-4, BUN); sp(BCX-1, BCY-4, BUN_EAR_P)
sp(BCX+1, BCY-4, BUN_EAR_P); sp(BCX+2, BCY-4, BUN)
# x=36~38, y=17 补蓝色（兔子脸，盖在粉色之后）
for _bx in range(36, 39): sp(_bx, 17, BUN)
# 头（7格宽，四角圆角）
fl(BCY-3, BCY,   BCX-3, BCX+3, BUN)
sp(BCX-3, BCY-3, WIND); sp(BCX+3, BCY-3, WIND)
sp(BCX-3, BCY,   WIND); sp(BCX+3, BCY,   WIND)
# 连心眉
sp(BCX-2, BCY-3, BUN_BROW); sp(BCX-1, BCY-3, BUN_BROW)
sp(BCX,   BCY-3, BUN_D)
sp(BCX+1, BCY-3, BUN_BROW); sp(BCX+2, BCY-3, BUN_BROW)
# 眼
sp(BCX-1, BCY-2, BUN_EY); sp(BCX+1, BCY-2, BUN_EY)
# 腮红
sp(BCX-2, BCY-1, BUN_BLUSH); sp(BCX+2, BCY-1, BUN_BLUSH)
# 嘴
sp(BCX-1, BCY, (255,255,255)); sp(BCX, BCY, (255,255,255)); sp(BCX+1, BCY, (255,255,255))

# ── Rear-view mirror (移到车顶中间上方，不遮玻璃) ──
fl(12, 13, 30, 33, (68, 78, 95))
wrow(12, 30, 33, (48, 58, 75))


# ── SF hillside (right x=48~63, y=8~30) ──
HILL    = (122, 162,  88)
HILL_D  = ( 92, 128,  65)
HILL_LT = (155, 195, 112)
H_WALL  = (232, 222, 205)
H_ROOF  = (188,  78,  62)
H_ROOF2 = ( 88, 148, 192)
H_ROOF3 = (215, 178,  88)
H_WIN   = (148, 198, 228)

# 山丘轮廓（从右侧延伸进来）
hill_profile = {
    48: 24, 49: 22, 50: 19, 51: 17, 52: 14, 53: 13,
    54: 12, 55: 12, 56: 12, 57: 12, 58: 12, 59: 12,
    60: 12, 61: 12, 62: 13, 63: 15
}
for hx, hy_top in hill_profile.items():
    wcol(hx, hy_top, 35, HILL)
    sp(hx, hy_top, HILL_LT)
    sp(hx, hy_top+1, HILL_D)

# 山腰小房子（散布在山丘上）
houses = [
    (48, 21, H_ROOF),  (50, 20, H_ROOF2), (52, 21, H_ROOF3),
    (54, 20, H_ROOF),  (56, 19, H_ROOF2), (58, 20, H_ROOF3),
    (60, 21, H_ROOF),  (62, 20, H_ROOF2),
]
for hx, hy, roof_c in houses:
    # 屋身2x3
    fl(hy+1, hy+3, hx, hx+2, H_WALL)
    # 屋顶三角（1格）
    wrow(hy, hx, hx+2, roof_c)
    sp(hx+1, hy-1, roof_c)
    # 小窗
    sp(hx+1, hy+2, H_WIN)

# ── Save ──
# Headlights
fl(21, 22, 22, 23, TES_CHR)
fl(21, 22, 40, 41, TES_CHR)



# ── Great Egret 大白鹭（镜像，朝左）──
EGRET    = (248, 248, 248)
EGRET_BK = ( 28,  28,  32)
EGRET_YL = (218, 178,  38)
# 嘴（朝左，4格）
sp(26, 21, EGRET_YL); sp(27, 21, EGRET_YL); sp(28, 21, EGRET_YL); sp(29, 21, EGRET_YL)
# 头
sp(30, 21, EGRET); sp(31, 21, EGRET)
sp(30, 21, EGRET_BK)  # 眼
# S形脖子（填密，镜像）
sp(30, 22, EGRET); sp(31, 22, EGRET)
sp(31, 23, EGRET); sp(32, 23, EGRET)
sp(31, 24, EGRET); sp(32, 24, EGRET)
sp(30, 25, EGRET); sp(31, 25, EGRET)
sp(30, 26, EGRET); sp(31, 26, EGRET)  # 脖身连接
# 身体
fl(26, 27, 30, 36, EGRET)
sp(29, 26, EGRET); sp(30, 26, EGRET); sp(31, 26, EGRET); sp(32, 26, EGRET); sp(33, 26, EGRET); sp(34, 26, EGRET); sp(35, 26, EGRET)
sp(29, 27, EGRET); sp(36, 27, EGRET)
# 长腿（6格）
sp(31, 28, EGRET_BK); sp(33, 28, EGRET_BK)
# 腿连线 (31,28)→(34,31)
sp(32, 29, EGRET_BK)
sp(33, 30, EGRET_BK)
sp(32, 31, EGRET_BK)
sp(30, 33, EGRET_BK)
sp(31, 32, EGRET_BK)
sp(29, 33, EGRET_BK)
sp(31, 34, EGRET_BK)
sp(33, 28, EGRET_BK)
sp(34, 29, EGRET_BK)
sp(35, 30, EGRET_BK)
sp(36, 31, EGRET_BK)

sp(36, 31, EGRET_BK)
sp(36, 32, EGRET_BK)
sp(36, 33, EGRET_BK)
# 脚趾
sp(35, 34, EGRET_BK); sp(36, 34, EGRET_BK); sp(37, 34, EGRET_BK)

# 车头两侧描边
sp(22, 22, TES_D)
sp(41, 22, TES_D)
img.save('pixel_rainbow.png')
print('Saved')
