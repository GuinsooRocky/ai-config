---
name: meta-memory-audit
description: Claude Code 记忆系统月度审计：检查所有项目的 MEMORY.md，清理过期条目、合并重复记忆、删除无关项。触发场景：每月记忆整理、感觉记忆杂乱时。触发词：/meta-memory-audit、记忆审计、清理 MEMORY.md。
---

# Memory Audit

对 Claude Code 记忆系统进行周期性清理，确保记忆质量。

**DB 路径**：`/Users/lengmo/Desktop/cc-memory/memory/data/memory.db`
**Memory 根目录**：`/Users/lengmo/.claude/projects/-Users-lengmo/memory/`

---

## Step 0：Memory DB 健康检查

```bash
DB=/Users/lengmo/Desktop/cc-memory/memory/data/memory.db
sqlite3 -header "$DB" "
SELECT
  (SELECT COUNT(*) FROM sessions) AS total_sessions,
  (SELECT COUNT(*) FROM messages) AS total_messages,
  (SELECT MIN(started_at) FROM sessions) AS earliest,
  (SELECT MAX(started_at) FROM sessions) AS latest,
  (SELECT COUNT(*) FROM sessions WHERE tool_call_count >= 25) AS skill_candidates,
  (SELECT COUNT(*) FROM memory_candidates WHERE reviewed = 0) AS pending_review;
"
```

判断是否异常：
- sessions 数 **每月增长 > 300**：正常（活跃使用）；> 600 则提示考虑归档
- skill candidates 占比 **> 30%**：阈值可能需要调整
- 最新记录与今天相差 **> 3 天**：Stop Hook 可能中断，需排查
- pending_review **> 200**：建议先跑 `/meta-memory-review`

输出一行摘要：`DB 状态：正常 / 异常（原因）`

---

## Step 1：扫描所有记忆文件

```bash
MEM_DIR=/Users/lengmo/.claude/projects/-Users-lengmo/memory
ls -la "$MEM_DIR"
cat "$MEM_DIR/MEMORY.md"
```

读取每个被 MEMORY.md 索引的具体记忆文件。

---

## Step 2：逐条审查

对每条记忆评估：

**过期检查**：
- 包含绝对日期的记忆 → 是否已过期（候选人面试、项目 deadline、活动）
- 包含「待推进」「计划中」「TODO」的记忆 → 是否已完成
- 包含具体版本号 / 分支名 → 该版本/分支是否还活着

**重复检查**：
- 主题相似的多条记忆 → 合并为一条
- 同一人物 / 项目的多条记录 → 统一到一个文件

**时效检查**：
- 文件路径 / 函数名 → 验证仍然存在（Grep 或 Read）
- 项目状态快照 → 是否与当前代码 / git 状态一致

---

## Step 3：分类整理结果

```
## Memory Audit 结果（YYYY-MM-DD）

### 建议删除（N 条）
- [文件名] 条目名：原因（已过期 / 已完成 / 不再相关）

### 建议合并（N 条）
- [文件 A] + [文件 B] → 合并为 [文件 C]：原因

### 建议更新（N 条）
- [文件名] 条目名：需要更新的内容

### 状态良好（N 条）
- 无需操作
```

---

## Step 4：等待确认后执行

在用户确认后：
- 删除对应文件，同时从 MEMORY.md 中移除对应条目
- 合并文件内容，更新 MEMORY.md 索引
- 更新需要修改的记忆文件内容

---

## Step 5：更新 audit marker

执行完成后写入 marker 文件，让 SessionStart hook 知道刚跑过：

```bash
mkdir -p /Users/lengmo/.claude/cache
date +%Y-%m-%d > /Users/lengmo/.claude/cache/memory_audit_last.txt
```

---

## 审查频率建议

- **月度**：全量审查（本命令）
- **即时**：每次发现记忆与现实不符时，立即更新或删除
- **新增时**：先检查是否有可更新的现有记忆，避免重复写入
