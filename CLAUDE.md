# Claude 全局工作指南

## 开工三问（接到任何施工方案/任务，第一段输出必须先答；这是义务不是许可）

1. **本项目的目标句是什么？** 读项目 CLAUDE.md 头部「目标」行；找不到目标句 → 先问 owner，不许开工
2. **这件事离目标句隔几步？** 隔两步以上（机制的机制、工具的工具、给闸修闸）必须明说再动
3. **有没有更简单的形态？** 有就说——说了不算越界，这条是对「改动别超边界」类规则的显式豁免

> 2026-08-17 立法。立法理由：/admin 空白页事故（八批迁移 CI 全绿、验收 10/10，owner 亲手打开是空页）+ 整套契约同步机制施工全程无一句「是否过重」的质疑。

---

## Git 偏好

- Git 同步分支用 rebase（详见 memory: feedback_rebase_over_merge.md）

---

## 删除/清理

- 帮删文件一律 `mv` 到 `~/.Trash`，**绝不 `rm`**（即使用户已批准）——保持可逆（详见 memory: feedback_cleanup_use_trash_not_rm.md）

---

## 抓网页分诊（别让 firecrawl 抢中文平台的活）

- 微信/小红书/X/B站/YouTube/播客链接 → `analyzer` skill（走 sf-reader-all，本机浏览器 + 登录态）；**云端抓这些站会吃风控页**
- 英文站单页 → WebFetch 够用
- 整站 URL 清单（`firecrawl map`）/ 整站抓（`crawl`）/ 关键词搜索带正文（`search`）→ `firecrawl` skill
- 官方 init 装的 31 个 firecrawl-* 子 skill 已砍，只留主入口；07-30 曾被重装回来一次，二次清理时连 `~/.agents/.skill-lock.json` 里的条目一起剪了——再冒出来就照这两步再砍

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
- 某个动作会往主对话灌 >200 行"只需要结论"的内容（读大文件/扫日志/长命令输出）→ 别自己干，派子 agent 只收结论（细则 model-dispatch §0/§1）
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

**验多少（默认最小充分集，全量是例外不是默认）**
- **开跑前必答一句**：「这次改动只跑哪几个测试文件够不够判定？」——答得上来就只跑那几个（`vitest run a.test.ts b.test.ts`），答不上来再往上走一档。想全量 → 先把「为什么增量不够」说出口，说不出就是不必要
- 先算改动面 `git diff --name-only`，再选验证动作；报告时说清"这次验的是什么、够不够判定这次改动"
- 纯 CSS / 文案 / 样式 → **跳单测**，直接运行时截图 + 像素取样（全量套件对样式毫无判别力）
- 碰了组件 / 模块 → `vitest run --changed`（未提交改动）或 `vitest run --changed origin/develop`（整分支）；vitest 顺 import 图反算受影响测试，别自己猜文件名，也别手抄一串路径
- **`--changed` ≠ 增量，它会退化成全量**：改到被广泛 import 的文件 / 配置 / base 选错 → 扇出成整库。所以**先干跑看清单再跑**：`npx vitest list --filesOnly --changed [base]`（vitest 4 实测可用，soliloquy 全库 1042 个测试文件做参照）。列出来是几百上千个文件 = 全量回来了 → **别跑**，回到第一条挑显式路径
- **熔断**：已经跑起来才发现测试数是四位数 → 当场 Ctrl-C，别等它绿；跑完了才发现 → 那次结果不算"增量验证"，报告里不许写成增量
- 类型 / 契约面 → 增量 `tsc`（onlychat 的 `typecheck` 已配 tsBuildInfoFile）+ 上一条
- 要证明某个失败是既有的 → `git stash` 后单跑那一个文件对比，别全量跑两遍
- **全量套件只在三种时候跑**：大面积重构收尾 / 依赖框架升级 / 发版前。其余场景想跑全量 → 先说一句为什么最小集不够
- 测试代码也是代码：新写/改动的测试文件先过仓库 lint 再跑（gts ESLint 曾一次拦 38 个 error 的教训）
- 立法理由：soliloquy 447 文件 5166 测试，为一个 CSS 改动全量跑被 owner 判「这个很蠢」；规则原住 memory（抽签召回、背景级）反复失效，2026-08-18 提级到本文件。2026-08-19 复发：以为写了 `--changed` 就是增量，实跑 11893 passed 全量回来了还照报——补上「干跑先看清单 + 四位数熔断」两条

**怎么算完**
- 把任务翻译成可验证的目标（"修 bug" → 先写能复现的测试，再修到绿）；多步任务列简短计划，每步配一个 verify
- "算不算真完成"的判据 → `judgment-rubrics.md`；派工的验收条件怎么写 → `model-dispatch.md` §3

@RTK.md
