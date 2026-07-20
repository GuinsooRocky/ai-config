---
name: feedback_truncated_output_is_not_ground_truth
description: 拿 | head 截断的输出当全量事实下结论 —— 要么去掉截断，要么先 --count 拿总数
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f2f56a2d-9fa8-4b35-961a-fc457b37287c
---

**任何要拿来下结论的命令输出，不能带 `| head` / `| tail` / `-5` 之类的截断。** 截断只用于「瞄一眼长什么样」；一旦这个输出要变成判断依据，先拿总数（`--count` / `wc -l`），或者干脆全量落盘再读。

```bash
git rev-list --count A..B        # 先要总数，再决定要不要看明细
git log --oneline A..B | wc -l
git diff --stat A B              # 文件级规模，一眼看出量级对不对
```

**Why**：2026-07-17 onlychat banner 发版，`git log v6.27.0..adfd435b77 | head` 吐了 10 条，我就当成「hotfix.0 = v6.27.0 + 10 个小修」，据此向 owner 喊「你的包丢了 7 个提交、线上可能回退」。实际 `git rev-list --count` = **93 个**。是 `| head` 截的，不是真的只有 10 个。同一天早些时候还用 `git branch --contains` 对 owner 报过另一个假警报（见 [[feedback_git_contains_misses_cherrypick]]）——两次同一个毛病：**拿一个查不全的输出下确定性结论**。owner 最后说「你打你的tag 管他们做什么」，是我把发版流程搅进了自己造的迷雾里。

**How to apply**：警报级结论（「线上要回退」「丢了改动」「夹带了别人的东西」）的门槛要比日常高一档——下结论前问自己「这个数字/列表是完整的吗，我怎么知道」。量级校验最省事：`git diff --stat` 一跑，625 files / 97k lines 立刻说明「这不是 10 个小修」，比逐条读 log 快得多也难骗。同源原则见 [[feedback_verify_capture_not_status]]、[[feedback_rtk_pipeline_corruption]]（管道摘要不可信，落盘复核）。
