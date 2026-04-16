from PIL import Image
import math

W, H = 768, 432
S = 12
GW, GH = W//S, H//S  # 64×36

canvas = Image.new('RGB', (W, H))

def set_px(c, x, y, col):
    if 0 <= x < GW and 0 <= y < GH:
        for dy in range(S):
            for dx in range(S):
                c.putpixel((x*S+dx, y*S+dy), col)

def wrow(c, y, x1, x2, col):
    for x in range(x1, x2+1):
        set_px(c, x, y, col)

def blend(c1, c2, t):
    return tuple(int(c1[i]*(1-t)+c2[i]*t) for i in range(3))

CX = 32  # center x
WL = 15  # water line y

# ── Sky ──────────────────────────────────────────────────────
SKY_TOP = (178, 210, 235)
SKY_BOT = (212, 232, 245)
SKY_TOP = (225, 138, 105)    # 动森紫（偏粉）
SKY_BOT = (248, 188, 105)   # 橙杏（柔和）
for y in range(WL):
    wrow(canvas, y, 0, GW-1, blend(SKY_TOP, SKY_BOT, y/WL))

# Distant sea horizon (sky level)
SEA_FAR = (122, 158, 162)
for y in range(WL-5, WL):
    t = (y-(WL-5))/5
    wrow(canvas, y, 0, GW-1, blend(SEA_FAR, blend(SEA_FAR,(42,105,135),0.5), t))

# ── Water surface ─────────────────────────────────────────────
SURF_LINE = (98, 195, 188)
wrow(canvas, WL,   0, GW-1, SURF_LINE)
wrow(canvas, WL+1, 0, GW-1, (72, 165, 178))
# ripple highlights symmetric
for rx in [CX-8, CX-3, CX+3, CX+8, CX+14, CX-14]:
    set_px(canvas, rx,   WL, (142, 218, 208))
    set_px(canvas, rx+1, WL, (122, 205, 198))



# ── Underwater ───────────────────────────────────────────────
DEEP  = (18, 65, 95)
MID   = (35, 115, 142)
SURF_U= (55, 158, 168)

for y in range(WL+2, GH):
    t = (y-WL-2)/(GH-WL-2)
    wrow(canvas, y, 0, GW-1, blend(SURF_U, blend(MID, DEEP, t), t))

