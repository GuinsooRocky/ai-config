---
name: daily-recap
description: 每日复盘 — 以 **06:00 为日界锚点**（凌晨 < 6 点跑则归入"昨天"）扫 Claude Code jsonl（`~/.claude/projects/-Users-lengmo/*.jsonl`），用 Sonnet 子 agent 按"业务模块"归并出**极简一句话** bullet 的日报，每个 bullet 保留 worktree 分支名 + 关键里程碑，其他全砍。日报**全部写进同一个文件** `~/Desktop/archives/每日复盘.md`（按日分节、最新在最下、`---` 分隔）并**只留最近 22 天**；**断网/没 token/没开电脑而漏掉的过去日，下次跑时自动回补**（jsonl 在本机长期保留，随时可补）。**周末（六/日）自动合并成一份**。触发词："每日复盘"、"今天跟 cc 聊了啥"、"今天跟你做了啥"、"写个日报"、"总结今天的对话"、"今天的 session 清单"。
---

# 每日复盘 Skill

用户要的是**可直接贴有道云笔记的极简日报**，不是分析报告。一个业务模块只一句 bullet，多余的细节让用户自己回 jsonl 翻，不要替他想。

## 何时使用

触发场景（任一命中即启动）：
- 用户说"每日复盘"、"帮我复盘"
- "今天跟 cc 都聊了啥"、"今天跟你做了啥"
- "写个日报"、"总结今天的对话"、"今天的 session 清单"

不适用：
- 只想展开某一个具体 session → 不走本 skill，直接 Read 对应 jsonl
- 跨多天的周报/月报 → 本 skill 只做当天，拒绝扩展（**周末合并是唯一例外**）

## 迭代校准（本 skill 每天回看一次）

用户每天用本 skill 跑一稿、手调出最终版、然后回看反推 skill。**累积约 10 次迭代后稳定**。

每次跑之前：
- 必看 `ref/samples/` 下最近 3-5 个 `YY.M.D-{星期}.md`，这是用户最近的成品口味，**新输出的 bullet 密度 / 粒度 / 措辞**要和样本对齐
- 样本数 < 3 时按本文规则跑，并提示用户跑完保存最终版到 `ref/samples/`

样本作用：本文是骨架规则，样本是当下口味校准 —— **样本和本文冲突时以样本为准**（口味会变，本文是滞后写下来的）。

## 周末合并（唯一的多日例外）

如果 `TARGET_DATE` 落在**周六或周日**（包括用户说的"上周末"、"周日"、"周六"等）→ **自动把六、日合并成一份**，不分两个标题。

判定与做法：
- `date -j -f "%Y-%m-%d" "$TARGET_DATE" "+%u"` 拿星期数（6=六、7=日），命中即扩展整周末
- Step 1 的 jsonl 扫描范围扩成 `[周六 06:00, 周一 06:00)`
- 标题用合并版：`YY.M.{D1}~{D2}-周末`（例 `26.4.25~26-周末`）；跨月写成 `26.5.31~6.1-周末`
- 跨两天同主题 → 一条 bullet；某一天没活动**不要**单列"周日无活动"

## 输出格式

### 全局排版铁律（最高优先级，覆盖一切）

- **不用 markdown 标题前缀**：日报标题 / cc 日记节标题都是**裸文本**，不带 `#` / `##` / `###`
- **不用加粗**：正文里**不出现** `**xxx**`
- **不用斜体**：正文里**不出现** `*xxx*` / `_xxx_`
- 唯一允许的 markdown：`-` bullet 前缀、反引号包代码标识符（如 worktree 名 / 文件路径 / 函数名）、以及**单文件里每天之间的 `---` 分节线**（由 upsert 脚本自动加，子 agent 不要自己写）
- 理由：成品要直接贴有道云笔记，多余的标题/加粗符号是噪声

