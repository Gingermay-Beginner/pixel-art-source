from PIL import Image

W, H, S = 64, 36, 12

img = Image.new("RGB", (W*S, H*S))
px = img.load()

def p(r, c, col):
    if 0<=r<H and 0<=c<W:
        for sy in range(S):
            for sx in range(S):
                px[c*S+sx, r*S+sy] = col

def fill(r1, r2, c1, c2, col):
    for r in range(r1, r2+1):
        for c in range(c1, c2+1):
            p(r, c, col)

def wrow(r, c1, c2, col):
    for c in range(c1, c2+1):
        p(r, c, col)

# ── Sky ──────────────────────────────────────────────────────────────────────
# Very still, deep, almost vacuum-like blue
sky = [
    (0,  2,  (82,  172, 228)),
    (3,  6,  (108, 192, 238)),
    (7,  11, (138, 210, 245)),
    (12, 16, (165, 222, 248)),
    (17, 21, (188, 232, 250)),
    (22, 26, (205, 238, 252)),
    (27, 29, (218, 242, 253)),
    (30, 31, (232, 248, 255)),   # horizon 接近白
]
for r1, r2, col in sky:
    fill(r1, r2, 0, W-1, col)

# ── Ocean ──────────────────────────────────────────────────────────────────
ocean = [
    (32, 32, (78,  188, 198)),
    (33, 33, (55,  162, 178)),
    (34, 34, (38,  138, 162)),
    (35, 35, (25,  112, 145)),
]
for r1, r2, col in ocean:
    fill(r1, r2, 0, W-1, col)

# Horizon thin highlight line
wrow(31, 0, W-1, (218, 238, 250))
wrow(32, 0, W-1, (85, 175, 200))

# ── Parachute canopy ──────────────────────────────────────────────────────
# Centered at col 31-32, rows 2-12
# Dome shape rows
dome_rows = [
    ( -2, 25, 39),
    ( -1, 22, 42),
    (  0, 20, 44),
    (  1, 18, 46),
    (  2, 17, 47),
    (  3, 16, 48),
    (  4, 15, 49),
    (  5, 14, 50),
    (  6, 13, 51),
    (  7, 13, 51),
    (  8, 12, 52),
    (  9, 12, 52),
    ( 10, 12, 52),
    ( 11, 11, 53),
    ( 12, 11, 53),
    ( 13, 11, 53),
    ( 14, 11, 53),
]
# 4 color panels (stripes)
CA = (225, 85,  65)    # AC 暖珊瑚红
CB = (248, 238, 215)  # AC 奶油白
CC = (248, 205, 58)   # AC 阳光黄
CD = (58, 145, 198)   # sky blue panel

def chute_col(c):
    # 4-wide stripes repeating
    zone = (c - 24) % 8
    if zone < 2:   return CA
    elif zone < 4: return CB
    elif zone < 6: return CC
    else:          return CB

CHUTE_DARK = (165, 52, 38)
CHUTE_RIM  = (190, 148, 38)

N_STRIPES = 8
stripe_cols = [CA, CB, CC, CB, CA, CB, CC, CB]

for (row, c1, c2) in dome_rows:
    width = c2 - c1 + 1
    for c in range(c1, c2+1):
        t = (c - c1) / width          # 0→1 across this row
        zone = int(t * N_STRIPES)
        zone = min(zone, N_STRIPES-1)
        col = stripe_cols[zone]
        # darken edges
        if c == c1 or c == c2:
            col = CHUTE_DARK
        p(row, c, col)
    # stripe boundary lines
    for i in range(1, N_STRIPES):
        sc = c1 + round(i * width / N_STRIPES)
        if c1 < sc < c2:
            r2, g2, b2 = stripe_cols[i-1]
            p(row, sc, (max(r2-25,0), max(g2-25,0), max(b2-20,0)))

for c in range(0, 0):  # top rim removed
    p(0, c, (248, 240, 225))

for c in range(0, 0):  # removed bottom shadow line
    p(14, c, (185, 155, 100))

# ── Suspension lines ──────────────────────────────────────────────────────
ROPE = (235, 225, 205)

def draw_rope(pts):
    """Interpolate and draw every row between control points."""
    for i in range(len(pts)-1):
        r0, c0 = pts[i]
        r1, c1 = pts[i+1]
        steps = abs(r1 - r0)
        for s in range(steps+1):
            r = r0 + s
            c = round(c0 + (c1-c0) * s/steps)
            p(r, c, ROPE)

rope_pts_L  = [(14,11),(18,17),(22,22),(25,26)]
rope_pts_ML = [(14,22),(18,24),(22,26),(25,27)]
rope_pts_MR = [(14,42),(18,40),(22,38),(25,37)]
rope_pts_R  = [(14,53),(18,47),(22,42),(25,38)]

for pts in [rope_pts_L, rope_pts_ML, rope_pts_MR, rope_pts_R]:
    draw_rope(pts)

# ── Harness removed - ropes connect directly to characters ────────────────

# ── GB (姜饼人, left) ─────────────────────────────────────────────────────
# Seated, dangling legs below seat
GB   = (185, 108, 48)
GBD  = (142, 78,  30)
GBE  = (28,  18,  12)   # eyes
GBB  = (155, 88,  35)   # body shade
GBH  = (198, 122, 58)   # highlight

