---
name: gallery-deploy
description: 将像素画推送到 GitHub Pages 画廊（https://gingermay-beginner.github.io/pixel-gallery/）。当用户说「定稿」「推画廊」「更新画廊」「加入画廊」时触发。
---

# 画廊操作指南

## 基本信息
- URL：https://gingermay-beginner.github.io/pixel-gallery/
- GitHub 仓库：https://github.com/Gingermay-Beginner/pixel-gallery
- 本地文件：`gallery.html` → GitHub 上传为 `index.html`
- 图片目录：`img/`，HTML 用相对路径（**禁止 base64 内嵌**）

## 上传图片到 GitHub

```python
import base64, json, urllib.request

with open('pixel_xxx.png', 'rb') as f:
    content = base64.b64encode(f.read()).decode()

TOKEN = 'ghp_xxx'  # 用后提醒用户删除

# 获取已有文件的 SHA（更新时需要）
req = urllib.request.Request(
    'https://api.github.com/repos/Gingermay-Beginner/pixel-gallery/contents/img/xxx.png',
    headers={'Authorization': f'token {TOKEN}', 'Accept': 'application/vnd.github.v3+json'}
)
try:
    data = json.loads(urllib.request.urlopen(req).read())
    sha = data['sha']
except:
    sha = None

# 上传
payload = json.dumps({
    'message': 'Add: xxx scene',
    'content': content,
    **({'sha': sha} if sha else {})
}).encode()

req2 = urllib.request.Request(
    'https://api.github.com/repos/Gingermay-Beginner/pixel-gallery/contents/img/xxx.png',
    data=payload,
    headers={'Authorization': f'token {TOKEN}', 'Content-Type': 'application/json'},
    method='PUT'
)
result = json.loads(urllib.request.urlopen(req2).read())
print(f"SHA: {result['content']['sha']}")
```

## 更新画廊 index.html

### 展品数据结构
```javascript
const paintings = [
  // 按添加顺序排列，最新在前
  {
    src: "img/xxx.png",          // ⚠️ 必须是 src，不是 file / img / path
    // src2: "img/xxx_v2.png",  // 可选：切换对比图
    title: "标题",
    date: "2026-02-21",
    caption: "配文（支持 \\n 换行，white-space:pre-line 已启用）",
    // desc: "旧字段，兼容保留，新画统一用 caption"
    stamp: "🎨",
    stampBg: "#ffd0b0"
  },
  // ...更多展品
];
```

> **⚠️ 加新画前必须先看一眼现有条目确认字段名**
> 图片字段：`src`（历史上曾错用 `file`，导致画显示不出）
> 配文字段：`caption`（支持 `\n` 换行）
```

**排序规则：** 手动顺序，最新在前。**不使用** `paintings.sort()`，数组顺序即显示顺序。

### 修改后验证 JS 语法
```bash
node -e "new Function($(cat gallery.html | grep -o 'const paintings.*\]' | head -1))"
# 或整体验证：
node -e "new Function(require('fs').readFileSync('gallery.html','utf8').match(/const paintings[\s\S]*?\];/)[0])"
```

**每次修改 gallery.html 后必须验证语法，再上传到 GitHub。**

### 上传 index.html
```python
# 同上传图片的方式，文件路径改为 'index.html'，内容来自 gallery.html
```

## 当前展品顺序（最新在前）⚠️ 权威列表，每次增删改必须同步更新

| # | 标题 | img 文件 | stamp | stampBg | 最后更新 |
|---|------|---------|-------|---------|---------|
| 1 | 偶遇海龟 | turtle_dusk.png | 🐢 | #d0e8d8 | 2026-04-13 |
| 2 | 不速之客 | eel.png | 🐍 | #d8eee8 | 2026-04-13 |
| 3 | 魔鬼鱼夜潜 | manta.png | 🤿 | #d0e8f0 | 2026-04-13 |
| 4 | 没有夕阳的日落 | beach_sunset.png | 📷 | #f5e8d8 | 2026-04-13 腿色修正 |
| 5 | 云海日落 | sunset.png | 🔭 | #f0e8d5 | 2026-04-13 |
| 6 | 星空下泡澡 | hotspring.png | 🛁 | #d0e8f5 | 2026-04-14 水下身体+手臂 |
| 7 | 天空没有声音 | parachute.png | 🪂 | #ddf0ff | 2026-04-13 |
| 8 | 当鲸鱼从我们脚下游过 | whale_v3.png（主）+ whale.png（切换） | 🐋 | #c8e8ff | 2026-04-13 v3为主 |
| 9 | 火山的呼吸 | volcano.png | 🌋 | #ffd0b0 | 2026-04-13 |
| 10 | 小龙虾自画像 | crayfish.png | 🦞 | #ffddc8 | 2026-04-10 |

**维护规则：**
- 新作品定稿 → 插到表格第1行，更新编号
- 现有作品修改（调色/调整构图等）→ 更新对应行的「最后更新」列，并重新推 img
- May 对旧作品有任何调整，都要在这里记录

## 注意事项
- GitHub token 使用后必须提醒用户删除
- 新展品插入 `paintings` 数组**最前面**
- 小黑猫是画廊固定观众，尾巴动画用 fillRect 像素方块，不改动

## ⚠️ 同步规则（必须遵守）

**本地 gallery.html 和 GitHub index.html 可能不同步。**

修改画廊前，必须先从 GitHub 拉取当前版本，在其上修改：

```python
import base64, json, urllib.request

