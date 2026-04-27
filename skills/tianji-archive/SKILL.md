---
name: tianji-archive
description: 天玑文章整理入库。当 May 发来公众号文章（正文或链接）要求入库时触发。
---

# 天玑文章整理入库

## 公众号来源（只有这三个，不要自己编）

| May 说的 | 实际来源 |
|---------|---------|
| 金 / 金渐成 | 金渐成 |
| 伯伯 / 生玑伯伯 | 生玑伯伯 |
| 天机奇谈 | 天机奇谈 |

## 文章类型判断

- **有标题 + 作者 + 日期** → 正式文章
- **无标题（唠嗑/随笔）** → 第一段作为飞书文档标题，正文从第二段开始写入（不重复第一段）

## 完整入库步骤

1. **创建飞书文档**
   - folder_token: `XScsf4W4El3GX9dbbIzcRPKBnKe`
   - 正式文章：标题用原文标题
   - 唠嗑类：第一段作为标题
   - 无法写入目标文件夹时：先创建文档，再 move

2. **写入正文**
   - 用 `POST /docx/v1/documents/{DOC}/blocks/{DOC}/children`
   - 每批最多 10 段，用 Python urllib 写入（避免 shell 转义问题）
   - 唠嗑类：末尾加日期行（`YYYY-MM-DD`）
   - 正式文章：不加日期

3. **授权 May**
   ```
   POST /drive/v1/permissions/{doc_id}/members?type=docx
   {"member_type":"openid","member_id":"ou_071dd6ed65e00f018de63aecf0ca98f7","perm":"full_access"}
   ```

4. **查自己标签现有选项**
   - `GET /bitable/v1/apps/RI3xbrusOah6Zzs6ph3cxRiAnRf/tables/tblu7rvFDwJBMXI7/fields`
   - 只从现有选项中选，绝不填不存在的
   - 按正文内容判断，不问 May

5. **天玑汇总新建行**
   - app_token: `RI3xbrusOah6Zzs6ph3cxRiAnRf`
   - table_id: `tblu7rvFDwJBMXI7`
   - 字段：
     - `飞书链接`：`{"text": "文章标题", "link": "https://my.feishu.cn/docx/{doc_id}"}`
     - `原文公众号链接`：`{"text": "来源名称", "link": "May发来的链接"}`
     - `Date`：文章日期毫秒时间戳（用代码动态计算，不硬编码）
     - `作者标签`：May 告知才填；不确定时问 May；May 没回复则留空，**不要自己猜填**
     - `自己标签`：从现有选项中选
     - `星级`：留空，问 May

6. **收尾**
   - 问 May 星级（May 用数字回答）
   - 问 May 是否有问答要加

## 问答追加格式

```
（正文和问答之间空一行）

问：……
答（YYYY-MM-DD）：……

问：……
答（YYYY-MM-DD）：……
```

- 每组之间空一行，组内不空行
- 不带用户名和作者名
- 已有记录不改

## 时间戳计算（必须用代码）

```python
from datetime import datetime, timezone
ts = int(datetime(2026, 4, 25, tzinfo=timezone.utc).timestamp() * 1000)
```

## 飞书 API 鉴权

```python
import json, urllib.request
resp = urllib.request.urlopen(urllib.request.Request(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    data=json.dumps({"app_id":"cli_a94a44921d79dcc9","app_secret":"jY4YOWoYziaq4GRlhSTfHbuefa2EF0n2"}).encode(),
    headers={"Content-Type":"application/json"}, method="POST"
))
TOKEN = json.loads(resp.read())["tenant_access_token"]
```