# Light rays underwater (centered, symmetric)
for rx in [CX-8, CX, CX+8]:
    for y in range(WL+2, WL+14):
        alpha = max(0, 0.14 - (y-WL)*0.008)
        for dx in [-1, 0, 1]:
            nx = rx+dx
            if 0<=nx<GW:
                cur = canvas.getpixel((nx*S+S//2, y*S+S//2))
                set_px(canvas, nx, y, blend(cur, (142, 218, 208), alpha))

# ── Rocky reef bottom (framing sides, open center for turtle) ─
ROCK_D  = (25, 40, 32)
ROCK_M  = (42, 62, 50)
ROCK_SUN_D = (62, 50, 40)   # 水上礁石暗
ROCK_SUN_M = (95, 78, 62)  # 水上礁石亮（受夕阳照）
ALGAE   = (40, 108, 60)
ALGAE_L = (60, 140, 78)

# 右半边礁石底色（在所有礁石群之前铺底）
for y in range(WL+1, GH):
    depth = (y - WL) / (GH - WL)
    rock_c = blend(ROCK_M, ROCK_D, depth)
    for x in range(32, GW):
        set_px(canvas, x, y, rock_c)

# 右半边礁石填充：多种形状叠加，制造不规则纹理
import random
rng = random.Random(42)

# 大块礁石（主结构）— 宽高随机错落
big_rocks = [
    (32,20,40,36),(38,22,47,36),(45,18,54,36),(52,21,60,36),
    (34,16,43,30),(41,14,50,28),(48,17,57,31),(55,19,64,33),
    (32,12,41,22),(40,10,50,20),(49,13,58,23),
    (33,17,39,27),(43,15,49,25),(51,18,57,28),
    (37,19,43,26),(46,18,52,27),
]
for x1,y1,x2,y2 in big_rocks:
    for y in range(max(WL+1,y1), min(y2,GH)):
        for x in range(max(32,x1), min(x2,GW)):
            if y == y1:
                set_px(canvas, x, y, ROCK_M)
            elif y == y1+1:
                set_px(canvas, x, y, blend(ROCK_M, ROCK_D, 0.4))
            else:
                set_px(canvas, x, y, ROCK_D)

# 亮面高光（礁石顶部受光）
for x1,y1,x2,y2 in big_rocks:
    if y1 >= WL+1:
        hx = (x1+x2)//2
        set_px(canvas, hx, y1, blend(ROCK_M, (75,95,78), 0.5))
        if hx+1 < x2: set_px(canvas, hx+1, y1, blend(ROCK_M, (75,95,78), 0.3))

# 缝隙暗色——沿大块礁石边缘1px暗边，自然轮廓感
GAP = blend(ROCK_D, (18,28,22), 0.6)
for x1,y1,x2,y2 in big_rocks:
    # 顶边
    ty = max(WL+1, y1)
    for x in range(max(32,x1), min(x2,GW)):
        set_px(canvas, x, ty, GAP)
    # 左边
    lx = max(32, x1)
    for y in range(max(WL+1,y1), min(y2,GH)):
        set_px(canvas, lx, y, GAP)

# 藻类点缀（绿色点）— 定义在此，绘制移到礁石之后
algae_spots = [(53,26),(59,22),(35,30),(46,32),(55,28)]




# Left rock cluster
left_rocks = [(0,29,6,36),(4,27,10,36),(8,28,14,36),(12,30,18,36)]
for x1,y1,x2,y2 in left_rocks:
    for y in range(y1, min(y2,GH)):
        for x in range(x1, min(x2,GW)):
            if y < WL:
                set_px(canvas, x, y, ROCK_SUN_M if y==y1 else ROCK_SUN_D)
            else:
                set_px(canvas, x, y, ROCK_M if y==y1 else ROCK_D)

# Right rock cluster (mirror) — kept on right
right_rocks = [(GW-7,29,GW-1,36),(GW-11,27,GW-5,36),(GW-15,28,GW-9,36),(GW-19,30,GW-13,36)]
for x1,y1,x2,y2 in right_rocks:
    for y in range(y1, min(y2,GH)):
        for x in range(x1, min(x2,GW)):
            if y < WL:
                set_px(canvas, x, y, ROCK_SUN_M if y==y1 else ROCK_SUN_D)
            else:
                set_px(canvas, x, y, ROCK_M if y==y1 else ROCK_D)

# 中央礁石（右侧礁石平移到画面中央，y上移2行作为背景层）
# 右侧原坐标: x≈45~63, 中心x≈54 → 移到 x=32, offset=-22, 同时y-2
ctr_offset_x = -22
ctr_offset_y = -13
center_rocks = [(x1+ctr_offset_x, y1+ctr_offset_y, x2+ctr_offset_x, y2+ctr_offset_y)
                for x1,y1,x2,y2 in right_rocks]
for x1,y1,x2,y2 in center_rocks:
    for y in range(max(0,y1), min(y2,GH)):
        for x in range(max(0,x1), min(x2,GW)):
            if y < WL:
                set_px(canvas, x, y, ROCK_SUN_M if y==y1 else ROCK_SUN_D)
            else:
                set_px(canvas, x, y, ROCK_M if y==y1 else ROCK_D)

# 下排左侧礁石（中央往左偏12格，y上移10）
left2_offset_x = -12
for x1,y1,x2,y2 in [(x1+ctr_offset_x+left2_offset_x, y1-10, x2+ctr_offset_x+left2_offset_x, y2-10)
                     for x1,y1,x2,y2 in right_rocks]:
    for y in range(max(0,y1), min(y2,GH)):
        for x in range(max(0,x1), min(x2,GW)):
            if y < WL:
                set_px(canvas, x, y, ROCK_SUN_M if y==y1 else ROCK_SUN_D)
            else:
                set_px(canvas, x, y, ROCK_M if y==y1 else ROCK_D)

# 下排右侧礁石（中央往右偏12格，y上移10）
right2_offset_x = 12
for x1,y1,x2,y2 in [(x1+ctr_offset_x+right2_offset_x, y1-10, x2+ctr_offset_x+right2_offset_x, y2-10)
                     for x1,y1,x2,y2 in right_rocks]:
    for y in range(max(0,y1), min(y2,GH)):
        for x in range(max(0,x1), min(x2,GW)):
            if y < WL:
                set_px(canvas, x, y, ROCK_SUN_M if y==y1 else ROCK_SUN_D)
            else:
                set_px(canvas, x, y, ROCK_M if y==y1 else ROCK_D)

# 第三排：中央+左右，再下移8格，各增宽4格
row3_dy = -2
for x1,y1,x2,y2 in [(x1+ctr_offset_x-3, y1+row3_dy, x2+ctr_offset_x+3, y2+row3_dy)
                     for x1,y1,x2,y2 in right_rocks]:
    for y in range(max(0,y1), min(y2,GH)):
        for x in range(max(0,x1), min(x2,GW)):
            if y < WL:
                set_px(canvas, x, y, ROCK_SUN_M if y==y1 else ROCK_SUN_D)
            else:
                set_px(canvas, x, y, ROCK_M if y==y1 else ROCK_D)
for x1,y1,x2,y2 in [(x1+ctr_offset_x-12-3, y1+row3_dy, x2+ctr_offset_x-12+3, y2+row3_dy)
                     for x1,y1,x2,y2 in right_rocks]:
    for y in range(max(0,y1), min(y2,GH)):
        for x in range(max(0,x1), min(x2,GW)):
            if y < WL:
                set_px(canvas, x, y, ROCK_SUN_M if y==y1 else ROCK_SUN_D)
            else:
                set_px(canvas, x, y, ROCK_M if y==y1 else ROCK_D)
for x1,y1,x2,y2 in [(x1+ctr_offset_x+12-3, y1+row3_dy, x2+ctr_offset_x+12+3, y2+row3_dy)
                     for x1,y1,x2,y2 in right_rocks]:
    for y in range(max(0,y1), min(y2,GH)):
        for x in range(max(0,x1), min(x2,GW)):
            if y < WL:
                set_px(canvas, x, y, ROCK_SUN_M if y==y1 else ROCK_SUN_D)
            else:
                set_px(canvas, x, y, ROCK_M if y==y1 else ROCK_D)

# Algae tufts — 绘制移到礁石之后（见下方）









# 右上角小坡（从第一排礁石往右上延伸）
# 第一排礁石 y1 = 29 + ctr_offset_y = 29-13 = 16, x范围约 10~54
# 小坡第一组：右偏15, 上移5
for x1,y1,x2,y2 in [(x1+ctr_offset_x+15, y1-21, x2+ctr_offset_x+15, y2-21)
                     for x1,y1,x2,y2 in right_rocks]:
    for y in range(max(0,y1), min(y2,GH)):
        for x in range(max(0,x1), min(x2,GW)):
            if y < WL:
                set_px(canvas, x, y, ROCK_SUN_M if y==y1 else ROCK_SUN_D)
            else:
                set_px(canvas, x, y, ROCK_M if y==y1 else ROCK_D)
# 小坡第二组：右偏28, 上移2（比第一组略低，形成下坡感）
for x1,y1,x2,y2 in [(x1+ctr_offset_x+28, y1-18, x2+ctr_offset_x+28, y2-18)
                     for x1,y1,x2,y2 in right_rocks]:
    for y in range(max(0,y1), min(y2,GH)):
        for x in range(max(0,x1), min(x2,GW)):
            if y < WL:
                set_px(canvas, x, y, ROCK_SUN_M if y==y1 else ROCK_SUN_D)
            else:
                set_px(canvas, x, y, ROCK_M if y==y1 else ROCK_D)

# 缝隙补石（第一排和小坡之间，x≈40，y≈12）
for x1,y1,x2,y2 in [(x1+ctr_offset_x+10, y1-17, x2+ctr_offset_x+10, y2-17)
                     for x1,y1,x2,y2 in right_rocks]:
    for y in range(max(0,y1), min(y2,GH)):
        for x in range(max(0,x1), min(x2,GW)):
            if y < WL:
                set_px(canvas, x, y, ROCK_SUN_M if y==y1 else ROCK_SUN_D)
            else:
                set_px(canvas, x, y, ROCK_M if y==y1 else ROCK_D)

# ── Sea Turtle CENTER, facing up toward surface ───────────────
# 左侧礁石纹路（横竖线，限在礁石群 x=0~18, y=27~36）
GAP_L = blend(ROCK_D, (18,28,22), 0.6)
# 横纹
for y, x1, x2 in [(29,10,17),(33,13,21)]:
    for x in range(x1, x2):
        set_px(canvas, x, y, GAP_L)
# 竖纹
for x, y1, y2 in [(14,28,33),(21,33,36)]:
    for y in range(y1, y2):
        set_px(canvas, x, y, GAP_L)

TX, TY = CX, 27

# 海草（在礁石之后画，确保不被遮住；跳过海龟区域）
def on_turtle(x, y):
    return (((x-TX)/10)**2 + ((y-TY)/7)**2) <= 1.2

for ax,ay in algae_spots:
    if WL+1 <= ay < GH and not on_turtle(ax, ay):
        set_px(canvas, ax, ay, ALGAE)
        if ax+1 < GW and not on_turtle(ax+1, ay): set_px(canvas, ax+1, ay, ALGAE_L)
for ax in [3,7,11,15, GW-4,GW-8,GW-12,GW-16]:
    if not on_turtle(ax, 29): set_px(canvas, ax, 29, ALGAE_L)
    if not on_turtle(ax, 28): set_px(canvas, ax, 28, ALGAE)

SHELL_D  = (68, 95, 45)
SHELL_M  = (90, 128, 58)
SHELL_L  = (115, 158, 72)
SHELL_HL = (142, 188, 88)
SCUTE    = (52, 72, 28)
SKIN_D   = (82, 112, 62)
SKIN_M   = (108, 145, 82)

# Flippers — 更强的上宽下窄，前鳍7字型
# 前左鳍：根部4格宽，逐步收窄到1格，末端下弯
fl = [
    # 根部（靠近壳）4行宽
    (TX-4, TY-6),(TX-4, TY-5),(TX-4, TY-4),(TX-4, TY-3),
    (TX-5, TY-6),(TX-5, TY-5),(TX-5, TY-4),(TX-5, TY-3),
    # 中段3行宽
    (TX-6, TY-6),(TX-6, TY-5),(TX-6, TY-4),
    (TX-7, TY-6),(TX-7, TY-5),(TX-7, TY-4),
    # 开始下弯，2行宽
    (TX-8,TY-5),(TX-8,TY-4),
    (TX-9,TY-4),(TX-9,TY-3),
    # 末端1格
    (TX-10,TY-3),
    (TX-10,TY-2),
]
for px,py in fl:
    d = TX - px  # 距壳边距离
    set_px(canvas, px, py, SKIN_M if d <= 2 else SKIN_D)

# 前右鳍（镜像）
fr = [
    (TX+4, TY-6),(TX+4, TY-5),(TX+4, TY-4),(TX+4, TY-3),
    (TX+5, TY-6),(TX+5, TY-5),(TX+5, TY-4),(TX+5, TY-3),
    (TX+6, TY-6),(TX+6, TY-5),(TX+6, TY-4),
    (TX+7, TY-6),(TX+7, TY-5),(TX+7, TY-4),
    (TX+8,TY-5),(TX+8,TY-4),
    (TX+9,TY-4),(TX+9,TY-3),
    (TX+10,TY-3),
    (TX+10,TY-2),
]
for px,py in fr:
    d = px - TX
    set_px(canvas, px, py, SKIN_M if d <= 2 else SKIN_D)

# 后左鳍：根部3行宽，收窄到1格
rl = [
    (TX-3, TY+3),(TX-3, TY+4),(TX-3, TY+5),   # 根部3格宽
    (TX-4, TY+3),(TX-4, TY+4),(TX-4, TY+5),
    (TX-5, TY+4),(TX-5, TY+5),                 # 中段2格宽
    (TX-6, TY+5),(TX-6, TY+6),
    (TX-7, TY+6),                               # 末端1格
]
for px,py in rl:
    d = TX - px
    set_px(canvas, px, py, SKIN_M if d <= 1 else SKIN_D)

# 后右鳍（镜像）
rr = [
    (TX+3, TY+3),(TX+3, TY+4),(TX+3, TY+5),
    (TX+4, TY+3),(TX+4, TY+4),(TX+4, TY+5),
    (TX+5, TY+4),(TX+5, TY+5),
    (TX+6, TY+5),(TX+6, TY+6),
    (TX+7, TY+6),
]
for px,py in rr:
    d = px - TX
    set_px(canvas, px, py, SKIN_M if d <= 1 else SKIN_D)

# Shell ellipse wider horizontally (top-down view)
for dy in range(-7, 8):
    width = max(0, (6 if dy==0 else 7) - abs(dy))  # 中间行收窄1格
    for dx in range(-width, width+1):
        ed = (dx/3.0)**2 + (dy/2.5)**2
        if ed <= 1: col = SHELL_HL
        elif (dx/6.5)**2 + (dy/4.5)**2 <= 1: col = SHELL_L
        elif (dx/9.0)**2 + (dy/6.0)**2 <= 1: col = SHELL_M
        else: col = SHELL_D
        set_px(canvas, TX+dx, TY+dy, col)

# Scute pattern — 六边形/O型网格
# 中心六边形
hex_pts = [
    (-3,-1),(-2,-2),(-1,-3),(0,-4),(1,-3),(2,-2),(3,-1),(4,0),
    (3,1),(2,2),(1,3),(0,4),(-1,3),(-2,2),(-3,1),
]
for dx,dy in hex_pts:
    if abs(dx) <= max(0, (6 if dy==0 else 7) - abs(dy)):
        set_px(canvas, TX+dx, TY+dy, SCUTE)
# 辐射条纹：延伸到壳边缘
for i in range(3, 10):   # 左右
    if i <= 6: set_px(canvas, TX+i, TY, SCUTE)
    if i <= 6: set_px(canvas, TX-i, TY, SCUTE)
for i in range(3, 8):    # 斜向
    dy_ = i//2
    if abs(i) <= max(0, 7 - dy_):
        set_px(canvas, TX+i, TY-dy_, SCUTE)
        set_px(canvas, TX-i, TY-dy_, SCUTE)
        set_px(canvas, TX+i, TY+dy_, SCUTE)
        set_px(canvas, TX-i, TY+dy_, SCUTE)
for i in range(3, 7):    # 上下
    if i <= 7: set_px(canvas, TX, TY-i, SCUTE)
    if i <= 7: set_px(canvas, TX, TY+i, SCUTE)

# Head (top, facing up)
for dy in range(-9, -6):
    set_px(canvas, TX-1, TY+dy, SKIN_M)
    set_px(canvas, TX,   TY+dy, SKIN_M)
    set_px(canvas, TX+1, TY+dy, SKIN_D)
# Eyes (two dots)
set_px(canvas, TX-1, TY-9, (22,18,10))
set_px(canvas, TX+1, TY-9, (22,18,10))


# ── 水线切割礁石：在水线处加湿润暗边 + 水面以上加礁石阴影 ─────────
REEF_WET  = (32, 52, 38)   # 水线处湿润暗边
REEF_WET2 = (22, 38, 28)   # 水线+1（水下一格，最暗）

# 小坡和缝隙礁石的x范围（水面以上部分）
# 小坡1: x ≈ ctr_offset_x+15 + right_rocks_x范围
# 粗略扫描：在y=WL行，凡是礁石色（ROCK_M/ROCK_D）的格子加湿润边
import struct
GW2, GH2 = 64, 36
S2 = 12
for x in range(GW2):
    px_color = canvas.getpixel((x*S2+S2//2, WL*S2+S2//2))
    # 判断是否为礁石色（绿灰系，非天空/海水色）
    r,g,b = px_color
    # 礁石色特征：g > r 或 接近 ROCK_M/ROCK_D
    is_rock = (g > 50 and r < 80 and b < 80) or (r < 50 and g < 75 and b < 55)
    if is_rock:
        # WL行保留亮水线（不覆盖，让礁石与水面交接处有自然水线）
        set_px(canvas, x, WL, SURF_LINE)
        # WL+1行（水下第一格）压暗
        set_px(canvas, x, WL+1, REEF_WET2)
        # WL-1行（水面以上礁石底部）加暗边
        cur = canvas.getpixel((x*S2+S2//2, (WL-1)*S2+S2//2))
        set_px(canvas, x, WL-1, blend(cur, (15,25,15), 0.35))
# ── Characters holding hands, centered upper area ─────────────
GB    = (185, 108, 48)
GB_LT = (215, 148, 78)
GBD   = (128, 72, 28)
RED   = (192, 62, 48)
BUN   = (112, 172, 232)
BUN_LT= (155, 205, 248)
BUND  = (40, 75, 130)
GOGGLE    = (38, 50, 72)
GOGGLE_IN = (215, 168, 108)
BGOGGLE_IN= (148, 188, 215)

# Gingerbread LEFT of center
GCX, GCY = CX-5, 9

# Head
for dy in range(-2,3):
    for dx in range(-2,3):
        if abs(dx)+abs(dy)<=3:
            set_px(canvas, GCX+dx, GCY+dy, GB_LT if abs(dx)<=0 and abs(dy)<=0 else GB)
# Hat（小巧版，下移1格，顶部去左格）
for dx in range(-1,3):
    set_px(canvas, GCX+dx, GCY-1, RED)  # 原-2→-1
    set_px(canvas, GCX+dx, GCY-2, RED)  # 原-3→-2
set_px(canvas, GCX+1, GCY-3, RED)       # 原-4→-3，只留右格
# Body
for dy in range(3,6):
    for dx in range(-1,2):
        set_px(canvas, GCX+dx, GCY+dy, GB_LT if (dx==0 and dy==3) else GB)
# Legs
for dy in range(6,9):
    set_px(canvas, GCX-1, GCY+dy, GBD)
    set_px(canvas, GCX+1, GCY+dy, GBD)
# Right arm → holding hand toward bunny
for dx in range(2,5):
    set_px(canvas, GCX+dx, GCY+3, GB)
# Left arm (outer side)
for dx in range(-4,-1):
    set_px(canvas, GCX+dx, GCY+3, GB)

# Bunny RIGHT of center
BHX, BHY = CX+5, 9

# Ears (two separate ears)
for dy in range(-6,-1):
    set_px(canvas, BHX-1, BHY+dy, BUN_LT)  # 左耳
for dy in range(-6,-1):
    set_px(canvas, BHX+1, BHY+dy, BUN_LT)  # 右耳（浅色）
# Head
for dy in range(-2,3):
    for dx in range(-2,3):
        if abs(dx)+abs(dy)<=3:
            set_px(canvas, BHX+dx, BHY+dy, BUN_LT if abs(dx)<=0 and abs(dy)<=0 else BUN)
# Body
for dy in range(3,6):
    for dx in range(-1,2):
        set_px(canvas, BHX+dx, BHY+dy, BUN_LT if dx==0 else BUN)
# Legs
for dy in range(6,9):
    set_px(canvas, BHX-1, BHY+dy, BUND)
    set_px(canvas, BHX+1, BHY+dy, BUND)
# Left arm → holding hand toward gingerbread
for dx in range(-4,-1):
    set_px(canvas, BHX+dx, BHY+3, BUN)
# Right arm (outer side)
for dx in range(2,5):
    set_px(canvas, BHX+dx, BHY+3, BUN)

# Held hands (center between the two)
set_px(canvas, CX, GCY+3, BUN)

# Front-facing eyes
# GB eyes
set_px(canvas, GCX-1, GCY, (40,25,10))
set_px(canvas, GCX+1, GCY, (40,25,10))
# GB smile
set_px(canvas, GCX-1, GCY+1, GB)
set_px(canvas, GCX,   GCY+2, (148,82,32))
set_px(canvas, GCX+1, GCY+1, GB)
# Bunny eyes
set_px(canvas, BHX-1, BHY, (25,45,88))
set_px(canvas, BHX+1, BHY, (25,45,88))
# Bunny smile
set_px(canvas, BHX-1, BHY+1, BUN)
set_px(canvas, BHX,   BHY+2, (85,135,195))
set_px(canvas, BHX+1, BHY+1, BUN)

# small fish removed


# ── 最后：WL 和 WL-1 整行覆盖，穿过所有元素 ────────────────────
wrow(canvas, WL,   0, GW-1, SURF_LINE)
wrow(canvas, WL-1, 0, GW-1, (90, 148, 155))

# ── 入水叠色：WL-1 行角色腿部叠身体色+水色，表达入水边缘 ────────
WATER_TINT = (90, 148, 155)
_gb = (185, 108, 48); _bun = (112, 172, 232)
for _cx, _body in [(GCX, _gb), (BHX, _bun)]:
    for _dx in [-1, 0, 1]:
        _c = tuple(int(_body[i]*0.5 + WATER_TINT[i]*0.5) for i in range(3))
        set_px(canvas, _cx+_dx, WL-1, _c)

# ── 水面亮点（在 wrow 之后覆盖，确保可见）──────────────────────
for rx in [CX-8, CX-3, CX+3, CX+8, CX+14, CX-14]:
    set_px(canvas, rx,   WL, (142, 218, 208))
    set_px(canvas, rx+1, WL, (122, 205, 198))

# ── 残阳（动森风，压在水线上，下半为倒影）──────────────────────
SUN_CORE = (255, 238, 145)
SUN_RIM  = (252, 178, 75)
SX, SY = 12, WL-6  # 上移6格
for dy in range(-5, 1):  # 只画上半圆
    for dx in range(-5, 6):
        dist = dx*dx*1.0 + dy*dy*1.4
        if dist <= 8:
            set_px(canvas, SX+dx, SY+dy, SUN_CORE)
        elif dist <= 20:
            set_px(canvas, SX+dx, SY+dy, SUN_RIM)
# ── 太阳倒影（海面区域，WL-1往上）──────────────────────────────
REFL_HI  = (255, 232, 128)   # 倒影亮黄
REFL_MID = (242, 165, 65)    # 倒影橙
BREAK_ROWS = {WL-3, WL-5}    # 隔行横穿
for di in range(1, 5):
    y = WL - 1 - di           # 从WL-1往上
    rw_map = {1: 1, 3: 2}; rw = rw_map.get(di, max(1, 2 - di//2))  # 各收一格
    rc_map = {1: blend(REFL_HI, REFL_MID, 0.75), 3: blend(REFL_HI, REFL_MID, 0.25)}; rc = rc_map.get(di, blend(REFL_HI, REFL_MID, di/4))  # WL-2/WL-4颜色对调
    if y in BREAK_ROWS:
        pass
    else:
        for dx in range(-rw, rw+1):
            nx = SX + dx
            if 0 <= nx < GW:
                set_px(canvas, nx, y, rc)
        if di % 2 == 1:
            for nx in [SX-rw-2, SX+rw+2]:
                if 0 <= nx < GW:
                    set_px(canvas, nx, y, REFL_MID)
# ── WL 太阳折射高光（正对太阳三格）────────────────────────────
for dx in range(-1, 2):
    set_px(canvas, SX+dx, WL, (205, 238, 198))  # 暖亮青白

# ── 水下光带（单条，太阳正下方，WL+1起）────────────────────────
for y in range(WL+1, WL+14):
    alpha = max(0, 0.18 - (y-WL)*0.010)
    for dx in [-1, 0, 1]:
        nx = SX+dx
        if 0<=nx<GW:
            cur = canvas.getpixel((nx*S+S//2, y*S+S//2))
            set_px(canvas, nx, y, blend(cur, (142, 218, 208), alpha))

# 乌龟下肢下方两行填礁石色（覆盖海水色）
ROCK_FILL = ROCK_D  # 水下礁石深色
for y_fill in [TY+7, TY+8]:
    for x_fill in range(18, GW-18):
        set_px(canvas, x_fill, y_fill, ROCK_FILL)

# 海龟竖线延伸段最后覆盖礁石（确保可见）
for i in range(7, 8):
    set_px(canvas, TX, TY+i, SCUTE)

canvas.save('pixel_turtle_dusk.png')
print(f"Saved: {W}×{H}px")