### 标题
第一行**裸文本** `YY.M.D-{星期}`（**不要** `# ` 前缀）：
- `YY` 两位（`26`），`M.D` 不补零（`5.13`）
- 星期中文单字：一/二/三/四/五/六/日
- 周末合并版：`YY.M.{D1}~{D2}-周末`

### 正文 —— 极简一句话 bullet
- **纯 bullet**（`- ...`），永远不用表格
- **每个业务模块一条 bullet，一句话**。同一项目下多个业务模块 → 多条平行 bullet，**不要套总 bullet + sub-bullet**
- 一句话里要带的信息（顺序固定）：
  1. **业务模块名**（用户认知里的口语名，如"世界卡首页"、"世界卡创建"，不是 PRD 编号）
  2. **worktree 分支名**（如有，反引号包）
  3. **关键里程碑**（接口转正式 / Phase X 完成 / PR #号 / Issue #号 / Discussion #号 / 落档路径 — 选 1-2 个最硬的）
- 模板：`- 世界卡首页：worktree onlychat-agg-tuning，接口从 mock 转正式，跑通 3000`
- **能合就合，不能合就砍**。宁可少 3 条也别多 3 条 —— 用户上一稿砍了 17 条到 6 条
- 唯一允许 sub-bullet 的场景：一个业务模块当天有 **3 个及以上**等量级硬产物（PRD 反讲 + 落档 + 接口切换），可挂最多 3 个 sub-bullet

### 结尾
**不带任何寄语结尾**——`你自己再调一调` 这句**文件里不写、聊天里也不说**（2026-06-25 用户砍掉）。日报本体写完就完，交付时只客观点明（补了哪几天 / 砍了啥存疑），不加任何"自己再调"之类的收尾话。

## 执行步骤

### Step 1 — 锚定目标日期 + 找 jsonl

06:00 锚点：把"一天"重定义成 `06:00 ~ 次日 06:00`：
- 现在 < 06:00 → `TARGET_DATE = 昨天`
- 现在 ≥ 06:00 → `TARGET_DATE = 今天`

```bash
if [ "$(date +%H)" -lt 6 ]; then
  TARGET_DATE=$(date -v-1d +%Y-%m-%d)
else
  TARGET_DATE=$(date +%Y-%m-%d)
fi
find /Users/lengmo/.claude/projects/-Users-lengmo -maxdepth 1 -type f -name "*.jsonl" \
  -newermt "$TARGET_DATE 06:00:00" 2>/dev/null | xargs ls -la 2>/dev/null
```

后续步骤的标题日期、周末判定、跨月写法全部基于 `TARGET_DATE`，不要用系统当天。

### Step 1.5 — 补写遗漏日（backfill）

断网 / 没 token / 没开电脑会让某些天根本没跑过本 skill，于是 `~/Desktop/archives/每日复盘.md` 缺那几天的 section。jsonl 在本机长期保留，**下次一跑就把欠的补齐**。

把"要生成的日期"算出来，而不是只生成 `TARGET_DATE` 一天：

1. 回看窗口 = `TARGET_DATE` 往前数 21 天（含 `TARGET_DATE`，共 22 天）。再往前没意义——保鲜只留 22 天，补再多也会被修掉。
2. 逐天判断它**应不应该有日报**：该天 `[当天 06:00, 次日 06:00)` 窗口内**有 jsonl 活动**（mtime 命中且过得了 Step 2 硬门槛）就应该有。
   ```bash
   for i in $(seq 21 -1 0); do
     D=$(date -j -v-"$i"d -f "%Y-%m-%d" "$TARGET_DATE" "+%Y-%m-%d")
     N=$(find /Users/lengmo/.claude/projects/-Users-lengmo -maxdepth 1 -type f -name "*.jsonl" \
           -newermt "$D 06:00:00" ! -newermt "$(date -j -v+1d -f "%Y-%m-%d" "$D" "+%Y-%m-%d") 06:00:00" 2>/dev/null | wc -l)
     echo "$D activity=$N"
   done
   ```
