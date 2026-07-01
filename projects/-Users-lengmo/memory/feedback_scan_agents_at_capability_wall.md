---
name: feedback_scan_agents_at_capability_wall
description: "撞\"需要浏览器/运行时验证\"墙时先扫可用 agent（visual-qa 驱动浏览器），别只盯自己的直接工具"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a7947bde-c46f-4692-9c01-9809ca663921
---

撞到能力墙——尤其"需要浏览器 / 真实渲染 / 运行时观察"——时，**先扫开局的「可用 agent 列表」再说"做不到"**，别只盯自己的直接工具（curl、node_modules 装没装 playwright、Chrome MCP 开没开）。

**Why:** 项目里 `visual-qa` 就是专门驱动浏览器做运行时走查的 agent（PC/mobile×dark/light 四象限截图、Network/Console、对照 Figma）；`mock-data-builder` 造数据态。但它们的 description 按**视觉/设计 QA**关键词写（截图走查/UI改版验收/figma对照）。当需求被我框成"断言 protected 请求数/401""网络层验证""运行时行为"这类**非视觉措辞**时，跟它的描述对不上、pattern 不 match，于是我跨**多个 session** 反复漏掉、反复宣布"需浏览器、自助不了"——用户已明确点名这是复发问题。根因：撞墙时锚在"我有没有浏览器工具"，而不是"有没有浏览器 agent"。

**How to apply:** 任何要输出"这步需要浏览器/运行时验收"结论的当口，先问"有没有 browser-capable agent"→ 是 `visual-qa`（数据态缺先 `mock-data-builder`）。**但关键修正（2026-06-29 实测）：visual-qa 自己也被 `claudeInChromeDefaultEnabled=false` 卡死 —— 它会去检索浏览器工具，会话没带 `claude --chrome` 时它一样起不了浏览器、只能如实喊停。** 所以浏览器 agent **不**绕过 Chrome 开关（这条之前写反了）。正确动作：撞浏览器墙时**一次性把两件事给用户**——(a) visual-qa 是对的执行者，(b) 但**会话要先 `claude --chrome`**，重开后再把任务丢给 visual-qa。别只甩"我做不了"，也别假设 agent 能替你越过 `--chrome`。关联 [[feedback_chrome_extension_on_demand]]（同一把开关，管所有浏览器工具，含 subagent）、[[feedback_agent_value_criterion]]。
