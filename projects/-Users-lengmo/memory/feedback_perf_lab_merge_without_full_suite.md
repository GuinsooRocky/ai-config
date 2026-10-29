---
name: feedback_perf_lab_merge_without_full_suite
description: perf-lab 小改（卡片文案、面板样式）合 main 不等 tests/all.mjs 全量，跑相关测试+反面验证就合；owner 说「直接合」就当场开 PR 自合
metadata:
  node_type: memory
  type: feedback
  originSessionId: ca565e64-d2f7-4676-85bf-27dad2c2dedb
  modified: 2026-10-29T12:40:44.193Z
---

crushon-ai-perf-lab 的仓内 CLAUDE.md 写着「提 PR 前跑 `node tests/all.mjs`」，但卡片文案、面板样式这类小改，owner 不要等全量（约 150 秒）再合：跑改到的那个测试文件（如 `node tests/notify.mjs`）＋换回 main 代码验反面，就开 PR 当场自合。

**Why:** 10-29 卡片加「内容变多」那行时，我在后台跑全量、说「跑完再合」，owner 回「用不了全量检查吧。。。 直接合」。当天还说过「直接合吧 都不用开pr了」——仓规不许直推 main，所以照旧开 PR 但当场自合，不等他点。

**How to apply:** 只改 `scripts/notify.mjs`、`scripts/panel.mjs` 文案或样式这类时，PR 描述写清跑了哪个测试文件、全量没跑（或跑完了就照实写）。改到比较、测量链路、登记表的仍按仓规跑全量。全局「验多少」规则见 ~/.claude/CLAUDE.md；相关 [[feedback_merge_without_owner_clickthrough]]。
