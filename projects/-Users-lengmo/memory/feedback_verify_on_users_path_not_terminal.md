---
name: feedback-verify-on-users-path-not-terminal
description: 我在终端里验通了 ≠ 用户点按钮那条路径能通；环境差异要在用户的入口上验
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 39810fa3-fe16-4e9d-bc8b-4707d657306e
  modified: 2026-08-27T18:00:25.528Z
---

交付「用户点一下就跑」的东西时，**在终端里跑通不算验证**。必须在用户真正的
入口上验（URL Handler / launchd / 服务进程），因为那条路径的环境是另一套。

**Why**：2026-08-27 收图按钮，一晚上三次「终端里通、按钮那条路径不通」，每次
我都以为补完了：
1. `PATH` 里没有 node（nvm 装的）→ 点了没反应
2. 没有 `NODE_EXTRA_CA_CERTS` → 一句没线索的「快照读失败」
3. 没有代理变量，且 **Node 的 fetch 默认不认 `http_proxy`**（要 `NODE_USE_ENV_PROXY`）
   → 领任务就崩，云端一个字都收不到

第 3 条还有更深一层：python 起 adapter 子进程时 `runtime_env` 是白名单式的，
上层辛苦导出的代理到那一层又被丢干净。**每多一层进程边界，就多一次环境被剥光
的机会。**

**How to apply**：
- 用 `env -i HOME=... PATH=/usr/bin:/bin` 模拟空环境跑一遍，别用自己的 shell
- 跨进程边界时查白名单（`env=`、`runtime_env=` 这类字典），别假设变量会传下去
- 判断「真的走代理了吗」用 `lsof -nP -p <pid> -i` 看 socket 打到哪，
  不看「跑得快了」——快慢会骗人
- 相关：[[feedback_gates_must_fail_on_purpose]]、[[feedback_truncated_output_is_not_ground_truth]]
