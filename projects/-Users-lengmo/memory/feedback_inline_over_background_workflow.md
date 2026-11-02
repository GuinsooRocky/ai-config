---
name: feedback-inline-over-background-workflow
description: 小的事实查询/单步活直接 inline 做，别开 background workflow（会空跑卡死、浪费几十分钟+token）；按名发射 workflow 前先看脚本配置块——args 不一定被脚本消费，残留写死配置会整轮跑错；长跑后台任务（loop/批处理）用 Bash run_in_background 起、别 nohup & 甩出去，并当场挂 Monitor 实时报；但进程已有守护脚本的（dev server / watchdog）绝不外挂——已复发三次
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6d282902-a6aa-47b0-a5d2-ca193123dd4c
  modified: 2026-11-02T07:52:45.093Z
---

小的单步活（查一个事实、读几个文件、跑一条命令、一次 WebSearch）**直接 inline 做**，不要开 background workflow / Agent。

**Why**：2026-05-29 我为"查 SWE-bench Pro 是什么"开了个 2-agent 后台 research workflow，一个 agent 卡死，空跑 **51 分钟 / 59k token**，用户截图说"再空跑效率很低"。background workflow 没有 per-agent 超时，一卡就空转到天荒地老，看不见也省不下。

**How to apply**：
- background workflow / Agent 只用于**真正需要并行 fan-out 的大活**（多文件审、多源深调研、多候选 PK、大迁移）。
- 查一个事实、读几个文件、跑一条命令 → 直接 WebSearch / Read / Bash inline，自己控、看得见、随时停。
- 即使 ultracode "默认用 workflow"，小的单步查询仍走 inline——别为省事把小活塞进会挂死的后台。

相关：[[feedback_owner_decision_interaction]]


补充：会空跑卡死，2026-05-29 空转51min

## 按名发射 workflow 先核配置块

按名字发射已保存的 workflow（`Workflow({name})`）前，必须先看脚本头部的配置块：很多脚本的目标（仓库路径/scope）写死在常量里、约定由上游 skill 发射前 Edit，`args` 只是给评审员的补充文本，**不会自动覆盖配置**。

**Why:** 2026-07-29 按名发射 pr-audit 审 onlychat PR #1275，脚本残留上次 mk 的写死配置，22 个 agent、139 万 token 全烧在错误仓库上，用户质问"这算你浪费我的 token 吗"。

**How to apply:** 发射前 grep 脚本的 `const` 配置块核对目标；pr-audit 已加 args 保险丝（args 带绝对路径即覆盖，claude-config 57ebe3f），其他 workflow 未必有。

## 长跑要挂 Monitor 报主对话

起了长跑后台任务（loop.sh、批处理、多轮脚本）就**当场挂 Monitor 把每轮进度打回主对话**，不要问"要 A 我不报 / B 我实时报"。用户已经因为这个问题被问了无数次（2026-07-21 原话「这个问题你问了我无数次」）。

**Why**：`run_in_background` 的 Bash 任务只在**整个进程退出**时才通知我，50 轮的 loop 在 harness 眼里是一个任务 ⇒ 中间几小时主对话完全静默。用户以为脚本天然会往对话里挂，实际不会。他要的是"离开电脑、回来看这个对话就知道全貌"。

**How to apply**：
- 用 `Monitor` + `persistent: true`（长跑要 session 级，别用默认 5 分钟 timeout）
- 事件源用脚本自己的人话流水文件（如 `loop/PROGRESS.md`）轮询新增行，别 tail 原始日志
- **必须覆盖失败面**：进程死了要发一条终止事件并 break——否则"崩了"和"还在跑"在对话里长得一模一样（这正是停掉的看板骗人的同一个病，见 [[project_soliloquy]] 的 board.sh）
- 长行 `cut -c1-400` 截断控 token
- 别自己 sleep 轮询（harness 会拦），也别为省事只报成功

**起法：必须用 Bash 的 `run_in_background`，别 `nohup ... &` 甩出去**（2026-07-20 立法）——`nohup ... &` 会让进程认 PID 1 当爹、脱离会话，harness 手上零句柄 ⇒ 进程退出时**永远不会 re-invoke 当前 session**。表现＝任务默默跑完默默停、session 全程装死，owner 得反复问「现在第几轮」。当日 owner 报「近 10 次跑 loop 都不反馈」，查明就是这一行的锅（不是 loop.sh 的 bug——它本来就只有 PROGRESS.md + macOS 通知两个给人眼看的出口，从没有通往 session 的通道）。**起的时候就写 `run_in_background: true`，一步到位**；已经用错姿势起了就别 kill 重起（丢当前进度），补一个 harness 托管的 pgrep 看门循环兜住。项目侧约定已落 `soliloquy/loop/README.md`（含轮数给满 20 的那条）。

**不适用：已有专职守护脚本的进程**（⚠ 已复发三次，起 dev 时把这条当硬闸：**手一碰 dev-watchdog.sh 就禁止再想 Monitor**，别等挂完才想起例外）。本条只管「我自己起的、没人管的」长跑任务。若该进程已有 owner 脚本在守（典型：`~/.local/bin/dev-watchdog.sh` 托管 :3000 dev server —— 自带内存阈值重启、HTTP 探活、崩溃拉起，状态写 `/tmp/onlychat-dev-<port>.json`），**别再外挂 Monitor**：要状态就读它的状态文件。2026-07-28 在 onlychat 挂了一次，三轮全是我 grep 关键词写错的误报（`tail` 多文件表头 `==> …watchdog… <==` 命中关键词、node_modules 里 node-fetch 的 `encoding` 老警告命中 `Module not found`），用户直接顶「监控这些事情交给脚本不好吗」。判据：动手前先问**这进程有没有 owner**，有就别重复造轮子。**2026-08-06 复发**：世界卡动效 session 里对 :3000 dev server 连挂 8 轮 Monitor（每次 OOM 重启就再挂一个），被顶「是有脚本的不需要session监听」——dev server 永远适用本例外，OOM 重启后只重启进程、不挂监听。**2026-08-14 三度复发**：onlychat 主仓起 dev 时又挂了一轮，还因为脚本重复吐同一行日志停掉重挂了一次（噪音全是我自己造的），被顶「不要一直做监听的活 我有脚本的」。

相关：本文件开头（该不该开后台：小活直接 inline）、[[feedback_owner_decision_interaction]]（带一个推荐直接走，别列 A/B）
