from PIL import Image

W, H = 64, 36
S = 12

# ── 颜色 ──
SKY       = (178, 210, 235)
WALL      = (238, 228, 210)
WALL_D    = (210, 198, 178)
ROOF      = (148, 108,  78)
ROOF_D    = (118,  85,  58)
WIN_FRAME = (142, 108,  72)
WIN_FRAME_D=(108,  80,  52)
WIN_IN    = ( 85,  95, 108)

GROUND    = (148, 178, 105)
GROUND_D  = (118, 148,  82)
GROUND_L  = (175, 205, 128)

AZA_P     = (225,  95, 148)
AZA_PD    = (185,  65, 118)
AZA_PL    = (248, 148, 185)
AZA_LEAF  = ( 72, 128,  58)
AZA_LEAF_D=( 52,  98,  42)
AZA_W     = (248, 225, 235)

BOAR      = ( 88,  72,  62)
BOAR_L    = (118,  98,  85)
BOAR_LT   = (155, 132, 112)
BOAR_B    = (168, 145, 125)
BOAR_SN   = (205, 158, 138)
BOAR_EY   = ( 22,  15,  10)
EYE_W     = (245, 242, 238)
BOAR_TK   = (238, 225, 192)
NOSTRIL   = ( 55,  38,  28)

BUN_BODY  = ( 95, 158, 215)
BUN_INNER = (210, 168, 190)
BUN_EYE   = ( 38,  22,  60)
HAT_RED   = (198,  42,  32)
HAT_DARK  = (140,  26,  20)
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

# ── 屋顶下沿（y=6~7） ──

# ── 房子墙面（y=8~22） ──
fl(8, 21, 18, 63, WALL)

# 左侧绿树（房子左方天空区）
TREE_G  = ( 32,  75,  32)   # 绿色主色
TREE_GD = ( 22,  55,  22)   # 深绿
TREE_GL = ( 48,  98,  42)   # 亮绿
TREE_WH = (245, 245, 240)   # 白花
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
for x,y in [(15,16),(10,17),(16,18),(7,18),(13,20),(8,19),(14,21),(9,21),(12,15),(6,16)]:
    sp2(x,y,TREE_GD)
# 亮绿高光
for x,y in [(13,15),(8,16),(11,17),(15,19),(6,18)]:
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
        canvas[_ry][_rx] = (80, 160, 80)

# 门（窗户右边）
DOOR_F = WIN_FRAME
DOOR_D = WIN_FRAME_D
DOOR_IN_UP = WIN_IN
DOOR_IN_LO = ROOF
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
sp(DX1+1, (DY1+DY2)//2, DOOR_D)

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
for y in range(WY1+1, WY2): sp(MX, y, WIN_FRAME)
# 屋顶材质（瓦片横纹）
for _ry in range(5, 12):
    _rx_left = round(18 - 8*(_ry-5)/6)
    _offset = (_ry % 2) * 3
    for _rx in range(_rx_left, 64):
        if canvas[_ry][_rx] == (80, 160, 80):
            # 每隔4格一道暗色竖缝（错位）
            if (_rx - _offset) % 4 == 0:
                canvas[_ry][_rx] = (55, 130, 55)
            # 偶数行底边暗一格
            elif _ry % 2 == 1:
                canvas[_ry][_rx] = (65, 145, 65)
wrow(11, 10, 63, ROOF)
wrow(12, 10, 63, ROOF_D)

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
fl(17, 19, 35, 38, HAT_RED)
wrow(17, 35, 38, HAT_DARK)
sp(38, 17, WIN_IN)
sp(38, 15, WIN_IN)
sp(36, 16, HAT_LITE)
fl(18, 19, 33, 38, GB_BODY)
sp(33, 18, WIN_IN); sp(38, 18, WIN_IN)
sp(34, 19, BUN_EYE); sp(36, 19, BUN_EYE)

# ── 地面（y=22~35） ──
fl(22, 35, 0, 63, GROUND)
wrow(22, 0, 63, GROUND_L)
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
    lfl(3,10, 0,10, BOAR_B)
    lfl(1,10, 2,9, BOAR_B)
    lsp(6,1,BOAR_B); lsp(9,4,BOAR_B)
    for lx,ly in [(2,1),(9,1),(1,2),(1,3),(1,10),(2,10),(0,10)]: lsp(lx,ly,GROUND)
    # 腿（3条，2格高）
    lfl(10,12, 1,2, BOAR_B)
    lfl(10,12, 7,8, BOAR_B)
    lfl(10,12, 13,14, BOAR_B)
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
    back_offsets = {0:0, 1:0, 2:-1, 3:-1, 4:-2, 5:-2, 6:-1, 7:-1, 8:0}
    for sx in range(0, 9):
        boff = back_offsets.get(sx, 0)
        lsp(sx, 3+boff, BOAR_STRIPE)
        lsp(sx, 2+boff, BOAR_STRIPE_L)
    # 头（最后画，盖身体/花纹）
    lfl(4,10, 7,17, BOAR_L)
    for lx,ly in [(17,4),(17,10)]: lsp(lx,ly,GROUND)
    for _ly in range(4,11): lsp(17,_ly,GROUND)
    lsp(7,4,BOAR_B); lsp(7,10,BOAR_B); lsp(7,5,BOAR_B)
    # 耳朵
    lfl(2,4, 8,10, BOAR_LT)
    lfl(2,4, 14,16, BOAR_LT)
    lsp(9,3,BOAR); lsp(9,4,BOAR); lsp(8,3,BOAR)
    lsp(15,3,BOAR); lsp(16,3,BOAR); lsp(15,4,BOAR)
    lsp(16,4,GROUND); lsp(17,5,GROUND)
    # 鼻吻
    lfl(7,9, 10,14, BOAR_SN)
    lsp(10,7,BOAR_L)
    lsp(11,8,NOSTRIL); lsp(13,8,NOSTRIL)
    lsp(10,9,BOAR_SN); lsp(12,9,BOAR_SN); lsp(14,9,BOAR_SN)
    # 獠牙
    lsp(9,9,BOAR_TK); lsp(15,9,BOAR_TK)
    # 眼睛
    lsp(10,7,BOAR_EY); lsp(14,7,BOAR_EY)

# 野猪1：左前景，向右
draw_boar(8, 20, 'right')
# 野猪2：右前景，向左
draw_boar(28, 21, 'left')

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
    for fy in range(top_y+3, bottom_y-2, 5):
        fx = (x1+x2)//2 + rng.randint(-1, 1)
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
