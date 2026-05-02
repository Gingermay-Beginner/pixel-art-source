from PIL import Image
import math

W, H, S = 64, 36, 12
img = Image.new("RGB", (W*S, H*S), (255,255,255))
pixels = img.load()

def sp(x, y, c):
    if 0<=x<W and 0<=y<H:
        for dy in range(S):
            for dx in range(S):
                pixels[x*S+dx, y*S+dy] = c[:3]

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

# ── Colors ──
WALL    = (205, 178, 142)
WALL_D  = (178, 152, 112)
WALL_LT = (225, 202, 165)
ARCH_FR = (188, 155, 112)
ARCH_D  = (148, 115, 78)
ARCH_IN = (72, 58, 105)     # 拱门内部（保留，不用）
ARCH_IN2= (95, 78, 138)
TILE_GN  = (58, 128, 88)    # 绿色瓷砖主
TILE_GND = (42, 98, 65)     # 绿色瓷砖暗缝
TILE_GNL = (88, 162, 112)   # 绿色瓷砖亮
ARCH_ST = (218, 215, 205)   # 星星
TILE_A  = (215, 188, 148)
TILE_B  = (185, 155, 112)
TILE_ACC= (162, 82, 55)     # 赤陶
FLOOR_A = (212, 192, 158)
FLOOR_B = (178, 152, 115)
FLOOR_G = (148, 115, 82)    # 地砖网格
TABLE   = (98, 68, 42)
TABLE_L = (132, 95, 62)
CLOTH   = (242, 232, 215)
LAMP_G  = (212, 158, 48)    # 金色灯笼
LAMP_L  = (252, 232, 155)
LAMP_D  = (168, 115, 25)

# 菜肴
PLATE   = (238, 230, 215)
HUMMUS  = (218, 188, 130)
HUMMUS_D= (185, 152, 88)
PITA    = (228, 200, 145)
PITA_D  = (195, 162, 102)
PARSLEY = (78, 155, 65)
OLIVE   = (55, 85, 42)
JUICE   = (185, 65, 48)
JUICE_L = (225, 108, 88)
CANDLE  = (252, 238, 168)
CANDLE_B= (218, 192, 148)

# 角色 - 姜饼人
GB      = (232, 155, 82)
GB_D    = (195, 122, 55)
GB_EYE  = (55, 38, 22)

# 角色 - 蓝兔子
BUN     = (108, 158, 212)
BUN_D   = (78, 125, 182)
BUN_IN  = (235, 148, 178)
BUN_EYE = (32, 65, 132)
BUN_LT  = (142, 188, 232)

# ── 1. 墙面 ──
fl(0, 29, 0, 63, WALL)
fl(24, 29, 0, 63, WALL_D)

