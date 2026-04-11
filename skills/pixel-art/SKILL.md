---
name: pixel-art
description: 为 May 创作像素画场景。当用户要求画像素画、新场景、修改现有场景，或讨论姜饼人/蓝兔子角色时触发。支持根据日记/经历描述创作、主动创作、角色调整。
---

# 像素画创作技能

## 画布规格

```python
W, H = 64, 36      # 格子数（16:9）
SCALE = 12         # 每格放大倍数 → 最终 768×432 px
```

## 风格规范

- **参考**：动物森友会（Animal Crossing）——饱和但柔和、圆润
- **硬边像素风**：所有元素必须硬切边缘，禁止软渐变
- **角色比例**：大头Q版（Chibi），头占身高约2/3
- **不自作主张加功能**：未告知用户的细节不加；想加先问

## 固定角色（定稿，禁止随意修改）

### 姜饼人 🍪（代表 May）
```python
GB_BODY  = (185, 108,  48)
GB_ICING = (245, 232, 210)
GB_EYE   = ( 62,  35,  15)
GB_CHEEK = (225, 148,  95)
# 小画家帽（海景/白天场景用）
HAT_RED  = (188,  55,  48)   # 降饱和红，与蓝色海景和谐
HAT_DARK = (135,  32,  28)
HAT_LITE = (215,  88,  72)
```

### 蓝兔子 🐰（代表男友）
```python
BUN_BODY  = ( 95, 158, 215)
BUN_INNER = (210, 168, 190)
BUN_EYE   = ( 38,  22,  60)
BUN_BLUSH = (235, 155, 172)
```

### 共同规范
- 嘴型：O 型嘴（竖着两格，下格稍浅）
- 高光：耳朵附近高光与 `BUN_BODY` 保持一致，不要额外亮色（会显不自然）
- 颜色常量：功能删掉时同步删掉对应颜色常量，不留残留

## 场景参考文件

| 场景 | 文件 | 特点 |
|------|------|------|
| 观鲸（定稿v2） | `references/scene_whale.py` | 阴天、白天、双云、画家帽、座头鲸 |
| 火山（定稿wes71） | `references/scene_volcano.py` | 夜景、AC夜色配色、硬边烟雾 |
| 降落伞（天空没有声音） | `references/scene_parachute.py` | AC配色、白云、海面波纹、双人共乘 |

新场景时读对应参考文件，复用布局函数和颜色体系。

## 通用函数模板

```python
def blend(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(c1[i]*(1-t) + c2[i]*t) for i in range(3))

def set_px(canvas, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        canvas[y][x] = color

def wrow(canvas, y, x1, x2, color):
    # x2 是包含的右边界
    for x in range(x1, min(x2+1, W)):
        set_px(canvas, x, y, color)
```

## 配色体系

### 白天海景（观鲸）
```python
SKY_TOP=(88,168,225), SKY_MID=(120,195,235), SKY_LOW=(158,218,242), HORIZON=(195,232,248)
OCEAN_SURF=(48,168,178), OCEAN_MID1=(28,130,158), OCEAN_MID2=(15,98,138), OCEAN_DEEP=(8,65,115)
CLOUD_GREY=(168,222,240), CLOUD_DARK=(145,200,222)   # 阴天云，接近浅天空色
```

### AC夜景（火山）
```python
SKY_TOP=(14,16,68), SKY_MID=(32,42,108), HORIZON=(118,68,72)
MOON_Y=(255,245,185), STAR=(255,252,200), STAR2=(210,220,255)
```

## 发送命令

```bash
openclaw message send --channel telegram --account pixel \
  --target 8126278557 \
  --media /home/azureuser/.openclaw/workspace/<filename>.png \
  --message "<caption>"
```

## 铁律（教训）

1. ❌ 不自作主张加功能，想加先问
2. ❌ 禁止软渐变烟雾/云，必须用硬边像素块
3. ❌ `wrow` 第三个参数是**包含**的右边界（`range(x1, x2+1)`）
4. ❌ 改鳍/突出物边缘时，腹部/衔接区域左边界必须同步更新
5. ❌ 身体行右边界必须对齐衔接区域右边界，防止裸露深色格
6. ❌ 颜色常量跟功能一起生死——功能删掉，常量同步删
7. ✅ 水面太阳倒影效果好，海景/湖景可复用
8. ❌ **发图前必须确认输出文件名**：`pixel_whale_v2.py` 输出 `pixel_whale.png`，不是 `pixel_whale_v2.png`；每次运行后检查 `Saved: xxx` 输出
9. ❌ 深海区单个深色格看不出来（深色融于深海背景）；单格在深海里需用纯黑 `(0,0,0)` 或亮色 `WHALE_BELLY` 才有对比；连续2-3格效果更好
