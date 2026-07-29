export const meta = {
  name: 'pr-audit',
  description: 'PR 审查引擎(可选 代码评审/质量体检)：对一组改动并行扇出多路评审 → 逐条独立对抗验证 → 汇总 P0/P1/P2。非阻塞，建 PR 后后台跑。',
  // phases 与代码里 agent() 的 opts.phase 分组名一一对应（两条 track 并发跑，
  // 不用全局 phase() —— 它有竞态；见 Workflow 文档对 parallel 内 phase 的警告）
  phases: [
    { title: '代码评审' },
    { title: '验证:代码评审' },
    { title: '质量体检' },
    { title: '验证:质量体检' },
  ],
}

// ===== 配置：cmm-pr fire 前会把这几行 Edit 成当前值 =====
const REPO_DEFAULT = '/Users/lengmo/Desktop/my-code/mk'   // 要审的仓库绝对路径
const SCOPE_DEFAULT = 'uncommitted'                 // 'uncommitted'=审未提交改动 | ref(如'HEAD~1'/'develop')=审 ref...HEAD
const RUN_CR = true                                // 代码评审(commit-cr 引擎)
const RUN_WQA = false                              // 质量体检(web-quality-audit)——仅对网页代码有意义
// =======================================================

// 保险丝：args 里带绝对路径/审查基准时以 args 为准，防止按名发射时吃到上次残留的写死配置
// （2026-07-29 教训：残留 mk 配置烧掉 139 万 token 审错仓）
const argsText = typeof args === 'string' ? args : ''
const argsRepo = (argsText.match(/\/Users\/[^\s（），。;；()]+/) || [])[0] || null
const argsScope = (argsText.match(/\b(origin\/[\w./-]+|develop|main|master|HEAD~\d+)\b/) || [])[0] || null
const REPO = argsRepo || REPO_DEFAULT
const SCOPE = argsRepo ? (argsScope || 'uncommitted') : SCOPE_DEFAULT
if (argsRepo && argsRepo !== REPO_DEFAULT) log(`args 覆盖写死配置：REPO=${REPO} SCOPE=${SCOPE}`)

const HOWTO = SCOPE === 'uncommitted'
  ? `已追踪改动跑 \`git -C ${REPO} diff HEAD\`；新增(未追踪)文件用 \`git -C ${REPO} ls-files --others --exclude-standard\` 列出后逐个 Read 全文。`
  : `跑 \`git -C ${REPO} diff ${SCOPE}...HEAD\` 拿到本分支相对 ${SCOPE} 的全部改动。`

const FINDINGS = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          title: { type: 'string' },
          location: { type: 'string' },
          evidence: { type: 'string' },
          severity: { type: 'string', enum: ['P0', 'P1', 'P2'] },
          lens: { type: 'string' },
        },
        required: ['title', 'location', 'evidence', 'severity'],
      },
    },
  },
  required: ['findings'],
}

const VERDICT = {
  type: 'object',
  properties: {
    real: { type: 'boolean' },
    finalSeverity: { type: 'string', enum: ['P0', 'P1', 'P2', '0'] },
    why: { type: 'string' },
    keyEvidence: { type: 'string' },
  },
  required: ['real', 'finalSeverity', 'why'],
}

// 代码评审三路（commit-cr 引擎）
const CODE_LENSES = [
  { key: '业务正确性', type: 'Explore', focus: `错误/异常处理、边界与空值、并发/竞态、资源释放、API/契约一致；状态作用域维度是否匹配；复用函数的副作用边界。` },
  { key: '代码卫生', type: 'Explore', focus: `debug/print 残留、注释掉的死代码、未用 import/变量、命名一致性、同文件多次改的遗留。` },
  { key: '盲区扫描', type: 'general-purpose', focus: `自定方向。安全、性能、跨文件影响、变更层级合理性(业务问题被下推到基础模块)。` },
]

