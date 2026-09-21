---
name: project-geo-audit
description: geo-audit 新项目=给任意站做「可被第三方复核」的 GEO 诊断；单一真相=仓内 docs/PRD.md；消费端采集不能自动化是天花板
metadata:
  type: project
---

2026-09-21 立项。**geo-audit** = 给任意网站产出**能被第三方复核**的 GEO 诊断与复测报告，目标是做成对外服务。

- 仓：`~/Desktop/my-code/geo-audit`，GitHub **private** `GuinsooRocky/geo-audit`
- **单一真相 = 仓内 `docs/PRD.md`**（350 行，含 T0 准入九项 / T1 结构十二项 / 证据库 / 分母状态机 / 验收判据）。桌面那份已移走，别再去桌面找
- 执行方是 **Codex**：整份 PRD 喂进去即可开工
- 0 号客户 = soliloquy 自己（D0=2026-09-14，D+14=2026-09-28），仓只读

**三条别忘的判断**（PRD 里已写死，复述给别人时别说反）：
1. 差异化不是「更会优化」，是**诚实测量** —— 市面 GEO 工具的两大卖点（llms.txt、schema）已被大样本证伪
2. **0 收录 = 0 引用**（Bing 官方：Copilot 与传统搜索共用同一套爬取索引底座）→ 体检第一刀是 T0 一票否决，没过就别做内容
3. **消费端 403 既是护城河也是天花板**：ChatGPT/Perplexity 无头浏览器全吃验证页，采集永远要人；云端 SaaS 竞品同样拿不到登录态

证据库上游在 `~/Desktop/loop_project/soliloquy/docs/growth/research-2026-09-13/`（五路调研），别重新调研。相关：[[project_chuhai_oem_seo]] [[project_soliloquy]]
