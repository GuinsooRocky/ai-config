---
name: soliloquy-verification-audit
description: soliloquy 验证机制（CI 闸 / Engineering Verification / 性能实验室 / 跑批线）空壳审查，2026-10-12 完成，真相在仓内 docs/prd/research/2026-10-12-验证机制审查.md
metadata:
  type: project
---

2026-10-12 用「闸到底验没验到东西」的角度审了 soliloquy 全部验证机制，结论文档落在仓内 `docs/prd/research/2026-10-12-验证机制审查.md`（已登记 docs/README research 索引），37 条问题（P0 4），3 条待拍（Engineering Full cron 停/接、deploy-edge 退役、reply+capacity 四场景撤目录）。

关键事实：main CI 自 09-08 无绿；09-09 起 Actions 账单停摆，10-01～10-09 恢复期 42 次全红无人读；Engineering Full 每天 12/12 unavailable 结构上不可能红；生产发布脚本不引用任何验证裁决。

未收尾：主仓 feature 分支上有一份未提交的 3+10 行修复（perfArtifactPrivacy 放行采集器自按 Escape 键），修后 perf:web completed 0→324 但仍 partial（28 样本缺 INP，V-17）。

**Why:** owner 当时记得「有个比架构高一层的框架放在 CI 上」，回查发现它半年空跑；三条待拍 owner 还没拍。
**How to apply:** 再碰 soliloquy CI / 性能采集 / Engineering Full 时先读那份文档，别重审；待拍没拍前别动 cron 和目录。相关 [[soliloquy-harness-loops]]。
