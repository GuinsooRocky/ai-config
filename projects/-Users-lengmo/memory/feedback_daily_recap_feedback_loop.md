---
name: feedback_daily_recap_feedback_loop
description: "daily-recap 自动化后的反馈方式——\"今日总结反馈 xxx\"消化进 skill；\"清掉反馈\"删流水账"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1cc6bcf6-c730-45e8-a4ad-ca13b7e307eb
---

daily-recap 已转无人值守 cron（见 [[project_daily_recap_automation]]），不再每日人工调稿、**不要做 promote/喂回样本的命令**。反馈走口头：

- 用户说「**今日总结反馈 xxx**」（一长串自然语言纠正）→ 我负责当场把它消化进 skill：改 `SKILL.md` 规则，或顺手修一份 `ref/samples/` 样本。用户只管说，不管存哪。
- 同时把这次反馈追加一笔到 `~/.claude/skills/daily-recap/ref/feedback-log.md`（带日期 + 我改了啥）当流水账。
- 用户说「**清掉反馈**」（预计十几轮、输出合格后）→ 删掉 `feedback-log.md`。

**Why:** 用户的心智模型是「反馈是临时的，skill 收敛后就删」。删流水账安全的前提是——真正的学习当场就焊进了 SKILL.md/样本，流水账只是历史记录，不是 skill 的活输入。

**How to apply:** 收到「今日总结反馈」先落 SKILL.md/样本（durable），再记流水账（可弃）；别只记流水账就完事，否则用户删了就丢了。