3. 算每天对应的**标题**（套周末合并规则：六/日折叠成一个 `YY.M.{D1}~{D2}-周末`），`grep -qF "<标题>" ~/Desktop/archives/每日复盘.md` 看这个 section 在不在：
   - **过去日（< `TARGET_DATE`）**：section **已在文件里就跳过**——那是用户手调过的成品，绝不覆盖；缺、且当天有活动 → **补写**。
   - **`TARGET_DATE` 当天**：永远重新生成（upsert 会按同标题覆盖那一节，不动别天）。
   - 当天**没活动**（电脑关着那天）→ 不写，那天本来就没东西。
4. 把"要生成的日期清单"按从旧到新排好，**逐个**走 Step 2→Step 5（每个日期独立锚定它自己的扫描窗口与标题，逐个 upsert 进单文件）。补写的过去日只需稳妥还原，不必追求和当天一样的精修。
5. upsert 脚本每次都内置 22 天保鲜，无需单独再跑一遍。

补写时若一次补了多天，在交付时一句话点明"顺手补了 X.X、X.X 两天"，别闷声生成。

### Step 2 — 过滤（硬门槛 + 救回白名单）

**硬门槛 skip**：`size < 0.1MB **且** user_msgs ≤ 3` → 直接丢弃，不进入 sub-agent 视野。

**救回白名单**（命中任一就加回）：
- session 里提了 GitHub/Gitea **PR / Issue / Discussion 号**（grep `#\d+` 配合上下文核证，不是裸数字）
- 当天**新装的 skill 且当天用过**（`Skill` tool 调用 + skill 安装路径在 `~/.claude/skills/` 下 mtime 命中当天）
- 提交了 **commit-cr / CI** 相关产物（沙盒分支、新 workflow 文件）

**其他一律不进入**（哪怕用户在那个 session 说过几句话）：
- 一句话浅聊（"z97 啥意思"、"为啥电脑热"）
- 磁盘清理 / 临时排查无结论
- 查别人的 PR 状态（自己没动）
- 临时给别人配工具（自己不用）
- 装了 skill 但当天没用

判定脚本（用 `ref/extract.py` 跑完拿到 `size_mb` + `user_msgs_count` + `keywords` 后逐条过）：
```python
def keep(s):
    if s.size_mb >= 0.1 or s.user_msgs_count > 3:
        return True
    # 救回白名单
    kws = s.keywords
    if any(k in kws for k in ('PR', 'Issue', 'Discussion')) and grep_real_hash(s):
        return True
    if installed_skill_used_today(s):
        return True
    if 'commit-cr' in kws or 'CI/CD' in kws:
        return True
    return False
```

（救回判定可以让主 agent 跑完 extract.py 后手工 grep 上下文核证，不必硬实现 `grep_real_hash`。）

### Step 3 — 抽取每个保留 session 的内容

用 `python3 ref/extract.py <path1> <path2> ...` 抽（按需 Read 该文件，不要默认加载到上下文）。

输出包含每个 session 的：`session_id` / `size_mb` / `cwds` / `user_msgs_first5` / `user_msgs_last5` / `tool_uses` Top15 / `keywords` 命中字典 / `context_resets` 次数。

### Step 4 — 调 Sonnet 子 agent 归并

**用 Agent 工具起一个 `general-purpose` 子 agent，model override 为 `sonnet`**（model id `claude-sonnet-4-6`，最新最便宜可用 Sonnet）。

子 agent 的输入：
1. Step 3 抽出来的所有保留 session 数据（JSON 整块）
2. `ref/samples/` 下最近 3-5 个最终成品（**作为口味标杆**）
3. 本文 `输出格式 · 正文` 段（作为硬约束）

