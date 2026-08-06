---
name: feedback_session_id_by_content_not_mtime
description: "认\"当前 session\"的 jsonl 别用 mtime（并发会话同目录会抓错身），按内容指纹 grep 认"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 643b1eb6-9bd7-4101-a7f6-b69efcc07fb2
  modified: 2026-08-04T09:18:49.218Z
---

问"当前 session id"时，**不要**用 `ls -t ~/.claude/projects/-Users-lengmo/*.jsonl | head -1`（最近 mtime）来认——`-Users-lengmo/` 这个 project 目录下**同时有多个并发会话在写**（chat-cc-bot、telegram bot、cron agent 等），mtime 是竞态，抓到的"最近改动"经常是别的会话。

**Why:** 2026-06-17 我把 mtime 最新的 `1101eeb0` 当成当前 session 报给用户，实际那是 chat-cc-bot 会话（grep 命中 chat-cc-bot×621、agg 内容 0）；本对话（agg eval 重锚活）真身是 `643b1eb6`。几分钟后两个文件 mtime 还互相反超，证明 mtime 不可作身份依据。

**How to apply:** 按**内容指纹**认——grep 各候选 jsonl 找只有当前对话才有的字符串（本轮如 `6d487fa99`/`pin-gold`/`重锚`/`世界卡`/`agg-tuning`），命中的那个才是。mtime 顶多在"多个都内容命中"时做次级排序。相关：[[project_codegen_workflow]]、daily-recap 扫 jsonl 同理要按内容归属，别假设一个目录=一个会话。

**追加（2026-08-04，找"丢失的 session"）：** 用 `rg` 搜 `~/.claude/projects/` 必须带 `--hidden --no-ignore`——rg 默认静默跳过隐藏目录内容，裸跑会零命中，看起来像"transcript 不存在"（实际都在）。cwd 在别处（如 onlychat 仓）开的会话未必落在对应 project 目录，`-Users-lengmo/` 下大杂烩，还是按内容指纹认。用户说"session 找不到了"≠文件没了，先 rg 指纹再下结论。
