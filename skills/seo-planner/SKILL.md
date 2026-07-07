---
name: seo-planner
description: 个人项目 SEO 规划一条龙入口——先对话收集约束（标的项目/市场语言/变现假设/每周投入/现有资产），约束确认后用 Workflow 扇出调研（关键词模式×SERP 现状并行侦察、竞品页面拆解、机会逐条对抗验证），方案判断接地于本地 SEO 知识库（哥飞×英文大牛双路对照，已证伪战术自动枪毙），最后合成带优先级的可落地方案（URL 结构/页面模板/质量线/GEO 专项/待实验项/30-60 天执行日历）回主对话拍板。覆盖编辑型 topic cluster 与数据×模板 pSEO 两种打法。触发词："SEO 规划"、"做 SEO"、"SEO 方案"、"关键词矩阵"、"topic cluster"、"pSEO"、"程序化 SEO"、"批量页面"、"给 XX 项目做 SEO"、"GEO 规划"、"AI 引用"、"被 AI 引用/推荐"、"AI 搜索优化"、"seo-planner"。不用于：已有页面的技术体检（用 web-quality-audit / performance / core-web-vitals）、单页 meta/JSON-LD 落码（临场直接写）、站内文案写作（xhs-writer）。
---

# seo-planner — 个人项目 SEO 规划

架构：**skill 对话收约束 → Workflow 确定性扇出调研 → 方案回主对话拍板 → 存盘**。
工人 agent 全部内联在下方脚本里，不注册独立 agent 文件。

## 知识库接地

方案不是凭空调研，本地已收口一份 SEO 知识库，三条路径按需读：

- **通用真相层**：`~/Desktop/archives/seo/对照与实验/哥飞vs大牛-对照表.md`（哥飞小册 vs 英文大牛双路对照：印证/冲突裁定/单边空白）——**方案合成前必读**；已决裁定不许在方案里翻案
- **实验格式标杆**：`~/Desktop/archives/seo/对照与实验/待实验清单.md`——只学它的格式（每条=可机械判定判据+成本+时点+优先级），内容是 soliloquy 专属，别照抄进其他项目
- **深挖入口**：`~/Desktop/archives/seo/notes/`（28 份大牛博客+播客 notes，按需加载，不必全读）

两条规则：
1. 方案中任何与对照表"证据已决"区冲突的建议＝违规，合成后自查一遍
2. "证据不足以裁"的两路冲突 → 进方案待实验项，不站队

## 何时使用

- 给个人项目（meat-encyclopedia / MK / 新副业）做 SEO 规划：选词、内容矩阵、pSEO 批量页设计
- 决定"起 web 端该做哪些页面才有搜索流量"的时刻
- 已有方案要复核/扩展某条线（可用 resumeFromRunId 只重跑局部）
- **不用于**：已有页面技术体检（web-quality-audit / performance / core-web-vitals）、单页 meta/JSON-LD 落码（临场直接写）、文章成稿（xhs-writer）

## Phase 1 — 约束对话（缺答案不开跑）

一次性问完以下 5 题（适合用 AskUserQuestion，最多补一轮追问），收齐后**复述约束求确认**再进 Phase 2：

1. **标的项目**：meat-encyclopedia / MK / 其他（决定数据源与参考模式族）
2. **目标市场与语言**：英文全球 / 中文 / 日文（决定查询语言与 SERP 地区）
3. **变现假设**：广告 / 导流 app 下载 / affiliate / 先攒流量再说（决定页面类型优先级）
4. **投入与耐心**：每周可投几小时；能接受多久见效（SEO 常态 3-6 个月）
5. **现有资产**：有无已上线域名/网站；无 → 方案自动含"第 0 步基建段"（Next.js + SSG 起站）

用户说"按默认"时的默认包：meat-encyclopedia ｜ 英文全球 ｜ 广告+导流下载 ｜ 每周 4h、可等 3-6 个月 ｜ 无现有站点。

## Phase 2 — 跑调研 Workflow

把下方脚本**原样**传给 Workflow 工具，`args` 按收集到的约束填。

**pattern_families 生成规则**：由你根据标的项目挑 3-5 个模式族（每族一个并行侦察员）。参考：