# Head: rows 19-24, cols 23-29
fill(19, 24, 23, 29, GB)
p(19, 23, sky[3][2]); p(19, 29, sky[3][2])
p(24, 23, sky[4][2]); p(24, 29, sky[4][2])
# Eyes (2px)
fill(21, 22, 24, 25, GBE)
fill(21, 22, 27, 28, GBE)
# Smile
p(23, 25, GBD); p(23, 26, GBD); p(23, 27, GBD)
# Cheeks
p(22, 23, (215, 130, 90)); p(22, 24, (215, 130, 90))
p(22, 28, (215, 130, 90)); p(22, 29, (215, 130, 90))

# Beret on GB — drawn AFTER head so it overlaps
HAT_RED  = (198, 42, 32)
HAT_DARK = (140, 26, 20)
fill(18, 19, 25, 29, HAT_RED)
p(18, 25, HAT_DARK); p(18, 29, HAT_DARK)
p(17, 27, HAT_RED)

# Body: rows 25-27
fill(25, 27, 25, 27, GB)
fill(25, 27, 26, 26, GBB)
# Buttons
p(25, 26, (242, 232, 210))
p(27, 26, (242, 232, 210))

# Legs dangling: rows 27-28
fill(27, 28, 25, 26, GB)
fill(27, 28, 26, 27, GB)
p(28, 25, GBD); p(28, 27, GBD)

# Arms
fill(25, 25, 22, 23, GB)
fill(25, 25, 28, 30, GB)

# ── BUN (蓝兔子, right) ──────────────────────────────────────────────────
BUN  = (95,  158, 215)
BUND = (65,  108, 178)
BUNE = (28,  18,  12)
BUNK = (225, 145, 165)   # ear pink
BUNH = (120, 178, 228)   # highlight

# Ears: rows 16-20
fill(16, 20, 35, 35, BUN); p(17, 35, BUNK); p(18, 35, BUNK)
fill(16, 20, 37, 37, BUN); p(17, 37, BUNK); p(18, 37, BUNK)

# Head: rows 19-24, cols 33-39
fill(19, 24, 33, 39, BUN)
p(19, 33, sky[3][2]); p(19, 39, sky[3][2])
p(24, 33, sky[4][2]); p(24, 39, sky[4][2])
# Eyes (2px)
fill(21, 22, 34, 35, BUNE)
fill(21, 22, 37, 38, BUNE)
# Nose
p(23, 36, BUNK)
# Cheeks (pink)
p(22, 33, (238, 148, 175)); p(22, 34, (238, 148, 175))
p(22, 38, (238, 148, 175)); p(22, 39, (238, 148, 175))

# Body: rows 25-27
fill(25, 27, 35, 37, BUN)
fill(25, 27, 36, 36, BUND)

# Legs dangling: rows 27-28
fill(27, 28, 35, 36, BUN)
fill(27, 28, 36, 37, BUN)
p(28, 35, BUND); p(28, 37, BUND)

# Arms
fill(25, 25, 32, 33, BUN)
fill(25, 25, 38, 40, BUN)

# birds removed

# shadow removed

# ── Clouds (AC style, round fluffy) ───────────────────────────────────────
CLD  = (255, 255, 255)
CLDS = (228, 238, 248)   # soft shadow

def cloud(r, c):
    # base row
    for dc in range(0, 6): p(r, c+dc, CLD)
    # top bumps
    for dc in range(1, 3): p(r-1, c+dc, CLD)
    for dc in range(3, 6): p(r-1, c+dc, CLD)
    p(r-2, c+2, CLD); p(r-2, c+3, CLD)
    # shadow bottom
    for dc in range(0, 6): p(r+1, c+dc, CLDS)

def cloud_big(r, c):
    # base row wider
    for dc in range(0, 9): p(r, c+dc, CLD)
    # top bumps
    for dc in range(1, 4): p(r-1, c+dc, CLD)
    for dc in range(4, 8): p(r-1, c+dc, CLD)
    p(r-2, c+3, CLD); p(r-2, c+4, CLD); p(r-2, c+5, CLD)
    # shadow bottom
    for dc in range(0, 9): p(r+1, c+dc, CLDS)

cloud(5, 4)    # left cloud
cloud_big(7, 52)   # right cloud
cloud(3, 47)   # upper right small
for dc in range(0,4): p(3, 47+dc, CLD)

# ── Ocean wave ripples ─────────────────────────────────────────────────────
WV1 = (98,  205, 215)
WV2 = (255, 255, 255)

# row 32 horizon shimmer
for c in [5, 12, 20, 28, 38, 48, 55]:
    p(32, c, WV2)

# row 33 ripple pairs
for c in [3, 10, 18, 26, 35, 44, 52, 58]:
    p(33, c,   WV1)
    p(33, c+1, WV1)

# row 34 ripple pairs offset
for c in [7, 15, 23, 31, 40, 50]:
    p(34, c,   WV1)
    p(34, c+1, WV1)

img.save("/home/azureuser/.openclaw/workspace/pixel_parachute.png")
print(f"Saved: {W*S}×{H*S}px")
