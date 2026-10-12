---
name: co-model-eval-arena
description: anna=eval-arena（多轮RP成对对战评测 + soliloquy 的 B 端）；owner 说「B端」指它别听成「客户端」；施工单一真相=仓内 docs/prd/，Lab 接线真相=服务器 README
metadata:
  node_type: memory
  type: project
  originSessionId: e880b644-17ae-42a9-a888-888faeef5f3c
  modified: 2026-09-21T09:00:00.000Z
---

**owner 叫它 anna**。触发词：「anna」「arena 对战」「给竞品聊天打分」「跟 soliloquy 对战」。路径 `~/Desktop/loop_project/eval-arena`（git 仓，来源痕迹已抹、别写回去）。三阶段成对对战：Phase1 对话生成（玩家模型代打 或 replay 回放）→ Phase2 盲判（15 子维度、位置对调）→ Phase3 BT 排名。细节地图=仓内 CLAUDE.md。

## 它同时是 soliloquy 的 B 端（2026-08-16 确认）

**owner 说「B 端」「后台」「控制台」= eval-arena**（`apps/local_worker` 运营后台 / `apps/control-api` 云控制面 / `apps/admin` 网页后台 / `eval_arena` 评测）；soliloquy 仓是 C 端（Tauri 客户端 + 网站）。目标：B 端线上可用、好用、不依赖 owner 的 Mac。**语音转写里「弊端/B端/客户端」高度易混，拿不准当场问**——2026-08-15 把「B端」听成「客户端」整夜改错方向，owner 中途明说四次都没接住。别拿「相册导入 1215 张图」当 Lab 代表作（owner 说翻篇了）。

- B 端能力从 soliloquy 迁 eval-arena **已收官**（08-16 八批）：控制面=`apps/admin`（挂 control-api `/admin`）、运维脚本=`apps/ops`、契约=`packages/lab-contracts`；soliloquy 只留 C 端 + 权力通道（写口/鉴权真门/发版工具等留守）。迁移台账文件（原 `~/.claude/plans/steady-stirring-llama-migration-batches.md`）09-21 核已消失、去向没查到；八批结果以仓内 `docs/deployment-status-2026-08-17.md` 为准
- **云控制面已上线**：`https://soliloquy-lab-control.guinsoo.workers.dev/admin`（同域 `/console`=只读镜像、`/app`=薄摘要，别混）。**别再报「C1 未部署」**——报状态前先 curl/wrangler/ssh 实查，文档里的「未部署」常是过时快照
- Lab 读侧三进程 08-16 已迁 soliloquy VPS systemd；**Mac 不再起 worker/pusher（防双写）**，账本 `~/.local/share/eval-arena.migrated-20260816` 已随 09-10「本机退役清理」移除（7 项 3.61 GiB 进废纸篓、已清空），与服务器不同的 23 个差异文件留在 `~/.local/share/eval-arena-cleanup/20260910-161623/retained-local-history.tar.gz`（原路径见同目录 roots.json）；该清理 README 同样写明「不要重新启动已退役执行器，以免与服务器重复领任务」。接线单一真相=服务器 `/home/lab/README.md`，部署盘点=仓内 `docs/deployment-status-2026-08-17.md`，**迁移期实测坑与未决项快照=仓内 `docs/lab-on-server-memo-2026-08-18.md`**（含两处「待 owner 拍」+「采集在 VPS 仍未成功一次，下次接手先查」）

## 评测侧要点

- **07-28 分期 PRD 已落仓**：`docs/prd/` = 施工单一真相，开工先读 `00-总纲-评测体系分期.md`；已长到 16 份（09-21 `ls`：00–15，含两个 10- 开头；前 10 份为 00 总纲 / 01-04 期1-期4 / 05 Lab 统一维护平台 / 06 群聊质量回归 / 07 流式首字速度与质量回归 / 08 多语言最短回复 / 09 新解锁的图收进相册），**份数以 `ls` 为准**。核心里程碑=期3 记忆三组对比 run（记忆开/关/全上下文）跑通后「记忆改版好坏」第一次可回答；期1 收口前任何榜单数字不当结论。期3 开工闸门（owner 侧）：soliloquy 迁移真库跑完、full-chain adapter 按 arena 契约实现、crushon 语料授权/脱敏
- 双用途：裸模型 + 竞品/装置混赛；api_config.yaml 一条目=一参赛者
- soliloquy 接入 shim 在 soliloquy 仓 `scripts/eval-arena-shim/`——⚠ prompt-only、长期记忆恒空，现在的 memory 分数测的是底模不是记忆系统，期3 换 full-chain adapter 才算数
- ⚠ judge：OpenRouter key 调 anthropic/openai 全 403 只通 DeepSeek；定版=三个异族中等模型投票（PoLL），不是换 key 用单强 judge
- 语料资产：`真实聊天/2026-07-28-crushon聊天记录/` 57 会话逐条真实时间戳 = 自己的 REALTALK（数据集本身不是参考素材）。单轮接话轻量 eval 另在 soliloquy 仓 `scripts/eval-engagement/`

相关裁定已收官：[[project_soliloquy_t158_memory_verdict]]（图谱不立项，工单三 bug 待 owner 拍）。

## 2026-10 全量查 bug 与修复

131 条 finding 的结论在 `~/Desktop/loop_project/eval-arena-bugscan-20261002/FINAL.md`，修复收口在同目录 `fix/FIX_SUMMARY.md`（修了什么 / 待 owner 拍的 12 项 / 发版注意）。修复分支 `lengmo_20261003_fix_bugscan`（eval-arena）与 `lengmo_20261006_fix_observability`（soliloquy，含未执行迁移）已推 origin、未合 main、未部署。服务器实查（10-03）：worker/pusher disabled、内容命令通道与一键收录配着、`execution_enabled=true` 只差 `--execute`。接手先读 FIX_SUMMARY。
- **合同同步 SOP（10-12 实跑）**：干净 worktree 基于远端 main → `python3 scripts/sync_soliloquy_contracts.py --soliloquy-root <产品仓 main>` → `.venv/bin/python scripts/check_soliloquy_contract_drift.py` + `unittest -p test_soliloquy*` + `apps/ops pnpm check` + `apps/admin tsc/test/build` → 推 main，CI 自动发服务器与 Cloudflare（本机 GitHub 要开 7897 代理）；worktree 里把主仓 `.venv` 软链进来，tests 会按相对路径找 `.venv/bin/python`。

## 2026-10-12 第二轮全量查 bug（只查不修）

结论=`~/Desktop/loop_project/eval-arena-bugscan-20261012/FINAL.md`（61 条：P0 1 / P1 2 / P2 34 含 4 已修 / 潜伏 22；基线 main 9707439≈线上，main 后前进到 683f3f5 只改契约镜像）。**P0 正在线上发生**：域命令发件箱 `lab-control/control-plane-domain-commands/state.json` 的 lease_attempts 4097 条 > 4096 硬上限（`control_plane_domain_commands.py:671`），09-19 21:43 UTC 起内容命令通道每分钟失败、六域投影停更、后台命令建不出来；14321c2 救不了存量账本。止血=lab 身份手工截尾到最后 8 条（保末条 pending、不换 worker_ref、备份别硬链接），**等 owner 一句「修」**；代码修=`_load` 内存截尾+回归测试。哨兵 09-02 起 40 天零成功 pass。上一轮 PR #3 仍未合且与 main 冲突，130 条已知仍在线上。ssh 直连 `ssh -o ProxyCommand=none -p 22222 root@167.179.78.237`（Clash 没开时）。
