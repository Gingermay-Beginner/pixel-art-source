"""
pixel_volcano.py — 火山夜景像素画
May 的像素画项目，场景：火山口旁姜饼人+蓝兔子牵手

当前版本：wes71
用法：python3 pixel_volcano.py
输出：pixel_volcano.png
"""

from PIL import Image
import math
import statistics

# ─────────────────────────────────────────────
# 画布
# ─────────────────────────────────────────────
W, H   = 64, 36   # 格子数（16:9）
SCALE  = 12       # 每格放大 px，最终 768×432

# ─────────────────────────────────────────────
# 天空配色（AC 动森夜景风）
# ─────────────────────────────────────────────
SKY_TOP    = (14,  16,  68)   # 深靛蓝（顶部）
SKY_MID    = (32,  42, 108)   # 中蓝偏紫
SKY_LOW    = (62,  42,  88)   # 蓝紫过渡
HORIZON    = (118, 68,  72)   # 暖粉红棕（地平线）
CLOUD_LIT  = (175,185, 228)   # 月亮周围晕染

# ─────────────────────────────────────────────
# 地面
# ─────────────────────────────────────────────
GROUND_A = (58, 40, 22)
GROUND_B = (72, 52, 30)
GROUND_C = (40, 28, 14)

# ─────────────────────────────────────────────
# 月亮 & 星星
# ─────────────────────────────────────────────
MOON_Y = (255, 245, 185)
STAR   = (255, 252, 200)
STAR2  = (210, 220, 255)

# 月亮位置
MCX, MCY, MR = 9, 7, 3

# 星星列表（x, y, color），13 颗
STARS = [
    (3,  2,  STAR),  (61, 2,  STAR2),
    (20, 5,  STAR),  (44, 5,  STAR2), (57, 6,  STAR),
    (2,  11, STAR),  (16, 9,  STAR2), (48, 10, STAR),  (62, 11, STAR2),
    (5,  17, STAR2), (22, 16, STAR),  (42, 16, STAR2), (59, 17, STAR),
]

# ─────────────────────────────────────────────
# 火山
# ─────────────────────────────────────────────
VOLC_D     = (42, 24, 16)
VOLC_M     = (62, 36, 22)
VOLC_HL    = (72, 46, 28)
VOLC_SH    = (22, 12,  8)
VOLC_RIDGE = (55, 35, 20)

CRATER_CENTER = (255, 155, 38)
CRATER_MID    = (220,  95, 20)
CRATER_INNER  = ( 85,  28,  6)
CRATER_LAVA   = (210,  72, 18)

# 火山口参数
VPX, VPY       = 32, 14   # 火山顶点
CRATER_Y       = VPY + 3  # = 17
CRATER_HALF    = 4         # 口沿半宽

# 暖光截止线：y >= WARM_GLOW_YMAX 的火山格不染橙
WARM_GLOW_YMAX = 19

# ─────────────────────────────────────────────
# 烟雾色板
# ─────────────────────────────────────────────
SMK1 = (155, 75,  28)
SMK2 = (112, 82,  65)
SMK3 = ( 78, 85, 118)
SMK4 = ( 58, 68, 108)
SMK5 = ( 44, 55,  95)

# ─────────────────────────────────────────────
# 灯笼
# ─────────────────────────────────────────────
LANTERN_FRAME = (165, 125,  55)
LANTERN_GLOW  = (255, 235, 115)
LANTERN_WARM  = (255, 205,  75)
L_LEFT  = (21, 29)   # 灯笼左中心（格子坐标）
L_RIGHT = (43, 29)   # 灯笼右中心
LANTERN_EXEMPT_R = 4.5  # 灯笼光晕豁免半径

# ─────────────────────────────────────────────
# 角色：姜饼人（May）
# ─────────────────────────────────────────────
GB_BODY  = (185, 108,  48)
GB_ICING = (245, 232, 210)
GB_EYE   = ( 62,  35,  15)
GB_CHEEK = (225, 148,  95)

