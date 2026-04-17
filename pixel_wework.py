from PIL import Image

W, H = 768, 432
S = 12
GW, GH = W//S, H//S  # 64×36

canvas = Image.new('RGB', (W, H))

def blend(c1, c2, t):
    return tuple(int(c1[i]*(1-t)+c2[i]*t) for i in range(3))

def set_px(img, gx, gy, col):
    if 0 <= gx < GW and 0 <= gy < GH:
        x0, y0 = gx*S, gy*S
        for dy in range(S):
            for dx in range(S):
                img.putpixel((x0+dx, y0+dy), col)

def wrow(img, gy, x1, x2, col):
    for gx in range(x1, x2+1):
        set_px(img, gx, gy, col)

def fill(img, y1, y2, x1, x2, col):
    for gy in range(y1, y2+1):
        for gx in range(x1, x2+1):
            set_px(img, gx, gy, col)

# ═══ 背景墙（暖米色）════════════════════════════
WALL     = (245, 235, 215)   # AC暖奶油白
WALL_D   = (225, 212, 188)
WALL_LT  = (255, 248, 235)
fill(canvas, 0, GH, 0, GW-1, WALL)

# ═══ 地板（木色）════════════════════════════════
FLOOR    = (162, 138, 98)    # 深一档，让前景桌面更跳
FLOOR_D  = (142, 118, 80)
FLOOR_LT = (182, 158, 118)
fill(canvas, 23, GH, 0, GW-1, FLOOR)
# 地板木纹
for y, x1, x2 in [(24,2,18),(24,22,40),(24,44,60),(26,5,25),(26,30,50)]:
    wrow(canvas, y, x1, x2, FLOOR_D)

# ═══ 大窗户（8格高，y=1~8）════════════════════
WIN_SKY  = (162, 212, 245)   # AC明亮天空蓝
WIN_SKY2 = (198, 228, 252)
WIN_FRAME= (192, 182, 165)
WIN_CITY = (148, 172, 198)
TREE_G   = (82, 168, 72)     # AC饱和暖绿
TREE_GD  = (55, 128, 48)
TREE_GL  = (122, 198, 98)
TREE_TR  = (128, 95, 58)     # 树干暖棕
BIRD_C   = (55, 45, 38)

fill(canvas, 2, 11, 2, 61, WIN_FRAME)    # 窗框外边
fill(canvas, 2, 11, 3, 60, WIN_SKY)      # 天空（单色）
wrow(canvas, 11, 2, 61, WIN_FRAME)       # 窗框底边
# 竖线均分三块
fill(canvas, 2, 11, 22, 22, WIN_FRAME)
fill(canvas, 2, 11, 42, 42, WIN_FRAME)

# 树（底部加宽，相邻连片）
# 左侧大树
for y, x1, x2 in [
    (4, 3, 8),(5, 2,12),(6, 2,14),(7, 2,16),(8, 2,18),
    (9, 3,19),(10, 4,20),(11,5,21),
]:
    wrow(canvas, y, x1, x2, TREE_G)
for px,py in [(5,4),(8,5),(3,6),(11,6),(4,8),(14,7),(16,9)]: set_px(canvas,px,py,TREE_GL)
for px,py in [(7,6),(10,8),(6,9),(13,10)]:                    set_px(canvas,px,py,TREE_GD)
for lx in [10,11]:
    for ly in range(10,12): set_px(canvas,lx,ly,TREE_TR)

# 中左小树
for y, x1, x2 in [
    (6,16,23),(7,15,25),(8,14,26),(9,13,26),(10,12,25),(11,11,24),
]:
    wrow(canvas, y, x1, x2, TREE_G)
for px,py in [(18,6),(23,6),(15,8),(25,8),(13,10),(24,9)]: set_px(canvas,px,py,TREE_GL)
for px,py in [(20,7),(17,9),(22,10)]:                      set_px(canvas,px,py,TREE_GD)
for lx in [19,20]:
    for ly in range(10,12): set_px(canvas,lx,ly,TREE_TR)

# 中右小树
for y, x1, x2 in [
    (6,38,45),(7,37,47),(8,37,49),(9,37,50),(10,38,51),(11,39,52),
]:
    wrow(canvas, y, x1, x2, TREE_G)
for px,py in [(40,6),(44,6),(38,8),(48,8),(37,10),(50,9)]: set_px(canvas,px,py,TREE_GL)
for px,py in [(42,7),(39,9),(46,10)]:                      set_px(canvas,px,py,TREE_GD)
for lx in [43,44]:
    for ly in range(10,12): set_px(canvas,lx,ly,TREE_TR)

