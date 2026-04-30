from PIL import Image, ImageDraw
import math, random

W, H, S = 64, 36, 12
img = Image.new('RGB', (W*S, H*S), (245, 243, 240))
draw = ImageDraw.Draw(img)

def sp(x, y, c):
    if 0<=x<W and 0<=y<H:
        draw.rectangle([x*S, y*S, x*S+S-1, y*S+S-1], fill=c)

def fl(y1, y2, x1, x2, c):
    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            sp(x, y, c)

def wr(y, x1, x2, c):
    for x in range(x1, x2+1): sp(x, y, c)

def wc(x, y1, y2, c):
    for y in range(y1, y2+1): sp(x, y, c)

# ── 背景 ──
fl(0, 35, 0, 63, (235, 232, 228))

# ── 三个手机框 ──
PHONE_BG   = (28, 26, 32)
SCREEN_BG  = (18, 20, 28)
PHONE_EDGE = (48, 45, 52)

def phone_frame(px1, py1, px2, py2):
    fl(py1, py2, px1, px2, PHONE_BG)
    # 圆角
    sp(px1, py1, (235,232,228)); sp(px2, py1, (235,232,228))
    sp(px1, py2, (235,232,228)); sp(px2, py2, (235,232,228))
    # 屏幕内区
    fl(py1+1, py2-1, px1+1, px2-1, SCREEN_BG)
    # 顶部刘海
    fl(py1+1, py1+1, px1+5, px2-5, (38,36,42))
    sp((px1+px2)//2, py1+1, (58,55,62))

# 手机1: x=1~19
phone_frame(1, 0, 19, 35)
# 手机2: x=23~41
phone_frame(23, 0, 41, 35)
# 手机3: x=45~63
phone_frame(45, 0, 63, 35)

# ══════════════════════════
# 手机1：AR 视角
# ══════════════════════════
# 街道背景
ASPHALT  = (72, 75, 82)
ASPHALT_L= (88, 92, 100)
SIDEWALK = (185, 178, 165)
GRASS    = (108, 158, 88)
SKY_AR   = (148, 195, 228)
BUILDING = (198, 188, 172)
BUILD_D  = (168, 158, 142)
WIN_AR   = (178, 215, 235)

# 天空
fl(2, 12, 2, 18, SKY_AR)
# 建筑左
fl(3, 14, 2, 7, BUILDING)
fl(3, 14, 8, 8, BUILD_D)
# 窗户
for wy in [4, 7, 10]:
    for wx in [3, 5]:
        sp(wx, wy, WIN_AR)
# 建筑右
fl(5, 14, 15, 18, BUILDING)
fl(5, 14, 14, 14, BUILD_D)
for wy in [6, 9, 12]:
    for wx in [16, 18]:
        sp(wx, wy, WIN_AR)
# 地面透视
fl(15, 22, 2, 18, SIDEWALK)
fl(15, 18, 6, 13, ASPHALT)
wr(15, 2, 18, (155,148,135))
wr(22, 2, 18, (155,148,135))
# 草地边缘
fl(15, 17, 2, 5, GRASS)
fl(15, 17, 14, 18, GRASS)

# 小柯基（底部中心）
DOG_O = (198, 148, 88)
DOG_D = (158, 108, 58)
DOG_W = (245, 240, 232)
DOG_N = (38, 32, 28)
_dx, _dy = 10, 26  # 狗中心
# 身体
fl(_dy-1, _dy+1, _dx-3, _dx+2, DOG_O)
# 头
fl(_dy-3, _dy-1, _dx-1, _dx+1, DOG_O)
sp(_dx-2, _dy-2, DOG_O); sp(_dx+2, _dy-2, DOG_O)
# 耳朵
sp(_dx-2, _dy-4, DOG_D); sp(_dx-1, _dy-4, DOG_D)
sp(_dx+1, _dy-4, DOG_D); sp(_dx+2, _dy-4, DOG_D)
# 眼睛
sp(_dx-1, _dy-3, DOG_N); sp(_dx+1, _dy-3, DOG_N)
# 鼻子
sp(_dx, _dy-2, DOG_N)
# 腿
sp(_dx-2, _dy+2, DOG_O); sp(_dx-1, _dy+2, DOG_O)
sp(_dx+1, _dy+2, DOG_O); sp(_dx+2, _dy+2, DOG_O)
sp(_dx-2, _dy+3, DOG_D); sp(_dx-1, _dy+3, DOG_D)
sp(_dx+1, _dy+3, DOG_D); sp(_dx+2, _dy+3, DOG_D)
# 尾巴
sp(_dx+3, _dy-1, DOG_O); sp(_dx+4, _dy-2, DOG_O); sp(_dx+4, _dy-3, DOG_O)
# 白肚皮
sp(_dx-1, _dy, DOG_W); sp(_dx, _dy, DOG_W); sp(_dx+1, _dy, DOG_W)

# AR UI 覆盖层
# 顶部状态栏
fl(2, 3, 2, 18, (18,20,28))
# 心情条
HRT = (228, 75, 95)
PAW = (228, 148, 88)
for hx in range(3, 9): sp(hx, 2, (45,42,52) if hx > 7 else HRT)
for px in range(10, 16): sp(px, 2, (45,42,52) if px > 13 else PAW)
sp(3, 3, HRT); sp(10, 3, PAW)
# 底部提示
fl(30, 33, 2, 18, (18,20,28))
BTN = (88, 178, 118)
fl(31, 32, 6, 14, BTN)
sp(6, 31, (62,148,88)); sp(14, 31, (62,148,88))
sp(6, 32, (62,148,88)); sp(14, 32, (62,148,88))
# 爪印图标 (小)
sp(4, 31, (245,240,232)); sp(4, 32, (245,240,232))

# 标签文字（像素点模拟）
# "AR" 两个像素字母
AR_C = (255, 235, 88)
# A
sp(3, 24, AR_C); sp(5, 24, AR_C)
sp(2, 25, AR_C); sp(4, 25, AR_C); sp(6, 25, AR_C)
sp(2, 26, AR_C); sp(3, 26, AR_C); sp(4, 26, AR_C); sp(5, 26, AR_C); sp(6, 26, AR_C)
sp(2, 27, AR_C); sp(6, 27, AR_C)
# R
sp(8, 24, AR_C); sp(9, 24, AR_C); sp(10, 24, AR_C)
sp(8, 25, AR_C); sp(11, 25, AR_C)
sp(8, 26, AR_C); sp(9, 26, AR_C); sp(10, 26, AR_C)
sp(8, 27, AR_C); sp(10, 27, AR_C); sp(11, 27, AR_C)

# ══════════════════════════
# 手机2：领养界面
# ══════════════════════════
# 顶部标题区
fl(2, 5, 24, 40, (28, 32, 48))
# 标题像素点
TC = (228, 218, 198)
# 三个狗牌卡片
CARD  = (38, 40, 52)
CARD_S= (52, 55, 68)  # selected
SEL   = (255, 195, 88)  # 选中边框色

cards = [(24, 6, 30, 15), (32, 6, 38, 15), (24, 17, 30, 26)]
labels = [(248,195,128), (168,108,68), (218,218,218)]  # 金毛/柴犬/萨摩
for i, (cx1, cy1, cx2, cy2) in enumerate(cards):
    c = CARD_S if i == 0 else CARD
    fl(cy1, cy2, cx1, cx2, c)
    if i == 0:  # 选中框
        wr(cy1, cx1, cx2, SEL); wr(cy2, cx1, cx2, SEL)
        wc(cx1, cy1, cy2, SEL); wc(cx2, cy1, cy2, SEL)
    # 狗狗头像（简化）
    dc = labels[i]
    _hdx, _hdy = (cx1+cx2)//2, (cy1+cy2)//2 - 1
    fl(_hdy-2, _hdy+1, _hdx-2, _hdx+2, dc)
    sp(_hdx-3, _hdy-1, dc); sp(_hdx+3, _hdy-1, dc)
    sp(_hdx-2, _hdy-3, (dc[0]//2, dc[1]//2, dc[2]//2))
    sp(_hdx+2, _hdy-3, (dc[0]//2, dc[1]//2, dc[2]//2))
    sp(_hdx-1, _hdy, (28,24,20)); sp(_hdx+1, _hdy, (28,24,20))
    sp(_hdx, _hdy+1, (28,24,20))

# 第4张空牌 + "?" (添加更多)
fl(17, 26, 32, 38, (32,34,45))
sp(35, 21, (88,88,108)); sp(35, 22, (88,88,108)); sp(35, 23, (88,88,108))
sp(34, 21, (88,88,108)); sp(36, 21, (88,88,108))
sp(35, 20, (88,88,108))

# 领养按钮
fl(28, 30, 26, 38, (88, 178, 118))
sp(26, 28, (62,148,88)); sp(38, 28, (62,148,88))
sp(26, 30, (62,148,88)); sp(38, 30, (62,148,88))
# 爪印
sp(30, 29, (245,240,232)); sp(31, 28, (245,240,232)); sp(32, 29, (245,240,232))
sp(31, 30, (245,240,232)); sp(33, 28, (245,240,232))

# 选中狗品种名(像素点装饰)
sp(28, 32, SEL); sp(29, 32, SEL); sp(30, 32, SEL)
sp(32, 32, TC); sp(33, 32, TC); sp(34, 32, TC)

# ══════════════════════════
# 手机3：地图印记
# ══════════════════════════
MAP_BG  = (62, 78, 72)
ROAD    = (88, 95, 108)
ROAD_L  = (108, 115, 128)
BLOCK   = (78, 98, 85)
PARK    = (88, 148, 95)

# 地图背景
fl(2, 33, 46, 62, MAP_BG)

# 道路网格
for rx in [48, 52, 56, 60]:
    wc(rx, 2, 33, ROAD)
for ry in [7, 13, 19, 25, 31]:
    wr(ry, 46, 62, ROAD)

# 街区填色
fl(3, 6, 47, 51, BLOCK)
fl(3, 6, 53, 59, BLOCK)
fl(8, 12, 47, 51, BLOCK)
fl(8, 12, 53, 59, BLOCK)
fl(8, 12, 61, 62, BLOCK)
fl(14, 18, 47, 51, BLOCK)
fl(14, 18, 57, 62, BLOCK)
fl(20, 24, 47, 51, BLOCK)
fl(20, 24, 53, 55, BLOCK)
fl(20, 24, 57, 62, BLOCK)
fl(26, 30, 47, 51, PARK)   # 公园
fl(26, 30, 53, 55, BLOCK)
fl(26, 30, 57, 62, BLOCK)
fl(32, 33, 47, 51, BLOCK)
fl(32, 33, 53, 62, BLOCK)

# 爪印标记（散布在道路上）
def paw(px, py, intensity):
    # 越深=越多狗来过
    base = max(30, 255 - intensity*60)
    c = (255, base, base) if intensity <= 2 else (255, 128+intensity*10, 88)
    if intensity >= 4: c = (255, 195, 88)  # 热点金色
    # 主掌
    sp(px, py, c)
    sp(px-1, py-1, c); sp(px+1, py-1, c)
    if intensity >= 2:
        sp(px-1, py+1, c); sp(px+1, py+1, c)

# 普通印记
paw(49, 4, 1); paw(55, 5, 1); paw(50, 10, 1)
paw(54, 11, 2); paw(58, 9, 1); paw(61, 4, 1)
paw(50, 16, 2); paw(54, 17, 1); paw(62, 15, 1)
paw(50, 22, 1); paw(61, 21, 2); paw(55, 23, 1)
paw(49, 28, 1); paw(57, 27, 2)
# 热点（公园，多狗聚集）
paw(48, 27, 5); paw(50, 29, 5); paw(49, 31, 4)
paw(51, 28, 4); paw(50, 26, 4)
# 路口热点
paw(52, 13, 3); paw(52, 19, 3); paw(52, 7, 2)

# 当前用户位置（蓝点）
USER_DOT = (88, 178, 235)
fl(22, 24, 54, 56, USER_DOT)
sp(53, 22, MAP_BG); sp(57, 22, MAP_BG)
sp(53, 24, MAP_BG); sp(57, 24, MAP_BG)
sp(55, 21, USER_DOT)  # 光晕顶

# 手机标题
fl(2, 4, 46, 62, (22, 28, 38))
for tx in [47,48,49]: sp(tx, 3, (88,178,235))
for tx in [51,52,53,54]: sp(tx, 3, (155,215,248))

img.save('pixel_pawprint.png')
print('Saved')
