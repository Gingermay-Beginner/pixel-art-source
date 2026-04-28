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

FONT_S = (242, 210, 138)   # 喷泉暖橙亮
FONT_D = (215, 178, 105)   # 喷泉暖橙暗
FONT_M = (228, 194, 122)   # 喷泉中间色
WATER   = ( 65, 228, 198)  # 水色
WATER_L = (185, 245, 228)  # 水浅色
SPRAY   = (185, 245, 228)

# ── 喷泉（中央，CX=32）新版 ──
FX = 32
SPRAY = (185, 245, 228)

# 第一层水盆外缘 x=22~42
fl(20, 21, 22, 42, FONT_S)
fl(22, 23, 23, 41, FONT_S)
wrow(19, 24, 40, FONT_S)
fl(20, 23, 23, 41, FONT_S)
sp(23, 20, FONT_D); sp(27, 20, FONT_D); sp(32, 20, FONT_D); sp(37, 20, FONT_D); sp(41, 20, FONT_D)

# 喷水柱
for _wy in range(17, 19):
    sp(31, _wy, WATER)
    sp(32, _wy, WATER_L)
    sp(33, _wy, WATER)
# 水花
for _wy in [17, 18]:
    _w = 18 - _wy
    for _wx in range(FX-_w, FX+_w+1):
        if abs(_wx - FX) >= _w-1:
            sp(_wx, _wy, SPRAY)
sp(FX-2, 17, SPRAY); sp(FX+2, 17, SPRAY)
sp(FX-1, 16, SPRAY); sp(FX, 16, SPRAY); sp(FX+1, 16, SPRAY)
sp(FX, 15, SPRAY)

# 底座 x=26~38
fl(24, 25, 29, 35, FONT_D)
wrow(24, 27, 37, FONT_S)

# 连接柱 x=29~35
fl(25, 28, 28, 36, FONT_M)
wcol(28, 25, 27, FONT_M)
wcol(36, 25, 27, FONT_M)

# 第二层水盆 x=18~46
fl(29, 30, 18, 46, FONT_S)
wrow(31, 20, 44, FONT_S)
wcol(16, 29, 30, FONT_S)
wcol(16, 31, 31, FONT_S)
wcol(17, 29, 31, FONT_S)
wcol(47, 29, 31, FONT_S)
wcol(48, 31, 31, FONT_S)
wcol(48, 29, 30, FONT_S)
fl(29, 30, 19, 45, WATER)
wrow(30, 18, 46, WATER_L)
wrow(30, 20, 44, WATER_L)
for _wx in [22, 18, 32, 46, 42]:
    sp(_wx, 29, WATER_L)
    sp(_wx, 30, WATER)

# 第二层底座 x=22~42
fl(31, 32, 22, 42, FONT_S)
wrow(31, 23, 41, FONT_S)

for _wx in [23, 27, 32, 37, 41]:
    sp(_wx, 19, WATER)
# 水流及盆面细节
sp(18, 24, (65, 228, 198)); sp(18, 25, (65, 228, 198)); sp(18, 26, (65, 228, 198))
sp(18, 27, (65, 228, 198)); sp(18, 28, (65, 228, 198))
sp(19, 22, (185, 245, 228)); sp(19, 23, (65, 228, 198)); sp(22, 28, (65, 228, 198))
sp(20, 21, (185, 245, 228))
sp(21, 20, (185, 245, 228))
sp(22, 19, (242, 210, 138)); sp(22, 20, (185, 245, 228)); sp(22, 21, (242, 210, 138))
sp(22, 25, WATER); sp(22, 26, WATER); sp(22, 27, WATER); sp(22, 28, (65, 228, 198)); sp(42, 25, WATER); sp(42, 26, WATER); sp(42, 27, WATER); sp(42, 28, (65, 228, 198))
sp(23, 19, (65, 228, 198)); sp(23, 21, (242, 210, 138)); sp(23, 22, (185, 245, 228)); sp(23, 23, (65, 228, 198)); sp(23, 24, (65, 228, 198))
sp(24, 21, (185, 245, 228)); sp(24, 22, (242, 210, 138))
sp(25, 20, (185, 245, 228)); sp(25, 21, (242, 210, 138))
sp(26, 20, (185, 245, 228))
sp(27, 19, (65, 228, 198))
sp(26, 24, (242, 210, 138)); sp(38, 24, (242, 210, 138))
sp(41, 19, (65, 228, 198)); sp(41, 21, (242, 210, 138)); sp(41, 22, (185, 245, 228)); sp(41, 23, (65, 228, 198)); sp(41, 24, (65, 228, 198))
sp(42, 19, (242, 210, 138)); sp(42, 20, (185, 245, 228)); sp(42, 21, (242, 210, 138))
sp(43, 20, (185, 245, 228))
sp(44, 21, (185, 245, 228))
sp(45, 22, (185, 245, 228)); sp(45, 23, (65, 228, 198))
sp(46, 24, (65, 228, 198)); sp(46, 25, (65, 228, 198)); sp(46, 26, (65, 228, 198)); sp(46, 27, (65, 228, 198)); sp(46, 28, (65, 228, 198))
sp(39, 20, (185, 245, 228)); sp(38, 20, (185, 245, 228))
sp(40, 21, (185, 245, 228))
sp(40, 22, (242, 210, 138))
sp(37, 19, (65, 228, 198))
sp(32, 21, WATER_L); sp(32, 22, WATER_L)
sp(32, 23, WATER); sp(32, 24, WATER); sp(32, 25, WATER); sp(32, 26, WATER); sp(32, 27, WATER); sp(32, 28, WATER)

# 喷泉底层（台阶之后画，不被覆盖）
wrow(31, 18, 46, FONT_S)
sp(18, 31, FONT_S); sp(46, 31, FONT_S)
wrow(32, 17, 47, FONT_S)

img.save('/home/azureuser/.openclaw/workspace/fountain_teal.png')
print('Saved')
