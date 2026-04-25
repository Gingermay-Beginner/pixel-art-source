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
SKY_TOP = (158, 198, 228)
SKY_HZ  = (205, 228, 245)   # horizon glow

WW_WALL = (28,  38,  55)
WW_WIN  = (58, 112, 175)
WW_WIN_L= (88, 148, 205)
WW_EDGE = (18,  25,  40)

BRIDGE  = (175, 168, 152)
BRIDGE_D= (145, 138, 120)
BRIDGE_L= (200, 195, 180)
ROAD_L  = (232, 225, 192)

TES     = ( 55, 105, 188)
TES_D   = ( 35,  75, 148)
TES_LT  = ( 88, 138, 218)
TES_CHR = (192, 202, 215)
WIND    = (172, 212, 238)
WIND_D  = (142, 185, 215)
WIND_RF = (215, 235, 248)  # windshield reflection

GB      = (185, 108,  48)
GBD     = (140,  82,  35)
GB_EYE  = ( 62,  35,  15)
GB_CHK  = (225, 148,  95)
HAT_R   = (188,  55,  48)
HAT_D   = (135,  32,  28)

BUN     = (108, 182, 248)
BUN_D   = ( 78, 145, 205)
BUN_EY  = ( 25,  45,  88)
BUN_IN  = (178, 215, 248)

# ── Sky (最底层) ──
fl(0, 35, 0, 63, SKY)
fl(0,  8, 0, 63, SKY_TOP)
wrow(16, 0, 63, SKY_HZ)
wrow(17, 0, 63, SKY_HZ)

# ── Rainbow ──
import random as _rnd
_rnd.seed(7)
RB = [(215,48,35),(235,138,45),(232,215,58),(95,185,78),(55,148,215),(82,75,192),(158,75,188)]
_fade_start_x = 18
_fade_end_x   = 33
for _bi, _color in enumerate(RB):
    _r1 = 13.0 + _bi * 1.2
    _r2 = _r1 + 1.2
    for _x in range(18, 64):
        for _y in range(0, 28):
            _dist = math.sqrt((_x - 38)**2 + (_y - 24)**2)
            if _r1 <= _dist < _r2:
                # 左侧渐隐：越靠左越稀疏
                if _x < _fade_end_x:
                    _t = (_x - _fade_start_x) / (_fade_end_x - _fade_start_x)
                    if _rnd.random() > _t:
                        continue
                sp(_x, _y, _color)

# ── WeWork building (left x=0~17) ──
fl(4, 35, 0, 17, WW_WALL)
# 楼顶黑色
fl(0, 3, 0, 17, WW_EDGE)
# 横向：蓝玻璃4格 + 黑4格
for wy in range(4, 36, 8):
    fl(wy,   wy+3, 1, 15, WW_WIN)
    wrow(wy, 1, 15, WW_WIN_L)
    fl(wy+4, min(wy+7, 35), 1, 15, WW_EDGE)
# 竖向分隔线
for vx in range(4, 16, 4):
    for wy in range(4, 36, 8):
        wcol(vx, wy, min(wy+3, 35), WW_WALL)
# Right edge shadow
wcol(16, 4, 35, WW_EDGE)
wcol(17, 4, 35, WW_EDGE)

# ── Bridge road perspective ──
# Near (y=35): x=10~53; Far (y=18): x=22~41 then curves right
for y in range(18, 36):
    t = (y - 18) / 17.0  # 0=far, 1=near
    xl = round(22 - t * 10)
    xr = round(41 + t * 12)
    wrow(y, xl, xr, BRIDGE)
    sp(xl, y, BRIDGE_D)
    sp(xr, y, BRIDGE_D)
    if xl - 1 >= 0: sp(xl - 1, y, BRIDGE_L)

# Road center dashes
for y in range(19, 36):
    if y % 3 != 1:
        sp(31, y, ROAD_L)

