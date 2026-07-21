---
name: memory-clean
description: 交互式精准清理 cc-memory 中期记忆库（SQLite）。支持按关键词/单次会话/项目路径/整库四种粒度，每一步都先预览后确认才执行。适用于：误录入敏感对话、清理测试数据、按项目批量移除。触发词：/memory-clean、清记忆、删 memory、清理 SQLite 中期记忆。只清 SQLite 中期记忆库；改 MEMORY.md 文件本体用 meta-memory-audit，审 memory_candidates 候选用 meta-memory-review。
---

# Memory Clean — 交互式精准清库

## 基本信息

- **DB 路径**：`/Users/lengmo/Desktop/cc-memory/memory/data/memory.db`
- **模块目录**：`/Users/lengmo/Desktop/cc-memory/`（所有 python 命令都要先 `cd` 到这里）
- **涉及表**：`sessions` / `messages` / `messages_fts`（虚表，触发器自动级联）/ `memory_candidates` / `recall_log` / `extraction_log`

## 核心原则（不可违反）

1. **永远先 SELECT 预览，再 DELETE** — 禁止无预览直接删
2. **永远用 AskUserQuestion 做二次确认** — 默认 No
3. **hard delete 是默认** — 物理删除，不保留 rolled_back 标记
4. **删完必须汇报剩余量** — 让用户知道库里还剩多少

## 流程

### Step 1：问用户删哪种粒度

用 `AskUserQuestion` 弹单选：

| 选项 | 说明 |
|---|---|
| `keyword` | 按消息内容关键词精准定位（最常用） |
| `session` | 删单次会话（需知道 session_id） |
| `project` | 按项目路径批量删 |
| `list` | 先不删，列近期 session 让用户看 |
| `nuke` | 整库清零（极危险） |

### Step 2：按用户选择跑预览

先跑这个命令拿到当前库状态作参考：

```bash
cd /Users/lengmo/Desktop/cc-memory && python3 -c "
from memory.db import get_memory_db
db = get_memory_db()
s = db.execute('SELECT COUNT(*) FROM sessions').fetchone()[0]
m = db.execute('SELECT COUNT(*) FROM messages').fetchone()[0]
mc = db.execute('SELECT COUNT(*) FROM memory_candidates').fetchone()[0]
print(f'当前：{s} sessions / {m} messages / {mc} candidates')
"
```

#### 2a. keyword 模式

问用户关键词，然后：

```bash
cd /Users/lengmo/Desktop/cc-memory && python3 <<'PY'
from memory.db import get_memory_db
db = get_memory_db()
KW = '<USER_KEYWORD>'  # 替换成用户给的关键词
rows = db.execute("""
    SELECT m.id, m.session_id, m.role, m.tool_name,
           substr(m.content, 1, 120) AS preview,
           m.timestamp,
           s.title, s.project_path
    FROM messages m JOIN sessions s ON s.id = m.session_id
    WHERE m.content LIKE ? AND m.rolled_back = 0
    ORDER BY m.timestamp DESC
    LIMIT 50
""", (f'%{KW}%',)).fetchall()
for i, r in enumerate(rows, 1):
    print(f"[{i}] msg_id={r['id']} sess={r['session_id'][:8]} role={r['role']} "
          f"{(r['project_path'] or '')[:30]} | {r['preview']!r}")
print(f"\n命中 {len(rows)} 条（若>50 只显示前 50）")
PY
```

列给用户看，然后用 `AskUserQuestion` 问：
- "删哪些？给编号（逗号分隔如 `1,3,5`），或 `all`，或 `cancel`"

如果用户给编号列表，用 `DELETE FROM messages WHERE id IN (...)` 精准删到消息级。
如果 `all`，删所有命中的消息。

#### 2b. session 模式

先跑 `memory_sessions` 等价的预览：

```bash
cd /Users/lengmo/Desktop/cc-memory && python3 -c "
from memory.db import get_memory_db
db = get_memory_db()
for r in db.execute('SELECT id, started_at, message_count, tool_call_count, substr(title,1,60) AS t, project_path FROM sessions ORDER BY started_at DESC LIMIT 30'):
    print(f\"{r['started_at'][:16]} | {r['id'][:8]} | msgs={r['message_count']:>4} | {r['project_path'] or '?':<35} | {r['t']}\")
"
```

让用户给完整 session_id（或前缀），用 `AskUserQuestion` 确认后删。

#### 2c. project 模式