子 agent 的任务（贴在 prompt 里）：
> 你要把这堆 jsonl 抽取结果归并成一份"日报草稿"。
>
> **排版铁律（最高优先级）**：
> - 日报标题用**裸文本** `YY.M.D-{星期}`，**绝不**带 `# ` 前缀
> - cc 日记节标题用**裸文本** `cc 日记（近 2 天）`，**绝不**带 `## ` 前缀
> - **不要任何加粗** `**...**`、**不要任何斜体** `*...*` / `_..._`
> - 唯一允许的 markdown：`-` bullet 前缀、反引号包代码标识符
>
> **内容硬约束**：
> - 一个业务模块一句话 bullet，平行排列
> - 每句话带：业务模块名（口语化）+ worktree 分支名（如有）+ 1-2 个硬里程碑（接口转正式 / Phase X / PR# / Issue# / 落档路径）
> - 总 bullet 数对照样本量级，宁少勿多
> - 不要 sub-bullet（除非某业务模块当天有 ≥3 个等量级硬产物）
> - 不写 session ID / size / 时间戳
> - 浅聊 / 磁盘清理 / 临时配置 / 装了未用 一律不出现
> - 关键词频次大 ≠ 主题，必须有 user_msg 证据才能写进 bullet
>
> **口味标杆**：参照 `ref/samples/` 里最近的成品的密度和措辞。样本里没有的细节类型，本次也别出现。
>
> **输出**：只返回 裸文本标题 + bullet 列表。**不要任何结尾寄语**（不写"你自己再调一调"之类），不要解释，不要 commentary。

子 agent 返回后，主 agent **唯一允许的二次加工**：逐行扫一遍，(a) 把标题行 / `cc 日记` 节标题行开头残留的 `#` / `##` / `###` 删掉（裸文本铁律兜底——子 agent 偶尔会无视铁律带 `#`，且旧样本可能污染口味校准）；(b) 删掉任何残留的 `你自己再调一调` 寄语行（旧样本会污染，子 agent 可能照抄）。除此之外不做任何改写。

### Step 5 — upsert 进单文件 + 报告

**全部日报都进同一个文件** `~/Desktop/archives/每日复盘.md`（按日分节、最新在最下、`---` 分隔）。不要自己手拼整文件——把清理好的**单天 section**（首行裸文本标题 + bullet，含偶数日的 cc 日记）丢给 `ref/upsert.py`，它确定性地做"同标题覆盖 / 否则插入 → 按日期升序排 → 22 天保鲜 → 回写"：

```bash
SECTION_FILE=$(mktemp)
cat > "$SECTION_FILE" <<'EOF'
<这里粘 Step 4 清理好的单天 section：首行 YY.M.D-星期，其后 bullet>
EOF
python3 /Users/lengmo/.claude/skills/daily-recap/ref/upsert.py \
  /Users/lengmo/Desktop/archives/每日复盘.md < "$SECTION_FILE"
rm -f "$SECTION_FILE"
```

- section 内容**不含** `---` 分隔线、**不含**任何 `你自己再调一调` 寄语（见"结尾"铁律）——分隔线由脚本统一加
- 同一天再跑 → upsert 按同标题覆盖那一节，**不动别天**
- backfill 多天 → 从旧到新逐天各调一次 upsert（脚本幂等，保鲜每次内置）

写完后在**聊天里**把这次生成/补写的 section 贴给用户。一次补了多天就点明补了哪几天。**不加任何收尾寄语**（不说"你自己再调一调"）。

**不要**问"要不要展开 X"、"要不要补 Y"。用户看到会直接提修改要求或自己去文件里改。

**样本另算**：`ref/samples/` 是口味校准用的成品库，**只有用户手调过的最终版才算数**。如果用户回了改稿（或说"OK"），轻轻提一句"调好后可以把最终版存到 `ref/samples/$TARGET_DATE-{星期}.md`"，**不要主动替用户存样本**（你猜的版本不算样本）——这跟上面自动 upsert 日报本体不冲突：日报本体自动存，样本永远手动。

