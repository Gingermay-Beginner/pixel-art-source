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
SKY     = (155, 205, 242)
SKY_TOP = (135, 192, 235)
SKY_HZ  = (198, 225, 245)   # horizon glow

WW_WALL = ( 62,  78, 102)
WW_WIN  = ( 72, 155, 195)
WW_WIN_L= (115, 185, 225)
WW_EDGE = ( 65,  92, 128)   # 层间暗带（提亮）
WW_TOP  = ( 72,  98, 138)   # 楼顶稍亮

BRIDGE  = (155, 152, 138)
BRIDGE_D= (135, 125, 102)
BRIDGE_L= (208, 200, 175)
ROAD_L  = (238, 228, 185)

TES     = ( 62, 108, 155)
TES_D   = ( 42,  80, 125)
TES_LT  = ( 82, 148, 212)
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
RB_RAW = [(238,185,95),(238,225,105),(125,198,125),(95,175,222),(155,135,215)]
SKY_C = (155, 205, 242)
_fade_start_x = 0
_fade_full_x  = 0   # 全圈统一饱和度
for _bi, _rc in enumerate(RB_RAW):
    _r1 = 13.0 + _bi * 1.3
    _r2 = _r1 + 1.3
    for _x in range(0, 64):
        for _y in range(0, 27):
            _dist = math.sqrt(((_x - 32))**2 + (_y - 21)**2)
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


# ── 远景波浪云团（横穿画面，y≈16~19）──
CLD    = (238, 242, 248)   # 云主体：偏冷白
CLD_D  = (210, 218, 232)   # 云底阴影
CLD_T  = (248, 250, 255)   # 云顶高光

# 波浪轮廓：每列云顶 y（波峰波谷交替）
_cld_top = {
     0:13,  1:13,  2:13,  3:12,  4:12,  5:12,  6:13,  7:13,
     8:13,  9:12, 10:11, 11:11, 12:11, 13:11, 14:12, 15:12,
    16:14, 17:14, 18:14, 19:14, 20:15, 21:16, 22:16, 23:16,
    24:16, 25:18, 26:17, 27:16, 28:15, 29:15, 30:15, 31:15,
    32:16, 33:17, 34:17, 35:17, 36:16, 37:15, 38:15, 39:15,
    40:15, 41:16, 42:16, 43:17, 44:17, 45:17, 46:17, 47:16,

}
_cld_bot = 26  # 云底延伸到 y=26

for _cx, _cy_top in _cld_top.items():
    sp(_cx, _cy_top, CLD_T)         # 云顶高光
    for _cy in range(_cy_top+1, _cld_bot):
        sp(_cx, _cy, CLD)           # 云主体
    sp(_cx, _cld_bot, CLD_D)        # 云底阴影


# 云层彩虹染色
_RB_RAW_T = [(238,185,95),(238,225,105),(125,198,125),(95,175,222),(155,135,215)]
for _bi, _rc in enumerate(_RB_RAW_T):
    _r1 = 13.0 + _bi * 1.3
    _r2 = _r1 + 1.3
    for _cx2 in range(0, 64):
        for _cy2 in range(0, 27):
            _dist2 = math.sqrt((_cx2 - 32)**2 + (_cy2 - 21)**2)
            if _r1 <= _dist2 < _r2:
                _ct = _cld_top.get(_cx2, 99)
                if _cy2 >= _ct and _cy2 <= _cld_bot:
                    _base = pixels[_cy2][_cx2] if False else (238,242,248)
                    _mix = 0.25
                    _rb2 = tuple(round(_rc[i]*_mix + 238*(1-_mix)) for i in range(3))
                    sp(_cx2, _cy2, _rb2)