// 质量体检四类（web-quality-audit 静态版，只针对网页代码 html/jsx/tsx/css）
const QUALITY_LENSES = [
  { key: '性能', type: 'Explore', focus: `Core Web Vitals 代码隐患：img/video 未设尺寸(CLS)、@import、字体缺 font-display: swap、未懒加载下方内容、第三方域缺 preconnect、LCP 资源缺 preload。` },
  { key: '无障碍', type: 'Explore', focus: `a11y：img 缺有意义 alt、表单控件缺 label、<html> 缺 lang、ARIA 误用/可用原生却没用、交互元素缺可访问名、缺 focus 可见态、仅靠颜色传达信息。` },
  { key: 'SEO', type: 'general-purpose', focus: `title 缺失/重复/超长、缺 meta description、heading 层级(多个 h1)、缺 canonical、缺结构化数据(JSON-LD)、"click here" 式链接文案。` },
  { key: '最佳实践', type: 'general-purpose', focus: `混合内容/非 HTTPS 资源、废弃 API(document.write/同步 XHR)、生产暴露 source map、缺 charset、可预见的 console 报错/CORS。` },
]

// 通用：一组 lens → 扇出评审 → 去重 → 逐条对抗 → 分级
async function runReview(lenses, track) {
  const reviews = await parallel(lenses.map((l) => () =>
    agent(
      `你是资深评审，只负责「${l.key}」这一路。仓库：${REPO}\n` +
      `审查范围：${HOWTO}\n` +
      `关注点：${l.focus}\n` +
      `每条结论必须附 file:line，亲自读过那一行。不输出 +/- diff。无问题就返回空 findings。`,
      { agentType: l.type, schema: FINDINGS, phase: track, label: `${track}:${l.key}` },
    ),
  ))
  const seen = new Set()
  const findings = reviews.filter(Boolean).flatMap((r) => r.findings).filter((f) => {
    const k = `${f.location}|${f.title}`
    if (seen.has(k)) return false
    seen.add(k)
    return true
  })
  log(`${track}：${findings.length} 条去重后待验证`)
  if (findings.length === 0) return { reviewed: 0, confirmed: 0, falsePositives: 0, P0: [], P1: [], P2: [] }

  const verdicts = await parallel(findings.map((f) => () =>
    agent(
      `你是怀疑态度的 Critic，只挑战这一条结论，尽量证伪。亲自打开 ${REPO} 下的 ${f.location} 读那一行，别信摘要。\n` +
      `结论：${f.title}\n位置：${f.location}\n依据：${f.evidence}\n初判：${f.severity}\n` +
      `证伪失败就确认为真。P0=功能bug/数据丢失/严重无障碍, P1=应修, P2=技术债/可选优化。`,
      { agentType: 'general-purpose', schema: VERDICT, phase: `验证:${track}`, label: `verify:${f.location}` },
    ).then((v) => ({ ...f, v })),
  ))
  const confirmed = verdicts.filter(Boolean).filter((x) => x.v.real)
  const byTier = (t) => confirmed.filter((x) => x.v.finalSeverity === t)
    .map((x) => ({ title: x.title, location: x.v.keyEvidence || x.location, why: x.v.why, lens: x.lens }))
  return {
    reviewed: findings.length,
    confirmed: confirmed.length,
    falsePositives: verdicts.filter(Boolean).length - confirmed.length,
    P0: byTier('P0'), P1: byTier('P1'), P2: byTier('P2'),
  }
}

if (!RUN_CR && !RUN_WQA) return { repo: REPO, scope: SCOPE, note: '未选择任何审查项' }

// 两条审查各自独立 → 并行跑（Promise.all），互不卡墙
const [codeReview, qualityAudit] = await Promise.all([
  RUN_CR ? runReview(CODE_LENSES, '代码评审') : Promise.resolve(null),
  RUN_WQA ? runReview(QUALITY_LENSES, '质量体检') : Promise.resolve(null),
])

return { repo: REPO, scope: SCOPE, codeReview, qualityAudit }