# 墙面砖缝（错落）
for _wy in range(0, 30):
    for _wx in range(0, 64):
        _woff = (_wy // 6) % 2
        _wxmod = (_wx + _woff * 6) % 12
        if _wy % 6 == 0 or _wxmod == 0:
            if not (14 <= _wx <= 50 and _wy >= 6):  # 拱门内不画
                sp(_wx, _wy, WALL_D)

# ── 2. 摩尔拱门（宽版：x=13~51，顶部从y=6开始）──
AX = 32
# 拱门内部矩形（宽36格，高y=13~24）
# 拱门内竖条瓷砖
for _ty in range(13, 25):
    for _tx in range(14, 51):
        if _tx % 3 == 0 or _ty % 4 == 0:
            sp(_tx, _ty, TILE_GND)
        elif _tx % 3 == 1:
            sp(_tx, _ty, TILE_GNL)
        else:
            sp(_tx, _ty, TILE_GN)
# 拱顶椭圆弧（均匀2格描边，中心(32,13)，半宽19，半高7.5）
import math as _am
_ea, _eb = 19.0, 7.5
for y in range(4, 14):
    for x in range(10, 55):
        _ew = ((x - AX)**2) / _ea**2 + ((y - 13)**2) / _eb**2
        if _ew <= 1.0:
            if x % 3 == 0 or y % 4 == 0:
                sp(x, y, TILE_GND)
            elif x % 3 == 1:
                sp(x, y, TILE_GNL)
            else:
                sp(x, y, TILE_GN)
        else:
            # 检查距椭圆边界的像素距离
            _min_d = 99
            for _ny in range(y-4, y+5):
                for _nx in range(x-4, x+5):
                    _nw = ((_nx - AX)**2) / _ea**2 + ((_ny - 13)**2) / _eb**2
                    if _nw <= 1.0:
                        _min_d = min(_min_d, _am.sqrt((_nx-x)**2+(_ny-y)**2))
            if _min_d <= 2.5:
                sp(x, y, ARCH_FR)

# 拱门框架柱
fl(13, 24, 12, 13, ARCH_FR)
fl(13, 24, 51, 52, ARCH_FR)
# 柱底座
fl(24, 25, 11, 14, ARCH_D)
fl(24, 25, 50, 53, ARCH_D)

# 拱门内渐变（上部稍亮）
for y in range(6, 18):
    for x in range(15, 50):
        _ew = ((x - AX)**2) / 17.0**2 + ((y - 13)**2) / 7.0**2
        if _ew <= 1.0:
            pass  # 瓷砖已画



# ── 3. 横向绿条瓷砖腰线 y=22~29（拱门外两侧）──
for _ly in range(20, 30):
    for _lx in range(0, 64):
        # 跳过拱门区域（框架和内部）
        if 12 <= _lx <= 52:
            continue
        _rel = _ly - 20
        _loff = (_rel // 3) % 2
        _lxmod = (_lx + _loff * 4) % 8
        _lymod = _rel % 3
        if _lymod == 0 or _lxmod == 0:
            sp(_lx, _ly, TILE_GND)
        elif _lymod == 1:
            sp(_lx, _ly, TILE_GNL)
        else:
            sp(_lx, _ly, TILE_GN)
# 拱门内不画腰线（覆盖回去）
for _ty in range(22, 25):
    for _tx in range(14, 51):
        if _tx % 3 == 0 or _ty % 4 == 0:
            sp(_tx, _ty, TILE_GND)
        elif _tx % 3 == 1:
            sp(_tx, _ty, TILE_GNL)
        else:
            sp(_tx, _ty, TILE_GN)
fl(22, 24, 12, 13, ARCH_FR)
fl(22, 24, 51, 52, ARCH_FR)

# 横向瓷砖底边深色线
for _bx in range(0, 64):
    if not (12 <= _bx <= 52):
        sp(_bx, 29, TILE_GND)

# ── 4. 几何花砖地板 y=30~35 ──
for y in range(30, 36):
    for x in range(0, 64):
        base = (x//4 + y//4) % 2
        sp(x, y, FLOOR_A if base==0 else FLOOR_B)

for y in range(30, 36, 4):
    wrow(y, 0, 63, FLOOR_G)
for x in range(0, 64, 4):
    wcol(x, 30, 35, FLOOR_G)
# 十字点缀
for y in range(32, 36, 4):
    for x in range(2, 64, 4):
        sp(x, y, TILE_ACC)

# ── 5. 悬挂灯笼（x=32） ──
wcol(32, 0, 0, LAMP_D)  # 细链
# 灯笼体
fl(1, 2, 30, 34, LAMP_G)
fl(2, 6, 29, 35, LAMP_G)
fl(6, 7, 30, 34, LAMP_G)
# 内光
fl(3, 5, 30, 34, LAMP_L)
wrow(2, 30, 34, LAMP_D)
wrow(6, 30, 34, LAMP_D)
wcol(29, 2, 6, LAMP_D)
wcol(35, 2, 6, LAMP_D)
# 光晕
sp(32, 8, LAMP_L); sp(31, 8, (242, 225, 148)); sp(33, 8, (242, 225, 148))

# ── 6. 角色 ──
# 姜饼人 GCX=12, GCY=18（头中心y）
GCX, GCY = 12, 18

# 头
fl(GCY-2, GCY+2, GCX-2, GCX+2, GB)
sp(GCX-2, GCY-2, WALL); sp(GCX+2, GCY-2, WALL)
sp(GCX-2, GCY+2, WALL); sp(GCX+2, GCY+2, WALL)
sp(GCX-1, GCY-1, GB_EYE); sp(GCX+1, GCY-1, GB_EYE)
sp(GCX, GCY-1, GB_EYE)  # 鼻子
sp(GCX-1, GCY+1, GB_D); sp(GCX, GCY+1, GB_D); sp(GCX+1, GCY+1, GB_D)  # 嘴
# 颈
sp(GCX, GCY+2, GB); sp(GCX-1, GCY+2, GB)
# 身体
fl(GCY+3, GCY+6, GCX-2, GCX+2, GB)
sp(GCX-2, GCY+6, WALL); sp(GCX+2, GCY+6, WALL)
# 胳膊（举起，伸向食物）
wrow(GCY+3, GCX+3, GCX+5, GB)
sp(GCX+5, GCY+2, GB)
wrow(GCY+3, GCX-4, GCX-3, GB)

# 蓝兔子 BCX=52, BCY=17（头顶y）
BCX, BCY = 52, 17

# 耳朵（短，内粉）
fl(BCY-3, BCY, BCX-1, BCX-1, BUN)
fl(BCY-3, BCY, BCX+1, BCX+1, BUN)
fl(BCY-2, BCY, BCX-2, BCX-2, BUN)
fl(BCY-2, BCY, BCX+2, BCX+2, BUN)
fl(BCY-2, BCY, BCX-1, BCX-1, BUN_IN)
fl(BCY-2, BCY, BCX+1, BCX+1, BUN_IN)
sp(BCX-2, BCY-2, WALL); sp(BCX+2, BCY-2, WALL)  # 耳尖圆角

# 头
fl(BCY, BCY+4, BCX-3, BCX+3, BUN)
sp(BCX-3, BCY, WALL); sp(BCX+3, BCY, WALL)
sp(BCX-3, BCY+4, WALL); sp(BCX+3, BCY+4, WALL)
sp(BCX-1, BCY+1, BUN_EYE); sp(BCX+1, BCY+1, BUN_EYE)
sp(BCX, BCY+3, BUN_IN)  # 鼻
sp(BCX-2, BCY+2, BUN_LT); sp(BCX+2, BCY+2, BUN_LT)  # 腮红
# 身体
fl(BCY+5, BCY+8, BCX-2, BCX+2, BUN)
sp(BCX-2, BCY+8, WALL); sp(BCX+2, BCY+8, WALL)
# 胳膊
wrow(BCY+5, BCX-4, BCX-3, BUN)
wrow(BCY+5, BCX+3, BCX+5, BUN)

# ── 7. 桌子 ──
# 桌面 y=25~26
fl(25, 26, 6, 58, CLOTH)
wrow(25, 6, 58, TABLE)
wrow(26, 6, 58, TABLE_L)
# 桌腿
fl(27, 33, 8, 10, TABLE)
fl(27, 33, 54, 56, TABLE)
wrow(31, 8, 56, TABLE_L)  # 横撑

# ── 8. 餐桌上的菜 ──
# Hummus 盘（中左）x=22~33 y=24
wrow(24, 22, 33, PLATE)
wrow(24, 23, 32, HUMMUS)
sp(27, 24, HUMMUS_D); sp(28, 24, HUMMUS_D)
sp(26, 24, PARSLEY); sp(29, 24, PARSLEY)

# Pita 饼 x=34~41 y=24
wrow(24, 34, 41, PITA)
wrow(24, 35, 40, PITA_D)

# 橄榄小碟 x=43~48 y=24
wrow(24, 43, 48, PLATE)
for ox in [43, 45, 47]:
    sp(ox, 24, OLIVE)

# 石榴汁（左，姜饼人侧）x=7~9 y=21~25
fl(21, 24, 7, 9, JUICE)
fl(21, 22, 8, 8, JUICE_L)
wcol(8, 25, 26, LAMP_D)  # 杯脚

# 石榴汁（右，兔子侧）x=55~57 y=21~25
fl(21, 24, 55, 57, JUICE)
fl(21, 22, 56, 56, JUICE_L)
wcol(56, 25, 26, LAMP_D)

# 烤花椰菜（整颗，桌子中央主角）x=28~37 y=18~25
CAU_LT  = (215, 185, 82)   # 焦黄亮
CAU     = (188, 152, 55)   # 焦黄主
CAU_D   = (148, 112, 32)   # 焦暗
CAU_CH  = (205, 168, 68)   # 中间色
CAU_GN  = (68, 112, 48)    # 叶子绿
CAU_GND = (48, 82, 32)     # 叶子深绿

import math as _m
_cx, _cy = 32, 21
# 球体主体（圆形）
for _y in range(17, 26):
    for _x in range(27, 38):
        _d = _m.sqrt((_x-_cx)**2 + (_y-_cy)**2)
        if _d <= 5.2:
            _r2 = ((_x*7+_y*13) % 100) / 100
            if _d < 2:
                _c = CAU_LT
            elif _r2 > 0.6:
                _c = CAU_LT
            elif _r2 < 0.3:
                _c = CAU_D
            else:
                _c = CAU_CH
            sp(_x, _y, _c)
        elif _d <= 5.8:
            sp(_x, _y, CAU_D)

# 底部叶子
for _lx, _ly in [(28,25),(29,26),(30,25),(31,26),(32,25),(33,26),(34,25),(35,26),(36,25)]:
    sp(_lx, _ly, CAU_GN)
for _lx, _ly in [(29,25),(31,25),(33,25),(35,25)]:
    sp(_lx, _ly, CAU_GND)

# 高光
sp(30, 18, CAU_LT); sp(31, 18, (235,210,130))

# 蜡烛（备用，暂不画）
# sp(16, 23, CANDLE)
# sp(15, 24, (248, 222, 128)); sp(16, 24, (245, 212, 108)); sp(17, 24, (248, 222, 128))
# fl(25, 26, 15, 17, CANDLE_B)
# wrow(26, 15, 17, LAMP_D)

img.save('/home/azureuser/.openclaw/workspace/pixel_mazra.png')
print("Saved 768x432px")
