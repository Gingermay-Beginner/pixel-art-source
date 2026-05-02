from PIL import Image

W, H, S = 64, 36, 12
SKY    = (188, 218, 235)   # 动森天蓝
GROUND = (162, 198,  95)
GROUND_D = (130, 162,  72)
GROUND_L = (185, 222, 125)

# 船/滑梯颜色
SHIP_G  = ( 52,  98,  68)   # 动森深绿船身
SHIP_GD = ( 27,  72,  48)   # 柱子暗面同色
SHIP_GL = ( 78, 138,  98)   # 动森亮绿高光
SHIP_GR = ( 35,  72,  52)   # 中间色
SHIP_W  = (245, 240, 228)   # 白色装饰
SHIP_YL = (228, 195,  78)   # 船头黄色装饰

# 梯子
LADDER  = (155, 118,  62)
LADDER_D= (108,  82,  42)

# 角色
GB      = (185, 108,  48)
GBD     = (140,  82,  35)
GB_EYE  = ( 62,  35,  15)
GB_CHEEK= (225, 148,  95)
BUN_BODY= (118, 188, 248)
BUN_EAR = (235, 148, 178)
BUN_EYE = ( 22,  48, 108)
BUN_IN  = (235, 148, 178)

# 食物
BENTO_W = (255, 255, 255)   # 饭盒白色
BENTO_D = (215, 205, 188)   # 饭盒暗边
MEAT_R  = (195,  85,  52)   # 烤肉
MEAT_D  = (148,  58,  35)   # 烤肉暗
MEAT_CH = (228, 148,  72)   # 焦边
POTATO  = (125,  72, 145)   # 紫薯
POTATO_D= ( 88,  48, 108)   # 紫薯暗
PEA_G   = ( 85, 165,  72)   # 豌豆绿
PEA_GD  = ( 58, 122,  48)   # 豌豆暗
PEA_L   = (118, 198,  95)   # 豌豆亮
JACK_Y  = (195, 162,  55)   # 菠萝蜜黄
JACK_YD = (148, 118,  35)   # 菠萝蜜暗
JACK_SP = (158, 128,  42)   # 菠萝蜜刺
PINE_Y  = (232, 198,  88)   # 菠萝干黄
PINE_YD = (205, 168,  78)   # 菠萝干暗
PINE_YL = (252, 225, 128)   # 菠萝干亮

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

def wcol(x, y1, y2, c):
    for y in range(y1, y2+1): sp(x, y, c)

# ── 远景高大深色树（背景，x=0~63, y=5~28）──
TREE_BG  = (168, 195, 208)  # 动森远景树（更退后）
TREE_BGD = (152, 178, 195)   # 动森轮廓