# 右侧大树
for y, x1, x2 in [
    (3,50,56),(4,48,58),(5,46,59),(6,44,60),(7,43,61),
    (8,43,61),(9,44,61),(10,45,60),(11,46,59),
]:
    wrow(canvas, y, x1, x2, TREE_G)
for px,py in [(52,4),(56,3),(48,5),(60,5),(44,7),(59,6),(46,9)]: set_px(canvas,px,py,TREE_GL)
for px,py in [(54,5),(57,7),(50,8),(47,10)]:                      set_px(canvas,px,py,TREE_GD)
for lx in [54,55]:
    for ly in range(10,12): set_px(canvas,lx,ly,TREE_TR)

# 小鸟已移除

# 窗框四边（树之后画，压住树冠）
wrow(canvas,  2, 2, 61, WIN_FRAME)   # 顶边
wrow(canvas, 11, 2, 61, WIN_FRAME)   # 底边
fill(canvas,  2, 11, 2,  2, WIN_FRAME)   # 左边
fill(canvas,  2, 11, 61, 61, WIN_FRAME)  # 右边
fill(canvas,  2, 11, 22, 22, WIN_FRAME)  # 竖线1
fill(canvas,  2, 11, 42, 42, WIN_FRAME)  # 竖线2

# ═══ 左侧电脑分开（姜饼人背后，y=8~13）════════════════════
BG_LAP_B  = (242, 243, 245)  # 最浅银白
BG_LAP_SC = (108, 128, 148)  # 屏幕深蓝
BG_LAP_LB = (145, 182, 218)  # 屏幕亮蓝
BG_LAP_LT = (228, 230, 232)  # 顶边与外壳接近
BG_WIN_W  = (228, 232, 242)

for ex in [3, 16]:
    for ly in range(9, 14): wrow(canvas, ly, ex, ex+8, BG_LAP_B)
    fill(canvas, 10, 13, ex+1, ex+7, BG_LAP_SC)
    fill(canvas, 10, 11, ex+1, ex+2, BG_LAP_LB)
    wrow(canvas, 9,  ex, ex+8, BG_LAP_LT)
    wrow(canvas, 14, ex-1, ex+9, BG_LAP_B)   # 底座
    for gy in [11, 12]:
        for gx in [ex+3, ex+4, ex+5]: set_px(canvas, gx, gy, BG_WIN_W)

# 电脑桌（y=15，1格厚）
BG_DESK   = (188, 178, 162)
BG_DESK_D = (165, 155, 140)
fill(canvas, 15, 15, 2, 25, BG_DESK)
wrow(canvas, 15, 2, 25, BG_DESK_D)
# 桌腿（y=16~22）
for lx in [3, 4, 23, 24]:
    for ly in range(16, 23): set_px(canvas, lx, ly, BG_DESK_D)

# ═══ 右侧沙发（蓝兔子背后，x=42~62）════════════════════
SOFA_CAR    = (205, 155, 88)   # AC焦糖暖橙
SOFA_CAR_D  = (162, 118, 55)
SOFA_CAR_L  = (232, 188, 122)
SOFA_SEAT_L = (248, 208, 145)
SOFA_SEAM   = (138, 92, 42)

# 靠背（y=14~18，x=40~58）
fill(canvas, 14, 18, 40, 58, SOFA_CAR)
fill(canvas, 14, 18, 41, 57, SOFA_CAR_L)
# 扶手（左 x=37~39，右 x=59~61，y=16~21）
fill(canvas, 16, 21, 37, 39, SOFA_CAR)
fill(canvas, 16, 21, 59, 61, SOFA_CAR)
wrow(canvas, 16, 37, 39, SOFA_CAR_L)
wrow(canvas, 16, 59, 61, SOFA_CAR_L)
# 坐垫（y=18~21，x=39~59）
fill(canvas, 18, 21, 39, 59, SOFA_CAR)
fill(canvas, 18, 18, 39, 59, SOFA_SEAT_L)
# 沙发腿（y=22，左 x=40~41，右 x=57~58）
for lx in [40, 41, 57, 58]:
    set_px(canvas, lx, 22, SOFA_CAR_D)

# ═══ 绿植（中间背景，x=30~34）═══════════════════
POT     = (168, 128, 88)
POT_D   = (138, 98, 62)
PLANT   = (72, 148, 82)
PLANT_D = (48, 112, 58)
PLANT_L = (108, 182, 95)

