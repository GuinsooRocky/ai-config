export const meta = {
  name: 'web-quality-audit',
  description: '四维 Web 质量运行时审计：性能 / 无障碍 / SEO / 最佳实践 各派一个浏览器 agent 并行跑，对抗验证，出 P0/P1/P2 报告',
  phases: [
    { title: '审计', detail: '性能 / 无障碍 / SEO / 最佳实践 四路 browser agent 并行' },
    { title: '验证', detail: '对每条 finding 独立对抗验证，去掉假阳性' },
    { title: '汇总', detail: '合并去重，按 P0/P1/P2 出修复清单' },
  ],
}

// args = {
//   url:      string   必填，目标页面（如 "http://localhost:3001/world-book" 或线上 URL）
//   scope?:   string   可选，补充说明（如 "首页" / "世界卡列表页"）
//   runA11y?: boolean  可选，默认 true，无障碍审计
//   runSEO?:  boolean  可选，默认 true，SEO 审计
// }

const { url, scope, runA11y = true, runSEO = true } = args

if (!url) throw new Error('缺少必填参数：url')

const pageDesc = scope ? `${url}（${scope}）` : url

const FINDINGS_SCHEMA = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          title:    { type: 'string' },
          location: { type: 'string' },
          evidence: { type: 'string' },
          severity: { type: 'string', enum: ['P0', 'P1', 'P2'] },
          lens:     { type: 'string' },
        },
        required: ['title', 'location', 'evidence', 'severity', 'lens'],
      },
    },
  },
  required: ['findings'],
}

const VERDICT_SCHEMA = {
  type: 'object',
  properties: {
    real:          { type: 'boolean' },
    finalSeverity: { type: 'string', enum: ['P0', 'P1', 'P2', 'skip'] },
    why:           { type: 'string' },
  },
  required: ['real', 'finalSeverity', 'why'],
}

// ─── Phase 1：四路并行审计 ────────────────────────────────────────────────
phase('审计')

const LENSES = [
  {
    key: '性能',
    always: true,
    prompt: `你是 Web 性能审计员。用浏览器打开目标页面，检查以下问题（每条必须有实际证据）：

目标页面：${pageDesc}

## 检查清单（2025/2026 标准）

**Core Web Vitals**
- LCP：最大内容绘制元素是什么？是否已 preload？是否在首屏？
- INP（已替换 FID）：主线程有没有长任务（>50ms）？事件监听器是否被动（passive）？
- CLS：图片/广告/字体是否有显式尺寸？是否存在动态插入导致跳动的元素？

**资源优化**
- 图片：是否使用 WebP/AVIF？是否有 srcset/sizes？下方图片是否 lazy load？未设宽高的 img？
- 字体：font-display: swap？关键字体是否 preload？
- JS：有无阻塞渲染的 <script>（无 defer/async）？有无明显的未使用大包？
- CSS：有无 @import（阻塞）？critical CSS 是否内联？

**加载策略**
- 关键第三方域有无 preconnect？
- LCP 元素资源有无 preload？

打开 console，记录所有 warning/error。
每条 finding 必须有 file:line 或「元素选择器 + URL」作为 location。无证据不报。`,
  },
  {
    key: '无障碍',
    always: runA11y,
    prompt: `你是无障碍审计员。用浏览器打开目标页面，检查 WCAG 2.2 AA 合规性：

目标页面：${pageDesc}

## 检查清单

**可感知（Perceivable）**
- img 的 alt：装饰图用 alt=""，内容图有有意义的描述（不是 "image" / 文件名）
- 颜色对比度：正文 ≥4.5:1，大文字 ≥3:1（视觉检查 or 取 CSS 颜色估算）
- 不仅依赖颜色传达信息（错误状态有图标/文字补充？）

**可操作（Operable）**
- 所有交互元素键盘可达（Tab 顺序合理？）
- 焦点指示器可见（focus 样式不是 outline: none 且无替代方案）
- WCAG 2.2 新增：焦点外观（2.4.11）—— focus ring 最小 2px，与背景对比 ≥3:1

**可理解（Understandable）**
- <html> 有 lang 属性
- 表单控件有关联 <label>（for/id 或 aria-label）
- 错误消息与字段关联

**健壮（Robust）**
- ARIA 角色与实际行为匹配（button 做 button 的事）
- 能用原生元素就不用 ARIA（div role="button" 有无必要？）
- 无重复 id

每条 finding 给出「元素选择器 or file:line」作为 location，severity：P0=完全阻碍使用 / P1=严重影响 / P2=可改进。`,
  },
  {
    key: 'SEO',
    always: runSEO,
    prompt: `你是 SEO 审计员。打开目标页面，检查技术 SEO 和页内 SEO：

目标页面：${pageDesc}

## 检查清单

**页内 SEO**
- <title>：存在？唯一？50-60 字符？含主关键词？
- <meta name="description">：存在？150-160 字符？
- Heading 层级：只有一个 <h1>？h2~h6 合理嵌套？
- 链接文本：有无 "点击这里" / "了解更多" 类无意义文案？

**技术 SEO**
- canonical <link rel="canonical"> 存在且指向正确 URL？
- meta robots / X-Robots-Tag 有无意外 noindex？
- 结构化数据（JSON-LD）：Article / BreadcrumbList / Product / FAQ 等，验证格式
- 图片 alt 也影响图片 SEO

**爬虫友好**
- 关键资源有无被 robots.txt 误封（需查看 /robots.txt）？
- HTTPS？混合内容（http 资源在 https 页）？
- 移动端友好：viewport meta 存在？tap target ≥ 48px？

每条 finding 给出「URL 路径 + 元素位置 or file:line」作为 location。`,
  },
  {
    key: '最佳实践',
    always: true,
    prompt: `你是 Web 最佳实践审计员。打开目标页面，检查安全与现代标准：

目标页面：${pageDesc}

## 检查清单

**安全**
- HTTPS（页面本身 + 所有子资源）
- Content Security Policy 响应头存在？（F12 → Network → Response Headers）
- 无生产环境 source map 暴露（.js.map 文件公开可访问？）
- 无废弃 API：document.write / 同步 XHR / 过期 navigator.platform 等

**现代标准**
- <!DOCTYPE html> 存在
- <meta charset="UTF-8"> 在 <head> 最前面
- 无 Console error / CORS 报错（打开 console 记录）
- 无已知漏洞 JS 库（检查主要依赖版本）

**UX**
- 无侵入式弹窗（页面加载后立即触发的全屏 modal / cookie banner 挡住内容）
- 权限请求（通知 / 地理位置）有上下文解释，不是立即弹

**隐私（2025 新增重点）**
- 有无第三方追踪 cookie（检查 Application → Cookies）
- Permissions-Policy 响应头（限制 camera/microphone/geolocation 等）

每条 finding 给出具体证据（响应头值 / console 截图描述 / 元素路径）。`,
  },
].filter(l => l.always)

