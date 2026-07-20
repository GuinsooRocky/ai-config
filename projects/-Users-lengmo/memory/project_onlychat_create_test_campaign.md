---
name: project-onlychat-create-test-campaign
description: onlychat「Create 五大创建」component test 战役进度与续跑入口（worktree onlychat-create-test）
metadata: 
  node_type: memory
  type: project
  originSessionId: e1a98655-f407-4a08-98df-2abae18cf430
---

onlychat「Create 五大创建 component test」战役（创建+编辑全链路，233 条目 / ~1483 预估用例）。

**单一真相**：`~/Desktop/cmm/onlychat-create-test/docs/testing/create-component-test/`——`INVENTORY.md`（233 条清单+勾选状态）+ `HANDOFF.md`（交接：本轮战报/派工模板/下轮分组/从哪开始）。

**2026-07-10 停机状态**：50/233 ☑，voice/model/target-play/world 四域 P0 全清，720 用例×2 遍全绿 + tsc 零错 + 源码零改动，**未 commit**。worktree=`onlychat-create-test`，分支 `lengmo_20260710_test_create_component`（基 origin/develop）。

**2026-07-11 战役收官（233/233 全清）**：全部五域 P0+P1+P2 清零（character 72 · model 15 · target-play 24 · voice 36 · world 86）。收官三波并行 opus：Wave B（world P1 剩 16，7 agent，+16 文件/89 例）→ P2 W1（character 22+model 6，8 agent，+28 文件/137 例）→ P2 W2（target-play 7+voice 14+world 14，8 agent，+33 文件/138 例）。**最终验收=全量合跑 264 文件/2036 用例全绿 + tsc exit 0 + 源码零改动**（每波 per-file JSON reporter 逐一核数，无 mv 丢文件）。NoteTypeDefaultImage gap-fill 存量已盖无新增；target-play [game_play_id] 去重 1 文件覆 2 条目。**仍未 commit**（工作仓，用户没说提交就不提交）。

**已提交（2026-07-11，用户放行）**：分支 lengmo_20260710_test_create_component 3 commits（c20b1d7677 测试+docs / f0c81012d0 coverage include 五创建域+排除 *.md / 15c82292a0 docs），**ahead 3 未 push**（push 始终不主动）。⚠ **踩坑**：pre-commit husky lint-staged 跑 gts ESLint，测试文件 38 个非自动修复 error 挡住首 commit（no-var-requires/consistent-type-imports/rules-of-hooks，含前几波——全程只 vitest+tsc 从没跑过 gts lint）；5×opus 修完 vitest 仍绿再 commit 过。**教训升级：测试也要过 gts lint 别只 vitest+tsc**。666 prettier error 由 hook prettier--write 自动修。

**收官剩余（待用户拍板）**：①fresh-context 复核（可选，已 per-file 核过）②源码债清单开不开修复单（全记 INVENTORY ⚠，最关键=NoteEditor.pc.tsx:140 inert 升 React19 静默丢防护归 next16）③push。全清单在 HANDOFF「✅ 收官后续」节。

**踩坑教训（保留）**：agent 别 mv 自己产出（第八波栽过丢文件）；主对话勾选前必须 per-file JSON reporter 核用例数别只看总绿；RSC 测法=await Page({params})（params 同步 Next13，多数 page 未 import notFound=结构性保证）。

工作法遵循 [[feedback-delegate-impl-to-opus-subagent]]（并行 opus 扇出、主对话只编排验收）；派工模板与硬技法全在 HANDOFF.md 第四节，别重新发明。
