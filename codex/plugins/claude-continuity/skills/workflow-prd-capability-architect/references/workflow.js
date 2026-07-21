export const meta = {
  name: 'prd-capability-architect',
  description: 'AI 架构师视角重新设计 PRD 相关能力栈：先并行测绘现状（skills/agents/workflows/数据源/触发词冲突），再用三种架构哲学并行出方案，对抗评审后合成一份可落地蓝图',
  phases: [
    { title: '现状测绘', detail: '4 路并行：skill 清单 / agent+workflow 清单 / PRD 数据源 / 触发词冲突' },
    { title: '架构方案', detail: '3 个架构师各持一种哲学并行出设计：路由派 / 能力分层派 / 最小改动派' },
    { title: '对抗合成', detail: '怀疑派评审三方案 → 合成最终蓝图' },
  ],
}

// args = { skillsDir, workflowsDir, paths: {...} }
const A = args || {}
const SKILLS = A.skillsDir || '/Users/lengmo/.claude/skills'
const WORKFLOWS = A.workflowsDir || '/Users/lengmo/.claude/workflows'

// 真实文件锚点（让 agent 读 ground truth，不要凭空设计）
const ANCHORS = `
## 已知 PRD 相关能力锚点（必须实际打开读，不许靠描述脑补）

### Skills（${SKILLS}/）
- cmm-drift-prd/SKILL.md — PRD vs 注释 vs 代码三方 drift；**依赖代码里手埋的 §X.X anchor 注释**；仅 onlychat；有 scripts/scope-discover.py + 3 个 references
- onlychat-prd-reflection/SKILL.md — PRD 自身反讲（矛盾/缺文案/反直觉）；仅 onlychat；产 HTML
- grill-with-prd/SKILL.md — 对话式拷问「方案 vs PRD」；通用；disable-model-invocation（仅主动触发）；默认落档目录 ~/Desktop/cmm/agg/真实需求落档/
- grill-me/SKILL.md — 通用版拷问（无 PRD），grill-with-prd 的母版
- brainstorm/SKILL.md — 开工前从 0 把想法聊成设计（PRD 上游）
- cmm-go/SKILL.md — 开工编排，按需拉 PRD/Figma；读 features.md
- cmm-pr/SKILL.md — 提交编排，会顺带带上 cmm-drift-prd 的 🟢 改动
- seo-planner/SKILL.md — 【样板】skill 内部用 Workflow 扇出的范式参考

### Agents（agentType）
- pageforge-acceptance-judge — 读 PRD 给生码成品打分（四维 25：PRD对照/Figma还原/能跑通/逻辑对照）；纯阅卷不开浏览器
- eval-harness-engineer — 把模糊判据造成可重复 eval（造 rubric/golden set）
- bug-hunter / adversary / judge — 三件套对抗评审（非 PRD 但是同源方法论）

### Workflows（${WORKFLOWS}/）
- pageforge-accept-pipeline.js — 造数据→visual-qa→acceptance-judge，**内部读 PRD 打分**
- pr-audit.js — 代码 diff 多镜头审计（含质量镜头）
- xhs-writer.js / web-quality-audit.js — 不相关，仅作 workflow 写法参考

### PRD 真相数据源（PRD 内容到底存在哪、怎么取）
- ~/Desktop/cc-memory/onlychat/features.md — onlychat 各 worktree 的 PRD 飞书链接 + PRD范围默认字段（手维护指针，cmm-go 读）
- ~/Desktop/cmm/agg/真实需求落档/MM.DD-*.md — 通用需求拆解/决策落档（grill-with-prd 默认目录）
- ~/Desktop/cmm/*/.pageforge/PRD.md — 生码工程的本地 PRD（markdown，带 §N 章节）
- 飞书 docx — onlychat PRD 单一真相，通过 social-proxy MCP get_document 只读拉取
- onlychat 代码注释里的 §X.X anchor — drift 检测的钉子

### 用户原话痛点（设计必须解决这个，不是另起炉灶）
「至少 5 处用到 PRD：3 个 skill + 1 个项目里的(features.md) + 1 个生码工程里的(pageforge)。很多时候大模型其实不知道怎么选。」
核心痛 = **路由混乱**：用户说「对一下 PRD / 看下 PRD / 扫一遍 PRD」时，多个 skill 触发词重叠，Claude 选错。
`