const auditResults = await parallel(
  LENSES.map(lens => () =>
    agent(lens.prompt, {
      label: `audit:${lens.key}`,
      phase: '审计',
      schema: FINDINGS_SCHEMA,
    })
  )
)

const allFindings = auditResults
  .filter(Boolean)
  .flatMap(r => r.findings)

log(`审计完成，${allFindings.length} 条 finding，开始对抗验证`)

// ─── Phase 2：逐条对抗验证（去掉假阳性）────────────────────────────────────
phase('验证')

if (allFindings.length === 0) {
  log('无 finding，跳过验证阶段')
}

const verdicts = allFindings.length > 0
  ? await parallel(
      allFindings.map(f => () =>
        agent(
          `你是怀疑态度的 Critic，尽量证伪这条 Web 质量 finding。
打开浏览器自己看一眼 ${url}，亲自验证 location 处的实际情况。

Finding：${f.title}
维度：${f.lens}
位置：${f.location}
证据：${f.evidence}
初判：${f.severity}

证伪失败就确认为真，并给出最终严重度（P0=必须立即修/影响核心功能或安全, P1=应在本迭代修, P2=技术债可规划修）。
如果 finding 在该页面根本不适用（如 SEO finding 对 localhost 无意义），finalSeverity 填 skip。`,
          {
            label: `verify:${f.lens}:${f.location.slice(0, 40)}`,
            phase: '验证',
            schema: VERDICT_SCHEMA,
          }
        ).then(v => ({ ...f, verdict: v }))
      )
    )
  : []

const confirmed = verdicts
  .filter(Boolean)
  .filter(x => x.verdict?.real && x.verdict?.finalSeverity !== 'skip')

log(`验证完成：${confirmed.length}/${allFindings.length} 条确认，${allFindings.length - confirmed.length} 条驳回`)

// ─── Phase 3：汇总 ────────────────────────────────────────────────────────
phase('汇总')

const byTier = t => confirmed
  .filter(x => x.verdict.finalSeverity === t)
  .map(x => `- [${x.lens}] **${x.title}**\n  位置：${x.location}\n  原因：${x.verdict.why}`)
  .join('\n')

const p0 = byTier('P0')
const p1 = byTier('P1')
const p2 = byTier('P2')

const report = [
  `# Web 质量审计报告`,
  `**目标：** ${pageDesc}`,
  `**审计维度：** ${LENSES.map(l => l.key).join(' / ')}`,
  `**结果：** 确认 ${confirmed.length} 条（P0: ${confirmed.filter(x=>x.verdict.finalSeverity==='P0').length} · P1: ${confirmed.filter(x=>x.verdict.finalSeverity==='P1').length} · P2: ${confirmed.filter(x=>x.verdict.finalSeverity==='P2').length}），驳回 ${allFindings.length - confirmed.length} 条假阳性`,
  '',
  p0 ? `## P0 — 必须立即修（${confirmed.filter(x=>x.verdict.finalSeverity==='P0').length} 条）\n${p0}` : '## P0 — 无',
  '',
  p1 ? `## P1 — 本迭代修（${confirmed.filter(x=>x.verdict.finalSeverity==='P1').length} 条）\n${p1}` : '## P1 — 无',
  '',
  p2 ? `## P2 — 规划修（${confirmed.filter(x=>x.verdict.finalSeverity==='P2').length} 条）\n${p2}` : '## P2 — 无',
].join('\n')

return { url, confirmed, falsePositives: allFindings.length - confirmed.length, report }
