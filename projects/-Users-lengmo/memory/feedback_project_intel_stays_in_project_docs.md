---
name: feedback_project_intel_stays_in_project_docs
description: 项目级情报(接口/迁移/探路结论)落项目文档，不写进全局 auto-memory
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9799331f-cae0-49f1-bac0-77ac558f460c
---

项目级的具体情报——某产品的接口 schema、迁移可行性结论、探路实测细节——**落到项目文档里**（如 `~/Desktop/cmm/*.MIGRATION-NOTES.md`），**不要写进全局 auto-memory**。全局 memory 只放**跨项目**的：人/偏好/工作法。

**Why**：2026-06-22 探 crushon 世界卡迁移接口后，我把"import JSON 写法+字段映射"建成 project 记忆，用户明确说"不要写进我的 memory，是项目级别的"。这类知识已存在项目文档中，重复进全局库是噪音。
**How to apply**：探路/调研收尾要存知识时，先分流——跨项目工作法→全局 memory；某项目的接口/数据/结论→项目内文档。拿不准就默认放项目文档。关联 [[feedback_real_requirement_archive]] [[feedback_research_must_writeback]]。
