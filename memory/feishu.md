# memory/feishu.md — 飞书操作知识库

## 身份信息

- **App ID:** `cli_a94a44921d79dcc9`
- **App Secret:** `jY4YOWoYziaq4GRlhSTfHbuefa2EF0n2`
- **May 的 open_id:** `ou_071dd6ed65e00f018de63aecf0ca98f7`

---

## 断舍离多维表格

- **URL:** https://my.feishu.cn/base/RMOmbWfqYaCpb4sWfyVcbxQHnic
- **app_token:** `RMOmbWfqYaCpb4sWfyVcbxQHnic`
- **table_id:** `tblrhvTCsUSKK30r`

### 字段列表

| 字段名 | field_id | type | 说明 |
|--------|----------|------|------|
| 文本 | fld51yRTFh | 1 | 商品名（主字段） |
| 图 | fldqt7aOw4 | 17 | 图片附件 |
| 断舍离 | fldO4XnD1e | 4 | 多选 |
| 货币 | flddIpYd4C | 2 | 价格 |
| 使用频率 | fldT6qg7BF | 3 | 单选 |
| 属性 | fldrKNfK38 | 4 | 多选 |
| 国家 | fldIGdVZuV | 3 | 单选 |
| 存放位置 | fldvqceS99 | 1 | 文本 |
| 购买日期 | fldGslMyuB | 5 | 日期（毫秒UTC时间戳） |
| 购买渠道 | fldBRlUW5r | 3 | 单选 |
| 到期查看 | fldDIxK41I | 5 | 日期 |
| 父记录 | fldtQ6cU1D | 18 | 单向关联 |
| Note | fldGklRNXg | 1 | 备注 |

### 断舍离选项
待断 / 非必需 / 已断 / 不心动 / 已舍 / 视觉更新 / 卖 / 扔 / 换 / 小样 / 心动 / 必须

### 属性选项（常用）
家居用品 / 收纳用品 / 生活用品 / 厨具 / 小家电 / 家用电器 / 服饰 / 体育用品 / 健身用品 / 旅行用品 / 配件 / 文具 / 工具 / 包 / 首饰 / 化妆品 / 护肤品 / 化妆工具 / 摄影器材 / 猫咪用品 / 电子工具 / 书 / 杂志

### 购买渠道选项
天猫 / 淘宝 / 拼多多 / 闲鱼 / 1688 / 实体店 / 公司礼品 / 赠送 / 公家云

### 国家选项
中国（默认）/ 美国

---

## 记录写入格式（关键）

```python
# ✅ 正确：多选字段用文字名称列表
{"断舍离": ["心动"], "属性": ["化妆品", "护肤品"]}

# ✅ 正确：单选字段用文字名称字符串
{"购买渠道": "淘宝", "国家": "中国"}

# ✅ 正确：日期字段用毫秒UTC时间戳
{"购买日期": 1731715200000}

# ✅ 正确：图片字段
{"图": [{"file_token": "xxxxx"}]}

# ✅ 正确：父记录（单向关联）
{"父记录": ["recxxx"]}

# ❌ 错误：不要用 option_id 写入记录（会创建垃圾选项）
{"断舍离": ["optx3VCBUb"]}  # 错！
```

---

## 图片上传

```bash
curl -X POST "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_name=image.jpg" \
  -F "parent_type=bitable_image" \
  -F "parent_node=RMOmbWfqYaCpb4sWfyVcbxQHnic" \
  -F "size=$(stat -c%s image.jpg)" \
  -F "file=@image.jpg"
```

---

## 批量更新（>10条时用）

```bash
POST /bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_update
Body: {"records": [{"record_id": "xxx", "fields": {...}}, ...]}
# 每次最多500条
```

---

## 每日健康记录

- **URL:** https://my.feishu.cn/base/D2pibRIXhan2Mcs7G0QcUsQSnZc
- **app_token:** `D2pibRIXhan2Mcs7G0QcUsQSnZc`

---

## 微软股票追踪

- **详细记录：** `memory/stocks/msft.md`
- **URL:** https://my.feishu.cn/base/EQ0SboVQiaScqHsuD8nc032nniD
- **app_token:** `EQ0SboVQiaScqHsuD8nc032nniD`
- **table_id:** `tbleyS17jHmhKMiH`

---

## 天玑文章汇总表格

- **app_token:** `RI3xbrusOah6Zzs6ph3cxRiAnRf`
- **table_id:** `tblu7rvFDwJBMXI7`
- **字段:** 飞书链接(fld03kMiuG,15) / 自己标签(fld1yC0fhp,4) / 星级(fld6A52euh,2) / 重点(fldApxGIen) / To Do(fld2FOKE8N) / Date(fldrq3FsTa,5) / 原文公众号链接(fldJ1IqY0B,15) / 作者标签(fld5NzPGvf,4)

---

## 云文档

- **金渐成随笔 doc_id:** `Ivq3dhDUzoUQK2xwYWucAeZsnkb`
- **目标文件夹 folder_token:** `XScsf4W4El3GX9dbbIzcRPKBnKe`
- 日常随笔标题用正文第一句话