fill(canvas, 19, 22, 30, 33, POT)
set_px(canvas, 30, 19, POT_D); set_px(canvas, 33, 19, POT_D)
for lx, ly, col in [(31,18,PLANT_L),(32,18,PLANT_L),(30,17,PLANT),(33,17,PLANT),
                    (29,16,PLANT_D),(31,16,PLANT_L),(33,16,PLANT),(32,16,PLANT_L),
                    (30,15,PLANT),(32,15,PLANT),(31,14,PLANT_D),(29,15,PLANT_D),(33,15,PLANT_D)]:
    set_px(canvas, lx, ly, col)

# ═══ 俯视桌面（前景，y=29~35 整块）════════════════════
TABLE_TOP = (225, 198, 158)   # AC明亮木色桌面
TABLE_LT  = (242, 218, 182)
TABLE_SHD = (192, 165, 125)
fill(canvas, 29, GH-1, 0, GW-1, TABLE_TOP)
# 桌面前缘厚度
wrow(canvas, 29, 0, GW-1, TABLE_LT)

# ─── 角色桌（横向长桌，y=27~28）───────────────
DESK_TOP = (195, 168, 128)
DESK_SHD = (162, 135, 98)
# 角色桌（已去掉，地板延伸到前景桌）

# ─── 俯视贝果（桌面上，圆圈视角）───────────────
BAGEL_PLAIN = (245, 222, 175); BAGEL_P_D = (125, 90, 45); BAGEL_P_RING = (198, 168, 108)
BAGEL_SES   = (168, 128, 72);  BAGEL_SES_D = (128, 90, 42)
BAGEL_SPI   = (108, 168, 95);  BAGEL_SPI_D = (68, 128, 58)
BAGEL_BLU   = (148, 112, 195); BAGEL_BLU_D = (105, 75, 155)
BAGEL_CIN   = (205, 108, 38);  BAGEL_CIN_D = (158, 72, 22)  # 肉桂
SEED = (88, 68, 35)

def draw_bagel_top(cx, cy, outer, inner, ring=None):
    if ring is None:
        ring = outer
    # 内圈8格（浅色填充，基于 outer 色）
    mid = tuple(int(outer[i]*0.85 + TABLE_TOP[i]*0.15) for i in range(3))
    for dx, dy in [(cx-1,cy),(cx,cy-1),(cx+1,cy-1),(cx+2,cy),(cx+2,cy+1),(cx+1,cy+2),(cx,cy+2),(cx-1,cy+1)]:
        set_px(canvas, dx, dy, mid)
    # 外圈描边（用 ring 色）
    for dx, dy in [(-2,0),(-2,1),(-1,-1),(-1,2),(0,-2),(0,3),(1,-2),(1,3),(2,-1),(2,2),(3,0),(3,1)]:
        set_px(canvas, cx+dx, cy+dy, ring)

def draw_bagel_hole(cx, cy, inner):
    # 孔边内阴影 + 镂空（单独调用，必须在所有贝果之后）
    for ddx, ddy in [(0,0),(1,0),(0,1),(1,1)]:
        set_px(canvas, cx+ddx, cy+ddy, inner)
    set_px(canvas, cx+1, cy+1, TABLE_TOP)

# (桌面贝果移到最后画)

# ─── 奶酪酱暂时移除 ───────────────

# ─── 红色面包机（侧视图，两台居中并排）───────────────
TOAST_R  = (215, 45, 38)
TOAST_RD = (168, 28, 22)
TOAST_LT = (245, 88, 72)
TOAST_SL = (45, 35, 28)
BAGEL_SLOT   = (218, 192, 148)
BAGEL_SLOT_M = (195, 165, 118)
BAGEL_SLOT_D = (175, 145, 102)

