export const meta = {
  name: 'xhs-writer',
  description: '小红书 9 宫格帖三路并行生成：同一素材同时跑科普/单点/故事三种角度，去AI味，最后出对比报告让用户选',
  phases: [
    { title: '三路起草', detail: '科普向 / 单点向 / 故事向三个角度并行生成草稿' },
    { title: '去AI味', detail: '对三路草稿并行执行去AI味扫描' },
    { title: '汇总', detail: '输出三路对比报告 + 推荐最优选' },
  ],
}

// args = { material: string, topic?: string }
const { material, topic } = args

if (!material) {
  throw new Error('缺少 material 参数，请传入素材原文')
}

const topicLine = topic ? `\n## 主题方向\n${topic}` : ''

// ─── 禁用词规则，embedded 进每个 agent prompt ───
const FORBIDDEN_RULES = `
## 禁用词（发现即替换，零容忍）
说白了 / 本质上 / 意味着什么 / 换句话说 / 综上所述 / 值得注意 / 总的来说 /
不得不说 / 简而言之 / 毋庸置疑 / 不言而喻 / 显而易见 / 不仅如此 / 与此同时

## 机器腔句式（找到就改）
- "这不仅...还..." → 拆成两句，直接说
- "无论是...还是..." → 直接说更重要那个
- "X 的重要性不言而喻" → 删，直接说 X 带来了什么
- "让我们一起..." → 删，直接进下一步
- "正是这种...使得..." → 拆开说

## 标点规则
- 破折号「——」改逗号或句号
- 句中冒号改逗号（卡片块标签冒号「例：」「⚠️ 坑：」保留）
- 双引号"..."改「」

## 风格要求
- 像跟朋友聊天，不像写报告
- 句子时长时短，大量逗号制造口语停顿感
- 一句话可以自成一段（强调用）
- 有活人感：「我当时就愣住了」优于「我当时很震惊」
- 判断力：敢下结论，有明确好恶，但不居高临下
`.trim()

const ANGLES = [
  {
    key: 'knowledge',
    label: '科普向',
    desc: '把一套知识讲清楚。收藏率高，适合工具/流程/方法论类内容。',
    structure: `
图1 封面：概念钩子大字 + 「学完能做什么」副标 + 一行可信背书小字
图2 概念卡：「X 是什么」用最简单的话说清楚
图3~7 干货卡×5：每张一个核心知识点，badge+标题+正文（2~3句），按「为什么→怎么做→踩过的坑」逻辑推进
图8 规则总结：大字卡，一句话金句归纳
图9 引流：收尾 + 邀评论互动钩子`,
  },
  {
    key: 'single',
    label: '单点向',
    desc: '只讲一个最反直觉的点。XHS 钩子最强，适合有明确反常识洞察的素材。',
    structure: `
图1 封面：反直觉钩子大字（让人觉得「咦？」）+ 副标筛共鸣 + 背书小字
图2 痛点卡：「你可能也有这个问题」，把读者的处境具体化
图3 核心点：这个反直觉的点是什么，用最口语的方式说
图4 为什么卡：背后的原因，可以用类比帮助理解
图5 怎么用卡：具体可执行的 1~2 个动作
图6 反例卡：「没做到这点会怎样」，强化说服力
图7 大字卡：一句金句归纳，整页一句话（.big-card）
图8 扩展：「延伸阅读」或「其他类似坑」，1~2 点
图9 引流：收尾 + 邀评论（「你有没有遇到过...」）`,
  },
  {
    key: 'story',
    label: '故事向',
    desc: '用「我踩了个坑」串起来。人味最足，适合有亲身经历的素材，评论互动最高。',
    structure: `
图1 封面：坑或转折结果大字（先说结局勾人）+ 副标「但我发现了...」 + 背书小字
图2 起因卡：事情怎么开始的，用场景感极强的一句话拉人入戏
图3 经过卡：过程中的关键节点，重点放在「我以为...结果...」的反差
图4 转折卡：大字卡，「然后我发现了一件事」，整页一句话制造悬念
图5 发现卡：核心洞察，这个经历让我明白了什么
图6 收获卡：具体可复用的方法或教训，1~2 点，加 ⚠️ 框标注常见坑
图7 延伸卡：「后来我还发现...」，继续深挖或给出更大的视角
图8 金句卡：大字卡，一句话归纳这个故事的核心
图9 引流：收尾 + 邀评论（「你有没有类似的经历？」）`,
  },
]

// ─── 起草 → 去AI味：按角度独立流水（pipeline，无 barrier）───
// 每路写完立刻去AI味，不等最慢一路；只有最后对比才真正需要三路齐。
// pipeline 把 angle 原样传给第二段，顺带修掉旧版 filter(Boolean) 后下标错位配错角度的 bug。

