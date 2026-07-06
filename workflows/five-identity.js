export const meta = {
  name: 'five-identity',
  description: 'Stage-aware Boris Cherny five-identity review — routes to the right mix based on product lifecycle stage',
  phases: [
    { title: 'Scout', detail: 'Explore project structure and determine product stage' },
    { title: 'Identities', detail: 'Run stage-appropriate identity mix' },
    { title: 'Verify', detail: 'Adversary challenges each P0 finding' },
    { title: 'Synthesize', detail: 'Judge produces final prioritized verdict' },
  ],
}

// args: { path: string, scope?: string, stage?: 'pre-pmf' | 'growing' | 'mature' }
//
// Boris Cherny's original routing (x.com/bcherny/status/2071379474277613732):
//   pre-pmf  → Prototyper(heavy) + Builder(heavy) + Sweeper(medium)
//   growing  → Builder(medium) + Sweeper(heavy) + Grower(heavy) + Maintainer(light)
//   mature   → Sweeper(medium) + Grower(heavy) + Maintainer(heavy) + Builder(light)
//
// Skill wiring:
//   Scout      → Explore agentType (read-only, no side effects)
//   Prototyper → brainstorm methodology (divergent, tradeoffs, constraints)
//   Builder    → kaka-perspective + improve-codebase-architecture methodology
//   Sweeper    → performance + web-quality-audit methodology
//   Grower     → general-design-review methodology
//   Maintainer → bug-hunter agentType (specialized bug scanner)
//   Verify     → adversary agentType (tries to prove findings wrong)
//   Synthesize → judge agentType (weighs evidence, final verdict)

const projectPath = (args && args.path) || '.'
const scope = (args && args.scope) || 'the entire project'
const stageOverride = (args && args.stage) || null

// ── Phase 1: Scout (Explore) ─────────────────────────────────────────────────
phase('Scout')

const STAGE_SCHEMA = {
  type: 'object',
  properties: {
    techStack: { type: 'string' },
    purpose: { type: 'string' },
    recentChanges: { type: 'string' },
    keyFiles: {
      type: 'array',
      items: {
        type: 'object',
        properties: { path: { type: 'string' }, purpose: { type: 'string' } },
        required: ['path', 'purpose'],
      },
    },
    stage: { type: 'string', enum: ['pre-pmf', 'growing', 'mature'] },
    stageReason: { type: 'string' },
    redFlags: { type: 'string' },
  },
  required: ['techStack', 'purpose', 'recentChanges', 'keyFiles', 'stage', 'stageReason'],
}

const scout = await agent(`
Scout this project for a multi-identity review. Read only, no changes.
Project path: ${projectPath}
Scope: ${scope}
${stageOverride ? 'Stage override from caller: ' + stageOverride + ' — still scout, but set stage to this value.' : ''}

Tasks:
1. Run \`ls -la ${projectPath}\` — identify tech stack and top-level structure
2. Read the most relevant context file: CLAUDE.md > README.md > package.json (pick one)
3. If scope names a specific feature/dir, list those files too
4. Run \`git -C ${projectPath} log --oneline -15\` — understand recent trajectory
5. Identify 5-8 KEY files most relevant to the scope — read brief excerpts from each

Stage signals (ignore if stage override provided):
- pre-pmf: early commits, experiments/reverts, no stable user flows, vague README
- growing: stable user-facing flows, active UX/feature iteration, prod concerns emerging
- mature: stable core, mostly bug fixes + perf + maintenance, incremental feature work

Return all fields. Be concise.
`, { label: 'scout (Explore)', phase: 'Scout', schema: STAGE_SCHEMA, agentType: 'Explore' })

const stage = stageOverride || (scout && scout.stage) || 'growing'
const context = scout
  ? JSON.stringify({
      techStack: scout.techStack,
      purpose: scout.purpose,
      recentChanges: scout.recentChanges,
      keyFiles: scout.keyFiles,
      redFlags: scout.redFlags,
    }, null, 2)
  : 'Scout failed — proceed with best effort.'

log('Stage: ' + stage + (scout ? ' — ' + scout.stageReason : ''))

// ── Stage routing ─────────────────────────────────────────────────────────────
// depth: 'heavy' = 5-7 findings, 'medium' = 3-4, 'light' = 1-2, null = skip
const STAGE_CONFIG = {
  'pre-pmf': {
    Prototyper: 'heavy',
    Builder:    'heavy',
    Sweeper:    'medium',
    Grower:     null,
    Maintainer: null,
  },
  'growing': {
    Prototyper: null,
    Builder:    'medium',
    Sweeper:    'heavy',
    Grower:     'heavy',
    Maintainer: 'light',
  },
  'mature': {
    Prototyper: null,
    Builder:    'light',
    Sweeper:    'medium',
    Grower:     'heavy',
    Maintainer: 'heavy',
  },
}

