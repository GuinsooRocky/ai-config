---
name: reference_rtk_is_third_party
description: RTK 是第三方工具 rtk-ai/rtk，非用户自有项目；本机仅预编译二进制无源码
metadata: 
  node_type: memory
  type: reference
  originSessionId: 443515de-f588-4ba6-bc19-7d8106d82508
---

RTK（Rust Token Killer）= 第三方开源工具 **`github.com/rtk-ai/rtk`**，**不是 lengmo 自己的仓**。本机只有预编译二进制 `~/.local/bin/rtk`（Mach-O arm64, v0.42.4，2026-06-18 从 0.38.0 升）经 curl install.sh 装（非 brew），升级=重跑 `curl -fsSL .../install.sh | sh`（管道会被 hook 搞坏，用绝对路径先落盘再 sh），**无源码** → 想改它只能 ① 提 upstream issue/PR，或 ② fork+clone+cargo build 自维护私 fork，**不能本地直接 edit**。

已知现有能力（strings 扒出）：`rtk learn`（从 CC error history 学 CLI 纠正，类似 headroom learn 用户已有）、`rtk proxy`（不过滤仅跟踪，逃生口但要重跑）、`rtk cache` **不存在**（无 CCR 可逆缓存）。

2026-06-18 已给上游提 CCR（Capture-Compress-Recall 可逆缓存）feature issue → [#2485](https://github.com/rtk-ai/rtk/issues/2485)，蹭 #1777（agent 缺信息重跑卡死，priority:high）。相关坑：#2148 rtk 现有缓存返回 stale 状态。用法痛点见 [[feedback_git_porcelain_with_rtk]] [[feedback_rtk_pipeline_corruption]]。