# ── WeWork building (left x=0~16) ──
fl(25, 34, 0, 11, WW_WALL)   # y>24
fl(17, 24, 0, 7, WW_WALL)   # y<=24
# 楼顶：深蓝 + 顶部反光线
fl(17, 20, 0, 7, WW_TOP)
wrow(17, 0, 7, (88, 118, 168))   # 顶部亮反光
wrow(20, 0, 7, (55, 78, 118))    # 楼顶底边暗线
# 楼层（y<=25 部分 x=0~7，y>25 部分 x=0~15）
for wy in range(21, 35, 8):
    _xl = 0
    _xr = 6 if wy <= 24 else 10
    wrow(wy-1, _xl, _xr, (52, 78, 118))
    fl(wy,   wy+3, _xl, _xr, WW_WIN)
    wrow(wy, _xl, _xr, WW_WIN_L)
    wrow(wy+1, _xl, _xr, (72, 128, 192))
    fl(wy+4, min(wy+7, 35), _xl, _xr, WW_EDGE)
    wrow(wy+4, _xl, _xr, (52, 75, 115))
    if wy+7 <= 35: wrow(wy+7, _xl, _xr, (28, 42, 68))
# 竖向分隔线（x=4,8,12）
for vx in range(3, 16, 4):
    for wy in range(21, 35, 8):
        _xr2 = 8 if wy <= 24 else 11
        if vx < _xr2:
            wcol(vx, wy, min(wy+3, 35), WW_WALL)
fl(25, 28, 7, 10, WW_EDGE)  # 补 y=26~29 x=7~11 为 WW_EDGE
wrow(25, 7, 10, (52, 75, 115))
# Right edge shadow



# x=12~16 y=18~35 补云色（WeWork右侧露空）
fl(17, 34, 12, 16, CLD)
# ── Trees along left road edge ──
PALM_TR  = (135, 112,  82)   # 棕榈干棕
PALM_TRD = (105,  85,  58)   # 干暗色
PALM_LF  = ( 75, 148, 115)   # 棕榈叶亮绿
PALM_LFD = ( 52, 108,  88)   # 叶深绿
PALM_LFY = (125, 178, 138)   # 叶黄绿
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
draw_palm(5, 38, height=25) # 橡树旁棕榈探高
# 中近：橡树+棕榈
draw_palm(13, 36, height=17)# 棕榈探出
# 中段：橡树+棕榈
draw_palm(19, 36, height=13)# 棕榈
# 远处：小橡树+棕榈
draw_palm(26, 31, height=8) # 远处棕榈

# 右侧波峰云（x=48~63，最顶层，盖在山坡上方）
_cld_r2 = {
    48:14, 49:14, 50:13, 51:13, 52:13, 53:13, 54:14, 55:15,
    56:16, 57:15, 58:14, 59:13, 60:12, 61:11, 62:11, 63:11,
}
for _cx, _cy_top in _cld_r2.items():
    sp(_cx, _cy_top, CLD_T)
    for _cy in range(_cy_top+1, 27):
        sp(_cx, _cy, CLD)
    sp(_cx, 27, CLD_D)

# ── SF hillside colors ──
HILL    = ( 88, 148, 118)
HILL_D  = ( 62, 108,  88)
HILL_LT = (118, 178, 148)
H_WALL  = (242, 235, 215)
H_ROOF  = (205,  88,  68)
H_ROOF2 = ( 98, 165, 208)
H_ROOF3 = (228, 195,  95)
H_WIN   = (148, 198, 228)

hill_profile = {
    48: 24, 49: 22, 50: 19, 51: 17, 52: 14, 53: 13,
    54: 12, 55: 12, 56: 12, 57: 12, 58: 12, 59: 12,
    60: 12, 61: 12, 62: 13, 63: 15
}

# 山体 y>=24 部分（路面下层）
for hx, hy_top in hill_profile.items():
    y_start = max(hy_top, 24)
    if y_start <= 35:
        wcol(hx, y_start, 35, HILL)