---

## 日常常规任务

### 任务一：金渐成文章整理入库
1. May 发来文章正文（或链接）
2. 判断类型：有标题/作者/日期 → 正式文章；无标题 → 唠嗑类
3. 在金渐成随笔文件夹新建飞书文档（folder: `XScsf4W4El3GX9dbbIzcRPKBnKe`）
   - 正式文章：标题用原文标题，正文从第一段写起
   - 唠嗑类：第一段作为标题，正文从第二段开始写入
4. 分批写入正文（15段/次），末尾加日期（唠嗑类加，正式文章不加）
5. 授权 May full_access（type=docx）
6. 查现有自己标签选项，按正文+问答内容选标签，不新建
7. 在天玑文章汇总新建行：
   - 飞书链接（文字默认文章标题）
   - 原文公众号链接（May 发来的链接，文字默认「金渐成」）
   - Date（文章日期，动态计算时间戳）
   - 作者标签（默认「金渐成」，May 指定才改）
   - 自己标签（查现有选项后填）
   - 星级（May 自己填）
8. 问 May 是否有问答要加

### 任务二：每日健康记录
- 表格：app_token `D2pibRIXhan2Mcs7G0QcUsQSnZc`，table_id `tblemTx7UgSGy64O`
- 字段：日期 / 体重(kg) / 跳绳数(个) / 跳绳时间(分钟) / 健康餐(次) / 普通饭菜(次) / 大餐(次) / 正面照 / 侧面照 / 牛奶咖啡(杯) / 水果 / 备注
- 流程：
  1. May 发来照片 → 上传图片到 bitable_image（parent_node 用该表 app_token）
  2. 询问其余数据（体重、咖啡、水果、运动、饮食次数）
  3. 一次性写入记录
  4. 有补充数据随时 PUT 更新
- 日期时间戳用代码动态计算：`datetime(y,m,d,tzinfo=timezone.utc).timestamp()*1000`

### 任务三：断舍离记录
- 表格：app_token `RMOmbWfqYaCpb4sWfyVcbxQHnic`，table_id `tblrhvTCsUSKK30r`
- 流程：
  1. 入库前先查重（按名称搜索）
  2. 国家默认中国，不询问
  3. 多选字段用文字名称列表
  4. 图片先上传获取 file_token，再写入
  5. >10条用 batch_create API
  6. 入库完发确认消息（含图片状态）

### 任务四：微软股票追踪（每月）
- 表格：app_token `EQ0SboVQiaScqHsuD8nc032nniD`，table_id `tbleyS17jHmhKMiH`
- May 告知 ESPP数量、Rewards数量、当前股价
- 写入日期 + 三个数字，公式字段自动计算总额

---



### 文章类型判断
- **有 title + 作者 + 日期** → 正常文章，标题用原文标题
- **唠嗑 / 日常随笔（无 title）** → 第一段作为飞书文档标题；**正文从第二段开始写入**（不重复第一段）；文字中无日期，May 会告知日期，放到文章末尾

### 完整入库步骤
1. 创建飞书文档（folder: `XScsf4W4El3GX9dbbIzcRPKBnKe`）
2. 写入全文正文（按段落分块，POST children API）
3. 唠嗑类：末尾加日期行
4. 授权 May full_access（type=docx）
5. 天玑表格新建行：飞书链接 + 原文公众号链接 + Date + 作者标签 + 自己标签 + 星级
6. 录完后问是否需要加问答

### 作者标签规则
- **不要自己添加**，必须 May 明确告知才填；必须从现有选项中选，不新建；不确定时问 May；May 没回复则留空

### 公众号来源规则（重要）
- 目前只有以下三个来源，不要自己编其他的：
  1. 金渐成
  2. 生玑伯伯
  3. 天机奇谈
- May 说"伯伯"= 生玑伯伯（默认）
- May 说"金"= 金渐成

### 自己标签规则
- ⚠️ 必须先查现有选项，只从里面选，绝不填不存在的
- May 不会指定，我来按内容判断，不问 May
- **正文和问答内容都要考虑**，两边提到的主题都可以加标签

### 星级规则
- 问 May，May 用数字回答（如：4）

### 问答格式（追加到文档末尾）
- 正文和问答之间空一行
- 格式：`问：……` / `答（YYYY-MM-DD）：……`
- 每组之间空一行，组内不空行
- 不带用户名和作者名
- 已有记录不改

### 飞书文档写入方式（关键）
- 用 POST `/docx/v1/documents/{DOC}/blocks/{DOC}/children`（不是 PATCH batch_update，那个会 404）
- 写入 body 保存到文件再 `--data-binary @file`（避免 shell 转义问题）
- 授权用 `type=docx`（不是 `type=doc`）

---

## 操作规则

- **国家默认中国**，除非 May 特别说明
- **每条新记录入库前查重**
- **断舍离选项**：必须 / 心动 / 视觉更新 / 换 / 非必需 / 不心动（无「收纳」）
- 改写入格式时先测一条，再批量