for cx in [25, 37]:  # 居中对齐：左移1格
    # 机身（cx-4 到 cx+5，10格宽，y=31~35）
    fill(canvas, 31, 35, cx-4, cx+5, TOAST_R)
    fill(canvas, 31, 35, cx-4, cx-4, TOAST_RD)  # 左侧深色
    fill(canvas, 31, 35, cx+5, cx+5, TOAST_RD)  # 右侧深色
    wrow(canvas, 35, cx-4, cx+5, TOAST_RD)       # 底边深色
    wrow(canvas, 31, cx-4, cx+5, TOAST_RD)       # 顶边深色（封闭）
    # 顶角两格露桌面色（圆角）——顶边画完后覆盖
    set_px(canvas, cx-4, 31, TABLE_TOP)
    set_px(canvas, cx+5, 31, TABLE_TOP)
    # 旋钮
    set_px(canvas, cx+5, 33, TOAST_RD)
    # 倒T按钮（⊥形：竖柄 y=33~34，横条 y=35）
    BTN = (118, 15, 10)
    set_px(canvas, cx+3, 33, BTN)
    set_px(canvas, cx+3, 34, BTN)
    for bx in [cx+2, cx+3, cx+4]: set_px(canvas, bx, 35, BTN)
    bagel_col = BAGEL_CIN  if cx == 25 else BAGEL_SPI
    bagel_d   = BAGEL_CIN_D if cx == 25 else BAGEL_SPI_D
    bagel_mid = tuple(int(bagel_col[i]*0.85 + TABLE_TOP[i]*0.15) for i in range(3))
    BY = 29  # 贝果基准y（上移，BY<机身顶端31）
    # 外弧
    for dx, dy in [(-2,0),(-2,1),(-1,-1),(0,-2),(1,-2),(2,-1),(3,0),(3,1)]:
        set_px(canvas, cx+dx, BY+dy, bagel_col)
    # 内圈
    for dx, dy in [(-1,0),(0,-1),(1,-1),(2,0),(2,1),(1,1),(0,1),(-1,1)]:
        set_px(canvas, cx+dx, BY+dy, bagel_mid)
    # 孔边内阴影（深色）——必须在 TABLE_TOP 之前
    set_px(canvas, cx,   BY,   bagel_d)
    set_px(canvas, cx+1, BY,   bagel_d)
    set_px(canvas, cx,   BY+1, bagel_d)
    # 孔中心（镂空，最后覆盖）
    set_px(canvas, cx+1, BY+1, TABLE_TOP)


# ─── 手持贝果颜色常量 ───────────────
BAGEL_PNK   = (235, 148, 165)  # 粉色贝果
BAGEL_PNK_D = (188, 98, 118)

# ═══ 姜饼人（前景左，GX=18，只露上半身）══════════════════
GB_BODY  = (198, 118, 52)
GB_ICING = (250, 238, 215)
GB_EYE   = (58, 32, 12)
GB_CHEEK = (232, 158, 102)
GB_HAT   = (218, 52, 52)
GB_HAT_B = (185, 32, 32)

GX, GY = 18, 31

# 头 y=19~24
for y in range(20, 25):
    wrow(canvas, y, GX-3, GX+3, GB_BODY)
wrow(canvas, 19, GX-2, GX+2, GB_BODY)
wrow(canvas, 24, GX-2, GX+2, GB_BODY)
# 眼睛
set_px(canvas, GX-1, 21, GB_EYE); set_px(canvas, GX+1, 21, GB_EYE)
# 腮红
set_px(canvas, GX-2, 22, GB_CHEEK); set_px(canvas, GX+2, 22, GB_CHEEK)
# 嘴
set_px(canvas, GX-1, 23, GB_ICING); set_px(canvas, GX, 23, GB_ICING); set_px(canvas, GX+1, 23, GB_ICING)
# 身体 y=25~28
for y in range(25, 29):
    wrow(canvas, y, GX-2, GX+2, GB_BODY)
# 纽扣
set_px(canvas, GX, 25, GB_ICING); set_px(canvas, GX, 27, GB_ICING)
# 双臂搭桌（y=26，保持不变）
for dx in range(-5, -2): set_px(canvas, GX+dx, 26, GB_BODY)
for dx in range(3, 6):   set_px(canvas, GX+dx, 26, GB_BODY)
# 帽子（y=18~19，pom y=17）
for dx in range(-1, 4): set_px(canvas, GX+dx, 18, GB_HAT)
for dx in range(-1, 4): set_px(canvas, GX+dx, 19, GB_HAT)
set_px(canvas, GX-1, 18, GB_HAT_B); set_px(canvas, GX+3, 18, GB_HAT_B)
set_px(canvas, GX-1, 19, GB_HAT_B); set_px(canvas, GX+3, 19, GB_HAT_B)
set_px(canvas, GX+1, 17, GB_HAT_B)
set_px(canvas, GX,   18, (248, 108, 88))

# ═══ 蓝兔子（前景右，BX=46，只露上半身）══════════════════
BUN_BODY  = (158, 208, 255)
BUN_LT    = (178, 220, 255)
BUN_INNER = (210, 168, 190)
BUN_EYE   = (42, 25, 72)
BROW_D    = (8, 2, 25)
BUN_BLUSH = (248, 162, 182)
BUN_SMILE = (245, 238, 225)

BX, BY = 46, 31

# 左耳
set_px(canvas, BX-1, 13, BUN_BODY)
for y in range(14, 19):
    wrow(canvas, y, BX-2, BX-1, BUN_BODY)