- meat-encyclopedia：`部位×吃法（"beef shank how to cook"）`、`叫法对照（"<部位英文名> cut"）`、`对比类（"chuck vs brisket"）`、`挑选/价格（"how to choose ..."）`
- MK：`竞品替代（"superwhisper alternative"）`、`场景工具（"best dictation app mac"）`、`技术向（"on-device transcription mac"）`

**args 形状**（JSON 对象直接传，不要字符串化）：

```json
{
  "project": "meat-encyclopedia",
  "project_notes": "RN/Expo 买肉点菜对照 app，23 条牛猪羊部位结构化数据，暂无 web 端",
  "market": "英文/全球",
  "monetization": "广告 + 导流 app 下载",
  "weekly_hours": 4,
  "horizon": "3-6 个月",
  "existing_site": "无，需新建 Next.js web 端",
  "pattern_families": ["部位×吃法", "叫法对照", "对比类 X vs Y", "挑选/价格"]
}
```

**workflow 脚本**：

```js
export const meta = {
  name: 'seo-research',
  description: 'SEO 机会调研：模式侦察 → 竞品拆解 → 对抗验证 → 方案合成',
  phases: [
    { title: 'Research', detail: '关键词模式侦察 + 编辑型选题侦察（并行）' },
    { title: 'Teardown', detail: '竞品页面拆解' },
    { title: 'Verify', detail: '机会逐条对抗验证' },
    { title: 'Synthesize', detail: '合成带优先级方案' },
  ],
}

const C = args
const CTX = `SEO 调研背景：
- 标的项目：${C.project}（${C.project_notes}）
- 目标市场/语言：${C.market}
- 变现假设：${C.monetization}
- 每周可投入：${C.weekly_hours} 小时；可接受见效周期：${C.horizon}
- 现有资产：${C.existing_site}
通用纪律：所有判断必须带 SERP 证据（WebSearch 实查）；不编造搜索量数字，只用可观察信号描述（autocomplete 是否补全、有无 PAA/相关搜索、首页被谁占、什么内容形态在赢）。

已决裁定（SEO 知识库 2026-07-07 收口，方案建议违反下列任一条即无效）：
- schema 对 AI 引用无增益（1885 页 DiD 实验≈0，5 家 AI 系统不读 JSON-LD），只当卫生要求半天上限；FAQ 富结果 Google 已基本停支持
- link velocity/外链"自然节奏"=Google 官方否认的伪概念（Illyes "made-up term"）；外链风险在质量与自然度，不在速度
- GEO=SEO 延伸+一层，同一份产能：ChatGPT 88% 引用先经搜索命中、AIO 引用大头仍在 Google 前 100——排名是 AI 引用的上游
- AI 内容红线=无人工审批关卡的批量生产，不是"是否用 AI"（2026 双核心更新口径）
- llms.txt 已证伪（13.7 万域名 97% 零请求，Google 官方不支持）
- ChatGPT 仅 34.5% query 联网；Instant/Thinking 引用池重叠仅 25.6%——押单一引用池（如只做 Reddit）要打折`

const CAND_SCHEMA = {
  type: 'object', required: ['candidates'],
  properties: { candidates: { type: 'array', items: { type: 'object',
    required: ['pattern', 'mode', 'example_queries', 'demand_evidence', 'competition', 'gap'],
    properties: {
      pattern: { type: 'string', description: '查询模式或 topic' },
      mode: { type: 'string', enum: ['pseo', 'editorial', 'geo'] },
      example_queries: { type: 'array', items: { type: 'string' } },
      demand_evidence: { type: 'string' },
      competition: { type: 'string' },
      gap: { type: 'string', description: '我们能赢的缺口' },
    } } } },
}
const TEARDOWN_SCHEMA = {
  type: 'object', required: ['teardowns'],
  properties: { teardowns: { type: 'array', items: { type: 'object',
    required: ['query', 'winner_url', 'template_notes', 'weakness'],
    properties: { query: { type: 'string' }, winner_url: { type: 'string' },
      template_notes: { type: 'string' }, weakness: { type: 'string' } } } } },
}
const VERDICT_SCHEMA = {
  type: 'object', required: ['keep', 'confidence', 'reason'],
  properties: { keep: { type: 'boolean' }, confidence: { type: 'number' }, reason: { type: 'string' } },
}
const PLAN_SCHEMA = { type: 'object', required: ['plan_md'], properties: { plan_md: { type: 'string', description: '硬性含 GEO 专项段与待实验项章节，缺一不可' } } }

phase('Research')
const scoutTasks = C.pattern_families.map(f => () => agent(
  `${CTX}