// ─────────────────────────────────────────────────────────────────────────
// Phase 1：现状测绘（4 路并行，每路读真实文件）
// ─────────────────────────────────────────────────────────────────────────
phase('现状测绘')

const MAP_SCHEMA = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          item:     { type: 'string' },   // 能力/工具/数据源名
          capability: { type: 'string' }, // 它提供的「能力」一句话
          scope:    { type: 'string' },   // 通用 / onlychat / agg / 生码
          layer:    { type: 'string' },   // skill / agent / workflow / 数据源 / 约定
          triggers: { type: 'string' },   // 触发方式/触发词
          evidence: { type: 'string' },   // file:line 或路径
          gapOrRisk:{ type: 'string' },   // 缺口/风险/重叠点
        },
        required: ['item', 'capability', 'scope', 'layer', 'evidence'],
      },
    },
    summary: { type: 'string' },
  },
  required: ['findings', 'summary'],
}

const MAPPERS = [
  {
    key: 'skills',
    label: 'map:skills',
    prompt: `你是能力测绘员。实际打开并读完下列每个 PRD 相关 skill 的 SKILL.md（含 frontmatter description 全文 + 触发词 + 「何时不用」），输出能力矩阵。

重点抽取：cmm-drift-prd / onlychat-prd-reflection / grill-with-prd / grill-me / brainstorm。
每个 skill 必须答清：① 它到底提供什么**能力**（不是它叫什么）② scope（通用还是绑 onlychat）③ 全部触发词原文 ④ 它声明的「不用于」边界。
特别标注：哪些触发词在多个 skill 间**字面重叠或语义重叠**（这是路由混乱的根）。`,
  },
  {
    key: 'agents-workflows',
    label: 'map:agents+workflows',
    prompt: `你是能力测绘员。读下列与 PRD 有关的 agent 定义和 workflow 脚本，输出它们如何使用 PRD。

- ${WORKFLOWS}/pageforge-accept-pipeline.js（看它内部哪一步读 PRD、怎么读、喂给谁）
- pageforge-acceptance-judge / eval-harness-engineer 这两个 agentType 的职责（从本会话已加载的 agent 描述里取，不用再找文件）
- ${WORKFLOWS}/pr-audit.js（它有没有碰 PRD，还是纯代码）

答清：PRD 在「验收/打分」这条线上是怎么被消费的？跟 skill 线（reflection/drift/grill）是不是两套独立体系、有没有断层？`,
  },
  {
    key: 'data-sources',
    label: 'map:数据源',
    prompt: `你是数据测绘员。PRD 的「内容真相」到底存在哪、每处怎么被读取？实际打开看：

- ~/Desktop/cc-memory/onlychat/features.md（PRD 链接指针 + PRD范围默认字段格式）
- ~/Desktop/cmm/agg/真实需求落档/ 下随便读 1-2 个 md（落档结构）
- ~/Desktop/cmm/*/.pageforge/PRD.md（生码本地 PRD 格式，带 §N 章节）
- 飞书 docx（onlychat PRD 单一真相，经 social-proxy MCP get_document 只读）

答清：① 同一份 PRD 在不同环节是从不同地方取的吗（飞书 vs 本地 md vs features.md 指针）② 有没有「同一真相多处副本、容易不同步」的问题 ③ anchor(§X.X 代码注释) 这套钉子机制覆盖到哪、没覆盖到哪。`,
  },
  {
    key: 'collisions',
    label: 'map:触发词冲突',
    prompt: `你是路由冲突分析员。模拟用户真实会说的话，判断当前会撞车的地方。

把这些用户原话逐句走一遍，列出每句**当前会命中哪些 skill / 该命中哪个 / 会不会选错**：
- 「对一下 PRD」 -「看下 PRD」 -「扫一遍 PRD」 -「PRD 更新了过一遍」
- 「把需求过一遍」 -「PRD 反讲」 -「拷问我的方案」 -「这张卡验收一下」
- 「PRD 有没有矛盾」 -「实现跟 PRD 跑偏没」 -「我这方案够不够」

已知事实：onlychat-prd-reflection 触发词含「对一下 PRD/把需求过一遍」；cmm-drift-prd 触发词含「对一下注释和 PRD/扫一遍 PRD」；grill-with-prd 是 disable-model-invocation（只主动触发）。
输出一张「用户话术 → 当前路由结果 → 是否歧义 → 正确归属」的冲突表，并指出**最危险的 3 个撞车点**。`,
  },
]