# ─────────────────────────────────────────────
# 角色：蓝兔子（男友）
# ─────────────────────────────────────────────
BUN_BODY  = ( 95, 158, 215)
BUN_LT    = (145, 195, 240)
BUN_INNER = (210, 168, 190)
BUN_EYE   = ( 38,  22,  60)
BUN_BLUSH = (235, 155, 172)
BUN_SMILE = (242, 235, 220)

# ─────────────────────────────────────────────
# 角色构图参数
# ─────────────────────────────────────────────
SKY_BAND   = 23
HORIZ_BAND = 24
GROUND_TOP = 28
GROUND_ROW = 32

CENTER = W // 2       # = 32
GAP    = 5
GB_CX  = CENTER - GAP  # = 27
BUN_CX = CENTER + GAP  # = 37
FIG_Y  = GROUND_ROW + 5  # = 37
MID    = (GB_CX + BUN_CX) // 2  # = 32

# 压暗参数（角色周边背景格）
DARK = (18, 10, 5)

# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────
def blend(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3))

def brightness(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]

def set_px(canvas, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        canvas[y][x] = color

def draw_pixel_puff(canvas, cx, cy, w, h, color):
    """硬边像素烟雾块：主矩形 + 顶部宽凸起 + 更窄顶尖"""
    for py in range(cy, cy + h):
        for px in range(cx - w, cx + w + 1):
            if 0 <= px < W and 0 <= py < H:
                canvas[py][px] = color
    for px in range(cx - w + 1, cx + w):
        if 0 <= px < W and 0 <= cy - 1 < H:
            canvas[cy - 1][px] = color
    for px in range(cx - w // 2, cx + w // 2 + 1):
        if 0 <= px < W and 0 <= cy - 2 < H:
            canvas[cy - 2][px] = color

def is_lantern_zone(x, y):
    d1 = math.sqrt((x - L_LEFT[0]) ** 2  + (y - L_LEFT[1]) ** 2)
    d2 = math.sqrt((x - L_RIGHT[0]) ** 2 + (y - L_RIGHT[1]) ** 2)
    return d1 <= LANTERN_EXEMPT_R or d2 <= LANTERN_EXEMPT_R

def is_crater_zone(x, y):
    return y <= CRATER_Y + 2 and abs(x - VPX) <= CRATER_HALF + 2

def is_ear_tip_zone(x, y):
    return (BUN_CX - 2 <= x <= BUN_CX + 4) and y <= FIG_Y - 17

# ─────────────────────────────────────────────
# 绘制
# ─────────────────────────────────────────────
def draw():
    canvas = [[SKY_TOP] * W for _ in range(H)]

    # ── 天空 & 地面背景 ──
    for y in range(H):
        for x in range(W):
            if y <= SKY_BAND:
                canvas[y][x] = blend(SKY_TOP, SKY_MID, y / SKY_BAND)
            elif y <= HORIZ_BAND:
                canvas[y][x] = blend(SKY_MID, SKY_LOW,
                                     (y - SKY_BAND) / (HORIZ_BAND - SKY_BAND))
            elif y < GROUND_TOP:
                canvas[y][x] = blend(SKY_LOW, HORIZON,
                                     (y - HORIZ_BAND) / (GROUND_TOP - HORIZ_BAND))
            else:
                noise = (x * 7 + y * 13 + x * y * 3) % 9
                if noise == 0:       canvas[y][x] = GROUND_B
                elif noise <= 2:     canvas[y][x] = GROUND_C
                else:                canvas[y][x] = GROUND_A

    # ── 火山体 ──
    volc_pixels = set()
    volc_half   = {}
    for y in range(VPY, GROUND_TOP):
        half = int((y - VPY) * 2.2)
        volc_half[y] = half
        for x in range(VPX - half, VPX + half + 1):
            if 0 <= x < W:
                volc_pixels.add((x, y))
                canvas[y][x] = blend(VOLC_D, VOLC_M, min(1, (y - VPY) / 10))

    # 火山底部过渡到地面
    for y in range(GROUND_TOP, GROUND_TOP + 2):
        half = int((GROUND_TOP - VPY) * 2.2)
        for x in range(VPX - half, VPX + half + 1):
            if 0 <= x < W:
                canvas[y][x] = blend(VOLC_M, GROUND_A, (y - GROUND_TOP) / 2)

    # 火山明暗、山脊
    EXPOSED_L = GB_CX + 3
    EXPOSED_R = BUN_CX - 3
    for y in range(VPY, GROUND_TOP):
        half = volc_half[y]
        if half == 0:
            continue
        for x in range(VPX - half, VPX + half + 1):
            if not (0 <= x < W):
                continue
            nx = (x - VPX) / half
            in_exposed = EXPOSED_L <= x <= EXPOSED_R
            if nx < -0.6:
                t = min(1, (-nx - 0.6) / 0.4)
                canvas[y][x] = blend(canvas[y][x], VOLC_HL, t * 0.35)
            elif nx > 0.55:
                t = min(1, (nx - 0.55) / 0.45)
                canvas[y][x] = blend(canvas[y][x], VOLC_SH, t * 0.45)
            depth   = (y - VPY) / max(1, GROUND_TOP - VPY)
            ridge_l = -0.35 + depth * 0.05
            ridge_r =  0.30 - depth * 0.05
            for ridge_pos, ridge_dir in [(ridge_l, -1), (ridge_r, 1)]:
                d_ridge = abs(nx - ridge_pos)
                if d_ridge < 0.08:
                    t_ridge = max(0, 1 - d_ridge / 0.08) * 0.28
                    col = (VOLC_HL if ridge_dir == -1 else VOLC_SH) if nx < ridge_pos \
                          else (VOLC_SH if ridge_dir == -1 else VOLC_RIDGE)
                    if in_exposed and col in (VOLC_HL, VOLC_RIDGE):
                        pass
                    else:
                        canvas[y][x] = blend(canvas[y][x], col, t_ridge)
            nv = (x * 17 + y * 13 + x * y * 7 + x * x * 3) % 16
            if in_exposed:
                if nv == 0: canvas[y][x] = blend(canvas[y][x], VOLC_SH, 0.18)
            else:
                if nv == 0:   canvas[y][x] = blend(canvas[y][x], VOLC_SH, 0.22)
                elif nv == 1: canvas[y][x] = blend(canvas[y][x], VOLC_HL, 0.12)

    # 火山边缘轮廓
    for y in range(VPY + 1, GROUND_TOP):
        lx = VPX - volc_half[y]
        rx = VPX + volc_half[y]
        for dx in range(0, 2):
            if 0 <= lx + dx < W:
                canvas[y][lx + dx] = blend(canvas[y][lx + dx], VOLC_HL, 0.28 - dx * 0.1)
        if 0 <= rx < W:
            canvas[y][rx] = blend(canvas[y][rx], VOLC_SH, 0.35)

    # ── 火山口暖光（y < WARM_GLOW_YMAX 才生效）──
    for y in range(HORIZ_BAND, GROUND_TOP + 1):
        if y >= WARM_GLOW_YMAX:
            continue
        for x in range(W):
            dx = abs(x - VPX)
            t = max(0, 0.55 - dx * 0.030) * max(0, 1 - (y - HORIZ_BAND) * 0.18)
            if t > 0:
                canvas[y][x] = blend(canvas[y][x], (145, 62, 25), t * 0.72)

    # ── 火山口口沿 ──
    volc_base_c = blend(VOLC_D, VOLC_M, min(1, (CRATER_Y - VPY) / 10))
    for dx in range(-CRATER_HALF, CRATER_HALF + 1):
        adx = abs(dx)
        rim = blend(CRATER_MID, CRATER_CENTER, 1 - adx * 0.18) if adx <= 2 \
              else blend(CRATER_MID, volc_base_c, (adx - 2) / (CRATER_HALF - 2))
        if (VPX + dx, CRATER_Y) in volc_pixels:
            canvas[CRATER_Y][VPX + dx] = rim

    # 内壁
    for di in range(1, 3):
        inner_half = CRATER_HALF - di * 2
        if inner_half < 0:
            break
        iy = CRATER_Y + di
        for dx in range(-inner_half, inner_half + 1):
            if (VPX + dx, iy) in volc_pixels:
                if abs(dx) == inner_half:
                    canvas[iy][VPX + dx] = blend(canvas[iy][VPX + dx], CRATER_MID, 0.5)
                else:
                    t_core = 1 - abs(dx) / max(inner_half, 1)
                    canvas[iy][VPX + dx] = blend(CRATER_LAVA, CRATER_INNER, t_core * 0.6)

    # 口沿光晕
    for dy in range(-2, 0):
        for dx in range(-CRATER_HALF, CRATER_HALF + 1):
            t = max(0, (1 - abs(dx) / CRATER_HALF) * 0.15 * (1 + dy * 0.3))
            cx2, cy2 = VPX + dx, CRATER_Y + dy
            if t > 0 and 0 <= cx2 < W and 0 <= cy2 < H:
                canvas[cy2][cx2] = blend(canvas[cy2][cx2], CRATER_CENTER, t)

    # ── 烟雾 ──
    smoke_base = CRATER_Y - 1
    puffs = [
        (0,  smoke_base-2,  2, 3, SMK1), (-1, smoke_base-4,  3, 3, SMK1),
        (1,  smoke_base-5,  3, 2, SMK2), (-2, smoke_base-7,  4, 3, SMK2),
        (2,  smoke_base-8,  4, 3, SMK2), (0,  smoke_base-9,  5, 3, SMK3),
        (-3, smoke_base-11, 5, 3, SMK3), (3,  smoke_base-12, 5, 3, SMK3),
        (-1, smoke_base-13, 6, 3, SMK4), (2,  smoke_base-14, 6, 3, SMK4),
        (-2, smoke_base-16, 7, 3, SMK4), (1,  smoke_base-17, 7, 3, SMK5),
        (-3, smoke_base-19, 8, 3, SMK5), (3,  smoke_base-20, 8, 3, SMK5),
        (0,  smoke_base-21, 8, 4, SMK5),
    ]
    for (ocx, top_y, hw, ht, col) in puffs:
        draw_pixel_puff(canvas, VPX + ocx, top_y, hw, ht, col)

    # ── 月亮 ──
    for y in range(MCY - MR - 1, MCY + MR + 2):
        for x in range(MCX - MR - 1, MCX + MR + 2):
            dx, dy = x - MCX, y - MCY
            d2 = dx * dx + dy * dy
            if d2 <= MR * MR and (x - MCX - 1) ** 2 + dy * dy > (MR - 1.1) ** 2:
                if dx == MR:
                    continue
                if 0 <= x < W and 0 <= y < H and canvas[y][x][0] < 130:
                    set_px(canvas, x, y, MOON_Y)

    # 月亮光晕
    for y in range(0, 18):
        for x in range(0, 24):
            dx, dy = x - MCX, y - MCY
            dist = math.sqrt(dx * dx + dy * dy)
            if 2.5 < dist < 11 and canvas[y][x][0] > 40:
                canvas[y][x] = blend(canvas[y][x], CLOUD_LIT,
                                     0.22 * (1 - (dist - 2.5) / 8.5))

    # ── 星星 ──
    for sx, sy, sc in STARS:
        if canvas[sy][sx][0] < 110:
            set_px(canvas, sx, sy, sc)
            for off in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx2, ny2 = sx + off[0], sy + off[1]
                if 0 <= nx2 < W and 0 <= ny2 < H:
                    set_px(canvas, nx2, ny2,
                           blend(canvas[ny2][nx2], sc, 0.28))

    # ── 灯笼光晕 ──
    def draw_lantern(lx, ly):
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < 3.2:
                    px2, py2 = lx + dx, ly + dy
                    t = max(0, 1 - dist / 3.2) * 0.55
                    if 0 <= px2 < W and 0 <= py2 < H:
                        canvas[py2][px2] = blend(canvas[py2][px2], LANTERN_WARM, t)
        set_px(canvas, lx,   ly - 1, LANTERN_FRAME)
        set_px(canvas, lx-1, ly,     LANTERN_FRAME)
        set_px(canvas, lx,   ly,     LANTERN_GLOW)
        set_px(canvas, lx+1, ly,     LANTERN_FRAME)
        set_px(canvas, lx-1, ly+1,   LANTERN_FRAME)
        set_px(canvas, lx,   ly+1,   LANTERN_GLOW)
        set_px(canvas, lx+1, ly+1,   LANTERN_FRAME)
        set_px(canvas, lx,   ly+2,   LANTERN_FRAME)

    draw_lantern(*L_LEFT)
    draw_lantern(*L_RIGHT)

    # ── 角色周边压暗（标记角色格 → 找邻近背景格 → 压暗偏亮的）──
    char_pixels = set()

    def mark(x, y):
        if 0 <= x < W and 0 <= y < H:
            char_pixels.add((x, y))

    gy = FIG_Y

    # 姜饼人占格
    cx = GB_CX
    for dx in [-1, 0, 1]:           mark(cx+dx, gy-16)
    for dx in [-2,-1, 0, 1, 2]:     mark(cx+dx, gy-15)
    for dx in range(-3, 4):
        for row in [gy-14,gy-13,gy-12,gy-9,gy-8,gy-7]: mark(cx+dx, row)
    for dx in [-2,-1, 0, 1, 2]:     mark(cx+dx, gy-11)
    for dx in [-1, 0, 1]:           mark(cx+dx, gy-10)
    for row in [gy-8, gy-9]:
        mark(cx-4, row); mark(cx-5, row)
        for ax in range(cx+4, MID): mark(ax, row)
    for dy2 in range(6, 9):
        for ddx in [-3,-2, 2, 3]:   mark(cx+ddx, gy-dy2)

    # 兔子占格
    cx = BUN_CX
    for y2 in range(gy-20, gy-15):
        for ddx in [-1, 0, 2, 3]:   mark(cx+ddx, y2)
    for dx in [-1, 0, 1]:           mark(cx+dx, gy-16)
    for dx in [-2,-1, 0, 1, 2]:     mark(cx+dx, gy-15)
    for dx in range(-3, 4):
        for row in [gy-14,gy-13,gy-12,gy-9,gy-8,gy-7]: mark(cx+dx, row)
    for dx in [-2,-1, 0, 1, 2]:     mark(cx+dx, gy-11)
    for dx in [-1, 0, 1]:           mark(cx+dx, gy-10)
    for row in [gy-8, gy-9]:
        mark(cx+4, row); mark(cx+5, row)
        for ax in range(MID, cx-3): mark(ax, row)
    for dy2 in range(6, 9):
        for ddx in [-3,-2, 2, 3]:   mark(cx+ddx, gy-dy2)

    # 邻近背景格
    adjacent = set()
    for (px2, py2) in char_pixels:
        for ddx in [-1, 0, 1]:
            for ddy in [-1, 0, 1]:
                if ddx == 0 and ddy == 0:
                    continue
                nx2, ny2 = px2 + ddx, py2 + ddy
                if (nx2, ny2) not in char_pixels and 0 <= nx2 < W and 0 <= ny2 < H:
                    adjacent.add((nx2, ny2))

    adj_filtered = [(x, y) for (x, y) in adjacent
                    if not is_crater_zone(x, y)
                    and not is_ear_tip_zone(x, y)
                    and not is_lantern_zone(x, y)]

    bvals = [brightness(canvas[y][x]) for (x, y) in adj_filtered]
    if bvals:
        avg_b = sum(bvals) / len(bvals)
        std_b = statistics.stdev(bvals) if len(bvals) > 1 else 0
        threshold = avg_b + 1.5 * std_b
        for (x, y) in adj_filtered:
            b = brightness(canvas[y][x])
            if b > threshold:
                excess = (b - threshold) / max(1, 200 - threshold)
                t = min(0.75, excess * 2.0)
                canvas[y][x] = blend(canvas[y][x], DARK, t)

    # y=19 行火山口附近额外压暗
    for x in range(VPX - 6, VPX + 7):
        if (x, 19) in volc_pixels and (x, 19) not in char_pixels:
            b = brightness(canvas[19][x])
            if b > 45:
                canvas[19][x] = blend(canvas[19][x], DARK, 0.65)

    # ── 绘制角色 ──
    HAT_RED  = (198, 42, 32)
    HAT_DARK = (140, 26, 20)
    HAT_LITE = (225, 72, 55)

    def draw_gingerbread(cx, gy):
        # 头
        for dx in [-1, 0, 1]:           set_px(canvas, cx+dx, gy-16, GB_BODY)
        for dx in [-2,-1, 0, 1, 2]:     set_px(canvas, cx+dx, gy-15, GB_BODY)
        for dx in range(-3, 4):
            for row in [gy-14,gy-13,gy-12]: set_px(canvas, cx+dx, row, GB_BODY)
        for dx in [-2,-1, 0, 1, 2]:     set_px(canvas, cx+dx, gy-11, GB_BODY)
        for dx in [-1, 0, 1]:           set_px(canvas, cx+dx, gy-10, GB_BODY)
        # 脸部细节
        set_px(canvas, cx-2, gy-14, GB_EYE);   set_px(canvas, cx+2, gy-14, GB_EYE)
        set_px(canvas, cx-3, gy-13, GB_CHEEK); set_px(canvas, cx+3, gy-13, GB_CHEEK)
        set_px(canvas, cx-2, gy-12, GB_EYE);   set_px(canvas, cx+2, gy-12, GB_EYE)
        set_px(canvas, cx-1, gy-11, GB_EYE);   set_px(canvas, cx, gy-11, GB_EYE);   set_px(canvas, cx+1, gy-11, GB_EYE)
        # 身体
        for dx in [-2,-1, 0, 1, 2]:     set_px(canvas, cx+dx, gy-9, GB_BODY)
        for dx in range(-3, 4):          set_px(canvas, cx+dx, gy-8, GB_BODY)
        for dx in [-2,-1, 0, 1, 2]:     set_px(canvas, cx+dx, gy-7, GB_BODY)
        set_px(canvas, cx, gy-9, GB_ICING); set_px(canvas, cx, gy-7, GB_ICING)
        # 胳膊
        for row in [gy-8, gy-9]:
            set_px(canvas, cx-4, row, GB_BODY); set_px(canvas, cx-5, row, GB_BODY)
            for ax in range(cx+4, MID): set_px(canvas, ax, row, GB_BODY)
        # 腿
        for dy2 in range(6, 9):
            for ddx in [-3,-2, 2, 3]: set_px(canvas, cx+ddx, gy-dy2, GB_BODY)
        # 帽子（最后画，盖在头上）
        set_px(canvas, cx+1, gy-17, HAT_DARK)                           # 小啾啾
        for dx in range(-1, 4): set_px(canvas, cx+dx, gy-16, HAT_RED)   # 帽身第1行
        for dx in range(-1, 4): set_px(canvas, cx+dx, gy-15, HAT_RED)   # 帽身第2行
        set_px(canvas, cx-1, gy-16, HAT_DARK); set_px(canvas, cx+3, gy-16, HAT_DARK)
        set_px(canvas, cx-1, gy-15, HAT_DARK); set_px(canvas, cx+3, gy-15, HAT_DARK)
        set_px(canvas, cx,   gy-16, HAT_LITE)

    def draw_bunny(cx, gy):
        # 耳朵（高5格，内耳2格）
        for y2 in range(gy-20, gy-15):
            set_px(canvas, cx-1, y2, BUN_BODY); set_px(canvas, cx,   y2, BUN_BODY)
            set_px(canvas, cx+2, y2, BUN_BODY); set_px(canvas, cx+3, y2, BUN_BODY)
        for y2 in range(gy-19, gy-17):
            set_px(canvas, cx,   y2, BUN_INNER)
            set_px(canvas, cx+2, y2, BUN_INNER)
        # 头
        for dx in [-1, 0, 1]:           set_px(canvas, cx+dx, gy-16, BUN_BODY)
        for dx in [-2,-1, 0, 1, 2]:     set_px(canvas, cx+dx, gy-15, BUN_BODY)
        for dx in range(-3, 4):
            for row in [gy-14,gy-13,gy-12]: set_px(canvas, cx+dx, row, BUN_BODY)
        for dx in [-2,-1, 0, 1, 2]:     set_px(canvas, cx+dx, gy-11, BUN_BODY)
        for dx in [-1, 0, 1]:           set_px(canvas, cx+dx, gy-10, BUN_BODY)
        # 脸部细节
        set_px(canvas, cx-2, gy-15, BUN_LT);    set_px(canvas, cx-3, gy-14, BUN_LT)
        set_px(canvas, cx-2, gy-14, BUN_EYE);   set_px(canvas, cx+2, gy-14, BUN_EYE)
        set_px(canvas, cx-3, gy-13, BUN_BLUSH); set_px(canvas, cx+3, gy-13, BUN_BLUSH)
        set_px(canvas, cx,   gy-13, BUN_INNER)
        set_px(canvas, cx-2, gy-12, BUN_SMILE); set_px(canvas, cx+2, gy-12, BUN_SMILE)
        set_px(canvas, cx-1, gy-11, BUN_SMILE)
        set_px(canvas, cx,   gy-11, BUN_SMILE)
        set_px(canvas, cx+1, gy-11, BUN_SMILE)
        # 身体
        for dx in [-2,-1, 0, 1, 2]:     set_px(canvas, cx+dx, gy-9, BUN_BODY)
        for dx in range(-3, 4):          set_px(canvas, cx+dx, gy-8, BUN_BODY)
        for dx in [-2,-1, 0, 1, 2]:     set_px(canvas, cx+dx, gy-7, BUN_BODY)
        set_px(canvas, cx,   gy-9, BUN_LT); set_px(canvas, cx, gy-8, BUN_LT)
        set_px(canvas, cx+3, gy-7, BUN_LT); set_px(canvas, cx+4, gy-7, BUN_LT)
        # 胳膊（右外 + 牵手侧从 MID 开始）
        for row in [gy-8, gy-9]:
            set_px(canvas, cx+4, row, BUN_BODY); set_px(canvas, cx+5, row, BUN_BODY)
            for ax in range(MID, cx-3): set_px(canvas, ax, row, BUN_BODY)
        # 腿
        for dy2 in range(6, 9):
            for ddx in [-3,-2, 2, 3]: set_px(canvas, cx+ddx, gy-dy2, BUN_BODY)

    draw_gingerbread(GB_CX, FIG_Y)
    draw_bunny(BUN_CX, FIG_Y)

    return canvas


def render(canvas, output="pixel_volcano.png"):
    img = Image.new("RGB", (W * SCALE, H * SCALE))
    px  = img.load()
    for y in range(H):
        for x in range(W):
            c = canvas[y][x]
            for sy in range(SCALE):
                for sx in range(SCALE):
                    px[x * SCALE + sx, y * SCALE + sy] = c
    img.save(output)
    print(f"Saved: {output}")


if __name__ == "__main__":
    canvas = draw()
    render(canvas, "pixel_volcano.png")