你是关键词模式侦察员，只负责【${f}】这一族。任务：
1. 枚举该族的 {变量}×{意图} 查询模式，落到 8-15 条具体查询
2. 用 WebSearch 抽查其中 3-5 条代表查询的真实 SERP：需求存在吗（autocomplete/PAA/相关搜索信号）？首页被谁占（权威大站/UGC/薄内容）？什么内容形态在赢（文章/视频/工具页）？
3. 产出本族 2-5 个候选机会，每个带证据、竞争度、可打的缺口；mode 标 pseo（模板×数据可批量）或 editorial（需人写的单篇/集群）`,
  { label: `scout:${f}`, phase: 'Research', schema: CAND_SCHEMA }))
const editorialTask = () => agent(
  `${CTX}
你是编辑型选题侦察员，不限于模板化模式。找 3-5 个值得做 pillar 页/内容集群的 topic（教程、对比、选购指南类），逐个用 WebSearch 验证需求信号与竞争度，mode 一律标 editorial。`,
  { label: 'scout:editorial', phase: 'Research', schema: CAND_SCHEMA })
const geoTask = () => agent(
  `${CTX}
你是站外引用池侦察员，用 WebSearch 摸清该赛道 AI 引擎常引的站外阵地：有哪些高流量榜单/评测站？Reddit/Quora 有没有活跃的求荐类 thread？有没有行业目录/资源聚合页可申请收录？产出 2-4 个候选机会，每个带证据、竞争度、可打的缺口；mode 一律标 geo。`,
  { label: 'scout:geo', phase: 'Research', schema: CAND_SCHEMA })
const found = await parallel([...scoutTasks, editorialTask, geoTask])
const raw = found.filter(Boolean).flatMap(r => r.candidates)
const seen = new Map()
for (const c of raw) { const k = c.pattern.toLowerCase(); if (!seen.has(k)) seen.set(k, c) }
const candidates = Array.from(seen.values()).slice(0, 14)
log(`侦察完成：原始 ${raw.length} 条，去重后 ${candidates.length} 条进入拆解+验证`)

phase('Teardown')
const topQueries = candidates.slice(0, 6).map(c => c.example_queries[0]).filter(Boolean)
const teardown = await agent(
  `${CTX}
你是竞品拆解员。对这些代表查询逐个用 WebSearch 找到当前第一梯队页面，并 WebFetch 精读其中 1-2 个：${JSON.stringify(topQueries)}
拆解每个：页面模板结构（标题层级/内容模块/字数量级）、schema 标记使用、强在哪、弱点与缺口在哪。`,
  { label: 'teardown', phase: 'Teardown', schema: TEARDOWN_SCHEMA })

phase('Verify')
const judged = await parallel(candidates.map((c, i) => () => agent(
  `${CTX}
候选机会 #${i + 1}：${JSON.stringify(c)}
你是对抗验证员，立场【枪毙它】，用 WebSearch 独立复查，不许直接采信侦察员结论：
1. 需求真实吗——SERP 信号亲自再查一遍
2. 零权重新站打得进吗——首页是否被高权重大站垄断
3. thin content 风险——批量生成后每页有模板外独有价值吗
4. 养得起吗——每周 ${C.weekly_hours}h 投入下这条线能维持吗
5. 对照 CTX 里的已决裁定——候选若依赖已证伪战术（schema 拉 AI 引用/按节奏买链/llms.txt/FAQ 富结果），直接 keep=false，reason 写明"违反已决：xxx"
全部扛住才 keep=true；confidence 0-1；reason 中文一两句。`,
  { label: `verify:${(c.pattern || '').slice(0, 24)}`, phase: 'Verify', schema: VERDICT_SCHEMA })
  .then(v => v ? { ...c, verdict: v } : null)))
const kept = judged.filter(Boolean).filter(x => x.verdict.keep)
const killed = judged.filter(Boolean).filter(x => !x.verdict.keep)
log(`验证完成：存活 ${kept.length} / 枪毙 ${killed.length}`)

phase('Synthesize')
const plan = await agent(
  `${CTX}