const maps = await parallel(
  MAPPERS.map(m => () =>
    agent(`${m.prompt}\n\n${ANCHORS}`, {
      label: m.label,
      phase: '现状测绘',
      schema: MAP_SCHEMA,
    })
  )
)

const mapDigest = MAPPERS.map((m, i) => {
  const r = maps[i]
  if (!r) return `### ${m.key}\n（测绘失败）`
  const rows = r.findings.map(f =>
    `- **${f.item}** [${f.layer}/${f.scope}] — ${f.capability}｜触发：${f.triggers || 'n/a'}｜证据：${f.evidence}｜缺口/重叠：${f.gapOrRisk || '—'}`
  ).join('\n')
  return `### ${m.key}\n${r.summary}\n${rows}`
}).join('\n\n')

log(`现状测绘完成，4 张图就绪（${maps.filter(Boolean).length}/4）`)

// ─────────────────────────────────────────────────────────────────────────
// Phase 2：三种架构哲学并行出方案
// ─────────────────────────────────────────────────────────────────────────
phase('架构方案')

const PROPOSAL_SCHEMA = {
  type: 'object',
  properties: {
    philosophy:   { type: 'string' },
    coreIdea:     { type: 'string' },
    targetMap: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          capability: { type: 'string' },          // 能力
          becomes:    { type: 'string' },           // 最终落成什么（skill/agent/workflow/路由表/合并/删除）
          rationale:  { type: 'string' },
        },
        required: ['capability', 'becomes', 'rationale'],
      },
    },
    routingRule:  { type: 'string' },               // 用户说 X → 走 Y 的判定逻辑
    migrationSteps: { type: 'array', items: { type: 'string' } },
    cost:         { type: 'string' },               // 改动量/风险
    keepsWhat:    { type: 'string' },               // 保留了哪些现有资产（防止推倒重来）
  },
  required: ['philosophy', 'coreIdea', 'targetMap', 'routingRule', 'migrationSteps', 'cost'],
}

const ARCHITECTS = [
  {
    key: 'routing',
    label: 'arch:路由派',
    lens: `你是【路由派 AI 架构师】。核心信念：现有能力大体是对的，真正的病是「入口歧义」。
不新增/不合并能力，只加一层**确定性路由**——一张决策表 + 收敛触发词，让 Claude 用 1-2 个判定问题就锁定唯一工具。
重点产出：① 两轴判定（目的轴：PRD自身质检 vs 实现漂移 vs 验收；绑定轴：通用 vs onlychat vs 生码）② 每个 skill 的触发词如何去重/改写以消除撞车 ③ 这张路由表放哪（CLAUDE.md PRD 路由段？还是一个 meta-skill）。`,
  },
  {
    key: 'stack',
    label: 'arch:能力分层派',
    lens: `你是【能力分层派 AI 架构师】。核心信念：skill=人机交互入口 / workflow=并行放大器 / agent=专才角色，三层各归其位。
逐个审视现有 PRD 能力，判断每个**当前层是否错配**：哪些该是 skill 薄入口、底下挂 workflow 扇出（参考 seo-planner 范式）；哪些纯属 agent 角色被误塞进 skill；通用 drift 这个缺口该长成哪一层。
重点产出：一张「能力 → 应处层级 → 现状是否错配 → 怎么搬」表，并说明分层后路由是否自然变清晰。`,
  },
  {
    key: 'minimal',
    label: 'arch:最小改动派',
    lens: `你是【最小改动派 AI 架构师 / Karpathy 信徒】。核心信念：能不动就不动，只修真正在痛的那一处，拒绝为「优雅」推倒重来。
你要主动质疑：用户真的需要重构吗？「路由混乱」是不是加 3 行 CLAUDE.md 提示 + 改 2 个触发词就解决？通用 drift workflow 到底是真缺口还是 YAGNI？
重点产出：① 真痛点排序（哪个最值得修，哪些是伪需求）② 最小干预清单（每条都说清省了什么）③ 明确点名哪些「看起来该做」的事建议**不做**及理由。`,
  },
]

