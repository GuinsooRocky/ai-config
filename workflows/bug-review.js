export const meta = {
  name: 'bug-review',
  description: 'bug-hunter → adversary → judge 三件套一条命令：扫描 → 对抗 → 裁决',
  phases: [
    { title: '扫描', detail: 'bug-hunter 四路并行扫描，产出编号 bug 报告' },
    { title: '对抗', detail: 'adversary 逐条挑战，尝试证伪每个 bug' },
    { title: '裁决', detail: 'judge 综合两份报告，TRUE/FALSE 裁决 + 双方评分' },
  ],
}

// args: string | { repo?: string, scope?: string }
// 例：
//   "HEAD~3..HEAD"
//   { repo: '/Users/lengmo/Desktop/cmm/onlychat', scope: 'develop' }
//   不传则扫当前工作区未提交改动

const isStr = typeof args === 'string'
const repo = (!isStr && args?.repo) ? args.repo : '当前工作目录'
const scope = isStr ? args : (args?.scope ?? '未提交改动（git diff HEAD）')

// ─── Phase 1: bug-hunter ──────────────────────────────────────────────────
phase('扫描')

const bugReport = await agent(
  `你是 Bug 猎手（bug-hunter 角色）。

扫描目标：${repo}
扫描范围：${scope}

按 bug-hunter 规范执行：
1. 读实际改动代码，不依赖 commit message
2. 并行四路子扫描（可用 Explore agent）：
   - API surface：重命名/删除 export、签名变更、async 化
   - 模块解析：ESM/CJS 混用、动态 require、peer dep 缺失
   - 运行时回归：状态 bug、竞态、effect deps、hydration 不匹配
   - 配置/环境：next.config、tsconfig paths、env var 变动
3. 每条结论必须亲自读到 file:line，无引证不进报告
4. 严重度：Low +1 / Medium +5 / Severe +10

输出格式（严格遵守）：
# Bug 猎手报告
**扫描范围:** <范围>
**Bug 总数:** N  |  **总分:** <sum>
## Bug 清单
### #1 — <标题>
- **严重度:** <Low +1 | Medium +5 | Severe +10>
- **位置:** path/file.ts:42
- **证据:** <2-3 行代码引用 + 为什么是 bug>
- **复现:** <一句话>
- **建议修复:** <一句话>

结尾写：报告完成，交给 adversary Agent 进行对抗评审。`,
  { agentType: 'bug-hunter', phase: '扫描', label: 'bug-hunter' }
)

log(`bug-hunter 完成，进入对抗评审`)

// ─── Phase 2: adversary ───────────────────────────────────────────────────
phase('对抗')

const adversaryReport = await agent(
  `你是 adversary（对抗评审员）。

下面是 bug-hunter 的原始报告，逐条挑战，尽量证伪每一条。
亲自打开对应文件读那一行，别信摘要。
证伪失败则确认为真。

## bug-hunter 原始报告
${bugReport}

每条输出格式：
### #N
- **结论:** confirmed real | false positive | partially wrong
- **理由:** <证据或证伪依据>

结尾写：对抗评审完成，交给裁判 Agent。`,
  { agentType: 'adversary', phase: '对抗', label: 'adversary' }
)

log(`adversary 完成，进入裁决`)

// ─── Phase 3: judge ───────────────────────────────────────────────────────
phase('裁决')

const verdict = await agent(
  `你是裁判（judge）。综合下面两份报告，逐条裁决 TRUE/FALSE，并按 +1/-1 对称规则给两个 Agent 打分。

## bug-hunter 报告
${bugReport}

## adversary 对抗评审
${adversaryReport}

输出：
1. 逐条裁决（#1 TRUE/FALSE + 一句理由）
2. 评分统计：bug-hunter 得分 / adversary 得分
3. 需要用户人工确认的 Top 3 bug（如有）`,
  { agentType: 'judge', phase: '裁决', label: 'judge' }
)

return { scope, bugReport, adversaryReport, verdict }
