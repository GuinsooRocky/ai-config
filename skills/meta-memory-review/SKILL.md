---
name: meta-memory-review
description: 审核 memory_candidates 中的待处理候选，提炼高价值条目写入 auto-memory，清空未通过候选。触发场景：bulk extract 跑完后、定期维护记忆库、会话开始发现大量未审核候选时。触发词：/meta-memory-review、审核记忆候选、清空 memory_candidates。
---

# Memory Review

$ARGUMENTS（可选：`--type feedback|project|user` 只处理指定类型，默认按 feedback → user → project 顺序全部处理）

**DB 路径**：`/Users/lengmo/Desktop/cc-memory/memory/data/memory.db`
**Auto-memory 根目录**：`/Users/lengmo/.claude/projects/-Users-lengmo/memory/`

---

## Step 0：现状确认

```bash
DB=/Users/lengmo/Desktop/cc-memory/memory/data/memory.db
sqlite3 -header "$DB" "
SELECT type, COUNT(*) AS cnt
FROM memory_candidates
WHERE reviewed = 0
GROUP BY type
ORDER BY type;
"
```

若所有类型均为 0，输出"无待审核候选，流程结束"并停止。

---

## Step 1：按类型分批拉取候选

每次处理一个类型，分批查询（每批 100 条，避免上下文过长）：

```bash
sqlite3 "$DB" "
SELECT id, name, content
FROM memory_candidates
WHERE type = '<type>' AND reviewed = 0
ORDER BY id
LIMIT 100 OFFSET <offset>;
"
```

**处理顺序**：`feedback` → `user` → `project`
- feedback 和 user 通常条数少、价值密度高，优先处理
- project 条数多、过期率高，放最后

---

## Step 2：逐批分析，识别高价值条目

对每批候选进行筛选，**写入 auto-memory 的判断标准**：

### feedback 类
写入条件（满足任意一条）：
- 用户明确纠正过行为（"不要这样"、"换成..."）
- 用户确认过一个非显然的做法（"对，就这样"）
- 规则适用范围超出单次对话

**跳过**：单次临时操作的细节、已有相似 memory 覆盖的

### user 类
写入条件：
- 揭示用户身份 / 角色 / 专业背景的新信息
- 工作习惯 / 偏好中的非显然部分
- 不同领域的跨界背景信息

**跳过**：已在现有 user_*.md 中覆盖的内容

### project 类
写入条件（同时满足）：
- **非代码可推导**：不是读代码就能知道的信息
- **跨会话仍有效**：不是"今天临时做了 X"这类一次性状态
- **有操作指导意义**：未来遇到相关话题时会改变行为

**跳过**（这是 project 候选中的大多数）：
- 代码实现细节、架构分析
- 已完成的一次性任务（邮件归档、某次发版等）
- 会话内的临时调试状态
- 已有现有 memory 文件覆盖的

---

## Step 3：检查现有 memory，避免重复

写入前，先查 MEMORY.md 索引确认：
- 没有主题相同的现有文件
- 如有相关文件，考虑更新现有文件而非新建

```bash
cat /Users/lengmo/.claude/projects/-Users-lengmo/memory/MEMORY.md
```

---

## Step 4：写入 auto-memory

对筛选出的高价值条目，按类型写入对应文件：

**文件命名规范**（写到 `/Users/lengmo/.claude/projects/-Users-lengmo/memory/`）：
- `feedback_<topic>.md`
- `user_<topic>.md`
- `project_<topic>.md`
- `reference_<topic>.md`

**文件格式**：
```markdown
---
name: <记忆名称>
description: <一句话描述，用于决定未来是否召回>
type: feedback|user|project|reference
originSessionId: <当前会话 ID 或 unknown>
---

<记忆内容>

（feedback / project 类必须包含）
**Why:** <原因>
**How to apply:** <适用场景>
```

**同时更新 MEMORY.md**：
- 在对应位置追加一行：`- [名称](文件名.md) — 一句话钩子（<150 字符）`
- MEMORY.md 总行数控制在 200 行以内；超出时合并同类项

---

## Step 5：Ack 所有已审核候选

写入完成后，将**本批次所有 ID**（包括未通过的）一次性 ack：

```bash
sqlite3 "$DB" "
UPDATE memory_candidates
SET reviewed = 1
WHERE id IN (<逗号分隔的本批所有 ID>);
"
```

**注意**：
- 必须在写入 memory 文件后才 ack，确保数据不丢失
- 先获取所有 ID 再 ack，不要边审核边 ack
- 一次 UPDATE 即可，不要循环单条 update

---

## Step 6：输出审核摘要

```
## Memory Review 完成（YYYY-MM-DD）

### 写入 auto-memory（N 条）
- feedback_xxx.md：<一句话描述>
- project_xxx.md：<一句话描述>

### 跳过（N 条）
- feedback：N 条（代码细节 / 已覆盖 / 临时状态）
- project：N 条（代码分析 / 已完成任务 / 过期）
- user：N 条（已覆盖）

### Ack 状态
- 已标记 N 条为已审核
- 当前未审核剩余：N 条
```

---

## 注意事项

1. **project 类候选拒绝率通常 > 90%**：bulk extract 来的项目候选大多是代码分析，正常
2. **分批处理**：每类候选超过 150 条时，分 2 批查询，避免上下文溢出
3. **时效性判断**：包含具体日期的 project memory，写入时将相对日期转为绝对日期
4. **不要猜测**：候选内容不清楚来源时，宁可跳过，不要凭推断写入