问用户项目路径关键词（如 `onlychat`），然后预览命中的 sessions：

```bash
cd /Users/lengmo/Desktop/cc-memory && python3 -c "
from memory.db import get_memory_db
db = get_memory_db()
KW='<USER_KW>'
for r in db.execute(\"SELECT id, started_at, project_path, substr(title,1,50) AS t FROM sessions WHERE project_path LIKE ? ORDER BY started_at DESC\", (f'%{KW}%',)):
    print(f\"{r['started_at'][:16]} | {r['id'][:8]} | {r['project_path']} | {r['t']}\")
"
```

#### 2d. list 模式

只展示，不删。用来帮用户记起 session_id。

#### 2e. nuke 模式

**特别警告**：必须让用户**手打 `CONFIRM NUKE`** 才继续（不是点选）。

### Step 3：二次确认

无论哪种模式，**执行删除前**再用 `AskUserQuestion` 问一次：
- 标题："确认删除这 N 条记录？"
- 选项：`No, cancel` (默认) / `Yes, delete`

### Step 4：执行 DELETE

**session 级删除的完整级联**（删一个 session 要清 6 张表）：

```python
def delete_sessions(db, session_ids: list[str]):
    ph = ','.join('?' * len(session_ids))
    db.execute(f"DELETE FROM messages WHERE session_id IN ({ph})", session_ids)
    db.execute(f"DELETE FROM memory_candidates WHERE session_id IN ({ph})", session_ids)
    db.execute(f"DELETE FROM recall_log WHERE session_id IN ({ph})", session_ids)
    db.execute(f"DELETE FROM extraction_log WHERE session_id IN ({ph})", session_ids)
    db.execute(f"DELETE FROM sessions WHERE id IN ({ph})", session_ids)
    db.commit()
```

**message 级删除**（messages_fts 靠触发器自动同步）：

```python
db.execute(f"DELETE FROM messages WHERE id IN ({ph})", message_ids)
db.commit()
```

**nuke**：

```python
db.execute("DELETE FROM messages")
db.execute("DELETE FROM memory_candidates")
db.execute("DELETE FROM recall_log")
db.execute("DELETE FROM extraction_log")
db.execute("DELETE FROM sessions")
db.commit()
db.execute("VACUUM")
```

### Step 5：汇报结果

再次跑第 2 步开头的统计命令，告诉用户：
- 删了多少（增量）
- 剩多少

对大批删除（>100 条消息）跑一次 `VACUUM` 回收磁盘空间。

## 边界情况

- **库不存在** → 提示用户可能没装 hook，指向 `/Users/lengmo/Desktop/cc-memory/`
- **关键词为空** → 拒绝，避免误伤
- **session_id 前缀匹配到多个** → 列出所有匹配让用户挑，或要求完整 ID
- **当前正在进行的 session** → 该 session 还没 Stop，不会在库里，不用担心

## 软删除（可选，默认不用）

如果用户明确说"先软删，以后可能恢复"，用：

```sql
UPDATE messages SET rolled_back = 1 WHERE id IN (...)
```

软删的消息：
- 不会出现在 `[Memory Recall]` 注入里（因为代码里 `WHERE rolled_back = 0`）
- 不会出现在 `memory_search` 结果里
- 但物理上还在库里，可以 `UPDATE rolled_back = 0` 恢复

## 示例对话

```
用户: /memory-clean

Claude: [AskUserQuestion] 你想清哪种粒度？
  → keyword / session / project / list / nuke

用户: keyword

Claude: 关键词？

用户: OPENROUTER_API_KEY

Claude: [跑 SELECT，显示]
  命中 3 条：
  [1] msg_id=1247 sess=a3f2b8c1 role=user | '...给你 OPENROUTER_API_KEY 是 sk-...'
  [2] msg_id=1248 sess=a3f2b8c1 role=assistant | '...收到 OPENROUTER_API_KEY ...'
  [3] msg_id=1523 sess=d7e9f022 role=tool_result | '...OPENROUTER_API_KEY 未设置...'

  删哪些？(编号 / all / cancel)

用户: 1,2

Claude: [AskUserQuestion] 确认删这 2 条？
  → No, cancel / Yes, delete

用户: Yes

Claude: ✅ 已删 2 条消息。
  库状态：123 sessions / 4567 messages（-2）/ 0 candidates
```

## Codex compatibility

Preserve this workflow's intent and evidence rules. Translate Claude-specific tool names to the available Codex tools.
