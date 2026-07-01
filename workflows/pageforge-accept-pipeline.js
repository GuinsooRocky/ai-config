export const meta = {
  name: 'pageforge-accept-pipeline',
  description: 'pageforge 生码验收三步全自动：mock-data-builder 造数据 → visual-qa 四象限走查（免确认）→ pageforge-acceptance-judge 打 100 分',
  phases: [
    { title: '造数据', detail: 'mock-data-builder 按 PRD 推断数据态，构造多条/单条/空态' },
    { title: '四象限走查', detail: 'visual-qa PC/mobile × dark/light 全覆盖，跳过 Phase 1 确认' },
    { title: '验收打分', detail: 'pageforge-acceptance-judge 四维各 25 分，出缺口清单' },
  ],
}

// args = {
//   card:     string   必填，卡名（如"世界卡创建"）
//   prdPath:  string   必填，PRD 路径（如"~/Desktop/archives/世界卡PRD.md"）
//   devUrl:   string   必填，dev 地址（如"http://localhost:3001/world-book/create"）
//   codePath: string?  可选，生码产物目录（缺省时让 judge 自行定位）
//   figmaUrl: string?  可选，Figma 链接（缺省时降级为异常检查模式）
// }

const { card, prdPath, devUrl, codePath, figmaUrl } = args

if (!card || !prdPath || !devUrl) {
  throw new Error('缺少必填参数：card / prdPath / devUrl')
}

const codeScope = codePath
  ? `产物目录：${codePath}`
  : `卡名「${card}」，请自行在 ~/Desktop/cmm/onlychat/src 下定位生码文件`

const figmaLine = figmaUrl
  ? `Figma 映射：${figmaUrl}`
  : 'Figma：无映射 → ② 维降级为 visual-qa 异常检查结果换算，报告注明降级模式'

// ─── Phase 1：造数据 ───────────────────────────────────────────────────────
phase('造数据')

const dataReport = await agent(
  `你是数据态构造师（mock-data-builder 角色）。

## 任务
为 pageforge 生码验收构造必要的数据态，让 visual-qa 能覆盖所有可见状态。

## 参数
- 目标卡：${card}
- 页面地址：${devUrl}
- PRD 路径：${prdPath}（读它了解该页面有哪些数据态）

## 执行顺序
1. 读 PRD 提取「数据态清单」（通常含：列表多条 ≥3 条 / 列表单条 / 空态 / 超长内容截断，按 PRD 实际判断）
2. 探测项目可用手段：tRPC 可写接口 > TS 类型 mock > 响应回放
3. 按策略阶梯构造每个态，带 [mock-test] 前缀标记
4. 构造不出的态标「未覆盖 + 原因」，绝不硬凑

## 白名单
只操作 localhost / 127.0.0.1（${devUrl} 已在白名单）

## 输出
数据态就绪报告（含：就绪清单 / 每态的入口 URL or 操作路径 / 未覆盖清单 / 待清理清单）`,
  { agentType: 'mock-data-builder', phase: '造数据', label: 'mock-data' }
)

log('数据态构造完成，进入走查')

// ─── Phase 2：四象限走查 ───────────────────────────────────────────────────
phase('四象限走查')

const qaReport = await agent(
  `你是 UI 四象限走查员（visual-qa 角色）。

## 参数
- 页面：${devUrl}（${card}）
- 走查范围：${card} 完整页面
- ${figmaLine}

## 数据态就绪报告（mock-data-builder 产出）
${dataReport}

## 关键指令：免确认直接走
跳过 Phase 1 状态清单确认，直接按就绪报告里的入口开始走查。
未覆盖态（就绪报告里标「未覆盖」的）标 ⬜ 跳过，写明原因。

## 走查矩阵
就绪报告里每个「就绪」态 × 4 象限：
- PC 1440×900 · light
- PC 1440×900 · dark
- mobile 390×844 · light
- mobile 390×844 · dark

onlychat 主题切换：localStorage.setItem('color-schema', 'dark' 或 'light') 后刷新页面。

## Browser discipline
- 每次开新 tab（tabs_context_mcp），不复用旧 tab ID
- 不触发 alert/confirm/prompt（会卡死会话）
- 同一操作失败 2-3 次就停并报告，不死循环

## 输出
UI 四象限走查报告（markdown，含矩阵总览表 + 差异清单 + 未覆盖清单）`,
  { agentType: 'visual-qa', phase: '四象限走查', label: 'visual-qa' }
)

log('走查完成，进入验收打分')

// ─── Phase 3：验收打分 ─────────────────────────────────────────────────────
phase('验收打分')

const verdict = await agent(
  `你是 pageforge 验收法官（pageforge-acceptance-judge 角色）。

## 输入材料
- 验收卡：${card}
- PRD 原文：${prdPath}（你自己去读）
- ${codeScope}（你自己去读代码）
- ${figmaLine}

## visual-qa 走查报告（运行时证据，唯一来源）
${qaReport}

## 四维各 25 分判据

① PRD 对照（25）
你读 PRD 原文，抽出每条可检验需求 → 逐条判定「已实现 / 走样 / 缺失」
头条永远是 PRD 覆盖率，不许让「能编译 / 能启动」掩盖缺章

② Figma 还原（25）
${figmaUrl ? `有映射 → 调 Figma MCP 取 rgba/hex/px，直接照抄比对，不估算` : '无映射 → 引用走查报告异常检查结果换算，注明降级模式'}

③ 能跑通（25）
引用走查报告矩阵的 ✅/❌/⚠️/⬜ 格 + console 错误 → 按核心流程权重换算分数

④ 逻辑对照（25）
你读代码 vs PRD 行为逻辑：状态管理 / 边界条件 / 数据流，等价实现给满分

## 铁律
- 每条扣分必须附引证（PRD 引句 / Figma 节点值 / 走查报告条目编号 / file:line），无引证一律无效
- 没写 = 真没做；tsc 绿 ≠ 需求完成
- 不开浏览器，不调任何 agent
- 管线外独立验收：不读 agg/eval/.spec.mjs 考卷，一切证据自取`,
  { agentType: 'pageforge-acceptance-judge', phase: '验收打分', label: 'judge' }
)

return { card, dataReport, qaReport, verdict }
