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

## 2026-10-12 第二轮全量查 bug + 10-13 修复（owner 全权委托「你觉得对的就修」）

结论=`~/Desktop/loop_project/eval-arena-bugscan-20261012/FINAL.md`（61 条），修复回执=同目录 `fix/FIX_SUMMARY.md`，发版手顺=`fix/RELEASE_HANDBOOK.md`，过程账=`STATUS.md`。
- **线上两层 P0 已手工止血并自愈**（10-12 17:09 截尾域命令发件箱 lease_attempts 4097→8；18:05 置空投影账本 records 走 sequence-stale 自愈，18:10 proj_age=0）。根因：①`control_plane_domain_commands.py:671` 4096 硬上限、写入侧 model_copy 不校验；②d49233f 给 `DomainProjectionV1` 加必填 total_count/truncated 无存量迁移。备份在服务器 `manual-backups/20261013-*`。
- **main 已含全部修复**：PR #4 合并提交 721175d（= PR #3 的 130 条 + 本轮 9 路，每路独立审查实跑红→绿）；release_check 14/14 绿。**未发版**：带 D1 迁移 0047/0048/0049（不可逆），接收器拒自动发布；本机 wrangler 登录已过期，迁移要在服务器以 lab 身份用 release-wrangler.toml 跑；发版走「先 ff 服务器仓再走接收器同 SHA 分支，空闲时重启 tasks」，全在 RELEASE_HANDBOOK。owner 不拍板，由我裁决今晚不发（线上已自愈、凌晨手工迁移风险>收益）。
- 生产可见变化（发版后）：默认每日额度 215→190、/app 退出登录、失败命令重发回真实状态、手工入库 CLI --occurred-at 必填。
- ssh 服务器：Clash 没开时 `ssh -o ProxyCommand=none -p 22222 root@167.179.78.237`；只读诊断用 lab 身份跑仓内 store API（手顺在 fix/reports/R1.md）。
- 教训：严格 pydantic 模型加必填字段/上限而不测「存量账本读回」= 本轮两起 P0 同形（14321c2、d49233f 的测试都只从空账本起步）；全仓同形排查已做（仅此 1 处落盘）。
