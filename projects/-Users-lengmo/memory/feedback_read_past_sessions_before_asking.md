---
name: feedback-read-past-sessions-before-asking
description: owner 提到「之前说过/细节在别的会话」的事，先翻 claude+codex 会话记录再答，别让他重讲或给出和旧结论打架的建议
metadata:
  type: feedback
---

owner 指向过往上下文时（「我告诉过你」「细节在 codex 里」），先搜 `~/.claude/projects/-Users-lengmo/*.jsonl` 和 `~/.codex/sessions/**` 的近几天记录，读完再答。

**Why:** 2026-09-30 聊 Google 号停用：09-29 会话里原因、两次申诉、论坛 Diamond 专家「无升级渠道」都已讲清，我没翻就反复让他补原因、重复推论坛，被怼「告诉过你很多次了，信你还是信别人」。
**How to apply:** 搜法见 [[feedback-find-lost-things-fast]]（python 逐行 json 解析，只抽 user/assistant 文本）；答时先复述已知事实表明读过，再给增量判断；自己旧结论与 owner 听来的说法冲突时，分「可核实/不可核实」摆出来，不硬压。

**接手 codex 停下的活（2026-10-22 lich 实例）：** codex rollout 里只有 user/assistant 文本可读，子 agent 消息与部分工具参数是加密串（`gAAAA…`），看不到它验到哪一步。可靠现场是 `git worktree list` 找它的分支与未提交 diff，加上 `/private/tmp/<项目>-*` 下它留的临时验收脚本和 report.json（含 failure 字段）。它自报的「验收通过」要自己重跑，那次它的临时脚本其实卡在一个过期按钮名上。
