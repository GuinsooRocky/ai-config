---
name: co-model-eval-arena
description: anna=eval-arena（多轮RP成对对战评测 + soliloquy 的 B 端）；owner 说「B端」指它别听成「客户端」；施工单一真相=仓内 docs/prd/，Lab 接线真相=服务器 README
metadata:
  node_type: memory
  type: project
  originSessionId: e880b644-17ae-42a9-a888-888faeef5f3c
  modified: 2026-08-26T07:16:31.398Z
---

**owner 叫它 anna**。触发词：「anna」「arena 对战」「给竞品聊天打分」「跟 soliloquy 对战」。路径 `~/Desktop/loop_project/eval-arena`（git 仓，来源痕迹已抹、别写回去）。三阶段成对对战：Phase1 对话生成（玩家模型代打 或 replay 回放）→ Phase2 盲判（15 子维度、位置对调）→ Phase3 BT 排名。细节地图=仓内 CLAUDE.md。

## 它同时是 soliloquy 的 B 端（2026-08-16 确认）

**owner 说「B 端」「后台」「控制台」= eval-arena**（`apps/local_worker` 运营后台 / `apps/control-api` 云控制面 / `apps/admin` 网页后台 / `eval_arena` 评测）；soliloquy 仓是 C 端（Tauri 客户端 + 网站）。目标：B 端线上可用、好用、不依赖 owner 的 Mac。**语音转写里「弊端/B端/客户端」高度易混，拿不准当场问**——2026-08-15 把「B端」听成「客户端」整夜改错方向，owner 中途明说四次都没接住。别拿「相册导入 1215 张图」当 Lab 代表作（owner 说翻篇了）。

- B 端能力从 soliloquy 迁 eval-arena **已收官**（08-16 八批）：控制面=`apps/admin`（挂 control-api `/admin`）、运维脚本=`apps/ops`、契约=`packages/lab-contracts`；soliloquy 只留 C 端 + 权力通道（写口/鉴权真门/发版工具等留守）。台账=`~/.claude/plans/steady-stirring-llama-migration-batches.md`
- **云控制面已上线**：`https://soliloquy-lab-control.guinsoo.workers.dev/admin`（同域 `/console`=只读镜像、`/app`=薄摘要，别混）。**别再报「C1 未部署」**——报状态前先 curl/wrangler/ssh 实查，文档里的「未部署」常是过时快照
- Lab 读侧三进程 08-16 已迁 soliloquy VPS systemd；**Mac 不再起 worker/pusher（防双写）**，账本封存 `~/.local/share/eval-arena.migrated-20260816`。接线单一真相=服务器 `/home/lab/README.md`，部署盘点=仓内 `docs/deployment-status-2026-08-17.md`，**迁移期实测坑与未决项快照=仓内 `docs/lab-on-server-memo-2026-08-18.md`**（含两处「待 owner 拍」+「采集在 VPS 仍未成功一次，下次接手先查」）

## 评测侧要点

- **07-28 分期 PRD 已落仓**：`docs/prd/` = 施工单一真相，开工先读 `00-总纲-评测体系分期.md`；已长到 10 份（00 总纲 / 01-04 期1-期4 / 05 Lab 统一维护平台 / 06 群聊质量回归 / 07 流式首字速度与质量回归 / 08 多语言最短回复 / 09 新解锁的图收进相册），**份数以 `ls` 为准**。核心里程碑=期3 记忆三组对比 run（记忆开/关/全上下文）跑通后「记忆改版好坏」第一次可回答；期1 收口前任何榜单数字不当结论。期3 开工闸门（owner 侧）：soliloquy 迁移真库跑完、full-chain adapter 按 arena 契约实现、crushon 语料授权/脱敏
- 双用途：裸模型 + 竞品/装置混赛；api_config.yaml 一条目=一参赛者
- soliloquy 接入 shim 在 soliloquy 仓 `scripts/eval-arena-shim/`——⚠ prompt-only、长期记忆恒空，现在的 memory 分数测的是底模不是记忆系统，期3 换 full-chain adapter 才算数
- ⚠ judge：OpenRouter key 调 anthropic/openai 全 403 只通 DeepSeek；定版=三个异族中等模型投票（PoLL），不是换 key 用单强 judge
- 语料资产：`真实聊天/2026-07-28-crushon聊天记录/` 57 会话逐条真实时间戳 = 自己的 REALTALK（数据集本身不是参考素材）。单轮接话轻量 eval 另在 soliloquy 仓 `scripts/eval-engagement/`

相关裁定已收官：[[project_soliloquy_t158_memory_verdict]]（图谱不立项，工单三 bug 待 owner 拍）。
