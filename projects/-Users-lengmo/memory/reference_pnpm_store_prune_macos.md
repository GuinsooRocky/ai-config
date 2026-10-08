---
name: pnpm-store-prune-macos-wipes-all
description: macOS 上 `pnpm store prune` 会把整个 store 当无引用清空（APFS clone 非硬链接），清缓存时别跑它
metadata:
  type: reference
---

2026-10-08 电脑体检清缓存时跑了 `pnpm store prune`：`~/Library/pnpm/store/v10` 1.0G → 12K，连 soliloquy 正在用的包都删了。原因推测是 macOS/APFS 上 pnpm 用 clone（写时复制）往 node_modules 放独立副本而非硬链接，prune 按链接数判「无引用」→ 全删。

**后果**：项目 node_modules 完好照常跑；只是下次 `pnpm install` 必须联网重下，离线装失效。不可恢复。

**How to apply:** 清 pnpm 缓存别用 `store prune`；要省空间就整个挪旧版 store（如 `store/v3`）进 ~/.Trash，或干脆不动。相关：[[feedback_cleanup_use_trash_not_rm]]
