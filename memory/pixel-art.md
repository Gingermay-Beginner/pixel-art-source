# memory/pixel-art.md — 像素画专题记忆

> 每次定稿后更新本文件。新会话直接读这里，不用靠 compact summary。

---

## 画布规格

- 尺寸：64×36 格（16:9），每格 12px 放大 = 768×432px
- 风格：动物森友会（AC-inspired），暖色柔和，**全程硬边像素块，禁止软渐变**
- 工具：Python + Pillow

---

## 固定角色设定（已定稿，勿改）

### 姜饼人 🍪（代表 May）
- 身体：`GB_BODY=(185,108,48)`，暗色：`GBD=(140,82,35)`
- 眼睛：`GBE=(62,35,15)`
- 腮红：`GB_CHEEK=(225,148,95)`
- 糖霜：`GB_ICING=(245,232,210)`
- 帽子（画家帽）：`HAT_RED=(198,42,32)` / `HAT_DARK=(140,26,20)` / `HAT_LITE=(225,72,55)`
- 嘴巴：3像素同行横排（非倒V三角）

### 蓝兔子 🐰（代表男友）
- 身体：`BUN_BODY=(95,158,215)`，亮色：`BUN_LT=(145,195,240)`，暗色：`BUND`
- 眼睛：`BUNE=(38,22,60)`
- 腮红：`BUN_BLUSH=(235,155,172)`
- 嘴巴：`BUN_SMILE=(242,235,220)`，3像素同行

---

## 定稿作品索引

| # | 标题 | 文件 | 日期 | GitHub |
|---|------|------|------|--------|
| 1 | 小龙虾自画像 | `pixel_crayfish.png` | 2026-04-10 | `img/crayfish.png` |
| 2 | 火山的呼吸 | `pixel_volcano.py` | 2026-02-22 | `img/volcano.png` |
| 3 | 当鲸鱼从我们脚下游过 | `pixel_whale_v2.py` | 2026-02-21 | `img/whale.png` |
| 4 | 天空没有声音 | `pixel_parachute.py` | 2026-02-23 | `img/parachute.png` |
| 5 | 星空下泡澡 | `pixel_hotspring.py` | 2026-02-21 | `img/hotspring.png` |
| 6 | 云海日落 | `pixel_sunset.py` | 2026-02-28 | `img/sunset.png` |

---

## 云海日落定稿参数（v2，commit 95a5e96）

- GCX=27（姜饼人），BCX=37（蓝兔子）
- 两人**坐姿**，腿悬空，中间牵手
- 姜饼人戴红色画家帽，胸前一颗 GB_ICING 纽扣
- 腿：深色（GBD / BUND）
- 太阳：SX=13（偏左）
- 左侧云丘：**无**
- 右侧天文台球体：OBS_X=55, OBS_Y=17，逆光（大部分暗 OBS_DARK，左边缘亮 OBS_LIT）
- 右侧云丘：y=22-25，逆光，只有最左一格亮
- 波纹：隔行错开2格，跳过 x>=42 区域
- 明信片文字：「有一座山从海底长出来\n比任何山都高\n我们坐在它的肩膀上\n看云海燃烧成晚霞」

---

## 画廊

- URL：https://gingermay-beginner.github.io/pixel-gallery/
- GitHub 仓库：https://github.com/Gingermay-Beginner/pixel-gallery
- 本地文件：`gallery.html` → 上传为 `index.html`
- 图片：单独上传到 `img/`，HTML 用相对路径（禁止 base64）
- 小黑猫：`img/cat.png`（pixel_cat4.py，3帧行走 spritesheet）

---

## 重要规则

- `wrow(canvas, y, x1, x2, color)` → `range(x1, x2+1)`，x2 包含
- 胸鳍必须在腹部之后画
- 单像素：`set_px(canvas, x, y, color)`
- 发送图片：`openclaw message send --channel telegram --account pixel --target 8126278557 --media pixel_xxx.png`

---

## 作者别名

| 公众号 | 等同作者 |
|--------|---------|
| 生玑伯伯 | 金渐成 |
