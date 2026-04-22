from PIL import Image

W, H = 64, 36
S = 12

# ── 颜色 ──
SKY       = (185, 218, 242)
WALL      = (215, 208, 198)
WALL_D    = (188, 182, 172)
ROOF      = (168, 188, 148)
ROOF_D    = (142, 165, 122)
WIN_FRAME = (168, 162, 155)
WIN_FRAME_D=(168, 162, 155)
WIN_IN    = (185, 188, 195)

GROUND    = (148, 178, 115)
GROUND_D  = (118, 150,  95)
GROUND_L  = (168, 215, 118)

AZA_P     = (235,  55,  75)
AZA_PD    = (198,  35,  50)
AZA_PL    = (252, 128,  98)
AZA_LEAF  = ( 72, 148,  45)
AZA_LEAF_D=( 52, 118,  35)
AZA_W     = (195, 192, 198)

BOAR      = ( 88,  72,  62)
BOAR_L    = (118,  98,  85)
BOAR_LT   = (168, 145, 118)
BOAR_B    = (182, 158, 132)
BOAR_SN   = (215, 165, 140)
BOAR_EY   = ( 22,  15,  10)
EYE_W     = (245, 242, 238)
BOAR_TK   = (238, 225, 192)
NOSTRIL   = ( 55,  38,  28)

BUN_BODY  = ( 95, 158, 215)
BUN_INNER = (210, 168, 190)
BUN_EYE   = ( 38,  22,  60)
HAT_RED   = (198,  42,  32)
HAT_DARK  = (165,  52,  42)
HAT_LITE  = (225,  72,  55)
GB_BODY   = (185, 108,  48)

canvas = [[SKY]*W for _ in range(H)]

