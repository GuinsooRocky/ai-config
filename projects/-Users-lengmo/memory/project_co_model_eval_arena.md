---
name: co-model-eval-arena
description: anna=多轮RP聊天成对对战评测仓（owner 给它起的外号）；既测裸大模型也测竞品/soliloquy装置；07-28 起分期 PRD 落仓 docs/prd/ 为施工单一真相
metadata: 
  node_type: memory
  type: project
  originSessionId: e880b644-17ae-42a9-a888-888faeef5f3c
  modified: 2026-07-30T06:40:47.681Z
---

**owner 叫它 anna**。触发词：「anna」「arena 对战」「给竞品聊天打分」「跟 soliloquy 对战」= 用这套。**路径已迁 `~/Desktop/loop_project/eval-arena`**（07-28 起，旧 co-model-eval-arena 名作废；现在是 git 仓但来源痕迹已抹、别写回去）。三阶段成对对战：Phase1 对话生成（玩家模型代打 或 replay 回放=竞品用户台词逐字喂被测端点）→ Phase2 盲判（15 子维度、位置对调）→ Phase3 BT 排名。细节地图=仓内 CLAUDE.md。

- **07-28 分期 PRD 已落仓并提交（169b609）**：`docs/prd/` 五份（00 总纲+期1 信任地基/期2 档位阶梯/期3 记忆与时间/期4 优化闭环）= **施工单一真相，开工先读 00 总纲**；调研原文三份在 `~/Desktop/loop_project/`（现状侦察 fable / 整体思考 gpt / 78 篇论文对标 fable，不进仓）。核心里程碑=期3 三臂对比 run（记忆开/关/全上下文）跑通后「记忆改版好坏」第一次可回答，估距开工 4-6 周；期1 收口前任何榜单数字不当结论。
- 期3 开工闸门（owner 侧）：soliloquy 迁移真库跑完、full-chain adapter 按 arena 契约实现、crushon 语料授权/脱敏记录。
- **双用途定位**：裸模型 + 竞品/装置混赛；api_config.yaml 一条目=一参赛者。
- **soliloquy 接入**：shim 在 [[project_soliloquy]] 仓 `scripts/eval-arena-shim/`——⚠ prompt-only、长期记忆恒空（emptyMemory 写死），现在的 memory 分数测的是底模不是记忆系统，期3 换 full-chain adapter 才算数。
- ⚠ judge 缺口：OpenRouter key 调 anthropic/openai 全 403 只通 DeepSeek；**定版方案=三个异族中等模型投票（PoLL），不是换一把 key 用单强 judge**（期1 T1）。
- 语料资产：`真实聊天/2026-07-28-crushon聊天记录/` 57 会话逐条真实时间戳 = 自己的 REALTALK（挖记忆/时间/承诺三类探针 + 回来节奏模板），是数据集本身不是参考素材。
- 单轮接话轻量 eval 另在 soliloquy 仓 `scripts/eval-engagement/`，互补。
