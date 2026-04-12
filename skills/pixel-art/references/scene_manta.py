from PIL import Image

W, H, S = 64, 36, 12

def set_px(c, x, y, col):
    if 0 <= x < W and 0 <= y < H:
        c[y][x] = list(col)

def fill(c, y1, y2, x1, x2, col):
    for y in range(y1, y2):
        for x in range(x1, x2):
            set_px(c, x, y, col)

def wrow(c, y, x1, x2, col):
    for x in range(x1, x2+1):
        set_px(c, x, y, col)

def blend(a, b, t):
    return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

# ── Colors ────────────────────────────────────────────────────────────────────
# 水色：动森风，深处偏暖墨绿，中层清蓝绿
DEEP      = (12,  48,  52)
MID       = (22, 102, 108)
SURF      = (38, 148, 142)
SURF_LT   = (62, 188, 175)
MOON_BEAM = (155, 218, 210)

# 魔鬼鱼：动森深蓝紫，偏暖
MANTA_DK  = (32,  38,  80)
MANTA_MID = (52,  72, 128)
MANTA_WH  = (215, 235, 242)
MANTA_GLO = (65, 195, 228)
MANTA_HI  = (185, 235, 248)

BUBBLE    = (105, 175, 228)

GB        = (185, 108, 48)
GBD       = (110, 65,  22)
GBE       = (62,  35,  15)
GB_CHEEK  = (225, 148, 95)
GB_ICING  = (245, 232, 210)
HAT_RED   = (198, 42,  32)
HAT_DARK  = (140, 26,  20)
HAT_LITE  = (225, 72,  55)

BUN       = (95,  158, 215)
BUN_LT    = (145, 195, 240)
BUND      = (55,  105, 165)
BUNE      = (38,  22,  60)
BUN_BLUSH = (235, 155, 172)
BUN_SMILE = (242, 235, 220)

SUIT      = (35, 58, 100)
TANK      = (72, 88, 108)