const proposals = await parallel(
  ARCHITECTS.map(a => () =>
    agent(
      `${a.lens}

## 现状测绘结果（Phase 1 四张图，这是你设计的事实基础，不要脱离它臆想）
${mapDigest}

## 设计约束（铁律）
- 必须解决用户原话痛点：路由混乱（说「对一下 PRD」不知道选哪个）
- 不许推倒重来：现有 cmm-drift-prd / reflection / pageforge 线是有效资产，方案要说清**保留什么**
- 必须落到具体：哪个文件改、触发词怎么改、路由判定逻辑写成可执行的 if/then
- 诚实标注改动成本和风险

按 schema 输出你这一派的完整方案。targetMap 要覆盖全部已知 PRD 能力（drift/reflection/grill/grill-me/pageforge-judge/features.md/落档/通用drift缺口）。`,
      { label: a.label, phase: '架构方案', schema: PROPOSAL_SCHEMA }
    )
  )
)

const proposalDigest = ARCHITECTS.map((a, i) => {
  const p = proposals[i]
  if (!p) return `## ${a.key} 派\n（出方案失败）`
  const rows = p.targetMap.map(t => `  - ${t.capability} → **${t.becomes}**（${t.rationale}）`).join('\n')
  return `## ${a.key} 派：${p.coreIdea}
**路由规则**：${p.routingRule}
**目标映射**：
${rows}
**迁移步骤**：${p.migrationSteps.join(' → ')}
**成本**：${p.cost}
**保留**：${p.keepsWhat || '未说明'}`
}).join('\n\n---\n\n')

log(`三派方案就绪（${proposals.filter(Boolean).length}/3），进入对抗评审`)

// ─────────────────────────────────────────────────────────────────────────
// Phase 3：对抗评审 + 合成
// ─────────────────────────────────────────────────────────────────────────
phase('对抗合成')

const critique = await agent(
  `你是怀疑态度的资深架构评审，专治「为重构而重构」。逐个挑战下面三派方案，目标是**戳穿过度设计、暴露未解决的真痛点**。

${proposalDigest}

## 现状事实（核对方案有没有脱离现实）
${mapDigest}

对每一派给出：① 它真能消除路由歧义吗，还是只是换了个壳 ② 最致命的弱点 ③ 哪一条建议是 YAGNI / 过度抽象，该砍。
最后给一句话裁决：哪一派的「骨架」最该作为合成底座，要嫁接另外两派的哪些零件。`,
  { label: 'critic', phase: '对抗合成' }
)

const FINAL_SCHEMA = {
  type: 'object',
  properties: {
    verdict:      { type: 'string' },   // 一句话结论：该怎么配
    routingTable: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          userSays:   { type: 'string' },  // 用户话术
          goesTo:     { type: 'string' },  // 路由到哪
          why:        { type: 'string' },
        },
        required: ['userSays', 'goesTo', 'why'],
      },
    },
    finalLayout: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          capability: { type: 'string' },
          decision:   { type: 'string' },  // 保留原样 / 改触发词 / 合并 / 新建 workflow / 新建路由表 / 不做
          action:     { type: 'string' },  // 具体到文件和改法
          priority:   { type: 'string', enum: ['P0', 'P1', 'P2', '不做'] },
        },
        required: ['capability', 'decision', 'action', 'priority'],
      },
    },
    doNot:        { type: 'array', items: { type: 'string' } },  // 明确不做什么
    quickWin:     { type: 'string' },  // 今天就能落、收益最大的一步
  },
  required: ['verdict', 'routingTable', 'finalLayout', 'doNot', 'quickWin'],
}

const blueprint = await agent(
  `你是首席 AI 架构师，做最终拍板。综合三派方案 + 评审意见，产出一份**用户可直接照做**的 PRD 能力配置蓝图。

## 三派方案
${proposalDigest}

## 对抗评审
${critique}

## 现状测绘
${mapDigest}

## 你的任务
不要复述三派，要做取舍后的**单一蓝图**。要求：
1. routingTable：把用户最可能说的话术（对一下PRD/扫一遍PRD/PRD反讲/拷问方案/验收这张卡/实现跑偏没…）逐句给出唯一去向 + 为什么
2. finalLayout：每个现有 PRD 能力的最终处置（多数应是「保留/微调触发词」，少数新建），带 P0/P1/P2 优先级
3. doNot：明确点名不做的事（防止过度设计）
4. quickWin：今天就能落、一步消除大部分歧义的动作

按 schema 输出。`,
  { label: 'synth', phase: '对抗合成', schema: FINAL_SCHEMA }
)

return { maps: mapDigest, proposals: proposalDigest, critique, blueprint }