set_px(canvas, BX-2, 15, BUN_INNER); set_px(canvas, BX-2, 16, BUN_INNER); set_px(canvas, BX-2, 17, BUN_INNER)
# 右耳（自然内粉色，无格纹）
set_px(canvas, BX+1, 13, BUN_BODY)
for y in range(14, 19):
    wrow(canvas, y, BX+1, BX+2, BUN_BODY)
set_px(canvas, BX+2, 15, BUN_INNER)
set_px(canvas, BX+2, 16, BUN_INNER)
set_px(canvas, BX+2, 17, BUN_INNER)
# 头 y=19~24
for y in range(20, 25):
    wrow(canvas, y, BX-3, BX+3, BUN_BODY)
wrow(canvas, 19, BX-2, BX+2, BUN_BODY)
wrow(canvas, 24, BX-2, BX+2, BUN_BODY)
for y in range(21, 24):
    wrow(canvas, y, BX-1, BX+1, BUN_LT)
# 连心眉
set_px(canvas, BX-2, 20, BUN_EYE); set_px(canvas, BX-1, 20, BUN_EYE)
set_px(canvas, BX,   20, (118, 158, 215))
set_px(canvas, BX+1, 20, BUN_EYE); set_px(canvas, BX+2, 20, BUN_EYE)
set_px(canvas, BX-1, 21, BROW_D); set_px(canvas, BX+1, 21, BROW_D)
# 腮红
set_px(canvas, BX-2, 22, BUN_BLUSH); set_px(canvas, BX+2, 22, BUN_BLUSH)
# 嘴
set_px(canvas, BX-1, 23, BUN_SMILE); set_px(canvas, BX, 23, BUN_SMILE); set_px(canvas, BX+1, 23, BUN_SMILE)
# 身体 y=25~28
for y in range(25, 29):
    wrow(canvas, y, BX-2, BX+2, BUN_BODY)
# 双臂搭桌（y=26，保持不变）
for dx in range(-5, -2): set_px(canvas, BX+dx, 26, BUN_BODY)
for dx in range(3, 6):   set_px(canvas, BX+dx, 26, BUN_BODY)

# ═══ 保存 ════════════════════════════════════════
# ─── 手持贝果（角色之后画，保证完整显示）───────────────
# 姜饼人右手边 cx=23, cy=23
draw_bagel_top(23, 23, BAGEL_PLAIN, BAGEL_P_D, ring=BAGEL_P_RING)
draw_bagel_hole(23, 23, BAGEL_P_D)
# 兔子左手边 cx=40, cy=23
draw_bagel_top(40, 23, BAGEL_PNK, BAGEL_PNK_D)
draw_bagel_hole(40, 23, BAGEL_PNK_D)

# ─── 桌面贝果（最后画，最上层）───────────────
# 左侧贝果组
draw_bagel_top(6,  29, BAGEL_PLAIN, BAGEL_P_D, ring=BAGEL_P_RING)
draw_bagel_top(13, 29, BAGEL_SPI,   BAGEL_SPI_D)
draw_bagel_top(6,  33, BAGEL_CIN,   BAGEL_CIN_D)
draw_bagel_top(13, 33, BAGEL_SES,   BAGEL_SES_D)
for sx, sy in [(12,33),(15,34),(13,35),(14,32)]: set_px(canvas, sx, sy, SEED)
draw_bagel_hole(6,  29, BAGEL_P_D)
draw_bagel_hole(13, 29, BAGEL_SPI_D)
draw_bagel_hole(6,  33, BAGEL_CIN_D)
draw_bagel_hole(13, 33, BAGEL_SES_D)
# 右侧贝果组
draw_bagel_top(49, 29, BAGEL_BLU,   BAGEL_BLU_D)
draw_bagel_top(56, 29, BAGEL_PLAIN, BAGEL_P_D, ring=BAGEL_P_RING)
draw_bagel_top(49, 33, BAGEL_SES,   BAGEL_SES_D)
draw_bagel_top(56, 33, BAGEL_SPI,   BAGEL_SPI_D)
for sx, sy in [(48,33),(51,34),(49,35),(50,32)]: set_px(canvas, sx, sy, SEED)
draw_bagel_hole(49, 29, BAGEL_BLU_D)
draw_bagel_hole(56, 29, BAGEL_P_D)
draw_bagel_hole(49, 33, BAGEL_SES_D)
draw_bagel_hole(56, 33, BAGEL_SPI_D)

canvas.save('pixel_wework.png')
print(f"Saved: {W}×{H}px")
