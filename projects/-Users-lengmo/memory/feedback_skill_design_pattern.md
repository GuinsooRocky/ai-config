---
name: Skill design pattern
description: skill/agent 资产维护守则四节：什么值得建（判据）、怎么写（结构/触发词）、建完必自审（meta-check ≥85）、审计时分清导入vs自有（D 档多是导入；自有是 A/B 混合非全 A）
type: feedback
originSessionId: 290b7bd2-b4fa-4424-a3f9-1e45803de401
modified: 2026-08-26T07:17:46.048Z
---

# Skill/Agent 资产维护守则

## 一、什么值得建（2026-06-12 用户裁定）

agent/skill 的价值 = 基座不知道的东西：用户偏好、项目纪律、真实踩坑、产品边界；**纯语言/框架栈专家增量≈0**（"怎么写 React"基座本来就会），除非后期沉淀出自己的设计风格/写法才值得装。推荐/新建前先过关：装的东西基座知道吗？知道就不建；把"真增量占比 vs 复读占比"拆开报。**"落不落"的裁决权在用户**——新建资产逐个给推荐 + 等点头，绝不批量代落（曾擅自落盘三个 agent 被要求撤销）。判例：#5 选题编辑不落 agent、并进 khazix-writer 产出线（没有大原料要隔离 + 需要用户参与挑卡 = agent 隔离价值用不上）。

## 二、怎么写

- **结构**：CLAUDE.md 做索引目录（IF-ELSE 路由）不放规则正文；SKILL.md < 500 行，细节下沉 references/（每文件单主题 < 200 行）；CLAUDE.md 超 100 行或涉 >3 类主题就启动下沉重构
- **规则写法**：每条 = 粗体断言 + 一句话展开 + 具体数字/阈值；代码示例强制 ❌/✅ 对子；阈值用表格
- **description**：必须有具体触发词（"LCP"、"rebase"），避免抽象词（"优化"、"最佳实践"）——空泛触发词引起 skill 竞争；**一律写单行**（多行 `>` 会被官方 listing 截断 + 审计误判，video 曾 57→81 靠拍平解决）

## 三、建完/大改必自审

新建或多轮大改 skill 后**必须立即跑 `meta-check-skill`**（`python3 ~/.claude/skills/meta-check-skill/ref/audit.py <name>`），≥85 才算交付。多轮编辑尤其危险——改一处忘同步其他处产生 drift（2026-05-15 skill-upstream-diff 3 处 drift 含自相矛盾指令，靠自审在交付前抓出）。审计重点看 Drift 维度（引用路径存在、章节指令一致）。

## 四、审计时分清导入 vs 自有

跑 `--all` 后先把"外部导入 vs 自有"分开：**D 档几乎全是外部导入**（识别信号：frontmatter 带 `license`/`metadata`/`author`；`disable-model-invocation: true` 是故意只手动调≠坏了；英文不列触发词的社区 skill 无法靠字段自动判，要单独确认来源）。导入的低分是没按本机 rubric 写，不是质量坏——**改它 = 跟上游分叉，要处理就整目录移走别编辑**；只对自有低分项给修复动作。

**自有 skill 是 A/B 混合，不是全 A**（2026-08-26 实测修正旧口径）：pages-publish 65 C、codex 64 C 都是自有；另有 7 个自有中文 skill 在 B 档。别拿"低分=导入"当铁律，判归属看字段和语言，不看分数。

相关：[[feedback_research_must_writeback]]（新能力优先长在现有 skill 上）。