const DEPTH_COUNTS = { heavy: '5-7', medium: '3-4', light: '1-2' }

// ── Identity definitions (with skill methodology injected) ───────────────────
const ALL_IDENTITIES = [
  {
    name: 'Prototyper',
    emoji: '💡',
    // powered by: brainstorm skill methodology
    lens: `You are the PROTOTYPER identity — powered by brainstorm methodology.

Your mindset: diverge before converging. Clarify intent and constraints first, then generate ideas.

Approach (from brainstorm skill):
- What is the REAL goal behind this feature/project? (not the stated spec)
- What constraints actually exist vs assumed constraints?
- Generate 2-3 distinct approaches to each opportunity — with their tradeoffs
- Flag which experiments would validate assumptions cheapest/fastest
- Ask: "what would unlock 10x user value here?"

Focus on: missing features, untapped opportunities, places where a fresh angle unlocks value.
Finding types: "opportunity", "improvement".`,
    agentType: null,
  },
  {
    name: 'Builder',
    emoji: '🏗️',
    // powered by: kaka-perspective + improve-codebase-architecture methodology
    lens: `You are the BUILDER identity — powered by kaka-perspective (yangbo frontend architect) and improve-codebase-architecture methodology.

Your mindset: ruthless about what's NOT production-ready, and what will hurt later.

Approach (from kaka-perspective + improve-codebase-architecture):
- Where is coupling too tight? What can't be tested in isolation?
- What abstractions are premature vs what abstractions are missing?
- Is the domain language consistent? (naming drift = concept drift)
- What's half-implemented — works in happy path but not edge cases?
- What architectural decisions will become load-bearing tech debt in 6 months?
- Look for: god components, business logic mixed into UI, missing error boundaries, untyped contracts between layers

Focus on: incomplete implementations, architectural gaps, coupling problems, missing prod requirements.
Finding types: "improvement", "bug".`,
    agentType: null,
  },
  {
    name: 'Sweeper',
    emoji: '🧹',
    // powered by: performance + web-quality-audit methodology
    lens: `You are the SWEEPER identity — powered by performance and web-quality-audit methodology.

Your mindset: every line that doesn't need to exist is a line that shouldn't exist.

Approach (from performance + web-quality-audit skills):
Code quality:
- Dead code, unused imports, variables, feature flags that never flip
- Over-engineered abstractions for single-use logic
- Components that do too much (split or simplify)
- Comments that describe WHAT instead of WHY

Web performance (if applicable):
- LCP blockers: render-blocking resources, unoptimized images, large bundles
- CLS causes: layout shifts from dynamic content, missing size attributes
- INP issues: long tasks on main thread, undeferred heavy handlers
- Bundle analysis: unnecessary deps, duplicate packages, missing code splitting

UI consistency:
- Hardcoded values that should be design tokens
- Inconsistent spacing/color usage across similar components

Focus on: dead code, over-complexity, performance bottlenecks, things to delete or simplify.
Finding types: "cleanup", "improvement".`,
    agentType: null,
  },
  {
    name: 'Grower',
    emoji: '📈',
    // powered by: general-design-review methodology
    lens: `You are the GROWER identity — powered by general-design-review methodology.

Your mindset: does this actually work for real users trying to accomplish real goals?

Approach (from general-design-review skill):
UX friction:
- Where do users get stuck or confused? What's the hardest step in the key flow?
- Is feedback immediate and clear? (loading states, error messages, success signals)
- What's the cognitive load? Can users predict what will happen?

Onboarding & retention:
- Does a new user know what to do first?
- Are there empty states that dead-end instead of guide?
- What would make users come back?

Product-market fit signals:
- Which features are core vs noise?
- What are users asking for that doesn't exist yet?
- Where does the product feel "almost there" but miss?

AI-specific UX (if applicable):
- Are AI capabilities discoverable?
- Is latency handled gracefully?
- Does the AI output feel trustworthy?

Focus on: user friction, confusing flows, missing feedback, onboarding gaps, engagement signals.
Finding types: "improvement", "opportunity".`,
    agentType: null,
  },
  {
    name: 'Maintainer',
    emoji: '🔧',
    // powered by: bug-hunter agentType
    lens: `You are the MAINTAINER identity — running as bug-hunter.

Your job: find real bugs and reliability risks. Not code smells, not opinions — actual bugs.

Hunt for:
- Edge case bugs: off-by-one, null/undefined not handled, race conditions
- Security: unvalidated input, exposed secrets, missing auth checks, XSS/injection vectors
- Error handling gaps at system boundaries (API calls, user input, external services)
- Deprecated dependencies with known CVEs
- Reliability: what fails silently? what corrupts state?
- Doc/code drift: comments or types that lie about what the code actually does

Every finding must point to a specific file and line number.
Finding types: "bug", "risk".`,
    agentType: 'bug-hunter',
  },
]