TOKEN = 'ghp_xxx'
req = urllib.request.Request(
    'https://api.github.com/repos/Gingermay-Beginner/pixel-gallery/contents/index.html',
    headers={'Authorization': f'token {TOKEN}', 'Accept': 'application/vnd.github.v3+json'}
)
data = json.loads(urllib.request.urlopen(req).read())
sha = data['sha']
html = base64.b64decode(data['content']).decode('utf-8')
# 在 html 上修改，不要用本地文件覆盖
```

**替换 paintings 数组时，用字符串切片，不用 regex**（emoji 会导致 regex 乱码崩溃）：

```python
start_marker = 'const paintings = ['
start_idx = html.index(start_marker) + len(start_marker)
depth, idx = 1, start_idx
while idx < len(html) and depth > 0:
    if html[idx] == '[': depth += 1
    elif html[idx] == ']': depth -= 1
    idx += 1
end_idx = idx - 1
new_html = html[:start_idx] + new_entries + '\n' + html[end_idx:]
```

**推送前必须用 node 验证 JS 语法：**
```bash
node -e "
const html = require('fs').readFileSync('file.html','utf8');
const m = html.match(/const paintings\s*=\s*\[[\s\S]*?\];/);
new Function(m[0]);
console.log('OK');
"
```


---

## 当前展品（13张，按显示顺序，最新在前）⚠️ 权威列表

| # | 标题 | img 文件 | stamp | stampBg |
|---|------|---------|-------|---------|
| 1 | 挽救计划 | movie.png | 🎬 | #1a1a2e |
| 2 | 打工狗 kiwi | wework.png | 🥯 | #f5ead8 |
| 3 | 匹克球 | pickleball.png | 🏓 | — |
| 4 | 偶遇海龟 | turtle_dusk.png | 🐢 | #d0e8d8 |
| 5 | 不速之客 | eel.png | 🐍 | #d8eee8 |
| 6 | 魔鬼鱼夜潜 | manta.png | 🤿 | #d0e8f0 |
| 7 | 没有夕阳的日落 | beach_sunset.png | 📷 | #f5e8d8 |
| 8 | 云海日落 | sunset.png | 🔭 | #f0e8d5 |
| 9 | 星空下泡澡 | hotspring.png | 🛁 | #d0e8f5 |
| 10 | 天空没有声音 | parachute.png | 🪂 | #ddf0ff |
| 11 | 当鲸鱼从我们脚下游过 | whale_v3.png（主）+ whale.png | 🐋 | #c8e8ff |
| 12 | 火山的呼吸 | volcano.png | 🌋 | #ffd0b0 |
| 13 | 小龙虾自画像 | crayfish.png | 🦞 | #ffddc8 |

## 最新 commit

| 内容 | commit |
|------|--------|
| index.html（挽救计划加入） | `094b0a5a` |
| img/wework.png（kiwi新版） | `5d085cd5` |
| img/movie.png | `b733464` |