# Bridge far end curves right (y=18~21)
for y in range(18, 22):
    t = (21 - y) / 3.0
    offset = round(t * 5)
    xl = round(22 + offset)
    xr = round(41 + offset + 2)
    wrow(y, xl, xr, BRIDGE)
    sp(xl - 1, y, BRIDGE_L)

# ── Wheels (车体之前画) ──
TIRE  = ( 38,  38,  42)
TIRE_D= ( 22,  22,  25)
RIM   = (188, 195, 205)
fl(28, 33, 17, 22, TIRE)
sp(17, 28, TIRE_D); sp(22, 28, TIRE_D)
sp(17, 33, TIRE_D); sp(22, 33, TIRE_D)
fl(29, 32, 18, 21, RIM)
sp(19, 30, TIRE); sp(20, 30, TIRE)
fl(28, 33, 41, 46, TIRE)
sp(41, 28, TIRE_D); sp(46, 28, TIRE_D)
sp(41, 33, TIRE_D); sp(46, 33, TIRE_D)
fl(29, 32, 42, 45, RIM)
sp(43, 30, TIRE); sp(44, 30, TIRE)

# ── Tesla car front (x=17~46, y=20~34) ──
# Roof
fl(15, 17, 22, 41, TES)
wrow(15, 22, 41, TES_D)

# A-pillars
wcol(21, 16, 22, TES_D)
wcol(42, 16, 22, TES_D)

# Windshield
fl(16, 22, 22, 41, WIND)
# Windshield reflection stripe
wrow(17, 23, 40, WIND_RF)
wrow(22, 22, 41, WIND_D)

# Hood
fl(23, 29, 17, 46, TES)
wrow(23, 17, 46, TES_D)
wcol(17, 23, 29, TES_D)
wcol(46, 23, 29, TES_D)

# Headlights
fl(24, 26, 18, 22, TES_CHR)
fl(24, 26, 41, 45, TES_CHR)
fl(24, 25, 19, 21, (238, 242, 252))
fl(24, 25, 42, 44, (238, 242, 252))
sp(20, 30, TES_LT)
sp(43, 30, TES_LT)

# Lower bumper / no grille (Tesla)
fl(27, 29, 18, 45, TES_D)
fl(29, 30, 19, 44, (38, 42, 58))

# ── 姜饼人 in windshield (left) x=23~29 ──
# Hat
wrow(17, 24, 28, HAT_R)
wrow(16, 25, 27, HAT_R)
sp(26, 16, HAT_D)
# Head
fl(18, 21, 23, 29, GB)
sp(23, 18, WIND); sp(29, 18, WIND)
sp(23, 21, WIND); sp(29, 21, WIND)
# Eyes
sp(24, 19, GB_EYE); sp(27, 19, GB_EYE)
# Cheeks
sp(23, 20, GB_CHK); sp(29, 20, GB_CHK)
# Smile
sp(25, 21, GBD); sp(26, 21, GBD); sp(27, 21, GBD)
# Body hint
fl(22, 22, 24, 28, GB)

# ── 蓝兔子 in windshield (right) x=34~41 ──
# Ears
fl(15, 21, 35, 36, BUN_IN)
fl(15, 21, 38, 39, BUN_IN)
sp(35, 14, BUN); sp(36, 14, BUN)
sp(38, 14, BUN); sp(39, 14, BUN)
# Head
fl(18, 21, 34, 40, BUN)
sp(34, 18, WIND); sp(40, 18, WIND)
sp(34, 21, WIND); sp(40, 21, WIND)
# Eyes (connected brow)
for bx in range(35, 40): sp(bx, 18, BUN_EY)
sp(35, 19, BUN_EY); sp(38, 19, BUN_EY)
# Cheeks
sp(34, 20, BUN_IN); sp(40, 20, BUN_IN)
# Body hint
fl(22, 22, 35, 39, BUN)

# ── Rear-view mirror ──
fl(16, 22, 30, 33, (68, 78, 95))
wrow(16, 30, 33, (48, 58, 75))

# ── Save ──
img.save('pixel_rainbow.png')
print('Saved')
