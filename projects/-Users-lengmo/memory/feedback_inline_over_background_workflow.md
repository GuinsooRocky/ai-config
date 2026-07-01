---
name: feedback-inline-over-background-workflow
description: 小的事实查询/单步活直接 inline 做，别开 background workflow（会空跑卡死、浪费几十分钟+token）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6d282902-a6aa-47b0-a5d2-ca193123dd4c
---

小的单步活（查一个事实、读几个文件、跑一条命令、一次 WebSearch）**直接 inline 做**，不要开 background workflow / Agent。

**Why**：2026-05-29 我为"查 SWE-bench Pro 是什么"开了个 2-agent 后台 research workflow，一个 agent 卡死，空跑 **51 分钟 / 59k token**，用户截图说"再空跑效率很低"。background workflow 没有 per-agent 超时，一卡就空转到天荒地老，看不见也省不下。

**How to apply**：
- background workflow / Agent 只用于**真正需要并行 fan-out 的大活**（多文件审、多源深调研、多候选 PK、大迁移）。
- 查一个事实、读几个文件、跑一条命令 → 直接 WebSearch / Read / Bash inline，自己控、看得见、随时停。
- 即使 ultracode "默认用 workflow"，小的单步查询仍走 inline——别为省事把小活塞进会挂死的后台。

相关：[[feedback_just_do_no_stop_suggestions]]
