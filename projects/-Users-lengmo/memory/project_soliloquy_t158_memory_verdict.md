---
name: soliloquy-t158-memory-verdict
description: T158 图谱记忆验证已收官——图谱不立项，结论/工单/回归跑法文档全在 eval-arena，不在 soliloquy 仓
metadata: 
  node_type: memory
  type: project
  originSessionId: 90b825fa-b591-49f2-b37d-1d0de4e653ad
  modified: 2026-09-21T09:00:00.000Z
---

T158（soliloquy 图谱记忆验证）2026-08-02 收官。裁定：**图谱记忆不立项**（两种检索下 vs 平铺均无增益，p=1.0；失分主锅在检索层，全库直塞 62.5% vs 检索组 15% 坐实）。现状链路基线 **68/160**，库内上限 124。

文档单一真相 **2026-09-10 已从本机迁到 owner 的 Linux 服务器** `/home/lab/.local/share/eval-arena/soliloquy-t158`（293 文件、逐文件 SHA-256 核过；本机回执 `~/.local/share/eval-arena-cleanup/20260910-t158-migration/receipt.json`，服务器回执 `/home/lab/.local/share/eval-arena/migration-receipts/soliloquy-t158-20260910.json`；本机目录 `eval-arena/data/soliloquy-t158/` 与废纸篓副本都没了，别在本机找；09-21 只凭本机回执核，未 ssh 上去看）（[[project_co_model_eval_arena]] 同仓）：最终报告 / 结论-检索层封顶 / **产品侧工单-记忆修复三件**（soliloquy 真仓行号，owner 未拍修不修）/ 回归跑法（263 题冻结考卷可随时重考，一次≈$0.25）。soliloquy 仓全程零改动。

这把尺子仍在被用（09-21 核）：eval-arena `docs/prd/10-记忆KV事实臂对比-T158尺子重跑.md`（未开始，引基线 68/160、库内上限 124）、`docs/plans/2026-09-14-T158留出题-防修复环刷分.md`；「图谱不立项」裁定未被推翻。

owner 拍板：§11 销毁条款**豁免不删**（含 crushon 真实聊天派生物，本机留存不在意）。crushon 原始导出 55 份在 `eval-arena/research-assets/crushon-real-chats/`。

回归三戒律：不许照题面优化检索（尺子作废）；只测「记得住」不测「聊得好」；答题模型参数（deepseek-v4-pro/t=0/StreamLake）一格不动否则不可比。
