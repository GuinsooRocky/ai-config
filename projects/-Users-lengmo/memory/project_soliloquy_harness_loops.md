---
name: project-soliloquy-harness-loops
description: soliloquy loop/graph 两条 codex 自主跑批线的机制状态：07-27 下午减法收官（B档四刀落 main），机制唯一真相=main，分支自拉
metadata: 
  node_type: memory
  type: project
  originSessionId: 33d05e57-453e-43d4-b428-dd0bee1a4d33
  modified: 2026-07-27T09:13:37.613Z
---

07-27 下午"双机制优化"收官（在凌晨机制修复 19956cf1/2023187a 之上做减法）：

- **机制唯一真相 = main**（owner 拍板：只动 main，loop/auto、graph/auto 自己拉 main 更新）。c35ba67e 之后 main 上机制已是最新版，"主仓 graph/ 旧引擎"问题自然消解。
- **B档四刀（main 4 commits，净 -6793/+574，未 push）**：队列三态→next/ 目录约定 `892b51db`（roll-batch 809→92 行；batchControl 保留 271→187，validateBatchManifest 有四处消费方）；close-batch 1018 行 ts→136 行 sh `5aee1592`（含新增 BACKLOG/DONE 对账闸，接 docs/prd/）；调度器降级顺序领取+skip阻断 `c3e5b194`（loop 317→126、graph 242→128）；机制测试摘出产品闸单开 `pnpm gate:harness` `4517c753`（真病根是 vitest node project 的 shared/** include，不是 ENGINEERING_GATE_SCOPE）。验收独立复跑全绿：tsc 0 错、gate:harness 92 用例、select-ready 契约实跑。
- **清扫已清**：3 个 run-b-* worktree+分支已删（孤儿 J3 产出先导 patch）；iter28/iter47/iter49 stash 导 patch 归档后 drop（H3/J3 均已重做）；**B26 stash 保留**（B26 从未重做）；slowloop 全线退役（launchd bootout、plist 入废纸篓——它 07-21 起每晚 exit 78 且含主动 push/clean -fd 危险路径）；loop 日志 282M→71M。清扫 commit 在 loop/auto `e9acc146`、graph/auto `f763730d`（落在"只动main"指令之前，owner 知情）。
- **八原则+close-batch.sh 已回写 dk/ralph 骨架并推 GitHub**（b7e8405/8e7295c，ralph/PRINCIPLES.md + ralph/close-batch.sh）。
- **三拍已落（07-27 晚）**：①graph-batch-b 40 件补账进 DONE.md（id+标题一行式，全文考古指向 graph/archive/，commit c9064825）——两线对账闸实跑均绿；②DONE 搬运口径确认软化版（该台账号本批全落终态且≥1完成才要求进 DONE，与 DONE.md"完工才整段搬"惯例一致，loop 线 T147 半程实跑不误红）；③graphRunnerGuard.test 已挪 shared/engineering（54e93c04，gate:harness 17文件/98用例）。
- **别动**：soliloquy-loop 工作树里 maintenanceTaskReadModel×5 + server/index.ts 未提交改动 = 当前批(剩7件)半途现场，续跑处理。

**Why**：图调度器喂的是 0 依赖边清单、三态审批防的是"自己偷改自己"、close-batch 覆盖的是没发生过的正常路径——复杂度没落在瓶颈（组批和对账台账）上。保留的红线：ALL_DONE 专用通道、postgres 能力探测三态、滑动窗口熔断、monitor 指数退避、绿闸单行、commit message 代交。

相关：[[project_soliloquy]]、[[feedback_loop_needs_backpressure_first]]
