export const meta = {
  name: 'daily-recap',
  description: '每日复盘：侦察需补写日期 → 并行摘要各天 → 按序 upsert 进单文件',
  phases: [
    { title: '侦察', detail: '确定目标日期、找 jsonl、过滤无效 session、检测缺口' },
    { title: '摘要', detail: '各天并行：extract.py 抽取 → Sonnet 归并 → 返回 section 草稿' },
    { title: '写档', detail: '从旧到新逐天 upsert 进 ~/Desktop/archives/每日复盘.md' },
  ],
}

const SKILL_REF = '/Users/lengmo/.claude/skills/daily-recap/ref'
const OUTPUT_FILE = '/Users/lengmo/Desktop/archives/每日复盘.md'

// ─── Phase 1: 侦察 ────────────────────────────────────────────────────────
phase('侦察')

const DATES_SCHEMA = {
  type: 'object',
  properties: {
    targetDate: { type: 'string' },
    datesToProcess: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          date: { type: 'string' },          // YYYY-MM-DD（周末取周六）
          title: { type: 'string' },          // 裸文本标题，如 "26.6.30-一"
          isWeekend: { type: 'boolean' },
          sessionPaths: { type: 'array', items: { type: 'string' } },
          alreadyInFile: { type: 'boolean' },
          action: { type: 'string', enum: ['generate', 'skip'] },
        },
        required: ['date', 'title', 'sessionPaths', 'alreadyInFile', 'action'],
      },
    },
  },
  required: ['targetDate', 'datesToProcess'],
}

const scout = await agent(
  `你是复盘侦察员。确定今天要生成/补写哪些日期的日报。

## Step 1 — 确定 TARGET_DATE（06:00 锚点）
\`\`\`bash
if [ "$(date +%H)" -lt 6 ]; then
  TARGET_DATE=$(date -v-1d +%Y-%m-%d)
else
  TARGET_DATE=$(date +%Y-%m-%d)
fi
echo "$TARGET_DATE"
\`\`\`

## Step 2 — 回看 22 天，找有活动的天
\`\`\`bash
for i in $(seq 21 -1 0); do
  D=$(date -j -v-"$i"d -f "%Y-%m-%d" "$TARGET_DATE" "+%Y-%m-%d")
  FILES=$(find /Users/lengmo/.claude/projects/-Users-lengmo -maxdepth 1 -type f -name "*.jsonl" \\
    -newermt "$D 06:00:00" ! -newermt "$(date -j -v+1d -f "%Y-%m-%d" "$D" "+%Y-%m-%d") 06:00:00" 2>/dev/null)
  echo "DATE=$D FILES=$FILES"
done
\`\`\`

对每个有文件的天，进一步过滤（只保留 size>=0.1MB OR 行数>3 的 jsonl）：
\`\`\`bash
ls -la <jsonl_path>  # 看 size
wc -l <jsonl_path>   # 粗估 user_msgs
\`\`\`

## Step 3 — 周末合并
若某天为周六或周日（date +%u → 6/7），把该周六、周日合并为一个条目：
- date 取周六的日期
- title 格式：YY.M.{D1}~{D2}-周末（如 26.6.28~29-周末）
- sessionPaths 合并两天的文件

## Step 4 — 检查哪些 section 已在文件里
\`\`\`bash
grep -qF "<TITLE>" ${OUTPUT_FILE} && echo "exists" || echo "missing"
\`\`\`

## 规则
- 过去日（< TARGET_DATE）：已存在 → action=skip；缺且有活动 → action=generate
- TARGET_DATE 当天：永远 action=generate
- 没活动的天：不列入 datesToProcess

返回结构化数据。`,
  { schema: DATES_SCHEMA, phase: '侦察', label: 'scout' }
)

const toGenerate = scout.datesToProcess.filter(d => d.action === 'generate')
log(`侦察完成：${toGenerate.length} 天需生成，${scout.datesToProcess.filter(d => d.action === 'skip').length} 天跳过`)