def sp(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        canvas[y][x] = c

def fl(y1, y2, x1, x2, c):
    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            sp(x, y, c)

def wrow(y, x1, x2, c):
    for x in range(x1, x2+1): sp(x, y, c)

# ── 天空 ──
fl(0, 7, 0, 63, SKY)
# 右侧加盖墙（x=32~63，y=0~4）
fl(0, 4, 32, 63, WALL)

# ── 屋顶下沿（y=6~7） ──

# ── 房子墙面（y=8~22） ──
fl(8, 21, 18, 63, WALL)

# 左侧绿树（房子左方天空区）
TREE_G  = ( 92, 118, 112)   # 绿色主色
TREE_GD = ( 72,  88,  85)   # 深绿
TREE_GL = (105, 148, 135)   # 亮绿
TREE_WH = (238, 242, 248)   # 白花
TREE_TK2= ( 78,  55,  28)   # 树干

def sp2(x, y, c):
    if 0 <= y < H and 0 <= x < W: canvas[y][x] = c
def wrow2(y, x1, x2, c):
    for x in range(x1, x2+1): sp2(x, y, c)
def wcol2(x, y1, y2, c):
    for y in range(y1, y2+1): sp2(x, y, c)

# 树冠（不规则大块）
for y, x1, x2 in [
    (4,  8, 10),  (5,  6, 12),  (6,  5, 14),
    (7,  5, 15),  (8,  5, 16),  (9,  5, 16),
    (10, 5, 16),  (11, 6, 16),  (12, 7, 16),
    (13, 7, 16),  (14, 8, 16),  (15, 5, 17),
    (16, 5, 17),  (17, 5, 17),  (18, 5, 17),
    (19, 5, 16),  (20, 6, 15),  (21, 7, 14),
]:
    wrow2(y, x1, x2, TREE_G)
# 深绿阴影
for x,y in [(16,18),(13,20),(14,21),(12,15)]:
    sp2(x,y,TREE_GD)
# 亮绿高光
for x,y in [(13,15),(11,17)]:
    sp2(x,y,TREE_GL)
# 大白花（5朵）
for fx,fy in [(8,13),(13,14),(10,17),(15,16),(11,19),(9,5),(14,6),(11,8),(7,7),(13,9)]:
    for dx,dy in [(0,0),(1,0),(-1,0),(0,-1),(0,1)]:
        sp2(fx+dx,fy+dy,TREE_WH)
# 树干
if False:
    for dx,dy in [(0,0),(1,0),(-1,0),(0,-1),(0,1)]:
        sp2(fx+dx,fy+dy,TREE_WH)

# 绿色屋顶（斜线填充）
for _ry in range(5, 12):
    _rx_left = round(18 - 8*(_ry-5)/6)
    for _rx in range(_rx_left, 64):
        canvas[_ry][_rx] = (148, 195, 105)

# 门（窗户右边）
DOOR_F = WIN_FRAME
DOOR_D = WIN_FRAME_D
DOOR_IN_UP = WIN_IN
DOOR_IN_LO = WIN_FRAME
DX1, DX2 = 45, 51
DY1, DY2 = 12, 21
fl(DY1, DY2, DX1, DX2, DOOR_F)
for dy in range(DY1, DY2+1): sp(DX1, dy, DOOR_D)
for dx in range(DX1, DX2+1): sp(dx, DY2, DOOR_D)
# 玻璃（上半）
fl(DY1+1, DY1+4, DX1+1, DX2-1, DOOR_IN_UP)
# 下半实心
fl(DY1+5, DY2-1, DX1+1, DX2-1, DOOR_IN_LO)
# 门把手
sp(DX1+1, (DY1+DY2)//2, WIN_IN)

fl(8, 21, 60, 63, WALL_D)

# ── 窗户（正中，x=24~40, y=9~21） ──
WX1, WX2 = 24, 40
WY1, WY2 = 12, 20

fl(WY1, WY2, WX1, WX2, WIN_FRAME)
for y in range(WY1, WY2+1): sp(WX1, y, WIN_FRAME_D)
for x in range(WX1, WX2+1): sp(x, WY2, WIN_FRAME_D)
fl(WY1+1, WY2-1, WX1+1, WX2-1, WIN_IN)

MX = (WX1+WX2)//2   # 32
MY = (WY1+WY2)//2   # 15
for y in range(WY1+1, WY2): sp(MX, y, (168, 162, 155))
# 屋顶材质（瓦片横纹）
for _ry in range(5, 12):
    _rx_left = round(18 - 8*(_ry-5)/6)
    _offset = (_ry % 2) * 3
    for _rx in range(_rx_left, 64):
        if canvas[_ry][_rx] == (148, 195, 105):
            # 每隔4格一道暗色竖缝（错位）
            if (_rx - _offset) % 4 == 0:
                canvas[_ry][_rx] = (140, 178, 112)
            # 偶数行底边暗一格
            elif _ry % 2 == 1:
                canvas[_ry][_rx] = (143, 182, 116)
wrow(11, 10, 63, ROOF)
wrow(12, 10, 63, ROOF_D)

# 二层窗户（x=45~61, y=-∞~8，距屋顶1格）
W2X1, W2X2 = 45, 61
W2Y1, W2Y2 = 0, 3   # 上移5格
fl(W2Y1+1, W2Y2-1, W2X1, W2X2, (195, 190, 182))
for y in range(W2Y1, W2Y2+1): sp(W2X1, y, (168, 162, 155))
for y in range(W2Y1, W2Y2+1): sp(W2X2, y, (168, 162, 155))
for x in range(W2X1, W2X2+1): sp(x, W2Y2, (168, 162, 155))
for x in range(W2X1+1, W2X2): sp(x, 0, (185, 188, 195))  # y=0延伸窗色
fl(W2Y1+1, W2Y2-1, W2X1+1, W2X2-1, (185, 188, 195))
MX2 = (W2X1+W2X2)//2  # 53
for y in range(W2Y1, W2Y2): sp(MX2, y, (168, 162, 155))
# ── 窗内角色（偷看） ──
# 兔子（左半窗）：露耳朵 + 眼睛
fl(14, 17, 27, 27, BUN_BODY)
fl(14, 17, 29, 29, BUN_BODY)
fl(15, 16, 27, 27, BUN_INNER)
fl(15, 16, 29, 29, BUN_INNER)
fl(18, 19, 26, 31, BUN_BODY)
sp(26, 18, WIN_IN); sp(31, 18, WIN_IN)
sp(28, 19, BUN_EYE); sp(30, 19, BUN_EYE)

# 姜饼人（右半窗）：露帽子 + 头顶
sp(38, 17, WIN_IN)
sp(38, 15, WIN_IN)
sp(36, 16, HAT_LITE)
fl(18, 19, 33, 38, GB_BODY)
sp(33, 18, WIN_IN); sp(38, 18, WIN_IN)
sp(34, 19, BUN_EYE); sp(36, 19, BUN_EYE)

# ── 地面（y=22~35） ──
fl(22, 35, 0, 63, GROUND)
# wrow(22, 0, 63, GROUND_L)
for x in range(0, 64, 4):
    sp(x, 25, GROUND_D)
    sp(x+2, 28, GROUND_D)
    sp(x+1, 32, GROUND_D)

# ── 野猪绘制函数 ──
def draw_boar(ox, oy, facing='right'):
    BW = 27
    def lsp(lx, ly, c):
        if facing == 'right': sp(ox+lx, oy+ly, c)
        else: sp(ox+(BW-1-lx), oy+ly, c)
    def lfl(ly1, ly2, lx1, lx2, c):
        for ly in range(ly1, ly2+1):
            for lx in range(lx1, lx2+1): lsp(lx, ly, c)

    # 身体
    lfl(3,8, 0,10, BOAR_B)
    lfl(3,8, 2,9, BOAR_B)
    lfl(2,2, 2,8, BOAR_B)
    lfl(1,1, 2,6, BOAR_B)
    lsp(6,1,BOAR_B); lsp(9,4,BOAR_B)
    for lx,ly in [(2,1),(9,1),(1,2),(1,3),(1,10),(2,10),(0,10)]: lsp(lx,ly,GROUND)
    # 腿（3条，1格高）
    lfl(9,10, 0,1, BOAR_L)
    lfl(9,10, 5,6, BOAR_L)
    lfl(9,10, 12,13, BOAR_L)
    # 尾巴
    lsp(0,3,BOAR_L); lsp(1,2,BOAR_L)
    # 横纹（在头之前画）
    BOAR_STRIPE = (108, 85, 65)
    BOAR_STRIPE_L = (195, 172, 145)
    stripe_offsets = {0:0, 1:0, 2:0, 3:-1, 4:-1, 5:-1, 6:-1, 7:0, 8:0}
    for sx in range(0, 9):
        off = stripe_offsets.get(sx, 0)
        lsp(sx, 5+off, BOAR_STRIPE)
        lsp(sx, 6+off, BOAR_STRIPE_L)
        lsp(sx, 8+off, BOAR_STRIPE)
    back_offsets = {0:0, 1:0, 2:-1, 3:-1, 4:-1, 5:-1, 6:-1, 7:-1, 8:0}
    for sx in range(0, 9):
        boff = back_offsets.get(sx, 0)
        lsp(sx, 3+boff, BOAR_STRIPE)
        if not (sx in [4,5] and 2+boff < 1) and not (sx == 7 and 2+boff == 1): lsp(sx, 2+boff, BOAR_STRIPE_L)
    # 头（最后画，盖身体/花纹）
    lfl(6,7, 9,15, BOAR_L)   # 上两行窄（x=9~15）
    lfl(8,10, 8,17, BOAR_L)   # 下三行全宽
    lsp(17,11,GROUND)
    lsp(17,5,BOAR)
    for _ly in range(5,12): lsp(17,_ly,GROUND)
    # x=1 延伸列
    lsp(1,6,BOAR_STRIPE); lsp(1,7,BOAR_B); lsp(1,8,BOAR_STRIPE); lsp(1,9,BOAR_STRIPE_L)
    # 花纹暗色（身体）
    lsp(7,2,BOAR_STRIPE)
    # 耳朵
    lfl(5,5, 9,10, BOAR_STRIPE_L); lsp(10,6,BOAR_STRIPE_L)
    lfl(5,5, 14,15, BOAR_STRIPE_L); lsp(14,6,BOAR_STRIPE_L)
    lsp(9,5,BOAR_STRIPE_L); lsp(9,6,BOAR)
    lsp(15,5,BOAR_STRIPE_L); lsp(15,6,BOAR)
    lsp(17,6,GROUND)
    # 鼻吻
    lfl(8,10, 10,14, BOAR_SN)
    lsp(10,8,BOAR_L)
    lsp(11,9,NOSTRIL); lsp(13,9,NOSTRIL)
    lsp(10,10,BOAR_SN); lsp(12,10,BOAR_SN); lsp(14,10,BOAR_SN)
    # 獠牙
    lsp(9,10,BOAR_TK); lsp(15,10,BOAR_TK)
    # 眼睛
    lsp(10,8,BOAR_EY); lsp(14,8,BOAR_EY)
    # 背部花纹（顶层）
    for _bx in range(10,12): lsp(_bx,4,BOAR_STRIPE)
    for _bx in range(6,9): lsp(_bx,2,BOAR_B)
    for _bx in range(8,10): lsp(_bx,3,BOAR_STRIPE)
    lsp(5,2,BOAR_STRIPE); lsp(6,2,BOAR_STRIPE)
    lsp(7,2,BOAR_STRIPE); lsp(9,3,BOAR_STRIPE)
    lsp(0,6,BOAR_STRIPE_L)  # (8,26) 花纹亮色
    lsp(1,6,BOAR_STRIPE_L)  # (9,26) 花纹亮色
    lsp(11,4,BOAR_B)  # (19,24) 身体主色
    lsp(11,5,(108,85,65))  # (19,25) 花纹暗色（身体顶层）
    lsp(12,5,BOAR_B)  # (20,25) 身体主色（顶层覆盖）
    lsp(1,9,BOAR_L)  # (9,29) 腿色

# 野猪1：左前景，向右
draw_boar(8, 20, 'right')
# 野猪2：右前景，向左
draw_boar(32, 21, 'left')

# ── 两侧茂密杜鹃花枝 ──
def dense_aza(x1, x2, top_y, bottom_y, side='left'):
    """茂密叶墙，不规则上边缘，通到底部"""
    import random
    rng = random.Random(99)
    # 不规则上边缘：每列随机偏移
    col_tops = {}
    for x in range(x1, x2+1):
        col_tops[x] = top_y + rng.randint(0, 4)
    # 每行的侧边缘也随机缩进
    row_indent = {}
    for y in range(top_y-3, bottom_y+1):
        row_indent[y] = rng.randint(0, 2)
    # 叶子填充（左右边缘不齐）
    for x in range(x1, x2+1):
        for y in range(col_tops.get(x, top_y), bottom_y+1):
            indent = row_indent.get(y, 0)
            if side == 'left' and x > x2 - indent:
                continue
            if side == 'right' and x < x1 + indent:
                continue
            if rng.random() < 0.3:
                sp(x, y, AZA_LEAF_D)
            else:
                sp(x, y, AZA_LEAF)
    # 上边缘额外凸起（有机感）
    for x in range(x1, x2+1):
        ty = col_tops.get(x, top_y)
        if rng.random() < 0.4:
            sp(x, ty-1, AZA_LEAF)
        if rng.random() < 0.2:
            sp(x, ty-2, AZA_LEAF_D)
    # 点缀明显花朵
    offsets = [-2, 2, -1, 3, 0, -3, 1, -1, 2, -2]
    for i, fy in enumerate(range(top_y+3, bottom_y-2, 4)):
        fx = (x1+x2)//2 + offsets[i % len(offsets)]
        for dx, dy in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0)]:
            sp(fx+dx, fy+dy, AZA_P)
        sp(fx, fy, AZA_PD)
        for dx, dy in [(0,-2),(-2,-1),(2,-1)]:
            sp(fx+dx, fy+dy, AZA_PL)