const activeConfig = STAGE_CONFIG[stage] || STAGE_CONFIG['growing']
const activeIdentities = ALL_IDENTITIES.filter(a => activeConfig[a.name] !== null)

log('Active: ' + activeIdentities.map(a => a.emoji + ' ' + a.name + ' (' + activeConfig[a.name] + ')').join(', '))

// ── Phase 2: Run active identities ───────────────────────────────────────────
phase('Identities')

const FINDINGS_SCHEMA = {
  type: 'object',
  properties: {
    archetype: { type: 'string' },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          title: { type: 'string' },
          description: { type: 'string' },
          type: { type: 'string', enum: ['bug', 'improvement', 'opportunity', 'risk', 'cleanup'] },
          priority: { type: 'string', enum: ['P0', 'P1', 'P2'] },
          files: { type: 'array', items: { type: 'string' } },
          action: { type: 'string' },
        },
        required: ['title', 'description', 'type', 'priority', 'action'],
      },
    },
  },
  required: ['archetype', 'findings'],
}

const identityResults = await parallel(
  activeIdentities.map(a => {
    const depth = activeConfig[a.name]
    const count = DEPTH_COUNTS[depth]
    const opts = {
      label: a.emoji + ' ' + a.name + ' (' + depth + ')',
      phase: 'Identities',
      schema: FINDINGS_SCHEMA,
    }
    if (a.agentType) opts.agentType = a.agentType

    return () => agent(`
${a.lens}

Product stage: ${stage} — your weight in this review is "${depth}".
${depth === 'heavy' ? 'This is the most critical lens for this stage — go deep, read widely.' : ''}
${depth === 'light' ? 'Light pass only — flag the 1-2 most obvious issues from your lens.' : ''}

Project context (from Scout):
${context}

Project path: ${projectPath}
Scope: ${scope}

Instructions:
- Use Bash and Read tools to examine the key files listed in context
- Stay strictly in your lane — apply only your identity's lens
- Reference specific files and line numbers in every finding
- P0 = critical/blocking, P1 = important, P2 = nice-to-have
- Produce ${count} findings
- Set archetype field to "${a.name}"
`, opts)
  })
)

const allFindings = identityResults.filter(Boolean)

// ── Phase 3: Verify P0s (adversary) ──────────────────────────────────────────
phase('Verify')

const p0Findings = allFindings.flatMap(r =>
  (r.findings || [])
    .filter(f => f.priority === 'P0')
    .map(f => Object.assign({}, f, { fromIdentity: r.archetype }))
)

const VERDICT_SCHEMA = {
  type: 'object',
  properties: {
    title: { type: 'string' },
    isReal: { type: 'boolean' },
    reason: { type: 'string' },
  },
  required: ['title', 'isReal', 'reason'],
}

const verdicts = p0Findings.length > 0
  ? await parallel(
      p0Findings.map(f => () => agent(`
You are an adversary. Your job is to REFUTE this P0 finding.
Assume isReal=false unless you find definitive proof otherwise.

Finding from ${f.fromIdentity}:
Title: "${f.title}"
Description: ${f.description}
Files: ${(f.files || []).join(', ')}
Proposed action: ${f.action}

Read every referenced file. Challenge the finding:
- Does the code actually have this problem?
- Is it really P0, or is it handled elsewhere?
- Could this be a false positive?

Set isReal=true ONLY if you're fully convinced this is a genuine, critical issue.
`, {
        label: '⚔️ ' + f.title.slice(0, 40),
        phase: 'Verify',
        schema: VERDICT_SCHEMA,
        agentType: 'adversary',
      }))
    )
  : []

const confirmedP0Titles = new Set(
  verdicts.filter(Boolean).filter(v => v.isReal).map(v => v.title)
)
const refutedP0Titles = new Set(
  verdicts.filter(Boolean).filter(v => !v.isReal).map(v => v.title)
)

