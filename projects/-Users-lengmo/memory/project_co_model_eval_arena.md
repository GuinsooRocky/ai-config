---
name: co-model-eval-arena
description: anna=多轮RP聊天成对对战评测仓（owner 给它起的外号）；既测裸大模型也测竞品/soliloquy装置；回放竞品台词盲判出BT榜
metadata: 
  node_type: memory
  type: project
  originSessionId: e880b644-17ae-42a9-a888-888faeef5f3c
---

**owner 叫它 anna**（说「anna 打分/anna 对战」= 用这套）。**路径 `~/Desktop/loop_project/co-model-eval-arena`**（Python，无 git——2026-07-12 已抹掉全部来源痕迹，来路别写回去）。三阶段成对对战：Phase1 对话生成（玩家模型代打 或 **replay 回放模式**=竞品聊天里用户台词当剧本逐轮喂被测端点，用户输入逐字相同才 apples-to-apples）→ Phase2 盲判（15 子维度=consistency/memory/writing 各 5，Model A/B 隐身份，每子维度×2 位置对调，[[A>>B]] 五档）→ Phase3 BT 排名出榜。细节地图=仓内 CLAUDE.md。

- **双用途定位**：裸模型评测 + 竞品/装置（harness）评测混赛；api_config.yaml 一个条目=一个参赛者（OpenRouter 直连 / localhost shim / 抓取转写）。
- **soliloquy 接入**：shim 在 [[soliloquy]] 仓 `scripts/eval-arena-shim/`（commit 1ddc4ea），`pnpm exec tsx scripts/eval-arena-shim/server.ts` 起本地 OpenAI 兼容端点（默认 8787），内部走生产 buildSystemPrompt(roleplay)+RP_PRESET+OpenRouter，key 自读 .env.local。
- **竞品内容工作流**：owner 抓 crushon 等聊天 md → `scripts/import_chat_md.py` 导入（认群卡/单卡两种导出）→ replay 配置跑三阶段。venv 在仓内 `.venv/`。
- ⚠ **judge 缺口**：soliloquy 的 OpenRouter key 调 anthropic/openai 全 403（只通 DeepSeek 系），smoke 裁判退化用 deepseek-v4-pro 有同族自偏；正式榜前要 owner 换/开权限一把跨族 key，judge 换回 gpt-5.2-chat 或 claude-sonnet-4.6。
- 首轮 smoke（2026-07-12，仅证管线）：crushon 50% vs soliloquy ~20%，裁判理由=情绪恢复太快/遣词套话/推进平。正式结论需 8-20 张卡 + 跨族 judge。
- 单轮接话质量另有轻量 eval 在 soliloquy 仓 `scripts/eval-engagement/`（四维绝对分），跟本仓多轮对战互补。