# 左侧：从y=8开始（留天空），通到底部y=35
dense_aza(0, 7, 8, 35, 'left')
# 右侧
dense_aza(56, 63, 8, 35, 'right')

# 地面低矮花丛（中间点缀）
def azalea(cx, cy):
    for dx, dy in [(-2,1),(-1,2),(0,2),(1,2),(2,1),(-2,0),(2,0),(0,3),(1,3),(-1,3)]:
        sp(cx+dx, cy+dy, AZA_LEAF)
    for dx, dy in [(-1,1),(0,1),(1,1)]:
        sp(cx+dx, cy+dy, AZA_LEAF_D)
    for dx, dy in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0)]:
        sp(cx+dx, cy+dy, AZA_P)
    sp(cx, cy, AZA_PD)
    for dx, dy in [(0,-2),(-2,-1),(2,-1)]:
        sp(cx+dx, cy+dy, AZA_PL)

# 地面花暂时去掉


# 两猪中间小土堆
DIRT   = (148, 118,  78)
DIRT_D = (118,  92,  58)
DIRT_L = (178, 148, 105)
# 土堆1 x=34, y=28
for dx,dy in [(0,0),(1,0),(-1,0),(2,0),(-2,0),(0,-1),(1,-1),(-1,-1)]:
    sp(31+dx, 28+dy, DIRT)