if (toGenerate.length === 0) {
  return { message: '所有日报均已是最新', targetDate: scout.targetDate }
}

// ─── Phase 2: 并行摘要 ────────────────────────────────────────────────────
phase('摘要')

const SECTION_SCHEMA = {
  type: 'object',
  properties: {
    title: { type: 'string' },
    section: { type: 'string' },  // 完整 section 文本，不含 --- 分隔线
  },
  required: ['title', 'section'],
}

const sections = await parallel(toGenerate.map(d => () =>
  agent(
    `你是复盘摘要员。为 ${d.title} 生成日报 section。

## 会话文件（过滤后）
${d.sessionPaths.join('\n')}

## 执行顺序

1. 用 extract.py 抽取摘要：
   python3 ${SKILL_REF}/extract.py ${d.sessionPaths.join(' ')}

2. 读口味样本（最近 3-5 个）：
   ls ${SKILL_REF}/samples/ | tail -5
   （按需 Read 对应文件）

3. 用 Sonnet 子 agent（model: claude-sonnet-4-6）归并，prompt 里带入：
   - 所有 session 抽取数据
   - 样本（作为口味标杆）
   - 铁律：裸文本标题不带 #；不加粗不斜体；一模块一句 bullet；不写结尾寄语

4. 二次加工（主 agent 执行）：
   - 删标题行残留的 # / ## / ###
   - 删任何"你自己再调一调"收尾行

${d.date === scout.targetDate ? `
5. 若今天（${d.title}）日期为偶数，追加 cc 日记节：
   find ~/.claude/skills -name "SKILL.md" -newer "$ANCHOR" 2>/dev/null
   find ~/.claude/agents -name "*.md" -newer "$ANCHOR" 2>/dev/null
   find ~/.claude/projects/-Users-lengmo/memory -name "*.md" -newer "$ANCHOR" 2>/dev/null
   节标题裸文本"cc 日记（近 2 天）"，不带 ## 前缀。
` : ''}

## 格式铁律
- 标题第一行：裸文本 YY.M.D-星期（不带 #）
- 正文：纯 - bullet，不用表格、不加粗、不加斜体
- 不写 session ID、大小、时间戳

返回 title 和完整 section（不含 --- 分隔线）。`,
    { schema: SECTION_SCHEMA, phase: '摘要', label: `recap:${d.title}` }
  )
))

const validSections = sections.filter(Boolean)
log(`摘要完成：${validSections.length}/${toGenerate.length} 天生成成功`)

if (validSections.length === 0) {
  return { message: '摘要全部失败', targetDate: scout.targetDate }
}

// ─── Phase 3: 写档 ────────────────────────────────────────────────────────
phase('写档')

const backfilled = validSections.filter(s => s.title !== scout.targetDate)

const upsertResult = await agent(
  `你是写档员。把以下 ${validSections.length} 个日报 section 从旧到新逐个 upsert 进 ${OUTPUT_FILE}。

## Section 清单（按此顺序处理）
${validSections.map(s => `=== ${s.title} ===\n${s.section}`).join('\n\n')}

## 每个 section 的操作
\`\`\`bash
SECTION_FILE=$(mktemp)
cat > "$SECTION_FILE" << 'ENDSECTION'
<title行>
<bullet内容>
ENDSECTION
python3 ${SKILL_REF}/upsert.py ${OUTPUT_FILE} < "$SECTION_FILE"
rm -f "$SECTION_FILE"
\`\`\`

## 完成后
1. 把 ${scout.targetDate} 当天的 section 原文贴出来给用户看
${backfilled.length > 0 ? `2. 一句话点明顺手补写了：${backfilled.map(s => s.title).join('、')}` : ''}
3. 不加任何收尾寄语`,
  { phase: '写档', label: 'upsert' }
)

return {
  targetDate: scout.targetDate,
  generated: validSections.map(s => s.title),
  skipped: scout.datesToProcess.filter(d => d.action === 'skip').map(d => d.title),
  result: upsertResult,
}
