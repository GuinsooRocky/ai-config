---
name: reference_session_transcripts_30day_window
description: Claude 会话记录只留 30 天（settings.json cleanupPeriodDays=30）；用 jsonl 做统计或找旧现场前先核真实时间窗，别按 mtime 过滤条件当样本起点
metadata:
  node_type: memory
  type: reference
  originSessionId: 3dba695b-8bab-46af-973f-1fd67d9f576a
  modified: 2026-10-30T15:01:36.269Z
---

`~/.claude/settings.json` 的 `cleanupPeriodDays` 是 30，`~/.claude/projects/*/*.jsonl` 里更早的会话已被清掉。

- 按「某日以来」扫会话时，mtime 过滤只是上限，样本实际只回溯约 30 天。报数前先取每个会话首条 timestamp 的最小值，写明真实窗口。
- 更早的事故现场要从项目 git 记录和仓内 docs 重建，翻不到不等于没发生过。

10-30 审开工三问时，我把一个月的样本说成「08-17 以来」，复核时才发现。相关：[[feedback_read_past_sessions_before_asking]]、[[feedback_find_lost_things_fast]]