def draw():
    canvas = [[list(DEEP)]*W for _ in range(H)]

    # ── 水体渐变 ──────────────────────────────────────────────────────────────
    for y in range(H):
        t = y / (H-1)
        col = blend(MID, DEEP, t**0.7)
        wrow(canvas, y, 0, W-1, col)

    # ── 水中亮杂质（浮游粒子感，有亮有暗）─────────────────────────────────────
    specks = [
        (8,6,(165,198,218)),(18,11,(118,162,192)),(45,8,(178,210,228)),(55,14,(105,155,185)),
        (11,18,(148,188,210)),(28,15,(128,172,200)),(38,22,(182,212,232)),(58,20,(100,152,180)),
        (3,25,(135,178,205)),(14,28,(112,158,188)),(22,24,(170,205,225)),(35,27,(122,168,195)),
        (50,26,(155,192,215)),(60,29,(108,155,182)),(7,32,(132,175,200)),(16,33,(168,205,225)),
        (42,30,(112,158,185)),(53,34,(178,210,230)),(25,35,(125,168,195)),(63,9,(155,192,215)),
        (30,19,(105,152,180)),(47,23,(175,208,228)),(2,15,(140,182,208)),(57,31,(115,162,188)),
    ]
    for sx, sy, sc in specks:
        set_px(canvas, sx, sy, sc)

    # ── 月光光柱（已去掉）────────────────────────────────────────────────────

    # 光带已去掉

    # caustics 已去掉

    # ── 小鱼群（三角形构成，在光晕之前画）───────────────────────────────────
    FISH_BASE = (38, 98, 115)
    def draw_fish(cx, cy, d):
        wrow(canvas, cy-1, cx+1, cx+3, FISH_BASE)
        wrow(canvas, cy,   cx,   cx+4, FISH_BASE)
        wrow(canvas, cy+1, cx+1, cx+3, FISH_BASE)
        water_eye = tuple(canvas[cy][cx+3 if d==1 else cx+2])  # 镂空用当前水色
        if d == 1:
            set_px(canvas, cx+3, cy, water_eye)
            set_px(canvas, cx-1, cy-1, FISH_BASE)
            set_px(canvas, cx-1, cy+1, FISH_BASE)
        else:
            set_px(canvas, cx+1, cy, water_eye)
            set_px(canvas, cx+5, cy-1, FISH_BASE)
            set_px(canvas, cx+5, cy+1, FISH_BASE)

    fish_list = [
        (53, 23, -1),(49, 29, -1),(54, 32, -1),
        (5,  24,  1),(8,  30,  1),(3,  31,  1),
        (20, 31, 1),
    ]
    for fx, fy, d in fish_list:
        draw_fish(fx, fy, d)

    # ── 顶部光晕（6层，每层12格）────────────────────────────────────────
    LIGHT_HI = (140, 200, 235)
    for y in range(H):
        for x in range(W):
            dist = ((x - 32)**2 + y**2) ** 0.5
            if   dist < 6:  t = 0.60
            elif dist < 18: t = 0.45
            elif dist < 30: t = 0.32
            elif dist < 42: t = 0.20
            elif dist < 54: t = 0.12
            elif dist < 66: t = 0.06
            else:            t = 0
            if t > 0:
                canvas[y][x] = list(blend(tuple(canvas[y][x]), LIGHT_HI, t))

    # ── 魔鬼鱼（背景，更大，MX=32，MY=14）──────────────────────────────────
    MX, MY = 32, 15

    wing_shape = {
        MY-9: (2, 7),
        MY-8: (2, 8),
        MY-7: (2, 12),
        MY-6: (3, 16),
        MY-5: (4, 19),
        MY-4: (4, 22),
        MY-3: (4, 24),
        MY-2: (4, 25),
        MY-1: (4, 25),
        MY:   (4, 25),
        MY+1: (4, 24),
        MY+2: (4, 22),
        MY+3: (3, 19),
        MY+4: (3, 15),
        MY+5: (2, 10),
        MY+6: (1, 6),
        MY+7: (1, 3),
    }
    MANTA_WING = (185, 210, 230)  # 比 MANTA_WH 稍暗一点
    for y, (inner, outer) in wing_shape.items():
        wrow(canvas, y, MX-outer, MX+outer, MANTA_WING)   # 整体填翼色
        # 外缘深色轮廓
        set_px(canvas, MX-outer, y, MANTA_MID)
        set_px(canvas, MX+outer, y, MANTA_MID)

    # 中心深色（背部）
    belly = {
        MY-6: (1, 1), MY-5: (2, 2), MY-4: (3, 3), MY-3: (4, 4), MY-2: (5, 5), MY-1: (5, 5),
        MY:   (5, 5), MY+1: (5, 5), MY+2: (4, 4), MY+3: (3, 3), MY+4: (2, 2),
    }
    for y, (x1, x2) in belly.items():
        wrow(canvas, y, MX-x1, MX+x2, MANTA_WH)

    # 头部
    STRIPE_C = (130, 158, 182)
    wrow(canvas, MY-6, MX-1, MX+1, STRIPE_C)
    set_px(canvas, MX-3, MY-8, STRIPE_C); set_px(canvas, MX-2, MY-8, STRIPE_C)
    set_px(canvas, MX+2, MY-8, STRIPE_C); set_px(canvas, MX+3, MY-8, STRIPE_C)
    set_px(canvas, MX-2, MY-7, STRIPE_C); set_px(canvas, MX+2, MY-7, STRIPE_C)
    # 牛角头鳍（向内弯曲，尖端朝中间）
    for dx, dy in [(-4,-8),(-4,-9),(-4,-10),(-3,-11),(-2,-11)]:  # 左角
        set_px(canvas, MX+dx, MY+dy, MANTA_WING)
    for dx, dy in [(4,-8),(4,-9),(4,-10),(3,-11),(2,-11)]:         # 右角
        set_px(canvas, MX+dx, MY+dy, MANTA_WING)

    # 肚子纹路（6条，顶部2条↔底部2条对调，中间2条不变）
    stripe_color = (165, 192, 215)
    # 原始：(y=MY-1,x_off=0), (y=MY+1,x_off=1), (y=MY+3,x_off=2)
    # 对调后：顶行用底的x_off，底行用顶的x_off，中间不变
    stripes = [
        (MY-4, 2),  # 顶行，改用x_off=2（原底）
        (MY-2, 1),  # 中行，不变
        (MY,   0),  # 底行，改用x_off=0（原顶）
    ]
    for sy, x_off in stripes:
        for dx in range(1, 5):
            set_px(canvas, MX - dx - x_off, sy, stripe_color)
            set_px(canvas, MX + dx + x_off, sy, stripe_color)
    # 尾巴（根部亮蓝过渡，渐变黑色，左侧加蓝边）
    tail = [(1,5),(1,6),(1,7),(1,8),(2,9),(2,10),(2,11),(2,12),(3,13),(3,14),(3,15),(3,16),(3,17)]
    for i, (dx, dy) in enumerate(tail):
        col = MANTA_WH
        set_px(canvas, MX+dx, MY+dy, col)
        # 衔接处（dy=5~7）左边改白，dy=8保留蓝，其余也蓝
        edge_col = MANTA_WH if dy <= 7 else MANTA_GLO
        set_px(canvas, MX+dx-1, MY+dy, edge_col)
    for y, (inner, outer) in wing_shape.items():
        set_px(canvas, MX-outer, y, MANTA_GLO)
        set_px(canvas, MX+outer, y, MANTA_GLO)
        if outer > 1:
            set_px(canvas, MX-outer+1, y, MANTA_HI)
            # 尾巴根部 MY+5~MY+7 右侧亮点与尾巴重叠，跳过
            if y <= MY+4:
                set_px(canvas, MX+outer-1, y, MANTA_HI)
    # 翅尖高光
    set_px(canvas, MX-23, MY-1, MANTA_HI); set_px(canvas, MX-23, MY, MANTA_HI)
    set_px(canvas, MX+23, MY-1, MANTA_HI); set_px(canvas, MX+23, MY, MANTA_HI)
    for dx, dy in [(-16,-1),(-11,0),(-6,-1),(6,-2),(11,-1)]:
        set_px(canvas, MX+dx, MY+dy, MANTA_HI)

    # 气泡已去掉

    # ── 姜饼人（前景，GCX=13，正面）────────────────────────────────────────
    GCX, GY = 23, 16
    # 帽子（右移1格）
    HX = GCX + 1
    set_px(canvas, HX, GY-2, HAT_DARK)
    for dx in range(-2, 3): set_px(canvas, HX+dx, GY-1, HAT_RED)
    for dx in range(-2, 3): set_px(canvas, HX+dx, GY,   HAT_RED)
    set_px(canvas, HX, GY-1, HAT_LITE)
    set_px(canvas, HX-2, GY-1, HAT_DARK); set_px(canvas, HX+2, GY-1, HAT_DARK)
    # 脸（正面对称）
    fill(canvas, GY+1, GY+6, GCX-3, GCX+4, GB)
    # 潜水镜（圆角长方形框，镜片内肤色变亮）
    GOGGLE = (45, 45, 45)
    GOGGLE_IN = (215, 168, 108)  # 亮版肤色
    for gy in range(GY+1, GY+4):
        wrow(canvas, gy, GCX-3, GCX+3, GOGGLE_IN)
    # 眼睛盖在镜片上
    set_px(canvas, GCX-2, GY+2, GBE); set_px(canvas, GCX+2, GY+2, GBE)
    # 镜框
    wrow(canvas, GY,   GCX-3, GCX+3, GOGGLE)
    wrow(canvas, GY+4, GCX-3, GCX-1, GOGGLE); wrow(canvas, GY+4, GCX+1, GCX+3, GOGGLE)
    set_px(canvas, GCX, GY+3, GOGGLE)  # 底边中间上移一格
    for gy in range(GY+1, GY+4):
        set_px(canvas, GCX-4, gy, GOGGLE)
        set_px(canvas, GCX+4, gy, GOGGLE)
    # 呼吸管（L型，姜饼人左侧）
    TUBE = (45, 45, 45)
    for gy in range(GY-2, GY+2):
        set_px(canvas, GCX-6, gy, TUBE)
    set_px(canvas, GCX-5, GY+2, TUBE)
    # 身体
    fill(canvas, GY+6, GY+10, GCX-2, GCX+3, GB)
    set_px(canvas, GCX, GY+7, GB_ICING)
    # 腿（正面，两腿对称）
    wrow(canvas, GY+10, GCX-2, GCX-1, GB); wrow(canvas, GY+10, GCX+1, GCX+2, GB)
    # 手臂（两侧）
    set_px(canvas, GCX-3, GY+7, GB); set_px(canvas, GCX-4, GY+7, GB)
    set_px(canvas, GCX+3, GY+7, GB); set_px(canvas, GCX+4, GY+7, GB)

    # ── 蓝兔子（前景，BCX=51，正面）────────────────────────────────────────
    BCX, BY = 41, 16
    # 耳朵（正面，两耳对称）
    for ey in range(BY-4, BY+1):
        set_px(canvas, BCX-2, ey, BUN); set_px(canvas, BCX-1, ey, BUN_LT)
        set_px(canvas, BCX+1, ey, BUN); set_px(canvas, BCX+2, ey, BUN_LT)
    # 脸（正面对称）
    fill(canvas, BY+1, BY+6, BCX-3, BCX+4, BUN)
    set_px(canvas, BCX-1, BY+1, BUN_LT); set_px(canvas, BCX+1, BY+1, BUN_LT)
    set_px(canvas, BCX-2, BY+2, BUNE); set_px(canvas, BCX+2, BY+2, BUNE)
    set_px(canvas, BCX-3, BY+3, BUN_BLUSH); set_px(canvas, BCX+3, BY+3, BUN_BLUSH)
    set_px(canvas, BCX-1, BY+4, BUN_SMILE); set_px(canvas, BCX, BY+4, BUN_SMILE); set_px(canvas, BCX+1, BY+4, BUN_SMILE)
    # 面镜
    BGOGGLE = (45, 45, 45)
    BGOGGLE_IN = (148, 188, 215)  # 淡蓝色
    for gy in range(BY+1, BY+4):
        wrow(canvas, gy, BCX-3, BCX+3, BGOGGLE_IN)
    set_px(canvas, BCX-2, BY+2, BUNE); set_px(canvas, BCX+2, BY+2, BUNE)
    wrow(canvas, BY,   BCX-3, BCX+3, BGOGGLE)
    wrow(canvas, BY+4, BCX-3, BCX-1, BGOGGLE); wrow(canvas, BY+4, BCX+1, BCX+3, BGOGGLE)
    set_px(canvas, BCX, BY+3, BGOGGLE)  # 底边中间上移一格
    for gy in range(BY+1, BY+4):
        set_px(canvas, BCX-4, gy, BGOGGLE)
        set_px(canvas, BCX+4, gy, BGOGGLE)
    # 兔子呼吸管（L型，右侧）
    BTUBE = (45, 45, 45)
    for gy in range(BY-2, BY+2):
        set_px(canvas, BCX+6, gy, BTUBE)
    set_px(canvas, BCX+5, BY+2, BTUBE)
    # 身体
    fill(canvas, BY+6, BY+10, BCX-2, BCX+3, BUN)
    # 腿
    wrow(canvas, BY+10, BCX-2, BCX-1, BUN); wrow(canvas, BY+10, BCX+1, BCX+2, BUN)
    # 手臂（两侧）
    set_px(canvas, BCX-3, BY+7, BUN); set_px(canvas, BCX-4, BY+7, BUN)
    set_px(canvas, BCX+3, BY+7, BUN); set_px(canvas, BCX+4, BY+7, BUN)

    # ── 小鱼（已移至光晕之前）────────────────────────────────────────────────

    # ── 输出 ─────────────────────────────────────────────────────────────────
    img = Image.new('RGB', (W*S, H*S))
    pixels = img.load()
    for y in range(H):
        for x in range(W):
            col = tuple(canvas[y][x])
            for dy in range(S):
                for dx in range(S):
                    pixels[x*S+dx, y*S+dy] = col
    img.save('pixel_manta.png')
    print(f"Saved: {W*S}×{H*S}px")

draw()
