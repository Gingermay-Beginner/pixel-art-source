from PIL import Image

S = 12
W, H = 64*S, 36*S
img = Image.new('RGB', (W, H), (180, 200, 225))
pixels = img.load()

def sp(x, y, c):
    if 0 <= x < 64 and 0 <= y < 36:
        for dy in range(S):
            for dx in range(S):
                pixels[x*S+dx, y*S+dy] = c

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

FONT_S = (212, 188, 148)
FONT_D = (182, 158, 118)
WATER   = ( 88, 148, 188)
WATER_L = (138, 188, 218)
SPRAY   = (178, 215, 238)
FX = 32

# 第一层水盆外缘 x=22~42（+1右）
fl(20, 23, 22, 42, FONT_S)
wrow(19, 24, 40, FONT_S)
wrow(24, 24, 40, FONT_D)
wcol(22, 20, 23, FONT_D)
wcol(42, 20, 23, FONT_D)
# 水面 x=23~41
fl(20, 23, 23, 41, WATER)
wrow(20, 25, 39, WATER_L)
for _wx in [26, 29, 33, 38]:
    sp(_wx, 22, WATER_L)

# 喷水柱（不变）
for _wy in range(15, 20):
    sp(31, _wy, WATER)
    sp(32, _wy, WATER_L)
    sp(33, _wy, WATER)
# 水花（不变）
for _wy in [15, 16]:
    _w = 16 - _wy
    for _wx in range(FX-_w, FX+_w+1):
        if abs(_wx - FX) >= _w-1:
            sp(_wx, _wy, SPRAY)
sp(FX-2, 15, SPRAY); sp(FX+2, 15, SPRAY)
sp(FX-1, 14, SPRAY); sp(FX, 14, SPRAY); sp(FX+1, 14, SPRAY)
sp(FX, 13, SPRAY)

# 底座 x=26~38
fl(24, 25, 26, 38, FONT_D)
wrow(24, 27, 37, FONT_S)

# 连接柱 x=30~34
fl(25, 28, 30, 34, FONT_D)
wcol(30, 25, 28, FONT_S)
wcol(34, 25, 28, FONT_S)

# 第二层水盆 x=18~46
fl(29, 30, 18, 46, FONT_S)
wrow(28, 20, 44, FONT_S)
wrow(31, 20, 44, FONT_D)
wcol(18, 29, 30, FONT_D)
wcol(46, 29, 30, FONT_D)
# 水面 x=19~45
fl(29, 30, 19, 45, WATER)
wrow(29, 20, 44, WATER_L)
for _wx in [22, 27, 32, 38, 43]:
    sp(_wx, 30, WATER_L)

# 第二层底座 x=22~42
fl(31, 32, 22, 42, FONT_D)
wrow(31, 23, 41, FONT_S)

img.save('/tmp/fountain_draft.png')
print('Saved')