### Step 6 — 保鲜（22 天，已内置在 upsert）

不再是单独一步——`ref/upsert.py` 每次回写时都内置 22 天保鲜：丢掉**起始日 < 文件里最新 section 起始日 − 21 天**的 section。

- 锚点永远取文件里最新的 section（不是当前正在写的那天），所以 backfill 逐天 upsert 也不会误删较新的天
- 幂等：没有超窗的天就什么都不丢，可安全重复跑
- 旧 section 直接从文件移除（内容随时可由 jsonl 重新生成，不是不可逆删除；单文件内不再走废纸篓）

## 双数日 cc 日记（附加章节）

`TARGET_DATE` 的日（DD）为**偶数**（2/4/.../30）→ 在主复盘 bullet 之后追加一段"cc 日记"，回顾近 2 天 cc 配置变化。**奇数日跳过**。

```bash
DAY=$(date -j -f "%Y-%m-%d" "$TARGET_DATE" "+%d")
[ "$((10#$DAY % 2))" -eq 0 ] && RUN_DIARY=1
```

回顾 4 个维度（窗口：`TARGET_DATE - 2 天 06:00 ~ 现在`）：

```bash
ANCHOR=$(date -j -v-2d -f "%Y-%m-%d" "$TARGET_DATE" "+%Y-%m-%d")
find ~/.claude/skills        -name "SKILL.md" -newermt "$ANCHOR 06:00:00" 2>/dev/null
find ~/.claude/agents        -name "*.md"     -newermt "$ANCHOR 06:00:00" 2>/dev/null
find ~/.claude/projects/-Users-lengmo/memory -name "*.md" -newermt "$ANCHOR 06:00:00" 2>/dev/null
stat -f "%Sm %N" -t "%Y-%m-%d %H:%M" ~/.claude/settings.json ~/.claude/settings.local.json 2>/dev/null
```

输出格式（**节标题裸文本，不带 `##` 前缀**）：

```
cc 日记（近 2 天）

- skills：新增 `<name1>`、`<name2>`；改动 `<name3>`（一句话方向）
- agents：新增/改动 `<agent-name>`
- memory：删 `<feedback_xxx>` × N、加 `<feedback_yyy>` × M（方向）
- hooks：settings.json 加了 `<HookEvent>:<command>` / 无改动
```

规则：
- 每条 bullet **数量化 + 命名**（"加了 2 个 skill：daily-recap、meta-check-skill"），不写"加了一些"
- 某维度无改动 → 该 bullet 直接跳过
- 4 维全无改动 → 单列一行 "近 2 天 cc 配置无变化"
- 不写 daily-recap 自己的小修小补（主 bullet 已经看过）

## 反模式（踩过的坑）

1. **用户记错 session** —— 用户说"这个 session 改了 16 个走查"但 jsonl 没 `走查` → 按用户说的写，结尾单列疑点行让用户决定。
2. **Session 因 context reset 分段** —— jsonl 里多次出现 `This session is being continued from`，前后做的事常常不同，子 agent 看 user_msg 时要通读不能只看头。
3. **关键词频次 ≠ 主题** —— `runner` 几百次多半是 `~/.agentboard/hook-runner.js` 噪声；`Gitea` 高频可能只是日常 push；`commit-cr` 出现可能只是 `ls` 出 skills 目录。**任何因关键词频次推出的主题，必须 grep 实际上下文核证**。
4. **粒度过细** —— "分析组件链 + 建 V2 空壳 + 注册 AB topic + 写分析文档" 4 件小事合一句"X 改版摸底"。一条 bullet 抵四条。
5. **替用户存样本** —— `ref/samples/` 里用户手调的最终版才有效，你猜的版本不算，只提示不动手。（注意区分：日报本体 `~/Desktop/archives/每日复盘.md` 是 Step 5 自动 upsert 的；不动手只针对 `ref/samples/`。）