def tall_tree(cx, base_y, h=14, w=3):
    # 树干（1格宽）
    for i in range(h//3): sp(cx, base_y-i, TREE_BG)
    top_y = base_y - h//3
    crown_h = h - h//3
    # 树冠（圆角轮廓：上下渐窄，中间最宽）
    for dy in range(crown_h):
        t = dy / max(crown_h-1, 1)
        if t < 0.15:
            spread = max(0, round(w * t / 0.15))
        elif t > 0.82:
            spread = max(0, round(w * (1-t) / 0.18))
        else:
            spread = w
        for dx in range(-spread, spread+1):
            sp(cx+dx, top_y-dy, TREE_BG)
        if spread > 0:
            sp(cx-spread, top_y-dy, TREE_BG)
            sp(cx+spread, top_y-dy, TREE_BG)

tall_tree(1, 28, 22, 2); tall_tree(7, 28, 26, 2); tall_tree(13, 28, 21, 2)
tall_tree(50, 28, 22, 2); tall_tree(56, 28, 26, 2); tall_tree(62, 28, 21, 2)
tall_tree(4, 28, 18, 1); tall_tree(10, 28, 20, 2); tall_tree(59, 28, 19, 1)
tall_tree(18, 28, 30, 2); tall_tree(24, 28, 28, 2); tall_tree(30, 28, 32, 2)
tall_tree(36, 28, 30, 2); tall_tree(42, 28, 29, 2); tall_tree(47, 28, 27, 2)
tall_tree(21, 28, 25, 1); tall_tree(33, 28, 26, 1); tall_tree(44, 28, 24, 1)
# x=0~55 y=17~27 高树色填充（船体后面）
fl(17, 27, 0, 55, TREE_BG)
fl(17, 27, 56, 63, TREE_BG)
# ── 蕨类植物（羽毛状，像椰子树轮廓）──
FERN_D = (52, 98, 58)
FERN_L = (72, 138, 75)
FERN_H = (138, 185, 72)  # 动森黄绿高光

def fern(cx, by, h=6):
    # 细茎向上
    for i in range(h+1): sp(cx, by-i, FERN_D)
    top = by - h
    # 从顶部放射出弧形羽状叶（每片叶子是一条弧线）
    fronds = [
        [(-1,-1),(-2,-1),(-3,-2),(-4,-2),(-5,-3)],
        [(-1,-2),(-2,-3),(-3,-3),(-4,-4)],
        [(0,-1),(0,-2),(0,-3),(0,-4)],
        [(1,-2),(2,-3),(3,-3),(4,-4)],
        [(1,-1),(2,-1),(3,-2),(4,-2),(5,-3)],
        [(-1,0),(-2,0),(-3,-1),(-4,-1)],
        [(1,0),(2,0),(3,-1),(4,-1)],
    ]
    for frond in fronds:
        for i,(dx,dy) in enumerate(frond):
            c = FERN_H if i >= len(frond)-2 else FERN_L
            sp(cx+dx, top+dy, c)
        # 中段也加一点亮绿
        if len(frond) >= 3:
            dx,dy = frond[len(frond)//2]
            sp(cx+dx, top+dy, FERN_H)

fern(4, 28, 6); fern(9, 28, 7); fern(1, 28, 5)
fern(56, 30, 6); fern(60, 30, 7); fern(53, 29, 5); fern(62, 30, 5)

# ── 地面 ──
fl(28, 35, 0, 63, GROUND)
for x in range(0, 64, 3):
    sp(x, 28, GROUND_D)
    if x % 6 == 0: sp(x+1, 29, GROUND_L)

# ── 滑梯（蓝色，从二层甲板 y=12 延伸到地面 y=28，斜向左下）──
SLIDE_B  = ( 72, 138, 198)   # 凉亭屋顶主蓝
SLIDE_BD = ( 48,  98, 158)   # 凉亭深蓝
for i in range(17):
    y = 11 + i
    xc = 23 - i
    if xc - 1 > 17: continue
    if xc + 2 <= 17 and y <= 12: continue
    x2 = min(xc+1, 17)
    wrow(y, xc-1, x2, SLIDE_B)
    sp(xc-2, y, SLIDE_BD)
    if xc+2 <= 17 and y != 13: sp(xc+2, y, SLIDE_BD)
# 滑梯侧壁
for i in range(16):
    y = 11 + i
    xl = 21 - i
    xl2 = min(xl-1, 17)
    xl1 = min(xl-2, 17)
    if xl1 <= xl2 and not (y == 13 and xl1 == 17): fl(y, y, xl1, xl2, SLIDE_BD)
# 清除 x=17 y=11~12 多余滑梯像素
sp(17, 11, SKY); sp(17, 12, SKY)
# ── 大船滑梯（双层）──

# ── 一层：船身主体（y=21~26, x=9~58）船头在右 ──
fl(21, 26, 27, 51, SHIP_G)
# 船底多一行
wrow(27, 27, 51, SHIP_G)
# 船身侧边暗色
# 船头（右侧，新轮廓 y=17~27，沿(57,17)→(52,27)斜线）
BOW_PROFILE = {17:55, 18:54, 19:54, 20:53, 21:53, 22:52, 23:52, 24:51, 25:51, 26:50, 27:50}
for y, x2 in BOW_PROFILE.items():
    wrow(y, 42, x2, SHIP_G)
    sp(x2, y, SHIP_GD)
# 黄装饰（右移1格）
for y, x2 in BOW_PROFILE.items():
    sp(x2+1, y, SHIP_GD)
    sp(x2, y, SHIP_GD)
# 一层甲板（y=19~20, x=11~56）
fl(19, 20, 27, 51, SHIP_G)
wrow(19, 27, 51, SHIP_GL)
wrow(20, 27, 51, SHIP_GL)



# x=50 列覆盖回船身主色
wcol(48, 21, 26, SHIP_G)


# 右侧船楼（x=44~57, y=17~20，延伸到白线位置）
fl(17, 20, 42, 49, SHIP_G)
# 船楼右侧跟随船头斜线
for dy, x2 in enumerate([55, 55, 54, 53]):
    wrow(17+dy, 42, x2, SHIP_G)
    sp(x2, 17+dy, SHIP_GD)
# 船楼顶部白线（y=17，x=44~57）
for dy, x2 in enumerate([55, 55, 54, 53]):
    sp(x2-1, 17+dy, SHIP_GD); sp(x2, 17+dy, SHIP_GD)
wrow(16, 42, 54, SHIP_GL)
wrow(17, 43, 53, SHIP_GL)
sp(42, 17, SHIP_GL)
sp(42, 19, SHIP_G); sp(42, 20, SHIP_G)
# 清除红线左边多余黄点
sp(53, 19, SHIP_G); sp(52, 20, SHIP_G)
# 船楼左侧暗色竖边

# ── 锚形图案（船头，中心 x=53, y=23）──
ANCHOR = (178, 145,  88)   # 锚色=绳梯浅色
AX, AY = 46, 21
# 锚顶横杠
wrow(AY, AX-2, AX+2, ANCHOR)
# 锚竖柄
for _y in range(AY+1, AY+5): sp(AX, _y, ANCHOR)
# 锚底横杠（弯钩两端）
sp(AX-2, AY+3, ANCHOR); sp(AX+2, AY+3, ANCHOR)
# 底部弧连接
sp(AX-1, AY+4, ANCHOR); sp(AX+1, AY+4, ANCHOR)
# 弯钩向上
sp(AX-2, AY+2, ANCHOR); sp(AX+2, AY+2, ANCHOR)
# 锚环（顶部小圆）
sp(AX, AY-1, ANCHOR)
# ── 二层：较窄平台（y=13~18, x=21~50）──
fl(13, 18, 24, 39, SHIP_G)
# 二层侧边暗色
# 二层甲板（y=11~12）
fl(11, 12, 24, 39, SHIP_GL)
# 二层高光
wrow(13, 25, 37, SHIP_GL)


# ── 凉亭（第三层，两根柱子从一层甲板通上去）──
PILLAR  = ( 27,  72,  48)   # 柱子深绿
PILLAR_L= ( 52, 105,  72)   # 柱子亮边
ROOF_B  = ( 72, 138, 198)   # 蓝色屋顶
ROOF_BD = ( 48,  98, 158)   # 蓝色暗
ROOF_BL = (108, 178, 228)   # 蓝色亮

# 左柱 x=23~24, y=7~26
fl(7, 27, 23, 24, PILLAR)
wcol(23, 7, 27, PILLAR_L)
# 左柱副本 x=14~15（二层左边缘）
fl(14, 27, 14, 15, PILLAR)
wcol(14, 14, 27, PILLAR_L)

# 右柱 x=38~39, y=7~26
fl(7, 27, 38, 39, PILLAR)
wcol(38, 7, 27, PILLAR_L)

# 蓝色三角屋顶（鱼鳞瓦片，顶点 x=31, y=3；底边 y=7）
for y in range(3, 8):
    width = round((y - 3) * 2.2) + 1
    x1 = 31 - width
    x2 = 31 + width
    wrow(y, x1, x2, ROOF_B)
    sp(x1, y, ROOF_BD)
    sp(x2, y, ROOF_BD)
# 鱼鳞纹：y=4,5,6,7 每行都画，交错偏移
for y in range(4, 8):
    width = round((y - 3) * 2.2) + 1
    x1 = 31 - width + 1
    x2 = 31 + width - 1
    offset = y % 2  # 奇偶交错
    for x in range(x1 + offset, x2 + 1, 3):
        sp(x, y, ROOF_BD)
# 屋顶亮色高光（左斜面）
for y in range(3, 7):
    width = round((y - 3) * 2.2) + 1
    sp(31 - width + 1, y, ROOF_BL)
# 屋顶底边压暗
wrow(7, 21, 41, ROOF_BD)


# 舷窗（圆形，四角圆）
PORT_F = (108, 178, 228)
PORT_D = ( 27,  72,  48)   # 柱子暗面同色
# 玻璃主体（挖空，留后处理）
# 外框（无四角）
sp(33, 13, PORT_D); sp(34, 13, PORT_D); sp(35, 13, PORT_D)  # 顶
sp(33, 17, PORT_D); sp(34, 17, PORT_D); sp(35, 17, PORT_D)  # 底
sp(32, 14, PORT_D); sp(32, 15, PORT_D); sp(32, 16, PORT_D)  # 左
sp(36, 14, PORT_D); sp(36, 15, PORT_D); sp(36, 16, PORT_D)  # 右
# 第二个舷窗（x=27~29, y=14~16）
sp(28, 13, PORT_D); sp(28, 17, PORT_D)
sp(26, 14, PORT_D); sp(30, 14, PORT_D)
sp(26, 15, PORT_D); sp(30, 15, PORT_D)
sp(26, 16, PORT_D); sp(30, 16, PORT_D)
sp(27, 13, PORT_D); sp(29, 13, PORT_D)
sp(27, 17, PORT_D); sp(29, 17, PORT_D)
# 小门左墙（x=16~18, y=13~18，浅绿，右侧圆角）
fl(14, 18, 16, 18, SHIP_GL)
# 右圆角（渲染前处理）
# 小门右墙（x=20~22, y=13~18，浅绿，左侧圆角）
fl(14, 18, 20, 22, SHIP_GL)
# 左圆角（渲染前处理）
# 蓝色装饰块
fl(26, 27, 3, 4, SLIDE_BD)
sp(3, 25, SLIDE_BD)
sp(4, 24, SLIDE_BD); sp(5, 24, SLIDE_BD)
sp(4, 25, SLIDE_BD); sp(5, 25, SLIDE_BD)
sp(4, 26, SLIDE_BD); sp(4, 27, SLIDE_BD); sp(5, 27, SLIDE_B)
sp(5, 26, SLIDE_B); sp(6, 26, SLIDE_B)
# ── 绳梯（网状，x=21~27, y=20~26）──
ROPE_V = (178, 145,  88)   # 竖绳米黄
ROPE_H = (128,  98,  55)   # 横绳深棕
# 竖绳（4根）
for _rx in [16, 18, 20, 22]:
    for y in range(20, 27):
        sp(_rx, y, ROPE_V)
# 横绳（每两格一道，覆盖在竖绳上）
for y in range(20, 27, 2):
    for _rx in range(16, 23):
        sp(_rx, y, ROPE_H)



# ── 姜饼人（坐，居中左区）──
GCX, GCY = 26, 21
# 头（宽7格，四角挖空）
wrow(GCY,   GCX-2, GCX+2, GB)          # 顶行收窄
wrow(GCY+1, GCX-3, GCX+3, GB)
wrow(GCY+2, GCX-3, GCX+3, GB)
wrow(GCY+3, GCX-3, GCX+3, GB)
wrow(GCY+3, GCX-3, GCX+3, GB)
wrow(GCY+4, GCX-3, GCX+3, GB)          # 底行（加宽两侧）
# 眼睛
sp(GCX-1, GCY+2, GB_EYE); sp(GCX+1, GCY+2, GB_EYE)
# 腮红
sp(GCX-2, GCY+3, GB_CHEEK); sp(GCX+2, GCY+3, GB_CHEEK)
# 帽子
HAT_RED=(188,55,48); HAT_DARK=(135,32,27); HAT_LITE=(215,88,72)
fl(GCY-1, GCY, GCX-1, GCX+3, HAT_RED)
wcol(GCX-1, GCY-1, GCY, HAT_DARK)
wcol(GCX+3, GCY-1, GCY, HAT_DARK)
sp(GCX, GCY-1, HAT_LITE)
sp(GCX+1, GCY-2, HAT_DARK)
# 脖子
wrow(GCY+4, GCX-1, GCX+1, GB)
# 嘴（脖子之后画，覆盖脖子色）
sp(GCX-1, GCY+4, GBD); sp(GCX, GCY+4, GBD); sp(GCX+1, GCY+4, GBD)
# 身体
fl(GCY+5, GCY+9, GCX-2, GCX+2, GB)
sp(GCX, GCY+6, GB_CHEEK); sp(GCX, GCY+8, GB_CHEEK)
# 手臂
sp(GCX-3, GCY+6, GB); sp(GCX-3, GCY+7, GB)
sp(GCX+3, GCY+6, GB); sp(GCX+3, GCY+7, GB)
# 腿（坐姿横向）
fl(GCY+10, GCY+11, GCX-2, GCX-1, GB)
fl(GCY+10, GCY+11, GCX+1, GCX+2, GB)


sp(22, 29, GB); sp(30, 29, GB)  # 手
# ── 姜饼人手持物品 ──

# 左手菠萝干圆圈（5x5，圆角，孔1x1，中心x=21,y=26）
# ox=19, oy=24
# 顶行（圆角去四角）
wrow(24, 20, 22, PINE_Y)
# 中间3行
sp(19, 25, PINE_Y); wrow(25, 20, 22, PINE_Y); sp(23, 25, PINE_Y)
sp(19, 26, PINE_Y); sp(20, 26, PINE_Y); sp(22, 26, PINE_Y); sp(23, 26, PINE_Y)  # 中心(21,26)留空=孔
sp(19, 27, PINE_Y); wrow(27, 20, 22, PINE_Y); sp(23, 27, PINE_Y)
# 底行（圆角去四角）
wrow(28, 20, 22, PINE_Y)
# 高光
sp(20, 24, PINE_YL)
sp(19, 25, PINE_YD); sp(23, 25, PINE_YD)

# 右手豌豆荚（x=30~31, y=23~29）
sp(31, 23, PEA_G)
sp(30, 24, PEA_L); sp(31, 24, PEA_G)
sp(30, 25, PEA_G); sp(31, 25, PEA_G)
sp(30, 26, PEA_L); sp(31, 26, PEA_G)
sp(30, 27, PEA_G); sp(31, 27, PEA_G)
sp(30, 28, PEA_L); sp(31, 28, PEA_G)
sp(31, 29, PEA_G)
# ── 蓝兔子（坐，居中右区）──
BCX, BCY = 37, 21
# 耳朵（粉色外侧）
fl(BCY-4, BCY-1, BCX-1, BCX-1, BUN_BODY)
fl(BCY-4, BCY-1, BCX+1, BCX+1, BUN_BODY)
fl(BCY-3, BCY-1, BCX-1, BCX-1, BUN_IN)  # 左耳粉色内侧
fl(BCY-3, BCY-1, BCX+1, BCX+1, BUN_IN)  # 右耳粉色内侧
fl(BCY-3, BCY-1, BCX-2, BCX-2, BUN_BODY)  # 左耳外侧蓝
fl(BCY-3, BCY-1, BCX+2, BCX+2, BUN_BODY)  # 右耳外侧蓝
# 头（宽7格，四角挖空）
wrow(BCY,   BCX-2, BCX+2, BUN_BODY)
wrow(BCY+1, BCX-3, BCX+3, BUN_BODY)
wrow(BCY+2, BCX-3, BCX+3, BUN_BODY)
wrow(BCY+3, BCX-3, BCX+3, BUN_BODY)
wrow(BCY+4, BCX-3, BCX+3, BUN_BODY)
wrow(BCY+5, BCX-2, BCX+2, BUN_BODY)
# 连心眉（y=BCY+1）
sp(BCX-2, BCY+1, (35, 68, 135)); sp(BCX-1, BCY+1, (35, 68, 135))
sp(BCX, BCY+1, (95, 162, 222))  # 中间比身体略深一点点
sp(BCX+1, BCY+1, (35, 68, 135)); sp(BCX+2, BCY+1, (35, 68, 135))
# 眼睛
sp(BCX-1, BCY+2, BUN_EYE); sp(BCX+1, BCY+2, BUN_EYE)
# 腮红
sp(BCX-2, BCY+3, BUN_IN); sp(BCX+2, BCY+3, BUN_IN)
# 嘴
sp(BCX-1, BCY+4, (255,255,255)); sp(BCX, BCY+4, (255,255,255)); sp(BCX+1, BCY+4, (255,255,255))
# 脖子
wrow(BCY+5, BCX-1, BCX+1, BUN_BODY)
# 身体
fl(BCY+6, BCY+9, BCX-2, BCX+2, BUN_BODY)
# 手臂
sp(BCX-3, BCY+7, BUN_BODY); sp(BCX-4, BCY+8, BUN_BODY)
sp(BCX+3, BCY+7, BUN_BODY); sp(BCX+4, BCY+8, BUN_BODY)
# 腿
fl(BCY+10, BCY+11, BCX-2, BCX-1, BUN_BODY)
fl(BCY+10, BCY+11, BCX+1, BCX+2, BUN_BODY)

# 兔子左手紫薯（完整，x=32~34, y=25~27）
POTATO_L=(175,128,195)
fl(25, 27, 32, 34, POTATO)
sp(32, 27, POTATO_D); sp(34, 27, POTATO_D)
sp(33, 28, POTATO_D)  # 薯蒂
sp(33, 24, POTATO)    # 顶芽
# 兔子右手紫薯（吃了一半，x=40~42, y=25~27）
fl(25, 27, 40, 42, POTATO)
wrow(25, 40, 42, POTATO_L)   # 顶行浅紫（截面）
sp(40, 27, POTATO_D); sp(42, 27, POTATO_D)
sp(41, 28, POTATO_D)  # 薯蒂

# ── 饭盒（姜饼人与兔子之间，x=29~34, y=30~32）──
fl(30, 32, 29, 34, BENTO_W)
wrow(30, 29, 34, BENTO_D)
wcol(29, 30, 32, BENTO_D)
wcol(34, 30, 32, BENTO_D)
wrow(32, 29, 34, BENTO_D)
# 分格线
wcol(31, 30, 32, BENTO_D)
# 盒内烤肉
sp(30, 31, MEAT_R); sp(31, 31, MEAT_D); sp(32, 31, MEAT_R); sp(33, 31, MEAT_R)
sp(30, 30, MEAT_CH); sp(32, 30, MEAT_CH); sp(33, 30, MEAT_CH)



sp(41, 17, SHIP_GL); sp(42, 18, SHIP_GL)

# x=6 y=11~12 挖掉
sp(6, 11, TREE_BG); sp(6, 12, TREE_BG)
sp(17, 11, TREE_BG); sp(17, 12, TREE_BG)
# x=16~17 y=19 滑梯挖掉
sp(16, 19, SKY); sp(17, 19, SKY)
# 小门圆角挖空
sp(18, 13, TREE_BG); sp(18, 18, TREE_BG)
sp(20, 13, TREE_BG); sp(20, 18, TREE_BG)
# 舷窗挖空（透出背景树色）
fl(14, 16, 33, 35, TREE_BG)
fl(14, 16, 27, 29, TREE_BG)

# ── 渲染 ──
img = Image.new('RGB', (W*S, H*S))
px = img.load()
for gy in range(H):
    for gx in range(W):
        c = canvas[gy][gx]
        for dy in range(S):
            for dx in range(S):
                px[gx*S+dx, gy*S+dy] = c

# x=24~25, y=20 是一层甲板，覆盖为亮绿（直接写渲染后图像）
for _gx, _gy, _c in [(16,19,TREE_BG),(17,19,TREE_BG),(25,19,SHIP_GL),(26,19,SHIP_GL),(40,18,SHIP_GL),(41,18,SHIP_GL),(40,19,SHIP_GL),(41,19,SHIP_GL),(40,20,SHIP_G),(41,20,SHIP_G),(55,16,SHIP_GD),(56,16,SHIP_GD),(54,17,SHIP_GL)]:
    for _dy in range(S):
        for _dx in range(S):
            px[_gx*S+_dx, _gy*S+_dy] = _c
    for _dy in range(S):
        for _dx in range(S):
            px[_gx*S+_dx, _gy*S+_dy] = _c
img.save('pixel_market.png')
print(f'Saved: {W*S}x{H*S}px')
