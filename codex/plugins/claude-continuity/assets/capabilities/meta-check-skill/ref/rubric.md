# Meta-Check Skill · 评分词典（Rubric）

满分 **100**，五大维度各 **20 分**。每条细则给出"达标标准 + 检测方法 + 常见扣分"。audit.py 把这份词典内化为代码匹配规则；本文档仅用于：人工 review 评分 / 修改权重时参考。

---

## 1. Frontmatter 合规（20 分）

来源：[官方 Skills 文档 — Frontmatter reference](https://code.claude.com/docs/en/skills#frontmatter-reference)（2026-04 抓取）。

### 官方支持字段白名单（共 15 个）
`name`, `description`, `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `model`, `effort`, `context`, `agent`, `hooks`, `paths`, `shell`

未在此白名单的字段 → 被静默忽略，相当于写了白写。

### 细则
| 项 | 分 | 达标 | 检测 |
|---|---|---|---|
| name 存在 | 2 | `name: xxx` | frontmatter 里有 `name` 键 |
| name 匹配目录 | 3 | `name` == 父目录名 | 字符串相等 |
| description 存在 | 3 | 有 `description:` | frontmatter 里有 `description` 键 |
| description 长度 80-1000 字 | 3 | 去空格后 80-1000 字符 | `len(desc.strip())` |
| description 有"use when"指向 | 2 | 命中 `use when\|何时使用\|触发\|适用`（含 `when_to_use` 字段） | 正则 |
| description 有具体锚点 | 3 | 包含文件名（反引号）或 `触发词:` | `\`[^\`]+\`` 或 `触发词` |
| 无未知字段 | 4 | 字段集合 ⊆ 白名单 | 差集 |
| **合计** | **20** | | |

**额外硬约束**：`description + when_to_use` 合计 > 1536 字 → 会被官方 skill listing 截断，单独 issue。

**常见扣分**：
- description 写成 "Helps with X" —— 过泛无锚点，扣 2 分
- 乱加 `author:` / `version:` / `license:` —— 非官方字段，扣 3 分
- `name: foo` 但目录叫 `foo-skill` —— 不一致，扣 3 分

---

## 2. 触发词质量（20 分）

来源：[官方 Skills 文档 — Skill triggers too often / Skill descriptions are cut short](https://code.claude.com/docs/en/skills#troubleshooting) + 用户的"窄边界词 + 换词测试"原则。

### 细则
| 项 | 分 | 达标 | 检测 |
|---|---|---|---|
| 显式列出触发词 | 8 | body 或 desc 里出现 `触发词:` / `trigger:` / `Trigger words:` | 正则 |
| ≥3 种表达变体 | 8 | description 里引号内短语 ≥ 3 个 unique | `["""'\`]([^\n]{2,30})["""'\`]` |
| 负面边界 | 4 | desc/when_to_use 里有"什么时候不要用/该归谁"的指向 | `不触发\|不归\|不适用\|归 <other-skill>\|do not use\|not for\|instead` 等（只看 desc+when_to_use，body 不算） |

**分级给分**（第二项）：
- 变体 ≥ 3 → 满分 8
- 变体 1-2 → 部分 4 分
- 0 → 0 分

**常见扣分**：
- 只写一个触发词 —— LLM 命中概率低（用户说话总是千奇百怪）
- 全是英文触发词，无中文 —— 中文用户召唤不到
- 全是正式书面语，无口语变体（"帮我 xxx" / "能不能 xxx"）
- 没写负面边界 —— 与邻近 skill 抢触发（如 analyzer vs deep-research：`开放议题研究归 deep-research，给定来源集合的学习归本 skill`）

---

## 3. 结构完整（20 分）

来源：[官方 Skills 文档 — Configure skills](https://code.claude.com/docs/en/skills#configure-skills) 的 "Reference content / Task content" 区分。

### 细则
| 项 | 分 | 达标 | 检测 |
|---|---|---|---|
| 前置触发场景段 | 5 | body 前 500 字内出现 `Use this skill when\|何时使用\|触发\|适用` | 正则 |
| 分步骤 ≥ 3 | 5 | `Step \d\|步骤 \d\|Phase \d\|^\d\.` 出现 ≥ 3 次 | 正则计数 |
| 输出格式/硬约束段 | 5 | 出现 `output\|输出\|硬约束\|格式\|format` | 正则 |
| 验证/反模式段 | 5 | 出现 `verification\|验证\|自检\|反模式\|坑\|example` | 正则 |

**常见扣分**：
- 一整篇散文，没标号步骤 —— LLM 不知道是顺序执行还是挑着做
- 没有输出格式段 —— 执行完不知道怎么呈现
- 没有反模式段 —— 犯错时没有护栏

---

## 4. 简洁外科（20 分）

来源：用户全局 `~/.claude/CLAUDE.md` 中 "Andrej Karpathy Coding Guidelines" 四原则（Think Before / Simplicity First / Surgical Changes / Goal-Driven）+ 官方 "Keep SKILL.md under 500 lines" 提示。

### 细则
| 项 | 分 | 达标 | 检测 |
|---|---|---|---|
| 行数 ≤ 500 | 5 | `wc -l SKILL.md <= 500` | 行计数 |
| 犹豫词 ≤ 3 | 5 | maybe/probably/might/could/可能/或许/大概/将来/TODO 总计 ≤ 3 | 正则计数 |
| 硬约束词 ≥ 5 | 5 | MUST/NEVER/DO NOT/必须/永远不/不要/禁止/一定要 总计 ≥ 5 | 正则计数 |
| 无空壳抽象 | 5 | 不出现 `AbstractFactory\|HelperHelper\|ManagerManager` | 反例正则 |

**硬约束词分级**：
- ≥ 5 → 满分 5
- 2-4 → 部分 3 分（issue: "至少 5 处"）
- 0-1 → 0 分

**常见扣分**：
- 行数 600+ —— 超 500，应拆到 `ref/`（authoring-skills 的 File Structure 段）
- 通篇"可能需要" / "也许应该" —— LLM 不知道到底做不做，执行打折
- 没有一句 MUST / 必须 —— skill 变软建议
- 写 `SkillAuditorFactory`、`BaseCheckerManager` —— 空壳 OOP 污染

---

## 5. 漂移与一致性（20 分）

来源：drift-detection 通用思路 —— frontmatter 字段与官方表对齐、引用路径未被删、有可验证示例。

### 细则
| 项 | 分 | 达标 | 检测 |
|---|---|---|---|
| 只用官方 frontmatter 字段 | 10 | frontmatter 字段集 ⊆ 白名单 | 差集（与第 1 维重复检测，此处加权） |
| 引用路径存在 | 5 | body 中 `/Users/...` 或 `~/...` 路径都在磁盘上 | `os.path.exists()` |
| 有示例/参考输出 | 5 | 出现 `example\|示例\|样例\|reference output\|参考输出\|已知坑` | 正则 |

**路径存在性检查口径**：
- 仅检查以 `/` 或 `~/` 开头、且结尾是明显文件（`.md/.py/.ts/.tsx/.jsonl/.json/.sh/.yaml`）的路径
- 跳过：占位符（`<path>`、`*.ext`）、URL、`/tmp/*`、相对路径

**常见扣分**：
- body 里引用了一个已删掉的文件 —— 误导 LLM 去读空路径
- 没有任何示例 / dogfood 输出 —— 用户不知道这 skill 到底长什么样
- frontmatter 乱加字段（第 1 维也会扣，这里再扣是惩罚"两次不改"）

---

## 等级

| 等级 | 分数 | 含义 |
|---|---|---|
| A | 90-100 | 高质量，可直接用 |
| B | 75-89 | 能用，小瑕疵，建议补几处 |
| C | 60-74 | 能触发但行为不稳，有明显缺口 |
| D | <60 | 返工 |

## 修复优先级规则

audit.py 输出报告末尾应给 Top 3 修复建议。优先级由**该修复带来的分数增益**决定：

- **高**：修一处能补 ≥ 5 分的（如补 description 触发词变体 → +5）
- **中**：3-5 分的
- **低**：≤ 2 分或纯洁癖类

---

## 修改权重

想调整某项分数或加细则：

1. 改本文件对应表
2. 同步改 `ref/audit.py` 对应 scorer
3. 跑 `python3 ref/audit.py meta-check-skill` 重新自检，应仍 ≥ 85