// ── Phase 3b: P1 抽样复核（防 identity 自评把 critical 误标 P1 永久漏检）──────
// 确定性抽样（每 3 条取 1，~33%；Workflow 禁 Math.random）。抽中的双问：真不真 + 是不是被低估的 P0。
const p1Findings = allFindings.flatMap(r =>
  (r.findings || [])
    .filter(f => f.priority === 'P1')
    .map(f => Object.assign({}, f, { fromIdentity: r.archetype }))
)
const p1Sample = p1Findings.filter((_, i) => i % 3 === 0)

const P1_VERDICT_SCHEMA = {
  type: 'object',
  properties: {
    title: { type: 'string' },
    isReal: { type: 'boolean' },
    shouldBeP0: { type: 'boolean', description: '被低估的 critical？' },
    reason: { type: 'string' },
  },
  required: ['title', 'isReal', 'shouldBeP0', 'reason'],
}

const p1Verdicts = p1Sample.length > 0
  ? await parallel(
      p1Sample.map(f => () => agent(`
You are an adversary doing a spot-check on a P1 finding. Two questions:
1. Is it REAL? (assume false unless the code proves it)
2. Is it actually an UNDERESTIMATED P0? (critical/blocking but the identity self-rated it P1)

Finding from ${f.fromIdentity}:
Title: "${f.title}"
Description: ${f.description}
Files: ${(f.files || []).join(', ')}
Proposed action: ${f.action}

Read every referenced file yourself before answering.
`, {
        label: '🔍P1 ' + f.title.slice(0, 40),
        phase: 'Verify',
        schema: P1_VERDICT_SCHEMA,
        agentType: 'adversary',
      }))
    )
  : []

const escalatedP1Titles = new Set(
  p1Verdicts.filter(Boolean).filter(v => v.isReal && v.shouldBeP0).map(v => v.title)
)
const refutedP1Titles = new Set(
  p1Verdicts.filter(Boolean).filter(v => !v.isReal).map(v => v.title)
)
log(`P1 抽样 ${p1Sample.length}/${p1Findings.length}：升级 ${escalatedP1Titles.size}，驳回 ${refutedP1Titles.size}`)

// ── Phase 4: Synthesize (judge) ───────────────────────────────────────────────
phase('Synthesize')

const skippedIdentities = ALL_IDENTITIES
  .filter(a => activeConfig[a.name] === null)
  .map(a => a.emoji + ' ' + a.name)

const report = await agent(`
You are the judge. Weigh all the evidence and produce the final verdict report.

Project: ${projectPath}
Scope: ${scope}
Product stage: ${stage} — ${scout ? scout.stageReason : ''}

Active identities: ${activeIdentities.map(a => a.name + ' (' + activeConfig[a.name] + ')').join(', ')}
Skipped (not relevant for this stage): ${skippedIdentities.join(', ') || 'none'}

All findings submitted:
${JSON.stringify(allFindings, null, 2)}

Adversary verdicts on P0s:
- Confirmed real P0s: ${JSON.stringify([...confirmedP0Titles])}
- Refuted (downgrade to P1): ${JSON.stringify([...refutedP0Titles])}

P1 spot-check (${p1Sample.length}/${p1Findings.length} sampled):
- Escalate to P0 (underestimated criticals): ${JSON.stringify([...escalatedP1Titles])}
- Refuted P1s (drop or demote to P2): ${JSON.stringify([...refutedP1Titles])}
- Unsampled P1s stay P1 as-is.

Output this markdown report:

# 🧬 Five Identity Review — ${stage.toUpperCase()}
**Project**: [infer from path] · **Scope**: ${scope}
**Stage**: ${stage} · **Active identities**: [emoji + name + weight, comma separated]

---

## 🚨 P0 — Critical (adversary-confirmed)
[Confirmed P0s + escalated P1s from spot-check. Format:]
**[emoji Identity]** · \`type\`
> **[Title]** — [1-sentence description]
> Files: \`path/to/file:line\`
> Action: [concrete next step]

## ⚠️ P1 — Important
[All P1s + downgraded-from-P0s, grouped by identity, same format]

## 💡 P2 — Nice to Have
[Bullet list: • [Identity] [Title] — [action]]

---

## 📊 Summary
| Identity | Weight | P0 | P1 | P2 | Strongest signal |
|----------|--------|----|----|----|----|
[one row per active identity]

**Total**: X findings · P0: X (confirmed) · P1: X · P2: X
**Skipped identities**: ${skippedIdentities.join(', ') || 'none — all ran'}
**Recommended first action**: [single highest-leverage thing to do right now]

Be direct. ≤4 lines per finding. No filler.
`, { label: '⚖️ judge', phase: 'Synthesize', agentType: 'judge' })

return report
