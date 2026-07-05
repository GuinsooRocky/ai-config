---
name: meta-skill-mining
description: 从最近对话记录中提炼可复用 Skill 候选，识别重复执行的高频流程。触发场景：周期性梳理知识库、整理工作流、规划新 skill。触发词：/meta-skill-mining、扫高频流程、提炼 skill 候选。
---

# Skill Mining

$ARGUMENTS（可选：`--days N` 指定回溯天数，默认 7 天）

从最近 N 天的 Claude Code 对话中，识别重复出现的高频工作流，提炼为 Skill 候选清单。

**DB 路径**：`/Users/lengmo/Desktop/cc-memory/memory/data/memory.db`

---

## Step 1：DB 概况 + 会话列表

**1a. 先查 DB 整体分布**（Bash + sqlite3）：

```bash
DB=/Users/lengmo/Desktop/cc-memory/memory/data/memory.db
sqlite3 "$DB" "
SELECT
  CASE
    WHEN tool_call_count = 0 THEN '0'
    WHEN tool_call_count < 10 THEN '1-9'
    WHEN tool_call_count < 25 THEN '10-24'
    WHEN tool_call_count < 50 THEN '25-49'
    ELSE '50+'
  END AS bucket,
  COUNT(*) AS sessions
FROM sessions
WHERE started_at >= datetime('now', '-N days')
GROUP BY bucket ORDER BY bucket;
"
```

若 `tool_call_count >= 25`（skill candidate 阈值）的会话占比 > 30%，提示阈值偏低。

**1b. 拉取会话列表**（最近 N 天 top 50，按工具调用数排序）：

```bash
sqlite3 -header "$DB" "
SELECT id, project_path, title, started_at, tool_call_count, message_count
FROM sessions
WHERE started_at >= datetime('now', '-N days')
ORDER BY tool_call_count DESC
LIMIT 50;
"
```

重点关注：
- `tool_call_count >= 25` 的会话（skill candidate）
- 同一 `project_path` 重复出现的相似 `title`

---

## Step 2：采样高价值会话

对 skill candidate 中 tool_calls 最高的前 8-10 个 session，拉取开头消息：

```bash
SID="<session id>"
sqlite3 "$DB" "
SELECT role, substr(content, 1, 500) AS preview, tool_name
FROM messages
WHERE session_id = '$SID' AND rolled_back = 0
ORDER BY id ASC
LIMIT 15;
"
```

提取：
- 用户的初始请求（首条 user message）
- 执行了哪些主要步骤（assistant + tool 序列）
- 调用了哪些 MCP 工具（tool_name 字段）

---

## Step 3：识别可复用模式

判断标准（满足任意 2 条即为候选）：
1. **重复性**：同类请求在 N 天内出现 ≥ 2 次
2. **流程固定**：步骤顺序基本一致，有明确的 input → output
3. **工具组合**：使用了特定 MCP 工具链（如 figma + chrome、sqlite + grep）
4. **当前无 skill**：查看 `~/.claude/skills/` 和 `~/.claude/commands/` 确认未被覆盖

---

## Step 4：输出候选清单

格式：

```
## Skill 候选清单（YYYY-MM-DD，近 N 天）

### 高价值（建议本周创建）

**1. `<skill-name>`** — <一句话描述>
- 触发场景：...
- 核心步骤：...
- 工具依赖：...
- 放置位置：~/.claude/skills/ 或 ~/.claude/commands/<namespace>/

### 中价值（积累到 2-3 次再决定）

**2. `<skill-name>`** — <一句话描述>
- 触发场景：...
- 出现次数：N 次（具体日期）

### 已有 skill 可改进

- `<existing-skill>`：建议补充 <具体改进点>
```

> 本 skill 只出候选清单与改进点；已有 skill 的打分/frontmatter 合规审计交给 meta-check-skill。

---

## Step 5：更新 mining marker

执行完成后写入 marker 文件，让 SessionStart hook 知道刚跑过：

```bash
mkdir -p /Users/lengmo/.claude/cache
date +%Y-%m-%d > /Users/lengmo/.claude/cache/memory_mining_last.txt
```

---

## 参考：当前 Skill 分类规范

全局 skill（`~/.claude/skills/`）或全局 command（`~/.claude/commands/<ns>/`）：
- `meta:*`：系统维护类（skill-mining / memory-audit / memory-review）
- 其他按业务领域命名（onlychat / next15 / figma 等）

项目级 skill（`<project>/.claude/commands/`）：
- 依赖特定项目 MCP 工具或数据库的 skill
