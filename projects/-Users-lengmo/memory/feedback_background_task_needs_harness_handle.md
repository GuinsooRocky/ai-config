---
name: feedback_background_task_needs_harness_handle
description: 长跑后台任务必须用 Bash 的 run_in_background 起，别 nohup & 甩出去——否则 harness 无句柄、跑完永不通知 session
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 84931706-66f4-4cc7-9c09-d1c1dd6cfb59
  modified: 2026-07-20T12:49:26.599Z
---

起长跑任务（loop/批处理/监听）一律用 **Bash 工具的 `run_in_background: true`**，绝不自己写 `nohup ... &`。

**Why**：`nohup ... &` 会让进程认 PID 1 当爹、脱离会话，harness 手上零句柄 ⇒ 进程退出时**永远不会 re-invoke 当前 session**。表现＝任务默默跑完默默停，session 全程装死，owner 得反复问「现在第几轮」。2026-07-20 owner 报「近 10 次跑 loop 都不反馈」，查明就是这一行的锅（不是 loop.sh 的 bug——它本来就只有 PROGRESS.md + macOS 通知两个给人眼看的出口，从没有通往 session 的通道）。

**How to apply**：
- 起的时候就用 `run_in_background: true`，一步到位
- 已经用错姿势起了：别 kill 重起（丢当前进度），补一个 harness 托管的 pgrep 看门循环兜住
- 项目侧约定已落 `soliloquy/loop/README.md`（含轮数给满 20 的那条）

关联 [[project_soliloquy]] · [[feedback_inline_over_background_workflow]]
