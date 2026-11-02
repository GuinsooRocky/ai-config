---
name: feedback-migration-ok-pick-better-fix
description: lich 能迁移就迁移：别为绕开数据库迁移选次优方案；报方案时把「迁」的好处说出来
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8a263d9c-ae7f-4e12-8cfa-d1655e4b0300
  modified: 2026-11-02T15:23:47.113Z
---

修问题时不要为了「不用迁移」去选功能打折的方案。能追加迁移放行、行为更完整，就走迁移。

**Why:** 2026-11-03 lich 助手同步，我两次写「不用迁移」的绕法（字段只留本机，换电脑看不到），owner 说「如果要迁移，是可以迁移的」。迁移一个文件就解决了，换电脑的显示也完整。

**How to apply:** owner 放行后不重复问，照项目规则走：核对线上结构 → 回滚事务跑「修前失败」→ 执行 → 同样用例验允许与拒绝路径 → 先迁移再发代码。放宽类迁移才这样直接做；不可逆的数据改动仍先确认。相关：[[check-forbidden-before-batch-migration]]。
