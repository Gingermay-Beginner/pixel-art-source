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

FONT_S = (178, 195, 212)
FONT_D = (148, 162, 178)
WATER   = ( 88, 148, 188)
WATER_L = (138, 188, 218)
SPRAY   = (178, 215, 238)
FX = 32

fl(20, 23, 22, 41, FONT_S)
wrow(19, 24, 39, FONT_S)
wrow(24, 24, 39, FONT_D)
wcol(22, 20, 23, FONT_D)
wcol(41, 20, 23, FONT_D)
fl(20, 23, 23, 40, WATER)
wrow(20, 25, 38, WATER_L)
for _wx in [26, 29, 33, 37]:
    sp(_wx, 22, WATER_L)
for _wy in range(15, 20):
    sp(31, _wy, WATER)
    sp(32, _wy, WATER_L)
for _wy in [15, 16]:
    _w = 16 - _wy
    for _wx in range(FX-_w, FX+_w+1):
        if abs(_wx - FX) >= _w-1:
            sp(_wx, _wy, SPRAY)
sp(FX-2, 15, SPRAY); sp(FX+2, 15, SPRAY)
sp(FX-1, 14, SPRAY); sp(FX, 14, SPRAY); sp(FX+1, 14, SPRAY)
sp(FX, 13, SPRAY)
fl(24, 25, 26, 37, FONT_D)
wrow(24, 27, 36, FONT_S)
fl(25, 28, 30, 33, FONT_D)
wcol(30, 25, 28, FONT_S)
wcol(33, 25, 28, FONT_S)
fl(29, 30, 18, 45, FONT_S)
wrow(28, 20, 43, FONT_S)
wrow(31, 20, 43, FONT_D)
wcol(18, 29, 30, FONT_D)
wcol(45, 29, 30, FONT_D)
fl(29, 30, 19, 44, WATER)
wrow(29, 20, 43, WATER_L)
for _wx in [22, 27, 32, 37, 42]:
    sp(_wx, 30, WATER_L)
fl(31, 32, 22, 41, FONT_D)
wrow(31, 23, 40, FONT_S)

img.save('/tmp/fountain_draft.png')
