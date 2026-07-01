---
name: feedback_skill_audit_imported_vs_own
description: 审 skill 时低分多是外部导入/内置 skill，别当成自己的来改；自有 skill 才按自有 rubric 修
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 443515de-f588-4ba6-bc19-7d8106d82508
---

跑 `meta-check-skill --all` 后，低分（C/D 档）**绝大多数是外部导入/内置 skill**，不是 lengmo 自己写的。识别信号：① frontmatter 带非官方字段 `license`/`metadata`（= Anthropic web-dev 包，如 best-practices/performance/core-web-vitals/web-quality-audit/architecture-diagram）；② `disable-model-invocation: true`（如 zoom-out，故意只手动调，所以不在可用列表里 ≠ 坏了）；③ 英文 + 不列触发词的社区 skill（diagnose/grill-me/caveman 等）。

**Why:** 它们低分纯粹因为没按 lengmo 的 rubric 风格写（中英混合触发词/负面边界/分步骤），不是质量坏。改它们 = 跟上游分叉，不值当（同 [[reference_rtk_is_third_party]] 第三方教训）。lengmo 亲手写的 skill 全在 A 档（90-100），因为审计标准就是他自己定的。

**How to apply:** 审 skill 报告先把"外部导入 vs 自有"分开；只对自有低分项给修复动作；外部包除非要它更可靠触发（给 description 加一句触发词即可），否则不重写。真 bug 例外要修：多行 `description: >` 会被官方 listing 截断 + 审计误判（video 曾 57→81，拍平单行解决）—— 写 description 一律单行。配合 [[feedback_skill_dogfood_metacheck]] [[feedback_skill_design_pattern]]。