# 路面右侧到山体左边界的天空缺口填山体色（y=24~30）
import math as _m2
for _y in range(24, 31):
    _t = (_y - 18) / 17.0
    _cx = round(29 + (1-_t)**4 * 34)
    _xr = min(63, _cx + round(10 + _t*36)//2)
    if _xr + 1 <= 47:
        wrow(_y, _xr+1, 47, HILL)

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
    if y == 18: xl -= 10; xr -= 10  # y=18 路面左移10格
    if y == 19: xl -= 5; xr -= 5  # y=19 路面左移5格
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

# y=17 路延伸（y=18复制上移1格，右移4格）
wrow(17, 51, 57, BRIDGE)
sp(51, 17, BRIDGE_D)
sp(57, 17, BRIDGE_D)
sp(50, 17, BRIDGE_L)
# ── SF hillside upper (y<=23，路面上层，下移2格) ──

for hx, hy_top in hill_profile.items():
    _hy = hy_top + 2
    y_end = min(23, 35)
    if _hy <= y_end:
        wcol(hx, _hy, y_end, HILL)
        sp(hx, _hy, HILL_LT)
        sp(hx, _hy+1, HILL_D)

# 山腰小房子（散布在山丘上）
houses = [
    (48, 21, H_ROOF),  (50, 20, H_ROOF2), (52, 21, H_ROOF3),
    (54, 20, H_ROOF),  (56, 19, H_ROOF2), (58, 20, H_ROOF3),
    (60, 21, H_ROOF),  (62, 20, H_ROOF2),
]
for hx, hy, roof_c in houses:
    fl(hy+1, hy+3, hx, hx+2, H_WALL)
    wrow(hy, hx, hx+2, roof_c)
    sp(hx+1, hy-1, roof_c)
    sp(hx+1, hy+2, H_WIN)

# ── Wheels (车体之前画) ──
TIRE  = ( 55,  52,  62)
TIRE_D= ( 38,  35,  45)
RIM   = ( 22,  22,  26)
fl(24, 27, 23, 26, TIRE)
sp(23, 27, TIRE_D); sp(26, 27, TIRE_D)
fl(24, 26, 24, 25, RIM)

fl(24, 27, 38, 41, TIRE)
sp(38, 27, TIRE_D); sp(41, 27, TIRE_D)
fl(24, 26, 39, 40, RIM)


# ── Tesla car front (x=17~46, y=20~34) ──
# Roof
fl(13, 15, 24, 40, TES)
wrow(13, 24, 40, TES_D)

# A-pillars
wcol(23, 16, 20, TES_D)
wcol(41, 16, 20, TES_D)

# 车顶圆角（天空色挖角）
sp(24, 13, SKY); sp(40, 13, SKY)
sp(25, 13, SKY); sp(39, 13, SKY)
# Windshield
fl(14, 20, 24, 40, WIND)
# Windshield reflection stripe
wrow(15, 25, 39, WIND_RF)
wrow(20, 24, 40, WIND_D)
# 玻璃上角圆角（天空色挖角）
sp(24, 14, SKY); sp(25, 14, TES)
sp(40, 14, SKY); sp(39, 14, TES)
sp(24, 15, TES_D); sp(40, 15, TES_D)

# Hood
wrow(20, 22, 42, TES)  # 车头顶行
fl(21, 24, 21, 43, TES)


# Lower bumper / no grille (Tesla)
fl(25, 24, 22, 42, TES)
wrow(25, 22, 42, TES)  # 车头底部补行

# 轮子圆角（用当前路面色）
_WBG = BRIDGE
sp(23, 27, _WBG); sp(26, 27, _WBG)
sp(38, 27, _WBG); sp(41, 27, _WBG)
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



# 车顶彩虹遮挡修复
for _fx in range(30, 34):
    sp(_fx, 13, TES_D)

# 兔子头顶补色 y=15 x=35~37
for _fx in range(35, 38):
    sp(_fx, 15, BUN)

# y=19 两侧脸颊补色
sp(GCX-3, GCY, GB); sp(GCX+2, GCY, GB); sp(GCX+3, GCY, GB)  # 姜饼人
sp(BCX-3, BCY, BUN); sp(BCX-2, BCY, BUN); sp(BCX+3, BCY, BUN)  # 兔子

# ── 小私人飞机（右上角，向右飞）──
PL_BODY = (245, 245, 242); PL_WING = (228, 228, 222); PL_WIN = (148, 195, 225)
# 尾迹（飞机左侧往左渐消）
TRAIL   = (248, 250, 255)
TRAIL_D = (225, 232, 242)
for _ti, _tx in enumerate(range(11, 46)):
    _tc = TRAIL if _ti % 2 == 0 else TRAIL_D
    sp(_tx, 5, _tc)
for _ti, _tx in enumerate(range(13, 46)):
    if _ti % 3 != 0:
        sp(_tx, 6, TRAIL_D)
# 机身 x=50~54 y=4~5
wrow(4, 50, 54, PL_BODY)
wrow(5, 49, 54, PL_BODY)
# 机头
sp(55, 4, PL_BODY); sp(55, 5, PL_BODY); sp(56, 5, PL_BODY)
# 尾翼
sp(49, 3, PL_WING)
# 上翼
wrow(3, 49, 52, PL_WING)
# 下翼
wrow(2, 48, 50, PL_WING)
# 窗
sp(53, 4, PL_WIN); sp(54, 4, PL_WIN)
# 尾气
wrow(5, 47, 48, PL_BODY)
wrow(4, 46, 47, PL_BODY)
# ── Great Egret 大白鹭（镜像，朝左）──
EGRET    = (238, 245, 252)
EGRET_BK = ( 58,  42,  25)
EGRET_YL = (218, 178,  38)
# 嘴（朝左，4格）
sp(28, 22, EGRET_YL); sp(29, 22, EGRET_YL); sp(30, 22, EGRET_YL); sp(31, 22, EGRET_YL)
# 头
sp(32, 22, EGRET); sp(33, 22, EGRET)
sp(32, 22, EGRET_BK)  # 眼
# S形脖子（填密，镜像）
sp(32, 23, EGRET); sp(33, 23, EGRET)
sp(33, 23, EGRET); sp(34, 23, EGRET)
sp(33, 24, EGRET); sp(34, 24, EGRET)
sp(32, 26, EGRET); sp(33, 26, EGRET)
sp(32, 27, EGRET); sp(33, 27, EGRET)  # 脖身连接
sp(32, 25, EGRET); sp(33, 25, EGRET)  # 脖身衔接段
# 身体
fl(26, 26, 32, 38, EGRET)  # 身体上行
fl(27, 27, 32, 37, EGRET)  # 身体下行（右下角圆角挖掉）
sp(31, 26, EGRET); sp(32, 26, EGRET); sp(33, 26, EGRET); sp(34, 26, EGRET); sp(35, 26, EGRET); sp(36, 26, EGRET); sp(37, 26, EGRET)
sp(31, 27, EGRET)

# 长腿（6格）
sp(33, 28, EGRET_BK); sp(35, 28, EGRET_BK)
# 腿连线 (31,28)→(34,31)
sp(34, 29, EGRET_BK)
sp(35, 30, EGRET_BK)
sp(34, 31, EGRET_BK)
sp(32, 33, EGRET_BK)
sp(33, 32, EGRET_BK)
sp(31, 33, EGRET_BK)
sp(33, 34, EGRET_BK)
sp(35, 28, EGRET_BK)
sp(36, 29, EGRET_BK)
sp(37, 30, EGRET_BK)
sp(38, 31, EGRET_BK)

sp(38, 31, EGRET_BK)
sp(38, 32, EGRET_BK)
sp(38, 33, EGRET_BK)
# 脚趾
sp(37, 34, EGRET_BK); sp(38, 34, EGRET_BK); sp(39, 34, EGRET_BK)

# Headlights
fl(22, 23, 23, 24, TES_CHR)
fl(22, 23, 39, 40, TES_CHR)
img.save('pixel_rainbow.png')
print('Saved')