const polished = await pipeline(
  ANGLES,
  angle =>
    agent(
      `你是小红书内容专家，以卡兹克风格生成一条 XHS 9 宫格图文帖草稿。

## 输入素材
${material}${topicLine}

## 本次角度：${angle.label}
${angle.desc}

## 9 张卡片结构（严格按顺序）
${angle.structure}

${FORBIDDEN_RULES}

## 额外规则
- 封面大字用生活场景/痛点切入，不堆术语（「代码三个月后改不动」优于「架构耦合度过高」）
- 每张卡 2~3 种元素（badge+h2+p 为主）；整帖最多 1~2 张大字卡（.big-card）
- 禁止：eyebrow+h2 双标题；禁止 p1+p2+box 三段同义复读
- 标题 4 条候选，痛点向放第一条标「推荐」
- 正文 hashtag 8~12 个，垂直领域优先（AI/效率工具/个人成长/...）
- 干货 : 引流 ≈ 3:1，最后一图才放互动引导
- 不要写「一篇讲清楚 / 保姆级教程 / 收藏备用 / 直接抄作业」这种流量腔

## 输出格式（纯文字，不出 HTML）

**角度**: ${angle.label}

**标题候选**:
1. [推荐]
2.
3.
4.

**9 张卡片**:
[图1 封面] 大字: | 副标: | 背书小字:
[图2] badge: | 标题: | 正文:
[图3] badge: | 标题: | 正文:
[图4] badge: | 标题: | 正文:
[图5] badge: | 标题: | 正文:
[图6] badge: | 标题: | 正文:
[图7] 大字卡: （一句话）
[图8] badge: | 标题: | 正文:
[图9 引流] 收尾文字: | 互动钩子:

**帖子正文**:
（150~300 字，第一行是标题候选1，口语化，最后附 hashtag）`,
      { label: `draft:${angle.key}`, phase: '三路起草' }
    ),
  (draft, angle) => {
    if (draft == null) return null
    return agent(
      `你是去AI味专家。对以下小红书草稿逐句扫描，把所有机器腔改成人话。

${FORBIDDEN_RULES}

## 任务
1. 找出所有违规词/句式 → 就地替换
2. 检查每张卡片：有没有「凭什么证明 / 常见坑 / 值得关注 / 核心要点」这种模板标签 → 改成「我后来发现 / 真正卡住的是 / 这一步会劝退很多人」这种人话判断
3. 检查标点规则（破折号/句中冒号/双引号）

## 草稿原文（${angle.label}）
${draft}

## 输出
改后全文（保持原格式），每处变动在行尾加 【改】 标注。
最后一行输出：「共改 X 处」`,
      { label: `polish:${angle.key}`, phase: '去AI味' }
    ).then(text => ({ angle, text }))
  }
)

// ─── 汇总对比（真 barrier：确实需要三路齐）───

const validPolished = polished.filter(Boolean)
const sections = validPolished.map((x, i) =>
  `## 草稿 ${String.fromCharCode(65 + i)}（${x.angle.label}）\n${x.text}`
).join('\n\n---\n\n')

const COMPARE_SCHEMA = {
  type: 'object',
  properties: {
    recommended: { type: 'string', description: '推荐的草稿字母，如 A' },
    why: { type: 'string', description: '1-2 段：为什么这路最适合这份素材，结合素材特点' },
    scores: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          route: { type: 'string' },
          angle: { type: 'string' },
          hook: { type: 'string', description: '封面钩子摘要' },
          collectPotential: { type: 'integer', minimum: 1, maximum: 5 },
          commentPotential: { type: 'integer', minimum: 1, maximum: 5 },
        },
        required: ['route', 'angle', 'hook', 'collectPotential', 'commentPotential'],
      },
    },
    report: { type: 'string', description: '面向用户的完整对比报告 markdown（含三份完整草稿全文）' },
  },
  required: ['recommended', 'why', 'scores', 'report'],
}

const compare = await agent(
  `你是小红书内容编辑，帮用户从三路草稿里选出最适合发布的那路。

${sections}

## 要求
- scores：每路给封面钩子摘要 + 收藏潜力/评论互动潜力（1-5 整数）
- why：结合素材特点说，不要泛泛而谈
- report：面向用户的完整 markdown 报告，结构为「三路对比一览表 → 推荐选哪路 → 草稿 A/B/C 完整版全文 → 下一步（用户确认后用 references/xiaohongshu_template.html 生成 HTML 落到 ~/Desktop/archives/小红书/MM.DD-<标题>.html）」`,
  { label: 'assemble', phase: '汇总', schema: COMPARE_SCHEMA }
)

return compare
