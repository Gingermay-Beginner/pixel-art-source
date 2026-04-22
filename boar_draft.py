from PIL import Image

S = 24  # 放大倍数，方便看清
W, H = 30, 20
BG = (178, 210, 160)

BOAR_B   = (118,  98,  85)   # 主体深棕
BOAR_L   = (155, 132, 112)   # 浅棕
BOAR_LT  = (188, 165, 138)   # 更浅（耳）
BOAR_SN  = (178, 148, 122)   # 鼻吻粉棕
BOAR_EY  = ( 28,  18,  12)   # 眼睛黑
BOAR_TK  = ( 68,  50,  38)   # 深色轮廓
NOSTRIL  = ( 48,  32,  22)
TUSK     = (240, 228, 195)
STRIPE   = (148, 118,  92)
STRIPE_L = (168, 142, 112)

canvas = [[BG]*W for _ in range(H)]

def sp(x,y,c):
    if 0<=y<H and 0<=x<W: canvas[y][x]=c
def fl(y1,y2,x1,x2,c):
    for y in range(y1,y2+1):
        for x in range(x1,x2+1): sp(x,y,c)

ox,oy = 2,3  # 起点

# 身体（横向条纹）
fl(oy+2, oy+8, ox, ox+11, BOAR_L)
for sy in [oy+2, oy+4, oy+6]:
    fl(sy, sy+1, ox, ox+11, STRIPE)
    fl(sy, sy+1, ox+1, ox+10, STRIPE_L)

# 腿（4条）
for lx in [ox, ox+2, ox+8, ox+10]:
    fl(oy+9, oy+11, lx, lx+1, BOAR_B)

# 头（正面大方块，盖在身体右侧）
fl(oy+1, oy+9, ox+12, ox+19, BOAR_B)
# 头部圆角
for cx,cy in [(ox+12,oy+1),(ox+19,oy+1),(ox+12,oy+9),(ox+19,oy+9)]:
    sp(cx,cy,BG)

# 耳朵（头顶两个）
fl(oy-1, oy+1, ox+13, ox+14, BOAR_LT)
fl(oy-1, oy+1, ox+17, ox+18, BOAR_LT)
sp(ox+13,oy-1,BG); sp(ox+14,oy-1,BG)  # 耳尖圆角
sp(ox+17,oy-1,BG); sp(ox+18,oy-1,BG)

# 鼻吻（大方块）
fl(oy+4, oy+8, ox+13, ox+18, BOAR_SN)
sp(ox+13,oy+4,BOAR_B); sp(ox+18,oy+4,BOAR_B)
sp(ox+13,oy+8,BOAR_B); sp(ox+18,oy+8,BOAR_B)
# 鼻孔
sp(ox+14,oy+6,NOSTRIL); sp(ox+17,oy+6,NOSTRIL)
# 眼睛
sp(ox+14,oy+3,BOAR_EY); sp(ox+17,oy+3,BOAR_EY)
# 獠牙
sp(ox+14,oy+9,TUSK); sp(ox+15,oy+9,TUSK)
sp(ox+17,oy+9,TUSK); sp(ox+16,oy+9,TUSK)

img = Image.new('RGB',(W*S,H*S))
px = img.load()
for y in range(H):
    for x in range(W):
        c = canvas[y][x]
        for dy in range(S):
            for dx in range(S):
                px[x*S+dx,y*S+dy]=c
img.save('boar_draft.png')
print('Saved')