存活机会（带验证结论）：${JSON.stringify(kept)}
竞品拆解：${JSON.stringify(teardown)}
已枪毙（不许在方案中复活）：${JSON.stringify(killed.map(k => ({ pattern: k.pattern, reason: k.verdict.reason })))}

你是 SEO 方案合成师，产出可直接执行的 markdown 方案（plan_md），必须包含（第 7、8 条硬性要求，缺一不可）：
1. 机会优先级表（P0/P1/P2，每条带证据等级与预期角色）
2. 站点架构：URL 结构（hub/spoke）、pSEO 模板页字段清单、editorial pillar 页清单、技术基线体检清单（AI 爬虫显式放行——CDN 默认拦是新常态 / initial HTML 不渲染 JS 可读 / 动态路由 canonical / CWV 三阈值 / sitemap+GSC）
3. 质量线硬规则：每页模板外独有价值是什么；低于线宁可合并不发（防 doorway 惩罚）；可引用密度句式（首段 30 字直答、H2 先给可摘录结论、统计/定义/对比/步骤四类句式）；篇幅由目标词 SERP 前排均字数决定不设教条；AI 辅助写作必须有人工审批关卡
4. 30-60 天执行日历——严格对齐每周 ${C.weekly_hours}h，宁可砍范围不画大饼
5. 现有资产为"${C.existing_site}"：若无站点，给第 0 步基建段（Next.js + SSG 起站清单）
6. 衡量方式：上线后看什么信号（GSC 曝光/点击/收录）、何时复盘调向
7. GEO 专项段（硬性）：三轨结构——UGC/社区轨、官方文档轨（高推理模式吃官方页）、第三方背书轨（评测站 profile/目录收录/榜单）；branded 问答 own-your-answers 优先
8. 待实验项章节（硬性，缺了方案不合格）：存疑/冲突/新战术逐条列，每条带可机械判定判据+成本+时点，格式参照待实验清单.md`,
  { label: 'synthesize', phase: 'Synthesize', schema: PLAN_SCHEMA })

return {
  plan_md: plan.plan_md,
  kept_count: kept.length,
  killed: killed.map(k => ({ pattern: k.pattern, reason: k.verdict.reason })),
}
```

## Phase 3 — 呈现与拍板

1. 把 `plan_md` 呈现给用户，**标注证据等级**（实查 SERP 的 vs 推断的），附被枪毙清单及理由
2. 用户要改：小改直接改文本；要重查 → 编辑脚本后用 `resumeFromRunId` 续跑（已完成的侦察走缓存，只重跑改动之后的）
3. 确认后存盘：`~/Desktop/archives/SEO/MM.DD-<项目>-SEO方案.md`
4. 方案的执行（起站、写页面、落码）不归本 skill——回主对话按方案干

## 输出格式（硬约束）

最终交付必须是两样，缺一不可：

1. **主对话方案呈现**：机会优先级表（P0/P1/P2）+ 被枪毙清单及理由 + 证据等级标注——五档：大样本研究/官方文档/作者实测/个人经验/推测；厂商数据（Ahrefs/Semrush 等自家研究）必须标"利益相关"；每个 P0 必须附 example_queries 供用户自行搜索复核
2. **确认后的存盘文件**：`~/Desktop/archives/SEO/MM.DD-<项目>-SEO方案.md` = plan_md 全文 + 约束快照（args JSON）+ 枪毙清单

不要只给结论不给证据；不要在用户确认前存盘。

## 硬规则

- 约束没收齐不许跑 Workflow；跑完没呈现给用户不许存盘
- 每个机会必须带 SERP 证据；查不到证据的标"假设待验证"，不许混进 P0
- 方案规模对齐 weekly_hours，超出投入能力的机会进 P2/backlog，不画大饼
- 方案没有"待实验项"章节不许交付（学≠会）
