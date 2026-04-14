from PIL import Image

W, H = 64, 36
S = 12

def blend(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(c1[i]*(1-t) + c2[i]*t) for i in range(3))

def set_px(canvas, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        canvas[y][x] = color

def wrow(canvas, y, x1, x2, color):
    for x in range(x1, min(x2+1, W)):
        set_px(canvas, x, y, color)

def fill(canvas, y1, y2, x1, x2, color):
    for y in range(y1, y2+1):
        wrow(canvas, y, x1, x2, color)

# ── Colors ────────────────────────────────────────────────────────────────────
SKY_TOP  = (22, 18, 62)    # 深蓝紫夜空
SKY_MID  = (35, 28, 92)
SKY_BOT  = (52, 42, 118)

TREE     = (18, 15, 48)    # 深蓝紫树影

TUB_WOOD = (195, 148, 82)  # 动森暖木色
TUB_DARK = (148, 105, 48)
TUB_RIM  = (218, 175, 105)
TUB_LIT  = (235, 198, 128)

WATER_HI = (58, 175, 185)
WATER_MID= (38, 142, 158)
WATER_LO = (25, 108, 128)
WATER_SH = (155, 228, 235)  # shimmer

STEAM    = (182, 218, 228)

MOON_Y   = (255, 248, 195)
STAR_HI  = (255, 252, 210)
STAR_MED = (198, 212, 255)

GB       = (188, 112,  50)
GBD      = (145,  80,  32)
GBE      = ( 62,  35,  15)
GB_ICING = (245, 232, 210)
GB_CHEEK = (228, 152,  98)

BUN      = ( 98, 162, 218)
BUND     = ( 68, 112, 182)
BUNE     = ( 38,  22,  60)
BUNK     = (228, 148, 168)
BUN_LT   = (148, 198, 242)
BUN_BLUSH= (238, 158, 175)
BUN_SMILE= (242, 235, 220)

WINE     = (178,  45,  62)
GLASS    = (185, 155, 115)
CUP      = (225, 188,  88)

def draw():
    canvas = [[SKY_TOP]*W for _ in range(H)]

    # ── Sky gradient ──────────────────────────────────────────────────────────
    for y in range(H):
        t = y / (H - 1)
        col = blend(SKY_TOP, SKY_BOT, min(t * 1.2, 1.0))
        wrow(canvas, y, 0, W-1, col)

    # ── Moon: removed ─────────────────────────────────────────────────────────

    # ── Stars (AC style: big + small) ────────────────────────────────────────
    STAR_W  = (255, 252, 200)   # warm white
    STAR_C  = (210, 220, 255)   # cool blue-white

    # Big stars (cross glow)
    BIG_STARS = [
        (11,1,STAR_W),(19,3,STAR_C),(33,4,STAR_W),(46,3,STAR_C),(60,6,STAR_W),
        (7,6,STAR_C),(25,7,STAR_W),(42,4,STAR_C),(56,2,STAR_W),
        (4,10,STAR_W),(22,11,STAR_C),(38,9,STAR_W),(53,10,STAR_C),
    ]
    for sx, sy, sc in BIG_STARS:
        set_px(canvas, sx, sy, sc)
        for off in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = sx+off[0], sy+off[1]
            if 0 <= nx < W and 0 <= ny < H and canvas[ny][nx][0] < 50:
                canvas[ny][nx] = blend(canvas[ny][nx], sc, 0.35)

    # Small stars (single pixel)
    for sx, sy in [(3,2),(17,5),(28,3),(36,7),(50,5),(62,4),
                   (9,8),(31,5),(44,9),(58,7),(15,12),(48,13)]:
        if canvas[sy][sx][0] < 50:
            set_px(canvas, sx, sy, STAR_C)

    # ── Tree silhouettes ──────────────────────────────────────────────────────
    # Left trees — wider at bottom
    for y, x1, x2 in [
        (5,0,4),(6,0,6),(7,0,7),(8,0,8),(9,1,7),(10,0,6),(11,0,7),(12,1,6),
        (13,0,5),(14,0,6),(15,1,5),(16,0,5),(17,0,5),(18,0,6),(19,0,6),
        (20,0,7),(21,0,7),(22,0,8),(23,0,8),(24,0,9),(25,0,9),(26,0,10),(27,0,10),
    ]:
        wrow(canvas, y, x1, x2, TREE)
    fill(canvas, 16, 35, 0, 2, TREE)    # left trunk full height
    fill(canvas, 13, 35, 7, 9, TREE)    # left inner trunk full height

    for y, x1, x2 in [
        (7,6,11),(8,5,13),(9,6,13),(10,7,12),(11,6,13),(12,7,12),(13,8,11),
        (14,7,12),(15,6,13),(16,6,13),(17,6,14),(18,6,14),(19,6,15),(20,5,15),
        (21,5,15),(22,5,16),(23,5,16),(24,5,17),(25,5,17),(26,5,18),(27,5,18),
    ]:
        wrow(canvas, y, x1, x2, TREE)

    # Right trees — wider at bottom
    for y, x1, x2 in [
        (5,57,63),(6,55,63),(7,54,63),(8,55,63),(9,56,63),(10,55,63),
        (11,54,63),(12,55,63),(13,56,63),(14,57,62),(15,56,63),(16,57,63),
        (17,56,63),(18,56,63),(19,55,63),(20,55,63),(21,54,63),(22,54,63),(23,53,63),(24,53,63),
        (25,52,63),(26,52,63),(27,51,63),
    ]:
        wrow(canvas, y, x1, x2, TREE)
    fill(canvas, 16, 35, 59, 63, TREE)  # right trunk full height

    for y, x1, x2 in [
        (9,49,53),(10,48,54),(11,49,55),(12,50,54),(13,51,53),
        (14,50,54),(15,49,54),(16,48,54),(17,47,55),(18,47,55),(19,46,55),
        (20,46,56),(21,45,56),(22,45,56),(23,44,57),(24,44,57),
        (25,44,57),(26,43,57),(27,43,57),
    ]:
        wrow(canvas, y, x1, x2, TREE)
    fill(canvas, 13, 35, 50, 51, TREE)

    # Distant mountains removed

    # ── Ground ────────────────────────────────────────────────────────────────
    BUSH = (38, 88, 48)     # 动森暖绿
    BUSH_D = (38, 88, 48)  # same color

    # Left bushes — taller, cover tree trunks and ground below
    for y, x1, x2 in [
        (27, 4, 10), (26, 5, 12), (25, 6, 11),
        (27, 13, 18), (26, 14, 19), (25, 15, 18),
    ]:
        wrow(canvas, y, x1, x2, BUSH)
    # Fill down to ground to cover trunks
    fill(canvas, 28, 35, 0, 19, BUSH_D)
    fill(canvas, 28, 35, 0, 12, BUSH)   # overlap lighter front layer

    # Right bushes — taller, cover tree trunks and ground below
    for y, x1, x2 in [
        (27, 45, 52), (26, 44, 51), (25, 45, 50),
        (27, 54, 60), (26, 53, 59), (25, 54, 59),
    ]:
        wrow(canvas, y, x1, x2, BUSH)
    fill(canvas, 28, 35, 44, 63, BUSH_D)
    fill(canvas, 28, 35, 51, 63, BUSH)

    # Ground row — replace black with bush dark
    fill(canvas, 34, 35, 0, W-1, BUSH_D)

    # ── Hot tub (wooden barrel) ───────────────────────────────────────────────
    TX1, TX2 = 13, 50
    TY1, TY2 = 22, 34  # bottom thickened by 1

    # Outer wood body
    fill(canvas, TY1, TY2, TX1, TX2, TUB_WOOD)
    # Side shading
    fill(canvas, TY1, TY2, TX1,    TX1+1, TUB_DARK)
    fill(canvas, TY1, TY2, TX2-1, TX2,   TUB_DARK)
    # Round corners: remove bottom-left and bottom-right corners
    set_px(canvas, TX1,   TY2-1, BUSH_D)   # BL outer
    set_px(canvas, TX1,   TY2-2, BUSH_D)
    set_px(canvas, TX1+1, TY2-1, BUSH_D)
    set_px(canvas, TX2,   TY2-1, BUSH_D)   # BR outer
    set_px(canvas, TX2,   TY2-2, BUSH_D)
    set_px(canvas, TX2-1, TY2-1, BUSH_D)
    # No wood grain
    # Rim (full width — characters drawn after will cover it)
    wrow(canvas, TY1,   TX1, TX2, TUB_RIM)
    wrow(canvas, TY1+1, TX1, TX2, TUB_LIT)

    # ── Water ────────────────────────────────────────────────────────────────
    WX1, WX2 = 15, 48
    WY = 24   # water surface row

    fill(canvas, WY,   WY+1, WX1, WX2, WATER_HI)
    fill(canvas, WY+2, 29,   WX1, WX2, WATER_MID)
    fill(canvas, 30,   32,   WX1, WX2, WATER_LO)
    # Inner rounded corners — cut water corners at bottom-left and bottom-right
    set_px(canvas, WX1,   32, TUB_WOOD)
    set_px(canvas, WX1+1, 32, TUB_WOOD)
    set_px(canvas, WX1,   31, TUB_WOOD)
    set_px(canvas, WX2,   32, TUB_WOOD)
    set_px(canvas, WX2-1, 32, TUB_WOOD)
    set_px(canvas, WX2,   31, TUB_WOOD)
    # shimmer dots
    for sx in [17, 22, 27, 33, 39, 44]:
        set_px(canvas, sx, WY, WATER_SH)
    # Bubbles — small bright dots scattered in water
    BUBBLE = (95, 168, 182)
    for bx, by in [(18, WY+2),(23, WY+3),(30, WY+2),(35, WY+4),(40, WY+3),(45, WY+2),
                   (20, WY+5),(28, WY+4),(37, WY+5),(43, WY+6),(25, WY+6),(32, WY+3)]:
        set_px(canvas, bx, by, BUBBLE)

    # ── Steam (hard pixel blocks) ─────────────────────────────────────────────
    for sy, sx, sw in [
        (16, 24, 2),
    ]:
        wrow(canvas, sy, sx, sx+sw-1, STEAM)

    # ── GB (left, cx=27) ─────────────────────────────────────────────────────
    # 姜饼人语义区域（GCX=27，WY=24）：
    # 帽子小啾啾：(GCX+1, 15) = (28,15)
    # 帽身：x=GCX-1~GCX+3 (26~30), y=16~17
    # 头：x=GCX-3~GCX+3 (24~30), y=17~22  ← 四角 (24,17)(30,17) 为 SKY_MID
    # 脖子：x=GCX-2~GCX+2 (25~29), y=23~24
    # 肩膀水线：x=GCX-3~GCX+3 (24~30), y=24
    # 肩膀亮蓝：(GCX-4, 24)=(23,24), (GCX+4, 24)=(31,24)
    # 左臂：(GCX-3~GCX-7, WY~WY-4) = (24~20, 24~20)，斜上
    # 水下身体：x=GCX-2~GCX+2 (25~29), y=WY+1~WY+3 (25~27)，blend色
    GCX = 27

    # Head rows 16-21 (6×7)
    fill(canvas, 17, 22, GCX-3, GCX+3, GB)
    set_px(canvas, GCX-3, 17, SKY_MID); set_px(canvas, GCX+3, 17, SKY_MID)


    # Eyes: y=18 and y=20 (竖向两点，火山风格)
    set_px(canvas, GCX-2, 19, GBE);  set_px(canvas, GCX+2, 19, GBE)
    set_px(canvas, GCX-2, 21, GBE);  set_px(canvas, GCX+2, 21, GBE)
    # Cheeks: y=19
    set_px(canvas, GCX-3, 20, GB_CHEEK)
    set_px(canvas, GCX+3, 20, GB_CHEEK)
    # Mouth: U形（嘴角y=20，中间y=21）
    set_px(canvas, GCX-2, 21, GBE); set_px(canvas, GCX+2, 21, GBE)
    set_px(canvas, GCX-1, 22, GBE); set_px(canvas, GCX, 22, GBE); set_px(canvas, GCX+1, 22, GBE)
    # Neck/body y=22-23 (connects head to water)
    fill(canvas, 23, 24, GCX-2, GCX+2, GB)
    # Hat (painter beret, same as volcano)
    HAT_RED  = (198, 42, 32)
    HAT_DARK = (140, 26, 20)
    HAT_LITE = (225, 72, 55)
    set_px(canvas, GCX+1, 15, HAT_DARK)                              # 小啾啾
    for dx in range(-1, 4): set_px(canvas, GCX+dx, 16, HAT_RED)     # 帽身第1行
    for dx in range(-1, 4): set_px(canvas, GCX+dx, 17, HAT_RED)     # 帽身第2行
    set_px(canvas, GCX-1, 16, HAT_DARK); set_px(canvas, GCX+3, 16, HAT_DARK)
    set_px(canvas, GCX-1, 17, HAT_DARK); set_px(canvas, GCX+3, 17, HAT_DARK)
    set_px(canvas, GCX,   16, HAT_LITE)
    # Shoulders at water line row 22
    wrow(canvas, WY, GCX-3, GCX+3, GB)
    # 水面边缘亮蓝
    set_px(canvas, GCX-4, WY, (128, 220, 235)); set_px(canvas, GCX+4, WY, (128, 220, 235))
    # Left arm raised (holding glass)
    # Left arm — 2px wide, diagonal out (starts at water surface)
    for ax, ay in [(GCX-3, WY),(GCX-4, WY-1),(GCX-5, WY-2),(GCX-6, WY-3),(GCX-7, WY-4)]:
        set_px(canvas, ax, ay, GB)
        set_px(canvas, ax, ay+1, GB)
    # Submerged (blended)
    fill(canvas, WY+1, WY+3, GCX-2, GCX+2, blend(GB, WATER_MID, 0.55))

    # Wine glass (GB left, moved further out)
    set_px(canvas, GCX-8, WY-7, STAR_MED)   # 杯口左壁
    set_px(canvas, GCX-7, WY-7, STAR_MED)   # 杯口中间
    set_px(canvas, GCX-6, WY-7, STAR_MED)   # 杯口右壁
    set_px(canvas, GCX-7, WY-4, WINE)
    set_px(canvas, GCX-7, WY-5, WINE)
    set_px(canvas, GCX-8, WY-6, WINE)
    set_px(canvas, GCX-7, WY-6, WINE)
    set_px(canvas, GCX-6, WY-6, WINE)
    set_px(canvas, GCX-8, WY-5, WINE)
    set_px(canvas, GCX-6, WY-5, WINE)

    # ── BUN (right, cx=37) ───────────────────────────────────────────────────
    # 蓝兔子语义区域（BCX=37，WY=24）：
    # 耳朵：x=BCX-3~BCX-2 (34~35) 左耳, x=BCX~BCX+1 (37~38) 右耳, y=13~17
    #       耳朵外侧粉色 BUNK：(34,13~17), (38,13~17)
    #       耳内高光 BUN_LT：(34,14), (38,14) ← 手动覆盖为粉色
    # 头顶角点：(34,16)(38,16) ← 手动覆盖为粉色
    # 头：x=BCX-3~BCX+3 (34~40), y=17~22  ← 四角 (34,17)(40,17) 为 SKY_MID
    # 眼睛高光：(34,18)=BUN_LT
    # 脸颊：(34,20)(40,20)=BUN_BLUSH
    # 鼻子：(37,20)=BUNK
    # 嘴：y=21~22
    # 脖子：x=BCX-2~BCX+2 (35~39), y=23~24
    # 肩膀水线：x=BCX-3~BCX+3 (34~40), y=24
    # 肩膀亮蓝：(BCX-4, 24)=(33,24), (BCX+4, 24)=(41,24)
    # 右臂出水亮蓝：(42,24)
    # 右臂：(BCX+3~BCX+7, WY~WY-4) = (40~44, 24~20)，斜上
    # 水下身体：x=BCX-2~BCX+2 (35~39), y=WY+1~WY+3 (25~27)，blend色
    BCX = 37

    # Ears rows 12-16 (2px wide each, inner=BUN blue, outer=BUNK pink)
    fill(canvas, 13, 17, BCX-3, BCX-2, BUN)
    fill(canvas, 13, 17, BCX-3, BCX-3, BUNK)  # outer column pink
    set_px(canvas, BCX-3, 14, BUN_LT)
    fill(canvas, 13, 17, BCX, BCX+1, BUN)
    fill(canvas, 13, 17, BCX+1, BCX+1, BUNK)  # outer column pink
    set_px(canvas, BCX+1, 14, BUN_LT)

    # Head rows 16-21
    fill(canvas, 17, 22, BCX-3, BCX+3, BUN)
    set_px(canvas, BCX-3, 17, SKY_MID); set_px(canvas, BCX+3, 17, SKY_MID)


    # Eyes: y=18 单格 (火山风格)
    set_px(canvas, BCX-2, 19, BUNE);  set_px(canvas, BCX+2, 19, BUNE)
    # 眼睛左侧高光
    set_px(canvas, BCX-3, 18, BUN_LT)
    # 耳内高光（已在耳朵里）
    set_px(canvas, BCX-3, 14, BUN_LT); set_px(canvas, BCX+1, 14, BUN_LT)
    # 脸颊 y=19
    set_px(canvas, BCX-3, 20, BUN_BLUSH)
    set_px(canvas, BCX+3, 20, BUN_BLUSH)
    # 鼻子 y=19 中间
    set_px(canvas, BCX, 20, BUNK)
    # 嘴：U形（嘴角y=20，中间y=21），白色
    set_px(canvas, BCX-2, 21, BUN_SMILE); set_px(canvas, BCX+2, 21, BUN_SMILE)
    set_px(canvas, BCX-1, 22, BUN_SMILE); set_px(canvas, BCX, 22, BUN_SMILE); set_px(canvas, BCX+1, 22, BUN_SMILE)
    # Neck/body y=22-23
    fill(canvas, 23, 24, BCX-2, BCX+2, BUN)
    # Shoulders
    wrow(canvas, WY, BCX-3, BCX+3, BUN)
    # 水面边缘亮蓝
    set_px(canvas, BCX-4, WY, (128, 220, 235)); set_px(canvas, BCX+4, WY, (128, 220, 235))
    # Right arm raised (holding cup)
    # Right arm — 2px wide, diagonal out (starts at water surface)
    for ax, ay in [(BCX+3, WY),(BCX+4, WY-1),(BCX+5, WY-2),(BCX+6, WY-3),(BCX+7, WY-4)]:
        set_px(canvas, ax, ay, BUN)
        set_px(canvas, ax, ay+1, BUN)
    # Submerged
    fill(canvas, WY+1, WY+3, BCX-2, BCX+2, blend(BUN, WATER_MID, 0.55))

    # Cup — wine glass style, yellow instead of red
    YLIQ = (222, 185, 88)   # yellow liquid (same as CUP)
    set_px(canvas, BCX+7, WY-7, STAR_MED)   # 杯口左壁
    set_px(canvas, BCX+8, WY-7, STAR_MED)   # 杯口中间
    set_px(canvas, BCX+9, WY-7, STAR_MED)   # 杯口右壁
    set_px(canvas, BCX+7, WY-6, YLIQ)
    set_px(canvas, BCX+8, WY-6, YLIQ)
    set_px(canvas, BCX+9, WY-6, YLIQ)
    set_px(canvas, BCX+7, WY-5, YLIQ)
    set_px(canvas, BCX+9, WY-5, YLIQ)
    set_px(canvas, BCX+8, WY-4, YLIQ)   # 杯柄
    set_px(canvas, BCX+8, WY-5, YLIQ)

    return canvas

canvas = draw()

img = Image.new("RGB", (W*S, H*S))
px = img.load()
for y in range(H):
    for x in range(W):
        c = canvas[y][x]
        for dy in range(S):
            for dx in range(S):
                px[x*S+dx, y*S+dy] = c

# 胸前水面边缘（直接写px，最后绘制）
GCX = 27; BCX = 37; WY = 24
EDGE = (128, 220, 235)
for cx, cy in [(GCX+dx, WY+1) for dx in range(-4,5)] + [(BCX+dx, WY+1) for dx in range(-4,5)]:
    for dy in range(S):
        for dx in range(S):
            px[cx*S+dx, cy*S+dy] = EDGE

# 覆盖 y=16 x=24,25 多余格子（用天空渐变色）
_t = 16/35
_sky16 = tuple(int(a + (_t*(b-a))) for a,b in zip((20,12,58),(72,58,135)))
for _cx, _cy in [(24,16),(25,16)]:
    for _dy in range(S):
        for _dx in range(S):
            px[_cx*S+_dx, _cy*S+_dy] = _sky16

# 覆盖 BCX 头顶角点残影 y=16 x=34,38
for _cx, _cy in [(34,16),(38,16)]:
    for _dy in range(S):
        for _dx in range(S):
            px[_cx*S+_dx, _cy*S+_dy] = _sky16

# 覆盖耳朵上亮蓝点 (34,14) (38,14)
for _cx, _cy in [(34,14),(38,14)]:
    for _dy in range(S):
        for _dx in range(S):
            px[_cx*S+_dx, _cy*S+_dy] = _sky16

# 补回 (34,16)(38,16) 亮蓝色
for _cx, _cy in [(34,16),(38,16)]:
    for _dy in range(S):
        for _dx in range(S):
            px[_cx*S+_dx, _cy*S+_dy] = (228, 148, 168)

# 补回 (34,14)(38,14) 粉色 BUNK
for _cx, _cy in [(34,14),(38,14)]:
    for _dy in range(S):
        for _dx in range(S):
            px[_cx*S+_dx, _cy*S+_dy] = (228, 148, 168)

# 兔子胳膊出水处 (42,24) 亮蓝
for _dy in range(S):
    for _dx in range(S):
        px[42*S+_dx, 24*S+_dy] = (128, 220, 235)
img.save("/home/azureuser/.openclaw/workspace/pixel_hotspring.png")
print(f"Saved: {W*S}×{H*S}px")
