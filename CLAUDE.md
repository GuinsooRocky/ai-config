# Claude 全局工作指南

## Git 偏好

- Git 同步分支用 rebase（详见 memory: feedback_rebase_over_merge.md）

---

## 删除/清理

- 帮删文件一律 `mv` 到 `~/.Trash`，**绝不 `rm`**（即使用户已批准）——保持可逆（详见 memory: feedback_cleanup_use_trash_not_rm.md）

---

## 笔记存放约定

- **触发词**：用户说"存学习笔记"/"记一下"/"保存笔记" → 写到 `/Users/lengmo/Desktop/archives/技术总结/`
- **文件名**：`MM.DD-<简短标题>.md`（例：`04.20-Agent-Loop-四框架设计.md`）
- **写完告知**：报路径 + 提醒"可拖入有道云笔记 技术总结 文件夹"
- **理由**：有道云笔记数据加密封闭，无法自动导入，约定本地暂存后手动拖拽
- **别跟"落档"混**：触发词"落档"= 真实需求落档 → `~/Desktop/cmm/agg/真实需求落档/`（详见 memory: feedback_real_requirement_archive.md）

---

## PRD 路由（说"PRD"先分诊，别赌触发词）

- 审 PRD 本身（矛盾/缺文案/反讲）→ `onlychat-prd-reflection`
- 查代码注释跟 PRD 同没同步（§X.X anchor）→ `cmm-drift-prd`
- 拿方案对照 PRD 逐点拷问 → `/grill-with-prd`（手动）；无 PRD → `grill-me`
- 生码成品验收打分 → 全链路（含造数据+走查）用 `pageforge-accept-pipeline`；报告已齐只打分用 `pageforge-acceptance-judge`
- 裸"对一下 PRD/看下 PRD"意图不明 → 先反问 a审本身 / b查drift / c拷问方案，别乱选

---

## 模型调度与判断（制度文件，2026-07-06 Fable 立法）

- 派子 agent / 选 model / 验收升降级 → 先读 `~/.claude/model-dispatch.md`
- 拿不准"算不算完成 / 该不该问用户 / 该不该换路" → 查 `~/.claude/judgment-rubrics.md`
- 拿不准"某说法/某竞品/某数据是真的吗、该不该先查" → `judgment-rubrics.md` §6（警报词：我记得/应该/一般来说 = 该查的信号）
- 派工 prompt 直接套 `~/.claude/delegation-templates.md` 的模板（T1 搜索 / T2 实作 / T3 重构 / T4 研究 / T5 审查）
- 改以上制度文件前，先读 `~/.claude/harness-maintenance.md` 的权限分层

---

## 写码行为守则（源自 Karpathy Coding Guidelines，2026-07-06 Fable 精修）

> 原 80 行英文版精修至此；删掉的条款已被制度文件接管，去向见 commit 说明。整体偏保守：琐碎小活自行放宽。

**动手前**
- 摆明假设再动手；有多种理解时带 1 个推荐直接走，只有不可逆的分叉才停下问（"该不该问"的细则 → `judgment-rubrics.md`）
- 有更简单的做法要说出来；值得顶回时就顶回

**写多少**
- 只写解决问题的最小代码：不加没要的功能、单用途的抽象、没人要的"灵活性"、不可能场景的错误处理
- 200 行能写成 50 行就重写

**动哪里**
- 只动任务要求动的：不顺手"改进"旁边的代码/注释/格式，不重构没坏的东西，风格跟现有代码走
- 看到无关的死代码：提一句，不删；自己改动产生的孤儿（没人用的 import/变量/函数）要清干净
- 检验：每一行改动都能追溯到用户的原始请求

**怎么算完**
- 把任务翻译成可验证的目标（"修 bug" → 先写能复现的测试，再修到绿）；多步任务列简短计划，每步配一个 verify
- "算不算真完成"的判据 → `judgment-rubrics.md`；派工的验收条件怎么写 → `model-dispatch.md` §3

@RTK.md
