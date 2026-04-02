# MEMORY.md - 小龙虾的长期记忆索引（L4 核心）

> **四层记忆模型：**
> - L1 会话记忆：当前对话 context（本次会话）
> - L2 流程记忆：memory/pending.md、每日日志（跨会话直到完成）
> - L3 知识记忆：专题 md，永久保存
> - L4 组织记忆：MEMORY.md / AGENTS.md / SOUL.md，永久核心

> **记忆写入原则：**
> - 新建任何表格/文档 → 立刻写入 memory/feishu.md 和本文件索引
> - 重要决策/教训 → 写入 memory/lessons.md
> - 待办/未完成事项 → 写入 memory/pending.md
> - 每日操作日志 → memory/YYYY-MM-DD.md

---

## 关于 May

- 名字：May
- 时区：北京时间（CST，UTC+8）
- 首次接触：2026-03-23

---

## 记忆图谱

```
MEMORY.md ← 核心索引（每次主会话加载）
├── memory/feishu.md      ← 飞书 API 知识、所有表格/文档
├── memory/lessons.md     ← 踩坑教训 & 最佳实践
├── memory/pending.md     ← 未完成事项（L2 流程记忆）
├── memory/stocks/        ← 投资相关（微软股票追踪等）
└── memory/YYYY-MM-DD.md  ← 每日操作日志
```

---

## 常规任务（日常）

| 频率 | 任务 |
|------|------|
| 日常 | 金渐成文章整理入库（天玑文章汇总） |
| 日常 | 每日健康记录（体重/运动/饮食/照片） |
| 日常 | 断舍离记录 |
| 每月 | 微软股票追踪更新（ESPP/Rewards/股价） |

## May 的常用工具（快速索引）

| 工具 | 链接/标识 |
|------|----------|
| 断舍离多维表格 | https://my.feishu.cn/base/RMOmbWfqYaCpb4sWfyVcbxQHnic |
| 天玑文章汇总 | app_token `RI3xbrusOah6Zzs6ph3cxRiAnRf` |
| 金渐成随笔文件夹 | https://my.feishu.cn/drive/folder/XScsf4W4El3GX9dbbIzcRPKBnKe |
| 每日健康记录 | https://my.feishu.cn/base/D2pibRIXhan2Mcs7G0QcUsQSnZc |
| 微软股票追踪 | https://my.feishu.cn/base/EQ0SboVQiaScqHsuD8nc032nniD |

---

## 断舍离操作规则（高频快查）

- **国家默认中国**，除非 May 特别说明
- 断舍离选项：必须 / 心动 / 视觉更新 / 换 / 非必需 / 不心动（无「收纳」）
- 每条新记录入库前先查重
- 入库完后发完整确认消息（含图片状态）
- 批量操作（>10条）用 batch_update API

---

## 能力边界

- 飞书多维表格（Base）：✅ curl 直接调 OpenAPI
- 飞书普通文档（docx）：✅ feishu_doc 工具
