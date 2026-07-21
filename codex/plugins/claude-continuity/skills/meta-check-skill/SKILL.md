---
name: meta-check-skill
description: Skill 质量审计（对齐 2026-04 官方 frontmatter 15 字段表）— 用四步法（加载词典 → 解析 frontmatter+body → 逐项打分 → 生成报告）检测某个 SKILL.md 的质量，按 5 维度满分 100 评分并给修复优先级。触发词："检测 skill"、"审 skill"、"skill 水平"、"skill audit"、"skill 评审"、"skill 打分"、"meta check skill"。输入支持：skill 目录名（如 `daily-recap`）、SKILL.md 绝对路径、或 `--all` 同时扫 `~/.claude/skills/` 和当前 cwd 的 `.claude/skills/`。
---

# Meta-Check Skill

对 `SKILL.md` 做质量审计，输出**可执行的修复建议**（不是只打分）。

## 何时使用

- 用户说"审 skill"、"检测 skill 水平"、"skill 评审"、"meta check"
- 刚写完新 skill 需要 dogfood
- 批量体检 `~/.claude/skills/`

## 五维评分（各 20 分）

| 维度 | 出处 | 检测重点 |
|---|---|---|
| Frontmatter 合规 | `authoring-skills` 的字段清单 | `name` 匹配目录、`description` 长度 80-400、只用官方字段 |
| 触发词质量 | `authoring-skills` + 用户的"窄边界词+换词测试" | 显式列触发词、≥3 种表达变体、负面边界（Do NOT use for X / 归 <other-skill>） |
| 结构完整 | `authoring-skills` 的 Use-When / Steps / Output / Verify | 前置触发场景、分步骤、输出硬约束、反模式段 |
| 简洁外科 | `karpathy-guidelines` 四原则 | 行数 ≤ 500、犹豫词 ≤ 3、硬约束词 ≥ 5、不空壳抽象 |
| 漂移与一致性 | `workflow-claude-skills-agent` 的 drift 思路 | 只用支持字段、引用路径存在、有示例/反模式 |

**等级**：90+ A · 75+ B · 60+ C · <60 D

完整细则见 `ref/rubric.md`（默认不加载到上下文，用户追问"为什么这项扣分"时再 Read）。

## 执行步骤（严格四步法）

### Step 1 — 加载词典
仅当用户要求"改评分权重"或"加一条审计规则"时才 Read `ref/rubric.md`。
默认执行不需要读 —— audit.py 已经把词典内化。

### Step 2 — 解析目标 skill
```bash
python3 "${CLAUDE_SKILL_DIR}/ref/audit.py" <name|path|--all>
# ${CLAUDE_SKILL_DIR} 未设置时退回绝对路径：python3 ~/.claude/skills/meta-check-skill/ref/audit.py
```

- `<name>`：skill 目录名（如 `daily-recap`）→ 先查 `~/.claude/skills/<name>/SKILL.md`，找不到再查 cwd 的 `.claude/skills/<name>/SKILL.md`
- `<path>`：直接给 SKILL.md 的绝对路径（项目内 skill / plugin skill 都行）
- `--all`：同时扫 `~/.claude/skills/*/SKILL.md` 和当前 cwd 的 `.claude/skills/*/SKILL.md`

### Step 3 — 打分
audit.py 内置 5 类 scorer，逐条匹配词典并返回 `(score, issues[])`。
**不要自己手算** —— 跑脚本，拿结果。

### Step 4 — 生成报告

输出**硬约束**：
- **不用表格**（用户偏好，粘贴会乱行）
- 多个 skill 时：先一份排名 bullet list，再逐个展开
- 每条 issue 必须**可执行**（说清"缺什么 → 怎么加"），不要空话
- 结尾给 **Top 3 修复优先级**（高/中/低）
- 让用户自己决定要不要修 —— 不要自动改别的 skill

## 输入消歧

用户只说"审 skill"没指定 → 默认 `--all`，出排名表给用户挑哪个细看。
用户说了名字 → 按名字跑。
用户给路径 → 按路径跑（支持项目内 skill，如 `<project>/.claude/skills/<name>/SKILL.md`）。

## 反模式

1. **给分过松** —— 每个 issue 必须具体到"哪处 / 缺哪段"，不能写"结构不太好"
2. **只罗列不建议修** —— 每个 issue 必须附一条修复动作（加什么词、删哪段、改哪个字段）
3. **自己审自己必须 ≥ 85** —— dogfood 硬要求，否则 skill 本身就站不住
4. **报告里混私货** —— 只用 audit.py 的结果讲话，不要临时发挥加 issue（想加就改 rubric）
5. **审一次就写结论** —— 用户要的是"审哪几个"，别扫完 all 就不给展开

## 已知坑

- audit.py 对**中英混合**的触发词/硬约束词都能识别，但极短 description (< 40 字) 会因为词典命中不到全部扣分 —— 写 description 时刻意堆触发词
- 路径存在性检查只对本地绝对路径生效（`/Users/...`、`~/...`）；相对路径、URL、占位符（`<path>`）会跳过
- frontmatter 解析是简化版 YAML（只认 `key: value` 单行），多行字符串（`description: >`）会丢内容 → 建议 description 用单行
- 官方白名单跟着 2026 spec 走：`name, description, when_to_use, argument-hint, arguments, disable-model-invocation, user-invocable, allowed-tools, model, effort, context, agent, hooks, paths, shell` 共 15 个；任何字段不在表里都按"非官方"扣分
- description 单字段不再死卡 400 字，但 `description + when_to_use` 合计 > 1536 字会被官方 listing 截断

## 自检

写完后跑一次：
```bash
python3 "${CLAUDE_SKILL_DIR}/ref/audit.py" meta-check-skill
```
应得 ≥ 85 才算通过。

## Codex compatibility

Preserve this workflow's intent and evidence rules. Translate Claude-specific tool names to the available Codex tools.