sp(30,27,DIRT_D); sp(32,27,DIRT_D); sp(31,27,DIRT_L)
# 土堆2 x=39, y=29
for dx,dy in [(0,0),(1,0),(-1,0),(2,0),(0,-1),(1,-1)]:
    sp(36+dx, 29+dy, DIRT)
sp(35,28,DIRT_D); sp(37,28,DIRT_D); sp(36,28,DIRT_L)
# 土堆3 x=30, y=29（小）
for dx,dy in [(0,0),(1,0),(-1,0),(0,-1)]:
    sp(27+dx, 29+dy, DIRT)
sp(27,28,DIRT_L)
# 额外小土堆
for dx,dy in [(0,0),(1,0),(-1,0),(0,-1)]:
    sp(33+dx, 31+dy, DIRT)
sp(33,30,DIRT_L)
for dx,dy in [(0,0),(1,0),(-1,0),(2,0),(-2,0),(0,-1),(1,-1)]:
    sp(40+dx, 26+dy, DIRT)
sp(39,25,DIRT_D); sp(41,25,DIRT_D); sp(40,25,DIRT_L)
for dx,dy in [(0,0),(1,0),(-1,0),(0,-1)]:
    sp(29+dx, 32+dy, DIRT)
sp(29,31,DIRT_L)
for dx,dy in [(0,0),(1,0),(-1,0),(2,0),(-2,0),(0,-1),(1,-1)]:
    sp(38+dx, 33+dy, DIRT)
sp(37,32,DIRT_D); sp(39,32,DIRT_D); sp(38,32,DIRT_L)
sp(6, 12, TREE_G)  # 屋檐遮树叶修正
fl(17, 18, 35, 37, HAT_RED)
wrow(17, 35, 37, HAT_RED)
# ── 渲染 ──
img = Image.new('RGB', (W*S, H*S))
px = img.load()
for y in range(H):
    for x in range(W):
        c = canvas[y][x]
        for dy in range(S):
            for dx in range(S):
                px[x*S+dx, y*S+dy] = c

img.save('pixel_boar.png')
print(f'Saved: {W*S}x{H*S}px')
